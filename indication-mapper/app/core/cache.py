import json
from typing import Optional
import redis
from app.models.indication import DrugIndication
from dotenv import load_dotenv
import os

load_dotenv()

# Redis configuration
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", None)

# Initialize Redis client
redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB,
    password=REDIS_PASSWORD,
    decode_responses=True,
)


def get_cached_mapping(setid: str) -> Optional[DrugIndication]:
    """
    Retrieve a cached mapping from Redis.
    
    Args:
        setid: The set ID to look up in the cache
        
    Returns:
        DrugIndication object if found in cache, None otherwise
    """
    try:
        cached_data = redis_client.get(f"mapping:{setid}")
        if cached_data:
            data = json.loads(cached_data)
            return DrugIndication(**data)
        return None
    except Exception as e:
        # Log the error but don't fail the request
        print(f"Error retrieving from cache: {e}")
        return None


def cache_mapping(setid: str, mapping: DrugIndication):
    """
    Cache a mapping in Redis.
    
    Args:
        setid: The set ID to use as cache key
        mapping: The DrugIndication object to cache
    """
    try:
        # Convert DrugIndication to dict and then to JSON
        data = mapping.model_dump()
        redis_client.set(f"mapping:{setid}", json.dumps(data))
    except Exception as e:
        # Log the error but don't fail the request
        print(f"Error caching mapping: {e}")
