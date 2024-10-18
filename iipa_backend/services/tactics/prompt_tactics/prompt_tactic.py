from iipa_backend.models.prompt import Prompt
from iipa_backend.services.prompt.llm_quest import llm_quest
from iipa_backend.services.tactics.tactic import Tactic


class PromptTactic(Tactic):
    def __init__(self, label):
        super().__init__(label)
    
    async def perform_tactic(self, user_prompt: Prompt):
        template_variables = await self.user_prompt2template_variables(user_prompt)
        prompt = self.prompt_template_str.format(template_variables)
        llm_ans = llm_quest(prompt)
        return llm_ans

    async def user_prompt2template_variables(self, user_prompt: Prompt):
        pass
