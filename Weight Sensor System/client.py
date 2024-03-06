### LIBRARIES

import socket
import datetime
import pandas as pd
import os

### SERVER CONNECTION
HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = '192.168.1.5'

ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

cwd = os.getcwd()

### INITIALIZATION
weightResults = []
run = 1

lim = 0

try:
    while True:
        weightOutput = client.recv(2048).decode(FORMAT)
        print(weightOutput)
        weightOutputs = weightOutput.splitlines()
        lim += len(weightOutputs)
        for line in weightOutputs:
            time, weightOutput = line.split('; Side ')
            startTime, endTime = time.split('; ')
            sensor, weightValue = weightOutput.split(': ')
            sensorLocation, sensorNumber = sensor.split(' - Platform ')
            weightResults.append([startTime, endTime, sensorLocation, sensorNumber, weightValue])
        df = pd.DataFrame(weightResults)
        if run == 1:
            df.columns=["startTime", "endTime", "sensorLocation", "sensorNumber", "weightValue"]
            df.to_csv(cwd+"/clientWeightResults/11-07_Prototype-Demonstration-3.csv",index=False)
            weightResults = []
            run = 0
        else:
            if lim > 1000:
                df.to_csv(cwd+"/clientWeightResults/11-07_Prototype-Demonstration-3.csv", mode='a',header=False,index=False)
                weightResults = []
                lim = 0
except KeyboardInterrupt:
    pass
finally:
    df = pd.DataFrame(weightResults)
    df.to_csv(cwd+"/clientWeightResults/11-07_Prototype-Demonstration-3.csv", mode='a',header=False,index=False)