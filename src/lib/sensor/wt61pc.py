"""
    lib.sensor.wt61pc

"""
from machine import Pin
from micropython import const


class Accelerometer:
    FREQUENCY_0_1HZ: int = const(0X01)
    FREQUENCY_0_5HZ: int = const(0X02)
    FREQUENCY_1HZ: int = const(0X03)
    FREQUENCY_2HZ: int = const(0X04)
    FREQUENCY_5HZ: int = const(0X05)
    FREQUENCY_10HZ: int = const(0X06)
    FREQUENCY_20HZ: int = const(0X07)
    FREQUENCY_50HZ: int = const(0X08)
    FREQUENCY_100HZ: int = const(0x09)
    FREQUENCY_125HZ: int = const(0X0A)
    FREQUENCY_200HZ: int = const(0X0B)
    
    _HEADERACC: int = const(0x51)
    _HEADERGYRO: int = const(0x52)
    _HEADERANGLE: int = const(0x53)
    _HEADER55: int = const(0x55)
    
    _TIMEOUT: int = const(5000)
    
    _XL: int = const(2)
    _XH: int = const(3)
    _YL: int = const(4)
    _YH: int = const(5)
    _ZL: int = const(6)
    _ZH: int = const(7)
    
    def __init__(self, id: int = 0, tx: int = 16, rx: int = 17, baudrate: int = 9600):
        self._id: int = id
        self._TX: Pin = Pin(tx)
        self._RX: Pin = Pin(rx)
        self._BAUD: int = baudrate
        return
