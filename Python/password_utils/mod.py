"""
AllToolkit - Python Password Utilities

A zero-dependency, production-ready password utility module.
Supports password generation, strength analysis, validation, and secure hashing.

Author: AllToolkit
License: MIT
"""

import secrets
import string
import hashlib
import re
import base64
import hmac
from typing import List, Dict, Tuple, Optional, Set, Any
from dataclasses import dataclass, field
from enum import Enum
from collections import Counter
import time


# Character sets for password generation
LOWERCASE = string.ascii_lowercase
UPPERCASE = string.ascii_uppercase
DIGITS = string.digits
SPECIAL = "!@#$%^&*()_+-=[]{}|;:,.<>?"
HEX_CHARS = "0123456789abcdef"
BASE64_CHARS = string.ascii_letters + string.digits + "+/"


class StrengthLevel(Enum):
    """Password strength levels."""
    VERY_WEAK = "very_weak"
    WEAK = "weak"
    FAIR = "fair"
    STRONG = "strong"
    VERY_STRONG = "very_strong"


class ValidationError(Enum):
    """Password validation error types."""
    TOO_SHORT = "too_short"
    TOO_LONG = "too_long"
    NO_UPPERCASE = "no_uppercase"
    NO_LOWERCASE = "no_lowercase"
    NO_DIGIT = "no_digit"
    NO_SPECIAL = "no_special"
    COMMON_PASSWORD = "common_password"
    SEQUENTIAL_CHARS = "sequential_chars"
    REPEATED_CHARS = "repeated_chars"
    CONTAINS_USERNAME = "contains_username"
    CONTAINS_EMAIL = "contains_email"
    INVALID_CHARS = "invalid_chars"


@dataclass
class PasswordStrength:
    """Password strength analysis result."""
    level: StrengthLevel
    score: int  # 0-100
    entropy_bits: float
    length: int
    has_lowercase: bool
    has_uppercase: bool
    has_digits: bool
    has_special: bool
    character_diversity: float  # 0-1
    issues: List[str] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "level": self.level.value,
            "score": self.score,
            "entropy_bits": round(self.entropy_bits, 2),
            "length": self.length,
            "has_lowercase": self.has_lowercase,
            "has_uppercase": self.has_uppercase,
            "has_digits": self.has_digits,
            "has_special": self.has_special,
            "character_diversity": round(self.character_diversity, 3),
            "issues": self.issues,
            "suggestions": self.suggestions,
        }


@dataclass
class ValidationResult:
    """Password validation result."""
    is_valid: bool
    errors: List[ValidationError] = field(default_factory=list)
    error_messages: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "is_valid": self.is_valid,
            "errors": [e.value for e in self.errors],
            "error_messages": self.error_messages,
        }


# Common passwords list (top 100 for security checking)
COMMON_PASSWORDS = {
    "password", "123456", "12345678", "qwerty", "abc123", "monkey", "1234567",
    "letmein", "trustno1", "dragon", "baseball", "iloveyou", "master", "sunshine",
    "ashley", "bailey", "shadow", "123123", "654321", "superman", "qazwsx",
    "michael", "football", "password1", "password123", "welcome", "jesus",
    "ninja", "mustang", "password1234", "admin", "admin123", "root", "toor",
    "pass", "test", "guest", "master123", "changeme", "hello", "charlie",
    "donald", "password12", "qwerty123", "aa123456", "login", "princess",
    "starwars", "whatever", "solo", "welcome1", "flower", "hottie", "loveme",
    "zaq1zaq1", "access", "000000", "696969", "batman", "trustno1", "killer",
}

# Sequential patterns to detect
SEQUENTIAL_PATTERNS = [
    "abc", "bcd", "cde", "def", "efg", "fgh", "ghi", "hij", "ijk", "jkl",
    "klm", "lmn", "mno", "nop", "opq", "pqr", "qrs", "rst", "stu", "tuv",
    "uvw", "vwx", "wxy", "xyz",
    "012", "123", "234", "345", "456", "567", "678", "789", "890",
    "qwe", "wer", "ert", "rty", "tyu", "yui", "uio", "iop",
    "asd", "sdf", "dfg", "fgh", "ghj", "hjk", "jkl",
    "zxc", "xcv", "cvb", "vbn", "bnm",
]


