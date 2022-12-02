import machine
from machine import Pin
from machine import SPI as _SPI
from machine import I2C as _I2C

# reference: https://docs.micropython.org/en/latest/library/machine.SPI.html
class SPI:
    SELECT = 0
    DESELECT = 1
    PORTS = {
        'INTERNAL_RFM95W':   { 'spi_id': 0, 'polarity': 0, 'phase': 0, 'sck_pin': 18, 'mosi_pin': 19, 'miso_pin': 16, 'cs_pin': 17, 'baudrate': 4000000 },
        'INTERNAL_MAX31865': { 'spi_id': 1, 'polarity': 0, 'phase': 1, 'sck_pin': 10, 'mosi_pin': 11, 'miso_pin': 12, 'cs_pin': 13, 'baudrate': 115200  },
    }

    def __init__(self, *, port):
        if port not in SPI.PORTS:
            raise Exception(f'unknown SPI port id {port}')

        self._cs = Pin(SPI.PORTS[port]['cs_pin'], mode=Pin.OUT, value=SPI.DESELECT)

        self._spi = _SPI(
            SPI.PORTS[port]['spi_id'],
            baudrate=SPI.PORTS[port]['baudrate'], polarity=SPI.PORTS[port]['polarity'], phase=SPI.PORTS[port]['phase'], firstbit=_SPI.MSB,
            sck=Pin(SPI.PORTS[port]['sck_pin'], Pin.OUT),
            mosi=Pin(SPI.PORTS[port]['mosi_pin'], Pin.OUT),
            miso=Pin(SPI.PORTS[port]['miso_pin'], Pin.OUT),
        )

    def __enter__(self):
        self.select()
        return self._spi

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.deselect()

    def select(self):
        self._cs.value(SPI.SELECT)

    def deselect(self):
        self._cs.value(SPI.DESELECT)

# TODO
# reference: https://docs.micropython.org/en/latest/library/machine.I2C.html
def I2C(bus):
    BUSES = {
        0: { 'i2c_id': 0, 'sda_pin':  8, 'scl_pin':  9 },
        1: { 'i2c_id': 1, 'sda_pin': 14, 'scl_pin': 15 },
    }

    if bus not in BUSES:
        raise Exception(f'unknown I2C bus id {bus}')

    return _I2C(id=BUSES[bus]['i2c_id'], sda=Pin(BUSES[bus]['sda_pin']), scl=Pin(BUSES[bus]['scl_pin']), freq=400000)
