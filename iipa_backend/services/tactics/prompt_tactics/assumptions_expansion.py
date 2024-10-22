from iipa_backend.services.tactics.prompt_tactics.prompt_tactic import PromptTactic
from iipa_backend.config.config import ASSUMPTIONS_EXPANSION_LABEL


class AssumptionsExpander(PromptTactic):
    def __init__(self, label=ASSUMPTIONS_EXPANSION_LABEL):
        super().__init__(label)
