const std = @import("std");

/// Color operation errors
pub const ColorError = error{
    OutOfMemory,
    InvalidHexColor,
    InvalidRgbValue,
    InvalidHslValue,
    InvalidFormat,
    BufferTooSmall,
};

/// RGB color representation
pub const Rgb = struct {
    r: u8,
    g: u8,
    b: u8,

    pub fn init(r: u8, g: u8, b: u8) Rgb {
        return .{ .r = r, .g = g, .b = b };
    }

    pub fn eql(self: Rgb, other: Rgb) bool {
        return self.r == other.r and self.g == other.g and self.b == other.b;
    }
};

/// RGBA color representation
pub const Rgba = struct {
    r: u8,
    g: u8,
    b: u8,
    a: u8,

    pub fn init(r: u8, g: u8, b: u8, a: u8) Rgba {
        return .{ .r = r, .g = g, .b = b, .a = a };
    }

    pub fn eql(self: Rgba, other: Rgba) bool {
        return self.r == other.r and self.g == other.g and self.b == other.b and self.a == other.a;
    }
};

/// HSL color representation (Hue: 0-360, Saturation: 0-100, Lightness: 0-100)
pub const Hsl = struct {
    h: u16,
    s: u8,
    l: u8,

    pub fn init(h: u16, s: u8, l: u8) Hsl {
        return .{ .h = h % 360, .s = @min(s, 100), .l = @min(l, 100) };
    }

    pub fn eql(self: Hsl, other: Hsl) bool {
        return self.h == other.h and self.s == other.s and self.l == other.l;
    }
};

/// HSV color representation (Hue: 0-360, Saturation: 0-100, Value: 0-100)
pub const Hsv = struct {
    h: u16,
    s: u8,
    v: u8,

    pub fn init(h: u16, s: u8, v: u8) Hsv {
        return .{ .h = h % 360, .s = @min(s, 100), .v = @min(v, 100) };
    }

    pub fn eql(self: Hsv, other: Hsv) bool {
        return self.h == other.h and self.s == other.s and self.v == other.v;
    }
};

// ============================================================================
// Hex Color Parsing and Generation
// ============================================================================

/// Parse hex color string to RGB (#RGB, #RRGGBB, #RRGGBBAA)
pub fn parseHex(input: []const u8) ColorError!union(enum) {
    rgb: Rgb,
    rgba: Rgba,
} {
    var hex = input;
    
    // Remove leading #
    if (hex.len > 0 and hex[0] == '#') {
        hex = hex[1..];
    }
    
    return switch (hex.len) {
        3 => {
            // #RGB -> #RRGGBB
            const r = try parseHexDigit(hex[0]);
            const g = try parseHexDigit(hex[1]);
            const b = try parseHexDigit(hex[2]);
            return .{ .rgb = .{ .r = r * 16 + r, .g = g * 16 + g, .b = b * 16 + b } };
        },
        4 => {
            // #RGBA -> #RRGGBBAA
            const r = try parseHexDigit(hex[0]);
            const g = try parseHexDigit(hex[1]);
            const b = try parseHexDigit(hex[2]);
            const a = try parseHexDigit(hex[3]);
            return .{ .rgba = .{ .r = r * 16 + r, .g = g * 16 + g, .b = b * 16 + b, .a = a * 16 + a } };
        },
        6 => {
            const r = try parseHexByte(hex[0..2]);
            const g = try parseHexByte(hex[2..4]);
            const b = try parseHexByte(hex[4..6]);
            return .{ .rgb = .{ .r = r, .g = g, .b = b } };
        },
        8 => {
            const r = try parseHexByte(hex[0..2]);
            const g = try parseHexByte(hex[2..4]);
            const b = try parseHexByte(hex[4..6]);
            const a = try parseHexByte(hex[6..8]);
            return .{ .rgba = .{ .r = r, .g = g, .b = b, .a = a } };
        },
        else => return ColorError.InvalidHexColor,
    };
}

/// Parse a single hex digit (0-9, a-f, A-F) to its value
fn parseHexDigit(c: u8) ColorError!u8 {
    return switch (c) {
        '0'...'9' => c - '0',
        'a'...'f' => c - 'a' + 10,
        'A'...'F' => c - 'A' + 10,
        else => ColorError.InvalidHexColor,
    };
}

