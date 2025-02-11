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

async def storeTempPeriodically():
    global lastMessage
    while True:
        sensorData = {
            "_id": selectRandomRoomId(),
            "temperaturaCelsius": createRandomNumbers()
        }

        payload = json.dumps(sensorData)

        await asyncio.sleep(5)
        client.publish("new/world", payload)

        app.database["salas"].update_one(
            {"_id": int(selectRandomRoomId())},
            {"$set": {"temperaturaCelsius": createRandomNumbers()}}
        )
        print("Nova informação armazenada")

@router.on_event("startup")
async def startTask():
    asyncio.create_task(storeTempPeriodically())
    
def createRandomNumbers():
    return round(random.uniform(20, 33), 1)

def selectRandomRoomId():
    roomNumbers = list(app.database["salas"].distinct("_id"))
    randomIndexRoom = random.uniform(0,int(len(roomNumbers)))
    selectedRoom = roomNumbers[int(randomIndexRoom)]
    return str(selectedRoom)