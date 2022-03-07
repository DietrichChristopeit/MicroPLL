"""
    lib.motor.motorctrl

"""
from math import floor
from time import sleep_ms
from time import ticks_diff
from time import ticks_ms

from machine import PWM
from machine import Pin


class PWM_Motor_CTRL(PWM):
    
    def __init__(self, ctrl_pin: int = 15, frequency: int = 50):
        super().__init__(Pin(ctrl_pin, Pin.OUT))
        self.freq(frequency)
        self._last_runtime = ticks_ms()
        return
    
    @property
    def last_runtime(self):
        return self._last_runtime
    
    @last_runtime.setter
    def last_runtime(self, lrt: int) -> None:
        self._last_runtime = lrt
        return
    
    def run(self, speed: int = 0, direction: int = 1):
        self.last_runtime = ticks_ms()
        if direction == 1:
            self.duty_u16(4700 - floor(speed * 2900 / 100))
        elif direction == -1:
            self.duty_u16(5000 + floor(speed * 2900 / 100))
        return
    
    def run_for(self, t: int = 0, speed: int = 0, direction: int = 1):
        self.run(speed=speed, direction=direction)
        sleep_ms(t)
        self.stop()
        return
    
    def stop(self):
        self.deinit()
        self.last_runtime = ticks_diff(ticks_ms(), self.last_runtime)
        return


if __name__ == '__main__':
    # slowest: 4667 cw -> 4700
    # fastest: 1800 cw
    # delta: 2867 cw
    # slowest: 5030 ccw
    # fastest: 7897 ccw
    # delta stop: 363
    
    m: PWM_Motor_CTRL = PWM_Motor_CTRL()
    m.run_for(t=100, speed=90, direction=-1)
    # for _ in range(1, 101):
    #   m.run_for(t=100, speed=_, direction=1)
    #     for _ in range(101, 1, -1):
    #         m.run_for(t=5, speed=_, direction=1)
    #     for _ in range(1, 101):
    #         m.run_for(t=5, speed=_, direction=-1)
    #     for _ in range(101, 1, -1):
    #         m.run_for(t=5, speed=_, direction=-1)
    
    print(f"Last Run time: {m.last_runtime}ms")
