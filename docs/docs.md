# About cefrpy

The cefrpy python module offers a comprehensive toolkit for analyzing linguistic data based on the Common European Framework of Reference for Languages (CEFR).

# Installation

You can install `cefrpy` for Python >= 3.6 via pip:

```bash
pip install cefrpy
```

# Usage examples

## Getting part of speech level of a word

```py
from cefrpy import CEFRAnalyzer

analyzer = CEFRAnalyzer()

word = "happy"
pos_tag = "JJ"  # Adjective
level = analyzer.get_word_pos_level_float(word, pos_tag)
if level is not None:
    print(f"The level of '{word}' as a {pos_tag} is: {level}")
else:
    print(f"Level not found for '{word}' a {pos_tag}.")


# You can also get the level in CEFR format
cefr_level = analyzer.get_word_pos_level_CEFR(word, pos_tag)
if cefr_level is not None:
    print(f"The CEFR level of '{word}' as a {pos_tag} is: {cefr_level}")
else:
    print(f"CEFR level not found for '{word}' as a {pos_tag}.")
```

## Getting average level of a word:

```py
from cefrpy import CEFRAnalyzer

analyzer = CEFRAnalyzer()

word = "supremacy"
average_level = analyzer.get_average_word_level_float(word)
if average_level is not None:
    print(f"The average level of '{word}' is: {average_level}")
else:
    print(f"Average level not found for '{word}'.")


# You can also get the average level in CEFR format
cefr_average_level = analyzer.get_average_word_level_CEFR(word)
if cefr_average_level is not None:
    print(f"The CEFR average level of '{word}' is: {cefr_average_level}")
else:
    print(f"CEFR average level not found for '{word}'.")
```

## Recommended usage with [spaCy](https://spacy.io)

### Import spacy and load model:
```py
import spacy

from cefrpy import CEFRSpaCyAnalyzer, CEFRLevel

nlp = spacy.load("en_core_web_sm")
```

### Analyze any text

