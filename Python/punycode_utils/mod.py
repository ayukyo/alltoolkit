"""
AllToolkit - Python Punycode Utilities

A zero-dependency module for Punycode and Internationalized Domain Name (IDN) operations.
Provides encoding/decoding between Unicode domain names and ASCII-compatible encoding (ACE).

Punycode is used to represent Unicode domain names in ASCII format for DNS compatibility.
For example: 中国.cn → xn--fiqs8s.cn

Author: AllToolkit
License: MIT
"""

import re
from typing import Optional, List, Tuple, Dict, Any
from dataclasses import dataclass


@dataclass
class IDNResult:
    """Result of IDN encoding/decoding operation."""
    original: str           # Original input string
    encoded: str            # Encoded/decoded result
    is_ascii: bool          # Whether original was ASCII-only
    labels: List[Tuple[str, str]]  # List of (original, encoded) label pairs
    success: bool           # Operation success status
    error: Optional[str]   # Error message if failed


class PunycodeError(Exception):
    """Exception for Punycode/IDN operations."""
    pass


# Constants
ACE_PREFIX = "xn--"
ACE_PREFIX_BYTES = b"xn--"
MAX_LABEL_LENGTH = 63
MAX_DOMAIN_LENGTH = 253


def _is_ascii(s: str) -> bool:
    """Check if string contains only ASCII characters."""
    try:
        s.encode('ascii')
        return True
    except UnicodeEncodeError:
        return False


def _punycode_encode(label: str) -> str:
    """
    Encode a single label to Punycode.
    Uses Python's built-in punycode codec.
    
    Args:
        label: Unicode label to encode
    
    Returns:
        Punycode-encoded string (without xn-- prefix)
    """
    if _is_ascii(label):
        return label
    
    # Use Python's built-in punycode encoding
    encoded = label.encode('punycode').decode('ascii')
    return encoded


def _punycode_decode(label: str) -> str:
    """
    Decode a Punycode label to Unicode.
    Uses Python's built-in punycode codec.
    
    Args:
        label: Punycode-encoded label (without xn-- prefix)
    
    Returns:
        Unicode string
    """
    if not label.startswith('xn--'):
        return label
    
    # Remove xn-- prefix and decode
    punycode_part = label[4:]
    try:
        decoded = punycode_part.encode('ascii').decode('punycode')
        return decoded
    except (UnicodeError, ValueError):
        return label


def encode_domain(domain: str) -> IDNResult:
    """
    Encode an internationalized domain name to ASCII (Punycode).
    
    Converts Unicode domain names to ASCII-compatible encoding (ACE).
    Each label containing non-ASCII characters is prefixed with "xn--".
    
    Args:
        domain: Unicode domain name (e.g., "中国.cn")
    
    Returns:
        IDNResult with encoded domain and metadata
    
    Examples:
        >>> result = encode_domain("中国.cn")
        >>> print(result.encoded)
        xn--fiqs8s.cn
        
        >>> result = encode_domain("münchen.de")
        >>> print(result.encoded)
        xn--mnchen-3ya.de
        
        >>> result = encode_domain("example.com")
        >>> print(result.encoded)
        example.com
    """
    if not domain:
        return IDNResult(
            original=domain,
            encoded="",
            is_ascii=True,
            labels=[],
            success=False,
            error="Empty domain"
        )
    
    # Normalize: lowercase, strip whitespace
    domain = domain.strip().lower()
    
    # Remove trailing dot
    if domain.endswith('.'):
        domain = domain[:-1]
    
    try:
        labels = domain.split('.')
        encoded_labels = []
        label_pairs = []
        
        for label in labels:
            if not label:
                raise PunycodeError("Empty label in domain")
            
            is_label_ascii = _is_ascii(label)
            
            if is_label_ascii:
                encoded_labels.append(label)
                label_pairs.append((label, label))
            else:
                encoded = _punycode_encode(label)
                ace_label = f"{ACE_PREFIX}{encoded}"
                
                # Check length constraint
                if len(ace_label) > MAX_LABEL_LENGTH:
                    raise PunycodeError(
                        f"Label exceeds {MAX_LABEL_LENGTH} characters: {ace_label}"
                    )
                
                encoded_labels.append(ace_label)
                label_pairs.append((label, ace_label))
        
        encoded_domain = '.'.join(encoded_labels)
        
        # Check total domain length
        if len(encoded_domain) > MAX_DOMAIN_LENGTH:
            raise PunycodeError(
                f"Domain exceeds {MAX_DOMAIN_LENGTH} characters"
            )
        
        return IDNResult(
            original=domain,
            encoded=encoded_domain,
            is_ascii=_is_ascii(domain),
            labels=label_pairs,
            success=True,
            error=None
        )
    
    except Exception as e:
        return IDNResult(
            original=domain,
            encoded="",
            is_ascii=_is_ascii(domain),
            labels=[],
            success=False,
            error=str(e)
        )


