from iipa_backend.models.prompt import Prompt
from iipa_backend.services.prompt.prompt_service import PromptService


class PromptController:
    def __init__(self) -> None:
        self.prompt_service = PromptService()

    async def process_prompt(self, prompt: Prompt):
        answer = await self.prompt_service.process_user_prompt(prompt)
        return answer
