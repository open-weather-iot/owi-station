# PT100 Temperature Project 
# https://forum.micropython.org/viewtopic.php?t=5181
# https://forum.micropython.org/viewtopic.php?f=21&t=12779
# https://htlb-atk.github.io/schilf-iot-MAX31865/#spi-bus-interface

# SPI com Raspberry Pico
# https://www.youtube.com/watch?time_continue=232&v=s7Lud1Gqrqw&feature=emb_logo&ab_channel=LearnEmbeddedSystems

import math


class TemperaturePT100MAX31865:

    ### Register constants, see data sheet for info.
    # Read Addresses
    MAX31865_REG_READ_CONFIG  = 0x00
    MAX31865_REG_READ_RTD_MSB = 0x01
    MAX31865_REG_READ_RTD_LSB = 0x02
    MAX31865_REG_READ_HFT_MSB = 0x03
    MAX31865_REG_READ_HFT_LSB = 0x04
    MAX31865_REG_READ_LFT_MSB = 0x05
    MAX31865_REG_READ_LFT_LSB = 0x06
    MAX31865_REG_READ_FAULT   = 0x07

    # Write Addresses
    MAX31865_REG_WRITE_CONFIG  = 0x80
    MAX31865_REG_WRITE_HFT_MSB = 0x83
    MAX31865_REG_WRITE_HFT_LSB = 0x84
    MAX31865_REG_WRITE_LFT_MSB = 0x85
    MAX31865_REG_WRITE_LFT_LSB = 0x86

    # Configuration Register
    MAX31865_CONFIG_50HZ_FILTER = 0x01
    MAX31865_CONFIG_CLEAR_FAULT = 0x02
    MAX31865_CONFIG_3WIRE       = 0x10
    MAX31865_CONFIG_ONE_SHOT    = 0x20
    MAX31865_CONFIG_AUTO        = 0x40
    MAX31865_CONFIG_BIAS_ON     = 0x80

    # *Use GPIO Number as port pin number
    # Pela página 15 do datasheet do MAX31865, ele só funciona nos modos 1 e 3 de comunicação SPI
      
    def __init__(self, spi_bus, *, wires_pt100=4):
        self.spi_bus = spi_bus
        self.wires_pt100 = wires_pt100

        self.reset()

        self.RefR = 424.0                         # Rref measured with multimeter on MAX31865. *May be different a little different for other boards
        self.R0  = 100.0                          # Resistance for 0ºC

    def reset(self):
        # set configuration register
        config = self.MAX31865_CONFIG_BIAS_ON + self.MAX31865_CONFIG_AUTO + self.MAX31865_CONFIG_CLEAR_FAULT + self.MAX31865_CONFIG_50HZ_FILTER
        if self.wires_pt100 == 3:
            config = config + self.MAX31865_CONFIG_3WIRE

        buf = bytearray(2)
        buf[0] = self.MAX31865_REG_WRITE_CONFIG   # config write address
        buf[1] = config
        with self.spi_bus as spi:
            spi.write(buf) # write config

    def read(self):
        raw = self._get_raw()
        temperature, resistance = self._RawToTemp(raw)

        status = self._get_status(raw)
        if status != 'OK':
            raise Exception(status)

        return {
            #'status': status,
            'temperature': { 'raw': { 'adc': raw, 'resistance': resistance }, 'value': temperature, 'unit': 'ºC' },
        }

    def _get_status(self,raw):      
        status = 'OK'
        if(raw==0 or raw == 32767):
            status = 'invalid_read_value'
        return status 

    def _get_raw(self):
        with self.spi_bus as spi: # automatic enable and disable management
            spi.write(bytes([0x01])) # first read address
            MSB = spi.read(1)           # multi-byte transfer
            LSB = spi.read(1)

        raw = (MSB[0] << 8) + LSB[0]
        raw = raw >> 1
        return raw

    def _RawToTemp(self, raw):
        RTD = (raw * self.RefR) / (32768)
        A = 3.908e-3
        B = -5.775e-7

        temperature = (-A + math.sqrt(A*A - 4*B*(1-RTD/self.R0))) / (2*B)
        return temperature, RTD
