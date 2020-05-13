#!/usr/bin/python
from gpiozero import DigitalInputDevice
import time
import mysql.connector as mariadb
import sys
import Adafruit_DHT
from picamera import PiCamera
from time import sleep
# pentru a putea utiliza baza de date trebuie sa o instalam
# C:\Users\Your Name\AppData\Local\Programs\Python\Python36-32\Scripts>python -m pip install mysql-connector
# daca nu exista o baza de date o va crea, iar daca exista e va conecta la ea
try:
    database = mariadb.connect(
        host="localhost",
        user="greenHouse",
        passwd="greenHouse",
        mydb="mydatabase"
        )
    mycursor = database.cursor()
except mariadb.Error:
    database = mysql.connector.connect(
        host="localhost",
        user="greenHouse",
        passwd="greenHouse"
        )
    mycursor = database.cursor()
    mycursor.execute("CREATE DATABASE mydatabase")
    mycursor.execute("CREATE TABLE greenHouseInformation(id INT AUTO_INCREMENT PRIMARY KEY, temperatura INT, umiditate INT)")

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
    sql = "INSERT INTO greenHouseInformation(temperatura, umiditate) VALUES (%d,%d)"   
    val = (temperature, humidity)
    mycursor.execute(sql,val)
    database.commit()
    time.sleep(60)



