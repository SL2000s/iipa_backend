from iipa_backend.config import TACTICS
from iipa_backend.services.prompt.config import NL2TACTIC_PROMPT_TEMPLATE
from iipa_backend.services.prompt.llm_quest import llm_quest


class PromptService:
    async def nl2tactic(self, user_prompt):
        nl2tactic_prompt = NL2TACTIC_PROMPT_TEMPLATE.format(prompt=user_prompt)
        ans = await llm_quest(nl2tactic_prompt)
        return ans

    async def process_user_prompt(self, user_prompt):
        tactic = await self.nl2tactic(user_prompt)
        return tactic
