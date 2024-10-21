from abc import ABC, abstractmethod

from iipa_backend.config.config import TACTICS_DATA


class Tactic(ABC):
    def __init__(self, label):
        self.label = label
        self.description = TACTICS_DATA[label]['description']
        self.prompt_template = TACTICS_DATA[label]['tactic_prompt_template']
        self.template_variables = TACTICS_DATA[label]['template_variables']
        self.examples = TACTICS_DATA[label].get('examples', [])

    @abstractmethod
    async def perform_tactic():
        pass
