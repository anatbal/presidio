from typing import Optional, List

from presidio_analyzer import Pattern, PatternRecognizer


class UsItinRecognizer(PatternRecognizer):
    """
    Recognizes US ITIN (Individual Taxpayer Identification Number) using regex.

    :param patterns: List of patterns to be used by this recognizer
    :param context: List of context words to increase confidence in detection
    :param supported_language: Language this recognizer supports
    :param supported_entity: The entity this recognizer can detect
    """

    PATTERNS = [
        Pattern(
            "Itin (very weak)",
            r"(\b(9\d{2})[- ]{1}((7[0-9]{1}|8[0-8]{1})|(9[0-2]{1})|(9[4-9]{1}))(\d{4})\b)|(\b(9\d{2})((7[0-9]{1}|8[0-8]{1})|(9[0-2]{1})|(9[4-9]{1}))[- ]{1}(\d{4})\b)",  # noqa: E501
            0.05,
        ),
        Pattern(
            "Itin (weak)",
            r"\b(9\d{2})((7[0-9]{1}|8[0-8]{1})|(9[0-2]{1})|(9[4-9]{1}))(\d{4})\b",  # noqa: E501
            0.3,
        ),
        Pattern(
            "Itin (medium)",
            r"\b(9\d{2})[- ]{1}((7[0-9]{1}|8[0-8]{1})|(9[0-2]{1})|(9[4-9]{1}))[- ]{1}(\d{4})\b",  # noqa: E501
            0.5,
        ),
    ]

    CONTEXT = ["individual", "taxpayer", "itin", "tax", "payer", "taxid", "tin"]

    def __init__(
        self,
        patterns: Optional[List[Pattern]] = None,
        context: Optional[List[str]] = CONTEXT,
        supported_language: str = "en",
        supported_entity: str = "US_ITIN",
    ):
        patterns = patterns if patterns else self.PATTERNS
        super().__init__(
            supported_entity=supported_entity,
            patterns=patterns,
            context=context,
            supported_language=supported_language,
        )
