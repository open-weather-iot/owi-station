#import all requiered parts
import machine
import time
import onewire
import utime
import ubinascii
import os
import random

from micropython import const
from ulora import TTN, uLoRa

#Define os pinos do Rasp Pico

LORA_MISO = const(16)
LORA_CS = const(17) # NSS
LORA_SCK = const(18)
LORA_MOSI = const(19)
LORA_IRQ = const(20) #DIO0
LORA_RST = const(21) # RESET


#Define o Fator de espalhamento (Spreading Factor - SF) e a Largura da Banda (Bandwidth - BW )
LORA_DATARATE = "SF7BW125"  # Choose from several available

#Dados do End Device registrado no TTN
DEVADDR = bytearray([0x26, 0x0D, 0xAB, 0x9A])
NWKEY = bytearray([0xDA, 0x68, 0xDE, 0xC3, 0xF6, 0xD6, 0x46, 0xE8, 0xD6, 0xE6, 0x0F, 0xDA, 0xAB, 0xD7, 0xD4, 0xDD])
APP = bytearray([0x5F, 0x14, 0xAD, 0xA4, 0x10, 0xE5, 0xF6, 0xE5, 0x29, 0x48, 0x72, 0x79, 0x41, 0x08, 0x77, 0x10])

# Definir o plano de frequencia utilizado - Brasil utiliza o plano australiano AU915-928 
TTN_CONFIG = TTN(DEVADDR, NWKEY, APP, country="AU")
FPORT = 1


#Inicia a configuração do modulo RFM95
lora = uLoRa(
    cs=LORA_CS,
    sck=LORA_SCK,
    mosi=LORA_MOSI,
    miso=LORA_MISO,
    irq=LORA_IRQ,
    rst=LORA_RST,
    ttn_config=TTN_CONFIG,
    datarate=LORA_DATARATE,
    fport=FPORT
)



while True:
	#Cria 8 variaveis com valores aleatorios
    var1=random.uniform(0.50, 575.51)
    var2=random.uniform(0.50, 575.51)
    var3=random.uniform(0.50, 575.51)
    var4=random.uniform(0.50, 575.51)
    var5=random.uniform(0.50, 575.51)
    var6=random.uniform(0.50, 575.51)
    var7=random.uniform(0.50, 575.51)
    var8=random.uniform(0.50, 575.51)
    
    #Monta a estrutura do dado a ser enviado
    data = b''
    data += '{"val1": '
    data += str(var1)
    data += ', "val2": '
    data += str(var2)
    data += ', "val3": '
    data += str(var3)
    data += ', "val4": '
    data += str(var4)
    data += ', "val5": '
    data += str(var5)
    data += ', "val6": '
    data += str(var6)
    data += ', "val7": '
    data += str(var7)
    data += ', "val8": '
    data += str(var8)
    data += '}'
    
    print("Sending packet...", lora.frame_counter, ubinascii.hexlify(data))
    # Comando para enviar a variavel data
    lora.send_data(data, len(data), lora.frame_counter)
    print(len(data), "bytes sent!")
    # incrementa 1 unidade para o frame counter
    lora.frame_counter += 1
    # Aguarda 15s para enviar o proximo pacote de dados
    time.sleep(15)

