# Diffie-Hellman Key Exchange Utils

A pure Rust implementation of the Diffie-Hellman key exchange protocol with **zero external dependencies**.

## Features

- **Key Generation**: Generate secure key pairs with configurable parameters
- **RFC 3526 Support**: Pre-defined safe primes (1536, 2048, 3072, 4096 bits)
- **Shared Secret Computation**: Derive shared secrets from public keys
- **Key Validation**: Validate public keys for security
- **Constant-Time Comparison**: Security-focused comparison for secrets
- **Key Derivation**: Derive encryption keys from shared secrets
- **BigInt Implementation**: Full BigInt arithmetic for large number operations

## Installation

Add to your `Cargo.toml`:

```toml
[dependencies]
diffie_hellman_utils = { path = "." }
```

## Quick Start

```rust
use diffie_hellman_utils::{DHParams, DHKeyPair, DHExchange, verify_shared_secret};

// Method 1: Using DHExchange (simplified)
let alice = DHExchange::new();
let bob = DHExchange::new();

let alice_secret = alice.compute_secret(bob.public_key());
let bob_secret = bob.compute_secret(alice.public_key());

assert!(verify_shared_secret(&alice_secret, &bob_secret));

// Method 2: Using DHKeyPair (more control)
let params = DHParams::rfc3526_2048();
let alice_key = DHKeyPair::generate(&params);
let bob_key = DHKeyPair::generate(&params);

let alice_secret = alice_key.compute_shared_secret(bob_key.public_key());
let bob_secret = bob_key.compute_shared_secret(alice_key.public_key());

assert!(verify_shared_secret(&alice_secret, &bob_secret));
```

## API Reference

### DHParams

Diffie-Hellman parameters (prime modulus and generator).

```rust
// Use RFC 3526 standardized parameters
let params = DHParams::rfc3526_2048();  // 2048-bit
let params = DHParams::rfc3526_3072();  // 3072-bit
let params = DHParams::rfc3526_4096();  // 4096-bit

// Create custom parameters
let params = DHParams::from_hex("FF...", 2)?;
```

### DHKeyPair

A Diffie-Hellman key pair containing private and public keys.

```rust
let keypair = DHKeyPair::generate(&params);

// Get keys
let public = keypair.public_key();   // Share this!
let private = keypair.private_key(); // Keep secret!

// Compute shared secret
let shared = keypair.compute_shared_secret(&other_public);
```

### DHExchange

Simplified interface for quick key exchange.

```rust
let exchange = DHExchange::new();

// Get public key
let public_hex = exchange.public_key_hex();

// Compute secret from other's public key
let secret = exchange.compute_secret_from_hex(&other_public_hex)?;

// Derive encryption key
let key = exchange.derive_key(&secret, 32);  // 256-bit key
```

### BigInt

Arbitrary-precision integer for cryptographic operations.

```rust
use diffie_hellman_utils::BigInt;

let a = BigInt::from_hex("FFFFFFFFFFFFFFFF")?;
let b = BigInt::from_u64(1);

// Arithmetic operations
let sum = a.add(&b);
let diff = a.sub(&b);
let product = a.mul(&b);

// Modular arithmetic
let remainder = a.modulo(&m);
let power = base.pow_mod(&exp, &m);

// Division
let (quotient, remainder) = a.div_rem(&b);

// Conversion
let hex = a.to_hex();
```

## Security Considerations

1. **Private Key Protection**: Never share or transmit private keys
2. **Key Validation**: Always validate received public keys
3. **Parameter Selection**: Use RFC 3526 parameters for proven security
4. **Forward Secrecy**: Generate new key pairs for each session
5. **Key Derivation**: Use a proper KDF (HKDF, PBKDF2) for production use

## Security Features

- Constant-time comparison for secret verification
- Public key validation (1 < public_key < prime)
- Uses well-tested RFC 3526 safe primes
- No external dependencies reduces attack surface

## Example: Secure Messaging

```rust
use diffie_hellman_utils::{DHExchange, verify_shared_secret};

fn main() {
    // Alice creates her key exchange
    let alice = DHExchange::new();
    let alice_public = alice.public_key_hex();
    
    // Bob creates his key exchange
    let bob = DHExchange::new();
    let bob_public = bob.public_key_hex();
    
    // They exchange public keys over an insecure channel
    // (In practice, use authenticated channels)
    
    // Both compute the same shared secret
    let alice_secret = alice.compute_secret_from_hex(&bob_public).unwrap();
    let bob_secret = bob.compute_secret_from_hex(&alice_public).unwrap();
    
    // Verify secrets match
    if verify_shared_secret(&alice_secret, &bob_secret) {
        // Derive encryption key
        let key = alice.derive_key(&alice_secret, 32);
        println!("Secure channel established!");
        println!("Key: {:02x?}", key);
    }
}
```

## Testing

Run the test suite:

```bash
cargo test
```

Run the example:

```bash
cargo run --example example
```

## License

MIT License