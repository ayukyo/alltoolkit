"""
AllToolkit - Python UUID Utilities

A zero-dependency, production-ready UUID generation and manipulation utility module.
Supports UUID v1 (time-based), v3 (MD5 namespace), v4 (random), v5 (SHA-1 namespace),
and provides validation, comparison, and conversion utilities.

Author: AllToolkit
License: MIT
"""

import uuid
import hashlib
import re
from typing import Union, Optional, Tuple, List
from datetime import datetime


class UUIDUtils:
    """
    UUID generation and manipulation utilities.
    
    Provides functions for:
    - UUID v1/v3/v4/v5 generation
    - UUID validation and parsing
    - UUID comparison and sorting
    - Namespace management
    - Conversion between formats
    - Timestamp extraction (v1)
    """

    # Predefined namespace UUIDs (RFC 4122)
    NAMESPACE_DNS = uuid.UUID('6ba7b810-9dad-11d1-80b4-00c04fd430c8')
    NAMESPACE_URL = uuid.UUID('6ba7b811-9dad-11d1-80b4-00c04fd430c8')
    NAMESPACE_OID = uuid.UUID('6ba7b812-9dad-11d1-80b4-00c04fd430c8')
    NAMESPACE_X500 = uuid.UUID('6ba7b814-9dad-11d1-80b4-00c04fd430c8')

    @staticmethod
    def generate_v1() -> uuid.UUID:
        """
        Generate a UUID version 1 (time-based).
        
        Uses MAC address and current time. Useful for generating
        sortable UUIDs that reveal creation order.

        Returns:
            UUID object (version 1)

        Example:
            >>> u = UUIDUtils.generate_v1()
            >>> isinstance(u, uuid.UUID)
            True
            >>> u.version
            1
        """
        return uuid.uuid1()

    @staticmethod
    def generate_v3(namespace: Union[uuid.UUID, str], name: str) -> uuid.UUID:
        """
        Generate a UUID version 3 (MD5 namespace-based).
        
        Deterministic: same namespace + name always produces same UUID.
        Useful for generating consistent IDs from known strings.

        Args:
            namespace: Namespace UUID or string ('dns', 'url', 'oid', 'x500')
            name: The name to hash within the namespace

        Returns:
            UUID object (version 3)

        Example:
            >>> u = UUIDUtils.generate_v3(UUIDUtils.NAMESPACE_DNS, 'example.com')
            >>> str(u)
            '9073926b-929f-31c2-abc9-fad77ae3e8eb'
        """
        ns = UUIDUtils._parse_namespace(namespace)
        return uuid.uuid3(ns, name)

    @staticmethod
    def generate_v4() -> uuid.UUID:
        """
        Generate a UUID version 4 (random).
        
        Most commonly used UUID version. Uses random or pseudo-random numbers.
        Collision probability is extremely low.

        Returns:
            UUID object (version 4)

        Example:
            >>> u = UUIDUtils.generate_v4()
            >>> isinstance(u, uuid.UUID)
            True
            >>> u.version
            4
        """
        return uuid.uuid4()

    @staticmethod
    def generate_v5(namespace: Union[uuid.UUID, str], name: str) -> uuid.UUID:
        """
        Generate a UUID version 5 (SHA-1 namespace-based).
        
        Deterministic: same namespace + name always produces same UUID.
        Preferred over v3 for new applications (uses SHA-1 instead of MD5).

        Args:
            namespace: Namespace UUID or string ('dns', 'url', 'oid', 'x500')
            name: The name to hash within the namespace

        Returns:
            UUID object (version 5)

        Example:
            >>> u = UUIDUtils.generate_v5(UUIDUtils.NAMESPACE_DNS, 'example.com')
            >>> str(u)
            'cfbff0d1-9375-5685-968c-48ce8b15ae17'
        """
        ns = UUIDUtils._parse_namespace(namespace)
        return uuid.uuid5(ns, name)

    @staticmethod
    def _parse_namespace(namespace: Union[uuid.UUID, str]) -> uuid.UUID:
        """
        Parse namespace string to UUID.

        Args:
            namespace: Namespace UUID or string identifier

        Returns:
            UUID object

        Raises:
            ValueError: If namespace string is not recognized
        """
        if isinstance(namespace, uuid.UUID):
            return namespace
        
        ns_map = {
            'dns': UUIDUtils.NAMESPACE_DNS,
            'url': UUIDUtils.NAMESPACE_URL,
            'oid': UUIDUtils.NAMESPACE_OID,
            'x500': UUIDUtils.NAMESPACE_X500,
        }
        
        ns_lower = namespace.lower()
        if ns_lower in ns_map:
            return ns_map[ns_lower]
        
        # Try to parse as UUID string
        try:
            return uuid.UUID(namespace)
        except ValueError:
            raise ValueError(f"Unknown namespace: {namespace}. Use 'dns', 'url', 'oid', 'x500', or a valid UUID.")

    @staticmethod
    def parse(uuid_string: str) -> uuid.UUID:
        """
        Parse a UUID string into a UUID object.
        
        Accepts various formats:
        - Standard: '123e4567-e89b-12d3-a456-426614174000'
        - Braced: '{123e4567-e89b-12d3-a456-426614174000}'
        - URN: 'urn:uuid:123e4567-e89b-12d3-a456-426614174000'
        - No hyphens: '123e4567e89b12d3a456426614174000'

        Args:
            uuid_string: The UUID string to parse

        Returns:
            UUID object

        Raises:
            ValueError: If string is not a valid UUID

        Example:
            >>> u = UUIDUtils.parse('123e4567-e89b-12d3-a456-426614174000')
            >>> str(u)
            '123e4567-e89b-12d3-a456-426614174000'
        """
        return uuid.UUID(uuid_string)

    @staticmethod
    def is_valid(uuid_string: str) -> bool:
        """
        Check if a string is a valid UUID.

        Args:
            uuid_string: The string to validate

        Returns:
            True if valid UUID, False otherwise

        Example:
            >>> UUIDUtils.is_valid('123e4567-e89b-12d3-a456-426614174000')
            True
            >>> UUIDUtils.is_valid('not-a-uuid')
            False
        """
        if not isinstance(uuid_string, str):
            return False
        
        try:
            uuid.UUID(uuid_string)
            return True
        except (ValueError, TypeError, AttributeError):
            return False

    # Pre-compiled regex patterns for validation
    _UUID_PATTERN = re.compile(
        r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$',
        re.IGNORECASE
    )
    _UUID_BRACED_PATTERN = re.compile(
        r'^\{[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\}$',
        re.IGNORECASE
    )
    _UUID_URN_PATTERN = re.compile(
        r'^urn:uuid:[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$',
        re.IGNORECASE
    )
    _UUID_NO_HYPHEN_PATTERN = re.compile(
        r'^[0-9a-f]{32}$',
        re.IGNORECASE
    )

    @staticmethod
    def is_valid_fast(uuid_string: str) -> bool:
        """
        Fast UUID validation using regex (doesn't verify version/variant).
        
        Much faster than is_valid() for bulk validation, but less thorough.

        Args:
            uuid_string: The string to validate

        Returns:
            True if matches UUID format, False otherwise

        Example:
            >>> UUIDUtils.is_valid_fast('123e4567-e89b-12d3-a456-426614174000')
            True
        """
        if not isinstance(uuid_string, str):
            return False
        
        return (
            UUIDUtils._UUID_PATTERN.match(uuid_string) is not None or
            UUIDUtils._UUID_BRACED_PATTERN.match(uuid_string) is not None or
            UUIDUtils._UUID_URN_PATTERN.match(uuid_string) is not None or
            UUIDUtils._UUID_NO_HYPHEN_PATTERN.match(uuid_string) is not None
        )

    @staticmethod
    def get_version(uuid_obj: Union[uuid.UUID, str]) -> Optional[int]:
        """
        Get the version of a UUID.

        Args:
            uuid_obj: UUID object or string

        Returns:
            Version number (1-5) or None if not versioned

        Example:
            >>> u = UUIDUtils.generate_v4()
            >>> UUIDUtils.get_version(u)
            4
        """
        if isinstance(uuid_obj, str):
            uuid_obj = uuid.UUID(uuid_obj)
        return uuid_obj.version

    @staticmethod
    def get_variant(uuid_obj: Union[uuid.UUID, str]) -> Optional[str]:
        """
        Get the variant of a UUID.

        Args:
            uuid_obj: UUID object or string

        Returns:
            Variant string or None

        Example:
            >>> u = UUIDUtils.generate_v4()
            >>> UUIDUtils.get_variant(u)
            'RFC 4122'
        """
        if isinstance(uuid_obj, str):
            uuid_obj = uuid.UUID(uuid_obj)
        
        variant_map = {
            uuid.RFC_4122: 'RFC 4122',
            uuid.RESERVED_NCS: 'Reserved for NCS compatibility',
            uuid.RESERVED_MICROSOFT: 'Reserved for Microsoft compatibility',
            uuid.RESERVED_FUTURE: 'Reserved for future definition',
        }
        return variant_map.get(uuid_obj.variant)

    @staticmethod
    def to_string(uuid_obj: uuid.UUID, format: str = 'standard') -> str:
        """
        Convert UUID to string in various formats.

        Args:
            uuid_obj: UUID object
            format: Output format ('standard', 'braced', 'urn', 'no-hyphen', 'upper')

        Returns:
            Formatted UUID string

        Raises:
            ValueError: If format is not recognized

        Example:
            >>> u = uuid.UUID('123e4567-e89b-12d3-a456-426614174000')
            >>> UUIDUtils.to_string(u, 'no-hyphen')
            '123e4567e89b12d3a456426614174000'
        """
        if format == 'standard':
            return str(uuid_obj)
        elif format == 'braced':
            return f'{{{uuid_obj}}}'
        elif format == 'urn':
            return f'urn:uuid:{uuid_obj}'
        elif format == 'no-hyphen':
            return uuid_obj.hex
        elif format == 'upper':
            return str(uuid_obj).upper()
        else:
            raise ValueError(f"Unknown format: {format}. Use 'standard', 'braced', 'urn', 'no-hyphen', or 'upper'.")

    @staticmethod
    def to_bytes(uuid_obj: uuid.UUID) -> bytes:
        """
        Convert UUID to 16-byte string.

        Args:
            uuid_obj: UUID object

        Returns:
            16-byte representation

        Example:
            >>> u = uuid.UUID('123e4567-e89b-12d3-a456-426614174000')
            >>> len(UUIDUtils.to_bytes(u))
            16
        """
        return uuid_obj.bytes

    @staticmethod
    def from_bytes(data: bytes) -> uuid.UUID:
        """
        Create UUID from 16-byte string.

        Args:
            data: 16-byte data

        Returns:
            UUID object

        Raises:
            ValueError: If data is not 16 bytes

        Example:
            >>> data = b'\\x12>e\\x07\\xe8\\x9b\\x12\\xd3\\xa4VFf\\x14\\x17@\\x00'
            >>> UUIDUtils.from_bytes(data)
            UUID('123e4567-e89b-12d3-a456-426614174000')
        """
        return uuid.UUID(bytes=data)

    @staticmethod
    def to_int(uuid_obj: uuid.UUID) -> int:
        """
        Convert UUID to 128-bit integer.

        Args:
            uuid_obj: UUID object

        Returns:
            128-bit integer representation

        Example:
            >>> u = uuid.UUID('123e4567-e89b-12d3-a456-426614174000')
            >>> UUIDUtils.to_int(u)
            24364026093169643450911120739550478336
        """
        return uuid_obj.int

    @staticmethod
    def from_int(value: int) -> uuid.UUID:
        """
        Create UUID from 128-bit integer.

        Args:
            value: 128-bit integer (0 to 2^128-1)

        Returns:
            UUID object

        Raises:
            ValueError: If value is out of range

        Example:
            >>> UUIDUtils.from_int(24364026093169643450911120739550478336)
            UUID('123e4567-e89b-12d3-a456-426614174000')
        """
        return uuid.UUID(int=value)

    @staticmethod
    def compare(uuid1: Union[uuid.UUID, str], uuid2: Union[uuid.UUID, str]) -> int:
        """
        Compare two UUIDs.

        Args:
            uuid1: First UUID
            uuid2: Second UUID

        Returns:
            -1 if uuid1 < uuid2, 0 if equal, 1 if uuid1 > uuid2

        Example:
            >>> u1 = uuid.UUID('123e4567-e89b-12d3-a456-426614174000')
            >>> u2 = uuid.UUID('123e4567-e89b-12d3-a456-426614174001')
            >>> UUIDUtils.compare(u1, u2)
            -1
        """
        if isinstance(uuid1, str):
            uuid1 = uuid.UUID(uuid1)
        if isinstance(uuid2, str):
            uuid2 = uuid.UUID(uuid2)
        
        if uuid1 < uuid2:
            return -1
        elif uuid1 > uuid2:
            return 1
        else:
            return 0

    @staticmethod
    def equal(uuid1: Union[uuid.UUID, str], uuid2: Union[uuid.UUID, str]) -> bool:
        """
        Check if two UUIDs are equal.

        Args:
            uuid1: First UUID
            uuid2: Second UUID

        Returns:
            True if equal, False otherwise

        Example:
            >>> u1 = uuid.UUID('123e4567-e89b-12d3-a456-426614174000')
            >>> UUIDUtils.equal(u1, '123e4567-e89b-12d3-a456-426614174000')
            True
        """
        if isinstance(uuid1, str):
            uuid1 = uuid.UUID(uuid1)
        if isinstance(uuid2, str):
            uuid2 = uuid.UUID(uuid2)
        
        return uuid1 == uuid2

    @staticmethod
    def sort(uuid_list: List[Union[uuid.UUID, str]], reverse: bool = False) -> List[uuid.UUID]:
        """
        Sort a list of UUIDs.

        Args:
            uuid_list: List of UUID objects or strings
            reverse: Sort in descending order if True

        Returns:
            Sorted list of UUID objects

        Example:
            >>> uuids = [
            ...     '123e4567-e89b-12d3-a456-426614174002',
            ...     '123e4567-e89b-12d3-a456-426614174000',
            ...     '123e4567-e89b-12d3-a456-426614174001'
            ... ]
            >>> sorted_uuids = UUIDUtils.sort(uuids)
            >>> str(sorted_uuids[0])
            '123e4567-e89b-12d3-a456-426614174000'
        """
        uuid_objects = [
            u if isinstance(u, uuid.UUID) else uuid.UUID(u)
            for u in uuid_list
        ]
        return sorted(uuid_objects, reverse=reverse)

    @staticmethod
    def get_timestamp(uuid_obj: Union[uuid.UUID, str]) -> Optional[datetime]:
        """
        Extract timestamp from a UUID v1.
        
        Only works with version 1 (time-based) UUIDs.

        Args:
            uuid_obj: UUID object or string

        Returns:
            datetime object or None if not a v1 UUID

        Example:
            >>> u = UUIDUtils.generate_v1()
            >>> ts = UUIDUtils.get_timestamp(u)
            >>> isinstance(ts, datetime)
            True
        """
        if isinstance(uuid_obj, str):
            uuid_obj = uuid.UUID(uuid_obj)
        
        if uuid_obj.version != 1:
            return None
        
        # UUID v1 timestamp is in 100-nanosecond intervals since October 15, 1582
        timestamp = uuid_obj.time
        # Convert to seconds since epoch
        # Epoch offset: 12219292800 seconds (between 1582-10-15 and 1970-01-01)
        epoch_offset = 12219292800
        seconds = (timestamp / 10000000) - epoch_offset
        return datetime.fromtimestamp(seconds)

    @staticmethod
    def get_node(uuid_obj: Union[uuid.UUID, str]) -> Optional[int]:
        """
        Extract node (MAC address) from a UUID v1.
        
        Only works with version 1 (time-based) UUIDs.

        Args:
            uuid_obj: UUID object or string

        Returns:
            Node ID as integer or None if not a v1 UUID

        Example:
            >>> u = UUIDUtils.generate_v1()
            >>> node = UUIDUtils.get_node(u)
            >>> isinstance(node, int)
            True
        """
        if isinstance(uuid_obj, str):
            uuid_obj = uuid.UUID(uuid_obj)
        
        if uuid_obj.version != 1:
            return None
        
        return uuid_obj.node

    @staticmethod
    def generate_batch(count: int, version: int = 4) -> List[uuid.UUID]:
        """
        Generate a batch of UUIDs.

        Args:
            count: Number of UUIDs to generate
            version: UUID version (1, 3, 4, or 5)

        Returns:
            List of UUID objects

        Raises:
            ValueError: If version is not supported for batch generation

        Example:
            >>> uuids = UUIDUtils.generate_batch(5, version=4)
            >>> len(uuids)
            5
        """
        if version == 1:
            return [uuid.uuid1() for _ in range(count)]
        elif version == 4:
            return [uuid.uuid4() for _ in range(count)]
        elif version in (3, 5):
            raise ValueError(f"Batch generation not supported for version {version}. Use generate_v3/v5 with specific namespace and name.")
        else:
            raise ValueError(f"Unsupported UUID version: {version}. Use 1, 3, 4, or 5.")

    @staticmethod
    def nil() -> uuid.UUID:
        """
        Get the nil UUID (all zeros).

        Returns:
            Nil UUID (00000000-0000-0000-0000-000000000000)

        Example:
            >>> UUIDUtils.nil()
            UUID('00000000-0000-0000-0000-000000000000')
        """
        return uuid.UUID(int=0)

    @staticmethod
    def is_nil(uuid_obj: Union[uuid.UUID, str]) -> bool:
        """
        Check if a UUID is the nil UUID.

        Args:
            uuid_obj: UUID object or string

        Returns:
            True if nil UUID, False otherwise

        Example:
            >>> UUIDUtils.is_nil('00000000-0000-0000-0000-000000000000')
            True
        """
        if isinstance(uuid_obj, str):
            uuid_obj = uuid.UUID(uuid_obj)
        
        return uuid_obj.int == 0

    @staticmethod
    def hash_to_uuid(data: Union[str, bytes], algorithm: str = 'sha256') -> uuid.UUID:
        """
        Generate a UUID from hashed data (custom deterministic UUID).
        
        Uses SHA-256 (or specified algorithm) to create a deterministic UUID
        from any input data. The resulting UUID follows RFC 4122 variant.

        Args:
            data: Input data to hash
            algorithm: Hash algorithm ('md5', 'sha1', 'sha256', 'sha512')

        Returns:
            UUID object derived from hash

        Raises:
            ValueError: If algorithm is not supported

        Example:
            >>> u = UUIDUtils.hash_to_uuid('my-custom-seed')
            >>> isinstance(u, uuid.UUID)
            True
        """
        if isinstance(data, str):
            data = data.encode('utf-8')
        
        if algorithm == 'md5':
            hash_obj = hashlib.md5(data)
        elif algorithm == 'sha1':
            hash_obj = hashlib.sha1(data)
        elif algorithm == 'sha256':
            hash_obj = hashlib.sha256(data)
        elif algorithm == 'sha512':
            hash_obj = hashlib.sha512(data)
        else:
            raise ValueError(f"Unsupported algorithm: {algorithm}. Use 'md5', 'sha1', 'sha256', or 'sha512'.")
        
        # Use first 16 bytes of hash
        hash_bytes = hash_obj.digest()[:16]
        
        # Set version (use 5 for SHA-based) and variant bits
        hash_list = bytearray(hash_bytes)
        hash_list[6] = (hash_list[6] & 0x0f) | 0x50  # Version 5
        hash_list[8] = (hash_list[8] & 0x3f) | 0x80  # RFC 4122 variant
        
        return uuid.UUID(bytes=bytes(hash_list))


