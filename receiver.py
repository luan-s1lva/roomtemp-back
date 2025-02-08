import time
import json
import asyncio
import random
import paho.mqtt.client as mqtt
from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List
from models import Room
from database import app

router = APIRouter()

lastMessage = None
max_salas = app.database["salas"].find_one(sort=[("_id",-1)])

def onConnect(client, userdata, flags, reason_code, properties):
    if reason_code==0:
        print("connected succesfully")
    else:
        print("impossible to connect")

def onPublish(client, userdata, mid, reason_codes, properties):
    print(f"mid: {mid}\nclient: {client}")

def onMessage(client,userdata,message):
    global lastMessage
    print(f"Mensagem: {message.payload}. \nRecebida do tópico:{message.topic}")

    try:
        lastMessage = json.loads(message.payload.decode())
    except json.JSONDecodeError:
        lastMessage = None
    
client = mqtt.Client(client_id="p1",callback_api_version=mqtt.CallbackAPIVersion.VERSION2)

client.on_connect=onConnect
client.on_publish=onPublish
client.on_message=onMessage

client.connect("broker.hivemq.com")
client.subscribe("new/world")

async def storeTempPeriodically(request:Request):
    global lastMessage
    i = 0
    while i > 10:
        sensorData = {
            "_id": createRandomRoomId(),
            "temperaturaCelsius": createRandomNumbers(),
            "isLightOn": False
        }

        payload = json.dumps(sensorData)
        i+=1
        # client.loop_start()
        # client.publish("new/world", payload)
        # time.sleep(8)
        # client.loop_stop()

        # await asyncio.sleep(10)
        # if lastMessage != None:
        #     app.database["salas"].insert_one(lastMessage)
        #     print("Nova temp armazenada: ", lastMessage)

@router.on_event("startup")
async def startTask():
    asyncio.create_task(storeTempPeriodically(request=None))
    
def createRandomNumbers():
    return round(random.uniform(20, 33), 1)

def createRandomRoomId():
    return random.randrange(1, max_salas)

print("Execution finished")
