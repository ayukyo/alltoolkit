"""
MinHash - Probabilistic algorithm for efficient Jaccard similarity estimation.

MinHash uses hash functions to create compact signatures that can estimate
the Jaccard similarity between sets without comparing all elements directly.

Key features:
- Space-efficient: O(k) space per set where k is signature size
- Fast similarity estimation: O(k) comparison time
- Scalable: Can estimate similarity of large sets quickly
- Approximate: Trade-off between accuracy and signature size

Reference: "Mining of Massive Datasets" by Leskovec, Rajaraman, Ullman

Use cases:
- Document similarity detection
- Plagiarism detection
- Near-duplicate detection
- Recommendation systems
- Clustering similar items
"""

import hashlib
import random
import json
from typing import List, Set, Optional, Dict, Any, Tuple, Union, Iterable
from collections.abc import Hashable

__version__ = "1.0.0"

# Default number of hash functions (signature size)
DEFAULT_NUM_HASH = 128

# Large prime for hash function
LARGE_PRIME = 4294967311  # Prime > 2^32


class MinHashSignature:
    """
    A MinHash signature for a single set.
    
    Stores the minimum hash values for each hash function,
    representing the set's compact signature for similarity comparison.
    """
    
    def __init__(self, signature: List[int], num_hash: int):
        """
        Initialize a MinHash signature.
        
        Args:
            signature: List of minimum hash values
            num_hash: Number of hash functions used
        """
        self._signature = list(signature)
        self._num_hash = num_hash
    
    @property
    def signature(self) -> List[int]:
        """Return the signature values."""
        return self._signature.copy()
    
    @property
    def num_hash(self) -> int:
        """Return the number of hash functions."""
        return self._num_hash
    
    def jaccard_similarity(self, other: 'MinHashSignature') -> float:
        """
        Estimate Jaccard similarity with another signature.
        
        Args:
            other: Another MinHashSignature to compare with
        
        Returns:
            Estimated Jaccard similarity (0.0 to 1.0)
        
        Example:
            >>> sig1 = MinHashSignature([1, 2, 3, 4], 4)
            >>> sig2 = MinHashSignature([1, 2, 5, 6], 4)
            >>> sim = sig1.jaccard_similarity(sig2)
            >>> 0.0 <= sim <= 1.0
            True
        """
        if self._num_hash != other._num_hash:
            raise ValueError("Signatures must have the same number of hash functions")
        
        matches = sum(1 for a, b in zip(self._signature, other._signature) if a == b)
        return matches / self._num_hash
    
    def jaccard_distance(self, other: 'MinHashSignature') -> float:
        """
        Estimate Jaccard distance with another signature.
        
        Args:
            other: Another MinHashSignature to compare with
        
        Returns:
            Estimated Jaccard distance (0.0 to 1.0)
        """
        return 1.0 - self.jaccard_similarity(other)
    
    def to_json(self) -> str:
        """
        Serialize signature to JSON string.
        
        Returns:
            JSON representation
        """
        return json.dumps({
            'signature': self._signature,
            'num_hash': self._num_hash
        })
    
    @classmethod
    def from_json(cls, data: str) -> 'MinHashSignature':
        """
        Deserialize signature from JSON string.
        
        Args:
            data: JSON string representation
        
        Returns:
            New MinHashSignature instance
        """
        obj = json.loads(data)
        return cls(obj['signature'], obj['num_hash'])
    
    def __repr__(self) -> str:
        preview = self._signature[:5]
        return f"MinHashSignature(num_hash={self._num_hash}, preview={preview}...)"
    
    def __len__(self) -> int:
        return self._num_hash
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, MinHashSignature):
            return False
        return self._signature == other._signature and self._num_hash == other._num_hash


