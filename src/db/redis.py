# import aioredis
from redis import asyncio as aioredis
from src.config import setting

JTI_EXPIRY = 3600
token_blocklist = aioredis.StrictRedis(
    host=setting.REDIS_HOST, port=setting.REDIS_PORT, db=0
)


async def add_jti_to_blocklist(jti: str):
    print("Hello from the add to jti blockslist function")
    return await token_blocklist.set(name=jti, value="", ex=JTI_EXPIRY)==True


async def token_in_blocklist(jti:str):
    JTI=await token_blocklist.get(jti)
    if JTI:
        return True
    return False

# print(token_blocklist)