from iipa_backend.services.tactics.prompt_tactics.prompt_tactic import PromptTactic
from iipa_backend.config.config import PROOF_IN_CONTEXT_LABEL


class ProverInContext(PromptTactic):
    def __init__(self, label=PROOF_IN_CONTEXT_LABEL):
        super().__init__(label)
