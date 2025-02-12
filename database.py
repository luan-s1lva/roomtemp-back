from pymongo import MongoClient
from dotenv import dotenv_values
from fastapi import FastAPI

config = dotenv_values(".env")

app = FastAPI()

app.mongodb_client = MongoClient(config["ATLAS_URI"])
app.database = app.mongodb_client[config["DB_NAME"]]