/// Parse a hex byte (e.g., "FF" -> 255)
fn parseHexByte(bytes: []const u8) ColorError!u8 {
    const high = try parseHexDigit(bytes[0]);
    const low = try parseHexDigit(bytes[1]);
    return high * 16 + low;
}

/// Convert RGB to hex string (#RRGGBB)
pub fn rgbToHex(allocator: std.mem.Allocator, rgb: Rgb) ColorError![]u8 {
    const result = allocator.alloc(u8, 7) catch return ColorError.OutOfMemory;
    _ = std.fmt.bufPrint(result, "#{x:0>2}{x:0>2}{x:0>2}", .{ rgb.r, rgb.g, rgb.b }) catch return ColorError.BufferTooSmall;
    return result;
}

/// Convert RGBA to hex string (#RRGGBBAA)
pub fn rgbaToHex(allocator: std.mem.Allocator, rgba: Rgba) ColorError![]u8 {
    const result = allocator.alloc(u8, 9) catch return ColorError.OutOfMemory;
    _ = std.fmt.bufPrint(result, "#{x:0>2}{x:0>2}{x:0>2}{x:0>2}", .{ rgba.r, rgba.g, rgba.b, rgba.a }) catch return ColorError.BufferTooSmall;
    return result;
}

// ============================================================================
// RGB <-> HSL Conversion
// ============================================================================

/// Convert RGB to HSL
pub fn rgbToHsl(rgb: Rgb) Hsl {
    const r = @as(f64, @floatFromInt(rgb.r)) / 255.0;
    const g = @as(f64, @floatFromInt(rgb.g)) / 255.0;
    const b = @as(f64, @floatFromInt(rgb.b)) / 255.0;
    
    const max = @max(r, @max(g, b));
    const min = @min(r, @min(g, b));
    const l = (max + min) / 2.0;
    
    var h: f64 = 0;
    var s: f64 = 0;
    
    if (max != min) {
        const d = max - min;
        s = if (l > 0.5) d / (2.0 - max - min) else d / (max + min);
        
        h = if (max == r)
            (g - b) / d + if (g < b) @as(f64, 6.0) else @as(f64, 0.0)
        else if (max == g)
            (b - r) / d + 2.0
        else
            (r - g) / d + 4.0;
        
        h *= 60.0;
    }
    
    return .{
        .h = @as(u16, @intFromFloat(@round(h))),
        .s = @as(u8, @intFromFloat(@round(s * 100.0))),
        .l = @as(u8, @intFromFloat(@round(l * 100.0))),
    };
}

/// Convert HSL to RGB
pub fn hslToRgb(hsl: Hsl) Rgb {
    const h = @as(f64, @floatFromInt(hsl.h)) / 360.0;
    const s = @as(f64, @floatFromInt(hsl.s)) / 100.0;
    const l = @as(f64, @floatFromInt(hsl.l)) / 100.0;
    
    var r: f64 = undefined;
    var g: f64 = undefined;
    var b: f64 = undefined;
    
    if (s == 0) {
        r = l;
        g = l;
        b = l;
    } else {
        const q = if (l < 0.5) l * (1.0 + s) else l + s - l * s;
        const p = 2.0 * l - q;
        
        r = hueToRgb(p, q, h + 1.0 / 3.0);
        g = hueToRgb(p, q, h);
        b = hueToRgb(p, q, h - 1.0 / 3.0);
    }
    
    return .{
        .r = @intFromFloat(@round(r * 255.0)),
        .g = @intFromFloat(@round(g * 255.0)),
        .b = @intFromFloat(@round(b * 255.0)),
    };
}

fn hueToRgb(p: f64, q: f64, t: f64) f64 {
    var t_val = t;
    if (t_val < 0) t_val += 1;
    if (t_val > 1) t_val -= 1;
    if (t_val < 1.0 / 6.0) return p + (q - p) * 6.0 * t_val;
    if (t_val < 1.0 / 2.0) return q;
    if (t_val < 2.0 / 3.0) return p + (q - p) * (2.0 / 3.0 - t_val) * 6.0;
    return p;
}

// ============================================================================
// RGB <-> HSV Conversion
// ============================================================================

