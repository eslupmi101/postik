import motor.motor_asyncio

from core import settings

client = motor.motor_asyncio.AsyncIOMotorClient(settings.MINIO_URI)

db = client[settings.NAME_DATABASE]

col = db[settings.NAME_COLLECTION]
