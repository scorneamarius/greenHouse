import RPi.GPIO as GPIO
import time
from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from gpiozero import DigitalInputDevice
import datetime
import sqlite3
import Adafruit_DHT
from picamera import PiCamera
from time import sleep
GPIO.setmode(GPIO.BOARD)
contor = 0


app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"]=True
@app.route('/', methods=['POST', 'GET'])
def index(): #print the main page
    return render_template('index.html')


@app.route('/waterplant', methods=['POST','GET'])
def waterPlant():
    h=1.0 # placeholder pt campuri de umiditate si temperatura 
    t=1.0 # atunci cand e nevoie sa udam plantisoara
    database = sqlite3.connect('smartgarden.db')
    d0_input = DigitalInputDevice(17) # citim valorile
    d1_input = DigitalInputDevice(27) # senzorilor
    if not d0_input.value and not d1_input.value: #cand ambii senzori de umiditate sunt 1, nu trebuie udat
        return "Moisture threshold reached"
    else:
    	GPIO.setup(36, GPIO.OUT)
    	GPIO.output(36, True)  # deschidem valva
    	sleep(10)  # delay-ul , atata timp va uda gradina
    	GPIO.output(36, False)  # inchidem valva
    	current_time = datetime.date.today().strftime('%d/%m/%Y')
    	try: # insereaza intr-o tabela existenta parametrii senzorilor
       	   database.execute("INSERT INTO GREENHOUSE (temperatura,umiditate,date) VALUES (?,?,?)", (h, t, current_time))
    	except: # cand nu exista tabela , cream una noua
       	   database.execute(
             '''CREATE TABLE GREENHOUSE(ID INTEGER PRIMARY KEY AUTOINCREMENT,temperatura FLOAT, umiditate FLOAT, date TEXT)''')
           database.execute("INSERT INTO GREENHOUSE (temperatura,umiditate,date) VALUES (?,?,?)", (h, t,current_time))
    database.commit() # salvam modificarile
    database.close() # inchide baza de date
    return str(d0_input.value) + str(d1_input.value) # concatenam valorile senz



@app.route('/airhumidity')
def getAirHumidity():
    humidity ,temperature = Adafruit_DHT.read_retry(11, 4) #citim valorile senzorului DHT11
    current_time=datetime.date.today().strftime('%d/%m/%Y')
    database = sqlite3.connect('smartgarden.db') 
    try: # adaugam in db valorile senz si data curenta
        database.execute("INSERT INTO GREENHOUSE (temperatura,umiditate,date) VALUES (?,?,?)", (temperature, humidity, current_time))
        print(humidity)
    except: # in cazul in care nu avem creata o tabela
        database.execute(
            '''CREATE TABLE GREENHOUSE(ID INTEGER PRIMARY KEY AUTOINCREMENT,temperatura FLOAT, umiditate FLOAT, date TEXT)''')
        database.execute("INSERT INTO GREENHOUSE (temperatura,umiditate,date) VALUES (?,?,?)", (temperature, humidity, current_time))
    database.commit()
    database.close()
    return "Humidity is "+str(humidity)
    


@app.route('/airtemperature')
def getAirTemp():
    humidity ,temperature = Adafruit_DHT.read_retry(11, 4) 
    current_time=datetime.date.today().strftime('%d/%m/%Y')
    database = sqlite3.connect('smartgarden.db')
    try:
        database.execute("INSERT INTO GREENHOUSE (temperatura,umiditate,date) VALUES (?,?,?)", (temperature, humidity, current_time))
        print(temperature)
    except:
        database.execute(
            '''CREATE TABLE GREENHOUSE(ID INTEGER PRIMARY KEY AUTOINCREMENT,temperatura FLOAT, umiditate FLOAT,date TEXT)''')
        database.execute("INSERT INTO GREENHOUSE (temperatura,umiditate,date) VALUES (?,?,?)", (temperature, humidity, current_time))
    database.commit()
    database.close()
    return "Temperature is "+str(temperature)


# afiseaza ultimele 5 inregistrari din baza de date
@app.route("/viewstatistics", methods=["GET"])
def seeHistory(): 
    string=""
    database = sqlite3.connect('smartgarden.db')
    cursor = database.execute("SELECT * from GREENHOUSE WHERE ID > (SELECT MAX(ID) FROM GREENHOUSE)-5")
    for row in cursor: #concatenam ultimele 5 inregistrari din db
        string += "Date: "+str(row[3])+" Temperature: " + str(row[1])+" Humidity: " + str(row[2])+"<br \>"
    database.close()
    return string


@app.route('/viewcamera')
def viewCameraFeed(): #captura de ecran a serei
    camera = PiCamera()
    camera.rotation = 180
    camera.start_preview()
    sleep(2)
    camera.capture('./static/image.jpg')
    camera.stop_preview()
    return render_template("camera.html")
if __name__ == "__main__":
    app.run(debug=True)