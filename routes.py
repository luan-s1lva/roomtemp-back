from fastapi import APIRouter,Request
from typing import List
from models import Sensor
from database import app

router = APIRouter()

@router.get("/show",response_model=List[Sensor])
def showTemps(request:Request):
    temps = list(app.database["sensors"].find(limit=100))
    return temps