import time
import json
from machine import Pin
import micropython

from util.bus import SPI, I2C

from util.lora_communication import LoRaCommunication
import lora_params

from src.sys_stats import SYSStats
from src.humidity_hdc1080 import HumidityHDC1080
from src.pressure_bme680 import PressureBME680
from src.temperature_pt100_max31865 import TemperaturePT100MAX31865
from src.wind_direction_hmc5883l import WindDirectionHMC5883L
from src.wind_speed_hmc5883l import WindSpeedHMC5883L


def has_method(o, name):
    return callable(getattr(o, name, None))

def main():
    # ---------------------------------------
    # ------------- SETUP    ----------------
    # ---------------------------------------
    reset_pin     = Pin(0, Pin.IN, Pin.PULL_DOWN)
    calibrate_pin = Pin(0, Pin.IN, Pin.PULL_DOWN)
    led_internal  = Pin('LED', Pin.OUT)

    led_internal.value(1)

    read_interval_ms = 1000

    lora = LoRaCommunication(SPI(port='INTERNAL_RFM95W'), device_addr=lora_params.device_addr, network_key=lora_params.network_key, app_key=lora_params.app_key)

    sensors = {
        'SYS': SYSStats(),
        'HDC1080': HumidityHDC1080(I2C(bus=0)),
        'BME680': PressureBME680(I2C(bus=0)),
        'PT100': TemperaturePT100MAX31865(SPI(port='INTERNAL_MAX31865')),
        'HMC5883L/0': WindDirectionHMC5883L(I2C(bus=0)),
        'HMC5883L/1': WindSpeedHMC5883L(I2C(bus=0)),
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

    # ---------------------------------------
    # -------------   LOOP   ----------------
    # ---------------------------------------
    while True:
        readings = {}

        for (name, sensor) in sensors.items():
            try:
                sensor_reading = sensor.read()
            except:
                continue

            for (metric, value) in sensor_reading.items():
                readings[f'{name}/{metric}'] = value

        #lora.send(bytes(json.dumps(readings), encoding='utf8'))
        #lora.send(json.dumps(readings))
        print(readings)

        led_internal.toggle() # internal led toggle
        time.sleep_ms(read_interval_ms)

if __name__ == "__main__":
    main()
