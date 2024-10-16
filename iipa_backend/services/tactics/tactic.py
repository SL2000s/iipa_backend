from abc import ABC, abstractmethod


class Tactic(ABC):
    @property
    @abstractmethod
    def label():
        pass

    @property
    @abstractmethod
    def description():
        pass

    @property
    @abstractmethod
    def prompt_template():
        pass
