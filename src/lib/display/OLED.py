"""
    pipicoio.display.OLED

"""
from machine import Pin
from machine import I2C
from ssd1306 import SSD1306_I2C
from time import sleep_ms

class OLED(SSD1306_I2C):
    def __init__(self, id: str='disp_0', init_text: str=None, x: int=0, y: int=0):
        self._id: str = id
        self._i2c_conn: I2C = I2C(0,sda=Pin(0), scl=Pin(1), freq=400_000)
        super().__init__(128, 64, self._i2c_conn)
        self.fill(0)
        self._cur_text: str = None
        if init_text is not None:
            self._cur_text = init_text
        else:
            self._cur_text = id
        self.text(self._cur_text, x, y)
        self.show()
        return
    
    @property
    def i2c_conn(self) -> I2C:
        return self._i2c_conn

    @i2c_conn.setter
    def i2c_conn(self, i2c_conn: I2C) -> None:
        self._i2c_conn = i2c_conn
        return
    
    @property
    def cur_text(self) -> str:
        return self._cur_text
    
    @cur_text.setter
    def cur_text(self, text: str) -> None:
        self._cur_text = text
        return
    

if __name__ == '__main__':
    
    oled: OLED = OLED()
    sleep_ms(8000)
    oled.fill(0)
    oled.text("HO LALLES", 0, 0)
    oled.show()
    sleep_ms(8000)
    oled.fill(0)
    oled.text("LALLES, I SAY", 0, 0)
    oled.text("Showing img now", 0, 50)
    oled.show()
    sleep_ms(1500)
    oled.fill(0)
    oled.fill_rect(0, 0, 64, 32, 1)
    oled.show()
