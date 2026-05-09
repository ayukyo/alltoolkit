"""
TOTP (Time-based One-Time Password) Utilities

A complete implementation of TOTP (RFC 6238) and HOTP (RFC 4226) algorithms.
Zero external dependencies - uses only Python standard library.

Features:
- Generate TOTP codes (like Google Authenticator)
- Verify TOTP codes with configurable tolerance
- Support multiple hash algorithms (SHA1, SHA256, SHA512)
- Generate QR code URL for easy setup
- Secret key generation and validation
- Counter-based HOTP support
"""

import hmac
import hashlib
import struct
import base64
import time
import secrets
import urllib.parse
from typing import Optional, Tuple, List


class TOTPUtils:
    """TOTP (Time-based One-Time Password) utility class"""
    
    DEFAULT_DIGITS = 6
    DEFAULT_INTERVAL = 30  # seconds
    DEFAULT_ALGORITHM = 'sha1'
    
    def __init__(
        self,
        secret: str,
        digits: int = DEFAULT_DIGITS,
        interval: int = DEFAULT_INTERVAL,
        algorithm: str = DEFAULT_ALGORITHM
    ):
        """
        Initialize TOTP generator.
        
        Args:
            secret: Base32 encoded secret key
            digits: Number of digits in the code (6 or 8)
            interval: Time interval in seconds (default 30)
            algorithm: Hash algorithm ('sha1', 'sha256', 'sha512')
        """
        self.secret = secret.upper().replace(' ', '').replace('-', '')
        self.digits = digits
        self.interval = interval
        self.algorithm = algorithm.lower()
        
        if self.digits not in (6, 8):
            raise ValueError("Digits must be 6 or 8")
        
        if self.algorithm not in ('sha1', 'sha256', 'sha512'):
            raise ValueError("Algorithm must be 'sha1', 'sha256', or 'sha512'")
        
        # Decode base32 secret
        try:
            self._key = base64.b32decode(self.secret)
        except Exception as e:
            raise ValueError(f"Invalid base32 secret: {e}")
    
    def _get_counter(self, timestamp: Optional[int] = None) -> int:
        """Get time-based counter value."""
        if timestamp is None:
            timestamp = int(time.time())
        return timestamp // self.interval
    
    def _generate_hotp(self, counter: int) -> int:
        """Generate HOTP code for a given counter."""
        # Convert counter to bytes (big-endian, 8 bytes)
        counter_bytes = struct.pack('>Q', counter)
        
        # HMAC hash
        hash_func = getattr(hashlib, self.algorithm)
        hmac_result = hmac.new(self._key, counter_bytes, hash_func).digest()
        
        # Dynamic truncation
        offset = hmac_result[-1] & 0x0F
        code = struct.unpack('>I', hmac_result[offset:offset + 4])[0]
        code = code & 0x7FFFFFFF  # Remove sign bit
        
        # Get last N digits
        return code % (10 ** self.digits)
    
    def generate(self, timestamp: Optional[int] = None) -> str:
        """
        Generate TOTP code.
        
        Args:
            timestamp: Unix timestamp (default: current time)
            
        Returns:
            TOTP code as string with leading zeros
        """
        counter = self._get_counter(timestamp)
        code = self._generate_hotp(counter)
        return str(code).zfill(self.digits)
    
    def verify(
        self,
        code: str,
        timestamp: Optional[int] = None,
        tolerance: int = 1
    ) -> bool:
        """
        Verify a TOTP code.
        
        Args:
            code: The code to verify
            timestamp: Unix timestamp (default: current time)
            tolerance: Number of intervals before/after to accept (default 1)
            
        Returns:
            True if code is valid
        """
        code = code.strip()
        if len(code) != self.digits or not code.isdigit():
            return False
        
        counter = self._get_counter(timestamp)
        
        # Check current and adjacent intervals
        for i in range(-tolerance, tolerance + 1):
            expected = self._generate_hotp(counter + i)
            if str(expected).zfill(self.digits) == code:
                return True
        
        return False
    
    def get_remaining_seconds(self, timestamp: Optional[int] = None) -> int:
        """Get seconds remaining until next code."""
        if timestamp is None:
            timestamp = int(time.time())
        return self.interval - (timestamp % self.interval)
    
    def get_otpauth_url(
        self,
        issuer: str,
        account: str,
        issuer_in_label: bool = True
    ) -> str:
        """
        Generate otpauth:// URL for QR code generation.
        
        Args:
            issuer: Service name (e.g., "MyApp")
            account: User account (e.g., "user@example.com")
            issuer_in_label: Include issuer in label (recommended)
            
        Returns:
            otpauth:// URL
        """
        label = f"{issuer}:{account}" if issuer_in_label else account
        
        params = {
            'secret': self.secret,
            'issuer': issuer,
            'algorithm': self.algorithm.upper(),
            'digits': self.digits,
            'period': self.interval
        }
        
        return f"otpauth://totp/{urllib.parse.quote(label)}?{urllib.parse.urlencode(params)}"
    
    def get_qr_code_url(
        self,
        issuer: str,
        account: str,
        qr_service: str = 'google'
    ) -> str:
        """
        Generate URL for QR code image.
        
        Args:
            issuer: Service name
            account: User account
            qr_service: QR code service ('google', 'qrserver', 'goqr')
            
        Returns:
            URL to QR code image
        """
        otpauth_url = self.get_otpauth_url(issuer, account)
        
        if qr_service == 'google':
            return f"https://chart.googleapis.com/chart?chs=200x200&cht=qr&chl={urllib.parse.quote(otpauth_url)}"
        elif qr_service == 'qrserver':
            return f"https://api.qrserver.com/v1/create-qr-code/?size=200x200&data={urllib.parse.quote(otpauth_url)}"
        elif qr_service == 'goqr':
            return f"https://api.qrserver.com/v1/create-qr-code/?size=200x200&data={urllib.parse.quote(otpauth_url)}"
        else:
            raise ValueError(f"Unknown QR service: {qr_service}")


