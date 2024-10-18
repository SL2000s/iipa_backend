from iipa_backend.models.prompt import Prompt
from iipa_backend.services.tactics.tactics import Tactics


class TacticController:
    def __init__(self) -> None:
        self.tactics = Tactics()

    async def process_user_prompt(self, user_prompt: Prompt):
        answer = await self.tactics.process_user_prompt(user_prompt)
        return answer