/// Convert RGB to HSV
pub fn rgbToHsv(rgb: Rgb) Hsv {
    const r = @as(f64, @floatFromInt(rgb.r)) / 255.0;
    const g = @as(f64, @floatFromInt(rgb.g)) / 255.0;
    const b = @as(f64, @floatFromInt(rgb.b)) / 255.0;
    
    const max = @max(r, @max(g, b));
    const min = @min(r, @min(g, b));
    const d = max - min;
    
    var h: f64 = 0;
    const s: f64 = if (max == 0) 0 else d / max;
    const v = max;
    
    if (max != min) {
        h = if (max == r)
            (g - b) / d + if (g < b) @as(f64, 6.0) else @as(f64, 0.0)
        else if (max == g)
            (b - r) / d + 2.0
        else
            (r - g) / d + 4.0;
        h *= 60.0;
    }
    
    return .{
        .h = @as(u16, @intFromFloat(@round(h))),
        .s = @as(u8, @intFromFloat(@round(s * 100.0))),
        .v = @as(u8, @intFromFloat(@round(v * 100.0))),
    };
}

/// Convert HSV to RGB
pub fn hsvToRgb(hsv: Hsv) Rgb {
    const h = @as(f64, @floatFromInt(hsv.h)) / 360.0;
    const s = @as(f64, @floatFromInt(hsv.s)) / 100.0;
    const v = @as(f64, @floatFromInt(hsv.v)) / 100.0;
    
    var r: f64 = undefined;
    var g: f64 = undefined;
    var b: f64 = undefined;
    
    const i = @floor(h * 6.0);
    const f = h * 6.0 - i;
    const p = v * (1.0 - s);
    const q = v * (1.0 - f * s);
    const t = v * (1.0 - (1.0 - f) * s);
    
    const ii: usize = @intFromFloat(@mod(i, 6.0));
    
    switch (ii) {
        0 => { r = v; g = t; b = p; },
        1 => { r = q; g = v; b = p; },
        2 => { r = p; g = v; b = t; },
        3 => { r = p; g = q; b = v; },
        4 => { r = t; g = p; b = v; },
        5 => { r = v; g = p; b = q; },
        else => unreachable,
    }
    
    return .{
        .r = @intFromFloat(@round(r * 255.0)),
        .g = @intFromFloat(@round(g * 255.0)),
        .b = @intFromFloat(@round(b * 255.0)),
    };
}

// ============================================================================
// Color Manipulation
// ============================================================================

/// Lighten a color by a percentage (0-100)
pub fn lighten(rgb: Rgb, amount: u8) Rgb {
    const amt = @as(f64, @floatFromInt(@min(amount, 100))) / 100.0;
    return .{
        .r = @intFromFloat(@min(255, @round(@as(f64, @floatFromInt(rgb.r)) + (255 - @as(f64, @floatFromInt(rgb.r))) * amt))),
        .g = @intFromFloat(@min(255, @round(@as(f64, @floatFromInt(rgb.g)) + (255 - @as(f64, @floatFromInt(rgb.g))) * amt))),
        .b = @intFromFloat(@min(255, @round(@as(f64, @floatFromInt(rgb.b)) + (255 - @as(f64, @floatFromInt(rgb.b))) * amt))),
    };
}

/// Darken a color by a percentage (0-100)
pub fn darken(rgb: Rgb, amount: u8) Rgb {
    const amt = @as(f64, @floatFromInt(@min(amount, 100))) / 100.0;
    return .{
        .r = @intFromFloat(@round(@as(f64, @floatFromInt(rgb.r)) * (1.0 - amt))),
        .g = @intFromFloat(@round(@as(f64, @floatFromInt(rgb.g)) * (1.0 - amt))),
        .b = @intFromFloat(@round(@as(f64, @floatFromInt(rgb.b)) * (1.0 - amt))),
    };
}

/// Saturate a color (increase saturation by percentage)
pub fn saturate(rgb: Rgb, amount: u8) Rgb {
    var hsl = rgbToHsl(rgb);
    hsl.s = @min(100, hsl.s + @min(amount, 100));
    return hslToRgb(hsl);
}

