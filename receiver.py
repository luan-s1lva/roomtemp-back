import time
import json
import asyncio
import random
import paho.mqtt.client as mqtt
from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List
from models import Sensor
from database import app

router = APIRouter()

lastMessage = None

def onConnect(client, userdata, flags, reason_code, properties):
    if reason_code==0:
        print("connected succesfully")
    else:
        print("impossible to connect")

def onSubscribe(client, userdata, mid, reason_codes, properties):
    for sub_result in reason_codes:
        if sub_result == 1:
            print("QoS == 1")
            # process QoS == 1
        # Any reason code >= 128 is a failure.
        if sub_result >= 128:
            print("error")
            # error processing

def onPublish(client, userdata, mid, reason_codes, properties):
    print(f"mid: {mid}\nclient: {client}")

def onMessage(client,userdata,message):
    global lastMessage
    print(f"Mensagem: {message.payload}. \nRecebida do tópico:{message.topic}")

    try:
        lastMessage = json.loads(message.payload.decode())
    except json.JSONDecodeError:
        lastMessage = None
    
async def storeTempPeriodically(request:Request):
    global lastMessage
    while True:
        sensorData = {
            "temperaturaCelsius": createRandomNumbers(),
            "idSala": createRandomRoomId()
        }

        payload = json.dumps(sensorData)
        
        client.loop_start()
        client.publish("new/world", payload)
        time.sleep(8)
        client.loop_stop()

        await asyncio.sleep(10)
        if lastMessage != None:
            app.database["sensors"].insert_one(lastMessage)
            print("Nova temp armazenada: ", lastMessage)

@router.on_event("startup")
async def startTask():
    asyncio.create_task(storeTempPeriodically(request=None))
    
def createRandomNumbers():
    return round(random.uniform(20, 30), 1)

def createRandomRoomId():
    return random.randrange(1, 300)

client = mqtt.Client(client_id="p1",callback_api_version=mqtt.CallbackAPIVersion.VERSION2)

client.on_connect=onConnect
client.on_publish=onPublish
client.on_subscribe=onSubscribe
client.on_message=onMessage

client.connect("broker.hivemq.com")
client.subscribe("new/world")

print("Execution finished")