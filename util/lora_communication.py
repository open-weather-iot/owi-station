from micropython import const
import ujson as json
import urandom as random
from lib.ulora import TTN, uLoRa

_LORA_IRQ = const(20) # DIO0
_LORA_RST = const(21) # RESET

_MAX_PAYLOAD_SIZE = 241 # 242 bytes payload size limit - 1 byte header
_PKT_TYPE_NOT_FRAG = b'0'
_PKT_TYPE_FRAG_PARTIAL = b'1'
_PKT_TYPE_FRAG_FINAL = b'2'

class LoRaCommunication:
    def __init__(self, spi_bus, *, device_addr, network_key, app_key):
        random.seed(None)
        self.lora = uLoRa(
            spi_bus=spi_bus,
            irq=_LORA_IRQ,
            rst=_LORA_RST,
            ttn_config=TTN(device_addr, network_key, app_key, country='AU'), # defines the frequency plan (brazil uses the australian standard AU915-928)
            datarate='SF7BW125', # spreading factor - SR: 7; band width - BW: 125
            fport=1,
        )

    def _send(self, data):
        self.lora.send_data(data, len(data), self.lora.frame_counter)
        self.lora.frame_counter += 1

    def send(self, data):
        data = json.dumps(data, separators=(',', ':')).encode('utf8')
        if len(data) <= _MAX_PAYLOAD_SIZE:
            return self._send(_PKT_TYPE_NOT_FRAG + data)

        print('packet too big. fragmentation not implemented')
        return
        # TYPE (1) + PACKET ID (10) + SEQUENCE NUMBER (3)
        #pkt_id = random.getrandbits(32)
        #sequence = 0

        #while True:
        #    idata = data[:]
        #    self._send(_PKT_TYPE_FRAG_PARTIAL + idata)
        #    self._send(_PKT_TYPE_FRAG_FINAL + idata)
