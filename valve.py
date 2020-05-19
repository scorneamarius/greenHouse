import RPi.GPIO as GPIO
import time
from time import sleep
GPIO.setmode(GPIO.BOARD)
GPIO.setup(36,GPIO.OUT)
GPIO.output(36,True) #deschidem valva
sleep(15) # delay-ul , atata timp va uda gradina
GPIO.output(36,False) #inchidem valva
# Se foloseste pinul 36 de pe placa