Optionally supports custom abbreviation mapping and exclusion of specific [spaCy](https://spacy.io) entity types (such as names of people, languages, countries, cities, etc.) from CEFR level matching.

```py
# Source: ChatGPT 3.5
text = """
In the heart of every forest, a hidden world thrives among the towering trees. Trees, 
those silent giants, are more than just passive observers of nature's drama; they are 
active participants in an intricate dance of life.

Did you know that trees communicate with each other? It's not through words or gestures 
like ours, but rather through a complex network of fungi that connect their roots 
underground. This network, often called the "wood wide web," allows trees to share 
nutrients, water, and even warnings about potential threats.

But trees are not just generous benefactors; they are also masters of adaptation. Take 
the mighty sequoias, for example, towering giants that have stood the test of time for 
thousands of years. These giants have evolved thick, fire-resistant bark to withstand 
the frequent wildfires of their native California.

And speaking of longevity, did you know that some trees have been around for centuries, 
witnessing history unfold? The ancient bristlecone pines of the American West, for 
instance, can live for over 5,000 years, making them some of the oldest living organisms 
on Earth.

So the next time you find yourself wandering through a forest, take a moment to appreciate 
the remarkable world of trees. They may seem like silent spectators, but their lives are 
full of fascinating stories waiting to be discovered.
"""

ABBREVIATION_MAPPING = {
    "'m": "am",
    "'s": "is",
    "'re": "are",
    "'ve": "have",
    "'d": "had",
    "n't": "not",
    "'ll": "will"
}

# Optional. List of all possible spaCY entity types:
# 'CARDINAL', 'DATE', 'EVENT', 'FAC', 'GPE', 'LANGUAGE', 'LAW', 'LOC', 'MONEY',
# 'NORP', 'ORDINAL', 'ORG', 'PERCENT', 'PERSON', 'PRODUCT', 'QUANTITY', 'TIME',
# 'WORK_OF_ART'
ENTITY_TYPES_TO_SKIP_CEFR = {
    'QUANTITY', 'MONEY', 'LANGUAGE', 'LAW',
    'WORK_OF_ART', 'PRODUCT', 'GPE',
    'ORG', 'FAC', 'PERSON'
}

doc = nlp(text)
text_analyzer = CEFRSpaCyAnalyzer(entity_types_to_skip=ENTITY_TYPES_TO_SKIP_CEFR, abbreviation_mapping=ABBREVIATION_MAPPING)
tokens = text_analyzer.analize_doc(doc)

print('-' * 55)
print(f' {"WORD".ljust(26)}\tPOS\tLEVEL\tCEFR')
print('-' * 55)
for token in tokens:
    word, pos, is_skipped, level, _, _ = token
    print(f'{word.ljust(26)}\t{pos}\t{"Skip" if is_skipped else "{:.2f}".format(level)}\t{CEFRLevel(round(level)) if level else None}')

```

Result (truncated):

```
-------------------------------------------------------
 WORD                      	POS	LEVEL	CEFR
-------------------------------------------------------
                          	_SP	Skip	None
In                        	IN	1.00	A1
the                       	DT	1.00	A1
heart                     	NN	1.00	A1
of                        	IN	1.00	A1
every                     	DT	1.00	A1
forest                    	NN	2.00	A2
,                         	,	Skip	None
a                         	DT	1.00	A1
hidden                    	JJ	3.00	B1
world                     	NN	1.00	A1
thrives                   	VBZ	5.86	C2
among                     	IN	2.00	A2
the                       	DT	1.00	A1
towering                  	VBG	1.00	A1
trees                     	NNS	1.00	A1
.                         	.	Skip	None
Trees                     	NNS	1.00	A1
,                         	,	Skip	None
                          	_SP	Skip	None
those                     	DT	1.00	A1
silent                    	JJ	3.00	B1
```

### Get more statistical information

1. Filter tokens by level:

```py
def filter_for_desired_level(level_tokens: list[tuple[str, str, bool, float, int, int]],
                            min_level: float | int = 1.0, max_level: float | int = 6.0
                            ) -> set[tuple[str, str, bool, float, int, int]]:
    filtered_tokens = set()
    for token in level_tokens:
        level = token[3]

        if level and level >= min_level and level <= max_level:
            filtered_tokens.add(token)

    return filtered_tokens


# You can also set min/max level as an int or float in range from 1 to 6
desired_min_level = CEFRLevel.C1
desired_level_words_set = filter_for_desired_level(tokens, min_level=int(desired_min_level))

desired_level_words_list = list(desired_level_words_set)
desired_level_words_list.sort()

print(f'\tWords with level {desired_min_level} and higher: {len(desired_level_words_list)}')
for word_data in desired_level_words_list:
    word, pos, _, level, _, _ = word_data
    print(f"{word.ljust(26)} {pos.ljust(6)} {'{:.2f}'.format(level).ljust(6)} {CEFRLevel(round(level))}")
```

```
Words with level B2 and higher: 16
benefactors                NNS    6.00   C2
bristlecone                NN     6.00   C2
evolved                    VBN    4.00   B2
fungi                      NNS    5.20   C1
living                     NN     4.00   B2
longevity                  NN     5.96   C2
masters                    NNS    4.00   B2
mighty                     JJ     4.00   B2
observers                  NNS    4.00   B2
pines                      NNS    4.00   B2
potential                  JJ     4.00   B2
sequoias                   NNS    6.00   C2
thrives                    VBZ    5.86   C2
underground                RB     4.00   B2
wildfires                  NNS    6.00   C2
withstand                  VB     5.12   C1
```

2. Get CEFR statistic of the text:

```py
def get_word_level_count_statistic(level_tokens: list[tuple[str, str, bool, float, int, int]]) -> list[int]:
    difficulty_levels_count = [0] * 6
    for token in level_tokens:
        level = token[3]
        if not level:
            continue

        level_round = round(level)
        difficulty_levels_count[level_round - 1] += 1

    return difficulty_levels_count

difficulty_levels_count = get_word_level_count_statistic(tokens)
print('CEFR statistic (total words):')
for i in range(1, 7):
    print(f'{CEFRLevel(i)}: {difficulty_levels_count[i - 1]}')
```

```
CEFR statistic (total words):
A1: 136
A2: 36
B1: 27
B2: 11
C1: 2
C2: 6
```

3. Get CEFR statistic for unique words in the text:

```py
def get_word_level_count_statistic_unique(level_tokens: list[tuple[str, str, bool, float, int, int]]) -> list[int]:
    processed_word_pos_set = set()
    difficulty_levels_count = [0] * 6
    for token in level_tokens:
        level = token[3]
        if not level:
            continue

        to_check_tuple = (token[0], token[1])
        if not to_check_tuple in processed_word_pos_set:
            level_round = round(token[3])
            difficulty_levels_count[level_round - 1] += 1
            processed_word_pos_set.add(to_check_tuple)

    return difficulty_levels_count


difficulty_levels_count_unique = get_word_level_count_statistic_unique(tokens)
print('CEFR statistic (unique words):')
for i in range(1, 7):
    print(f'{CEFRLevel(i)}: {difficulty_levels_count_unique[i - 1]}')
```

```
CEFR statistic (unique words):
A1: 77
A2: 33
B1: 23
B2: 11
C1: 2
C2: 6
```

4. Get set of not found CEFR levels for words in text:

```py
def get_not_found_words(level_tokens: list[tuple[str, str, bool, float, int, int]]) -> set[str]:
    not_found_words = set()
    for token in level_tokens:
        if token[2]:
            continue

        if not token[3]:
            not_found_words.add(token[0])

    return not_found_words


not_found_words_set = get_not_found_words(tokens)
not_found_words_list = list(not_found_words_set)
not_found_words_list.sort()

print('Not found words:', len(not_found_words_list))
if len(not_found_words_list):
    print('\n'.join(not_found_words_list))
```

```
Not found words: 0
```

# Additional features

## Get all possible part-of-speech tags for a word

```py
from cefrpy import CEFRAnalyzer

analyzer = CEFRAnalyzer()

print(analyzer.get_all_pos_for_word("test")) # [<POSTag.JJ: 4>, <POSTag.NN: 8>, <POSTag.VB: 19>]
print(analyzer.get_all_pos_for_word_as_str("test")) # ['JJ', 'NN']

# {<POSTag.JJ: 4>: <CEFRLevel.A2: 2>, <POSTag.NN: 8>: <CEFRLevel.A1: 1>, <POSTag.VB: 19>: <CEFRLevel.B2: 4>}
print(analyzer.get_pos_level_dict_for_word("test"))

# {'JJ': 2.5, 'NN': 1.0, 'VB': 4.0}
print(analyzer.get_pos_level_dict_for_word("test", pos_tag_as_string=True, word_level_as_float=True))
```

## Checking if a word exists in the database

```py
from cefrpy import CEFRAnalyzer

analyzer = CEFRAnalyzer()

word = "apple"
if analyzer.is_word_in_database(word):
    print(f"'{word}' exists in the database.")
else:
    print(f"'{word}' does not exist in the database.")
```

## Checking if a word with a specific part-of-speech exists in the database

```py
from cefrpy import CEFRAnalyzer

analyzer = CEFRAnalyzer()

word = "run"
pos_tag = "VB"  # Verb
if analyzer.is_word_pos_id_database(word, pos_tag):
    print(f"'{word}' with part of speech '{pos_tag}' exists in the database.")
else:
    print(f"'{word}' with part of speech '{pos_tag}' does not exist in the database.")
```

## POSTag usage examples

```py
from cefrpy import POSTag

# Get list of all part-of-speech tag names
print(POSTag.get_all_tags()) # ['CC', 'CD', 'DT', ...]

# Print total tags
print(POSTag.get_total_tags()) # 28

# Get description for a tag
print(POSTag.get_description_by_tag_name('NN')) # Noun, singular or mass

tag = POSTag.VB
print(tag)                          # VB
print(POSTag.get_description(tag))  # Verb, base form
print(int(tag))                     # 19 (unique tag id)
print(tag == POSTag.NN)             # False
```

## CEFRLevel usage examples

```py
from cefrpy import CEFRLevel

level = CEFRLevel.A1
print(level)            # A1
print(int(level))       # 1

level2 = CEFRLevel.C2
print(level2)           # C2
print(int(level2))      # 6

# You can perform any comparisons:
print(level2 > level)   # True
print(level2 == level)  # False

print(CEFRLevel.from_str("B1") == CEFRLevel.B1) # True
print(CEFRLevel.from_str("B1") == CEFRLevel(3)) # True
```

## Yields CEFRAnalyzer methods

For every example you should import and initialize `CEFRAnalyzer`:

```py
from cefrpy import CEFRAnalyzer

analyzer = CEFRAnalyzer()
```

### Iterating over words with a specific length (alphabetical order)
```py
iteration_limit = 10
word_list = []
for word in analyzer.yield_words_with_length(6):
    if iteration_limit == 0:
        break
    word_list.append(word)
    iteration_limit -= 1

# ['aaberg', 'aachen', 'aahing', 'aargau', 'aarhus', 'abacus', 'abadan', 'abadia', 'abakan', 'abaris']
print(word_list)
```

### Iterating over words with a specific length (reversed alphabetical order)

```py
iteration_limit = 10
word_list = []
for word in analyzer.yield_words_with_length(6, reverse_order=True):
    if iteration_limit == 0:
        break
    word_list.append(word)
    iteration_limit -= 1

# ['zymase', 'zygote', 'zygoma', 'zydeco', 'zwolle', 'zwicky', 'zuzana', 'zusman', 'zurvan', 'zurich']
print(word_list)
```

### Iterating over words in alphabetical order

```py
iteration_limit = 10
word_list = []
for word in analyzer.yield_words():
    if iteration_limit == 0:
        break
    word_list.append(word)
    iteration_limit -= 1

# ['a', 'aa', 'aaa', 'aaaa', 'aaas', 'aaberg', 'aachen', 'aae', 'aaee', 'aaf']
print(word_list)
```

### Iterating over words with their pos in alphabetical order with word length priority ascending

```py
iteration_limit = 6
word_pos_list = []
for word, pos_tag in analyzer.yield_word_pos(word_length_sort=True):
    if iteration_limit == 0:
        break
    word_pos_list.append((word, pos_tag))
    iteration_limit -= 1

# [('a', <POSTag.DT: 2>), ('a', <POSTag.IN: 3>), ('a', <POSTag.JJ: 4>), ('a', <POSTag.NN: 8>), ('a', <POSTag.VB: 19>), ('b', <POSTag.JJ: 4>)]
print(word_pos_list)
```

### Iterating over words with their pos as str and levels as float in reversed alphabetical order with word length priority descending 

```py
iteration_limit = 3
word_pos_list = []
for word, pos_tag, level in analyzer.yield_word_pos_level(word_length_sort=True, reverse_order=True, pos_tag_as_string=True, word_level_as_float=True):
    if iteration_limit == 0:
        break
    word_pos_list.append((word, pos_tag, level))
    iteration_limit -= 1

# [('demethylchlortetracycline', 'NN', 6.0), ('electrocardiographically', 'RB', 6.0), ('polytetrafluoroethylene', 'NN', 6.0)]
print(word_pos_list)
```


# License
This project is licensed under the MIT License - see the LICENSE file for details.

# Acknowledgments
I would like to acknowledge the contributions of the following resources. I used them to create my initial SQLite version [Words-CEFR-Dataset](https://github.com/Maximax67/Words-CEFR-Dataset):
- [Spacy](https://spacy.io/)
- [CEFR-J](https://cefr-j.org/)
- [LemmInflect](https://github.com/bjascob/LemmInflect)
- [The Google Books Ngram Viewer (used 1-grams dataset, version 20200217)](https://books.google.com/ngrams/)
- [List of pos tags form Penn Treebank Project](https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html)

Also I used these resources to create my [valid English words list](https://github.com/Maximax67/English-Valid-Words):
- [Word list by infochimps (archived)](https://web.archive.org/web/20131118073324/https://www.infochimps.com/datasets/word-list-350000-simple-english-words-excel-readable)
- [English words github repo by dwyl](https://github.com/dwyl/english-words)
- [NLTK (Natural Language Toolkit)](https://www.nltk.org/)
- [WordNet](https://wordnet.princeton.edu/)