def decode_domain(domain: str) -> IDNResult:
    """
    Decode a Punycode domain name to Unicode.
    
    Converts ASCII-compatible encoding (ACE) back to Unicode characters.
    Labels starting with "xn--" are decoded.
    
    Args:
        domain: Punycode-encoded domain (e.g., "xn--fiqs8s.cn")
    
    Returns:
        IDNResult with decoded domain and metadata
    
    Examples:
        >>> result = decode_domain("xn--fiqs8s.cn")
        >>> print(result.encoded)
        中国.cn
        
        >>> result = decode_domain("xn--mnchen-3ya.de")
        >>> print(result.encoded)
        münchen.de
    """
    if not domain:
        return IDNResult(
            original=domain,
            encoded="",
            is_ascii=True,
            labels=[],
            success=False,
            error="Empty domain"
        )
    
    domain = domain.strip().lower()
    
    if domain.endswith('.'):
        domain = domain[:-1]
    
    try:
        labels = domain.split('.')
        decoded_labels = []
        label_pairs = []
        
        for label in labels:
            if not label:
                raise PunycodeError("Empty label in domain")
            
            if label.startswith(ACE_PREFIX):
                decoded = _punycode_decode(label)
                decoded_labels.append(decoded)
                label_pairs.append((label, decoded))
            else:
                decoded_labels.append(label)
                label_pairs.append((label, label))
        
        decoded_domain = '.'.join(decoded_labels)
        
        return IDNResult(
            original=domain,
            encoded=decoded_domain,
            is_ascii=not any(l.startswith(ACE_PREFIX) for l in labels),
            labels=label_pairs,
            success=True,
            error=None
        )
    
    except Exception as e:
        return IDNResult(
            original=domain,
            encoded="",
            is_ascii=True,
            labels=[],
            success=False,
            error=str(e)
        )


def encode_email(email: str) -> str:
    """
    Encode an email address with internationalized domain to ASCII.
    
    Only the domain part is encoded; local part is preserved.
    
    Args:
        email: Email address with possible Unicode domain
    
    Returns:
        Email address with ASCII domain
    
    Examples:
        >>> encode_email("test@中国.cn")
        'test@xn--fiqs8s.cn'
        
        >>> encode_email("用户@example.com")
        '用户@example.com'
    """
    if '@' not in email:
        return email
    
    local, domain = email.rsplit('@', 1)
    
    # Encode domain part
    result = encode_domain(domain)
    if result.success:
        return f"{local}@{result.encoded}"
    
    return email


def decode_email(email: str) -> str:
    """
    Decode an email address with Punycode domain to Unicode.
    
    Args:
        email: Email address with Punycode domain
    
    Returns:
        Email address with Unicode domain
    
    Examples:
        >>> decode_email("test@xn--fiqs8s.cn")
        'test@中国.cn'
    """
    if '@' not in email:
        return email
    
    local, domain = email.rsplit('@', 1)
    
    result = decode_domain(domain)
    if result.success:
        return f"{local}@{result.encoded}"
    
    return email