class MinHash:
    """
    MinHash generator for computing and comparing set similarity signatures.
    
    Uses k independent hash functions to create compact signatures that
    can estimate Jaccard similarity efficiently.
    
    Example:
        >>> mh = MinHash(num_hash=128)
        >>> sig1 = mh.compute_signature({'a', 'b', 'c'})
        >>> sig2 = mh.compute_signature({'a', 'b', 'd'})
        >>> similarity = sig1.jaccard_similarity(sig2)
        >>> 0.0 <= similarity <= 1.0
        True
    """
    
    def __init__(self, num_hash: int = DEFAULT_NUM_HASH, seed: Optional[int] = None):
        """
        Initialize a MinHash generator.
        
        Args:
            num_hash: Number of hash functions (signature size)
            seed: Random seed for reproducible hash functions
        
        Raises:
            ValueError: If num_hash <= 0
        """
        if num_hash <= 0:
            raise ValueError("num_hash must be positive")
        
        self._num_hash = num_hash
        
        # Generate random hash function coefficients
        rng = random.Random(seed)
        self._coeff_a = [rng.randint(1, LARGE_PRIME - 1) for _ in range(num_hash)]
        self._coeff_b = [rng.randint(0, LARGE_PRIME - 1) for _ in range(num_hash)]
    
    @property
    def num_hash(self) -> int:
        """Return the number of hash functions."""
        return self._num_hash
    
    def _hash_element(self, element: Hashable, idx: int) -> int:
        """
        Compute hash value for an element using the idx-th hash function.
        
        Uses polynomial rolling hash formula: h(x) = (a * h(x) + b) mod p
        
        Args:
            element: Element to hash
            idx: Hash function index
        
        Returns:
            Hash value
        """
        # Convert element to bytes for hashing
        if isinstance(element, bytes):
            data = element
        elif isinstance(element, str):
            data = element.encode('utf-8')
        else:
            data = str(element).encode('utf-8')
        
        # Use SHA-256 to get a consistent integer value
        h = int.from_bytes(hashlib.sha256(data).digest()[:8], 'big')
        
        # Apply linear transformation for independent hash function
        a = self._coeff_a[idx]
        b = self._coeff_b[idx]
        
        return (a * h + b) % LARGE_PRIME
    
    def compute_signature(self, elements: Iterable[Hashable]) -> MinHashSignature:
        """
        Compute MinHash signature for a set of elements.
        
        Args:
            elements: Iterable of hashable elements
        
        Returns:
            MinHashSignature representing the set
        
        Example:
            >>> mh = MinHash(num_hash=64, seed=42)
            >>> sig = mh.compute_signature(['apple', 'banana', 'cherry'])
            >>> len(sig)
            64
        """
        # Initialize signature with infinity
        signature = [LARGE_PRIME] * self._num_hash
        
        for element in elements:
            for i in range(self._num_hash):
                h = self._hash_element(element, i)
                if h < signature[i]:
                    signature[i] = h
        
        return MinHashSignature(signature, self._num_hash)
    
    def compute_signature_from_text(self, text: str, 
                                     ngram_size: int = 3,
                                     word_level: bool = False) -> MinHashSignature:
        """
        Compute MinHash signature from text using shingling.
        
        Args:
            text: Input text
            ngram_size: Size of n-grams (default: 3 for character shingles)
            word_level: If True, use word n-grams instead of character n-grams
        
        Returns:
            MinHashSignature representing the text
        
        Example:
            >>> mh = MinHash(num_hash=64, seed=42)
            >>> sig = mh.compute_signature_from_text("hello world")
            >>> len(sig)
            64
        """
        if word_level:
            words = text.lower().split()
            if len(words) < ngram_size:
                shingles = set(tuple(words[i:i+ngram_size]) 
                              for i in range(max(1, len(words) - ngram_size + 1)))
            else:
                shingles = set(tuple(words[i:i+ngram_size]) 
                              for i in range(len(words) - ngram_size + 1))
        else:
            # Character n-grams (shingles)
            text_lower = text.lower()
            if len(text_lower) < ngram_size:
                shingles = {text_lower}
            else:
                shingles = {text_lower[i:i+ngram_size] 
                           for i in range(len(text_lower) - ngram_size + 1)}
        
        return self.compute_signature(shingles)
    
    def jaccard_similarity(self, set1: Set[Hashable], set2: Set[Hashable]) -> float:
        """
        Estimate Jaccard similarity between two sets.
        
        Args:
            set1: First set
            set2: Second set
        
        Returns:
            Estimated Jaccard similarity (0.0 to 1.0)
        
        Note:
            For exact similarity, use exact_jaccard_similarity()
        """
        sig1 = self.compute_signature(set1)
        sig2 = self.compute_signature(set2)
        return sig1.jaccard_similarity(sig2)
    
    def jaccard_distance(self, set1: Set[Hashable], set2: Set[Hashable]) -> float:
        """
        Estimate Jaccard distance between two sets.
        
        Args:
            set1: First set
            set2: Second set
        
        Returns:
            Estimated Jaccard distance (0.0 to 1.0)
        """
        return 1.0 - self.jaccard_similarity(set1, set2)
    
    def get_hash_coefficients(self) -> Tuple[List[int], List[int]]:
        """
        Get the hash function coefficients for serialization.
        
        Returns:
            Tuple of (coefficients_a, coefficients_b)
        
        Example:
            >>> mh = MinHash(num_hash=64, seed=42)
            >>> a, b = mh.get_hash_coefficients()
            >>> len(a)
            64
        """
        return self._coeff_a.copy(), self._coeff_b.copy()
    
    def to_json(self) -> str:
        """
        Serialize MinHash generator to JSON.
        
        Returns:
            JSON representation
        
        Example:
            >>> mh1 = MinHash(num_hash=64, seed=42)
            >>> data = mh1.to_json()
            >>> mh2 = MinHash.from_json(data)
            >>> sig1 = mh1.compute_signature({'a', 'b'})
            >>> sig2 = mh2.compute_signature({'a', 'b'})
            >>> sig1 == sig2
            True
        """
        return json.dumps({
            'num_hash': self._num_hash,
            'coeff_a': self._coeff_a,
            'coeff_b': self._coeff_b
        })
    
    @classmethod
    def from_json(cls, data: str) -> 'MinHash':
        """
        Deserialize MinHash generator from JSON.
        
        Args:
            data: JSON string representation
        
        Returns:
            New MinHash instance
        """
        obj = json.loads(data)
        mh = cls.__new__(cls)
        mh._num_hash = obj['num_hash']
        mh._coeff_a = obj['coeff_a']
        mh._coeff_b = obj['coeff_b']
        return mh
    
    def __repr__(self) -> str:
        return f"MinHash(num_hash={self._num_hash})"


