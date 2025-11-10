"""
Redis client with RedisJSON support for the Telegram bot.
"""
import os
import redis
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RedisJSONClient:
    """Redis client with JSON support using RedisJSON module."""
    
    def __init__(self):
        """Initialize Redis connection with JSON support."""
        self.host = os.getenv('REDIS_HOST', 'localhost')
        self.port = int(os.getenv('REDIS_PORT', 6379))
        self.db = int(os.getenv('REDIS_DB', 0))
        self.password = os.getenv('REDIS_PASSWORD', None)
        
        try:
            # Create Redis connection
            self.client = redis.Redis(
                host=self.host,
                port=self.port,
                db=self.db,
                password=self.password if self.password else None,
                decode_responses=True
            )
            
            # Test connection
            self.client.ping()
            logger.info(f"✅ Connected to Redis at {self.host}:{self.port}")
            
            # Log Redis info
            info = self.client.info()
            logger.info(f"📊 Redis version: {info.get('redis_version', 'unknown')}")
            
            # Check for RedisJSON module
            modules = self.client.execute_command('MODULE', 'LIST')
            json_loaded = any('ReJSON' in str(module) or 'json' in str(module) for module in modules)
            
            if json_loaded:
                logger.info("✅ RedisJSON module loaded")
                # Log RedisJSON API versions
                logger.info("📦 RedisJSON APIs available:")
                logger.info("   - RedisJSON_V1 API")
                logger.info("   - RedisJSON_V2 API")
                logger.info("   - RedisJSON_V3 API")
                logger.info("   - RedisJSON_V4 API")
            else:
                logger.warning("⚠️  RedisJSON module not found. JSON operations may not work.")
                
        except redis.ConnectionError as e:
            logger.error(f"❌ Failed to connect to Redis: {e}")
            raise
        except Exception as e:
            logger.error(f"❌ Redis initialization error: {e}")
            raise
    
    def set_json(self, key, path, value):
        """
        Set JSON value at path.
        
        Args:
            key: Redis key
            path: JSON path (e.g., '$' for root, '$.field' for nested)
            value: Value to set (will be JSON encoded)
        """
        try:
            return self.client.execute_command('JSON.SET', key, path, value)
        except Exception as e:
            logger.error(f"Error setting JSON: {e}")
            return None
    
    def get_json(self, key, path='$'):
        """
        Get JSON value at path.
        
        Args:
            key: Redis key
            path: JSON path (default: '$' for root)
            
        Returns:
            JSON value or None if not found
        """
        try:
            return self.client.execute_command('JSON.GET', key, path)
        except Exception as e:
            logger.error(f"Error getting JSON: {e}")
            return None
    
    def delete_json(self, key, path='$'):
        """
        Delete JSON value at path.
        
        Args:
            key: Redis key
            path: JSON path (default: '$' for root)
        """
        try:
            return self.client.execute_command('JSON.DEL', key, path)
        except Exception as e:
            logger.error(f"Error deleting JSON: {e}")
            return None
    
    def get(self, key):
        """Get string value."""
        return self.client.get(key)
    
    def set(self, key, value, ex=None):
        """
        Set string value.
        
        Args:
            key: Redis key
            value: Value to set
            ex: Expiration time in seconds (optional)
        """
        return self.client.set(key, value, ex=ex)
    
    def delete(self, *keys):
        """Delete one or more keys."""
        return self.client.delete(*keys)
    
    def exists(self, *keys):
        """Check if one or more keys exist."""
        return self.client.exists(*keys)
    
    def keys(self, pattern='*'):
        """Get all keys matching pattern."""
        return self.client.keys(pattern)
    
    def close(self):
        """Close Redis connection."""
        if self.client:
            self.client.close()
            logger.info("Redis connection closed")


# Global Redis client instance
_redis_client = None


def get_redis_client():
    """Get or create the global Redis client instance."""
    global _redis_client
    if _redis_client is None:
        _redis_client = RedisJSONClient()
    return _redis_client


def close_redis_client():
    """Close the global Redis client instance."""
    global _redis_client
    if _redis_client is not None:
        _redis_client.close()
        _redis_client = None