# Convenience functions for direct import

def generate_v1() -> uuid.UUID:
    """Generate a UUID version 1 (time-based)."""
    return UUIDUtils.generate_v1()


def generate_v3(namespace: Union[uuid.UUID, str], name: str) -> uuid.UUID:
    """Generate a UUID version 3 (MD5 namespace-based)."""
    return UUIDUtils.generate_v3(namespace, name)


def generate_v4() -> uuid.UUID:
    """Generate a UUID version 4 (random)."""
    return UUIDUtils.generate_v4()


def generate_v5(namespace: Union[uuid.UUID, str], name: str) -> uuid.UUID:
    """Generate a UUID version 5 (SHA-1 namespace-based)."""
    return UUIDUtils.generate_v5(namespace, name)


def parse(uuid_string: str) -> uuid.UUID:
    """Parse a UUID string into a UUID object."""
    return UUIDUtils.parse(uuid_string)


def is_valid(uuid_string: str) -> bool:
    """Check if a string is a valid UUID."""
    return UUIDUtils.is_valid(uuid_string)


def is_valid_fast(uuid_string: str) -> bool:
    """Fast UUID validation using regex."""
    return UUIDUtils.is_valid_fast(uuid_string)


def get_version(uuid_obj: Union[uuid.UUID, str]) -> Optional[int]:
    """Get the version of a UUID."""
    return UUIDUtils.get_version(uuid_obj)


