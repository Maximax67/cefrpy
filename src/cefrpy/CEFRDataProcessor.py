import struct

from typing import Union
from heapq import heapify, heappush, heappop

from .CEFRDataReader import CEFRDataReader


class HeapqReverseDataWrapper():
    """
    Wrapper class to reverse the ordering of data when using heapq.

    This class is used to wrap data objects to reverse their ordering when they are stored in a heapq. By default, heapq
    stores items in ascending order. This wrapper class allows items to be stored in descending order.

    Args:
        data: The data object to be wrapped.

    Attributes:
        data: The wrapped data object.

    Methods:
        __lt__(self, other): Less-than comparison method used to determine the ordering of the wrapped data.
    """
    def __init__(self, data) -> None:
        """
        Initialize the HeapqReverseDataWrapper instance.

        Args:
            data: The data object to be wrapped.
        """
        self.data = data

    def __lt__(self, other) -> bool:
        """
        Less-than comparison method used to determine the reversed ordering of the wrapped data.

        Args:
            other: Another object to compare with.

        Returns:
            bool: True if the wrapped data is greater than the other object, False otherwise.
        """
        return self.data.__gt__(other.data)


class CEFRDataProcessor:
    """
    A class to process CEFR (Common European Framework of Reference for Languages) data.

    Attributes:
        _data_reader (CEFRDataReader): An instance of CEFRDataReader to read CEFR data.
    """

    def __init__(self, data_reader: CEFRDataReader = CEFRDataReader()) -> None:
        """
        Initialize the CEFRDataProcessor with an optional data_reader.

        Args:
            data_reader (CEFRDataReader, optional): An instance of CEFRDataReader to read CEFR data. Defaults to CEFRDataReader().
        """
        self._data_reader = data_reader


    def get_max_word_len(self) -> int:
        """
        Get the maximum word length available in the data.

        Returns:
            int: The maximum word length.
        """
        return self._data_reader.get_wlp_len() - 1


    def is_word_len_valid(self, word_len: int) -> bool:
        """
        Check if the word length is valid.

        Args:
            word_len (int): The length of the word.

        Returns:
            bool: True if the word length is valid, False otherwise.
        """
        return 0 < word_len < self._data_reader.get_wlp_len()


    def _get_first_word_match_pos(self, word_packed: bytes) -> int:
        """
        Get the position of the first occurrence of a word in the data.

        Args:
            word_packed (bytes): The packed representation of the word.

        Returns:
            int: The position of the first occurrence of the word, or -1 if not found.
        """
        word_packed_len = len(word_packed)
        data_block_len = word_packed_len + 2
        l = self._data_reader.get_wlp_value_at(word_packed_len - 1)
        r = self._data_reader.get_wlp_value_at(word_packed_len)

        while l <= r:
            m = (((r - l) // data_block_len) >> 1) * data_block_len + l
            i = m
            matched = True
            for c1 in word_packed:
                c2 = self._data_reader.get_data_array_value_at(i)
                if c2 < c1:
                    l = m + data_block_len
                    matched = False
                    break

                if c2 > c1:
                    r = m - data_block_len
                    matched = False
                    break

                i += 1

            if matched:
                return m

        return -1


    def _get_int_word_level_for_pos_id(self, word_packed: bytes, pos_tag_id: int, avg_level_not_found_pos: bool = False) -> Union[int, None]:
        """
        Get the packed level of a word's part of speech.

        Args:
            word_packed (bytes): The packed word to query.
            pos_tag_id (int): The part of speech tag ID.
            avg_level_not_found_pos (bool, optional): If True, returns the average level of the part of speech
                when not found. Defaults to False.
        Returns:
            Union[int, None]: The packed level of the word's part of speech, or None if not found.
        """
        first_match = self._get_first_word_match_pos(word_packed)
        if first_match == -1:
            return

        word_packed_len = len(word_packed)
        i = first_match + word_packed_len
        p = self._data_reader.get_data_array_value_at(i)
        level = self._data_reader.get_data_array_value_at(i + 1)

        if p == pos_tag_id:
            return level

        data_block_len = word_packed_len + 2
        start_segment_pos = self._data_reader.get_wlp_value_at(word_packed_len - 1)
        end_segment_pos = self._data_reader.get_wlp_value_at(word_packed_len)

        m = first_match
        founded_pos = 1
        level_accumulator = level

        if p > pos_tag_id:
            while True:
                m -= data_block_len
                if m < start_segment_pos:
                    break

                i = m
                for c1 in word_packed:
                    if self._data_reader.get_data_array_value_at(i) != c1:
                        break

                    i += 1
                else:
                    p = self._data_reader.get_data_array_value_at(i)
                    level = self._data_reader.get_data_array_value_at(i + 1)

                    if p == pos_tag_id:
                        return level

                    founded_pos += 1
                    level_accumulator += level
                    continue

                break

            m = first_match

            
        else:
            while True:
                m += data_block_len
                if m >= end_segment_pos:
                    break

                i = m
                for c1 in word_packed:
                    if self._data_reader.get_data_array_value_at(i) != c1:
                        break

                    i += 1
                else:
                    p = self._data_reader.get_data_array_value_at(i)
                    level = self._data_reader.get_data_array_value_at(i + 1)

                    if p == pos_tag_id:
                        return level

                    founded_pos += 1
                    level_accumulator += level
                    continue

                break

            m = first_match

            while True:
                m -= data_block_len
                if m < start_segment_pos:
                    break

                i = m
                for c1 in word_packed:
                    if self._data_reader.get_data_array_value_at(i) != c1:
                        break

                    i += 1
                else:
                    founded_pos += 1
                    level_accumulator += self._data_reader.get_data_array_value_at(i + 1)
                    continue

                break

        if avg_level_not_found_pos:
            return round(level_accumulator / founded_pos)


    def _get_word_data_range(self, word: str) -> Union[range, None]:
        """
        Determines the range of data associated with a given word.

        Args:
            word (str): The word to determine the data range for.

        Returns:
            Union[range, None]: A range representing the positions in the data array where the word's information is stored.
                If the word is not found in the data or its length is invalid, returns None.
        """
        if not self.is_word_len_valid(len(word)):
            return

        word_packed = self.pack_word(word)
        first_match = self._get_first_word_match_pos(word_packed)
        if first_match == -1:
            return

        word_packed_len = len(word_packed)
        data_block_len = word_packed_len + 2

        start_segment_pos = self._data_reader.get_wlp_value_at(word_packed_len - 1)
        end_segment_pos = self._data_reader.get_wlp_value_at(word_packed_len)

        m = first_match
        i = first_match + word_packed_len

        while True:
            m -= data_block_len
            if m < start_segment_pos:
                break

            i = m
            for c1 in word_packed:
                if self._data_reader.get_data_array_value_at(i) != c1:
                    break

                i += 1
            else:
                continue

            break

        start_range = m + data_block_len + word_packed_len
        m = first_match

        while True:
            m += data_block_len
            if m >= end_segment_pos:
                break

            i = m
            for c1 in word_packed:
                if self._data_reader.get_data_array_value_at(i) != c1:
                    break

                i += 1
            else:
                continue

            break

        end_range = i - data_block_len + word_packed_len + 1

        return range(start_range, end_range, data_block_len)


    def get_all_pos_for_word(self, word: str) -> list[int]:
        """
        Retrieves the IDs of all part-of-speech tags associated with a given word.

        Args:
            word (str): The word to retrieve part-of-speech tags for.

        Returns:
            list[int]: A list of IDs representing the part-of-speech tags associated with the word. 
                If the word is not found in the data, an empty list is returned.
        """
        data_range = self._get_word_data_range(word)
        if data_range is None:
            return []

        pos_list = []
        for i in data_range:
            pos_tag = self._data_reader.get_data_array_value_at(i)
            pos_list.append(pos_tag)

        return pos_list


    def get_pos_level_dict_for_word(self, word: str) -> dict[int, float]:
        """
        Retrieves a dictionary mapping part-of-speech tag IDs to their associated CEFR levels for a given word.

        Args:
            word (str): The word to retrieve part-of-speech tags and their associated levels for.

        Returns:
            dict[int, float]: A dictionary mapping part-of-speech tag IDs to their associated CEFR levels (as floats).
                If the word is not found in the data, an empty dictionary is returned.
        """
        data_range = self._get_word_data_range(word)
        if data_range is None:
            return dict()

        result = dict()
        for i in data_range:
            pos_tag = self._data_reader.get_data_array_value_at(i)
            level = self._data_reader.get_data_array_value_at(i + 1)
            word_level_float = self.byte_int_level_to_float(level)

            result[pos_tag] = word_level_float

        return result


    def get_word_level_for_pos_id(self, word: str, pos_tag_id: int, avg_level_not_found_pos: bool = False) -> Union[float, None]:
        """
        Get the level of a word's part of speech.

        Args:
            word (str): The word to query.
            pos_tag_id (int): The part of speech tag ID.
            avg_level_not_found_pos (bool, optional): If True, returns the average level of the part of speech when not found. Defaults to False.

        Returns:
            Union[float, None]: The level of the word's part of speech, or None if not found.
        """
        if not self.is_word_len_valid(len(word)):
            return

        word_packed = self.pack_word(word)
        level = self._get_int_word_level_for_pos_id(word_packed, pos_tag_id, avg_level_not_found_pos)

        if level is not None:
            return self.byte_int_level_to_float(level)


    def is_word_in_database(self, word: str) -> bool:
        """
        Check if a word is in the database.

        Args:
            word (str): The word to check.

        Returns:
            bool: True if the word is in the database, False otherwise.
        """
        if not self.is_word_len_valid(len(word)):
            return False

        word_packed = self.pack_word(word)

        return self._get_first_word_match_pos(word_packed) != -1


    def is_word_pos_id_database(self, word: str, pos_tag_id: int) -> bool:
        """
        Check if a word pos is in the database.

        Args:
            word (str): The word to check.
            pos_tag_id (int): The part of speech tag ID.

        Returns:
            bool: True if the word is in the database, False otherwise.
        """
        return self.get_word_level_for_pos_id(word, pos_tag_id) is not None


    def _unpack_word_in_data_array(self, i: int, word_length: int) -> str:
        """
        Unpack a word in the data array starting from index 'i' with a given length.

        Args:
            i (int): The starting index of the word in the data array.
            word_len (int): The length of the word to unpack.

        Returns:
            str: The unpacked word.

        Note:
            It iterates over the specified range in the data array and constructs the word
            character by character using the ASCII values.
        """
        word = ""
        for j in range(i, i + word_length):
            word += chr(self._data_reader.get_data_array_value_at(j))

        return word


    def _get_word_yield_start_block_range(self, word_length: int, reverse_order: bool = False):
        """
        Get the range of block indices to start yielding words of a specific length.

        Args:
            word_length (int): The length of the words to yield.
            reverse_order (bool, optional): If True, yield words in reverse order. Defaults to False.

        Returns:
            range: A range of block indices indicating where to start yielding words of the specified length.
        """
        segment_start = self._data_reader.get_wlp_value_at(word_length - 1)
        segment_end = self._data_reader.get_wlp_value_at(word_length)
        data_block_len = word_length + 2

        if reverse_order:
            # This approach should be faster than reversed(range(...)):
            # https://stackoverflow.com/a/7286465/15070145
            return range(segment_end - data_block_len, segment_start - data_block_len, -data_block_len)

        return range(segment_start, segment_end, data_block_len)


    def yield_words_with_length(self, word_length: int, reverse_order: bool = False):
        """
        Yield words of a specific length from the database.

        Args:
            word_length (int): The length of the words to yield.
            reverse_order (bool, optional): If True, yield words in reverse order. Defaults to False.

        Yields:
            str: A word from the database with the specified length.
        """
        if not self.is_word_len_valid(word_length):
            return

        start_block_range = self._get_word_yield_start_block_range(word_length, reverse_order)

        last_word = None
        for i in start_block_range:
            word = self._unpack_word_in_data_array(i, word_length)

            if word != last_word:
                yield word
                last_word = word


    def yield_word_pos_id_with_length(self, word_length: int, reverse_order: bool = False):
        """
        Yield words of a specific length with their associated part-of-speech tag IDs from the database.

        Args:
            word_length (int): The length of the words to yield.
            reverse_order (bool, optional): If True, yield words in reverse order. Defaults to False.

        Yields:
            tuple[str, int]: A tuple containing a word from the database with the specified length and its associated
            part-of-speech tag ID as an integer.
        """
        if not self.is_word_len_valid(word_length):
            return

        start_block_range = self._get_word_yield_start_block_range(word_length, reverse_order)

        for i in start_block_range:
            word = self._unpack_word_in_data_array(i, word_length)
            word_pos = self._data_reader.get_data_array_value_at(i + word_length)

            yield (word, word_pos)


    def yield_word_pos_level_with_length(self, word_length: int, reverse_order: bool = False):
        """
        Yield words of a specific length with their part-of-speech tag IDs and levels from the database.

        Args:
            word_length (int): The length of the words to yield.
            reverse_order (bool, optional): If True, yield words in reverse order. Defaults to False.

        Yields:
            tuple[str, int, float]: A tuple containing a word from the database with the specified length, its associated
            part-of-speech tag ID, and its level.
        """
        if not self.is_word_len_valid(word_length):
            return

        start_block_range = self._get_word_yield_start_block_range(word_length, reverse_order)

        for i in start_block_range:
            word = self._unpack_word_in_data_array(i, word_length)

            j = i + word_length
            word_pos = self._data_reader.get_data_array_value_at(j)
            word_level = self._data_reader.get_data_array_value_at(j + 1)
            word_level_float = self.byte_int_level_to_float(word_level)

            yield (word, word_pos, word_level_float)


    def _yield_all_data(self, yield_method_with_word_length: callable, reverse_order: bool, word_lenght_sort: bool):
        """
        Yields data from various generators based on word length.

        Args:
            yield_method_with_word_length (callable): A method to yield data by word length.
            reverse_order (bool): If True, yields data in reverse order.
            word_length_sort (bool): If True, yields data sorted by word length.

        Yields:
            object: Data from the yield_method_with_word_length generator.
        """
        max_word_len = self.get_max_word_len()

        if word_lenght_sort:
            if reverse_order:
                reverse_range = range(max_word_len, 0, -1)
            else:
                reverse_range = range(1, max_word_len + 1)

            for length in reverse_range:
                for data in yield_method_with_word_length(length, reverse_order):
                    yield data

            return

        generators = [yield_method_with_word_length(i, reverse_order) for i in range(1, max_word_len + 1)]
        words_heap = []
        heapify(words_heap)

        if reverse_order:
            for i, generator in enumerate(generators):
                try:
                    data = next(generator)
                    heappush(words_heap, (HeapqReverseDataWrapper(data), i))
                except StopIteration:
                    pass

            while len(words_heap):
                data, generator_idx = heappop(words_heap)
                yield data.data

                try:
                    data = next(generators[generator_idx])
                    heappush(words_heap, (HeapqReverseDataWrapper(data), generator_idx))
                except StopIteration:
                    pass

            return

        for i, generator in enumerate(generators):
            try:
                data = next(generator)
                heappush(words_heap, (data, i))
            except StopIteration:
                pass

        while len(words_heap):
            data, generator_idx = heappop(words_heap)
            yield data

            try:
                data = next(generators[generator_idx])
                heappush(words_heap, (data, generator_idx))
            except StopIteration:
                pass


    def yield_words(self, reverse_order: bool = False, word_lenght_sort: bool = False):
        """
        Yield all words in the database.

        Args:
            reverse_order (bool, optional): If True, yield words in reverse order. Defaults to False.
            word_length_sort (bool, optional): If True, yield words sorted by word length. Defaults to False.

        Yields:
            str: A word from the database.
        """
        return self._yield_all_data(self.yield_words_with_length, reverse_order, word_lenght_sort)


    def yield_word_pos_id(self, reverse_order: bool = False, word_lenght_sort: bool = False):
        """
        Yield words with their part-of-speech tag IDs from the database.

        Args:
            reverse_order (bool, optional): If True, yield words in reverse order. Defaults to False.
            word_length_sort (bool, optional): If True, yield words sorted by word length. Defaults to False.

        Yields:
            tuple[str, int]: A tuple containing a word from the database and its associated part-of-speech tag ID.
        """
        return self._yield_all_data(self.yield_word_pos_id_with_length, reverse_order, word_lenght_sort)


    def yield_word_pos_level(self, reverse_order: bool = False, word_lenght_sort: bool = False):
        """
        Yield words with their part-of-speech tag IDs and levels from the database.

        Args:
            reverse_order (bool, optional): If True, yield words in reverse order. Defaults to False.
            word_length_sort (bool, optional): If True, yield words sorted by word length. Defaults to False.

        Yields:
            tuple[str, int, float]: A tuple containing a word from the database, its associated part-of-speech tag ID,
                and its level.
        """
        return self._yield_all_data(self.yield_word_pos_level_with_length, reverse_order, word_lenght_sort)


    def get_word_count_for_length(self, word_length: int) -> int:
        """
        Count the number of words of a specific length in the data.

        Args:
            word_length (int): Length of the words to count.

        Returns:
            int: Number of words of the specified length.
        """
        if not self.is_word_len_valid(word_length):
            return 0

        unique_words_counter = 0
        start_block_range = self._get_word_yield_start_block_range(word_length)

        last_word = bytearray(word_length)
        for i in start_block_range:
            for j in range(word_length):
                array_pos = i + j
                current_char = self._data_reader.get_data_array_value_at(array_pos)
                if current_char != last_word[j]:
                    last_word[j] = current_char
                    unique_words_counter += 1

                    for k in range(j + 1, word_length):
                        array_pos += 1
                        last_word[k] = self._data_reader.get_data_array_value_at(array_pos)

                    break

        return unique_words_counter


    def get_total_words(self) -> int:
        """
        Get the total count of words in the data.

        Returns:
            int: Total count of words.
        """
        counter = 0
        max_word_len = self.get_max_word_len()

        for length in range(1, max_word_len + 1):
            counter += self.get_word_count_for_length(length)

        return counter


    def get_word_pos_count_for_length(self, word_length: int) -> int:
        """
        Count the number of positions in the data where words of a specific length start.

        Args:
            word_length (int): Length of the words to count positions for.

        Returns:
            int: Number of positions where words of the specified length start.
        """
        if not self.is_word_len_valid(word_length):
            return 0

        segment_start = self._data_reader.get_wlp_value_at(word_length - 1)
        segment_end = self._data_reader.get_wlp_value_at(word_length)
        data_block_len = word_length + 2

        return (segment_end - segment_start) // data_block_len


    def get_word_pos_count(self) -> int:
        """
        Get the total count of positions in the data where words start, across all word lengths.

        Returns:
            int: Total count of positions where words start.
        """
        counter = 0
        max_word_len = self.get_max_word_len()

        for length in range(1, max_word_len + 1):
            counter += self.get_word_pos_count_for_length(length)

        return counter


    @staticmethod
    def pack_word(word: str) -> bytes:
        """
        Pack a word into bytes.

        Args:
            word (str): The word to pack.

        Returns:
            bytes: The packed representation of the word.
        """
        return struct.pack('B' * len(word), *map(ord, word))


    @staticmethod
    def byte_int_level_to_float(level: int) -> float:
        """
        Convert packed level to float.

        Args:
            level (int): level in range 0 <= level <= 250.

        Returns:
            float: The level in range 1 <= level <= 6.

        Raises:
            ValueError: If the level not in range 0 <= level <= 250.
        """
        if 0 <= level <= 250:
            return level / 50 + 1

        raise ValueError("Level should be in range 0 <= level <= 250")
