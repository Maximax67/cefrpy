from array import array
from string import ascii_lowercase

from .POSTag import POSTag # :noindex:

# A set of valid characters for words in the data.
VALID_WORD_CHARACTERS = set(ascii_lowercase)

# Maximum position tag ID allowed in the data.
MAX_POS_TAG_ID = POSTag.get_total_tags() - 1

# Maximum level value allowed in the data.
MAX_LEVEL_VALUE = 6 * 50


def is_wlp_length_valid(wlp_length: int) -> bool:
    """
    Check if the length of the Word Length Position (WLP) array is valid.

    Args:
        wlp_length (int): The length of the WLP array.

    Returns:
        bool: True if the length is valid, False otherwise.
    """
    return 2 <= wlp_length <= 255


def is_wlp_array_valid(wlp_array: array) -> bool:
    """
    Check if the Word Length Position (WLP) array is valid.

    Args:
        wlp_array (array): The WLP array.

    Returns:
        bool: True if the WLP array is valid, False otherwise.
    """
    wlp_array_len = len(wlp_array)
    if not is_wlp_length_valid(wlp_array_len):
        return False

    array_iter = iter(wlp_array)
    sector_end = next(array_iter)
    block_size = 2

    for _ in range(wlp_array_len - 1):
        sector_start = sector_end
        sector_end = next(array_iter)
        block_size += 1

        if sector_end < sector_start:
            return False

        if (sector_end - sector_start) % block_size != 0:
            return False

    return True


def validate_data_block(data: bytearray, start_pos: int, block_length: int) -> bool:
    """
    Validate a data block within the CEFR data.

    Args:
        data (bytearray): The CEFR data.
        start_pos (int): The starting position of the data block.
        block_length (int): The length of the data block.

    Returns:
        bool: True if the data block is valid, False otherwise.
    """
    word_len = block_length - 2
    for i in range(start_pos, start_pos + word_len):
        if not chr(data[i]) in VALID_WORD_CHARACTERS:
            return False

    if data[i + 1] > MAX_POS_TAG_ID:
        return False

    if data[i + 2] > MAX_LEVEL_VALUE:
        return False

    return True


def is_data_valid(wlp_array: array, data: bytearray) -> bool:
    """
    Check if the CEFR data is valid.

    Args:
        wlp_array (array): The Word Length Position (WLP) array.
        data (bytearray): The CEFR data.

    Returns:
        bool: True if the data is valid, False otherwise.
    """
    if not is_wlp_array_valid(wlp_array):
        return False

    if wlp_array[-1] > len(data):
        return False

    wlp_array_len = len(wlp_array)
    array_iter = iter(wlp_array)
    sector_end = next(array_iter)
    block_size = 2

    for _ in range(wlp_array_len - 1):
        block_size += 1
        sector_start = sector_end
        sector_end = next(array_iter)

        for start_block_pos in range(sector_start, sector_end, block_size):
            if not validate_data_block(data, start_block_pos, block_size):
                return False

    return True
