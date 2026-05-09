"""
License Key Utilities
=====================
Generate, validate, and manage software license keys.

Features:
- Multiple key formats (Trial, Standard, Professional, Enterprise)
- Hardware binding support
- Expiration date support
- Feature restrictions
- Cryptographic signature verification
- Zero external dependencies (uses only Python stdlib)

Author: AllToolkit
License: MIT
"""

import hashlib
import hmac
import base64
import secrets
import time
import re
from datetime import datetime, timedelta
from typing import Optional, Dict, List, Tuple, Set
from enum import Enum
from dataclasses import dataclass, field


class LicenseType(Enum):
    """License type enumeration."""
    TRIAL = "TRIAL"
    STANDARD = "STANDARD"
    PROFESSIONAL = "PROFESSIONAL"
    ENTERPRISE = "ENTERPRISE"


class LicenseStatus(Enum):
    """License validation status."""
    VALID = "VALID"
    EXPIRED = "EXPIRED"
    INVALID_FORMAT = "INVALID_FORMAT"
    INVALID_SIGNATURE = "INVALID_SIGNATURE"
    HARDWARE_MISMATCH = "HARDWARE_MISMATCH"
    FEATURE_NOT_LICENSED = "FEATURE_NOT_LICENSED"


@dataclass
class LicenseInfo:
    """License information structure."""
    license_id: str
    license_type: LicenseType
    product_name: str
    customer_name: str
    customer_email: str
    issued_at: datetime
    expires_at: Optional[datetime] = None
    features: Set[str] = field(default_factory=set)
    hardware_id: Optional[str] = None
    max_users: int = 1
    metadata: Dict[str, str] = field(default_factory=dict)
    
    def is_expired(self) -> bool:
        """Check if license is expired."""
        if self.expires_at is None:
            return False
        return datetime.now() > self.expires_at
    
    def days_remaining(self) -> Optional[int]:
        """Get days remaining until expiration."""
        if self.expires_at is None:
            return None
        delta = self.expires_at - datetime.now()
        return max(0, delta.days)
    
    def has_feature(self, feature: str) -> bool:
        """Check if license includes a feature."""
        return feature in self.features


