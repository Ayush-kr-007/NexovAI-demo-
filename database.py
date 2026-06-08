# database.py — clean version
from pymongo import MongoClient
from loguru import logger
import os

client = None
db = None
leads_collection = None

def init_db():
    global client, db, leads_collection
    try:
        uri = os.getenv("MONGO_URI")
        client = MongoClient(uri)
        client.admin.command("ping")
        db = client["nexovai"]
        leads_collection = db["leads"]
        logger.success("✅ MongoDB Connected")
    except Exception as e:
        logger.error(f"MongoDB Error: {e}")

def save_lead_to_db(lead):
    global leads_collection
    try:
        result = leads_collection.insert_one(lead)
        logger.success(f"Lead saved. ID: {result.inserted_id}")
    except Exception as e:
        logger.error(f"Failed to save lead: {e}")