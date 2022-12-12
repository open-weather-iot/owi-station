import time
import math
import _thread

from util.has_method import has_method


class FastSampling:
    def __init__(self, sensor, *, reducer=None, sampling_rate_hz=None):
        self.sensor = sensor
        assert has_method(self.sensor, 'read'), 'sensor should have the method `read`'

        if type(sampling_rate_hz) is int:
            self.sampling_rate_hz = sampling_rate_hz
        else:
            assert type(sensor.sampling_rate_hz) is int, 'if FastSampling parameter `sampling_rate_hz` is not given, then the sensor should have the property `sampling_rate_hz` of type int'
            self.sampling_rate_hz = sensor.sampling_rate_hz

        if callable(reducer):
            self.reducer = reducer
        else:
            assert callable(sensor.reducer), 'if FastSampling parameter `reducer` is not given, then the sensor should have the method `reducer`'
            self.reducer = sensor.reducer

        self.samples = []
        self.errors = []
        self.thread = _thread.start_new_thread(lambda: self.sample(), [])

    def sample(self):
        while True:
            try:
                sensor_measurements = self.sensor.read()
                self.samples.append(sensor_measurements)
            except Exception as e:
                err_msg = f'got error `{type(e).__name__}: {e}` while fast sampling sensor'
                self.errors.append(err_msg)

            time.sleep_ms(math.ceil(1000 / self.sampling_rate_hz))

    def read(self):
        samples = self.samples
        errors = self.errors

        self.samples = []
        self.errors = []

        return [self.reducer(samples), errors]
