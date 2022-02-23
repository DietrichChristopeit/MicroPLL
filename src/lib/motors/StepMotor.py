"""
    lib.StepMotor.py

"""
from machine import Pin
from ucollections import OrderedDict

"""This class enables the access of a Stepmotor.

Additionally a motor Driver is needed that 
    1. Facilitates an independent power source -- most motors require an input of 5V which can do serious harm to the Pi Pico.
    
        a. Make sure to guard the Pi Pico from currents caused by self induction that essentially gflow back into the Pi Pico. This can be done with a shunt
    
    2. Connect all cables -- depending on motor 3 or 4:
        
"""
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
