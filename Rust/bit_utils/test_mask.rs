fn mask_range_u8(start: u32, end: u32) -> u8 {
    if start > end || end >= 8 {
        return 0;
    }
    let len = end - start + 1;
    let mask: u8 = ((1u16 << len) - 1) as u8;
    mask << start
}

fn clear_bit_u8(self_val: u8, pos: u32) -> u8 {
    if pos >= 8 {
        return self_val;
    }
    self_val & !(1 << pos)
}

fn main() {
    let m = mask_range_u8(0, 0);
    println!("mask_range(0, 0) = {} (binary: {:08b})", m, m);
    let c = clear_bit_u8(m, 0);
    println!("clear_bit({}, 0) = {} (binary: {:08b})", m, c, c);
    println!("mask_range(0, 0).clear_bit(0) = {}", c);
}
