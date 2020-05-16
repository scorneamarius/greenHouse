import time

from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from gpiozero import DigitalInputDevice
import datetime
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

app = Flask(__name__)

while True:
    humidity, temperature = Adafruit_DHT.read_retry(11, 4)
    break
time.sleep(60)

@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')


@app.route('/waterplant', methods=['POST','GET'])
def waterPlant():
    if request.method == "POST":
        database = sqlite3.connect('smartgarden.db')
        if not d0_input.value or not d1_input.value:
            print('Info from sensor:Moisture threshhold reached!')
            current_time=""
        else:
            print('Need to water the plant') #cod pompa de apa
            current_time=datetime.date.today().strftime('%d/%m/%Y')

        print('Temp: {0:0.1f} C  Humidity: {1:0.1f} %'.format(temperature, humidity))
        try:
            database.execute("INSERT INTO GREENHOUSE (temperatura,umiditate,date) VALUES (?,?,?)", (temperature, humidity, current_time))
        except:
            database.execute(
                '''CREATE TABLE GREENHOUSE(ID INTEGER PRIMARY KEY AUTOINCREMENT,temperatura FLOAT, umiditate FLOAT)''')
            database.execute("INSERT INTO GREENHOUSE (temperatura,umiditate,date) VALUES (?,?,?)", (temperature, humidity,current_time))
        database.commit()
        cursor = database.execute("SELECT ID,temperatura, umiditate from GREENHOUSE")
        for row in cursor:
            print(row[0])
            print(row[1])
            print(row[2])
        database.close()
    return "Ok"



@app.route('/airhumidity')
def getAirHumidity():
    #cod senzor umiditate aer
    return "You have accessed air humidity"


@app.route('/airtemperature')
def getAirTemp():
    #cod senzor temperatura aer
    return "You have accessed air temperature"


@app.route('/viewcamera')
def viewCameraFeed():
    #cod camera
    return render_template("camera.html")


if __name__ == "__main__":
    app.run(debug=True)
