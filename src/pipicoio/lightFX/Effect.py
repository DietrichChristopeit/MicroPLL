"""
    pipicoio.lightFX.Effect.py

"""
from abc import ABC
from abc import abstractmethod

class Effect(ABC):


    @abstractmethod
    def pwf(self, start: int, end: int) -> None:
        """

        :rtype: int
        """
        raise NotImplementedError

    @abstractmethod
    def run_effect(self) -> None:
        raise NotImplementedError
