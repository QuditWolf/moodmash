"""
Embedding Cache Service

This module provides caching for embedding vectors to minimize Titan API calls.
Uses DynamoDB as the cache backend with SHA-256 hashing for cache keys.
"""

import hashlib
import logging
import time
from typing import List, Optional
from .dynamodb_client import get_dynamodb_client

logger = logging.getLogger(__name__)


class CacheService:
    """
    Embedding cache service using DynamoDB.
    
    Caches embedding vectors keyed by SHA-256 hash of the embedding document.
    Tracks hit count and last accessed timestamp for cache analytics.
    """
    
    def __init__(self, table_name: str = "EmbeddingCache"):
        """
        Initialize cache service.
        
        Args:
            table_name: Name of DynamoDB table for cache
        """
        self.table_name = table_name
        self.dynamodb = get_dynamodb_client()
        logger.info(f"Cache service initialized (table: {table_name})")
    
    def _compute_hash(self, document: str) -> str:
        """
        Compute SHA-256 hash of document.
        
        Args:
            document: Text document to hash
            
        Returns:
            Hex string of SHA-256 hash
        """
        return hashlib.sha256(document.encode('utf-8')).hexdigest()
    
    def get(self, document: str) -> Optional[List[float]]:
        """
        Get cached embedding vector for document.
        
        Args:
            document: Embedding document text
            
        Returns:
            Cached vector if found, None otherwise
        """
        try:
            doc_hash = self._compute_hash(document)
            
            # Try to get from cache
            item = self.dynamodb.get_item(
                self.table_name,
                {'docHash': doc_hash}
            )
            
            if item:
                # Cache hit - update hit count and last accessed
                vector = item.get('vector')
                hit_count = item.get('hitCount', 0)
                
                logger.info(f"Cache HIT for hash {doc_hash[:8]}... (hits: {hit_count + 1})")
                
                # Update hit count and last accessed timestamp
                self.dynamodb.update_item(
                    self.table_name,
                    {'docHash': doc_hash},
                    {
                        'hitCount': hit_count + 1,
                        'lastAccessedAt': int(time.time())
                    }
                )
                
                return vector
            else:
                # Cache miss
                logger.info(f"Cache MISS for hash {doc_hash[:8]}...")
                return None
                
        except Exception as e:
            logger.error(f"Cache get error: {str(e)}")
            # Return None on cache errors (don't fail the request)
            return None
    
    def put(self, document: str, vector: List[float]) -> bool:
        """
        Store embedding vector in cache.
        
        Args:
            document: Embedding document text
            vector: Embedding vector to cache
            
        Returns:
            True if successful
        """
        try:
            doc_hash = self._compute_hash(document)
            timestamp = int(time.time())
            
            # Store in cache
            item = {
                'docHash': doc_hash,
                'vector': vector,
                'createdAt': timestamp,
                'hitCount': 0,
                'lastAccessedAt': timestamp
            }
            
            self.dynamodb.put_item(self.table_name, item)
            
            logger.info(f"Cached embedding for hash {doc_hash[:8]}...")
            return True
            
        except Exception as e:
            logger.error(f"Cache put error: {str(e)}")
            # Don't fail the request on cache errors
            return False
    
    def get_stats(self) -> dict:
        """
        Get cache statistics.
        
        Returns:
            Dictionary with cache stats (total entries, total hits, etc.)
        """
        try:
            # Scan cache table for stats
            items = self.dynamodb.scan(self.table_name)
            
            total_entries = len(items)
            total_hits = sum(item.get('hitCount', 0) for item in items)
            
            return {
                'totalEntries': total_entries,
                'totalHits': total_hits,
                'averageHits': total_hits / total_entries if total_entries > 0 else 0
            }
        except Exception as e:
            logger.error(f"Failed to get cache stats: {str(e)}")
            return {
                'totalEntries': 0,
                'totalHits': 0,
                'averageHits': 0,
                'error': str(e)
            }


# Singleton instance
_cache_service = None


def get_cache_service() -> CacheService:
    """Get singleton cache service instance."""
    global _cache_service
    if _cache_service is None:
        _cache_service = CacheService()
    return _cache_service
