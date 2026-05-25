fn gray_to_binary_u8(gray: u8) -> u8 {
    let mut binary = gray;
    let mut shift: u32 = 1;
    
    while shift < 8 {
        binary = binary ^ (binary >> shift);
        shift += 1;
    }
    binary
}

fn main() {
    println!("gray_to_binary(0) = {}", gray_to_binary_u8(0));
    println!("gray_to_binary(1) = {}", gray_to_binary_u8(1));
    println!("gray_to_binary(3) = {}", gray_to_binary_u8(3));
    println!("gray_to_binary(2) = {}", gray_to_binary_u8(2));
    println!("gray_to_binary(6) = {}", gray_to_binary_u8(6));
}