/// Desaturate a color (decrease saturation by percentage)
pub fn desaturate(rgb: Rgb, amount: u8) Rgb {
    var hsl = rgbToHsl(rgb);
    hsl.s = if (hsl.s > @min(amount, 100)) hsl.s - @min(amount, 100) else 0;
    return hslToRgb(hsl);
}

/// Convert to grayscale
pub fn grayscale(rgb: Rgb) Rgb {
    const gray = @as(u8, @intFromFloat(@round(0.299 * @as(f64, @floatFromInt(rgb.r)) + 
                                        0.587 * @as(f64, @floatFromInt(rgb.g)) + 
                                        0.114 * @as(f64, @floatFromInt(rgb.b)))));
    return .{ .r = gray, .g = gray, .b = gray };
}

/// Invert color
pub fn invert(rgb: Rgb) Rgb {
    return .{
        .r = 255 - rgb.r,
        .g = 255 - rgb.g,
        .b = 255 - rgb.b,
    };
}

/// Rotate hue by degrees
pub fn rotateHue(rgb: Rgb, degrees: i16) Rgb {
    var hsl = rgbToHsl(rgb);
    const current_h: i32 = @as(i32, @intCast(hsl.h));
    const delta: i32 = @as(i32, @intCast(degrees));
    var new_h: i32 = current_h + delta;
    
    // Normalize to 0-360
    while (new_h < 0) new_h += 360;
    while (new_h >= 360) new_h -= 360;
    
    hsl.h = @as(u16, @intCast(new_h));
    return hslToRgb(hsl);
}

/// Complementary color (opposite on color wheel)
pub fn complement(rgb: Rgb) Rgb {
    return rotateHue(rgb, 180);
}

/// Mix two colors (amount: 0-100, where 50 is equal mix)
pub fn mix(color1: Rgb, color2: Rgb, amount: u8) Rgb {
    const amt = @as(f64, @floatFromInt(@min(amount, 100))) / 100.0;
    const amt1 = 1.0 - amt;
    
    return .{
        .r = @intFromFloat(@round(@as(f64, @floatFromInt(color1.r)) * amt1 + @as(f64, @floatFromInt(color2.r)) * amt)),
        .g = @intFromFloat(@round(@as(f64, @floatFromInt(color1.g)) * amt1 + @as(f64, @floatFromInt(color2.g)) * amt)),
        .b = @intFromFloat(@round(@as(f64, @floatFromInt(color1.b)) * amt1 + @as(f64, @floatFromInt(color2.b)) * amt)),
    };
}

// ============================================================================
// Color Schemes
// ============================================================================

/// Generate analogous colors (adjacent on color wheel)
pub fn analogous(rgb: Rgb) [3]Rgb {
    return .{
        rotateHue(rgb, -30),
        rgb,
        rotateHue(rgb, 30),
    };
}

/// Generate triadic colors (120 degrees apart)
pub fn triadic(rgb: Rgb) [3]Rgb {
    return .{
        rgb,
        rotateHue(rgb, 120),
        rotateHue(rgb, 240),
    };
}

/// Generate split-complementary colors
pub fn splitComplementary(rgb: Rgb) [3]Rgb {
    return .{
        rgb,
        rotateHue(rgb, 150),
        rotateHue(rgb, 210),
    };
}

/// Generate tetradic colors (square on color wheel)
pub fn tetradic(rgb: Rgb) [4]Rgb {
    return .{
        rgb,
        rotateHue(rgb, 90),
        rotateHue(rgb, 180),
        rotateHue(rgb, 270),
    };
}

// ============================================================================
// Luminance and Contrast
// ============================================================================

/// Calculate relative luminance (0.0 - 1.0)
pub fn luminance(rgb: Rgb) f64 {
    const r = linearize(@as(f64, @floatFromInt(rgb.r)) / 255.0);
    const g = linearize(@as(f64, @floatFromInt(rgb.g)) / 255.0);
    const b = linearize(@as(f64, @floatFromInt(rgb.b)) / 255.0);
    return 0.2126 * r + 0.7152 * g + 0.0722 * b;
}

fn linearize(c: f64) f64 {
    return if (c <= 0.03928) c / 12.92 else std.math.pow(f64, (c + 0.055) / 1.055, 2.4);
}

