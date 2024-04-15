from math import inf
from typing import Union

from .CEFRDataProcessor import CEFRDataProcessor
from .POSTag import POSTag
from .CEFRLevel import CEFRLevel


class CEFRAnalyzer:
    """
    A class to analyze CEFR (Common European Framework of Reference for Languages) data.

    This class provides methods to analyze word part of speech levels and retrieve information
    about words' average levels.

    Attributes:
        _data_processor (CEFRDataProcessor): The CEFR data processor object to use.
    """

    def __init__(self, data_processor: CEFRDataProcessor = CEFRDataProcessor()) -> None:
        """
        Initialize the CEFRAnalyzer with a data processor.

        Parameters:
            data_processor (CEFRDataProcessor, optional): The CEFR data processor object to use. Defaults to CEFRDataProcessor().
        """
        self._data_processor = data_processor


    def get_word_pos_level_float(self, word: str, pos_tag: Union[str, POSTag], avg_level_not_found_pos: bool = False) -> Union[float, None]:
        """
        Get the level of a word's part of speech.

        Args:
            word (str): The word to query.
            pos_tag (Union[str, POSTag]): The part of speech tag.
            avg_level_not_found_pos (bool, optional): If True, returns the average level of the part of speech when not found. Defaults to False.

        Returns:
            Union[float, None]: The level of the word's part of speech, or None if not found.
        """
        pos_tag_id = self.get_pos_tag_id(pos_tag)
        if pos_tag_id is None:
            if not avg_level_not_found_pos:
                return

            pos_tag_id = inf

        return self._data_processor.get_word_level_for_pos_id(word, pos_tag_id, avg_level_not_found_pos)


    def get_word_pos_level_CEFR(self, word: str, pos_tag: Union[str, POSTag], avg_level_not_found_pos: bool = False) -> Union[CEFRLevel, None]:
        """
        Get the CEFR level of a word's part of speech.

        Args:
            word (str): The word to query.
            pos_tag (Union[str, POSTag]): The part of speech tag.
            avg_level_not_found_pos (bool, optional): If True, returns the average level of the part of speech when not found. Defaults to False.

        Returns:
            Union[CEFRLevel, None]: The level of the word's part of speech, or None if not found.
        """
        float_level = self.get_word_pos_level_float(word, pos_tag, avg_level_not_found_pos)
        if float_level is None:
            return

        return CEFRLevel(round(float_level))


    def get_average_word_level_float(self, word: str) -> Union[float, None]:
        """
        Get the average level of the word.

        Args:
            word (str): The word to query.

        Returns:
            Union[float, None]: The average level of the word, or None if not found.
        """
        return self._data_processor.get_word_level_for_pos_id(word, inf, True)


    def get_average_word_level_CEFR(self, word: str) -> Union[CEFRLevel, None]:
        """
        Get the average CEFR level of the word.

        Args:
            word (str): The word to query.

        Returns:
            Union[CEFRLevel, None]: The average level of the word, or None if not found.
        """
        float_level = self.get_average_word_level_float(word)
        if float_level is None:
            return

        return CEFRLevel(round(float_level))


    def get_all_pos_for_word_as_str(self, word: str) -> list[str]:
        """
        Retrieves the names of all part-of-speech tags associated with a given word.

        Args:
            word (str): The word to retrieve part-of-speech tags for.

        Returns:
            list[str]: A list of strings representing the names of the part-of-speech tags associated with the word. 
                If the word is not found in the data, an empty list is returned.
        """
        pos_tags = self._data_processor.get_all_pos_for_word(word)
        pos_tags_str_list = []

        for pos_tag_id in pos_tags:
            pos_tag_str = POSTag.get_tag_name_by_id(pos_tag_id)
            pos_tags_str_list.append(pos_tag_str)

        return pos_tags_str_list


    def get_all_pos_for_word(self, word: str) -> list[POSTag]:
        """
        Retrieves all part-of-speech tags associated with a given word as POSTag enums.

        Args:
            word (str): The word to retrieve part-of-speech tags for.

        Returns:
            list[POSTag]: A list of POSTag enums representing the part-of-speech tags associated with the word. 
                If the word is not found in the data, an empty list is returned.
        """
        pos_tags = self._data_processor.get_all_pos_for_word(word)
        pos_tags_list = []

        for pos_tag_id in pos_tags:
            pos_tags_list.append(POSTag(pos_tag_id))

        return pos_tags_list


    def get_pos_level_dict_for_word(self, word: str, pos_tag_as_string: bool = False, 
                                    word_level_as_float: bool = False) -> dict[Union[str, POSTag], Union[float, CEFRLevel]]:
        """
        Retrieves a dictionary mapping part-of-speech tags to their associated CEFR levels for a given word.

        Args:
            word (str): The word to retrieve part-of-speech tags and their associated levels for.
            pos_tag_as_string (bool, optional): If True, part-of-speech tags are returned as strings; if False, as POSTag enums. Defaults to False.
            word_level_as_float (bool, optional): If True, CEFR levels are returned as floats; if False, as CEFRLevel enums. Defaults to False.

        Returns:
            dict[Union[str, POSTag], Union[float, CEFRLevel]]: A dictionary mapping part-of-speech tags to their associated CEFR levels.
                If `pos_tag_as_string` is True, part-of-speech tags are strings; otherwise, they are POSTag enums.
                If `word_level_as_float` is True, CEFR levels are floats; otherwise, they are CEFRLevel enums.
                If the word is not found in the data, an empty dictionary is returned.
        """
        if pos_tag_as_string:
            pos_converter = lambda x: POSTag.get_tag_name_by_id(x)
        else:
            pos_converter = lambda x: POSTag(x)

        pos_and_levels = self._data_processor.get_pos_level_dict_for_word(word)
        pos_and_levels_formatted = dict()

        if word_level_as_float:
            for pos, level in pos_and_levels.items():
                formatted_pos = pos_converter(pos)
                pos_and_levels_formatted[formatted_pos] = level
        else:
            for pos, level in pos_and_levels.items():
                formatted_pos = pos_converter(pos)
                pos_and_levels_formatted[formatted_pos] = CEFRLevel(round(level))

        return pos_and_levels_formatted


    def get_max_word_len(self) -> int:
        """
        Get the maximum word length available in the data.

        Returns:
            int: The maximum word length.
        """
        return self._data_processor.get_max_word_len()


    def is_word_in_database(self, word: str) -> bool:
        """
        Check if a word is in the DataReader database.

        Args:
            word (str): The word to check.

        Returns:
            bool: True if the word is in the database, False otherwise.
        """
        return self._data_processor.is_word_in_database(word)


    def is_word_pos_id_database(self, word: str, pos_tag: Union[str, POSTag]) -> bool:
        """
        Check if a word pos is in the database.

        Args:
            word (str): The word to check.
            pos_tag (Union[str, POSTag]): The part of speech tag.

        Returns:
            bool: True if the word is in the database, False otherwise.
        """
        pos_tag_id = self.get_pos_tag_id(pos_tag)
        if pos_tag_id is None:
            return False

        return self._data_processor.is_word_pos_id_database(word, pos_tag_id)


    def yield_words_with_length(self, word_length: int, reverse_order: bool = False):
        """
        Yield words of a specific length from the database.

        Args:
            word_length (int): The length of the words to yield.
            reverse_order (bool, optional): If True, yield words in reverse order. Defaults to False.

        Yields:
            str: A word from the database with the specified length.
        """
        return self._data_processor.yield_words_with_length(word_length, reverse_order)


    def yield_words(self, reverse_order: bool = False, word_length_sort: bool = False):
        """
        Yield all words in the database.

        Args:
            reverse_order (bool, optional): If True, yield words in reverse order. Defaults to False.
            word_length_sort (bool, optional): If True, yield words sorted by word length. Defaults to False.

        Yields:
            str: A word from the database.
        """
        return self._data_processor.yield_words(reverse_order, word_length_sort)


    def yield_word_pos_with_length(self, word_length: int, reverse_order: bool = False, pos_tag_as_string: bool = False):
        """
        Yield words of a specific length with their associated part-of-speech tag IDs from the database.

        Args:
            word_length (int): The length of the words to yield.
            reverse_order (bool, optional): If True, yield words in reverse order. Defaults to False.
            pos_tag_as_string (bool, optional): If True, yield part-of-speech tags as strings; if False, yield them as POSTag enums. Defaults to False.

        Yields:
            tuple: A tuple containing the word and its associated part-of-speech tag.
                If `pos_tag_as_string` is True, the tuple format is (str, str).
                If `pos_tag_as_string` is False, the tuple format is (str, POSTag).
        """
        if pos_tag_as_string:
            pos_converter = lambda x: POSTag.get_tag_name_by_id(x)
        else:
            pos_converter = lambda x: POSTag(x)

        for word, pos_tag_id in self._data_processor.yield_word_pos_id_with_length(word_length, reverse_order):
            yield (word, pos_converter(pos_tag_id))


    def yield_word_pos(self, reverse_order: bool = False, pos_tag_as_string: bool = False, word_length_sort: bool = False):
        """
        Yield all words with their associated part-of-speech tag IDs from the database.

        Args:
            reverse_order (bool, optional): If True, yield words in reverse order. Defaults to False.
            pos_tag_as_string (bool, optional): If True, yield part-of-speech tags as strings; if False, yield them as POSTag enums. Defaults to False.
            word_length_sort (bool): If True, yields data sorted by word length.

        Yields:
            tuple: A tuple containing the word and its associated part-of-speech tag.
                If `pos_tag_as_string` is True, the tuple format is (str, str).
                If `pos_tag_as_string` is False, the tuple format is (str, POSTag).
        """
        if pos_tag_as_string:
            pos_converter = lambda x: POSTag.get_tag_name_by_id(x)
        else:
            pos_converter = lambda x: POSTag(x)

        for word, pos_tag_id in self._data_processor.yield_word_pos_id(reverse_order, word_length_sort):
            yield (word, pos_converter(pos_tag_id))


    def yield_word_pos_level_with_length(self, word_length: int, reverse_order: bool = False, 
                                        pos_tag_as_string: bool = False, word_level_as_float: bool = False):
        """
        Yield words of a specific length, their part-of-speech tags, and their CEFR levels from the database based on the specified criteria.

        Args:
            word_length (int): The length of the words to yield.
            reverse_order (bool, optional): If True, yield words in reverse order. Defaults to False.
            pos_tag_as_string (bool, optional): If True, yield part-of-speech tags as strings; if False, yield them as POSTag enums. Defaults to False.
            word_level_as_float (bool, optional): If True, yield CEFR levels as floats instead of CEFRLevel enums. Defaults to False.

        Yields:
            tuple: A tuple containing the word, its part-of-speech tag, and its CEFR level. If `pos_tag_as_string` is True, the part-of-speech tag is a string, 
                otherwise, it's a POSTag enum. If `word_level_as_float` is True, the level is a float, otherwise, it's a CEFRLevel enum.
        """
        if pos_tag_as_string:
            pos_converter = lambda x: POSTag.get_tag_name_by_id(x)
        else:
            pos_converter = lambda x: POSTag(x)

        if word_level_as_float:
            for word, pos_tag_id, level in self._data_processor.yield_word_pos_level_with_length(word_length, reverse_order):
                yield (word, pos_converter(pos_tag_id), level)

            return

        for word, pos_tag_id, level in self._data_processor.yield_word_pos_level_with_length(word_length, reverse_order):
            yield (word, pos_converter(pos_tag_id), CEFRLevel(round(level)))


    def yield_word_pos_level(self, reverse_order: bool = False, pos_tag_as_string: bool = False,
                            word_level_as_float: bool = False, word_length_sort: bool = False):
        """
        Yield all words, their part-of-speech tags, and their CEFR levels from the database based on the specified criteria.

        Args:
            reverse_order (bool, optional): If True, yield words in reverse order. Defaults to False.
            pos_tag_as_string (bool, optional): If True, yield part-of-speech tags as strings; if False, yield them as POSTag enums. Defaults to False.
            word_level_as_float (bool, optional): If True, yield CEFR levels as floats instead of CEFRLevel enums. Defaults to False.
            word_length_sort (bool): If True, yields data sorted by word length.

        Yields:
            tuple: A tuple containing the word, its part-of-speech tag, and its CEFR level. If `pos_tag_as_string` is True, the part-of-speech tag is a string, 
                otherwise, it's a POSTag enum. If `word_level_as_float` is True, the level is a float, otherwise, it's a CEFRLevel enum.
        """
        if pos_tag_as_string:
            pos_converter = lambda x: POSTag.get_tag_name_by_id(x)
        else:
            pos_converter = lambda x: POSTag(x)

        if word_level_as_float:
            for word, pos_tag_id, level in self._data_processor.yield_word_pos_level(reverse_order, word_length_sort):
                yield (word, pos_converter(pos_tag_id), level)

            return

        for word, pos_tag_id, level in self._data_processor.yield_word_pos_level(reverse_order, word_length_sort):
            yield (word, pos_converter(pos_tag_id), CEFRLevel(round(level)))


    def get_word_count_for_length(self, word_length: int) -> int:
        """
        Count the number of words of a specific length in the data.

        Args:
            word_length (int): Length of the words to count.

        Returns:
            int: Number of words of the specified length.
        """
        return self._data_processor.get_word_count_for_length(word_length)


    def get_total_words(self) -> int:
        """
        Get the total count of words in the data.

        Returns:
            int: Total count of words.
        """
        return self._data_processor.get_total_words()


    def get_word_pos_count_for_length(self, word_length: int) -> int:
        """
        Count the number of positions in the data where words of a specific length start.

        Args:
            word_length (int): Length of the words to count positions for.

        Returns:
            int: Number of positions where words of the specified length start.
        """
        return self._data_processor.get_word_pos_count_for_length(word_length)


    def get_word_pos_count(self) -> int:
        """
        Get the total count of positions in the data where words start, across all word lengths.

        Returns:
            int: Total count of positions where words start.
        """
        return self._data_processor.get_word_pos_count()


    @staticmethod
    def get_pos_tag_id(pos_tag: Union[str, POSTag]) -> Union[int, None]:
        """
        Get the part of speech id.

        Args:
            pos_tag (Union[str, POSTag]): The part of speech tag.

        Returns:
            Union[int, None]: The part of speech id, or None if an exception occurs.
        """
        if isinstance(pos_tag, POSTag):
            return int(pos_tag)

        try:
            return POSTag.get_id_by_tag_name(pos_tag)
        except ValueError:
            return