class HOTPUtils:
    """HOTP (HMAC-based One-Time Password) utility class"""
    
    DEFAULT_DIGITS = 6
    DEFAULT_ALGORITHM = 'sha1'
    
    def __init__(
        self,
        secret: str,
        digits: int = DEFAULT_DIGITS,
        algorithm: str = DEFAULT_ALGORITHM
    ):
        """
        Initialize HOTP generator.
        
        Args:
            secret: Base32 encoded secret key
            digits: Number of digits in the code (6 or 8)
            algorithm: Hash algorithm ('sha1', 'sha256', 'sha512')
        """
        self.secret = secret.upper().replace(' ', '').replace('-', '')
        self.digits = digits
        self.algorithm = algorithm.lower()
        
        if self.digits not in (6, 8):
            raise ValueError("Digits must be 6 or 8")
        
        if self.algorithm not in ('sha1', 'sha256', 'sha512'):
            raise ValueError("Algorithm must be 'sha1', 'sha256', or 'sha512'")
        
        try:
            self._key = base64.b32decode(self.secret)
        except Exception as e:
            raise ValueError(f"Invalid base32 secret: {e}")
    
    def generate(self, counter: int) -> str:
        """
        Generate HOTP code for a given counter.
        
        Args:
            counter: Counter value
            
        Returns:
            HOTP code as string with leading zeros
        """
        counter_bytes = struct.pack('>Q', counter)
        hash_func = getattr(hashlib, self.algorithm)
        hmac_result = hmac.new(self._key, counter_bytes, hash_func).digest()
        
        offset = hmac_result[-1] & 0x0F
        code = struct.unpack('>I', hmac_result[offset:offset + 4])[0]
        code = code & 0x7FFFFFFF
        
        return str(code % (10 ** self.digits)).zfill(self.digits)
    
    def verify(self, code: str, counter: int) -> bool:
        """
        Verify an HOTP code.
        
        Args:
            code: The code to verify
            counter: Expected counter value
            
        Returns:
            True if code is valid
        """
        expected = self.generate(counter)
        return secrets.compare_digest(expected, code.strip())


# Utility functions

def generate_secret(length: int = 20) -> str:
    """
    Generate a random base32 secret key.
    
    Args:
        length: Number of random bytes (20 = 160 bits, recommended)
        
    Returns:
        Base32 encoded secret string
    """
    random_bytes = secrets.token_bytes(length)
    return base64.b32encode(random_bytes).decode('utf-8').rstrip('=')


def is_valid_secret(secret: str) -> bool:
    """
    Check if a secret is a valid base32 string.
    
    Args:
        secret: Secret string to validate
        
    Returns:
        True if valid
    """
    try:
        if not secret or not secret.strip():
            return False
        secret = secret.upper().replace(' ', '').replace('-', '')
        if not secret:
            return False
        # Remove existing padding and add correct padding
        secret = secret.rstrip('=')
        padding = (8 - len(secret) % 8) % 8
        secret = secret + '=' * padding
        base64.b32decode(secret)
        return True
    except Exception:
        return False


def generate_totp(
    secret: str,
    digits: int = 6,
    interval: int = 30,
    algorithm: str = 'sha1',
    timestamp: Optional[int] = None
) -> str:
    """
    Convenience function to generate TOTP code.
    
    Args:
        secret: Base32 encoded secret key
        digits: Number of digits (6 or 8)
        interval: Time interval in seconds
        algorithm: Hash algorithm
        timestamp: Unix timestamp (default: current time)
        
    Returns:
        TOTP code
    """
    totp = TOTPUtils(secret, digits, interval, algorithm)
    return totp.generate(timestamp)