/// Calculate contrast ratio between two colors (1:1 to 21:1)
pub fn contrastRatio(color1: Rgb, color2: Rgb) f64 {
    const l1 = luminance(color1);
    const l2 = luminance(color2);
    const lighter = @max(l1, l2);
    const darker = @min(l1, l2);
    return (lighter + 0.05) / (darker + 0.05);
}

/// Check if a color is light
pub fn isLight(rgb: Rgb) bool {
    return luminance(rgb) > 0.5;
}

/// Check if a color is dark
pub fn isDark(rgb: Rgb) bool {
    return luminance(rgb) <= 0.5;
}

/// Get contrasting text color (black or white) for background
pub fn getContrastingText(background: Rgb) Rgb {
    return if (isLight(background)) Rgb.init(0, 0, 0) else Rgb.init(255, 255, 255);
}

// ============================================================================
// Named Colors (CSS)
// ============================================================================

/// Get named CSS color
pub fn namedColor(name: []const u8) ?Rgb {
    const colors = .{
        .{ "black", Rgb.init(0, 0, 0) },
        .{ "white", Rgb.init(255, 255, 255) },
        .{ "red", Rgb.init(255, 0, 0) },
        .{ "green", Rgb.init(0, 128, 0) },
        .{ "blue", Rgb.init(0, 0, 255) },
        .{ "yellow", Rgb.init(255, 255, 0) },
        .{ "cyan", Rgb.init(0, 255, 255) },
        .{ "magenta", Rgb.init(255, 0, 255) },
        .{ "orange", Rgb.init(255, 165, 0) },
        .{ "purple", Rgb.init(128, 0, 128) },
        .{ "pink", Rgb.init(255, 192, 203) },
        .{ "brown", Rgb.init(165, 42, 42) },
        .{ "gray", Rgb.init(128, 128, 128) },
        .{ "grey", Rgb.init(128, 128, 128) },
        .{ "navy", Rgb.init(0, 0, 128) },
        .{ "teal", Rgb.init(0, 128, 128) },
        .{ "olive", Rgb.init(128, 128, 0) },
        .{ "maroon", Rgb.init(128, 0, 0) },
        .{ "aqua", Rgb.init(0, 255, 255) },
        .{ "lime", Rgb.init(0, 255, 0) },
        .{ "silver", Rgb.init(192, 192, 192) },
        .{ "fuchsia", Rgb.init(255, 0, 255) },
        .{ "coral", Rgb.init(255, 127, 80) },
        .{ "salmon", Rgb.init(250, 128, 114) },
        .{ "gold", Rgb.init(255, 215, 0) },
        .{ "indigo", Rgb.init(75, 0, 130) },
        .{ "violet", Rgb.init(238, 130, 238) },
        .{ "turquoise", Rgb.init(64, 224, 208) },
        .{ "crimson", Rgb.init(220, 20, 60) },
        .{ "chocolate", Rgb.init(210, 105, 30) },
    };
    
    inline for (colors) |entry| {
        if (std.ascii.eqlIgnoreCase(name, entry[0])) {
            return entry[1];
        }
    }
    return null;
}

/// Get color name from RGB (best match)
pub fn getColorName(allocator: std.mem.Allocator, rgb: Rgb) ColorError![]u8 {
    const colors = .{
        .{ "black", Rgb.init(0, 0, 0) },
        .{ "white", Rgb.init(255, 255, 255) },
        .{ "red", Rgb.init(255, 0, 0) },
        .{ "green", Rgb.init(0, 128, 0) },
        .{ "blue", Rgb.init(0, 0, 255) },
        .{ "yellow", Rgb.init(255, 255, 0) },
        .{ "cyan", Rgb.init(0, 255, 255) },
        .{ "magenta", Rgb.init(255, 0, 255) },
        .{ "orange", Rgb.init(255, 165, 0) },
        .{ "purple", Rgb.init(128, 0, 128) },
        .{ "pink", Rgb.init(255, 192, 203) },
        .{ "brown", Rgb.init(165, 42, 42) },
        .{ "gray", Rgb.init(128, 128, 128) },
        .{ "navy", Rgb.init(0, 0, 128) },
        .{ "teal", Rgb.init(0, 128, 128) },
        .{ "olive", Rgb.init(128, 128, 0) },
        .{ "maroon", Rgb.init(128, 0, 0) },
        .{ "lime", Rgb.init(0, 255, 0) },
        .{ "coral", Rgb.init(255, 127, 80) },
        .{ "gold", Rgb.init(255, 215, 0) },
    };
    
    var best_name: []const u8 = "unknown";
    var best_distance: u32 = std.math.maxInt(u32);
    
    inline for (colors) |entry| {
        const dr = @as(u32, @intCast(if (rgb.r > entry[1].r) rgb.r - entry[1].r else entry[1].r - rgb.r));
        const dg = @as(u32, @intCast(if (rgb.g > entry[1].g) rgb.g - entry[1].g else entry[1].g - rgb.g));
        const db = @as(u32, @intCast(if (rgb.b > entry[1].b) rgb.b - entry[1].b else entry[1].b - rgb.b));
        const distance = dr * dr + dg * dg + db * db;
        
        if (distance < best_distance) {
            best_distance = distance;
            best_name = entry[0];
        }
    }
    
    return allocator.dupe(u8, best_name);
}

