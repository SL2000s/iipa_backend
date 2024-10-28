from pydantic import BaseModel, Field
from typing import List, Dict, Optional

from iipa_backend.config.config import PROMPT_WITH_HISTORY_TEMPLATE


class PromptAnswer(BaseModel):
    answer: str
    latex_macros: Optional[Dict[str, str]] = Field(default_factory=dict)


class Prompt(BaseModel):
    prompt: str
    history: List[Dict] = Field(default_factory=list)
    prompt_template: str = Field(default=PROMPT_WITH_HISTORY_TEMPLATE)
    kb_label: Optional[str] = Field(default=None)

    def history_str(self):
        history_strs = []
        for entry in self.history:
            history_strs.append(f'Prompt: {entry["prompt"]}\nAnswer: {entry["answer"]}')
        history_str = '\n'.join(history_strs) or '-'
        return history_str

    def prompt_with_history(self):
        prompt = PROMPT_WITH_HISTORY_TEMPLATE.format(
            history=self.history_str(),
            prompt=self.prompt,
        )
        return prompt
