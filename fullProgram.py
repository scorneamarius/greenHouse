#!/usr/bin/python
from gpiozero import DigitalInputDevice
import time
import sqlite3
import sys
import Adafruit_DHT
from picamera import PiCamera
from time import sleep
camera=PiCamera()
camera.rotation=180
camera.start_preview()
camera.start_recording('video.h264')
#sleep(30)
camera.stop_recording()
camera.stop_preview()
d0_input = DigitalInputDevice(17)
d1_input = DigitalInputDevice(27)
contor = 0
while True:
    database = sqlite3.connect('newgreen.db')
    if not d0_input.value:
        print('Info from 1st sensor:Moisture threshhold reached!')
    else:
        print('Info from 1st sensor:You need to put water!')
    if not d1_input.value:
        print('Info from 2nd sensor:Moisture threshhold reached!')
    else:
        print('Info from 2st sensor:You need to put water!')
    humidity, temperature = Adafruit_DHT.read_retry(11, 4)
    print ('Temp: {0:0.1f} C  Humidity: {1:0.1f} %'.format(temperature, humidity) )
    try:
        database.execute("INSERT INTO GREENHOUSE (temperatura,umiditate) VALUES (?,?)",(temperature,humidity))
    except:
        database.execute('''CREATE TABLE GREENHOUSE(ID INTEGER PRIMARY KEY AUTOINCREMENT,temperatura FLOAT, umiditate FLOAT)''')
        database.execute("INSERT INTO GREENHOUSE (temperatura,umiditate) VALUES (?,?)",(temperature,humidity))
    database.commit() 
    cursor = database.execute("SELECT ID,temperatura, umiditate from GREENHOUSE")
    for row in cursor:
        print(row[0])
        print(row[1])
        print(row[2])
    database.close()
    break
    time.sleep(60)