class MinHashLSH:
    """
    Locality-Sensitive Hashing (LSH) index for MinHash signatures.
    
    Efficiently finds candidate pairs of similar items without
    comparing all pairs. Uses band-based hashing to bucket similar items.
    
    Example:
        >>> lsh = MinHashLSH(num_hash=128, num_bands=32, rows_per_band=4)
        >>> mh = MinHash(num_hash=128, seed=42)
        >>> sig1 = mh.compute_signature({'a', 'b', 'c'})
        >>> sig2 = mh.compute_signature({'a', 'b', 'd'})
        >>> lsh.insert('item1', sig1)
        >>> lsh.insert('item2', sig2)
        >>> candidates = lsh.query(sig1)
        >>> 'item1' in candidates
        True
    """
    
    def __init__(self, num_hash: int, num_bands: int = 16, rows_per_band: int = 8):
        """
        Initialize LSH index.
        
        Args:
            num_hash: Number of hash functions (must match MinHash generator)
            num_bands: Number of bands for LSH
            rows_per_band: Number of rows per band
        
        Note:
            num_bands * rows_per_band should equal num_hash for best results.
            Higher num_bands gives higher recall but slower queries.
        """
        if num_hash != num_bands * rows_per_band:
            # Auto-adjust if mismatch
            num_bands = min(num_bands, num_hash // rows_per_band)
            if num_bands < 1:
                num_bands = 1
                rows_per_band = num_hash
        
        self._num_hash = num_hash
        self._num_bands = num_bands
        self._rows_per_band = rows_per_band
        
        # Storage: band_hash -> set of item keys
        self._buckets: List[Dict[str, Set[str]]] = [{} for _ in range(num_bands)]
        
        # Item storage: key -> signature
        self._items: Dict[str, MinHashSignature] = {}
    
    @property
    def num_bands(self) -> int:
        """Return number of bands."""
        return self._num_bands
    
    @property
    def rows_per_band(self) -> int:
        """Return rows per band."""
        return self._rows_per_band
    
    @property
    def count(self) -> int:
        """Return number of items in the index."""
        return len(self._items)
    
    def _band_hash(self, signature: List[int], band_idx: int) -> str:
        """
        Compute hash key for a band of the signature.
        
        Args:
            signature: Signature values
            band_idx: Band index
        
        Returns:
            Hash string for the band
        """
        start = band_idx * self._rows_per_band
        end = start + self._rows_per_band
        band_values = tuple(signature[start:end])
        # Use tuple as hash key
        return str(band_values)
    
    def insert(self, key: str, signature: MinHashSignature) -> None:
        """
        Insert an item into the LSH index.
        
        Args:
            key: Unique identifier for the item
            signature: MinHash signature for the item
        
        Example:
            >>> lsh = MinHashLSH(num_hash=64, num_bands=16, rows_per_band=4)
            >>> mh = MinHash(num_hash=64, seed=42)
            >>> sig = mh.compute_signature({'a', 'b'})
            >>> lsh.insert('my_item', sig)
            >>> lsh.count
            1
        """
        if signature.num_hash != self._num_hash:
            raise ValueError(f"Signature size {signature.num_hash} doesn't match index size {self._num_hash}")
        
        # Store item
        self._items[key] = signature
        
        # Add to buckets for each band
        sig_values = signature.signature
        for band_idx in range(self._num_bands):
            band_hash = self._band_hash(sig_values, band_idx)
            if band_hash not in self._buckets[band_idx]:
                self._buckets[band_idx][band_hash] = set()
            self._buckets[band_idx][band_hash].add(key)
    
    def query(self, signature: MinHashSignature, 
              include_key: Optional[str] = None) -> Set[str]:
        """
        Find candidate similar items for a signature.
        
        Args:
            signature: Query MinHash signature
            include_key: If provided, always include this key in results
        
        Returns:
            Set of candidate keys that may be similar
        
        Example:
            >>> lsh = MinHashLSH(num_hash=64, num_bands=16, rows_per_band=4)
            >>> mh = MinHash(num_hash=64, seed=42)
            >>> sig1 = mh.compute_signature({'a', 'b'})
            >>> sig2 = mh.compute_signature({'a', 'c'})
            >>> lsh.insert('item1', sig1)
            >>> lsh.insert('item2', sig2)
            >>> candidates = lsh.query(sig1)
            >>> 'item1' in candidates
            True
        """
        if signature.num_hash != self._num_hash:
            raise ValueError(f"Signature size {signature.num_hash} doesn't match index size {self._num_hash}")
        
        candidates: Set[str] = set()
        sig_values = signature.signature
        
        # Collect candidates from each band
        for band_idx in range(self._num_bands):
            band_hash = self._band_hash(sig_values, band_idx)
            if band_hash in self._buckets[band_idx]:
                candidates.update(self._buckets[band_idx][band_hash])
        
        # Optionally include a specific key
        if include_key is not None:
            candidates.add(include_key)
        
        return candidates
    
    def remove(self, key: str) -> bool:
        """
        Remove an item from the LSH index.
        
        Args:
            key: Key of item to remove
        
        Returns:
            True if item was found and removed, False otherwise
        """
        if key not in self._items:
            return False
        
        signature = self._items[key]
        sig_values = signature.signature
        
        # Remove from buckets
        for band_idx in range(self._num_bands):
            band_hash = self._band_hash(sig_values, band_idx)
            if band_hash in self._buckets[band_idx]:
                self._buckets[band_idx][band_hash].discard(key)
                # Clean up empty buckets
                if not self._buckets[band_idx][band_hash]:
                    del self._buckets[band_idx][band_hash]
        
        # Remove from items
        del self._items[key]
        return True
    
    def clear(self) -> None:
        """Clear all items from the index."""
        self._buckets = [{} for _ in range(self._num_bands)]
        self._items.clear()
    
    def get_signature(self, key: str) -> Optional[MinHashSignature]:
        """
        Get the signature for a stored item.
        
        Args:
            key: Item key
        
        Returns:
            MinHashSignature if found, None otherwise
        """
        return self._items.get(key)
    
    def find_similar_pairs(self, threshold: float = 0.5) -> List[Tuple[str, str, float]]:
        """
        Find all pairs of items with similarity above threshold.
        
        Args:
            threshold: Minimum similarity threshold (0.0 to 1.0)
        
        Returns:
            List of (key1, key2, similarity) tuples
        
        Example:
            >>> lsh = MinHashLSH(num_hash=64, num_bands=16, rows_per_band=4)
            >>> mh = MinHash(num_hash=64, seed=42)
            >>> sig1 = mh.compute_signature({'a', 'b', 'c'})
            >>> sig2 = mh.compute_signature({'a', 'b', 'd'})
            >>> lsh.insert('item1', sig1)
            >>> lsh.insert('item2', sig2)
            >>> pairs = lsh.find_similar_pairs(threshold=0.3)
            >>> len(pairs) >= 0
            True
        """
        pairs: List[Tuple[str, str, float]] = []
        checked: Set[Tuple[str, str]] = set()
        
        for key1, sig1 in self._items.items():
            candidates = self.query(sig1, include_key=key1)
            
            for key2 in candidates:
                if key1 >= key2:
                    continue
                
                pair = (key1, key2)
                if pair in checked:
                    continue
                checked.add(pair)
                
                sig2 = self._items[key2]
                similarity = sig1.jaccard_similarity(sig2)
                
                if similarity >= threshold:
                    pairs.append((key1, key2, similarity))
        
        # Sort by similarity descending
        pairs.sort(key=lambda x: -x[2])
        return pairs
    
    def stats(self) -> Dict[str, Any]:
        """
        Get statistics about the LSH index.
        
        Returns:
            Dictionary with index statistics
        """
        total_buckets = sum(len(band) for band in self._buckets)
        avg_bucket_size = total_buckets / self._num_bands if self._num_bands > 0 else 0
        
        bucket_counts = []
        for band in self._buckets:
            band_sizes = [len(items) for items in band.values()]
            if band_sizes:
                bucket_counts.extend(band_sizes)
        
        return {
            'num_items': len(self._items),
            'num_bands': self._num_bands,
            'rows_per_band': self._rows_per_band,
            'total_buckets': total_buckets,
            'avg_buckets_per_band': avg_bucket_size,
            'avg_items_per_bucket': sum(bucket_counts) / len(bucket_counts) if bucket_counts else 0,
        }
    
    def __repr__(self) -> str:
        return f"MinHashLSH(num_items={self.count}, num_bands={self._num_bands})"


class MinHashMap:
    """
    A collection of MinHash signatures with similarity queries.
    
    Provides a high-level interface for managing multiple signatures
    and finding similar items.
    
    Example:
        >>> mh = MinHashMap(num_hash=128, seed=42)
        >>> mh.add('doc1', {'apple', 'banana', 'cherry'})
        >>> mh.add('doc2', {'apple', 'banana', 'date'})
        >>> similar = mh.find_similar('doc1', threshold=0.5)
        >>> len(similar) >= 0
        True
    """
    
    def __init__(self, num_hash: int = DEFAULT_NUM_HASH, seed: Optional[int] = None):
        """
        Initialize a MinHashMap.
        
        Args:
            num_hash: Number of hash functions
            seed: Random seed for reproducibility
        """
        self._minhash = MinHash(num_hash=num_hash, seed=seed)
        self._signatures: Dict[str, MinHashSignature] = {}
        self._lsh: Optional[MinHashLSH] = None
    
    @property
    def num_hash(self) -> int:
        """Return number of hash functions."""
        return self._minhash.num_hash
    
    @property
    def count(self) -> int:
        """Return number of items."""
        return len(self._signatures)
    
    def add(self, key: str, elements: Iterable[Hashable]) -> MinHashSignature:
        """
        Add a set with its signature.
        
        Args:
            key: Unique identifier
            elements: Set of elements
        
        Returns:
            Computed MinHashSignature
        
        Example:
            >>> mh = MinHashMap(num_hash=64, seed=42)
            >>> sig = mh.add('my_set', {1, 2, 3})
            >>> mh.contains('my_set')
            True
        """
        signature = self._minhash.compute_signature(elements)
        self._signatures[key] = signature
        
        # Invalidate LSH index
        self._lsh = None
        
        return signature
    
    def add_text(self, key: str, text: str, 
                 ngram_size: int = 3, word_level: bool = False) -> MinHashSignature:
        """
        Add a text document with shingling.
        
        Args:
            key: Unique identifier
            text: Text content
            ngram_size: Size of n-grams
            word_level: Use word n-grams if True
        
        Returns:
            Computed MinHashSignature
        """
        signature = self._minhash.compute_signature_from_text(
            text, ngram_size=ngram_size, word_level=word_level
        )
        self._signatures[key] = signature
        self._lsh = None
        return signature
    
    def add_signature(self, key: str, signature: MinHashSignature) -> None:
        """
        Add a pre-computed signature.
        
        Args:
            key: Unique identifier
            signature: MinHashSignature to add
        """
        if signature.num_hash != self.num_hash:
            raise ValueError(f"Signature size {signature.num_hash} doesn't match {self.num_hash}")
        self._signatures[key] = signature
        self._lsh = None
    
    def get(self, key: str) -> Optional[MinHashSignature]:
        """
        Get signature for a key.
        
        Args:
            key: Item key
        
        Returns:
            MinHashSignature if found, None otherwise
        """
        return self._signatures.get(key)
    
    def contains(self, key: str) -> bool:
        """Check if key exists."""
        return key in self._signatures
    
    def remove(self, key: str) -> bool:
        """
        Remove an item.
        
        Args:
            key: Key to remove
        
        Returns:
            True if removed, False if not found
        """
        if key in self._signatures:
            del self._signatures[key]
            self._lsh = None
            return True
        return False
    
    def similarity(self, key1: str, key2: str) -> float:
        """
        Compute similarity between two stored items.
        
        Args:
            key1: First item key
            key2: Second item key
        
        Returns:
            Estimated Jaccard similarity
        
        Raises:
            KeyError: If either key doesn't exist
        """
        sig1 = self._signatures[key1]
        sig2 = self._signatures[key2]
        return sig1.jaccard_similarity(sig2)
    
    def _build_lsh(self, num_bands: int = 16) -> MinHashLSH:
        """Build LSH index."""
        rows_per_band = self.num_hash // num_bands
        if rows_per_band < 1:
            rows_per_band = 1
        
        lsh = MinHashLSH(num_hash=self.num_hash, num_bands=num_bands, rows_per_band=rows_per_band)
        
        for key, sig in self._signatures.items():
            lsh.insert(key, sig)
        
        return lsh
    
    def find_similar(self, key: str, threshold: float = 0.5, 
                     num_bands: int = 16) -> List[Tuple[str, float]]:
        """
        Find items similar to a given key.
        
        Args:
            key: Key to find similar items for
            threshold: Minimum similarity threshold
            num_bands: Number of bands for LSH
        
        Returns:
            List of (key, similarity) tuples sorted by similarity descending
        
        Example:
            >>> mh = MinHashMap(num_hash=64, seed=42)
            >>> mh.add('a', {1, 2, 3})
            >>> mh.add('b', {1, 2, 4})
            >>> similar = mh.find_similar('a', threshold=0.3)
            >>> len(similar) >= 0
            True
        """
        if key not in self._signatures:
            raise KeyError(f"Key '{key}' not found")
        
        # Build LSH if needed
        if self._lsh is None:
            self._lsh = self._build_lsh(num_bands)
        
        signature = self._signatures[key]
        candidates = self._lsh.query(signature, include_key=key)
        
        results: List[Tuple[str, float]] = []
        for candidate_key in candidates:
            if candidate_key == key:
                continue
            sim = signature.jaccard_similarity(self._signatures[candidate_key])
            if sim >= threshold:
                results.append((candidate_key, sim))
        
        # Sort by similarity descending
        results.sort(key=lambda x: -x[1])
        return results
    
    def find_all_similar_pairs(self, threshold: float = 0.5, 
                               num_bands: int = 16) -> List[Tuple[str, str, float]]:
        """
        Find all pairs of similar items.
        
        Args:
            threshold: Minimum similarity threshold
            num_bands: Number of bands for LSH
        
        Returns:
            List of (key1, key2, similarity) tuples sorted by similarity descending
        """
        if self._lsh is None:
            self._lsh = self._build_lsh(num_bands)
        
        return self._lsh.find_similar_pairs(threshold)
    
    def query_signature(self, signature: MinHashSignature, 
                        threshold: float = 0.5,
                        num_bands: int = 16) -> List[Tuple[str, float]]:
        """
        Find items similar to a query signature.
        
        Args:
            signature: Query signature
            threshold: Minimum similarity threshold
            num_bands: Number of bands for LSH
        
        Returns:
            List of (key, similarity) tuples sorted by similarity descending
        """
        if signature.num_hash != self.num_hash:
            raise ValueError(f"Signature size mismatch: {signature.num_hash} vs {self.num_hash}")
        
        if self._lsh is None:
            self._lsh = self._build_lsh(num_bands)
        
        candidates = self._lsh.query(signature)
        
        results: List[Tuple[str, float]] = []
        for key in candidates:
            sim = signature.jaccard_similarity(self._signatures[key])
            if sim >= threshold:
                results.append((key, sim))
        
        results.sort(key=lambda x: -x[1])
        return results
    
    def clear(self) -> None:
        """Remove all items."""
        self._signatures.clear()
        self._lsh = None
    
    def keys(self) -> List[str]:
        """Return all keys."""
        return list(self._signatures.keys())
    
    def to_json(self) -> str:
        """
        Serialize to JSON.
        
        Returns:
            JSON string representation
        """
        data = {
            'num_hash': self.num_hash,
            'minhash': self._minhash.to_json(),
            'signatures': {k: v.to_json() for k, v in self._signatures.items()}
        }
        return json.dumps(data)
    
    @classmethod
    def from_json(cls, data: str) -> 'MinHashMap':
        """
        Deserialize from JSON.
        
        Args:
            data: JSON string representation
        
        Returns:
            New MinHashMap instance
        """
        obj = json.loads(data)
        mh = cls.__new__(cls)
        mh._minhash = MinHash.from_json(obj['minhash'])
        mh._signatures = {
            k: MinHashSignature.from_json(v) 
            for k, v in obj['signatures'].items()
        }
        mh._lsh = None
        return mh
    
    def __len__(self) -> int:
        return len(self._signatures)
    
    def __contains__(self, key: str) -> bool:
        return key in self._signatures
    
    def __repr__(self) -> str:
        return f"MinHashMap(num_items={self.count}, num_hash={self.num_hash})"


# Utility functions

def estimate_jaccard_similarity(set1: Set[Hashable], 
                                set2: Set[Hashable],
                                num_hash: int = DEFAULT_NUM_HASH,
                                seed: Optional[int] = None) -> float:
    """
    Estimate Jaccard similarity between two sets.
    
    Args:
        set1: First set
        set2: Second set
        num_hash: Number of hash functions
        seed: Random seed
    
    Returns:
        Estimated Jaccard similarity (0.0 to 1.0)
    
    Example:
        >>> sim = estimate_jaccard_similarity({1, 2, 3}, {2, 3, 4})
        >>> 0.0 <= sim <= 1.0
        True
    """
    mh = MinHash(num_hash=num_hash, seed=seed)
    return mh.jaccard_similarity(set1, set2)


def exact_jaccard_similarity(set1: Set[Hashable], set2: Set[Hashable]) -> float:
    """
    Compute exact Jaccard similarity between two sets.
    
    Args:
        set1: First set
        set2: Second set
    
    Returns:
        Exact Jaccard similarity (0.0 to 1.0)
    
    Example:
        >>> exact_jaccard_similarity({1, 2, 3}, {2, 3, 4})
        0.5
    """
    if not set1 and not set2:
        return 1.0
    if not set1 or not set2:
        return 0.0
    
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    
    return intersection / union if union > 0 else 0.0


def text_similarity(text1: str, text2: str,
                    ngram_size: int = 3,
                    num_hash: int = DEFAULT_NUM_HASH,
                    word_level: bool = False,
                    seed: Optional[int] = None) -> float:
    """
    Estimate similarity between two texts using MinHash.
    
    Args:
        text1: First text
        text2: Second text
        ngram_size: Size of n-grams for shingling
        num_hash: Number of hash functions
        word_level: Use word n-grams if True
        seed: Random seed
    
    Returns:
        Estimated Jaccard similarity
    
    Example:
        >>> sim = text_similarity("hello world", "hello earth")
        >>> 0.0 <= sim <= 1.0
        True
    """
    mh = MinHash(num_hash=num_hash, seed=seed)
    sig1 = mh.compute_signature_from_text(text1, ngram_size=ngram_size, word_level=word_level)
    sig2 = mh.compute_signature_from_text(text2, ngram_size=ngram_size, word_level=word_level)
    return sig1.jaccard_similarity(sig2)


def create_minhash_from_set(elements: Iterable[Hashable],
                            num_hash: int = DEFAULT_NUM_HASH,
                            seed: Optional[int] = None) -> MinHashSignature:
    """
    Create a MinHash signature from a set.
    
    Args:
        elements: Set elements
        num_hash: Number of hash functions
        seed: Random seed
    
    Returns:
        MinHashSignature
    
    Example:
        >>> sig = create_minhash_from_set({1, 2, 3}, num_hash=64)
        >>> len(sig)
        64
    """
    mh = MinHash(num_hash=num_hash, seed=seed)
    return mh.compute_signature(elements)


def create_minhash_from_text(text: str,
                             ngram_size: int = 3,
                             num_hash: int = DEFAULT_NUM_HASH,
                             word_level: bool = False,
                             seed: Optional[int] = None) -> MinHashSignature:
    """
    Create a MinHash signature from text.
    
    Args:
        text: Input text
        ngram_size: Size of n-grams
        num_hash: Number of hash functions
        word_level: Use word n-grams if True
        seed: Random seed
    
    Returns:
        MinHashSignature
    
    Example:
        >>> sig = create_minhash_from_text("hello world", num_hash=64)
        >>> len(sig)
        64
    """
    mh = MinHash(num_hash=num_hash, seed=seed)
    return mh.compute_signature_from_text(text, ngram_size=ngram_size, word_level=word_level)


def similarity_error_bounds(num_hash: int, confidence: float = 0.95) -> Tuple[float, float]:
    """
    Calculate expected error bounds for MinHash similarity estimation.
    
    Args:
        num_hash: Number of hash functions
        confidence: Confidence level (0.0 to 1.0)
    
    Returns:
        Tuple of (expected_error, confidence_interval)
    
    Example:
        >>> err, ci = similarity_error_bounds(128, 0.95)
        >>> err > 0
        True
    """
    import math
    
    # Standard error is approximately 1/sqrt(k)
    expected_error = 1.0 / math.sqrt(num_hash)
    
    # For 95% confidence, use z = 1.96
    z = 1.96 if confidence >= 0.95 else (1.64 if confidence >= 0.90 else 1.0)
    
    # Confidence interval half-width
    ci = z * expected_error
    
    return expected_error, ci


def recommended_num_hash(target_error: float = 0.1) -> int:
    """
    Calculate recommended number of hash functions for a target error.
    
    Args:
        target_error: Target standard error (0.0 to 1.0)
    
    Returns:
        Recommended number of hash functions
    
    Example:
        >>> n = recommended_num_hash(0.05)
        >>> n > 0
        True
    """
    import math
    return max(1, int(math.ceil(1.0 / (target_error ** 2))))