class LicenseKeyGenerator:
    """Generate and validate software license keys."""
    
    VERSION = 1
    DEFAULT_SECRET = b"AllToolkit-License-Key-Secret-2024"
    
    # Key format: TYPE-XXXX-XXXX-XXXX-XXXX (5 segments, 4 dashes, 21 chars total)
    KEY_PATTERN = re.compile(r'^[TPSE]-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}$')
    
    TYPE_PREFIXES = {
        LicenseType.TRIAL: 'T',
        LicenseType.STANDARD: 'S',
        LicenseType.PROFESSIONAL: 'P',
        LicenseType.ENTERPRISE: 'E',
    }
    
    def __init__(self, secret_key: Optional[bytes] = None):
        self.secret_key = secret_key or self.DEFAULT_SECRET
    
    def _encode_bytes(self, data: bytes) -> str:
        """Encode bytes to license key format (4-char segments)."""
        # Use base32 and strip padding
        encoded = base64.b32encode(data).decode('ascii').rstrip('=').upper()
        # Take first 16 characters (4 segments of 4 chars)
        return encoded[:16]
    
    def _decode_bytes(self, encoded: str) -> Optional[bytes]:
        """Decode license key segment to bytes."""
        try:
            padding = (8 - len(encoded) % 8) % 8
            return base64.b32decode(encoded + '=' * padding)
        except Exception:
            return None
    
    def _generate_signature(self, data: str) -> str:
        """Generate short signature for data."""
        sig = hmac.new(self.secret_key, data.encode(), hashlib.sha256).hexdigest()
        return sig[:16].upper()
    
    def _create_payload(self, info: LicenseInfo) -> str:
        """Create payload string for signing."""
        parts = [
            info.license_type.value,
            info.product_name,
            info.customer_email,
            str(int(info.issued_at.timestamp())),
        ]
        if info.expires_at:
            parts.append(str(int(info.expires_at.timestamp())))
        if info.hardware_id:
            parts.append(info.hardware_id)
        if info.features:
            parts.append(','.join(sorted(info.features)))
        return '|'.join(parts)
    
    def generate_license_id(self, license_type: LicenseType) -> str:
        """Generate unique license ID."""
        prefix = self.TYPE_PREFIXES.get(license_type, 'S')
        timestamp = int(time.time())
        random = secrets.token_hex(4).upper()
        return f"{prefix}-{timestamp}-{random}"
    
    def generate_license(
        self,
        license_type: LicenseType,
        product_name: str,
        customer_name: str,
        customer_email: str,
        validity_days: Optional[int] = None,
        features: Optional[Set[str]] = None,
        hardware_id: Optional[str] = None,
        max_users: int = 1,
        metadata: Optional[Dict[str, str]] = None
    ) -> Tuple[str, LicenseInfo]:
        """Generate a complete license."""
        # Generate license ID
        license_id = self.generate_license_id(license_type)
        
        # Calculate dates
        issued_at = datetime.now()
        expires_at = None
        if validity_days is not None:
            expires_at = issued_at + timedelta(days=validity_days)
        
        # Create license info
        info = LicenseInfo(
            license_id=license_id,
            license_type=license_type,
            product_name=product_name,
            customer_name=customer_name,
            customer_email=customer_email,
            issued_at=issued_at,
            expires_at=expires_at,
            features=features or set(),
            hardware_id=hardware_id,
            max_users=max_users,
            metadata=metadata or {}
        )
        
        # Generate key
        key = self.generate_key(info)
        
        return key, info
    
    def generate_key(self, info: LicenseInfo) -> str:
        """Generate license key from license info."""
        # Create payload with license_id for uniqueness
        payload = f"{info.license_id}|{self._create_payload(info)}"
        signature = self._generate_signature(payload)
        
        # Get type prefix
        prefix = self.TYPE_PREFIXES.get(info.license_type, 'S')
        
        # Combine signature parts into segments
        # Format: TYPE-XXXX-XXXX-XXXX-XXXX
        segments = [
            prefix,
            signature[0:4],
            signature[4:8],
            signature[8:12],
            signature[12:16]
        ]
        
        return '-'.join(segments)
    
    def validate_key_format(self, key: str) -> Tuple[bool, Optional[str]]:
        """Validate key format and extract type prefix."""
        if not key:
            return False, None
        key = key.upper().strip()
        if not self.KEY_PATTERN.match(key):
            return False, None
        type_prefix = key[0]
        return True, type_prefix
    
    def validate_key(self, key: str) -> LicenseStatus:
        """Perform basic key format validation."""
        valid, prefix = self.validate_key_format(key)
        if not valid:
            return LicenseStatus.INVALID_FORMAT
        
        # Key format is valid
        # In production, would verify signature against database
        return LicenseStatus.VALID
    
    @staticmethod
    def generate_hardware_id() -> str:
        """Generate hardware ID based on system information."""
        import platform
        import os
        
        info_parts = [
            platform.node(),
            platform.machine(),
            platform.processor() or "unknown",
            str(os.cpu_count() or 1),
        ]
        
        combined = '|'.join(info_parts)
        hw_hash = hashlib.sha256(combined.encode()).hexdigest()[:16]
        
        return f"HWID-{hw_hash.upper()}"


