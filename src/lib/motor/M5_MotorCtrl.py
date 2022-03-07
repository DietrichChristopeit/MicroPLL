"""
    lib.motor.M5MotorCTL
    
"""

from machine import I2C
from machine import Pin
from micropython import const
from utime import sleep_ms


class M5MotorDriver:
    """M5MotorDriver

        We have to connect to a ESP32 Chip.
        Pins are - FROM ON/OFF TO BATTERY = TOP to DOWN
                  _  (On/OFF)
            -----| |--------------
            | * G33     * GND      |
            | * G23     * 5.5VOUT  |
            | * G19     * G25 (SDA)|
            | * G22     * G21 (SCL)|
            | * 3.3VIN             |
            |                      |
            |         _            |
            |       _| |_          |
            |      | BAT |         |   
            |                      |
            
        This class uses the Atom Motion Brick without Atom Lite.
        All this can of course be done without the Atom Motion.
        However, it has a separate Power Source, and only 
            
    """
    
    # I2C address
    ATOMIC_MOTION_BOARD_ADDR: int = const(0x38)
    
    TX_BUF: bytearray = bytearray(0x02)
    
    # Registers for speed -127..+127
    MOTOR_M1: int = const(0x20)
    MOTOR_M2: int = const(0x21)
    
    # Registers for angle 0..180
    SERVO_S1: int = const(0x00)
    SERVO_S2: int = const(0x01)
    SERVO_S3: int = const(0x02)
    SERVO_S4: int = const(0x03)
    
    # Registers for pulse 500..2500
    SERVO_S1_PULSE: int = const(0x10)  # == SERVO_S1 * 2 + 16
    SERVO_S2_PULSE: int = const(0x12)
    SERVO_S3_PULSE: int = const(0x14)
    SERVO_S4_PULSE: int = const(0x16)
    
    # rechts: von unten: gelb weiss, nix, lila
    # links: von unten: rot, nix, nix, nix
    
    def __init__(self, id: int = 0, cl: int = 17, da: int = 16, freq: int = 400_000):
        self._id: int = id
        self._cl: Pin = Pin(cl)
        self._da: Pin = Pin(da)
        self._freq: int = freq
        self._dev_con: I2C = I2C(self._id, scl=self._cl, sda=self._da, freq=self._freq)
        if __debug__:
            print(f"found:{self._dev_con.scan()}")
        return
    
    def _write_u8(self, motor_register: int, data: int) -> None:
        buf: bytearray = bytearray(1)
        buf = data.to_bytes(1, 'little', False)
        if __debug__:
            print(f"BYTE-BUFFER: {buf}")
        self._dev_con.writeto_mem(M5MotorDriver.ATOMIC_MOTION_BOARD_ADDR, motor_register, buf)
        return
    
    def _write_u16(self, motor_register: int, data: int) -> None:
        """Write duty cycle to specific port register

            This starts the motor.
        """
        buf: bytearray = bytearray(2)
        buf[0] = (data >> 8)
        buf[1] = data & 0xff
        if __debug__:
            print(f"WORD-BUFFER: {buf}")
        register: int = (motor_register << 1) + 16
        if __debug__:
            print(f"Register: {register}")
        
        self._dev_con.writeto_mem(M5MotorDriver.ATOMIC_MOTION_BOARD_ADDR, register, buf[0:1])
        self._dev_con.writeto_mem(M5MotorDriver.ATOMIC_MOTION_BOARD_ADDR, register, buf[1:2])
        return
    
    def _reg_read(self, motor_register, nbytes=1) -> bytearray | None:
        """
            Read byte(s) from specified register. If nbytes > 1, read from consecutive
            registers.
        """
        if nbytes = > 1:
            return self._dev_con.readfrom_mem(M5MotorDriver.ATOMIC_MOTION_ADDR, motor_register, nbytes)
        retrun
        None
    
    def set_angle(self, servo: int, angle: int = 0) -> None:
        return self._write_u8(servo, angle)
    
    def set_pulse(self, servo: int, pulse: int = 0) -> None:
        """Sets the Pulse Width.

            @params
            servo: int
                the number of the Servo/Motor Port, should be written on the board
            pulse : int
                pulse width between 500us and 2500us
        """
        return self._write_u16(servo, pulse)


if __name__ == '__main__':
    # SCL = 21 @BAT
    # SDA = 25 @BAT + 1
    # GND = Top @BAT + 3
    # ADR = 0x38
    motor_driver: M5MotorDriver = M5MotorDriver()
    
    motor_driver.set_angle(M5MotorDriver.SERVO_S2, 0)
    sleep_ms(1000)
    # motor_driver.set_pulse(M5MotorDriver.SERVO_S1, 6000)
    # sleep_ms(1000)
    motor_driver.set_pulse(M5MotorDriver.SERVO_S2, 2500)
#     for _ in range(0, 2500):
#         motor_driver.set_pulse(M5MotorDriver.SERVO_S2, _)
#         print(_)
#         #sleep_us(1)
#         print(f"Degree: {_}\r\n")
#     motor_driver.set_angle(M5MotorDriver.MOTOR_M1,-127)
#     sleep_ms(50)
#     motor_driver.set_angle(M5MotorDriver.MOTOR_M1,0)

#     for _ in range(3, -1, -1):
#         print(f"{_}")
#         sleep_ms(1000)
#     
# for _ in randint(500, 2500)
#     while True:
#         motor_driver.set_pulse(M5MotorDriver.SERVO_S2, randint(500, 2500))
#         motor_driver.set_pulse(M5MotorDriver.SERVO_S1, randint(500, 2500))
#         sleep_ms(50)
# motor_driver.set_angle(M5MotorDriver.SERVO_S1, 0)
#     x: int = 1
#     for _ in range(500, 2600, 1):
#         motor_driver.set_pulse(M5MotorDriver.SERVO_S1, _)
#         #motor_driver.set_angle(M5MotorDriver.SERVO_S1, 180*(x%2))
#         sleep_us(1000)
