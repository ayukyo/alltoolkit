# OTP Utilities Module

A comprehensive One-Time Password (OTP) utility module for Python with **zero external dependencies**.

## Features

- **TOTP** (Time-based One-Time Password) generation and validation (RFC 6238)
- **HOTP** (HMAC-based One-Time Password) generation and validation (RFC 4226)
- Base32 secret encoding/decoding
- OTP URI generation for QR codes (authenticator apps)
- Configurable digits (6, 7, 8) and hash algorithms (SHA1, SHA256, SHA512)
- Recovery codes generation for 2FA backup
- Convenience classes `TOTP` and `HOTP`

## Installation

No installation required! This module uses only Python standard library.

```python
from otp_utils.mod import TOTP, HOTP, generate_secret
```

## Quick Start

### TOTP (Time-based OTP)

```python
from otp_utils.mod import TOTP, generate_secret

# Generate a new secret
secret = generate_secret()

# Create TOTP instance
totp = TOTP(secret)

# Generate current code
code = totp.generate()
print(f"Current code: {code}")

# Validate a code
if totp.validate(code):
    print("Valid!")

# Get URI for authenticator app
uri = totp.get_uri('user@example.com', 'MyApp')
print(f"Add to authenticator: {uri}")

# Time remaining until next code
remaining = totp.get_remaining_seconds()
print(f"Seconds until next code: {remaining}")
```

### HOTP (Counter-based OTP)

```python
from otp_utils.mod import HOTP, generate_secret

secret = generate_secret()
hotp = HOTP(secret)

# Generate codes (counter auto-increments)
code0 = hotp.generate()  # counter = 0, then increments
code1 = hotp.generate()  # counter = 1

# Validate at specific counter
if hotp.validate(code0, 0):
    print("Valid!")

# Get URI for authenticator
uri = hotp.get_uri('user@example.com', 'MyApp')
```

### Recovery Codes

```python
from otp_utils.mod import generate_recovery_codes, validate_recovery_code

# Generate 10 recovery codes
codes = generate_recovery_codes(10, 8)
# ['ABCD-EFGH', 'IJKL-MNOP', ...]

# Validate and consume a code
is_valid, remaining = validate_recovery_code(codes, 'ABCD-EFGH')
if is_valid:
    print("Valid recovery code!")
```

## API Reference

### Functions

| Function | Description |
|----------|-------------|
| `generate_secret(length=20)` | Generate a random Base32 secret |
| `encode_base32(data)` | Encode bytes to Base32 |
| `decode_base32(data)` | Decode Base32 to bytes |
| `generate_totp(secret, ...)` | Generate TOTP code |
| `validate_totp(secret, code, ...)` | Validate TOTP code |
| `generate_hotp(secret, counter, ...)` | Generate HOTP code |
| `validate_hotp(secret, counter, code, ...)` | Validate HOTP code |
| `build_totp_uri(secret, account, issuer, ...)` | Build otpauth:// URI for TOTP |
| `build_hotp_uri(secret, account, issuer, counter, ...)` | Build otpauth:// URI for HOTP |
| `parse_otp_uri(uri)` | Parse otpauth:// URI |
| `generate_recovery_codes(count, length)` | Generate backup codes |
| `validate_recovery_code(codes, input_code, ...)` | Validate recovery code |
| `get_remaining_seconds(period, timestamp)` | Time until next TOTP |
| `format_code(code, group_size)` | Format code with spaces |

### Parameters

| Parameter | Default | Options |
|-----------|---------|---------|
| `digits` | 6 | 6, 7, 8 |
| `algorithm` | SHA1 | SHA1, SHA256, SHA512 |
| `period` | 30 | Any positive integer (seconds) |
| `window` | 1 | Number of intervals for validation |

### Classes

#### TOTP

```python
totp = TOTP(secret, digits=6, period=30, algorithm='SHA1')
totp.generate()           # Generate current code
totp.validate(code)       # Validate code
totp.get_uri(account, issuer)  # Get otpauth:// URI
totp.get_remaining_seconds()   # Time until next refresh
```

#### HOTP

```python
hotp = HOTP(secret, digits=6, algorithm='SHA1')
hotp.generate()           # Generate and increment counter
hotp.generate(counter)    # Generate at specific counter
hotp.validate(code, counter)  # Validate code
hotp.get_uri(account, issuer)  # Get otpauth:// URI
hotp.reset_counter(value)      # Reset counter
```

## Security Notes

1. **Secret Storage**: Store secrets securely (encrypted database, not plain text)
2. **HTTPS**: Always use HTTPS when transmitting secrets
3. **Window Size**: Keep validation window small (default 1) to prevent replay attacks
4. **Recovery Codes**: Generate and store recovery codes securely as backup

## Running Tests

```bash
python otp_utils_test.py
```

## License

MIT License - Part of AllToolkit