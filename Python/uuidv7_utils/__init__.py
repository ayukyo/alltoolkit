"""
UUIDv7 Utils - Time-Ordered UUID Generation

UUIDv7 is defined in RFC 9562 as a time-ordered UUID format.
Ideal for database primary keys, distributed systems, and time-based queries.

Quick start:
    from uuidv7_utils import generate
    
    uuid = generate()
    print(uuid)  # 018f3b6a-1b2c-7d3e-8f4a-5b6c7d8e9f0a

Features:
- Zero external dependencies
- Thread-safe generation
- Monotonically increasing IDs
- Timestamp extraction
- Time-based filtering
"""

from uuidv7_utils.mod import (
    # Core classes
    UUIDv7,
    UUIDv7Generator,
    UUIDv7Validator,
    UUIDv7Set,
    UUIDv7Range,
    
    # Enums and dataclasses
    UUIDv7Strategy,
    UUIDv7Components,
    
    # Convenience functions
    generate,
    generate_monotonic,
    generate_batch,
    parse,
    is_uuidv7,
    from_timestamp,
    from_datetime,
)

__version__ = "1.0.0"
__all__ = [
    'UUIDv7',
    'UUIDv7Generator',
    'UUIDv7Validator',
    'UUIDv7Set',
    'UUIDv7Range',
    'UUIDv7Strategy',
    'UUIDv7Components',
    'generate',
    'generate_monotonic',
    'generate_batch',
    'parse',
    'is_uuidv7',
    'from_timestamp',
    'from_datetime',
]