import machine
from machine import Pin
from machine import SPI as _SPI
from machine import I2C as _I2C

# reference: https://docs.micropython.org/en/latest/library/machine.SPI.html
class SPI:
    BUS_BAUDRATE = 115200
    SELECT = 0
    DESELECT = 1
    PORTS = {
        1: { 'spi_id': 1, 'sck_pin': 10, 'mosi_pin': 11, 'miso_pin': 12, 'cs_pin': 13 },
    }

    def __init__(self, *, port):
        if port not in SPI.PORTS:
            raise Exception(f'unknown SPI port id {port}')

        self._cs = Pin(SPI.PORTS[port]['cs_pin'], mode=Pin.OUT)
        self._cs.value(SPI.DESELECT)

        self._spi = _SPI(
            SPI.PORTS[port]['spi_id'], 
            baudrate=SPI.BUS_BAUDRATE, polarity=0, phase=1, firstbit=_SPI.MSB, 
            sck=Pin(SPI.PORTS[port]['sck_pin'], Pin.OUT),
            mosi=Pin(SPI.PORTS[port]['mosi_pin'], Pin.OUT),
            miso=Pin(SPI.PORTS[port]['miso_pin'], Pin.OUT),
        )

    def __enter__(self):
        self.select()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.deselect()

    def select(self):
        self._cs.value(SPI.SELECT)

    def deselect(self):
        self._cs.value(SPI.DESELECT)

    def read(self, nbytes, *, auto_select=False):
        if auto_select: self.select()
        value = self._spi.read(nbytes)
        if auto_select: self.deselect()
        return value

    def write(self, buf, *, auto_select=False):
        if auto_select: self.select()
        self._spi.write(buf)
        if auto_select: self.deselect()

# TODO
# reference: https://docs.micropython.org/en/latest/library/machine.I2C.html
def I2C(bus):
    BUSES = {
        0: { 'i2c_id': 0, 'scl_pin': 21, 'sda_pin': 20 },
        1: { 'i2c_id': 0, 'scl_pin': 21, 'sda_pin': 20 },
    }

    if bus not in BUSES:
        raise Exception(f'unknown I2C bus id {bus}')

    return _I2C(id=BUSES[bus]['i2c_id'], scl=Pin(BUSES[bus]['scl_pin']), sda=Pin(BUSES[bus]['sda_pin']))
