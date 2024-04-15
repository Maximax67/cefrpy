from enum import Enum, unique

@unique
class CEFRLevel(Enum):
    """
    Represents CEFR (Common European Framework of Reference for Languages) levels.
    """

    A1 = 1
    A2 = 2
    B1 = 3
    B2 = 4
    C1 = 5
    C2 = 6

    def __str__(self) -> str:
        """
        Returns a string representation of the CEFR level.
        """
        return self.name

    def __int__(self) -> int:
        """
        Returns an integer representation of the CEFR level.
        """
        return self.value

    def __eq__(self, other) -> bool:
        """
        Checks if this CEFR level is equal to another CEFR level.
        """
        if isinstance(other, CEFRLevel):
            return self.value == other.value
        return NotImplemented

    def __lt__(self, other) -> bool:
        """
        Checks if this CEFR level is less than another CEFR level.
        """
        if isinstance(other, CEFRLevel):
            return self.value < other.value
        return NotImplemented

    def __le__(self, other) -> bool:
        """
        Checks if this CEFR level is less than or equal to another CEFR level.
        """
        if isinstance(other, CEFRLevel):
            return self.value <= other.value
        return NotImplemented

    def __gt__(self, other) -> bool:
        """
        Checks if this CEFR level is greater than another CEFR level.
        """
        if isinstance(other, CEFRLevel):
            return self.value > other.value
        return NotImplemented

    def __ge__(self, other) -> bool:
        """
        Checks if this CEFR level is greater than or equal to another CEFR level.
        """
        if isinstance(other, CEFRLevel):
            return self.value >= other.value
        return NotImplemented

    @classmethod
    def from_str(cls, level_str: str):
        """
        Creates a CEFRLevel instance from a string representation of the level.

        Parameters:
            level_str (str): The string representation of the CEFR level.

        Returns:
            CEFRLevel: The CEFRLevel instance corresponding to the input string.

        Raises:
            ValueError: If the provided string is invalid.
        """
        level = cls.__members__.get(level_str.upper())
        if level is None:
            raise ValueError(f"Invalid CEFR level string: {level_str}")

        return level
