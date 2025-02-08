import time
import json
import random
import paho.mqtt.client as mqtt
from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List
from models import Sensor

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
    

def createRandomNumbers():
    return round(random.uniform(20, 30), 1)

def createRandomRoomId():
    return random.randrange(1, 150)


client = mqtt.Client(client_id="p1",callback_api_version=mqtt.CallbackAPIVersion.VERSION2)

client.on_connect=onConnect
client.on_publish=onPublish
client.on_subscribe=onSubscribe
client.on_message=onMessage

sensorData = {
    "temperaturaCelsius": createRandomNumbers(),
    "idSala": createRandomRoomId()
}

payload = json.dumps(sensorData)

client.connect("broker.hivemq.com")
client.subscribe("new/world")

time.sleep(4)

client.loop_start()
client.publish("new/world", payload)
time.sleep(4)
client.loop_stop()

print("Execution finished")

@router.post("/",response_description="storing new temp",response_model=Sensor)
def storeTemp(request:Request):
    global lastMessage

    if lastMessage != None:
        request.app.database["sensors"].insert_one(lastMessage)
        