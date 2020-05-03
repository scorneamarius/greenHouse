#!/usr/bin/python
from gpiozero import DigitalInputDevice
import time
import sys
import Adafruit_DHT
from picamera import PiCamera
from time import sleep
camera=PiCamera()
camera.rotation=180
camera.start_preview()
camera.start_recording('video.h264')
sleep(30)
camera.stop_recording()
camera.stop_preview()
d0_input = DigitalInputDevice(17)
d1_input = DigitalInputDevice(27)
while True:
    if not d0_input.value:
        print('Info from 1st sensor:Moisture threshhold reached!')
    else:
        print('Info from 1st sensor:You need to put water!')
    if not d1_input.value:
        print('Info from 2nd sensor:Moisture threshhold reached!')
    else:
        print('Info from 2st sensor:You need to put water!')
    humidity, temperature = Adafruit_DHT.read_retry(11, 4)
    print 'Temp: {0:0.1f} C  Humidity: {1:0.1f} %'.format(temperature, humidity)    
    time.sleep(60)



