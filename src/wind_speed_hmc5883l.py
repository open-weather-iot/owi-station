import time
import math

from lib.hmc5883l import HMC5883L


_STICK_LENGTH_METERS = 0.096

class WindSpeedHMC5883L:
    # sampling_rate_hz = [0.75, 1.5, 3, 7.5, 15, 30, 75]
    def __init__(self, i2c_bus, *, sampling_rate_hz='75', xs=1, ys=1, xb=0, yb=0):
        self.sensor = HMC5883L(i2c_bus, averaged_samples='1', sampling_rate_hz=sampling_rate_hz, gauss='1.3')
        self.sampling_rate_hz = sampling_rate_hz

        # calibration parameters
        self.xs = xs
        self.ys = ys
        self.xb = xb
        self.yb = yb

        self.previous_degrees = 0
        self.tZ = 0

    def calibrate(self):
        # self.sampling_rate_hz
        self.sensor.calibrate()

    def read(self):
        previous_degrees = self.previous_degrees
        tZ = self.tZ
        tA = time.ticks_ms()
        x, y, _z = self.sensor.read()
        x = x * self.xs + self.xb
        y = y * self.ys + self.yb
        degrees, _minutes = self.sensor.heading(x, y)
        dTheta = degrees - previous_degrees

        if dTheta < -90:
            dTheta += 360

        dt = (tZ - tA) / 1000
        w = dTheta * dt
        cosTheta = math.cos(dTheta * math.pi / 180)
        windSpeedMS = w * abs(cosTheta) * _STICK_LENGTH_METERS

        self.previous_degrees = degrees
        self.tZ = tA

        return {
            #'status': status,
            'wind_speed': { 'raw' : { 'x': x, 'y': y, 'previous_degrees': previous_degrees, 'degrees': degrees, 'tZ': tZ, 'tA': tA, 'length': _STICK_LENGTH_METERS }, 'value': windSpeedMS, 'unit': 'm/s' },
        }
