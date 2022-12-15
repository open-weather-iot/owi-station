import time
import math
import _thread

from util.has_method import has_method


class FastSampling:
    thread = None
    thread_running = False

    def __init__(self, sensor, *, reducer=None, sampling_rate_hz=None):
        self.sensor = sensor
        assert has_method(self.sensor, 'read'), 'sensor should have the method `read`'

        if type(sampling_rate_hz) is str:
            self.sampling_rate_hz = float(sampling_rate_hz)
        else:
            assert type(sensor.sampling_rate_hz) is str, 'if FastSampling parameter `sampling_rate_hz` is not given, then the sensor should have the property `sampling_rate_hz` of type str'
            self.sampling_rate_hz = float(sensor.sampling_rate_hz)

        if callable(reducer):
            self.reducer = reducer
        else:
            assert callable(sensor.reducer), 'if FastSampling parameter `reducer` is not given, then the sensor should have the method `reducer`'
            self.reducer = sensor.reducer

        self.samples = []
        self.errors = []
        FastSampling.thread_running = True
        FastSampling.thread = _thread.start_new_thread(self._sample, [])

    @staticmethod
    def stop_thread():
        FastSampling.thread_running = False

    def reset(self):
        if has_method(self.sensor, 'reset'):
            self.sensor.reset()

    def _sample(self):
        while FastSampling.thread_running:
            try:
                sensor_measurements = self.sensor.read()
                self.samples.append(sensor_measurements)
            except Exception as e:
                err_msg = f'got error `{type(e).__name__}: {e}` while fast sampling sensor'
                if err_msg not in self.errors:
                    self.errors.append(err_msg)

            time.sleep_ms(math.ceil(1000 / self.sampling_rate_hz))

    def read(self):
        samples = self.samples
        errors = self.errors

        self.samples = []
        self.errors = []

        return [self.reducer(samples), errors]
