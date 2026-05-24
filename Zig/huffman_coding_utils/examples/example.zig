const std = @import("std");
const huffman = @import("../mod.zig");

pub fn main() !void {
    // 使用页面分配器作为通用分配器
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer _ = gpa.deinit();
    const allocator = gpa.allocator();

    std.debug.print("=== 霍夫曼编码工具示例 ===\n\n", .{});

    // 示例1: 基本编码
    try basicEncodingExample(allocator);
    std.debug.print("\n", .{});

    // 示例2: 完整编码解码
    try fullEncodeDecodeExample(allocator);
    std.debug.print("\n", .{});

    // 示例3: 压缩统计
    try compressionStatsExample(allocator);
    std.debug.print("\n", .{});

    // 示例4: 二进制数据处理
    try binaryDataExample(allocator);
}

fn basicEncodingExample(allocator: std.mem.Allocator) !void {
    std.debug.print("=== 示例1: 基本编码 ===\n", .{});

    var encoder = huffman.HuffmanEncoder.init(allocator);
    defer encoder.deinit();

    const text = "hello world";
    std.debug.print("原始文本: \"{s}\"\n", .{text});

    // 构建霍夫曼编码
    try encoder.build(text);

    // 打印频率表
    var freq = try huffman.calculateFrequency(allocator, text);
    defer freq.deinit();
    huffman.printFrequencyMap(&freq);

    // 打印编码表
    huffman.printCodeTable(encoder.getCodeTable());
}

fn fullEncodeDecodeExample(allocator: std.mem.Allocator) !void {
    std.debug.print("=== 示例2: 完整编码解码流程 ===\n", .{});

    var encoder = huffman.HuffmanEncoder.init(allocator);
    defer encoder.deinit();

    const text = "the quick brown fox jumps over the lazy dog";
    std.debug.print("原始文本: \"{s}\"\n", .{text});
    std.debug.print("原始长度: {} 字节 ({} 位)\n", .{ text.len, text.len * 8 });

    // 编码
    try encoder.build(text);
    const encoded = try encoder.encode(text);
    defer allocator.free(encoded);

    // 计算总位数
    var total_bits: usize = 0;
    for (text) |char| {
        if (encoder.getCode(char)) |code| {
            total_bits += code.len;
        }
    }

    std.debug.print("编码后长度: {} 位 (约 {} 字节)\n", .{ total_bits, (total_bits + 7) / 8 });

    // 解码
    var decoder = huffman.HuffmanDecoder.init(allocator);
    defer decoder.deinit();

    try decoder.buildFromCodes(encoder.getCodeTable(), allocator);
    const decoded = try decoder.decode(encoded, total_bits, allocator);
    defer allocator.free(decoded);

    std.debug.print("解码文本: \"{s}\"\n", .{decoded});
    std.debug.print("解码成功: {}\n", .{std.mem.eql(u8, text, decoded)});
}

fn compressionStatsExample(allocator: std.mem.Allocator) !void {
    std.debug.print("=== 示例3: 压缩统计 ===\n", .{});

    const test_cases = [_][]const u8{
        "aaaaaaaab",
        "abcabcabc",
        "aaaaaaaaaa",
        "the quick brown fox",
        "aaaaabbbbbcccccddddd",
    };

    for (test_cases) |text| {
        var encoder = huffman.HuffmanEncoder.init(allocator);
        defer encoder.deinit();

        try encoder.build(text);
        const encoded = try encoder.encode(text);
        defer allocator.free(encoded);

        // 计算总位数
        var total_bits: usize = 0;
        for (text) |char| {
            if (encoder.getCode(char)) |code| {
                total_bits += code.len;
            }
        }

        const ratio = huffman.calculateCompressionRatio(text.len, total_bits);

        std.debug.print("\n文本: \"{s}\"", .{text});
        std.debug.print("\n  原始: {} 字节", .{text.len});
        std.debug.print("\n  编码: {} 位 ({} 字节)", .{ total_bits, (total_bits + 7) / 8 });
        std.debug.print("\n  压缩率: {d:.1}%\n", .{ratio});
    }
}

fn binaryDataExample(allocator: std.mem.Allocator) !void {
    std.debug.print("=== 示例4: 二进制数据处理 ===\n", .{});

    // 模拟二进制数据
    const data = [_]u8{ 0x00, 0x01, 0x00, 0x01, 0x02, 0x00, 0x01, 0x00, 0x00, 0x02 };

    std.debug.print("原始数据: ", .{});
    for (data) |byte| {
        std.debug.print("0x{x:0>2} ", .{byte});
    }
    std.debug.print("\n", .{});

    var encoder = huffman.HuffmanEncoder.init(allocator);
    defer encoder.deinit();

    try encoder.build(&data);
    const encoded = try encoder.encode(&data);
    defer allocator.free(encoded);

    // 计算总位数
    var total_bits: usize = 0;
    for (data) |byte| {
        if (encoder.getCode(byte)) |code| {
            total_bits += code.len;
        }
    }

    std.debug.print("编码后: {} 位 ({} 字节)\n", .{ total_bits, (total_bits + 7) / 8 });
    std.debug.print("压缩率: {d:.1}%\n", .{huffman.calculateCompressionRatio(data.len, total_bits)});

    // 打印编码表
    huffman.printCodeTable(encoder.getCodeTable());
}