from pymongo import MongoClient
from dotenv import dotenv_values
from fastapi import FastAPI
import os

# config = dotenv_values(".env")
ATLAS_URI = os.getenv("ATLAS_URI")
DB_NAME = os.getenv("DB_NAME")


app = FastAPI()

app.mongodb_client = MongoClient("ATLAS_URI")
app.database = app.mongodb_client["DB_NAME"]
