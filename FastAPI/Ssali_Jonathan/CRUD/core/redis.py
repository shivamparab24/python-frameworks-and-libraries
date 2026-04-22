import redis.asyncio as redis

from FastAPI.Ssali_Jonathan.CRUD.core.config import get_settings

settings = get_settings()

JTI_EXPIRY = 3600

# token_blocklist = redis.StrictRedis(
#     host = settings.redis_host,
#     port = settings.redis_port,
#     db = 0
# )

token_blocklist = redis.from_url(
    settings.redis_url
)

async def add_jti_to_blocklist(jti: str) -> None:
    await token_blocklist.set(
        name = jti,
        value = "",
        ex = JTI_EXPIRY
    ) 


async def token_in_blocklist(jti: str) -> bool:
    jti = await token_blocklist.get(jti)

    return jti is not None



# admin

[
    "adding users", 
    "change roles",
    "crud on useers",
    "book submissions",
    "crud on users",
    "crud on reviews",
    "revoking access"
]



# users

[
    "crud on their own book submissons",
    "crud on their reviews",
    "crud on their own accounts"
]