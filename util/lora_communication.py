from micropython import const
from ulora import TTN, uLoRa

_LORA_IRQ = const(20) # DIO0
_LORA_RST = const(21) # RESET

class LoRaCommunication:
    def __init__(self, spi_bus, *, device_addr, network_key, app_key):
        self.lora = uLoRa(
            spi_bus=spi_bus,
            irq=_LORA_IRQ,
            rst=_LORA_RST,
            ttn_config=TTN(device_addr, network_key, app_key, country='AU'), # defines the frequency plan (brazil uses the australian standard AU915-928)
            datarate='SF7BW125', # spreading factor - SR: 7; band width - BW: 125
            fport=1,
        )

    def send(self, data):
        self.lora.send_data(data, len(data), self.lora.frame_counter)
        self.lora.frame_counter += 1
