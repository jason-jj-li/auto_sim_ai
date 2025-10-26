"""Response caching system for LLM simulation to avoid redundant API calls."""
import hashlib
import json
import os
import pickle
import time
from pathlib import Path
from typing import Optional, Dict, Any, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta


@dataclass
class CacheEntry:
    """Single cache entry with metadata."""
    response: str
    timestamp: float
    hits: int = 0
    
    def is_expired(self, max_age_seconds: Optional[float] = None) -> bool:
        """Check if entry has expired."""
        if max_age_seconds is None:
            return False
        return (time.time() - self.timestamp) > max_age_seconds


class ResponseCache:
    """Intelligent caching system for LLM responses."""
    
    def __init__(
        self,
        cache_dir: str = "data/cache",
        strategy: str = "hybrid",  # none, memory, disk, hybrid
        max_memory_entries: int = 1000,
        max_disk_size_mb: float = 500,
        max_age_hours: Optional[float] = None
    ):
        """
        Initialize response cache.
        
        Args:
            cache_dir: Directory for disk cache
            strategy: Caching strategy (none, memory, disk, hybrid)
            max_memory_entries: Maximum entries to keep in memory
            max_disk_size_mb: Maximum disk cache size in MB
            max_age_hours: Maximum age for cache entries (None = never expire)
        """
        self.cache_dir = Path(cache_dir)
        self.strategy = strategy
        self.max_memory_entries = max_memory_entries
        self.max_disk_size_mb = max_disk_size_mb
        self.max_age_seconds = max_age_hours * 3600 if max_age_hours else None
        
        # In-memory cache
        self.memory_cache: Dict[str, CacheEntry] = {}
        
        # Statistics
        self.stats = {
            'hits': 0,
            'misses': 0,
            'memory_hits': 0,
            'disk_hits': 0,
            'evictions': 0
        }
        
        # Create cache directory
        if self.strategy in ['disk', 'hybrid']:
            self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    def _generate_key(
        self,
        persona_json: str,
        question: str,
        temperature: float,
        survey_context: Optional[str] = None
    ) -> str:
        """
        Generate cache key from inputs.
        
        Args:
            persona_json: JSON representation of persona
            question: Question text
            temperature: LLM temperature
            survey_context: Optional survey context
            
        Returns:
            Cache key (hash string)
        """
        # Create a deterministic representation
        key_data = {
            'persona': persona_json,
            'question': question,
            'temperature': round(temperature, 2),  # Round to avoid float precision issues
            'context': survey_context or ""
        }
        key_string = json.dumps(key_data, sort_keys=True)
        return hashlib.sha256(key_string.encode()).hexdigest()
    
    def get(
        self,
        persona_json: str,
        question: str,
        temperature: float,
        survey_context: Optional[str] = None
    ) -> Optional[str]:
        """
        Get cached response if available.
        
        Returns:
            Cached response or None if not found/expired
        """
        if self.strategy == 'none':
            return None
        
        key = self._generate_key(persona_json, question, temperature, survey_context)
        
        # Try memory cache first
        if key in self.memory_cache:
            entry = self.memory_cache[key]
            if not entry.is_expired(self.max_age_seconds):
                entry.hits += 1
                self.stats['hits'] += 1
                self.stats['memory_hits'] += 1
                return entry.response
            else:
                # Expired, remove it
                del self.memory_cache[key]
        
        # Try disk cache if hybrid or disk-only
        if self.strategy in ['disk', 'hybrid']:
            disk_entry = self._load_from_disk(key)
            if disk_entry:
                if not disk_entry.is_expired(self.max_age_seconds):
                    disk_entry.hits += 1
                    self.stats['hits'] += 1
                    self.stats['disk_hits'] += 1
                    
                    # Promote to memory cache if hybrid
                    if self.strategy == 'hybrid':
                        self._add_to_memory(key, disk_entry)
                    
                    return disk_entry.response
                else:
                    # Expired, remove from disk
                    self._delete_from_disk(key)
        
        self.stats['misses'] += 1
        return None
    
    def put(
        self,
        persona_json: str,
        question: str,
        temperature: float,
        response: str,
        survey_context: Optional[str] = None
    ):
        """
        Store response in cache.
        
        Args:
            persona_json: JSON representation of persona
            question: Question text
            temperature: LLM temperature
            response: LLM response to cache
            survey_context: Optional survey context
        """
        if self.strategy == 'none':
            return
        
        key = self._generate_key(persona_json, question, temperature, survey_context)
        entry = CacheEntry(response=response, timestamp=time.time(), hits=0)
        
        # Store in memory
        if self.strategy in ['memory', 'hybrid']:
            self._add_to_memory(key, entry)
        
        # Store on disk
        if self.strategy in ['disk', 'hybrid']:
            self._save_to_disk(key, entry)
    
    def _add_to_memory(self, key: str, entry: CacheEntry):
        """Add entry to memory cache with LRU eviction."""
        # Check if we need to evict
        if len(self.memory_cache) >= self.max_memory_entries:
            # Evict least recently used (oldest timestamp, fewest hits)
            lru_key = min(
                self.memory_cache.keys(),
                key=lambda k: (self.memory_cache[k].hits, self.memory_cache[k].timestamp)
            )
            del self.memory_cache[lru_key]
            self.stats['evictions'] += 1
        
        self.memory_cache[key] = entry
    
    def _get_cache_file_path(self, key: str) -> Path:
        """Get file path for cache key."""
        # Use first 2 chars as subdirectory for better filesystem performance
        subdir = self.cache_dir / key[:2]
        subdir.mkdir(exist_ok=True)
        return subdir / f"{key}.pkl"
    
    def _save_to_disk(self, key: str, entry: CacheEntry):
        """Save entry to disk."""
        try:
            # Check disk size limit
            if self._get_disk_cache_size_mb() > self.max_disk_size_mb:
                self._cleanup_disk_cache()
            
            filepath = self._get_cache_file_path(key)
            with open(filepath, 'wb') as f:
                pickle.dump(entry, f)
        except Exception as e:
            print(f"Warning: Failed to save cache to disk: {e}")
    
    def _load_from_disk(self, key: str) -> Optional[CacheEntry]:
        """Load entry from disk."""
        try:
            filepath = self._get_cache_file_path(key)
            if filepath.exists():
                with open(filepath, 'rb') as f:
                    return pickle.load(f)
        except Exception as e:
            print(f"Warning: Failed to load cache from disk: {e}")
        return None
    
    def _delete_from_disk(self, key: str):
        """Delete entry from disk."""
        try:
            filepath = self._get_cache_file_path(key)
            if filepath.exists():
                filepath.unlink()
        except Exception as e:
            print(f"Warning: Failed to delete cache from disk: {e}")
    
    def _get_disk_cache_size_mb(self) -> float:
        """Get total disk cache size in MB."""
        total_size = 0
        try:
            for filepath in self.cache_dir.rglob("*.pkl"):
                total_size += filepath.stat().st_size
        except Exception:
            pass
        return total_size / (1024 * 1024)
    
    def _cleanup_disk_cache(self):
        """Remove oldest cache entries to stay under size limit."""
        # Get all cache files with their timestamps
        cache_files = []
        for filepath in self.cache_dir.rglob("*.pkl"):
            try:
                entry = pickle.load(open(filepath, 'rb'))
                cache_files.append((filepath, entry.timestamp, entry.hits))
            except Exception:
                continue
        
        # Sort by hits and timestamp (remove least valuable first)
        cache_files.sort(key=lambda x: (x[2], x[1]))
        
        # Remove oldest 20% of files
        num_to_remove = max(1, len(cache_files) // 5)
        for filepath, _, _ in cache_files[:num_to_remove]:
            try:
                filepath.unlink()
            except Exception:
                pass
    
    def clear(self):
        """Clear all cache (memory and disk)."""
        self.memory_cache.clear()
        
        if self.strategy in ['disk', 'hybrid']:
            try:
                for filepath in self.cache_dir.rglob("*.pkl"):
                    filepath.unlink()
            except Exception as e:
                print(f"Warning: Failed to clear disk cache: {e}")
        
        # Reset statistics
        self.stats = {
            'hits': 0,
            'misses': 0,
            'memory_hits': 0,
            'disk_hits': 0,
            'evictions': 0
        }
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics.
        
        Returns:
            Dictionary with cache performance stats
        """
        total_queries = self.stats['hits'] + self.stats['misses']
        hit_rate = self.stats['hits'] / total_queries if total_queries > 0 else 0.0
        
        return {
            **self.stats,
            'hit_rate': hit_rate,
            'memory_entries': len(self.memory_cache),
            'disk_size_mb': self._get_disk_cache_size_mb() if self.strategy in ['disk', 'hybrid'] else 0,
            'total_queries': total_queries
        }
    
    def export_cache(self, export_path: str):
        """Export cache to file for sharing/backup."""
        export_data = {
            'memory_cache': {k: asdict(v) for k, v in self.memory_cache.items()},
            'stats': self.stats,
            'exported_at': datetime.now().isoformat()
        }
        
        with open(export_path, 'wb') as f:
            pickle.dump(export_data, f)
    
    def import_cache(self, import_path: str, merge: bool = True):
        """
        Import cache from file.
        
        Args:
            import_path: Path to cache file
            merge: If True, merge with existing cache; if False, replace
        """
        try:
            with open(import_path, 'rb') as f:
                import_data = pickle.load(f)
            
            if not merge:
                self.clear()
            
            # Import memory cache
            for key, entry_dict in import_data['memory_cache'].items():
                entry = CacheEntry(**entry_dict)
                if not entry.is_expired(self.max_age_seconds):
                    self.memory_cache[key] = entry
        except Exception as e:
            print(f"Warning: Failed to import cache: {e}")