class PasswordUtils:
    """
    Comprehensive password utility class.
    
    Features:
    - Secure password generation with customizable rules
    - Password strength analysis with entropy calculation
    - Password validation against security policies
    - Secure hashing with salt
    - Password breach checking (local common password list)
    - Passphrase generation
    """
    
    def __init__(self, min_length: int = 8, max_length: int = 128):
        """
        Initialize password utilities.
        
        Args:
            min_length: Minimum password length for validation
            max_length: Maximum password length for validation
        """
        self.min_length = min_length
        self.max_length = max_length
    
    def generate(
        self,
        length: int = 16,
        use_lowercase: bool = True,
        use_uppercase: bool = True,
        use_digits: bool = True,
        use_special: bool = True,
        exclude_ambiguous: bool = False,
        ensure_all_types: bool = True,
    ) -> str:
        """
        Generate a cryptographically secure random password.
        
        Args:
            length: Password length (default: 16)
            use_lowercase: Include lowercase letters
            use_uppercase: Include uppercase letters
            use_digits: Include digits
            use_special: Include special characters
            exclude_ambiguous: Exclude ambiguous characters (0, O, l, I, 1)
            ensure_all_types: Ensure at least one character from each enabled type
            
        Returns:
            Generated password string
            
        Raises:
            ValueError: If no character types are enabled or length is invalid
        """
        if length < 1:
            raise ValueError("Password length must be at least 1")
        
        if length > self.max_length:
            raise ValueError(f"Password length cannot exceed {self.max_length}")
        
        # Build character pool
        pool = ""
        type_pools = []
        
        if use_lowercase:
            chars = LOWERCASE
            if exclude_ambiguous:
                chars = chars.replace("l", "")
            pool += chars
            type_pools.append(chars)
        
        if use_uppercase:
            chars = UPPERCASE
            if exclude_ambiguous:
                chars = chars.replace("O", "").replace("I", "")
            pool += chars
            type_pools.append(chars)
        
        if use_digits:
            chars = DIGITS
            if exclude_ambiguous:
                chars = chars.replace("0", "").replace("1", "")
            pool += chars
            type_pools.append(chars)
        
        if use_special:
            chars = SPECIAL
            if exclude_ambiguous:
                chars = chars.replace("|", "").replace(";", "")
            pool += chars
            type_pools.append(chars)
        
        if not pool:
            raise ValueError("At least one character type must be enabled")
        
        # Generate password
        if ensure_all_types and len(type_pools) > 1 and length >= len(type_pools):
            # Ensure at least one character from each type
            password_chars = [secrets.choice(pool) for _ in range(length)]
            
            # Replace characters at random positions with required types
            positions = list(range(length))
            secrets.SystemRandom().shuffle(positions)
            
            for i, pool_chars in enumerate(type_pools):
                if i < len(positions):
                    password_chars[positions[i]] = secrets.choice(pool_chars)
            
            # Shuffle final password
            secrets.SystemRandom().shuffle(password_chars)
            return "".join(password_chars)
        else:
            return "".join(secrets.choice(pool) for _ in range(length))
    
    def generate_passphrase(
        self,
        word_count: int = 4,
        separator: str = "-",
        use_capitalization: bool = True,
        add_number: bool = False,
        add_symbol: bool = False,
        word_list: Optional[List[str]] = None,
    ) -> str:
        """
        Generate a memorable passphrase.
        
        Args:
            word_count: Number of words in the passphrase
            separator: Word separator (default: "-")
            use_capitalization: Capitalize first letter of each word
            add_number: Append a random number
            add_symbol: Append a random symbol
            word_list: Custom word list (uses common words if None)
            
        Returns:
            Generated passphrase
        """
        if word_list is None:
            word_list = self._get_common_words()
        
        if word_count < 1:
            raise ValueError("Word count must be at least 1")
        
        if word_count > len(word_list):
            raise ValueError(f"Word count cannot exceed word list size ({len(word_list)})")
        
        # Select random words
        words = secrets.SystemRandom().sample(word_list, word_count)
        
        # Apply capitalization
        if use_capitalization:
            words = [w.capitalize() for w in words]
        
        # Build passphrase
        passphrase = separator.join(words)
        
        # Add number
        if add_number:
            passphrase += str(secrets.randbelow(100))
        
        # Add symbol
        if add_symbol:
            passphrase += secrets.choice(SPECIAL)
        
        return passphrase
    
    def analyze_strength(self, password: str) -> PasswordStrength:
        """
        Analyze password strength.
        
        Args:
            password: Password to analyze
            
        Returns:
            PasswordStrength object with detailed analysis
        """
        length = len(password)
        has_lower = bool(re.search(r"[a-z]", password))
        has_upper = bool(re.search(r"[A-Z]", password))
        has_digit = bool(re.search(r"\d", password))
        has_special = bool(re.search(r"[^a-zA-Z0-9]", password))
        
        # Calculate character diversity
        unique_chars = len(set(password))
        diversity = unique_chars / length if length > 0 else 0
        
        # Calculate entropy
        charset_size = 0
        if has_lower:
            charset_size += 26
        if has_upper:
            charset_size += 26
        if has_digit:
            charset_size += 10
        if has_special:
            charset_size += len(SPECIAL)
        
        entropy = length * (charset_size.bit_length()) if charset_size > 0 else 0
        
        # Calculate score (0-100)
        score = 0
        issues = []
        suggestions = []
        
        # Length scoring (max 30 points)
        if length >= 16:
            score += 30
        elif length >= 12:
            score += 25
        elif length >= 10:
            score += 20
        elif length >= 8:
            score += 15
        else:
            score += max(0, length * 2)
            issues.append("Password is too short")
            suggestions.append("Use at least 12 characters")
        
        # Character type scoring (max 40 points)
        type_count = sum([has_lower, has_upper, has_digit, has_special])
        score += type_count * 10
        
        if not has_lower:
            issues.append("Missing lowercase letters")
            suggestions.append("Add lowercase letters (a-z)")
        if not has_upper:
            issues.append("Missing uppercase letters")
            suggestions.append("Add uppercase letters (A-Z)")
        if not has_digit:
            issues.append("Missing digits")
            suggestions.append("Add numbers (0-9)")
        if not has_special:
            issues.append("Missing special characters")
            suggestions.append("Add special characters (!@#$%^&*)")
        
        # Diversity scoring (max 15 points)
        score += int(diversity * 15)
        
        # Penalty for common patterns
        if password.lower() in COMMON_PASSWORDS:
            score -= 30
            issues.append("This is a commonly used password")
            suggestions.append("Choose a unique password")
        
        # Check for sequential patterns
        lower_pwd = password.lower()
        for pattern in SEQUENTIAL_PATTERNS:
            if pattern in lower_pwd:
                score -= 10
                issues.append("Contains sequential characters")
                suggestions.append("Avoid sequential patterns like 'abc' or '123'")
                break
        
        # Check for repeated characters
        if re.search(r"(.)\1{2,}", password):
            score -= 10
            issues.append("Contains repeated characters")
            suggestions.append("Avoid repeating the same character")
        
        # Clamp score
        score = max(0, min(100, score))
        
        # Determine strength level
        if score >= 90:
            level = StrengthLevel.VERY_STRONG
        elif score >= 75:
            level = StrengthLevel.STRONG
        elif score >= 50:
            level = StrengthLevel.FAIR
        elif score >= 25:
            level = StrengthLevel.WEAK
        else:
            level = StrengthLevel.VERY_WEAK
        
        return PasswordStrength(
            level=level,
            score=score,
            entropy_bits=entropy,
            length=length,
            has_lowercase=has_lower,
            has_uppercase=has_upper,
            has_digits=has_digit,
            has_special=has_special,
            character_diversity=diversity,
            issues=issues,
            suggestions=suggestions,
        )
    
    def validate(
        self,
        password: str,
        require_uppercase: bool = True,
        require_lowercase: bool = True,
        require_digit: bool = True,
        require_special: bool = False,
        check_common: bool = True,
        check_sequential: bool = True,
        username: Optional[str] = None,
        email: Optional[str] = None,
    ) -> ValidationResult:
        """
        Validate password against security policy.
        
        Args:
            password: Password to validate
            require_uppercase: Require uppercase letters
            require_lowercase: Require lowercase letters
            require_digit: Require digits
            require_special: Require special characters
            check_common: Check against common passwords list
            check_sequential: Check for sequential patterns
            username: Username to check against (optional)
            email: Email to check against (optional)
            
        Returns:
            ValidationResult with validation status and errors
        """
        errors = []
        error_messages = []
        
        # Length check
        if len(password) < self.min_length:
            errors.append(ValidationError.TOO_SHORT)
            error_messages.append(f"Password must be at least {self.min_length} characters")
        
        if len(password) > self.max_length:
            errors.append(ValidationError.TOO_LONG)
            error_messages.append(f"Password cannot exceed {self.max_length} characters")
        
        # Character type checks
        if require_uppercase and not re.search(r"[A-Z]", password):
            errors.append(ValidationError.NO_UPPERCASE)
            error_messages.append("Password must contain uppercase letters")
        
        if require_lowercase and not re.search(r"[a-z]", password):
            errors.append(ValidationError.NO_LOWERCASE)
            error_messages.append("Password must contain lowercase letters")
        
        if require_digit and not re.search(r"\d", password):
            errors.append(ValidationError.NO_DIGIT)
            error_messages.append("Password must contain digits")
        
        if require_special and not re.search(r"[^a-zA-Z0-9]", password):
            errors.append(ValidationError.NO_SPECIAL)
            error_messages.append("Password must contain special characters")
        
        # Common password check
        if check_common and password.lower() in COMMON_PASSWORDS:
            errors.append(ValidationError.COMMON_PASSWORD)
            error_messages.append("This is a commonly used password")
        
        # Sequential pattern check
        if check_sequential:
            lower_pwd = password.lower()
            for pattern in SEQUENTIAL_PATTERNS:
                if pattern in lower_pwd:
                    errors.append(ValidationError.SEQUENTIAL_CHARS)
                    error_messages.append("Password contains sequential characters")
                    break
        
        # Repeated characters check
        if re.search(r"(.)\1{3,}", password):
            errors.append(ValidationError.REPEATED_CHARS)
            error_messages.append("Password contains too many repeated characters")
        
        # Username/email check
        if username and username.lower() in password.lower():
            errors.append(ValidationError.CONTAINS_USERNAME)
            error_messages.append("Password cannot contain username")
        
        if email and "@" in email:
            email_user = email.split("@")[0]
            if email_user.lower() in password.lower():
                errors.append(ValidationError.CONTAINS_EMAIL)
                error_messages.append("Password cannot contain email address")
        
        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            error_messages=error_messages,
        )
    
    def hash_password(
        self,
        password: str,
        salt: Optional[bytes] = None,
        algorithm: str = "sha256",
        iterations: int = 100000,
    ) -> Tuple[str, str]:
        """
        Hash a password with salt.
        
        Args:
            password: Password to hash
            salt: Salt bytes (generated if None)
            algorithm: Hash algorithm (sha256, sha512, blake2b)
            iterations: Number of iterations for key stretching
            
        Returns:
            Tuple of (hashed_password_hex, salt_hex)
        """
        if salt is None:
            salt = secrets.token_bytes(32)
        
        # Key stretching with multiple iterations
        password_bytes = password.encode("utf-8")
        hash_bytes = hashlib.pbkdf2_hmac(
            algorithm,
            password_bytes,
            salt,
            iterations,
        )
        
        return hash_bytes.hex(), salt.hex()
    
    def verify_password(
        self,
        password: str,
        stored_hash: str,
        salt_hex: str,
        algorithm: str = "sha256",
        iterations: int = 100000,
    ) -> bool:
        """
        Verify a password against stored hash.
        
        Args:
            password: Password to verify
            stored_hash: Stored hash (hex string)
            salt_hex: Salt (hex string)
            algorithm: Hash algorithm used
            iterations: Number of iterations used
            
        Returns:
            True if password matches, False otherwise
        """
        salt = bytes.fromhex(salt_hex)
        computed_hash, _ = self.hash_password(
            password, salt, algorithm, iterations
        )
        return hmac.compare_digest(computed_hash, stored_hash)
    
    def is_breached(self, password: str) -> bool:
        """
        Check if password appears in common breached passwords list.
        
        Args:
            password: Password to check
            
        Returns:
            True if password is in common passwords list
        """
        return password.lower() in COMMON_PASSWORDS
    
    def estimate_crack_time(
        self,
        password: str,
        guesses_per_second: int = 10_000_000_000,
    ) -> Dict[str, Any]:
        """
        Estimate time to crack password via brute force.
        
        Args:
            password: Password to analyze
            guesses_per_second: Assumed attack speed (default: 10 billion/s)
            
        Returns:
            Dictionary with time estimates
        """
        strength = self.analyze_strength(password)
        
        # Calculate total combinations
        combinations = 2 ** strength.entropy_bits
        
        # Time in seconds
        seconds = combinations / guesses_per_second
        
        # Format time
        if seconds < 1:
            time_str = "instantly"
        elif seconds < 60:
            time_str = f"{seconds:.1f} seconds"
        elif seconds < 3600:
            time_str = f"{seconds / 60:.1f} minutes"
        elif seconds < 86400:
            time_str = f"{seconds / 3600:.1f} hours"
        elif seconds < 31536000:
            time_str = f"{seconds / 86400:.1f} days"
        elif seconds < 31536000 * 100:
            time_str = f"{seconds / 31536000:.1f} years"
        elif seconds < 31536000 * 1000000:
            time_str = f"{seconds / 31536000:.0f} years"
        else:
            time_str = "centuries"
        
        return {
            "entropy_bits": round(strength.entropy_bits, 2),
            "combinations": f"{combinations:.2e}",
            "guesses_per_second": guesses_per_second,
            "time_to_crack": time_str,
            "seconds": seconds,
        }
    
    def _get_common_words(self) -> List[str]:
        """Get a list of common words for passphrase generation."""
        return [
            "apple", "river", "mountain", "ocean", "forest", "sunset", "dawn",
            "winter", "summer", "spring", "autumn", "thunder", "lightning",
            "rainbow", "crystal", "diamond", "silver", "golden", "bronze",
            "eagle", "falcon", "phoenix", "dragon", "tiger", "wolf", "bear",
            "shadow", "spirit", "wisdom", "courage", "freedom", "justice",
            "harmony", "balance", "nature", "cosmos", "galaxy", "stellar",
            "quantum", "atomic", "molecular", "digital", "cyber", "neural",
            "silent", "quiet", "peaceful", "calm", "serene", "tranquil",
            "bright", "brilliant", "radiant", "luminous", "glowing", "shining",
            "swift", "rapid", "quick", "fast", "speedy", "nimble", "agile",
            "strong", "mighty", "powerful", "robust", "sturdy", "solid",
            "gentle", "kind", "warm", "friendly", "loyal", "faithful",
            "ancient", "eternal", "timeless", "infinite", "endless", "boundless",
        ]


