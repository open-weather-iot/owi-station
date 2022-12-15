from machine import Pin, I2C
from bme680 import *
from time import ticks_ms, sleep_ms
from ssd1306 import SSD1306_SPI
  

i2c = I2C(1, scl=Pin(15), sda=Pin(14))

bme = BME680_I2C(i2c=i2c)

sleep_ms(1000)

while(True):
    
    temp = str(round(bme.temperature, 2)) + ' C'
    hum = str(round(bme.humidity, 2)) + ' %'
    pres = str(round(bme.pressure, 2)) + ' hPa'
    ar = str(round(bme.gas/1000, 2)) + ' KOhms'
    alt = str(round(bme.altitude, 2)) + ' m'
    
    print(temp)
    print(hum)
    print(pres)
    print(ar)
    print(alt)
    
    sleep_ms(3000)

