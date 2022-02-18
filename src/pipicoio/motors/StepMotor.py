from machine import Pin
from ucollections import OrderedDict


class StepMotor:

    def __init__(self, phasePinMap: OrderedDict[str, int]=None, base_freq: int=1_500, phase_cycle_freq: int=1, cycle_sentence: str='AABBBCCCDD', step_time_us: float=1.5):
        """
        Lorem Ipsum

        :type phasePinMap: OrderedDict[str, int]
        """

        self._phasePins: OrderedDict[str, Pin] = OrderedDict()

        if phasePinMap is None:
            self._phasePinMap: OrderedDict[str, int] = OrderedDict({'A': 16, 'B': 17, 'C': 18, 'D': 19})
        else:
            self._phasePinMap: OrderedDict[str, int] = phasePinMap
        for name, pin in self._phasePinMap.items():
            self._phasePins[name] = Pin(pin, Pin.OUT)
            self._phasePins[name].low()
        self._base_freq: int = base_freq
        self._phase_cycle_freq: int = phase_cycle_freq
        self._cycle_sentence: str = cycle_sentence
        self._step_time_us: float = step_time_us

        return
