"""
    lib.sensor.bmx160

"""
import time

from machine import I2C
from machine import Pin
from micropython import const


class BMX160:
    _DEV_ADDR: int = const(0x68)
    _CHIP_ID_ADDR: int = const(0x00)
    _ERROR_REG_ADDR: int = const(0x02)
    _MAG_DATA_ADDR: int = 0x04
    _GYRO_DATA_ADDR: int = const(0x0C)
    _ACCEL_DATA_ADDR: int = const(0x12)
    _STATUS_ADDR: int = const(0x1B)
    _INT_STATUS_ADDR: int = const(0x1C)
    _FIFO_LENGTH_ADDR: int = const(0x22)
    _FIFO_DATA_ADDR: int = const(0x24)
    _ACCEL_CONFIG_ADDR: int = const(0x40)
    _ACCEL_RANGE_ADDR: int = const(0x41)
    _GYRO_CONFIG_ADDR: int = const(0x42)
    _GYRO_RANGE_ADDR: int = const(0x43)
    _MAGN_CONFIG_ADDR: int = const(0x44)
    _FIFO_DOWN_ADDR: int = const(0x45)
    _FIFO_CONFIG_0_ADDR: int = const(0x46)
    _FIFO_CONFIG_1_ADDR: int = const(0x47)
    _MAGN_RANGE_ADDR: int = const(0x4B)
    _MAGN_IF_0_ADDR: int = const(0x4C)
    _MAGN_IF_1_ADDR: int = const(0x4D)
    _MAGN_IF_2_ADDR: int = const(0x4E)
    _MAGN_IF_3_ADDR: int = const(0x4F)
    _INT_ENABLE_0_ADDR: int = const(0x50)
    _INT_ENABLE_1_ADDR: int = const(0x51)
    _INT_ENABLE_2_ADDR: int = const(0x52)
    _INT_OUT_CTRL_ADDR: int = const(0x53)
    _INT_LATCH_ADDR: int = const(0x54)
    _INT_MAP_0_ADDR: int = const(0x55)
    _INT_MAP_1_ADDR: int = const(0x56)
    _INT_MAP_2_ADDR: int = const(0x57)
    _INT_DATA_0_ADDR: int = const(0x58)
    _INT_DATA_1_ADDR: int = const(0x59)
    _INT_LOWHIGH_0_ADDR: int = const(0x5A)
    _INT_LOWHIGH_1_ADDR: int = const(0x5B)
    _INT_LOWHIGH_2_ADDR: int = const(0x5C)
    _INT_LOWHIGH_3_ADDR: int = const(0x5D)
    _INT_LOWHIGH_4_ADDR: int = const(0x5E)
    _INT_MOTION_0_ADDR: int = const(0x5F)
    _INT_MOTION_1_ADDR: int = const(0x60)
    _INT_MOTION_2_ADDR: int = const(0x61)
    _INT_MOTION_3_ADDR: int = const(0x62)
    _INT_TAP_0_ADDR: int = const(0x63)
    _INT_TAP_1_ADDR: int = const(0x64)
    _INT_ORIENT_0_ADDR: int = const(0x65)
    _INT_ORIENT_1_ADDR: int = const(0x66)
    _INT_FLAT_0_ADDR: int = const(0x67)
    _INT_FLAT_1_ADDR: int = const(0x68)
    _FOC_CONF_ADDR: int = const(0x69)
    _CONF_ADDR: int = const(0x6A)
    _IF_CONF_ADDR: int = const(0x6B)
    _SELF_TEST_ADDR: int = const(0x6D)
    _OFFSET_ADDR: int = const(0x71)
    _OFFSET_CONF_ADDR: int = const(0x77)
    _INT_STEP_CNT_0_ADDR: int = const(0x78)
    _INT_STEP_CONFIG_0_ADDR: int = const(0x7A)
    _INT_STEP_CONFIG_1_ADDR: int = const(0x7B)
    _COMMAND_REG_ADDR: int = const(0x7E)
    
    _SOFT_RESET_CMD: bytes = b'\xB6'
    _MAGN_UT_LSB: float = 0.3
    
    _GYRO_SENSITIVITY_125DPS: float = 0.0038110
    _GYRO_SENSITIVITY_250DPS: float = 0.0076220
    _GYRO_SENSITIVITY_500DPS: float = 0.0152439
    _GYRO_SENSITIVITY_1000DPS: float = 0.0304878
    _GYRO_SENSITIVITY_2000DPS: float = 0.0609756
    
    _GYRO_RANGE_125DPS: int = const(0x00)
    _GYRO_RANGE_250DPS: int = const(0x01)
    _GYRO_RANGE_500DPS: int = const(0x02)
    _GYRO_RANGE_1000DPS: int = const(0x03)
    _GYRO_RANGE_2000DPS: int = const(0x04)
    
    _ACCEL_SENSITIVITY_2G: float = 0.000061035
    _ACCEL_SENSITIVITY_4G: float = 0.000122070
    _ACCEL_SENSITIVITY_8G: float = 0.000244141
    _ACCEL_SENSITIVITY_16G: float = 0.000488281
    
    _ACCEL_RANGE_2G: int = _GYRO_RANGE_125DPS
    _ACCEL_RANGE_4G: int = _GYRO_RANGE_250DPS
    _ACCEL_RANGE_8G: int = _GYRO_RANGE_500DPS
    _ACCEL_RANGE_16G: int = _GYRO_RANGE_1000DPS
    
    def __init__(self, i2c_bus: int = 0, sda: int = 8, scl: int = 9):
        self._sda: Pin = Pin(sda)
        self._scl: Pin = Pin(scl)
        self._i2c: I2C = I2C(i2c_bus, sda=self._sda, scl=self._scl)
        self._GYRO_RANGE: int = self._GYRO_RANGE_250DPS
        self._GYRO_SENSITIVITY: float = self._GYRO_SENSITIVITY_250DPS
        self._ACCEL_RANGE: int = self._ACCEL_RANGE_2G
        self._ACCEL_SENSITIVITY: float = self._ACCEL_SENSITIVITY_2G
        
        time.sleep(0.16)
        return
    
    def begin(self) -> bool:
        """Initialization of the sensor.

        """
        if not self._i2c.scan():
            return False
        else:
            print(f"Sensor at: {self._i2c.scan()}")
            self.soft_reset()
            self._i2c.writeto_mem(self._DEV_ADDR, self._COMMAND_REG_ADDR, b'\x11')
            time.sleep(0.05)
            self._i2c.writeto_mem(self._DEV_ADDR, self._COMMAND_REG_ADDR, b'\x15')
            time.sleep(0.1)
            self._i2c.writeto_mem(self._DEV_ADDR, self._COMMAND_REG_ADDR, b'\x19')
            time.sleep(0.01)
            self.set_magn_conf()
            return True
    
    def set_low_power(self) -> None:
        """Switch into low power mode.

                Disable the
                    1. magn
                    2. gyro sensor
                to reduce power consumption.

        """
        self.soft_reset()
        time.sleep(0.1)
        self.set_magn_conf()
        time.sleep(0.1)
        self._i2c.writeto_mem(self._DEV_ADDR, self._COMMAND_REG_ADDR, b'\x12')
        time.sleep(0.1)
        self._i2c.writeto_mem(self._DEV_ADDR, self._COMMAND_REG_ADDR, b'\x17')
        time.sleep(0.1)
        self._i2c.writeto_mem(self._DEV_ADDR, self._COMMAND_REG_ADDR, b'\x1B')
        time.sleep(0.1)
        return
    
    def wake_up(self) -> None:
        """Enabled the magn, gyro sensor

        """
        self.soft_reset()
        time.sleep(0.1)
        self.set_magn_conf()
        time.sleep(0.1)
        self._i2c.writeto_mem(self._DEV_ADDR, self._COMMAND_REG_ADDR, b'\x11')
        time.sleep(0.1)
        self._i2c.writeto_mem(self._DEV_ADDR, self._COMMAND_REG_ADDR, b'\x15')
        time.sleep(0.1)
        self._i2c.writeto_mem(self._DEV_ADDR, self._COMMAND_REG_ADDR, b'\x19')
        time.sleep(0.1)
        return
    
    def soft_reset(self) -> bool:
        """Resets BMX160 hardware

          :return: True
        """
        self._i2c.writeto_mem(self._DEV_ADDR, self._COMMAND_REG_ADDR, self._SOFT_RESET_CMD)
        time.sleep(0.015)
        return True
    
    def set_magn_conf(self) -> None:
        """Set magnetometer configuration.

          :return: None
        """
        self._i2c.writeto_mem(self._DEV_ADDR, self._MAGN_IF_0_ADDR, b'\x80')
        time.sleep(0.05)
        self._i2c.writeto_mem(self._DEV_ADDR, self._MAGN_IF_3_ADDR, b'\x01')
        self._i2c.writeto_mem(self._DEV_ADDR, self._MAGN_IF_2_ADDR, b'\x4B')
        self._i2c.writeto_mem(self._DEV_ADDR, self._MAGN_IF_3_ADDR, b'\x04')
        self._i2c.writeto_mem(self._DEV_ADDR, self._MAGN_IF_2_ADDR, b'\x51')
        self._i2c.writeto_mem(self._DEV_ADDR, self._MAGN_IF_3_ADDR, b'\x0E')
        self._i2c.writeto_mem(self._DEV_ADDR, self._MAGN_IF_2_ADDR, b'\x52')
        
        self._i2c.writeto_mem(self._DEV_ADDR, self._MAGN_IF_3_ADDR, b'\x02')
        self._i2c.writeto_mem(self._DEV_ADDR, self._MAGN_IF_2_ADDR, b'\x4C')
        self._i2c.writeto_mem(self._DEV_ADDR, self._MAGN_IF_1_ADDR, b'\x42')
        self._i2c.writeto_mem(self._DEV_ADDR, self._MAGN_CONFIG_ADDR, b'\x08')
        self._i2c.writeto_mem(self._DEV_ADDR, self._MAGN_IF_0_ADDR, b'\x03')
        time.sleep(0.05)
        return
    
    @property
    def GYRO_RANGE(self) -> int:
        return self._GYRO_RANGE
    
    @GYRO_RANGE.setter
    def GYRO_RANGE(self, gRange: int) -> None:
        self._GYRO_RANGE = gRange
        return
    
    @property
    def GYRO_SENSITIVITY(self) -> float:
        return self._GYRO_SENSITIVITY
    
    @GYRO_SENSITIVITY.setter
    def GYRO_SENSITIVITY(self, bits: int) -> None:
        """Set gyroscope angular rate range and resolution.

          :param bits: int
            GyroRange_125DPS
                Gyroscope sensitivity at 125dps
            GyroRange_250DPS
                Gyroscope sensitivity at 250dps
            GyroRange_500DPS
                Gyroscope sensitivity at 500dps
            GyroRange_1000DPS
                Gyroscope sensitivity at 1000dps
            GyroRange_2000DPS
                Gyroscope sensitivity at 2000dps
        """
        if bits == 0:
            self._GYRO_SENSITIVITY = self._GYRO_SENSITIVITY_125DPS
        elif bits == 1:
            self._GYRO_SENSITIVITY = self._GYRO_SENSITIVITY_250DPS
        elif bits == 2:
            self._GYRO_SENSITIVITY = self._GYRO_SENSITIVITY_500DPS
        elif bits == 3:
            self._GYRO_SENSITIVITY = self._GYRO_SENSITIVITY_1000DPS
        elif bits == 4:
            self._GYRO_SENSITIVITY = self._GYRO_SENSITIVITY_2000DPS
        else:
            self._GYRO_SENSITIVITY = self._GYRO_SENSITIVITY_250DPS
        return
    
    @property
    def ACCEL_SENSITIVITY(self) -> float:
        return self._ACCEL_SENSITIVITY
    
    @ACCEL_SENSITIVITY.setter
    def ACCEL_SENSITIVITY(self, aRange: int) -> None:
        """Set the Accelerometer Sensitivity.
        
        """
        if aRange == 0:
            self.ACCEL_SENSITIVITY = self._ACCEL_SENSITIVITY_2G
        elif aRange == 1:
            self.ACCEL_SENSITIVITY = self._ACCEL_SENSITIVITY_4G
        elif aRange == 2:
            self.ACCEL_SENSITIVITY = self._ACCEL_SENSITIVITY_8G
        elif aRange == 3:
            self.ACCEL_SENSITIVITY = self._ACCEL_SENSITIVITY_16G
        else:
            self.ACCEL_SENSITIVITY = self._ACCEL_SENSITIVITY_2G
    
    def get_all_data(self) -> [int]:
        """Return all current sensor data: magn, gyro and accel data

        :return: [int]
            the values of the magnetometer, gyroscope and accelerometer
        """
        data = self._i2c.readfrom_mem(self._DEV_ADDR, self._MAG_DATA_ADDR, 20)
        if data[1] & 0x80:
            magnx = - 0x10000 + ((data[1] << 8) | (data[0]))
        else:
            magnx = (data[1] << 8) | (data[0])
        if data[3] & 0x80:
            magny = - 0x10000 + ((data[3] << 8) | (data[2]))
        else:
            magny = (data[3] << 8) | (data[2])
        if data[5] & 0x80:
            magnz = - 0x10000 + ((data[5] << 8) | (data[4]))
        else:
            magnz = (data[5] << 8) | (data[4])
        
        if data[9] & 0x80:
            gyrox = - 0x10000 + ((data[9] << 8) | (data[8]))
        else:
            gyrox = (data[9] << 8) | (data[8])
        if data[11] & 0x80:
            gyroy = - 0x10000 + ((data[11] << 8) | (data[10]))
        else:
            gyroy = (data[11] << 8) | (data[10])
        if data[13] & 0x80:
            gyroz = - 0x10000 + ((data[13] << 8) | (data[12]))
        else:
            gyroz = (data[13] << 8) | (data[12])
        
        if data[15] & 0x80:
            accelx = - 0x10000 + ((data[15] << 8) | (data[14]))
        else:
            accelx = (data[15] << 8) | (data[14])
        if data[17] & 0x80:
            accely = - 0x10000 + ((data[17] << 8) | (data[16]))
        else:
            accely = (data[17] << 8) | (data[16])
        if data[19] & 0x80:
            accelz = - 0x10000 + ((data[19] << 8) | (data[18]))
        else:
            accelz = (data[19] << 8) | (data[18])
        
        magnx *= self._MAGN_UT_LSB
        magny *= self._MAGN_UT_LSB
        magnz *= self._MAGN_UT_LSB
        
        gyrox *= self._GYRO_SENSITIVITY
        gyroy *= self._GYRO_SENSITIVITY
        gyroz *= self._GYRO_SENSITIVITY
        
        accelx *= self._ACCEL_SENSITIVITY * 9.80665
        accely *= self._ACCEL_SENSITIVITY * 9.80665
        accelz *= self._ACCEL_SENSITIVITY * 9.80665
        return [magnx, magny, magnz, gyrox, gyroy, gyroz, accelx, accely, accelz]


def main() -> None:
    gyro: BMX160 = BMX160()
    gyro.begin()
    while True:
        print(gyro.get_all_data())
        time.sleep_ms(1000)
    return


if __name__ == '__main__':
    main()
