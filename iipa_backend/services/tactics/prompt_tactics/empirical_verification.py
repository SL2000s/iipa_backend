from iipa_backend.services.tactics.prompt_tactics.prompt_tactic import PromptTactic
from iipa_backend.config.config import EMPIRICAL_VERIFICATION_LABEL


class EmpiricalVerifier(PromptTactic):
    def __init__(self, label=EMPIRICAL_VERIFICATION_LABEL):
        super().__init__(label)
