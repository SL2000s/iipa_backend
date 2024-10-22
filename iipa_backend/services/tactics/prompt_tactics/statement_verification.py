from iipa_backend.services.tactics.prompt_tactics.prompt_tactic import PromptTactic
from iipa_backend.config.config import STATEMENT_VERIFICATION_LABEL


class StatementVerifier(PromptTactic):
    def __init__(self, label=STATEMENT_VERIFICATION_LABEL):
        super().__init__(label)
