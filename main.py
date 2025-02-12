from fastapi import FastAPI
from dotenv import dotenv_values
from pymongo import MongoClient
from updateRoomInfo import router as sensor_router
from routes import router as showAll
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
import os

# config = dotenv_values(".env")
ATLAS_URI = os.getenv("ATLAS_URI")
DB_NAME = os.getenv("DB_NAME")

origins = ["*"]

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Iniciando conexão com o MongoDB...")
    app.mongodb_client = MongoClient(ATLAS_URI)
    app.database = app.mongodb_client[DB_NAME]
    print("Conectado ao MongoDB!")

    yield  # Aqui o app fica rodando

    print("Fechando conexão com o MongoDB...")
    app.mongodb_client.close()
    print("Conexão encerrada!")

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(sensor_router, prefix="/temp")
app.include_router(showAll, prefix="/temp")
