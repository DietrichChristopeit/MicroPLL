"""
    pipicoio.lightFX.FlashLED.py

"""
from machine import Pin

from lib.lightFX.Effect import Effect


class FlashLED(Effect):

    def __init__(self, ledPin: Pin=None):
        super(FlashLED, self).__init__()
        self._ledPin = ledPin
        return

    def pwf(self, start: int, end: int) -> None:
        pass
