from fastapi import APIRouter,Request,Body
from fastapi.encoders import jsonable_encoder
from typing import List
from models import Room
from models import RoomControls
from database import app
from fastapi.middleware.cors import CORSMiddleware

router = APIRouter()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@router.get("/show",response_model=List[Room])
def showTemps(request:Request):
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
    print(data)
    app.database["salas"].update_one(
        {"_id": data.idSala},
        {"$set": {"isACOn": data.isACOn, "isLightOn": data.isLightOn}}
    )