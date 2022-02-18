"""
    lib/epd_2in9ws_rp2.py
    
"""
# *****************************************************************************
# * | File        :	  Pico_ePaper-2.9.py
# * | Author      :   Waveshare team
# * | Function    :   Electronic paper driver
# * | Info        :
# *----------------
# * | This version:   V1.0
# * | Date        :   2021-03-16
# # | Info        :   python demo
# -----------------------------------------------------------------------------
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documnetation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to  whom the Software is
# furished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS OR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

from utime import sleep_ms

import framebuf
from machine import Pin
from machine import SPI


class EPD_2in9(framebuf.FrameBuffer):

    WF_PARTIAL_2IN9: [int] = [
        0x0,0x40,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,
        0x80,0x80,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,
        0x40,0x40,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,
        0x0,0x80,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,
        0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,
        0x0A,0x0,0x0,0x0,0x0,0x0,0x1,
        0x1,0x0,0x0,0x0,0x0,0x0,0x0,
        0x1,0x0,0x0,0x0,0x0,0x0,0x0,
        0x0,0x0,0x0,0x0,0x0,0x0,0x0,
        0x0,0x0,0x0,0x0,0x0,0x0,0x0,
        0x0,0x0,0x0,0x0,0x0,0x0,0x0,
        0x0,0x0,0x0,0x0,0x0,0x0,0x0,
        0x0,0x0,0x0,0x0,0x0,0x0,0x0,
        0x0,0x0,0x0,0x0,0x0,0x0,0x0,
        0x0,0x0,0x0,0x0,0x0,0x0,0x0,
        0x0,0x0,0x0,0x0,0x0,0x0,0x0,
        0x0,0x0,0x0,0x0,0x0,0x0,0x0,
        0x22,0x22,0x22,0x22,0x22,0x22,0x0,0x0,0x0,
        0x22,0x17,0x41,0xB0,0x32,0x36,
        ]


    def __init__(self, RST_PIN: int=12, DC_PIN: int=8, CS_PIN: int=9, BUSY_PIN: int=13, EPD_WIDTH: int=128, EPD_HEIGHT: int=296, portrait: bool=True):
        self._window: (int, int, int, int) = None
        self._cursor: (int, int) = None
        self._reset_pin: Pin = Pin(RST_PIN, Pin.OUT)

        self._busy_pin: Pin = Pin(BUSY_PIN, Pin.IN, Pin.PULL_UP)
        self._cs_pin: Pin = Pin(CS_PIN, Pin.OUT)
        self._dc_pin: Pin = Pin(DC_PIN, Pin.OUT)
        if portrait is True:
            self._width: int = EPD_WIDTH
            self._height: int = EPD_HEIGHT
        else:
            self._width: int = EPD_HEIGHT
            self._height: int = EPD_WIDTH

        self._lut: [int] = self.WF_PARTIAL_2IN9

        self._spi: SPI = SPI(1)
        self._spi.init(baudrate=4000_000)


        self._buffer: bytearray = bytearray(self._height * self._width // 8)
        super().__init__(self._buffer, self._width, self._height, framebuf.MONO_HLSB)
        self.prepare_display()
        return

    def spi_writebyte(self, data):
        self._spi.write(bytearray(data))
        return

    def off(self):
        self._reset_pin.value(0)
        return

    # Hardware reset
    def reset(self):
        self._reset_pin.value(1)
        sleep_ms(50)
        self._reset_pin.value(0)
        sleep_ms(2)
        self._reset_pin.value(1)
        sleep_ms(50)
        return

    def send_command(self, command):
        self._dc_pin.value(0)
        self._cs_pin.value(0)
        self.spi_writebyte([command])
        self._cs_pin.value(1)
        return

    def send_data(self, data):
        self._dc_pin.value(1)
        self._cs_pin.value(0)
        self.spi_writebyte([data])
        self._cs_pin.value(1)
        return

    def wait_free(self):
        while self._busy_pin.value() == 1:      #  0: idle, 1: busy
            sleep_ms(10)
        return

    def on(self, partial: bool=False):
        self.send_command(0x22) # DISPLAY_UPDATE_CONTROL_2

        if partial is not True:
            self.send_data(0xF7)
        else:
            self.send_data(0x0F)
        self.send_command(0x20) # MASTER_ACTIVATION
        self.wait_free()
        return

    def send_lut(self):
        """The method sends all data provided to the e-paper-module.

        :rtype: None
        """
        self.send_command(0x32)
        for _ in range(0, 153):
            self.send_data(self._lut[_])
        self.wait_free()
        return

    @property
    def buffer(self) -> bytearray:
        return self._buffer

    @buffer.setter
    def buffer(self, buf: bytearray):
        self._buffer = buf

    @property
    def window(self) -> (int, int, int, int):
        return self._window

    @window.setter
    def window(self, wdw: (int, int, int, int)):  # window = (x_start, y_start, x_end, y_end)
        self._window = wdw
        self.send_command(0x44) # SET_RAM_X_ADDRESS_START_END_POSITION
        # x point must be the multiple of 8 or the last 3 bits will be ignored
        self.send_data((self._window[0]>>3) & 0xFF)
        self.send_data((self._window[2]>>3) & 0xFF)
        self.send_command(0x45) # SET_RAM_Y_ADDRESS_START_END_POSITION
        self.send_data(self._window[1] & 0xFF)
        self.send_data((self._window[1] >> 8) & 0xFF)
        self.send_data(self._window[3] & 0xFF)
        self.send_data((self._window[3]>> 8) & 0xFF)
        return

    @property
    def cursor(self) -> (int, int):
        return self._cursor

    @cursor.setter
    def cursor(self, pos: (int, int)):
        self._cursor = pos
        self.send_command(0x4E) # SET_RAM_X_ADDRESS_COUNTER
        self.send_data(self._cursor[0] & 0xFF)

        self.send_command(0x4F) # SET_RAM_Y_ADDRESS_COUNTER
        self.send_data(self._cursor[1] & 0xFF)
        self.send_data((self._cursor[1] >> 8) & 0xFF)
        self.wait_free()
        return

    def prepare_display(self):
        # EPD hardware init start
        self.reset()

        self.wait_free()
        self.send_command(0x12)  #SWRESET
        self.wait_free()

        self.send_command(0x01) #Driver output control
        self.send_data(0x27)
        self.send_data(0x01)
        self.send_data(0x00)

        self.send_command(0x11) #data entry mode
        self.send_data(0x03)

        self.window = (0, 0, self._width - 1, self._height - 1)

        self.send_command(0x21) #  Display update control
        self.send_data(0x00)
        self.send_data(0x80)

        self.cursor = (0, 0)
        self.wait_free()
        # EPD hardware init end
        return

    def display_image(self, image):
        if image is None:
            return

        self.send_command(0x24) # WRITE_RAM
        for j in range(0, self._height):
            for i in range(0, int(self._width / 8)):
                self.send_data(image[i + j * int(self._width / 8)])
        self.on()
        return

    def display_base(self, image):
        if image is None:
            return
        self.send_command(0x24) # WRITE_RAM
        for j in range(0, self._height):
            for i in range(0, int(self._width / 8)):
                self.send_data(image[i + j * int(self._width / 8)])

        self.send_command(0x26) # WRITE_RAM
        for j in range(0, self._height):
            for i in range(0, int(self._width / 8)):
                self.send_data(image[i + j * int(self._width / 8)])

        self.on()
        return

    def on_partial(self, image):
        if image is None:
            return

        self._reset_pin.value(0)
        sleep_ms(2)
        self._reset_pin.value(1)
        sleep_ms(2)

        self.send_lut()
        self.send_command(0x37)
        for _ in range(0, 5):
            self.send_data(0x00)
        self.send_data(0x40)
        for _ in range(0, 4):
            self.send_data(0x00)

        self.send_command(0x3C) #BorderWavefrom
        self.send_data(0x80)

        self.send_command(0x22)
        self.send_data(0xC0)
        self.send_command(0x20)
        self.wait_free()

        self.window = (0, 0, self._width - 1, self._height - 1)
        self.cursor = (0, 0)

        self.send_command(0x24) # WRITE_RAM
        for j in range(0, self._height):
            for i in range(0, int(self._width / 8)):
                self.send_data(image[i + j * int(self._width / 8)])
        self.on(partial=True)
        return

    def clear(self, color):
        self.send_command(0x24) # WRITE_RAM
        for j in range(0, self._height):
            for i in range(0, int(self._width / 8)):
                self.send_data(color)
        self.on()
        return

    def power_down(self):
        self.send_command(0x10) # DEEP_SLEEP_MODE
        self.send_data(0x01)

        sleep_ms(2000)
        self.off()
        return

if __name__ == '__main__':
    # Portrait
    epd: EPD_2in9 = EPD_2in9(portrait=True)
    epd.clear(0xff)

    epd.fill(0xff)
    epd.text("Waveshare", 5, 10, 0x00)
    epd.text("Pico_ePaper-2.9", 5, 40, 0x00)
    epd.text("Raspberry Pico", 5, 70, 0x00)
    epd.display_image(epd.buffer)
    sleep_ms(2000)

    epd.vline(10, 90, 60, 0x00)
    epd.vline(120, 90, 60, 0x00)
    epd.hline(10, 90, 110, 0x00)
    epd.hline(10, 150, 110, 0x00)
    epd.line(10, 90, 120, 150, 0x00)
    epd.line(120, 90, 10, 150, 0x00)
    epd.display_image(epd.buffer)
    sleep_ms(2000)

    epd.rect(10, 180, 50, 80, 0x00)
    epd.fill_rect(70, 180, 50, 80, 0x00)
    epd.display_base(epd.buffer)
    sleep_ms(2000)

    for i in range(0, 10):
        epd.fill_rect(40, 270, 40, 10, 0xff)
        epd.text(str(i), 60, 270, 0x00)
        epd.on_partial(epd.buffer)

    #epd.prepare_display()
    #epd.clear(0xff)
    sleep_ms(2000)
    print("sleep")
    epd.power_down()
