import time
from machine import Pin
import micropython

from util.bus import SPI, I2C
#from util.fast_sampling import FastSampling
from util.has_method import has_method

from util.lora_communication import LoRaCommunication
import lora_params

from src.sys_stats import SYSStats
from src.humidity_hdc1080 import HumidityHDC1080
from src.pressure_bme680 import PressureBME680
from src.temperature_pt100_max31865 import TemperaturePT100MAX31865
from src.wind_direction_hmc5883l import WindDirectionHMC5883L
from src.wind_speed_hmc5883l import WindSpeedHMC5883L


def main():
    # ------------------------------------
    # ------------    SETUP   ------------
    # ------------------------------------
    #reset_pin     = Pin(0, Pin.IN, Pin.PULL_DOWN)
    #calibrate_pin = Pin(0, Pin.IN, Pin.PULL_DOWN)
    led_internal  = Pin('LED', Pin.OUT, value=1)

    read_interval_ms = 1_000

    lora = LoRaCommunication(SPI(port='INTERNAL_RFM95W'), device_addr=lora_params.device_addr, network_key=lora_params.network_key, app_key=lora_params.app_key)

    sensors = {
        'SYS': SYSStats(),
        #'HDC1080': HumidityHDC1080(I2C(bus=0)),
        #'BME680': PressureBME680(I2C(bus=0)),
        #'PT100': TemperaturePT100MAX31865(SPI(port='INTERNAL_MAX31865')),
        #'HMC5883L/0': FastSampling(WindDirectionHMC5883L(I2C(bus=0))),
        #'HMC5883L/1': FastSampling(WindSpeedHMC5883L(I2C(bus=0))),
    }

    def reset(_):
        for sensor in sensors.values():
            if has_method(sensor, 'reset'):
                sensor.reset()

    def calibrate(_):
        for sensor in sensors.values():
            if has_method(sensor, 'calibrate'):
                sensor.calibrate()

    #reset_pin.irq(handler=lambda _: micropython.schedule(reset, None), trigger=Pin.IRQ_HIGH_LEVEL)
    #calibrate_pin.irq(handler=lambda _: micropython.schedule(calibrate, None), trigger=Pin.IRQ_HIGH_LEVEL)

    # inicialização de cada sensor (se o método setup existe)
    for sensor in sensors.values():
        if has_method(sensor, 'setup'):
            sensor.setup()

    # ------------------------------------
    # ------------    LOOP    ------------
    # ------------------------------------
    while True:
        measurements = {}
        errors = []

        for (name, sensor) in sensors.items():
            try:
                result = sensor.read()
                if isinstance(sensor, FastSampling):
                    sensor_measurements, sensor_errors = result
                    for i in sensor_errors:
                        errors.append(err_msg)
                else:
                    sensor_measurements = result
            except Exception as e:
                err_msg = f'got error `{type(e).__name__}: {e}` while sampling sensor `{name}`'
                errors.append(err_msg)
                continue

            for (metric, value) in sensor_measurements.items():
                measurements[f'{name}/{metric}'] = value

        pkt = { 'measurements': measurements, 'errors': errors }
        print(pkt)
        lora.send(pkt)

        led_internal.toggle()
        time.sleep_ms(read_interval_ms)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f'got error `{type(e).__name__}: {e}` on main')
