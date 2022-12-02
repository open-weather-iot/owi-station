import machine


class SYSStats:
    def __init__(self):
        self.internal_temp_adc = machine.ADC(4)

    def read(self):
        conversion_factor = 3.3 / 65535
        temp_reading = self.internal_temp_adc.read_u16() * conversion_factor 
        temp = 27 - (temp_reading - 0.706) / 0.001721

        return {
            #'status': status,
            'cpu/temperature': { 'raw' : { 'adc': temp_reading }, 'value': temp, 'unit': 'ºC' },
            #'power/voltage': { 'raw' : { 'adc': volt_reading }, 'value': volt, 'unit': 'V' },
        }
