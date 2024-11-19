from iipa_backend.config.config import EMPIRICAL_VERIFICATION_LABEL
from iipa_backend.services.prompt.llm_quest import append_prompt_context
from iipa_backend.services.prompt.autogen_codegen import a_generate_code
from iipa_backend.models.prompt import Prompt, PromptAnswer
from iipa_backend.services.tactics.prompt_tactics.prompt_tactic import PromptTactic
from iipa_backend.utils.utils import str2md
# from iipa_backend.utils.utils import execute_code_str


class EmpiricalVerifier(PromptTactic):
    def __init__(self, label=EMPIRICAL_VERIFICATION_LABEL):
        super().__init__(label)

    async def perform_tactic(self, user_prompt: Prompt, md_output: bool = True):
        template_variables = await self.user_prompt2template_variables(user_prompt)
        prompt = self.prompt_template.format(**template_variables)
        prompt_with_context, latex_macros = append_prompt_context(prompt, user_prompt.kb_label)
        llm_ans = await a_generate_code(prompt_with_context)
        if md_output:
            llm_ans = str2md(llm_ans).replace('>', '\>')
        prompt_answer = PromptAnswer(
            answer=f"**Internal AutoGen reasoning**:\n\n{llm_ans}",
            latex_macros=latex_macros,
        )
        return prompt_answer
        # llm_code_ans = await super().perform_tactic(user_prompt=user_prompt)
        # prompt_answer.latex_macros.update(llm_code_ans.latex_macros)
        # code = extract_llm_ans_code(llm_code_ans.answer)
        # execution_result = execute_code_str(code).strip('\n')
        # prompt_answer.answer = f"Code:\n```python\n{code}\n```\nExecution result:\n```\n{execution_result}\n```"
