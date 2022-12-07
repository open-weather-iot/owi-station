# based on: https://github.com/gvalkov/micropython-esp8266-hmc5883l
# reference: https://peppe8o.com/magnetometer-compass-with-raspberry-pi-pico-gy-271-hmc5883l-wiring-and-use-with-micropython/
# reference: https://cdn-shop.adafruit.com/datasheets/HMC5883L_3-Axis_Digital_Compass_IC.pdf

import math
from ustruct import pack
from array import array

_HMC5883L_ADDR = const(0x1e)
_HMC5883L_CONFIG_A_REG = const(0x0)
_HMC5883L_CONFIG_B_REG = const(0x1)
_HMC5883L_MODE_REG = const(0x2)
_HMC5883L_DATA_OUT_START_REG = const(0x3)
_HMC5883L_CONTINUOUS_MODE = const(0x0)
_HMC5883L_SINGLE_MODE = const(0x1)
_HMC5883L_GAIN = {
    '0.88': (0 << 5, 0.73),
    '1.3':  (1 << 5, 0.92),
    '1.9':  (2 << 5, 1.22),
    '2.5':  (3 << 5, 1.52),
    '4.0':  (4 << 5, 2.27),
    '4.7':  (5 << 5, 2.56),
    '5.6':  (6 << 5, 3.03),
    '8.1':  (7 << 5, 4.35),
}
_HMC5883L_AVERAGED_SAMPLES = {
    '1': 0b00,
    '2': 0b01,
    '4': 0b10,
    '8': 0b11,
}
_HMC5883L_SAMPLING_RATE_HZ = {
    '0.75': 0b000,
    '1.5':  0b001,
    '3':    0b010,
    '7.5':  0b011,
    '15':   0b100,
    '30':   0b101,
    '75':   0b110,
}

class HMC5883L:
    def __init__(self, i2c, *, averaged_samples='8', sampling_rate_hz='15', gauss='1.3'):
        self.i2c = i2c

        # Initialize sensor.
        i2c.start()

        # Configuration register A:
        #   0bxSSRRRMM  -> SS (averaged samples per measurement), RRR (sampling rate), MM (measurement mode)
        i2c.writeto_mem(_HMC5883L_ADDR, _HMC5883L_CONFIG_A_REG, pack('B', _HMC5883L_AVERAGED_SAMPLES[averaged_samples] << 5 | _HMC5883L_SAMPLING_RATE_HZ[sampling_rate_hz] << 2 | 0b00))

        # Configuration register B:
        reg_value, self.gain = _HMC5883L_GAIN[gauss]
        i2c.writeto_mem(_HMC5883L_ADDR, _HMC5883L_CONFIG_B_REG, pack('B', reg_value))

        # Set mode register to continuous mode
        i2c.writeto_mem(_HMC5883L_ADDR, _HMC5883L_MODE_REG, pack('B', _HMC5883L_CONTINUOUS_MODE))
        i2c.stop()

        # Reserve some memory for the raw xyz measurements
        self.data = array('B', [0] * 6)

    def calibrate(self):
        X = []
        Y = []

        while False:
            x, y, _z = self.read()
            X.append(x)
            Y.append(y)

        Xmin = min(X)
        Xmax = max(X)
        Ymin = min(Y)
        Ymax = max(Y)

        xs = 1
        ys = (Xmax - Xmin) / (Ymax - Ymin)
        xb = xs * (1/2 * (Xmax - Xmin) - Xmax)
        yb = xs * (1/2 * (Ymax - Ymin) - Ymax)

        return xs, ys, xb, yb

    def read(self):
        data = self.data
        gain = self.gain

        self.i2c.readfrom_mem_into(_HMC5883L_ADDR, _HMC5883L_DATA_OUT_START_REG, data)

        x = (data[0] << 8) | data[1]
        y = (data[4] << 8) | data[5]
        z = (data[2] << 8) | data[3]

        x = x - (1 << 16) if x & (1 << 15) else x
        y = y - (1 << 16) if y & (1 << 15) else y
        z = z - (1 << 16) if z & (1 << 15) else z

        x = round(x * gain, 4)
        y = round(y * gain, 4)
        z = round(z * gain, 4)

        return x, y, z

    def heading(self, x, y, declination=(0,0)):
        heading_rad = math.atan2(y, x)
        heading_rad += declination

        if heading_rad < 0:  # Correct reverse heading
            heading_rad += 2 * math.pi
        elif heading_rad > 2 * math.pi:  # Compensate for wrapping
            heading_rad -= 2 * math.pi

        # Convert from radians to degrees
        heading = heading_rad * 180 / math.pi
        degrees = math.floor(heading)
        minutes = round((heading - degrees) * 60)

        return degrees, minutes
