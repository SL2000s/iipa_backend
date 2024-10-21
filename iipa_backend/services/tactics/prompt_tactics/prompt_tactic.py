import json

from iipa_backend.config.config import (
    EXAMPLE_PROMPT2TEMPLATE_VARIABLES_TEMPLATE,
    PROMPT2TEMPLATE_VARIABLES_TEMPLATE,
)
from iipa_backend.models.prompt import Prompt
from iipa_backend.services.prompt.llm_quest import (
    llm_quest,
)
from iipa_backend.services.tactics.tactic import Tactic


class PromptTactic(Tactic):
    def __init__(
        self, label: str,
        example_prompt2template_variables_template: str = EXAMPLE_PROMPT2TEMPLATE_VARIABLES_TEMPLATE,
        prompt2template_variables_template: str = PROMPT2TEMPLATE_VARIABLES_TEMPLATE,
    ):
        super().__init__(label)
        self.prompt2template_variables_template = prompt2template_variables_template
        self.examples_template_variables_str = self._examples_template_variables_str(
            example_prompt2template_variables_template,
        )

    def _examples_template_variables_str(self, example_template):
        example_strs = []
        for example in self.examples:
            example_str = example_template.format(
                user_prompt=example['user_prompt'],
                answer=json.dumps(example['template_variables']),
            )
            example_strs.append(example_str)
        examples_str = '\n\n'.join(example_strs)
        return examples_str

    async def perform_tactic(self, user_prompt: Prompt):
        template_variables = await self.user_prompt2template_variables(user_prompt)
        prompt = self.prompt_template.format(**template_variables)
        llm_ans = await llm_quest(prompt)
        return llm_ans

    async def user_prompt2template_variables(self, user_prompt: Prompt):
        prompt = self.prompt2template_variables_template.format(
            prompt_template=self.prompt_template,
            template_variables=self.template_variables,
            examples=self.examples_template_variables_str,
            user_prompt=user_prompt.prompt,                             # TODO: add history
        )
        llm_ans = await llm_quest(prompt, extract_code=True)
        template_variables = json.loads(llm_ans)
        return template_variables
