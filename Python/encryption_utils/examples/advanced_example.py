"""
AllToolkit - Encryption Utils Advanced Examples

Advanced use cases including authentication, API security, and data integrity.
"""

import sys
import os
import time
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    hash_password, verify_password,
    compute_hmac, verify_hmac,
    generate_token, generate_api_key, generate_session_id,
    derive_key,
    HashChain,
    SecureString,
    url_safe_encode, url_safe_decode,
    xor_encrypt, xor_decrypt,
    base64_encode,
    hash_data,
    EncryptionError,
)


# =============================================================================
# Example 1: User Authentication System
# =============================================================================

class AuthSystem:
    """Simple authentication system demonstration."""
    
    def __init__(self):
        self.users = {}  # username -> hashed_password
        self.sessions = {}  # session_id -> username
    
    def register(self, username: str, password: str) -> bool:
        """Register a new user."""
        if username in self.users:
            return False
        
        hashed = hash_password(password)
        self.users[username] = hashed
        print(f"  ✓ User '{username}' registered")
        return True
    
    def login(self, username: str, password: str) -> str:
        """Login and return session ID."""
        if username not in self.users:
            raise ValueError("User not found")
        
        if not verify_password(password, self.users[username]):
            raise ValueError("Invalid password")
        
        session_id = generate_session_id()
        self.sessions[session_id] = username
        print(f"  ✓ User '{username}' logged in")
        return session_id
    
    def logout(self, session_id: str) -> bool:
        """Logout and invalidate session."""
        if session_id in self.sessions:
            username = self.sessions.pop(session_id)
            print(f"  ✓ User '{username}' logged out")
            return True
        return False
    
    def get_user(self, session_id: str) -> str:
        """Get username from session."""
        return self.sessions.get(session_id)


def example_auth_system():
    """Demonstrate authentication system."""
    print("\n" + "=" * 60)
    print("Example 1: User Authentication System")
    print("=" * 60)
    
    auth = AuthSystem()
    
    # Register users
    print("\n[Register]");
    auth.register("alice", "AliceP@ss123")
    auth.register("bob", "BobSecure456")
    
    # Login
    print("\n[Login]");
    session1 = auth.login("alice", "AliceP@ss123")
    print(f"  Session: {session1[:20]}...")
    
    session2 = auth.login("bob", "BobSecure456")
    print(f"  Session: {session2[:20]}...")
    
    # Wrong password
    print("\n[Failed Login]");
    try:
        auth.login("alice", "wrong_password")
    except ValueError as e:
        print(f"  ✗ {e}")
    
    # Get user from session
    print("\n[Session Lookup]");
    print(f"  Session 1 user: {auth.get_user(session1)}")
    print(f"  Session 2 user: {auth.get_user(session2)}")
    
    # Logout
    print("\n[Logout]");
    auth.logout(session1)
    print(f"  Session 1 user after logout: {auth.get_user(session1)}")


# =============================================================================
# Example 2: API Request Signing
# =============================================================================

class APISecurity:
    """API request signing and verification."""
    
    def __init__(self):
        self.api_keys = {}  # key_id -> secret
    
    def create_credentials(self, user_id: str) -> tuple:
        """Create API credentials for a user."""
        key_id = generate_api_key(prefix="ak")
        secret = generate_token(url_safe=True)
        self.api_keys[key_id] = secret
        return key_id, secret
    
    def sign_request(self, method: str, path: str, body: str, secret: str) -> str:
        """Sign an API request."""
        # Create message to sign
        timestamp = str(int(time.time()))
        message = f"{method}:{path}:{timestamp}:{body}"
        signature = compute_hmac(message, secret)
        return f"{timestamp}:{signature}"
    
    def verify_request(self, method: str, path: str, body: str, 
                       key_id: str, timestamp_signature: str,
                       max_age: int = 300) -> bool:
        """Verify an API request signature."""
        secret = self.api_keys.get(key_id)
        if not secret:
            return False
        
        try:
            timestamp_str, signature = timestamp_signature.split(':', 1)
            timestamp = int(timestamp_str)
            
            # Check timestamp freshness
            if abs(time.time() - timestamp) > max_age:
                print("  ✗ Request expired")
                return False
            
            # Verify signature
            message = f"{method}:{path}:{timestamp_str}:{body}"
            return verify_hmac(message, signature, secret)
        except Exception as e:
            print(f"  ✗ Verification error: {e}")
            return False


