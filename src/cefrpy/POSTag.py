from enum import Enum, unique

POS_TAGS_DESCRIPTIONS = [
    'Coordinating conjunction',
    'Cardinal number',
    'Determiner',
    'Preposition or subordinating conjunction',
    'Adjective',
    'Adjective, comparative',
    'Adjective, superlative',
    'Modal',
    'Noun, singular or mass',
    'Noun, plural',
    'Proper noun, singular',
    'Proper noun, plural',
    'Personal/Posessive pronoun',
    'Adverb',
    'Adverb, comparative',
    'Adverb, superlative',
    'Particle',
    'To',
    'Interjection',
    'Verb, base form',
    'Verb, past tense',
    'Verb, gerund or present participle',
    'Verb, past participle',
    'Verb, non-3rd person singular present',
    'Verb, 3rd person singular present',
    'Wh-determiner',
    'Wh-pronoun',
    'Wh-adverb'
]

@unique
class POSTag(Enum):
    """
    Enumeration of Part-of-Speech (POS) tags with their corresponding IDs and descriptions.
    """

    CC = 0
    CD = 1
    DT = 2
    IN = 3
    JJ = 4
    JJR = 5
    JJS = 6
    MD = 7
    NN = 8
    NNS = 9
    NNP = 10
    NNPS = 11
    PRP = 12
    RB = 13
    RBR = 14
    RBS = 15
    RP = 16
    TO = 17
    UH = 18
    VB = 19
    VBD = 20
    VBG = 21
    VBN = 22
    VBP = 23
    VBZ = 24
    WDT = 25
    WP = 26
    WRB = 27


    def __str__(self) -> str:
        """
        Returns a string representation of the POS tag.
        """
        return self.name


    def __int__(self) -> int:
        """
        Returns an integer representation of the POS tag.
        """
        return self.value


    def __eq__(self, other) -> bool:
        """
        Checks if this POS tag is equal to another POS tag.
        """
        if isinstance(other, POSTag):
            return self.value == other.value

        return NotImplemented


    def __hash__(self) -> int:
        """
        Returns the hash value of the POS tag.
        """
        return self.value


    def get_description(self) -> str:
        """
        Retrieve the description of a POS tag.
        """
        return POS_TAGS_DESCRIPTIONS[self.value]


    @classmethod
    def from_tag_name(cls, tag_name: str):
        """
        Initialize a POS tag using its name.

        Args:
            tag_name (str): The name of the POS tag.

        Returns:
            POSTag: The POS tag corresponding to the given name.

        Raises:
            ValueError: If the provided tag name is invalid.
        """
        tag = cls.__members__.get(tag_name)
        if tag is None:
            raise ValueError(f"Invalid tag name: {tag_name}")

        return tag


    @staticmethod
    def get_id_by_tag_name(tag_name: str) -> int:
        """
        Retrieve the ID of a POS tag by its name.

        Args:
            tag_name (str): The name of the POS tag.

        Returns:
            int: The ID corresponding to the given POS tag name.

        Raises:
            ValueError: If the provided tag name is invalid.
        """
        if tag_name not in POSTag.__members__:
            raise ValueError(f"Invalid tag name: {tag_name}")

        return POSTag[tag_name].value


    @staticmethod
    def get_tag_name_by_id(tag_id: int) -> str:
        """
        Retrieve the name of a Part-of-Speech (POS) tag by its corresponding ID.

        Args:
            tag_id (int): The integer ID of the POS tag.

        Returns:
            str: The name of the POS tag corresponding to the provided ID.

        Raises:
            ValueError: If the provided tag_id is not within the valid range of tag IDs.
        """
        if 0 <= tag_id <= POSTag.get_total_tags():
            return POSTag(tag_id).name

        raise ValueError(f"Invalid tag id: {tag_id}")


    @staticmethod
    def get_description_by_tag_name(tag_name: str) -> str:
        """
        Retrieve the description of a POS tag by its name.

        Args:
            tag_name (str): The name of the POS tag.

        Returns:
            str: The description corresponding to the given POS tag name.

        Raises:
            ValueError: If the provided tag name is invalid.
        """
        tag_id = POSTag.get_id_by_tag_name(tag_name)

        return POS_TAGS_DESCRIPTIONS[tag_id]


    @staticmethod
    def get_description_by_tag_id(tag_id: int) -> str:
        """
        Retrieve the description of a POS tag by its ID.

        Args:
            tag_id (int): The ID of the POS tag.

        Returns:
            str: The description corresponding to the given POS tag ID.

        Raises:
            ValueError: If the provided tag ID is invalid.
        """
        if tag_id < 0 or tag_id >= len(POS_TAGS_DESCRIPTIONS):
            raise ValueError(f"Invalid tag id: {tag_id}")

        return POS_TAGS_DESCRIPTIONS[tag_id]


    @staticmethod
    def get_total_tags() -> int:
        """
        Retrieve the total number of POS tags.

        Returns:
            int: The total number of POS tags.
        """
        return len(POSTag.__members__)


    @staticmethod
    def get_all_tags() -> list[str]:
        """
        Get a list of all part-of-speech tag names.

        Returns:
            list[str]: A list containing all part-of-speech tag names.
        """
        return [*POSTag.__members__]
