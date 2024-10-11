from app.services.kb.kb_service import (
    add_context,
    add_premise,
    search_premise,
)
from app.services.prompt.llm_quest import llm_quest
from app.services.tactics.tactics_service import (
    expand_assumptions,
    prove,
    prove_within_context,
    verify_proof,
    verify_statement,
)


class PromptService:
    def nl2tactic(self, prompt):
        pass

    async def process_user_prompt(self, prompt):
        return "TODO: PROMPT LLM"