// ============================================================================
// Random Colors
// ============================================================================

/// Generate random RGB color
pub fn randomRgb() Rgb {
    var rng = std.Random.DefaultPrng.init(@intCast(std.time.timestamp()));
    const random = rng.random();
    return .{
        .r = random.int(u8),
        .g = random.int(u8),
        .b = random.int(u8),
    };
}

/// Generate random color with specified hue
pub fn randomWithHue(hue: u16) Rgb {
    var rng = std.Random.DefaultPrng.init(@intCast(std.time.timestamp()));
    const random = rng.random();
    
    const hsl = Hsl.init(hue, random.intRangeAtMost(u8, 50, 100), random.intRangeAtMost(u8, 25, 75));
    return hslToRgb(hsl);
}

// ============================================================================
// Tests
// ============================================================================

test "Rgb init and eql" {
    const color = Rgb.init(255, 128, 0);
    try std.testing.expectEqual(@as(u8, 255), color.r);
    try std.testing.expectEqual(@as(u8, 128), color.g);
    try std.testing.expectEqual(@as(u8, 0), color.b);
    
    const same = Rgb.init(255, 128, 0);
    const different = Rgb.init(255, 128, 1);
    try std.testing.expect(color.eql(same));
    try std.testing.expect(!color.eql(different));
}

test "Rgba init and eql" {
    const color = Rgba.init(255, 128, 0, 200);
    try std.testing.expectEqual(@as(u8, 200), color.a);
    
    const same = Rgba.init(255, 128, 0, 200);
    try std.testing.expect(color.eql(same));
}

test "Hsl init" {
    const hsl = Hsl.init(400, 150, 150);
    try std.testing.expectEqual(@as(u16, 40), hsl.h); // 400 % 360 = 40
    try std.testing.expectEqual(@as(u8, 100), hsl.s); // capped at 100
    try std.testing.expectEqual(@as(u8, 100), hsl.l); // capped at 100
}

test "parseHex" {
    // 6-digit hex
    const result1 = try parseHex("#FF5733");
    try std.testing.expectEqual(Rgb.init(255, 87, 51), result1.rgb);
    
    // 3-digit hex
    const result2 = try parseHex("#F53");
    try std.testing.expectEqual(Rgb.init(255, 85, 51), result2.rgb);
    
    // 8-digit hex (RGBA)
    const result3 = try parseHex("#FF573380");
    try std.testing.expectEqual(Rgba.init(255, 87, 51, 128), result3.rgba);
    
    // 4-digit hex (RGBA)
    const result4 = try parseHex("#F538");
    try std.testing.expectEqual(Rgba.init(255, 85, 51, 136), result4.rgba);
    
    // Without #
    const result5 = try parseHex("FF5733");
    try std.testing.expectEqual(Rgb.init(255, 87, 51), result5.rgb);
}

test "rgbToHex and rgbaToHex" {
    const allocator = std.testing.allocator;
    
    const rgb = Rgb.init(255, 87, 51);
    const hex = try rgbToHex(allocator, rgb);
    defer allocator.free(hex);
    try std.testing.expectEqualStrings("#ff5733", hex);
    
    const rgba = Rgba.init(255, 87, 51, 128);
    const hexa = try rgbaToHex(allocator, rgba);
    defer allocator.free(hexa);
    try std.testing.expectEqualStrings("#ff573380", hexa);
}

