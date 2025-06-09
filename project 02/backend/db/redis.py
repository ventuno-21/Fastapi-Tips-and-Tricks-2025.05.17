from redis.asyncio import Redis
import os
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")


# Initialize a Redis client instance to interact with the Redis database
# Uses REDIS_HOST and REDIS_PORT variables (assumed to be defined elsewhere) for connection
# Connects to database index 0
_token_blacklist = Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=0,
)


# Async function to add a JWT token identifier (jti) to the Redis blacklist
# Takes a string parameter 'jti' representing the unique token identifier
async def add_jti_to_blacklist(jti: str):
    # Sets a key in Redis with the name 'jti' and value "blacklisted"
    # This marks the token as blacklisted, preventing its use
    await _token_blacklist.set(jti, "blacklisted")


# Async function to check if a JWT token identifier (jti) is blacklisted
# Takes a string parameter 'jti' and returns a boolean
async def is_jti_blacklisted(jti: str) -> bool:
    # Checks if the 'jti' key exists in the Redis database
    # Returns True if the token is blacklisted, False otherwise
    return await _token_blacklist.exists(jti)
