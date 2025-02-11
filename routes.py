from fastapi import APIRouter,Request,Body
from fastapi.encoders import jsonable_encoder
from typing import List
from models import Room
from models import RoomControls
from database import app
from fastapi.middleware.cors import CORSMiddleware
import paho.mqtt.client as mqtt
import json
import time

router = APIRouter()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

client = mqtt.Client(client_id="p2",callback_api_version=mqtt.CallbackAPIVersion.VERSION2)

client.on_connect=onConnect
client.on_publish=onPublish
client.on_message=onMessage

client.connect("broker.hivemq.com")
client.subscribe("sensors/return/action")

@router.get("/show",response_model=List[Room])
def showTemps(request:Request):
    print("Olá")
    temps = list(app.database["salas"].find(limit=100))
    return temps

@router.post("/add/room",response_model=Room)
def addRoom(request:Request, room:Room = Body(...)):
    room = jsonable_encoder(room)
    app.database["salas"].insert_one(room)

@router.delete("/remove/room/")
def removeRoom(request:Request, _id:int):
    app.database["salas"].delete_one({"_id":_id})

@router.put("/update/room/")
def updateRoom(data:RoomControls):
    app.database["salas"].update_one(
        {"_id": data.idSala},
        {"$set": {"isACOn": data.isACOn, "isLightOn": data.isLightOn}}
    )

    roomData = {
        "idSala": data.idSala,
        "Lights": "Ligada" if data.isLightOn == True else "Desligada",
        "AC": "Ligada" if data.isACOn == True else "Desligada"
    }

    payload = json.dumps(roomData)
    client.loop_start()
    time.sleep(5)
    client.publish("sensors/return/action", payload)
    client.loop_stop()