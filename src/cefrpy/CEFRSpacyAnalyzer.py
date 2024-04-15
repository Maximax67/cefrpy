from typing import Iterator

from typing import Union

from .CEFRAnalyzer import CEFRAnalyzer

class CEFRSpaCyAnalyzer():
    """
    Analyze text for CEFR levels, considering provided entity types to skip and abbreviation mapping.

    Attributes:
        _analyzer (CEFRAnalyzer): The CEFR analyzer instance.
        entity_types_to_skip (set[str]): Set of entity types to skip.
        abbreviation_mapping (dict[str, str]): Dictionary mapping abbreviations to their full forms.
        tokens (list[tuple[str, str, bool, float, int, int]]): List of token tuples containing word, POS tag, skip status, CEFR level, start index, and end index.
    """

    def __init__(self, analyzer: CEFRAnalyzer = CEFRAnalyzer(), entity_types_to_skip: Union[set[str], list[str], None] = None,
                abbreviation_mapping: Union[dict[str, str], None] = None) -> None:
        """
        Initialize the CEFRSpaCyAnalyzer instance.

        Parameters:
            analyzer (CEFRAnalyzer, optional): An instance of CEFRAnalyzer. Defaults to CEFRAnalyzer().
            entity_types_to_skip (Union[set[str], list[str], None], optional): A set or list of spaCy entity types to skip during analysis. Defaults to None.
            abbreviation_mapping (Union[dict[str, str], None], optional): A dictionary mapping abbreviations to their full forms. Defaults to None.
        """
        self._analyzer = analyzer
        self.entity_types_to_skip = set() if entity_types_to_skip is None else set(entity_types_to_skip)
        self.abbreviation_mapping = dict() if abbreviation_mapping is None else abbreviation_mapping

    def _get_next_entity(self, entities_iter: Iterator):
        """
        Get the next entity from the iterator.
        """
        try:
            return next(entities_iter)
        except StopIteration:
            return None

    def _get_word_pos_tokens_set(self, tokens: list[tuple[str, str, bool]]) -> set[tuple[str, str]]:
        """G
        et unique word and POS tag tuples from tokens.

        Args:
            tokens (list[tuple[str, str, bool]]): List of token tuples.

        Returns:
            set[tuple[str, str]]: Set of unique word and POS tag tuples.
        """
        return {(token[1], token[2]) for token in tokens if not token[3]}

    def _fetch_word_pos_level_tokens(self, word_pos_tokens_set: set[tuple[str, str]]) -> dict[tuple[str, str], float]:
        """
        Fetch CEFR levels for unique word and POS tag tuples.

        Args:
            word_pos_tokens_set (set[tuple[str, str]]): Set of unique word and POS tag tuples.

        Returns:
            dict[tuple[str, str], float]: Dictionary mapping word and POS tag tuples to CEFR levels.
        """
        result_dict = dict()
        for word, pos_tag in word_pos_tokens_set:
            level = self._analyzer.get_word_pos_level_float(word, pos_tag, avg_level_not_found_pos=True)
            result_dict[(word, pos_tag)] = level if level is not None else 0

        return result_dict

    def analize_doc(self, doc) -> list[str, str, bool, float, int, int]:
        """
        Analyze the document for CEFR levels, considering skipped entities and abbreviation mapping.

        Args:
            doc: SpaCy tokens.

        Returns:
            list[tuple[str, str, bool, float, int, int]]: List of token tuples containing word, POS tag, skip status, CEFR level, start index, and end index.
        """

        self.tokens = []

        if len(self.entity_types_to_skip):
            entities_iter = iter(doc.ents)
            current_entity = self._get_next_entity(entities_iter)
        else:
            current_entity = None

        nlp_tokens = []
        for token in doc:
            to_skip = False
            token_start = token.idx
            token_end = token_start + len(token.text)

            if current_entity:
                while current_entity and token_start > current_entity.start_char:
                    current_entity = self._get_next_entity(entities_iter)

                if current_entity and current_entity.label_ in self.entity_types_to_skip \
                    and current_entity.start_char <= token_start < current_entity.end_char:
                    to_skip = True

            word = token.text.strip()
            word_lower = word.lower()
            word_pos = token.tag_

            if word_pos == 'POS' and word_lower == "'s":
                to_skip = True
            else:
                abbreviation_form = self.abbreviation_mapping.get(word_lower)
                if abbreviation_form:
                    word = abbreviation_form
                    word_lower = abbreviation_form

                if not to_skip and not word.isalpha():
                    to_skip = True

            nlp_tokens.append((word, word_lower, word_pos, to_skip, token_start, token_end))

        word_pos_set = self._get_word_pos_tokens_set(nlp_tokens)
        word_pos_unique_level_tokens = self._fetch_word_pos_level_tokens(word_pos_set)

        self.tokens = []
        for word, word_lower, word_pos, is_skipped, token_start, token_end in nlp_tokens:
            level = word_pos_unique_level_tokens.get((word_lower, word_pos))
            self.tokens.append((word, word_pos, is_skipped, level, token_start, token_end))

        return self.tokens
