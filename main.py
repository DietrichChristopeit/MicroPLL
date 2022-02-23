from math import exp
from math import fabs
from time import sleep_ms

from machine import PWM
from machine import Pin

from lib.display import OLED


def operational(pin: int = 25, pin1: int = 27) -> (PWM, PWM):
    opp: Pin = Pin(pin, Pin.OUT)
    opp.off()
    pwmOKLED: PWM = PWM(opp)
    pwmOKLED.freq(200_000)
    opp1: Pin = Pin(pin1, Pin.OUT)
    opp1.off()
    pwmOKLED1: PWM = PWM(opp1)
    pwmOKLED1.freq(200_000)
    for _ in range(3):
        for _ in range(1, 12):
            pwmOKLED.duty_u16(int(exp(_)))
            pwmOKLED1.duty_u16(int(exp(_)))
            sleep_ms(int(fabs(100 - _ * _)))
        pwmOKLED.duty_u16(0)
        pwmOKLED1.duty_u16(0)
    return pwmOKLED, pwmOKLED1


if __name__ == '__main__':
    display: OLED = OLED()

    # pwmOKLED, pwmOKLED1 = operational(28, 27)
    # sleep_ms(500)
    # pwmOKLED.duty_u16(150000)
    # pwmOKLED1.duty_u16(150000)
