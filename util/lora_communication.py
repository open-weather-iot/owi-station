import utime as time
from micropython import const
import ujson as json
import urandom as random
from lib.ulora import TTN, uLoRa

_LORA_IRQ = const(20) # DIO0
_LORA_RST = const(21) # RESET

_PACKET_TYPE_SIZE = 1
_PACKET_ID_SIZE = 10
_SEQUENCE_SIZE = 3
_MAX_PAYLOAD_SIZE = 242 - _PACKET_TYPE_SIZE
_MAX_FRAGMENT_PAYLOAD_SIZE = 242 - _PACKET_TYPE_SIZE - _PACKET_ID_SIZE - _SEQUENCE_SIZE
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
            datarate='SF7BW125', # spreading factor - SR; band width - BW
            fport=1,
        )

    def _send(self, data):
        length = len(data)
        self.lora.frame_counter += 1
        self.lora.send_data(data, length, self.lora.frame_counter)
        return length

    def send(self, data):
        data = json.dumps(data, separators=(',', ':')).encode('utf8')
        length = len(data)
        if length <= _MAX_PAYLOAD_SIZE:
            return self._send(_PKT_TYPE_NOT_FRAG + data)

        pkt_id = random.getrandbits(32)
        sequence = 0

        while len(data[sequence*_MAX_FRAGMENT_PAYLOAD_SIZE:]) > 0:
            idata = data[sequence*_MAX_FRAGMENT_PAYLOAD_SIZE:sequence*_MAX_FRAGMENT_PAYLOAD_SIZE+_MAX_FRAGMENT_PAYLOAD_SIZE]

            # check if there's a next fragment to use type _PKT_TYPE_FRAG_PARTIAL, else _PKT_TYPE_FRAG_FINAL
            if len(data[(sequence+1)*_MAX_FRAGMENT_PAYLOAD_SIZE:]) > 0:
                pkt_type = _PKT_TYPE_FRAG_PARTIAL
            else:
                pkt_type = _PKT_TYPE_FRAG_FINAL

            self._send(pkt_type + f'{pkt_id:010d}'.encode('utf8') + f'{sequence+1:03d}'.encode('utf8') + idata)
            time.sleep_ms(200)

            sequence += 1

        return length