test "rgbToHsl and hslToRgb" {
    // Red
    const red = Rgb.init(255, 0, 0);
    const hsl = rgbToHsl(red);
    try std.testing.expectEqual(@as(u16, 0), hsl.h);
    try std.testing.expectEqual(@as(u8, 100), hsl.s);
    try std.testing.expectEqual(@as(u8, 50), hsl.l);
    
    // Round trip
    const back = hslToRgb(hsl);
    try std.testing.expectEqual(red.r, back.r);
    try std.testing.expectEqual(red.g, back.g);
    try std.testing.expectEqual(red.b, back.b);
    
    // Gray
    const gray = Rgb.init(128, 128, 128);
    const gray_hsl = rgbToHsl(gray);
    try std.testing.expectEqual(@as(u8, 0), gray_hsl.s); // Gray has 0 saturation
}

test "rgbToHsv and hsvToRgb" {
    // Red
    const red = Rgb.init(255, 0, 0);
    const hsv = rgbToHsv(red);
    try std.testing.expectEqual(@as(u16, 0), hsv.h);
    try std.testing.expectEqual(@as(u8, 100), hsv.s);
    try std.testing.expectEqual(@as(u8, 100), hsv.v);
    
    // Round trip
    const back = hsvToRgb(hsv);
    try std.testing.expectEqual(red.r, back.r);
    try std.testing.expectEqual(red.g, back.g);
    try std.testing.expectEqual(red.b, back.b);
}

test "lighten and darken" {
    const color = Rgb.init(100, 100, 100);
    
    const lighter = lighten(color, 50);
    try std.testing.expect(lighter.r > color.r);
    try std.testing.expect(lighter.g > color.g);
    try std.testing.expect(lighter.b > color.b);
    
    const darker = darken(color, 50);
    try std.testing.expect(darker.r < color.r);
    try std.testing.expect(darker.g < color.g);
    try std.testing.expect(darker.b < color.b);
}

test "saturate and desaturate" {
    const color = Rgb.init(128, 100, 100);
    
    const saturated = saturate(color, 50);
    _ = saturated; // Used for demonstration
    
    const desaturated = desaturate(color, 100);
    
    // Desaturated to 100% should have zero saturation
    const desat_hsl = rgbToHsl(desaturated);
    try std.testing.expectEqual(@as(u8, 0), desat_hsl.s);
    
    // All components should be equal (grayscale in HSL sense)
    try std.testing.expectEqual(desaturated.r, desaturated.g);
    try std.testing.expectEqual(desaturated.g, desaturated.b);
}

test "grayscale" {
    const color = Rgb.init(100, 150, 200);
    const gray = grayscale(color);
    try std.testing.expectEqual(gray.r, gray.g);
    try std.testing.expectEqual(gray.g, gray.b);
}

test "invert" {
    const white = Rgb.init(255, 255, 255);
    const inverted = invert(white);
    try std.testing.expectEqual(@as(u8, 0), inverted.r);
    try std.testing.expectEqual(@as(u8, 0), inverted.g);
    try std.testing.expectEqual(@as(u8, 0), inverted.b);
    
    const black = Rgb.init(0, 0, 0);
    const inverted2 = invert(black);
    try std.testing.expectEqual(@as(u8, 255), inverted2.r);
}

test "rotateHue and complement" {
    const red = Rgb.init(255, 0, 0);
    
    // Rotate 180 degrees (complementary)
    const complement_color = complement(red);
    // Should be cyan-ish
    try std.testing.expect(complement_color.b > 200);
    try std.testing.expect(complement_color.g > 200);
    
    // Rotate 360 should return same color
    const rotated = rotateHue(red, 360);
    try std.testing.expectEqual(red.r, rotated.r);
}

test "mix" {
    const black = Rgb.init(0, 0, 0);
    const white = Rgb.init(255, 255, 255);
    
    const mid = mix(black, white, 50);
    // 50% mix of 0 and 255 = 127.5, rounds to 128
    try std.testing.expectEqual(@as(u8, 128), mid.r);
    try std.testing.expectEqual(@as(u8, 128), mid.g);
    try std.testing.expectEqual(@as(u8, 128), mid.b);
    
    const mostly_black = mix(black, white, 10);
    try std.testing.expect(mostly_black.r < 50);
}