def get_variant(uuid_obj: Union[uuid.UUID, str]) -> Optional[str]:
    """Get the variant of a UUID."""
    return UUIDUtils.get_variant(uuid_obj)


def to_string(uuid_obj: uuid.UUID, format: str = 'standard') -> str:
    """Convert UUID to string in various formats."""
    return UUIDUtils.to_string(uuid_obj, format)


def to_bytes(uuid_obj: uuid.UUID) -> bytes:
    """Convert UUID to 16-byte string."""
    return UUIDUtils.to_bytes(uuid_obj)


def from_bytes(data: bytes) -> uuid.UUID:
    """Create UUID from 16-byte string."""
    return UUIDUtils.from_bytes(data)


def to_int(uuid_obj: uuid.UUID) -> int:
    """Convert UUID to 128-bit integer."""
    return UUIDUtils.to_int(uuid_obj)


def from_int(value: int) -> uuid.UUID:
    """Create UUID from 128-bit integer."""
    return UUIDUtils.from_int(value)


def compare(uuid1: Union[uuid.UUID, str], uuid2: Union[uuid.UUID, str]) -> int:
    """Compare two UUIDs."""
    return UUIDUtils.compare(uuid1, uuid2)


def equal(uuid1: Union[uuid.UUID, str], uuid2: Union[uuid.UUID, str]) -> bool:
    """Check if two UUIDs are equal."""
    return UUIDUtils.equal(uuid1, uuid2)


