from pymongo import MongoClient, ASCENDING
from pymongo.collection import Collection
from pymongo.database import Database
import os
import logging


# =====================================
# MongoDB Configuration
# =====================================

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "crm_db")


# =====================================
# Mongo Client (Singleton)
# =====================================

_client: MongoClient | None = None
_db: Database | None = None


def get_mongo_client() -> MongoClient:
    """
    گرفتن یا ساخت singleton MongoClient
    """
    global _client

    if _client is None:
        _client = MongoClient(MONGO_URI)
        logging.info("MongoDB client initialized")

    return _client


def get_database() -> Database:
    """
    گرفتن دیتابیس اصلی
    """
    global _db

    if _db is None:
        client = get_mongo_client()
        _db = client[MONGO_DB_NAME]
        logging.info(f"Connected to MongoDB database: {MONGO_DB_NAME}")

    return _db


# =====================================
# Collections
# =====================================

def get_partners_collection() -> Collection:
    """
    کالکشن اصلی مخاطبین / مشتریان
    """
    db = get_database()
    return db["partners"]


# =====================================
# Indexes (Call once on startup)
# =====================================

def ensure_indexes():
    """
    ساخت ایندکس‌های ضروری برای performance
    این تابع فقط یک‌بار هنگام startup صدا زده شود
    """
    collection = get_partners_collection()

    collection.create_index([("analysis.funnel_stage", ASCENDING)])
    collection.create_index([("identity.business_type", ASCENDING)])
    collection.create_index([("analysis.customer_level", ASCENDING)])
    collection.create_index([("analysis.potential_level", ASCENDING)])
    collection.create_index([("acquisition.source", ASCENDING)])
    collection.create_index([("identity.city", ASCENDING)])
    collection.create_index([("meta.created_at", ASCENDING)])

    logging.info("MongoDB indexes ensured")