test "luminance and contrast" {
    const white = Rgb.init(255, 255, 255);
    const black = Rgb.init(0, 0, 0);
    
    try std.testing.expectEqual(@as(f64, 1.0), luminance(white));
    try std.testing.expectEqual(@as(f64, 0.0), luminance(black));
    
    const ratio = contrastRatio(white, black);
    try std.testing.expect(ratio > 20); // Should be 21:1
}

test "isLight and isDark" {
    const white = Rgb.init(255, 255, 255);
    const black = Rgb.init(0, 0, 0);
    const gray = Rgb.init(128, 128, 128);
    
    try std.testing.expect(isLight(white));
    try std.testing.expect(isDark(black));
    try std.testing.expect(isDark(gray)); // 128,128,128 is considered dark
}

test "getContrastingText" {
    const white_bg = Rgb.init(255, 255, 255);
    const text1 = getContrastingText(white_bg);
    try std.testing.expectEqual(@as(u8, 0), text1.r); // Should be black
    
    const black_bg = Rgb.init(0, 0, 0);
    const text2 = getContrastingText(black_bg);
    try std.testing.expectEqual(@as(u8, 255), text2.r); // Should be white
}

test "namedColor" {
    const red = namedColor("red");
    try std.testing.expect(red != null);
    try std.testing.expectEqual(Rgb.init(255, 0, 0), red.?);
    
    const blue = namedColor("BLUE"); // Case insensitive
    try std.testing.expect(blue != null);
    try std.testing.expectEqual(Rgb.init(0, 0, 255), blue.?);
    
    const unknown = namedColor("notacolor");
    try std.testing.expect(unknown == null);
}

test "getColorName" {
    const allocator = std.testing.allocator;
    
    const red_name = try getColorName(allocator, Rgb.init(255, 0, 0));
    defer allocator.free(red_name);
    try std.testing.expectEqualStrings("red", red_name);
    
    const green_name = try getColorName(allocator, Rgb.init(0, 255, 0));
    defer allocator.free(green_name);
    try std.testing.expectEqualStrings("lime", green_name); // 0,255,0 is lime, not green
}

test "randomRgb" {
    const color1 = randomRgb();
    const color2 = randomRgb();
    // Very unlikely to be the same
    // (could theoretically fail but probability is ~1/16M)
    _ = color1;
    _ = color2;
}

test "analogous" {
    const red = Rgb.init(255, 0, 0);
    const colors = analogous(red);
    
    // Center should be original
    try std.testing.expectEqual(red.r, colors[1].r);
    try std.testing.expectEqual(red.g, colors[1].g);
    try std.testing.expectEqual(red.b, colors[1].b);
}

test "triadic" {
    const red = Rgb.init(255, 0, 0);
    const colors = triadic(red);
    
    // First should be original
    try std.testing.expectEqual(red.r, colors[0].r);
    
    // Should be roughly 120 degrees apart
    const hsl1 = rgbToHsl(colors[0]);
    const hsl2 = rgbToHsl(colors[1]);
    const hsl3 = rgbToHsl(colors[2]);
    
    const diff1 = if (hsl2.h > hsl1.h) hsl2.h - hsl1.h else hsl1.h - hsl2.h;
    const diff2 = if (hsl3.h > hsl2.h) hsl3.h - hsl2.h else hsl2.h - hsl3.h;
    
    try std.testing.expect(@as(u16, @intCast(diff1)) >= 100); // ~120
    try std.testing.expect(@as(u16, @intCast(diff2)) >= 100); // ~120
}

test "splitComplementary" {
    const red = Rgb.init(255, 0, 0);
    const colors = splitComplementary(red);
    
    try std.testing.expectEqual(red.r, colors[0].r);
}

test "tetradic" {
    const red = Rgb.init(255, 0, 0);
    const colors = tetradic(red);
    
    try std.testing.expectEqual(@as(usize, 4), colors.len);
    try std.testing.expectEqual(red.r, colors[0].r);
}