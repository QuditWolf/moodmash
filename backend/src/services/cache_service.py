"""
Embedding Cache Service

Provides caching for embedding generation to avoid redundant API calls.
Uses SHA-256 hashing for cache keys.
"""

import hashlib
import time
import logging
from typing import List, Optional, Dict, Any
from datetime import datetime

from .dynamodb_client import DynamoDBClient

logger = logging.getLogger(__name__)


class CacheService:
    """
    Cache service for embedding vectors.
    
    Caches embeddings by document hash to avoid redundant Titan API calls.
    Tracks hit count and last accessed timestamp for analytics.
    """
    
    def __init__(self, dynamodb_client: Optional[DynamoDBClient] = None):
        """
        Initialize cache service.
        
        Args:
            dynamodb_client: DynamoDBClient instance (creates new if None)
        """
        self.db = dynamodb_client or DynamoDBClient()
    
    def compute_hash(self, document: str) -> str:
        """
        Compute SHA-256 hash of document.
        
        Args:
            document: Text document to hash
            
        Returns:
            Hexadecimal hash string (64 characters)
        """
        doc_bytes = document.encode('utf-8')
        hash_obj = hashlib.sha256(doc_bytes)
        return hash_obj.hexdigest()
    
    def get(self, doc_hash: str) -> Optional[List[float]]:
        """
        Get cached embedding by document hash.
        
        Args:
            doc_hash: SHA-256 hash of document
            
        Returns:
            Cached embedding vector if found, None otherwise
        """
        try:
            cache_entry = self.db.get_cache(doc_hash)
            
            if cache_entry:
                # Update hit count and last accessed
                self._update_cache_stats(doc_hash, cache_entry)
                
                embedding = cache_entry.get("embedding")
                logger.info(f"Cache HIT for hash {doc_hash[:16]}...")
                return embedding
            
            logger.info(f"Cache MISS for hash {doc_hash[:16]}...")
            return None
            
        except Exception as e:
            logger.error(f"Error getting cache entry: {e}")
            return None
    
    def put(
        self,
        doc_hash: str,
        embedding: List[float],
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Put embedding into cache.
        
        Args:
            doc_hash: SHA-256 hash of document
            embedding: Embedding vector to cache
            metadata: Optional metadata to store with cache entry
            
        Returns:
            True if successful, False otherwise
        """
        try:
            cache_entry = {
                "docHash": doc_hash,
                "embedding": embedding,
                "hitCount": 0,
                "createdAt": datetime.utcnow().isoformat(),
                "lastAccessedAt": datetime.utcnow().isoformat()
            }
            
            if metadata:
                cache_entry["metadata"] = metadata
            
            self.db.put_cache(cache_entry)
            logger.info(f"Cached embedding for hash {doc_hash[:16]}...")
            return True
            
        except Exception as e:
            logger.error(f"Error putting cache entry: {e}")
            return False
    
    def _update_cache_stats(
        self,
        doc_hash: str,
        cache_entry: Dict[str, Any]
    ) -> None:
        """
        Update cache statistics (hit count and last accessed).
        
        Args:
            doc_hash: Document hash
            cache_entry: Current cache entry
        """
        try:
            current_hits = cache_entry.get("hitCount", 0)
            
            self.db.update(
                table_name=self.db.cache_table,
                key={"docHash": doc_hash},
                update_expression="SET hitCount = :hits, lastAccessedAt = :timestamp",
                expression_values={
                    ":hits": current_hits + 1,
                    ":timestamp": datetime.utcnow().isoformat()
                }
            )
            
            logger.debug(f"Updated cache stats for {doc_hash[:16]}... (hits: {current_hits + 1})")
            
        except Exception as e:
            # Don't fail the cache get if stats update fails
            logger.warning(f"Failed to update cache stats: {e}")
    
    def get_or_generate(
        self,
        document: str,
        generator_func,
        metadata: Optional[Dict[str, Any]] = None
    ) -> tuple[List[float], bool]:
        """
        Get embedding from cache or generate if not found.
        
        This is a convenience method that handles the cache-or-generate pattern.
        
        Args:
            document: Text document to embed
            generator_func: Function to call if cache miss (should return embedding)
            metadata: Optional metadata to store with new cache entry
            
        Returns:
            Tuple of (embedding, was_cached)
            - embedding: The embedding vector
            - was_cached: True if from cache, False if newly generated
            
        Example:
            >>> cache = CacheService()
            >>> def generate():
            ...     return titan_service.embed_text("document")
            >>> embedding, cached = cache.get_or_generate("document", generate)
        """
        # Compute hash
        doc_hash = self.compute_hash(document)
        
        # Try cache first
        cached_embedding = self.get(doc_hash)
        if cached_embedding is not None:
            return cached_embedding, True
        
        # Cache miss - generate new embedding
        logger.info(f"Generating new embedding for hash {doc_hash[:16]}...")
        start_time = time.time()
        
        new_embedding = generator_func()
        
        elapsed = time.time() - start_time
        logger.info(f"Embedding generated in {elapsed:.2f}s")
        
        # Cache the new embedding
        self.put(doc_hash, new_embedding, metadata)
        
        return new_embedding, False
    
    def get_stats(self, doc_hash: str) -> Optional[Dict[str, Any]]:
        """
        Get cache statistics for a document hash.
        
        Args:
            doc_hash: Document hash
            
        Returns:
            Dictionary with hitCount, createdAt, lastAccessedAt if found
        """
        try:
            cache_entry = self.db.get_cache(doc_hash)
            
            if cache_entry:
                return {
                    "hitCount": cache_entry.get("hitCount", 0),
                    "createdAt": cache_entry.get("createdAt"),
                    "lastAccessedAt": cache_entry.get("lastAccessedAt")
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting cache stats: {e}")
            return None
    
    def clear_cache(self, doc_hash: str) -> bool:
        """
        Clear specific cache entry.
        
        Args:
            doc_hash: Document hash to clear
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self.db.delete(
                table_name=self.db.cache_table,
                key={"docHash": doc_hash}
            )
            logger.info(f"Cleared cache for hash {doc_hash[:16]}...")
            return True
            
        except Exception as e:
            logger.error(f"Error clearing cache: {e}")
            return False
