from machine import ADC, Pin

# ADC defines
_ADC_REF_VOLTAGE = 3.3
_ADC_BIT_RESOLUTION = 12

_CONVERSION_RESOLUTION = 65535 # read_u16 scales the raw 12 bit ADC reading to 16 bit using a Taylor expansion 
_CONVERSION_FACTOR = _ADC_REF_VOLTAGE / _CONVERSION_RESOLUTION

# Hardware defines
_VSYS_CONVERSION_FACTOR = 3 * _CONVERSION_FACTOR  #  VSYS is R-C filtered and divided by 3 
                                            # (by R5, R6 and C3 in the Pico schematic)

_ADC0_CONVERSION_FACTOR = (1 / (100e3 / (100e3+100e3))) * _CONVERSION_FACTOR
_ADC1_CONVERSION_FACTOR = 1 / (100e3 / (100e3+330e3)) * _CONVERSION_FACTOR

# Battery defines
_BATTERY_MAX_VOLTAGE = 4.2
_BATTERY_MIN_VOLTAGE = 2.8


class SYSStats:
    def __init__(self):
        self.temp = ADC(4)
        self.adc0 = ADC(Pin(26)) # battery
        self.adc1 = ADC(Pin(27)) # solar panel
        self.vsys = ADC(Pin(29))

    def read(self):
        # Reading ADCs
        temp_raw = self.temp.read_u16()
        adc0_raw = self.adc0.read_u16()
        adc1_raw = self.adc1.read_u16()
        vsys_raw = self.vsys.read_u16()

        # Converting to voltage values
        temp_voltage        = temp_raw * _CONVERSION_FACTOR
        battery_voltage     = adc0_raw * _ADC0_CONVERSION_FACTOR
        solar_panel_voltage = adc1_raw * _ADC1_CONVERSION_FACTOR
        vsys_voltage        = vsys_raw * _VSYS_CONVERSION_FACTOR

        temp = 27 - (temp_voltage - 0.706) / 0.001721

        battery_percentage = 100 * (battery_voltage - _BATTERY_MIN_VOLTAGE) / (_BATTERY_MAX_VOLTAGE - _BATTERY_MIN_VOLTAGE)

        # Treating limits
        battery_percentage = min(battery_percentage, 100) # prevent 100% overflow
        battery_percentage = max(battery_percentage, 0) # prevent 0% underflow

        return {
            'cpu/temperature':           { 'raw': temp_raw, 'value': temp,                'unit': 'ºC' },
            'power/vsys/voltage':        { 'raw': vsys_raw, 'value': vsys_voltage,        'unit': 'V'  },
            'power/battery/voltage':     { 'raw': adc0_raw, 'value': battery_voltage,     'unit': 'V'  },
            'power/battery/percentage':  { 'raw': adc0_raw, 'value': battery_percentage,  'unit': '%'  },
            'power/solar_panel/voltage': { 'raw': adc1_raw, 'value': solar_panel_voltage, 'unit': 'V'  },
        }
