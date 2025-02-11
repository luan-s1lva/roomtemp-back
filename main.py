from fastapi import FastAPI
from dotenv import dotenv_values
from pymongo import MongoClient
from updateRoomInfo import router as sensor_router
from routes import router as showAll
from fastapi.middleware.cors import CORSMiddleware
import os

# config = dotenv_values(".env")
ATLAS_URI = os.getenv("ATLAS_URI")
DB_NAME = os.getenv("DB_NAME")


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient("ATLAS_URI")
    app.database = app.mongodb_client["DB_NAME"]
    print("Connected to the MongoDB database!")

@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()


app.include_router(sensor_router, prefix="/temp")
app.include_router(showAll, prefix="/temp")
