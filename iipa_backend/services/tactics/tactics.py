from typing import Dict, List

from iipa_backend.config.config import (
    ACTIVE_TACTICS,
    EXAMPLE_NL2TACTIC_TEMPLATE,
    NL2TACTIC_TEMPLATE,
    TACTICS_DATA,
    TACTIC_STR_TEMPLATE,
)
from iipa_backend.models.prompt import Prompt
from iipa_backend.services.prompt.llm_quest import llm_quest
from iipa_backend.utils.utils import instantiate_class


class Tactics:
    def __init__(self, active_tactics: List[str] = ACTIVE_TACTICS,
                 example_nl2tactic_template: str = EXAMPLE_NL2TACTIC_TEMPLATE,
                 nl2tactic_template: str = NL2TACTIC_TEMPLATE,
                 tactics_data: Dict = TACTICS_DATA,
                 tactic_str_template: str = TACTIC_STR_TEMPLATE):
        self.tactics = self._instantiate_tactic_classes(
            active_tactics,
            tactics_data,
        )
        self.label2tactic_instance_dict = self._label2tactic_instances_dict()
        self.tactics_str = self._tactics_str(tactic_str_template)
        self.examples_nl2tactic_str = self._examples_nl2tactic_str(example_nl2tactic_template)
        self.nl2tactic_template = nl2tactic_template

    def _instantiate_tactic_classes(self, active_tactics, tactics_data):
        tactics = []
        for tactic_label in active_tactics:
            module_path = tactics_data[tactic_label]['location']['module_path']
            class_name = tactics_data[tactic_label]['location']['class_name']
            tactic = instantiate_class(module_path, class_name)
            tactics.append(tactic)
        return tactics

    def _label2tactic_instances_dict(self):
        label2tactic = {tactic.label: tactic for tactic in self.tactics}
        return label2tactic

    def _tactics_str(self, tactic_str_template):
        tactic_strs = [
            tactic_str_template.format(
                label=tactic.label,
                description=tactic.description,
                prompt=tactic.prompt_template,
            ) for tactic in self.tactics
        ]
        tactics_str = '\n\n'.join(tactic_strs)
        return tactics_str

    def _examples_nl2tactic_str(self, example_template):
        example_strs = []
        for tactic in self.tactics:
            for example in tactic.examples:
                example_str = example_template.format(
                    task=example['user_prompt'],
                    answer=tactic.label,
                )
                example_strs.append(example_str)
        examples_str = '\n\n'.join(example_strs)
        return examples_str

    def label2tactic_instance(self, label):
        return self.label2tactic_instance_dict.get(label)

    async def perform_tactic_by_label(self, label, user_prompt: Prompt, kb_label: str):
        tactic = self.label2tactic_instance(label)
        if tactic:
            ans = await tactic.perform_tactic(user_prompt, kb_label)
            return ans
        return 'Failed to find a suiting tactic'  # TODO: add proper logging and raise error

    async def nl2tactic(self, user_prompt: Prompt):
        nl2tactic_prompt = self.nl2tactic_template.format(
            tactics=self.tactics_str,
            examples=self.examples_nl2tactic_str,
            prompt=user_prompt.prompt,
        )
        ans = await llm_quest(nl2tactic_prompt)
        return ans

    async def process_user_prompt(self, user_prompt: Prompt, kb_label: str):
        # return await llm_quest(user_prompt.prompt_with_history())
        tactic_label = await self.nl2tactic(user_prompt)
        # return tactic
        ans = await self.perform_tactic_by_label(tactic_label, user_prompt, kb_label)
        return ans