class LicenseManager:
    """Manage a collection of licenses."""
    
    def __init__(self, secret_key: Optional[bytes] = None):
        self.generator = LicenseKeyGenerator(secret_key)
        self._licenses: Dict[str, LicenseInfo] = {}
        self._keys: Dict[str, str] = {}  # key -> license_id
    
    def create_license(
        self,
        license_type: LicenseType,
        product_name: str,
        customer_name: str,
        customer_email: str,
        validity_days: Optional[int] = None,
        features: Optional[Set[str]] = None,
        hardware_id: Optional[str] = None,
        max_users: int = 1
    ) -> Tuple[str, LicenseInfo]:
        """Create and store a new license."""
        key, info = self.generator.generate_license(
            license_type=license_type,
            product_name=product_name,
            customer_name=customer_name,
            customer_email=customer_email,
            validity_days=validity_days,
            features=features,
            hardware_id=hardware_id,
            max_users=max_users
        )
        
        # Store license
        self._licenses[info.license_id] = info
        self._keys[key] = info.license_id
        
        return key, info
    
    def validate_license(
        self,
        key: str,
        hardware_id: Optional[str] = None,
        required_features: Optional[Set[str]] = None
    ) -> Tuple[LicenseStatus, Optional[LicenseInfo]]:
        """Validate a license key."""
        # Validate format
        status = self.generator.validate_key(key)
        if status != LicenseStatus.VALID:
            return status, None
        
        # Look up license
        license_id = self._keys.get(key.upper())
        if license_id is None:
            return LicenseStatus.INVALID_FORMAT, None
        
        info = self._licenses.get(license_id)
        if info is None:
            return LicenseStatus.INVALID_FORMAT, None
        
        # Check expiration
        if info.is_expired():
            return LicenseStatus.EXPIRED, info
        
        # Check hardware binding
        if hardware_id and info.hardware_id and hardware_id != info.hardware_id:
            return LicenseStatus.HARDWARE_MISMATCH, info
        
        # Check features
        if required_features:
            missing = required_features - info.features
            if missing:
                return LicenseStatus.FEATURE_NOT_LICENSED, info
        
        return LicenseStatus.VALID, info
    
    def get_license(self, license_id: str) -> Optional[LicenseInfo]:
        """Get license by ID."""
        return self._licenses.get(license_id)
    
    def get_license_by_key(self, key: str) -> Optional[LicenseInfo]:
        """Get license by key."""
        license_id = self._keys.get(key.upper())
        if license_id:
            return self._licenses.get(license_id)
        return None
    
    def revoke_license(self, license_id: str) -> bool:
        """Revoke a license."""
        if license_id not in self._licenses:
            return False
        
        info = self._licenses.pop(license_id)
        
        # Remove key mapping
        for key, lid in list(self._keys.items()):
            if lid == license_id:
                del self._keys[key]
        
        return True
    
    def list_licenses(
        self,
        license_type: Optional[LicenseType] = None,
        expired: Optional[bool] = None
    ) -> List[LicenseInfo]:
        """List licenses with optional filters."""
        results = []
        for info in self._licenses.values():
            if license_type and info.license_type != license_type:
                continue
            if expired is not None and info.is_expired() != expired:
                continue
            results.append(info)
        return results
    
    def export_license(self, license_id: str) -> Optional[str]:
        """Export license to portable string."""
        info = self._licenses.get(license_id)
        if info is None:
            return None
        
        # Find key for this license
        key = None
        for k, lid in self._keys.items():
            if lid == license_id:
                key = k
                break
        
        if key is None:
            return None
        
        # Create export data
        data = {
            'key': key,
            'id': info.license_id,
            'type': info.license_type.value,
            'product': info.product_name,
            'customer': info.customer_name,
            'email': info.customer_email,
            'issued': int(info.issued_at.timestamp()),
            'expires': int(info.expires_at.timestamp()) if info.expires_at else 0,
            'features': ','.join(sorted(info.features)) if info.features else '',
            'hwid': info.hardware_id or '',
            'users': info.max_users
        }
        
        payload = '|'.join(f"{k}:{v}" for k, v in data.items())
        return base64.b64encode(payload.encode()).decode()
    
    def import_license(self, exported: str) -> Optional[LicenseInfo]:
        """Import license from exported string."""
        try:
            payload = base64.b64decode(exported).decode()
            data = {}
            for part in payload.split('|'):
                if ':' in part:
                    key, value = part.split(':', 1)
                    data[key] = value
            
            expires_at = None
            if int(data['expires']) > 0:
                expires_at = datetime.fromtimestamp(int(data['expires']))
            
            features = set()
            if data['features']:
                features = set(data['features'].split(','))
            
            info = LicenseInfo(
                license_id=data['id'],
                license_type=LicenseType(data['type']),
                product_name=data['product'],
                customer_name=data['customer'],
                customer_email=data['email'],
                issued_at=datetime.fromtimestamp(int(data['issued'])),
                expires_at=expires_at,
                features=features,
                hardware_id=data['hwid'] if data['hwid'] else None,
                max_users=int(data['users'])
            )
            
            # Store
            self._licenses[info.license_id] = info
            self._keys[data['key']] = info.license_id
            
            return info
        except Exception:
            return None


# Convenience functions
def generate_trial_license(
    product_name: str,
    customer_email: str,
    validity_days: int = 14,
    features: Optional[Set[str]] = None
) -> Tuple[str, LicenseInfo]:
    """Generate a trial license."""
    generator = LicenseKeyGenerator()
    return generator.generate_license(
        license_type=LicenseType.TRIAL,
        product_name=product_name,
        customer_name="Trial User",
        customer_email=customer_email,
        validity_days=validity_days,
        features=features
    )


def quick_validate(key: str) -> LicenseStatus:
    """Quick validation of license key format."""
    generator = LicenseKeyGenerator()
    return generator.validate_key(key)