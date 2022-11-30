from micropython import const
from time import sleep


_HDC1080_ADDR = const(0x40)
_HDC1080_HUMIDITY_REG = const(0x01)


class HumidityHDC1080:
    def __init__(self, i2c_bus):
        self.i2c_bus = i2c_bus

    def read(self):
        self.i2c_bus.writeto(_HDC1080_ADDR, bytearray([_HDC1080_HUMIDITY_REG]))
        sleep(0.065)
        data = self.i2c_bus.readfrom(_HDC1080_ADDR, 2)
        value = int.from_bytes(data, 'big')
        relative_humidity = value * 100 / 2**16  # conversion per the spec

        return {
            #'status': status,
            'humidity': { 'raw': value, 'value': relative_humidity, 'unit': '% RH' },
        }
