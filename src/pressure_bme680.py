from lib.bme680 import BME680_I2C


class PressureBME680:
    def __init__(self, i2c_bus):
        self.sensor = None
        self.i2c_bus = i2c_bus

    def reset(self):
        self.sensor = None

    def read(self):
        if self.sensor == None:
            self.sensor = BME680_I2C(i2c=self.i2c_bus)

        return {
            #'status': ,
            'pressure':    { 'raw': None, 'value': self.sensor.pressure,    'unit': 'hPa'  },
            'temperature': { 'raw': None, 'value': self.sensor.temperature, 'unit': 'ºC'   },
            'humidity':    { 'raw': None, 'value': self.sensor.humidity,    'unit': '% RH' },
            'altitude':    { 'raw': None, 'value': self.sensor.altitude,    'unit': 'm'    },
            'gas':         { 'raw': None, 'value': self.sensor.gas / 1000,  'unit': 'kOhm' },
        }
