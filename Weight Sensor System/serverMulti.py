### Libraries

## For Socket Connections
import socket
import threading
import time
import datetime

## For RPi and HX711
import RPi.GPIO as GPIO
from hx711 import HX711

## For Multiprocessing
import concurrent.futures
import itertools

# ##For Testing
# import random

HEADER = 64
FORMAT = "utf-8"
PORT = 5050 ## 8080 https; 4040 http; double check this in the future
            ## above 5000 is usually open
SERVER = '192.168.1.5' #wlan0

ADDR = (SERVER, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

DISCONNECT_MESSAGE = "!DISCONNECET"

def handle_client(conn, addr):
    print(f"NEW CONNECTION] {addr} connected.")
    connected = True
    while connected:
        currentTime = time.time()
        currentTime = int(currentTime*1e6)
        exactSecond = 1000000 - (currentTime % 1000000)
        time.sleep(exactSecond/1e6)
        startTime = datetime.datetime.now()
        weightSensor(conn, startTime)
    conn.close()

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

def specificWeightSensorInitialization(dout_pin, sensor_offset, sensor_ratio):
    specificHX711 = HX711(dout_pin, pd_sck_pin=26)
    specificHX711.set_offset(sensor_offset)
    specificHX711.set_scale_ratio(sensor_ratio)
    return specificHX711

def getWeight(hx, conn, sensor, startTime):
    weight = hx.get_weight_mean(15)
    endTime = datetime.datetime.now()
    if sensor < 7:
        side = "A"
    else:
        side = "B"
    conn.send(f"{startTime}; {endTime}; Side {side} - Platform {sensor}: {weight} \n".encode(FORMAT))
    return weight

### WEIGHT INITIALIZATION
GPIO.setmode(GPIO.BCM)

### hx = specificWeightSensorInitialization(DOUT, OFFSET, RATIO)
## S1-T
hx01 = specificWeightSensorInitialization(5, 151839, 419.5875)
hx02 = specificWeightSensorInitialization(6, 147192, 413.06060606060606)
hx03 = specificWeightSensorInitialization(13, 85675, 364.62857142857143)
## S1-B
hx04 = specificWeightSensorInitialization(16, 231951, 390.5)
hx05 = specificWeightSensorInitialization(20, 264089, 385.75)
hx06 = specificWeightSensorInitialization(21, 7553, 295.8333333333333)
## S2-T
hx07 = specificWeightSensorInitialization(17, 193709, 358.1125)
hx08 = specificWeightSensorInitialization(27, 113268, 373.21)
hx09 = specificWeightSensorInitialization(22, 202771, 400.1727272727273)
## S2-B
hx10 = specificWeightSensorInitialization(23, 237204, 383.3205882352941)
hx11 = specificWeightSensorInitialization(24, 170808, 369.9725)
hx12 = specificWeightSensorInitialization(25, 229262, 400.60625)

def weightSensor(conn, startTime):
    with concurrent.futures.ThreadPoolExecutor() as fetchWeight:
        hx = [hx01,hx02,hx03,hx04,hx05,hx06,hx07,hx08,hx09,hx10,hx11,hx12]
        sensor = [1,2,3,4,5,6,7,8,9,10,11,12]
        weigh = fetchWeight.map(getWeight, hx, itertools.repeat(conn, 12), sensor, itertools.repeat(startTime, 12))

###############    MAIN    ###############
print("[STARTING] server is starting...")

start()