from iipa_backend.services.tactics.prompt_tactics.prompt_tactic import PromptTactic
from iipa_backend.config.config import ENTAILMENT_VERIFICATION_LABEL


class EntailmentVerifier(PromptTactic):
    def __init__(self, label=ENTAILMENT_VERIFICATION_LABEL):
        super().__init__(label)
