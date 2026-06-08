from pymongo import MongoClient
from loguru import logger
import os

client = None
db = None
leads_collection = None


def init_db():
    global client, db, leads_collection

    try:
        client = MongoClient(os.getenv("MONGO_URI"))

        # Force connection test
        client.admin.command("ping")

        db = client["nexovai"]
        leads_collection = db["leads"]

        logger.success("✅ MongoDB Connected")

    except Exception as e:
        logger.error(f"❌ MongoDB Connection Failed: {e}")


def save_lead_to_db(lead):
    def save_lead_to_db(lead):
        global leads_collection

        try:
            result = leads_collection.insert_one(lead)

            logger.success(
                f"Lead saved successfully. ID={result.inserted_id}"
            )

        except Exception as e:
            logger.error(f"Failed to save lead: {e}")
    try:
        result = leads_collection.insert_one(lead)

        logger.success(
            f"Lead saved to MongoDB. ID: {result.inserted_id}"
        )

    except Exception as e:
        logger.error(f"Failed to save lead: {e}")

def init_db():
    global client, db, leads_collection

    try:
        uri = os.getenv("MONGO_URI")

        print("Mongo URI:", uri)

        client = MongoClient(uri)

        client.admin.command("ping")

        db = client["nexovai"]
        leads_collection = db["leads"]

        logger.success("✅ MongoDB Connected")

    except Exception as e:
        logger.error(f"MongoDB Error: {e}")