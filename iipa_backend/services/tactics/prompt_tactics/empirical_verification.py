from iipa_backend.config.config import EMPIRICAL_VERIFICATION_LABEL
from iipa_backend.services.prompt.llm_quest import extract_llm_ans_code
from iipa_backend.services.prompt.autogen_codegen import a_generate_code
from iipa_backend.models.prompt import Prompt, PromptAnswer
from iipa_backend.services.tactics.prompt_tactics.prompt_tactic import PromptTactic
from iipa_backend.utils.utils import execute_code_str


class EmpiricalVerifier(PromptTactic):
    def __init__(self, label=EMPIRICAL_VERIFICATION_LABEL):
        super().__init__(label)

    async def perform_tactic(self, user_prompt: Prompt):
        prompt_answer = PromptAnswer()
        template_variables = await self.user_prompt2template_variables(user_prompt)
        prompt = self.prompt_template.format(**template_variables)
        llm_ans = await a_generate_code(prompt)
        prompt_answer.answer = f"Internal AutoGen reasoning:\n{llm_ans}"
        return prompt_answer
        # llm_code_ans = await super().perform_tactic(user_prompt=user_prompt)
        # prompt_answer.latex_macros.update(llm_code_ans.latex_macros)
        # code = extract_llm_ans_code(llm_code_ans.answer)
        # execution_result = execute_code_str(code).strip('\n')
        # prompt_answer.answer = f"Code:\n```python\n{code}\n```\nExecution result:\n```\n{execution_result}\n```"
