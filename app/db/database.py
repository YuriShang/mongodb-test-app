import motor.motor_asyncio
from app.config.config import config

client = motor.motor_asyncio.AsyncIOMotorClient(config["mongodb"]["uri"])
db = client.testdb
collection = db.sample_collection