# Convenience functions (module-level)
_default_utils = PasswordUtils()


def generate_password(
    length: int = 16,
    use_lowercase: bool = True,
    use_uppercase: bool = True,
    use_digits: bool = True,
    use_special: bool = True,
    exclude_ambiguous: bool = False,
) -> str:
    """Generate a secure random password."""
    return _default_utils.generate(
        length, use_lowercase, use_uppercase, use_digits, use_special,
        exclude_ambiguous, ensure_all_types=True
    )


def generate_passphrase(
    word_count: int = 4,
    separator: str = "-",
    use_capitalization: bool = True,
    add_number: bool = False,
) -> str:
    """Generate a memorable passphrase."""
    return _default_utils.generate_passphrase(
        word_count, separator, use_capitalization, add_number
    )


def analyze(password: str) -> PasswordStrength:
    """Analyze password strength."""
    return _default_utils.analyze_strength(password)


def validate(
    password: str,
    require_uppercase: bool = True,
    require_lowercase: bool = True,
    require_digit: bool = True,
) -> ValidationResult:
    """Validate password against security policy."""
    return _default_utils.validate(
        password, require_uppercase, require_lowercase, require_digit
    )


def hash_password(password: str, salt: Optional[bytes] = None) -> Tuple[str, str]:
    """Hash a password with salt."""
    return _default_utils.hash_password(password, salt)


def verify_password(
    password: str, stored_hash: str, salt_hex: str
) -> bool:
    """Verify a password against stored hash."""
    return _default_utils.verify_password(password, stored_hash, salt_hex)


def is_weak(password: str) -> bool:
    """Check if password is weak."""
    strength = _default_utils.analyze_strength(password)
    return strength.level in [StrengthLevel.VERY_WEAK, StrengthLevel.WEAK]


def is_strong(password: str) -> bool:
    """Check if password is strong."""
    strength = _default_utils.analyze_strength(password)
    return strength.level in [StrengthLevel.STRONG, StrengthLevel.VERY_STRONG]
