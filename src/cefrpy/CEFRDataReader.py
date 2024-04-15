import os
import array
import struct

from typing import Union

from .CEFRDataValidator import is_wlp_length_valid, is_data_valid


class CEFRDataReader:
    """
    A class to read CEFR (Common European Framework of Reference for Languages) data from database file.

    This class provides methods to access word length positions in database file, data array values,
    and retrieve information about words' part of speech levels.

    Attributes:
        data_path (str): The path to the binary data file.
        _wlp (array.array): An array containing word length positions.
        _data_array (bytearray): The data array from the database file.
    """

    def __init__(self, data_path: Union[str, None] = None) -> None:
        """
        Initialize the CEFR DataReader.

        Args:
            data_path (str, optional): The path to the binary data file. If None, default is used.

        Raises:
            Exception: If the CEFR database file content is invalid.
        """

        self.data_path = os.path.join(os.path.dirname(__file__), 'data.bin') if data_path is None else data_path
        self._wlp = array.array('I')
        self._data_array = bytearray()

        if not self._read_data():
            raise Exception(f'CEFR database file content is invalid: {self.data_path}')


    def _read_data(self) -> bool:
        """
        Read data from the binary file.

        Returns:
            bool: True if the data is successfully read and valid, False otherwise.
        """
        with open(self.data_path, 'rb') as file:
            wlp_len = struct.unpack('B', file.read(1))[0]
            if not is_wlp_length_valid(wlp_len):
                return False

            wlp_data = file.read(wlp_len * struct.calcsize('I'))
            self._wlp.frombytes(wlp_data)
            self._data_array = bytearray(file.read())

        return is_data_valid(self._wlp, self._data_array)


    def get_wlp_value_at(self, i: int) -> int:
        """
        Get the value at index i in the word length positions array.

        Args:
            i (int): Index in the array.

        Returns:
            int: Value at the specified index.

        Raises:
            IndexError: If the index is out of range.
        """
        if 0 <= i < len(self._wlp):
            return self._wlp[i]

        raise IndexError("Index out of range for _wlp")


    def get_data_array_value_at(self, i: int) -> int:
        """
        Get the value at index i in the data array.

        Args:
            i (int): Index in the array.

        Returns:
            int: Value at the specified index.

        Raises:
            IndexError: If the index is out of range.
        """
        if 0 <= i < len(self._data_array):
            return self._data_array[i]

        raise IndexError("Index out of range for _data_array")


    def get_wlp_len(self) -> int:
        """
        Get the length of the word length positions array.

        Returns:
            int: Length of the word length positions array.
        """
        return len(self._wlp)


    def get_data_array_len(self) -> int:
        """
        Get the length of the data array.

        Returns:
            int: Length of the data array.
        """
        return len(self._data_array)
