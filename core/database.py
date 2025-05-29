# Copyright @ISmartDevs
# Channel t.me/TheSmartDev

from pymongo import MongoClient
from config import DATABASE_URL
from utils import LOGGER

# Log the initialization attempt
LOGGER.info("Creating Database Client From DATABASE_URL")

try:
    # Create MongoDB client using DATABASE_URL from config.py
    mongo_client = MongoClient(DATABASE_URL)
    # Access the "ItsSmartTool" database
    db = mongo_client["ItsSmartTool"]
    # Access the "auth_admins" collection for authorized admins
    auth_admins = db["auth_admins"]
    # Access the "banned_users" collection for banned users
    banned_users = db["banned_users"]
    LOGGER.info("Database Client Successfully Created!")
except Exception as e:
    # Log the error with details and raise it to halt execution
    LOGGER.error(f"Database Client Create Error: {e}")
    raise