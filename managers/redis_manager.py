import redis

from src.core.config import settings


class RedisManager:
    def __init__(
        self,
        host: str = settings.REDIS_HOST,
        port: int = settings.REDIS_PORT,
        cache_name: str = settings.CACHE_NAME,
        ttl: int = settings.refresh_token_ttl_min,
    ):
        self.redisClient = redis.StrictRedis(host=host, port=port, decode_responses=True)
        self.cache_name = cache_name
        self.redisClient.expire(cache_name, ttl)


redis_manager = RedisManager()
