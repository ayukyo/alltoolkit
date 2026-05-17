fn main() {
    let bytes = vec![10u8];
    println!("bytes: {:?}", bytes);
    
    let mut bits = Vec::new();
    for &byte in &bytes {
        for i in (0..8).rev() {
            bits.push((byte >> i) & 1 == 1);
        }
    }
    println!("bits: {:?}", bits);
}
