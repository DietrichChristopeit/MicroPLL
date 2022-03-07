"""
    lib.sensor.minitof
"""
from machine import Pin
from machine import UART
from micropython import const


class TOFLidar:
    """
    This class implements the whadda|copy| ToF Lidar Sensor:
        WPM349

    """
    """
    Constants
    
    """
    _BAUD_RATE: int = const(115200)
    _MAX_BYTES_BEFORE_HEADER: int = const(30)
    _MAX_MEASUREMENT_ATTEMPTS: int = const(10)
    
    _READY: int = const(0)
    _ERROR_SERIAL_NOHEADER: int = const(1)
    _ERROR_SERIAL_BADCHECKSUM: int = const(2)
    _ERROR_SERIAL_TOOMANYTRIES: int = const(3)
    _MEASUREMENT_OK: int = const(10)
    _CMD_HEADER: bytearray = bytearray([0x42, 0x57, 0x02, ])
    _C_STANDARDOUTPUT_MODE_S: bytearray = bytearray(_CMD_HEADER + bytearray([0x00, 0x00, 0x00, 0x01, 0x06, ]))
    _C_CONFIG_MODE_S: bytearray = bytearray(_CMD_HEADER + bytearray([0x00, 0x00, 0x00, 0x01, 0x02, ]))
    _C_SINGLESCAN_MODE_S: bytearray = bytearray(
        _C_CONFIG_MODE_S + _CMD_HEADER + bytearray([0x00, 0x00, 0x00, 0x01, 0x00, 0x40, ])
        )
    _C_SEND_EXTERNAL_TRIGGER: bytearray = bytearray(
        _C_CONFIG_MODE_S + _CMD_HEADER + bytearray([0x00, 0x00, 0x00, 0x01, 0x00, 0x41, ])
        )
    
    def __init__(self, bus_id: int = 0, tx: int = 16, rx: int = 17):
        self._TX: Pin = Pin(tx)
        self._RX: Pin = Pin(rx)
        self._RX_BUF: bytearray = bytearray(0x00 * 9)
        self._dev_con: UART = UART(bus_id, self._BAUD_RATE, tx=self._TX, rx=self._RX, rxbuf=9)
        self._distance: int = -1
        self._strength: int = -1
        self._state: int = self._READY
        v: int = self.set_mode(self._C_STANDARDOUTPUT_MODE_S)
        print(f"written {v} bytes")
        return
    
    @property
    def C_STANDARDOUTPUT_MODE_S(self) -> bytearray:
        return self._C_STANDARDOUTPUT_MODE_S
    
    @property
    def dev_con(self) -> UART:
        return self._dev_con
    
    @property
    def rx_buf(self) -> bytearray:
        return self._RX_BUF
    
    def set_mode(self, mode_cmd: bytearray = None) -> int | None:
        """
        
        :param mode_cmd: bytearray | None
        
        :return:
            int | None: the number of bytes successfully written
        """
        return self._dev_con.write(bytearray(mode_cmd))
    
    def take_measurement(self) -> bytes:
        return self._dev_con.read()  # _RX_BUF should be set implicitly


if __name__ == '__main__':
    lidar: TOFLidar = TOFLidar()
    # lidar.set_mode(bytearray(lidar.C_STANDARDOUTPUT_MODE_S))
    lidar.take_measurement()
