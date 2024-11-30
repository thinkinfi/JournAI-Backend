from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine
import os
from dotenv import load_dotenv
from urllib.parse import quote_plus

# Load .env
load_dotenv()

# Get MongoDB connection details from .env file
MONGODB_USERNAME = os.getenv("MONGODB_USERNAME")
MONGODB_PASSWORD = os.getenv("MONGODB_PASSWORD")
MONGODB_HOST = os.getenv("MONGODB_HOST")
MONGODB_DATABASE = os.getenv("MONGODB_DATABASE")

# Encode username and password
encoded_username = quote_plus(MONGODB_USERNAME)
encoded_password = quote_plus(MONGODB_PASSWORD)

# MongoDB connection string
MONGODB_URL = f"mongodb+srv://{encoded_username}:{encoded_password}@{MONGODB_HOST}/{MONGODB_DATABASE}?retryWrites=true&w=majority"

# Create the client and engine
client = AsyncIOMotorClient(MONGODB_URL)
database = client[MONGODB_DATABASE]
engine = AIOEngine(client=client, database=MONGODB_DATABASE)

async def init_db():
    try:
        await client.admin.command('ping')
        print("Successfully connected to MongoDB")
    except Exception as e:
        print(f"Unable to connect to MongoDB: {e}")

# Print the connection URL for debugging (remove in production)
print(f"Connecting to: {MONGODB_URL}")