def sort(uuid_list: List[Union[uuid.UUID, str]], reverse: bool = False) -> List[uuid.UUID]:
    """Sort a list of UUIDs."""
    return UUIDUtils.sort(uuid_list, reverse)


def get_timestamp(uuid_obj: Union[uuid.UUID, str]) -> Optional[datetime]:
    """Extract timestamp from a UUID v1."""
    return UUIDUtils.get_timestamp(uuid_obj)


def get_node(uuid_obj: Union[uuid.UUID, str]) -> Optional[int]:
    """Extract node (MAC address) from a UUID v1."""
    return UUIDUtils.get_node(uuid_obj)


def generate_batch(count: int, version: int = 4) -> List[uuid.UUID]:
    """Generate a batch of UUIDs."""
    return UUIDUtils.generate_batch(count, version)


def nil() -> uuid.UUID:
    """Get the nil UUID (all zeros)."""
    return UUIDUtils.nil()


def is_nil(uuid_obj: Union[uuid.UUID, str]) -> bool:
    """Check if a UUID is the nil UUID."""
    return UUIDUtils.is_nil(uuid_obj)


def hash_to_uuid(data: Union[str, bytes], algorithm: str = 'sha256') -> uuid.UUID:
    """Generate a UUID from hashed data."""
    return UUIDUtils.hash_to_uuid(data, algorithm)
