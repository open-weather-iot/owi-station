import machine


class CPUTemperature:
    def __init__(self):
        self.internal_temp_adc = machine.ADC(4)

    def read(self):
        conversion_factor = 3.3 / 65535
        reading = self.internal_temp_adc.read_u16() * conversion_factor 
        temperature = 27 - (reading - 0.706) / 0.001721

        return {
            #'status': status,
            'temperature': { 'raw' : { 'adc': reading }, 'value': temperature, 'unit': 'ºC' },
        }