def verify_totp(
    code: str,
    secret: str,
    digits: int = 6,
    interval: int = 30,
    algorithm: str = 'sha1',
    timestamp: Optional[int] = None,
    tolerance: int = 1
) -> bool:
    """
    Convenience function to verify TOTP code.
    
    Args:
        code: Code to verify
        secret: Base32 encoded secret key
        digits: Number of digits (6 or 8)
        interval: Time interval in seconds
        algorithm: Hash algorithm
        timestamp: Unix timestamp (default: current time)
        tolerance: Number of intervals to accept before/after
        
    Returns:
        True if valid
    """
    totp = TOTPUtils(secret, digits, interval, algorithm)
    return totp.verify(code, timestamp, tolerance)


def generate_hotp(
    secret: str,
    counter: int,
    digits: int = 6,
    algorithm: str = 'sha1'
) -> str:
    """
    Convenience function to generate HOTP code.
    
    Args:
        secret: Base32 encoded secret key
        counter: Counter value
        digits: Number of digits (6 or 8)
        algorithm: Hash algorithm
        
    Returns:
        HOTP code
    """
    hotp = HOTPUtils(secret, digits, algorithm)
    return hotp.generate(counter)


def generate_backup_codes(count: int = 10, length: int = 8) -> List[str]:
    """
    Generate backup/recovery codes.
    
    Args:
        count: Number of codes to generate
        length: Length of each code
        
    Returns:
        List of backup codes
    """
    codes = []
    for _ in range(count):
        code = secrets.token_hex(length // 2 + 1)[:length].upper()
        formatted = '-'.join([code[i:i+4] for i in range(0, len(code), 4)])
        codes.append(formatted)
    return codes


class TOTPManager:
    """
    High-level TOTP management for multi-account scenarios.
    """
    
    def __init__(self):
        self._accounts = {}
    
    def add_account(
        self,
        name: str,
        secret: str,
        issuer: str = '',
        digits: int = 6,
        interval: int = 30,
        algorithm: str = 'sha1'
    ) -> None:
        """Add a TOTP account."""
        self._accounts[name] = {
            'totp': TOTPUtils(secret, digits, interval, algorithm),
            'secret': secret,
            'issuer': issuer,
            'digits': digits,
            'interval': interval,
            'algorithm': algorithm
        }
    
    def remove_account(self, name: str) -> bool:
        """Remove a TOTP account."""
        if name in self._accounts:
            del self._accounts[name]
            return True
        return False
    
    def get_code(self, name: str, timestamp: Optional[int] = None) -> Optional[Tuple[str, int]]:
        """
        Get current TOTP code for an account.
        
        Returns:
            Tuple of (code, remaining_seconds) or None if account not found
        """
        if name not in self._accounts:
            return None
        
        account = self._accounts[name]
        totp = account['totp']
        code = totp.generate(timestamp)
        remaining = totp.get_remaining_seconds(timestamp)
        return (code, remaining)
    
    def get_all_codes(self, timestamp: Optional[int] = None) -> dict:
        """Get current codes for all accounts."""
        result = {}
        for name, account in self._accounts.items():
            totp = account['totp']
            code = totp.generate(timestamp)
            remaining = totp.get_remaining_seconds(timestamp)
            result[name] = {
                'code': code,
                'remaining': remaining,
                'issuer': account['issuer']
            }
        return result
    
    def list_accounts(self) -> List[str]:
        """List all account names."""
        return list(self._accounts.keys())


if __name__ == '__main__':
    # Demo
    print("=" * 50)
    print("TOTP Utils Demo")
    print("=" * 50)
    
    # Generate a secret
    secret = generate_secret(20)
    print(f"\nGenerated Secret: {secret}")
    
    # Create TOTP instance
    totp = TOTPUtils(secret)
    
    # Generate code
    code = totp.generate()
    print(f"Current TOTP: {code}")
    print(f"Remaining seconds: {totp.get_remaining_seconds()}")
    
    # Verify code
    print(f"Verify '{code}': {totp.verify(code)}")
    
    # Generate otpauth URL
    print(f"\nOTPAuth URL:")
    print(totp.get_otpauth_url("MyApp", "user@example.com"))
    
    # Generate QR code URL
    print(f"\nQR Code URL:")
    print(totp.get_qr_code_url("MyApp", "user@example.com"))
    
    # Demo TOTP Manager
    print("\n" + "=" * 50)
    print("TOTP Manager Demo")
    print("=" * 50)
    
    manager = TOTPManager()
    manager.add_account("GitHub", secret, "GitHub")
    manager.add_account("Google", generate_secret(), "Google")
    
    print("\nAccounts:", manager.list_accounts())
    print("\nAll codes:")
    for name, info in manager.get_all_codes().items():
        print(f"  {name}: {info['code']} ({info['remaining']}s remaining)")
    
    # Demo backup codes
    print("\n" + "=" * 50)
    print("Backup Codes Demo")
    print("=" * 50)
    print("\nBackup codes:")
    for code in generate_backup_codes(5):
        print(f"  {code}")