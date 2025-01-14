import json
from typing import List

from spacy.tokens import Doc, Span


class NlpArtifacts:
    """
    NlpArtifacts is an abstraction layer over the results of an NLP pipeline.

    processing over a given text, it holds attributes such as entities,
    tokens and lemmas which can be used by any recognizer
    """

    def __init__(
        self,
        entities: List[Span],
        tokens: Doc,
        tokens_indices: List[int],
        lemmas: List[str],
        nlp_engine,  # noqa ANN001
        language: str,
    ):
        self.entities = entities
        self.tokens = tokens
        self.lemmas = lemmas
        self.tokens_indices = tokens_indices
        self.keywords = self.set_keywords(nlp_engine, lemmas, language)
        self.nlp_engine = nlp_engine

    @staticmethod
    def set_keywords(
        nlp_engine, lemmas: List[str], language: str  # noqa ANN001
    ) -> List[str]:
        """
        Return keywords fpr text.

        Extracts lemmas with certain conditions as keywords.
        """
        if not nlp_engine:
            return []
        keywords = [
            k.lower()
            for k in lemmas
            if not nlp_engine.is_stopword(k, language)
            and not nlp_engine.is_punct(k, language)
            and k != "-PRON-"
            and k != "be"
        ]

        # best effort, try even further to break tokens into sub tokens,
        # this can result in reducing false negatives
        keywords = [i.split(":") for i in keywords]

        # splitting the list can, if happened, will result in list of lists,
        # we flatten the list
        keywords = [item for sublist in keywords for item in sublist]
        return keywords

    def to_json(self) -> str:
        """Convert nlp artifacts to json."""

        return_dict = self.__dict__.copy()

        # Ignore NLP engine as it's not serializable currently
        del return_dict['nlp_engine']

        # Converting spaCy tokens and spans to string as they are not serializable
        if "tokens" in return_dict:
            return_dict["tokens"] = [token.text for token in self.tokens]
        if "entities" in return_dict:
            return_dict["entities"] = [entity.text for entity in self.entities]

        return json.dumps(return_dict)
