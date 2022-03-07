"""
    lib.sensor.Accelerometer_DFRobot

"""


class Accelerometer:
    FREQUENCY_0_1HZ
    0X01
    FREQUENCY_0_5HZ
    0X02
    FREQUENCY_1HZ
    0X03
    FREQUENCY_2HZ
    0X04
    FREQUENCY_5HZ
    0X05
    FREQUENCY_10HZ
    0X06
    FREQUENCY_20HZ
    0X07
    FREQUENCY_50HZ
    0X08
    FREQUENCY_100HZ
    0X09
    FREQUENCY_125HZ
    0X0A
    FREQUENCY_200HZ
    0X0B
    
    def __init__(self, id: int = 0, tx: int = 16, rx: int = 17):
        self._id: int =
