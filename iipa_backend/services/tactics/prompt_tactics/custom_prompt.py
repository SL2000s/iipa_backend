from iipa_backend.config.config import CUSTOM_PROMPT_LABEL
from iipa_backend.models.prompt import Prompt
from iipa_backend.services.prompt.llm_quest import kb_quest
from iipa_backend.services.tactics.prompt_tactics.prompt_tactic import PromptTactic


class CustomPrompt(PromptTactic):
    def __init__(self, label=CUSTOM_PROMPT_LABEL):
        super().__init__(label)

    async def perform_tactic(self, user_prompt: Prompt, kb_label: str):
        llm_ans = await kb_quest(user_prompt.prompt_with_history(), kb_label)
        return llm_ans
