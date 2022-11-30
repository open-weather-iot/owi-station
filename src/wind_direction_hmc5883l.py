from lib.hmc5883l import HMC5883L


class WindDirectionHMC5883L:
    # Once you have your heading, you must then add your 'Declination Angle', which is the 'Error' of the magnetic field in your location.
    # Find yours here: http://www.magnetic-declination.com/
    # Campinas declination (-21,38)
    # averaged_samples = [1, 2, 4, 8]
    # sampling_rate_hz = [0.75, 1.5, 3, 7.5, 15, 30, 75]
    def __init__(self, i2c_bus, *, averaged_samples='8', sampling_rate_hz='15', declination=(0,0)):
        self.sensor = HMC5883L(i2c_bus, averaged_samples=averaged_samples, sampling_rate_hz=sampling_rate_hz, gauss='1.3')
        self.declination = (declination[0] + declination[1] / 60) * math.pi / 180
        self.sampling_rate_hz = sampling_rate_hz

    def calibrate(self):
        # self.sampling_rate_hz
        xs, ys, xb, yb = self.sensor.calibrate()
        self.xs = xs
        self.ys = ys
        self.xb = xb
        self.yb = yb

    def read(self):
        x, y, _z = sensor.read()
        x = x * self.xs + self.xb
        y = y * self.ys + self.yb
        corrected_degrees, _minutes = sensor.heading(x, y, declination=self.declination)
        degrees, _minutes = sensor.heading(x, y)

        return {
            #'status': status,
            'wind_direction': { 'raw' : { 'x': x, 'y': y, 'degrees': degrees, 'declination': self.declination }, 'value': corrected_degrees, 'unit': 'º' },
        }
