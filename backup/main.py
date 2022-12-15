import machine
import sdcard
import uos

CS = machine.Pin(5, machine.Pin.OUT)
spi = machine.SPI(0,baudrate=1000000,
                  polarity=0,
                  phase=0,
                  bits=8,
                  firstbit=machine.SPI.MSB,
                  sck=machine.Pin(6),
                  mosi=machine.Pin(3),
                  miso=machine.Pin(4))

sd = sdcard.SDCard(spi,CS)

vfs = uos.VfsFat(sd)
uos.mount(vfs, "/sd")

# Crie um arquivo e escreva algo nele
with open("/sd/data.txt", "w") as file:
    print("Escrevendo no data.txt...")
    file.write("UNICAMP FEEC\r\n")
    file.write(" ESTACAO METEREOLOGICA \r\n")

# Abra o arquivo que acabamos de criar e leia a partir dele
with open("/sd/data.txt", "r") as file:
    print("Lendo o data.txt...")
    data = file.read()
    print(data)
