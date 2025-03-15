# Complete project details at https://RandomNerdTutorials.com

from machine import Pin, I2C
import ssd1306
from time import sleep
import os
from time import sleep_ms


class textout:
    def __init__(self):

        # Check if display is there.
        # If not, keep running but just output text in log
        try:
            # ESP32 Pin assignment
            i2c = I2C(-1, scl=Pin(22), sda=Pin(21))

            # ESP8266 Pin assignment
            #i2c = I2C(-1, scl=Pin(5), sda=Pin(24))

            # Reset OLED
            oledReset=Pin(16, Pin.OUT)
            oledReset.value(0)
            sleep_ms(500)
            oledReset.value(1)

            self.oled_width = 128
            self.oled_height = 64
            self.oled = ssd1306.SSD1306_I2C(self.oled_width, self.oled_height, i2c)
            self.oled.fill(0)
            self.oled.show()
        except:
            self.oled = None

    def clear(self):
        if self.oled:
            self.oled.fill(0)

    def show(self):
        if self.oled:
            self.oled.show()

    def centerline(self, txt, line=4):
        txt = str(txt)
        Xstart = 64-len(txt)*4
        print(txt)
        if self.oled:
            self.oled.text(txt, Xstart, line*8)

    def leftline(self, txt, line=4):
        txt = str(txt)
        Xstart = 0
        print(txt)
        if self.oled:
            self.oled.text(txt, Xstart, line*8)

    def rightline(self, txt, line=4):
        txt = str(txt)
        Xstart = Xstart = 112-len(txt)*4
        print(txt)
        if self.oled:
            self.oled.text(txt, Xstart, line*8)

    def text(self, txt):
        txt = str(txt)
        print(txt)
        if self.oled:
            self.oled.fill(0)
            Xstart = 64-len(txt)*4
            self.oled.text(txt, Xstart, 32)
            self.oled.show()
    
    # Write as a terminal. Line is (second) yellow line. Scroll and one line to bottom
    def terminalline(self,txt):
        txt = str(txt)
        Xstart = 0
        print(txt)
        if self.oled:
            self.oled.scroll(0,8)
            self.oled.text(str(txt), 0, 8)
            self.oled.show()

    def vscroll(self,lines=1):
        pixels=-4*lines
        if self.oled:
            self.oled.scroll(0,pixels)
            self.oled.show()

    # Return oled reference for other graphics
    def display(self):
        return(self.oled)