def example_api_security():
    """Demonstrate API security."""
    print("\n" + "=" * 60)
    print("Example 2: API Request Signing")
    print("=" * 60)
    
    api = APISecurity()
    
    # Create credentials
    print("\n[Create Credentials]");
    key_id, secret = api.create_credentials("user_123")
    print(f"  Key ID: {key_id}")
    print(f"  Secret: {secret[:20]}...")
    
    # Sign request
    print("\n[Sign Request]");
    method = "POST"
    path = "/api/data"
    body = json.dumps({"action": "create", "value": 42})
    
    signature = api.sign_request(method, path, body, secret)
    print(f"  Signature: {signature[:50]}...")
    
    # Verify valid request
    print("\n[Verify Valid Request]");
    valid = api.verify_request(method, path, body, key_id, signature)
    print(f"  Valid: {valid}")
    
    # Verify tampered request
    print("\n[Verify Tampered Request]");
    tampered_body = json.dumps({"action": "delete", "value": 42})
    invalid = api.verify_request(method, path, tampered_body, key_id, signature)
    print(f"  Valid: {invalid}")


# =============================================================================
# Example 3: Data Integrity Chain
# =============================================================================

class AuditLogger:
    """Tamper-evident audit log using hash chain."""
    
    def __init__(self):
        self.chain = HashChain()
        self.entries = []
    
    def log(self, event_type: str, user: str, action: str, details: dict = None):
        """Add an audit log entry."""
        entry = {
            'timestamp': time.time(),
            'type': event_type,
            'user': user,
            'action': action,
            'details': details or {},
        }
        self.entries.append(entry)
        
        # Add to hash chain
        entry_str = json.dumps(entry, sort_keys=True)
        self.chain.add(entry_str)
        
        print(f"  ✓ Logged: {event_type} - {action}")
    
    def get_fingerprint(self) -> str:
        """Get current chain fingerprint."""
        return self.chain.get_chain_hash()
    
    def verify_integrity(self) -> bool:
        """Verify log integrity."""
        # Recreate chain from entries
        verify_chain = HashChain()
        for entry in self.entries:
            entry_str = json.dumps(entry, sort_keys=True)
            verify_chain.add(entry_str)
        
        expected = self.get_fingerprint()
        actual = verify_chain.get_chain_hash()
        
        return expected == actual
    
    def export(self) -> dict:
        """Export log with fingerprint."""
        return {
            'entries': self.entries,
            'fingerprint': self.get_fingerprint(),
            'count': len(self.entries),
        }


def example_audit_log():
    """Demonstrate audit logging."""
    print("\n" + "=" * 60)
    print("Example 3: Tamper-Evident Audit Log")
    print("=" * 60)
    
    logger = AuditLogger()
    
    # Log events
    print("\n[Log Events]");
    logger.log("LOGIN", "alice", "user_login", {'ip': '192.168.1.1'})
    logger.log("ACCESS", "alice", "read_file", {'file': '/docs/report.pdf'})
    logger.log("MODIFY", "alice", "update_record", {'table': 'users', 'id': 42})
    logger.log("LOGOUT", "alice", "user_logout", {})
    
    # Get fingerprint
    print("\n[Fingerprint]");
    fp = logger.get_fingerprint()
    print(f"  Chain hash: {fp[:40]}...")
    
    # Verify integrity
    print("\n[Verify Integrity]");
    valid = logger.verify_integrity()
    print(f"  Integrity: {'✓ Valid' if valid else '✗ Tampered'}")
    
    # Export
    print("\n[Export]");
    exported = logger.export()
    print(f"  Entries: {exported['count']}")
    print(f"  Fingerprint: {exported['fingerprint'][:40]}...")


# =============================================================================
# Example 4: Secure Configuration Storage
# =============================================================================

