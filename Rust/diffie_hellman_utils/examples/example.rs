//! Diffie-Hellman Key Exchange Example

use diffie_hellman_utils::{DHParams, DHKeyPair, DHExchange, BigInt, verify_shared_secret};

fn main() {
    println!("=== Diffie-Hellman Key Exchange Demo ===\n");

    // Example 1: Basic key exchange
    basic_exchange();

    // Example 2: Simplified DHExchange
    simplified_exchange();

    // Example 3: Different parameter sizes
    param_sizes();

    // Example 4: Key derivation
    key_derivation();

    // Example 5: BigInt operations
    bigint_ops();
}

fn basic_exchange() {
    println!("--- Example 1: Basic Key Exchange ---");
    
    let params = DHParams::rfc3526_2048();
    println!("Using {}-bit MODP group", params.bit_length());

    let alice = DHKeyPair::generate(&params);
    let alice_pub = alice.public_key();
    println!("Alice's public key: {}...{}", 
        &alice_pub.to_hex()[..16],
        &alice_pub.to_hex()[alice_pub.to_hex().len().saturating_sub(16)..]
    );

    let bob = DHKeyPair::generate(&params);
    let bob_pub = bob.public_key();
    println!("Bob's public key: {}...{}", 
        &bob_pub.to_hex()[..16],
        &bob_pub.to_hex()[bob_pub.to_hex().len().saturating_sub(16)..]
    );

    let alice_secret = alice.compute_shared_secret(&bob_pub);
    let bob_secret = bob.compute_shared_secret(&alice_pub);

    println!("Shared secret computed!");
    if verify_shared_secret(&alice_secret, &bob_secret) {
        println!("✓ Secrets match! Secure channel established.\n");
    }
}

fn simplified_exchange() {
    println!("--- Example 2: Simplified DHExchange ---");
    
    let alice = DHExchange::new();
    let bob = DHExchange::new();

    let alice_hex = alice.public_key_hex();
    let bob_hex = bob.public_key_hex();

    println!("Alice sends: {}...", &alice_hex[..32]);
    println!("Bob sends: {}...", &bob_hex[..32]);

    let alice_secret = alice.compute_secret_from_hex(&bob_hex).unwrap();
    let bob_secret = bob.compute_secret_from_hex(&alice_hex).unwrap();

    if verify_shared_secret(&alice_secret, &bob_secret) {
        println!("✓ Key exchange successful!\n");
    }
}

fn param_sizes() {
    println!("--- Example 3: Different Parameter Sizes ---");
    
    let sizes = [
        ("1536-bit", DHParams::rfc3526_1536()),
        ("2048-bit", DHParams::rfc3526_2048()),
        ("3072-bit", DHParams::rfc3526_3072()),
    ];

    for (name, params) in sizes {
        let alice = DHKeyPair::generate(&params);
        let bob = DHKeyPair::generate(&params);
        
        let bob_pub = bob.public_key();
        let secret = alice.compute_shared_secret(&bob_pub);
        
        println!("{}: secret length = {} bits", name, secret.bit_length());
    }
    println!();
}

fn key_derivation() {
    println!("--- Example 4: Key Derivation ---");
    
    let alice = DHExchange::new();
    let bob = DHExchange::new();
    
    let bob_pub = bob.public_key();
    let secret = alice.compute_secret(&bob_pub);

    let key_16 = alice.derive_key(&secret, 16);
    let key_32 = alice.derive_key(&secret, 32);

    println!("Derived keys from shared secret:");
    println!("128-bit key: {:02x?}", key_16);
    println!("256-bit key: {:02x?}", &key_32[..16]);
    println!("... (truncated)\n");
}

fn bigint_ops() {
    println!("--- Example 5: BigInt Operations ---");
    
    let a = BigInt::from_hex("FFFFFFFFFFFFFFFF").unwrap();
    let b = BigInt::from_u64(1);
    
    let sum = a.add(&b);
    println!("FFFFFFFFFFFFFFFF + 1 = {}", sum.to_hex());

    let x = BigInt::from_u64(12345);
    let y = BigInt::from_u64(67890);
    let product = x.mul(&y);
    println!("12345 * 67890 = {}", product.to_hex());

    let base = BigInt::from_u64(2);
    let exp = BigInt::from_u64(10);
    let mod_val = BigInt::from_u64(1000);
    let result = base.pow_mod(exp.as_bytes(), mod_val.as_bytes());
    println!("2^10 mod 1000 = {}", result.to_hex());

    let big = BigInt::from_hex("DEADBEEFCAFEBABE12345678").unwrap();
    println!("Bit length of DEADBEEFCAFEBABE12345678: {} bits", big.bit_length());
    
    println!();
}