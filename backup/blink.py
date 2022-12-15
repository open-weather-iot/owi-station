import time
from machine import Pin
ledR=Pin(2,Pin.OUT)        
ledG=Pin(7,Pin.OUT)        
tempo = 1

while True:
  ledR.value(1)            
  time.sleep(tempo)
  ledG.value(1)            
  ledR.value(0)
  time.sleep(tempo)
  ledG.value(1)            
  ledR.value(1)
  time.sleep(tempo)
  ledG.value(0)            
  ledR.value(0)
  time.sleep(tempo)
