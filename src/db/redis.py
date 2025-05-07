import aioredis
from src.config import Config



JTI_EXPIRY= 3600 #seconds

token_blocklist = aioredis.StrictRedis(
    host = Config.REDIS_HOST,
    port = Config.REDIS_PORT,
    db = 0
)


async def add_jti_to_blacklist(jti:str) -> None:
    await token_blocklist.set(
        name = jti,
        value= '',
        ex = JTI_EXPIRY
    )

async def token_in_blocklist(jti:  str) -> bool:
    jti = await token_blocklist.get(jti)
    return jti is not None

#Admin 
[
    "adding users",
    'change roles',
    'crud on users',
    'book submission',
    'crud on users',
    'crud on reviews',
    'revoking access'
]


#Users
['crud on their own book submission', 'crud on their reviews', 'crud on their accounts']


