from pydantic import BaseModel, Field
from typing import List, Dict

from iipa_backend.config.config import PROMPT_WITH_HISTORY_TEMPLATE


class Prompt(BaseModel):
    prompt: str
    history: List[Dict[str, str]] = Field(default_factory=list)
    prompt_template: str = Field(default=PROMPT_WITH_HISTORY_TEMPLATE)

    def history_str(self):
        history_strs = []
        for entry in self.history:
            history_strs.append(f'Prompt": {entry["prompt"]}\nAnswer: {entry["answer"]}')
        history_str = '\n'.join(history_strs) or '-'
        return history_str

    def prompt_with_history(self):
        prompt = PROMPT_WITH_HISTORY_TEMPLATE.format(
            history=self.history_str(),
            prompt=self.prompt,
        )
        return prompt

    def prompt(self):
        return self.prompt