def is_idn(domain: str) -> bool:
    """
    Check if a domain contains non-ASCII characters.
    
    Args:
        domain: Domain name to check
    
    Returns:
        True if domain contains Unicode characters
    
    Examples:
        >>> is_idn("中国.cn")
        True
        >>> is_idn("example.com")
        False
    """
    return not _is_ascii(domain)


def is_punycode(domain: str) -> bool:
    """
    Check if a domain is Punycode-encoded.
    
    Args:
        domain: Domain name to check
    
    Returns:
        True if any label starts with "xn--"
    
    Examples:
        >>> is_punycode("xn--fiqs8s.cn")
        True
        >>> is_punycode("example.com")
        False
    """
    if not domain:
        return False
    
    domain = domain.lower()
    labels = domain.split('.')
    
    return any(label.startswith(ACE_PREFIX) for label in labels)


def validate_domain(domain: str) -> Tuple[bool, Optional[str]]:
    """
    Validate a domain name (supports both Unicode and Punycode).
    
    Checks:
    - Valid label format
    - Label length (max 63 chars)
    - Total domain length (max 253 chars)
    - Valid characters
    
    Args:
        domain: Domain name to validate
    
    Returns:
        Tuple of (is_valid, error_message)
    
    Examples:
        >>> validate_domain("example.com")
        (True, None)
        >>> validate_domain("-invalid.com")
        (False, "Label cannot start or end with hyphen")
    """
    if not domain:
        return False, "Empty domain"
    
    domain = domain.strip().lower()
    
    if domain.endswith('.'):
        domain = domain[:-1]
    
    if len(domain) > MAX_DOMAIN_LENGTH:
        return False, f"Domain exceeds {MAX_DOMAIN_LENGTH} characters"
    
    labels = domain.split('.')
    
    if len(labels) < 2:
        return False, "Domain must have at least two labels"
    
    # Label validation regex
    # Allows letters, digits, hyphens (not at start/end)
    # For Punycode labels, allows xn-- prefix
    label_pattern = re.compile(
        r'^([a-z0-9]([a-z0-9-]*[a-z0-9])?)$'
    )
    
    for label in labels:
        if not label:
            return False, "Empty label in domain"
        
        if len(label) > MAX_LABEL_LENGTH:
            return False, f"Label exceeds {MAX_LABEL_LENGTH} characters: {label}"
        
        # For non-ASCII labels, skip character validation
        if not _is_ascii(label):
            # Basic validation for IDN labels
            if label.startswith('-') or label.endswith('-'):
                return False, "Label cannot start or end with hyphen"
            continue
        
        # For Punycode labels
        if label.startswith(ACE_PREFIX):
            punycode_part = label[4:]
            if not punycode_part:
                return False, "Invalid Punycode label"
            if not re.match(r'^[a-z0-9-]+$', punycode_part):
                return False, f"Invalid Punycode characters in: {label}"
            continue
        
        # Regular ASCII label validation
        if not label_pattern.match(label):
            return False, f"Invalid label format: {label}"
        
        if label.startswith('-') or label.endswith('-'):
            return False, "Label cannot start or end with hyphen"
    
    return True, None


def get_tld(domain: str) -> str:
    """
    Extract the top-level domain (TLD) from a domain name.
    
    Args:
        domain: Domain name (Unicode or Punycode)
    
    Returns:
        Top-level domain
    
    Examples:
        >>> get_tld("example.com")
        'com'
        >>> get_tld("中国.cn")
        'cn'
    """
    if not domain:
        return ""
    
    domain = domain.strip().lower()
    
    if domain.endswith('.'):
        domain = domain[:-1]
    
    labels = domain.split('.')
    
    if len(labels) >= 2:
        return labels[-1]
    
    return ""


