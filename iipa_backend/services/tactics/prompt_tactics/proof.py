from iipa_backend.services.tactics.prompt_tactics.prompt_tactic import PromptTactic
from iipa_backend.config.config import PROOF_LABEL


class Prover(PromptTactic):
    def __init__(self, label=PROOF_LABEL):
        super().__init__(label)
