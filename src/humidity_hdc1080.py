from micropython import const
from time import sleep


_HDC1080_ADDR = const(0x40)
_HDC1080_TEMPERATURE_REG = const(0x00)
_HDC1080_HUMIDITY_REG = const(0x01)


class HumidityHDC1080:
    def __init__(self, i2c_bus):
        self.i2c_bus = i2c_bus

    def read(self):
        self.i2c_bus.writeto(_HDC1080_ADDR, bytearray([_HDC1080_HUMIDITY_REG]))
        sleep(0.065)
        self.i2c_bus.scan()  # this is needed to prevent error on the next line (i don't know why it happens)
        hum_data = self.i2c_bus.readfrom(_HDC1080_ADDR, 2)
        hum_value = int.from_bytes(hum_data, 'big')
        relative_humidity = hum_value * 100 / 2**16  # conversion per the spec

        return {
            #'status': status,
            #'temperature': { 'raw': , 'hum_value': , 'unit': 'ºC },
            'humidity': { 'raw': hum_value, 'value': relative_humidity, 'unit': '% RH' },
        }
