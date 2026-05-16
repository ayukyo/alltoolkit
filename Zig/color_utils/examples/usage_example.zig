const std = @import("std");
const color_utils = @import("color_utils");

pub fn main() !void {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    const allocator = gpa.allocator();
    defer _ = gpa.deinit();

    const stdout = std.io.getStdOut().writer();

    try stdout.print("\n=== Color Utils Demo ===\n\n", .{});

    // Parse hex colors
    try stdout.print("Parsing Hex Colors:\n", .{});
    
    const hex_rgb = color_utils.parseHex("#FF5733") catch return;
    const rgb = hex_rgb.rgb;
    try stdout.print("  #FF5733 -> RGB({}, {}, {})\n", .{ rgb.r, rgb.g, rgb.b });
    
    const hex_rgba = color_utils.parseHex("#FF573380") catch return;
    const rgba = hex_rgba.rgba;
    try stdout.print("  #FF573380 -> RGBA({}, {}, {}, {})\n", .{ rgba.r, rgba.g, rgba.b, rgba.a });

    // RGB to Hex
    try stdout.print("\nRGB to Hex:\n", .{});
    const my_rgb = color_utils.Rgb.init(100, 200, 50);
    const hex_str = try color_utils.rgbToHex(allocator, my_rgb);
    defer allocator.free(hex_str);
    try stdout.print("  RGB({}, {}, {}) -> {s}\n", .{ my_rgb.r, my_rgb.g, my_rgb.b, hex_str });

    // HSL conversion
    try stdout.print("\nHSL Conversion:\n", .{});
    const red = color_utils.Rgb.init(255, 0, 0);
    const hsl = color_utils.rgbToHsl(red);
    try stdout.print("  RGB({}, {}, {}) -> HSL({}, {}%, {}%)\n", .{ red.r, red.g, red.b, hsl.h, hsl.s, hsl.l });
    
    const back_rgb = color_utils.hslToRgb(hsl);
    try stdout.print("  HSL({}, {}%, {}%) -> RGB({}, {}, {})\n", .{ hsl.h, hsl.s, hsl.l, back_rgb.r, back_rgb.g, back_rgb.b });

    // HSV conversion
    try stdout.print("\nHSV Conversion:\n", .{});
    const hsv = color_utils.rgbToHsv(red);
    try stdout.print("  RGB({}, {}, {}) -> HSV({}, {}%, {}%)\n", .{ red.r, red.g, red.b, hsv.h, hsv.s, hsv.v });

    // Color manipulation
    try stdout.print("\nColor Manipulation:\n", .{});
    
    const base_color = color_utils.Rgb.init(128, 128, 128);
    const lighter = color_utils.lighten(base_color, 30);
    try stdout.print("  Lighten({}, {}, {}, 30%) -> RGB({}, {}, {})\n", .{ 
        base_color.r, base_color.g, base_color.b, lighter.r, lighter.g, lighter.b 
    });
    
    const darker = color_utils.darken(base_color, 30);
    try stdout.print("  Darken({}, {}, {}, 30%) -> RGB({}, {}, {})\n", .{ 
        base_color.r, base_color.g, base_color.b, darker.r, darker.g, darker.b 
    });
    
    const inverted = color_utils.invert(base_color);
    try stdout.print("  Invert({}, {}, {}) -> RGB({}, {}, {})\n", .{ 
        base_color.r, base_color.g, base_color.b, inverted.r, inverted.g, inverted.b 
    });
    
    const gray = color_utils.grayscale(base_color);
    try stdout.print("  Grayscale({}, {}, {}) -> RGB({}, {}, {})\n", .{ 
        base_color.r, base_color.g, base_color.b, gray.r, gray.g, gray.b 
    });

    // Color mixing
    try stdout.print("\nColor Mixing:\n", .{});
    const color1 = color_utils.Rgb.init(0, 0, 0);
    const color2 = color_utils.Rgb.init(255, 255, 255);
    const mixed = color_utils.mix(color1, color2, 50);
    try stdout.print("  Mix(black, white, 50%) -> RGB({}, {}, {})\n", .{ mixed.r, mixed.g, mixed.b });

    // Complementary color
    try stdout.print("\nComplementary Color:\n", .{});
    const comp = color_utils.complement(red);
    try stdout.print("  Complement of red -> RGB({}, {}, {})\n", .{ comp.r, comp.g, comp.b });

    // Color schemes
    try stdout.print("\nColor Schemes:\n", .{});
    
    const tri_colors = color_utils.triadic(red);
    try stdout.print("  Triadic from red:\n", .{});
    for (tri_colors, 0..) |c, i| {
        try stdout.print("    [{}] RGB({}, {}, {})\n", .{ i, c.r, c.g, c.b });
    }
    
    const split_colors = color_utils.splitComplementary(red);
    try stdout.print("  Split-Complementary from red:\n", .{});
    for (split_colors, 0..) |c, i| {
        try stdout.print("    [{}] RGB({}, {}, {})\n", .{ i, c.r, c.g, c.b });
    }

    // Luminance and contrast
    try stdout.print("\nLuminance & Contrast:\n", .{});
    const lum = color_utils.luminance(red);
    try stdout.print("  Luminance of red: {d:.3}\n", .{ lum });
    
    const white = color_utils.Rgb.init(255, 255, 255);
    const contrast = color_utils.contrastRatio(red, white);
    try stdout.print("  Contrast ratio (red, white): {d:.2}:1\n", .{ contrast });
    
    const text_color = color_utils.getContrastingText(red);
    try stdout.print("  Best text color on red: RGB({}, {}, {})\n", .{ text_color.r, text_color.g, text_color.b });

    // Named colors
    try stdout.print("\nNamed Colors:\n", .{});
    
    if (color_utils.namedColor("coral")) |coral| {
        try stdout.print("  coral -> RGB({}, {}, {})\n", .{ coral.r, coral.g, coral.b });
    }
    
    if (color_utils.namedColor("navy")) |navy| {
        try stdout.print("  navy -> RGB({}, {}, {})\n", .{ navy.r, navy.g, navy.b });
    }
    
    const approx_name = try color_utils.getColorName(allocator, color_utils.Rgb.init(255, 0, 0));
    defer allocator.free(approx_name);
    try stdout.print("  RGB(255, 0, 0) is approximately: {s}\n", .{ approx_name });

    // Random colors
    try stdout.print("\nRandom Colors:\n", .{});
    const random1 = color_utils.randomRgb();
    try stdout.print("  Random: RGB({}, {}, {})\n", .{ random1.r, random1.g, random1.b });
    
    const random2 = color_utils.randomRgb();
    const hex2 = try color_utils.rgbToHex(allocator, random2);
    defer allocator.free(hex2);
    try stdout.print("  Random: {s}\n", .{ hex2 });

    try stdout.print("\n=== Demo Complete ===\n", .{});
}