def normalize_domain(domain: str, to_ascii: bool = True) -> str:
    """
    Normalize a domain name.
    
    Args:
        domain: Domain name to normalize
        to_ascii: If True, encode to ASCII (Punycode); if False, decode to Unicode
    
    Returns:
        Normalized domain name
    
    Examples:
        >>> normalize_domain("中国.cn", to_ascii=True)
        'xn--fiqs8s.cn'
        >>> normalize_domain("xn--fiqs8s.cn", to_ascii=False)
        '中国.cn'
    """
    if to_ascii:
        result = encode_domain(domain)
        return result.encoded if result.success else domain
    else:
        result = decode_domain(domain)
        return result.encoded if result.success else domain


def batch_encode(domains: List[str]) -> Dict[str, str]:
    """
    Batch encode multiple domain names.
    
    Args:
        domains: List of domain names to encode
    
    Returns:
        Dictionary mapping original domains to encoded versions
    
    Examples:
        >>> batch_encode(["中国.cn", "日本.jp", "example.com"])
        {'中国.cn': 'xn--fiqs8s.cn', '日本.jp': 'xn--wgv71a.jp', 'example.com': 'example.com'}
    """
    results = {}
    for domain in domains:
        result = encode_domain(domain)
        results[domain] = result.encoded if result.success else domain
    return results


def batch_decode(domains: List[str]) -> Dict[str, str]:
    """
    Batch decode multiple Punycode domain names.
    
    Args:
        domains: List of Punycode domain names to decode
    
    Returns:
        Dictionary mapping original domains to decoded versions
    
    Examples:
        >>> batch_decode(["xn--fiqs8s.cn", "xn--wgv71a.jp"])
        {'xn--fiqs8s.cn': '中国.cn', 'xn--wgv71a.jp': '日本.jp'}
    """
    results = {}
    for domain in domains:
        result = decode_domain(domain)
        results[domain] = result.encoded if result.success else domain
    return results


def domain_info(domain: str) -> Dict[str, Any]:
    """
    Get comprehensive information about a domain name.
    
    Args:
        domain: Domain name to analyze
    
    Returns:
        Dictionary with domain information
    
    Examples:
        >>> info = domain_info("中国.cn")
        >>> print(info['unicode'])
        中国.cn
        >>> print(info['ascii'])
        xn--fiqs8s.cn
        >>> print(info['is_idn'])
        True
    """
    # Determine if input is ASCII or Unicode
    is_input_ascii = _is_ascii(domain)
    
    # Get both encodings
    if is_input_ascii:
        if is_punycode(domain):
            ascii_form = domain
            unicode_form = decode_domain(domain).encoded
        else:
            ascii_form = domain
            unicode_form = domain
    else:
        ascii_form = encode_domain(domain).encoded
        unicode_form = domain
    
    is_valid, error = validate_domain(domain)
    
    return {
        'original': domain,
        'unicode': unicode_form,
        'ascii': ascii_form,
        'is_idn': not _is_ascii(unicode_form),
        'is_punycode': is_punycode(ascii_form),
        'is_valid': is_valid,
        'error': error,
        'tld': get_tld(domain),
        'labels': domain.strip().lower().rstrip('.').split('.'),
        'label_count': len(domain.strip().lower().rstrip('.').split('.')),
    }


# Convenience exports
__all__ = [
    # Data classes and exceptions
    'IDNResult',
    'PunycodeError',
    
    # Core functions
    'encode_domain',
    'decode_domain',
    'encode_email',
    'decode_email',
    
    # Validation and detection
    'is_idn',
    'is_punycode',
    'validate_domain',
    
    # Utilities
    'get_tld',
    'normalize_domain',
    
    # Batch operations
    'batch_encode',
    'batch_decode',
    
    # Analysis
    'domain_info',
    
    # Constants
    'ACE_PREFIX',
    'MAX_LABEL_LENGTH',
    'MAX_DOMAIN_LENGTH',
]