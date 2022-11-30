from lib.bme680 import BME680_I2C


class PressureBME680:
    def __init__(self, i2c_bus):
        self.bme = BME680_I2C(i2c=i2c_bus)

    def read(self):
        return {
            #'status': ,
            'pressure':    { 'raw' : None, 'value': self.bme.pressure,    'unit': 'hPa'  },
            'temperature': { 'raw' : None, 'value': self.bme.temperature, 'unit': 'ºC'   },
            'humidity':    { 'raw' : None, 'value': self.bme.humidity,    'unit': '% RH' },
            'altitude':    { 'raw' : None, 'value': self.bme.altitude,    'unit': 'm'    },
            'gas':         { 'raw' : None, 'value': self.bme.gas / 1000,  'unit': 'kOhm' },
        }