class SecureConfig:
    """Encrypt sensitive configuration values."""
    
    def __init__(self, master_password: str):
        self._key, self._salt = derive_key(master_password)
        self._config = {}
    
    def set(self, key: str, value: str):
        """Store encrypted config value."""
        encrypted = xor_encrypt(value, self._key)
        self._config[key] = base64_encode(encrypted)
        print(f"  ✓ Stored: {key}")
    
    def get(self, key: str) -> str:
        """Retrieve decrypted config value."""
        if key not in self._config:
            raise KeyError(key)
        
        encrypted = url_safe_decode(self._config[key])
        decrypted = xor_decrypt(encrypted, self._key)
        return decrypted.decode('utf-8')
    
    def list_keys(self) -> list:
        """List all config keys."""
        return list(self._config.keys())


def example_secure_config():
    """Demonstrate secure config storage."""
    print("\n" + "=" * 60)
    print("Example 4: Secure Configuration Storage")
    print("=" * 60)
    
    master = "MyMasterPassword123!"
    config = SecureConfig(master)
    
    # Store secrets
    print("\n[Store Secrets]");
    config.set("database.password", "db_secret_123")
    config.set("api.key", "sk_live_abcdef123456")
    config.set("jwt.secret", "super_secret_jwt_key")
    
    # Retrieve
    print("\n[Retrieve Secrets]");
    db_pass = config.get("database.password")
    print(f"  DB Password: {db_pass}")
    
    api_key = config.get("api.key")
    print(f"  API Key: {api_key}")
    
    # List keys
    print("\n[Config Keys]");
    print(f"  Keys: {config.list_keys()}")


# =============================================================================
# Example 5: Secure String Handling
# =============================================================================

def example_secure_string():
    """Demonstrate SecureString usage."""
    print("\n" + "=" * 60)
    print("Example 5: Secure String Handling")
    print("=" * 60)
    
    # Normal usage
    print("\n[Normal Usage]");
    with SecureString("sensitive_data") as ss:
        print(f"  Value: {ss.get()}")
        print(f"  Repr: {repr(ss)}")
    
    print(f"  After context: {repr(ss)}")
    
    # Manual consume
    print("\n[Manual Consume]");
    ss2 = SecureString("another_secret")
    value = ss2.consume()
    print(f"  Consumed value: {value}")
    
    try:
        ss2.get()
    except EncryptionError as e:
        print(f"  After consume: {e}")


# =============================================================================
# Example 6: Token-Based Session Management
# =============================================================================

class TokenSession:
    """Token-based session with expiration."""
    
    def __init__(self, ttl: int = 3600):
        self.ttl = ttl
        self.sessions = {}  # token -> {user, created}
    
    def create(self, user_id: str) -> str:
        """Create a new session token."""
        token = generate_token(url_safe=True, include_timestamp=True)
        self.sessions[token] = {
            'user': user_id,
            'created': time.time(),
        }
        return token
    
    def validate(self, token: str) -> dict:
        """Validate session token."""
        if token not in self.sessions:
            return None
        
        session = self.sessions[token]
        age = time.time() - session['created']
        
        if age > self.ttl:
            del self.sessions[token]
            return None
        
        return session
    
    def revoke(self, token: str) -> bool:
        """Revoke a session token."""
        if token in self.sessions:
            del self.sessions[token]
            return True
        return False


def example_token_session():
    """Demonstrate token sessions."""
    print("\n" + "=" * 60)
    print("Example 6: Token-Based Session Management")
    print("=" * 60)
    
    session_mgr = TokenSession(ttl=5)  # 5 second TTL for demo
    
    # Create session
    print("\n[Create Session]");
    token = session_mgr.create("user_456")
    print(f"  Token: {token[:40]}...")
    
    # Validate
    print("\n[Validate Session]");
    session = session_mgr.validate(token)
    print(f"  User: {session['user']}")
    print(f"  Created: {session['created']}")
    
    # Wait and revalidate (should expire)
    print("\n[Wait for expiration]");
    time.sleep(6)
    
    expired = session_mgr.validate(token)
    print(f"  After TTL: {'Expired' if expired is None else 'Valid'}")


# =============================================================================
# Main
# =============================================================================

def main():
    print("\n" + "█" * 60)
    print("█  AllToolkit - Encryption Utils Advanced Examples")
    print("█" * 60)
    
    example_auth_system()
    example_api_security()
    example_audit_log()
    example_secure_config()
    example_secure_string()
    example_token_session()
    
    print("\n" + "█" * 60)
    print("█  All examples completed!")
    print("█" * 60 + "\n")


if __name__ == '__main__':
    main()
