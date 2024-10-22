from iipa_backend.services.tactics.prompt_tactics.prompt_tactic import PromptTactic
from iipa_backend.config.config import PREMISES_RETRIEVAL_LABEL


class PremisesRetriever(PromptTactic):
    def __init__(self, label=PREMISES_RETRIEVAL_LABEL):
        super().__init__(label)
