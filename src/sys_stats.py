from machine import ADC, Pin


class SYSStats:
    def __init__(self):
        self.internal_temp_adc = ADC(4)
        self.internal_voltage_adc = ADC(Pin(29))

    def read(self):
        conversion_factor = 3.3 / 65535

        temp_reading = self.internal_temp_adc.read_u16()
        temp = 27 - (temp_reading * conversion_factor - 0.706) / 0.001721

        vsys_reading = self.internal_temp_adc.read_u16()
        vsys = vsys_reading * conversion_factor

        return {
            #'status': status,
            'cpu/temperature': { 'raw' : { 'adc': temp_reading }, 'value': temp, 'unit': 'ºC' },
            'power/vsys': { 'raw' : { 'adc': vsys_reading }, 'value': vsys, 'unit': 'V' },
        }
