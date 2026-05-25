trait BitOps: Copy + Clone {
    fn mask_range(start: u32, end: u32) -> Self;
    fn clear_bit(self, pos: u32) -> Self;
    fn bit_width() -> u32;
}

impl BitOps for u8 {
    fn mask_range(start: u32, end: u32) -> Self {
        if start > end || end >= 8 {
            return 0;
        }
        let len = end - start + 1;
        let mask: u8 = ((1u16 << len) - 1) as u8;
        mask << start
    }
    
    fn clear_bit(self, pos: u32) -> Self {
        if pos >= 8 {
            return self;
        }
        self & !(1 << pos)
    }
    
    fn bit_width() -> u32 { 8 }
}

fn gray_to_binary_u8(gray: u8) -> u8 {
    let mut binary = gray;
    let mut mask = gray >> 1u32;
    println!("Initial: gray={}, binary={}, mask={}", gray, binary, mask);
    let zero = u8::mask_range(0, 0).clear_bit(0);
    println!("zero = {}", zero);
    while mask != zero {
        println!("Loop: binary={}, mask={}", binary, mask);
        binary = binary ^ mask;
        mask = mask >> 1u32;
    }
    println!("Final binary = {}", binary);
    binary
}

fn main() {
    println!("gray_to_binary(1u8) = {}", gray_to_binary_u8(1));
}
