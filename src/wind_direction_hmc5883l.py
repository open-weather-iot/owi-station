import math

from lib.hmc5883l import HMC5883L


class WindDirectionHMC5883L:
    # Once you have your heading, you must then add your 'Declination Angle', which is the 'Error' of the magnetic field in your location.
    # Find yours here: http://www.magnetic-declination.com/
    # Campinas declination (-21,38)
    # averaged_samples = [1, 2, 4, 8]
    # sampling_rate_hz = [0.75, 1.5, 3, 7.5, 15, 30, 75]
    def __init__(self, i2c_bus, *, averaged_samples='8', sampling_rate_hz='15', declination=(0,0), xs=1, ys=1, xb=0, yb=0):
        self.sensor = None
        self.declination = (declination[0] + declination[1] / 60) * math.pi / 180
        self.i2c_bus = i2c_bus
        self.averaged_samples = averaged_samples
        self.sampling_rate_hz = sampling_rate_hz

        # calibration parameters
        self.xs = xs
        self.ys = ys
        self.xb = xb
        self.yb = yb

    def reset(self):
        self.sensor = None

    def calibrate(self):
        # self.sampling_rate_hz
        self.sensor.calibrate()

    @staticmethod
    def reducer(samples):
        return samples[0]

    def read(self):
        if self.sensor == None:
            self.sensor = HMC5883L(self.i2c_bus, averaged_samples=self.averaged_samples, sampling_rate_hz=self.sampling_rate_hz, gauss='1.3')

        x, y, _z = self.sensor.read()
        x = x * self.xs + self.xb
        y = y * self.ys + self.yb
        corrected_degrees, _minutes = self.sensor.heading(x, y, declination=self.declination)
        degrees, _minutes = self.sensor.heading(x, y)

        return {
            #'status': status,
            'wind_direction': { 'raw': { 'x': x, 'y': y, 'degrees': degrees, 'declination': self.declination }, 'value': corrected_degrees, 'unit': 'º' },
        }
