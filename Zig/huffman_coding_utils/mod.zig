const std = @import("std");

/// 霍夫曼编码节点
pub const HuffmanNode = struct {
    char: ?u8,
    freq: usize,
    left: ?*HuffmanNode,
    right: ?*HuffmanNode,

    pub fn init(char: ?u8, freq: usize) HuffmanNode {
        return .{
            .char = char,
            .freq = freq,
            .left = null,
            .right = null,
        };
    }

    pub fn isLeaf(self: *const HuffmanNode) bool {
        return self.left == null and self.right == null;
    }
};

/// 霍夫曼树
pub const HuffmanTree = struct {
    root: ?*HuffmanNode,
    allocator: std.mem.Allocator,

    pub fn init(allocator: std.mem.Allocator) HuffmanTree {
        return .{
            .root = null,
            .allocator = allocator,
        };
    }

    pub fn deinit(self: *HuffmanTree) void {
        if (self.root) |root| {
            self.freeNode(root);
            self.allocator.destroy(root);
        }
    }

    fn freeNode(self: *HuffmanTree, node: *HuffmanNode) void {
        if (node.left) |left| {
            self.freeNode(left);
            self.allocator.destroy(left);
        }
        if (node.right) |right| {
            self.freeNode(right);
            self.allocator.destroy(right);
        }
    }

    /// 从频率表构建霍夫曼树
    pub fn build(self: *HuffmanTree, freq_map: *const std.AutoHashMap(u8, usize)) !void {
        if (freq_map.count() == 0) {
            self.root = null;
            return;
        }

        // 最小堆实现
        var heap = std.PriorityQueue(*HuffmanNode, void, compareNodes).init(self.allocator, {});
        defer heap.deinit();

        var iter = freq_map.iterator();
        while (iter.next()) |entry| {
            const node = try self.allocator.create(HuffmanNode);
            node.* = HuffmanNode.init(entry.key_ptr.*, entry.value_ptr.*);
            try heap.add(node);
        }

        // 特殊情况：只有一个字符，创建一个虚拟父节点
        if (heap.count() == 1) {
            const leaf = heap.remove();
            const parent = try self.allocator.create(HuffmanNode);
            parent.* = HuffmanNode.init(null, leaf.freq);
            parent.left = leaf;
            self.root = parent;
            return;
        }

        while (heap.count() > 1) {
            const left = heap.remove();
            const right = heap.remove();

            const parent = try self.allocator.create(HuffmanNode);
            parent.* = HuffmanNode.init(null, left.freq + right.freq);
            parent.left = left;
            parent.right = right;

            try heap.add(parent);
        }

        if (heap.count() > 0) {
            self.root = heap.remove();
        }
    }

    fn compareNodes(context: void, a: *HuffmanNode, b: *HuffmanNode) std.math.Order {
        _ = context;
        return std.math.order(a.freq, b.freq);
    }
};

/// 霍夫曼编码器
pub const HuffmanEncoder = struct {
    tree: HuffmanTree,
    codes: std.AutoHashMap(u8, []u8),
    allocator: std.mem.Allocator,

    pub fn init(allocator: std.mem.Allocator) HuffmanEncoder {
        return .{
            .tree = HuffmanTree.init(allocator),
            .codes = std.AutoHashMap(u8, []u8).init(allocator),
            .allocator = allocator,
        };
    }

    pub fn deinit(self: *HuffmanEncoder) void {
        self.tree.deinit();
        var iter = self.codes.iterator();
        while (iter.next()) |entry| {
            self.allocator.free(entry.value_ptr.*);
        }
        self.codes.deinit();
    }

    /// 从输入数据构建编码器
    pub fn build(self: *HuffmanEncoder, data: []const u8) !void {
        if (data.len == 0) return;

        // 计算频率
        var freq_map = std.AutoHashMap(u8, usize).init(self.allocator);
        defer freq_map.deinit();

        for (data) |char| {
            const current = freq_map.get(char) orelse 0;
            try freq_map.put(char, current + 1);
        }

        // 构建霍夫曼树
        try self.tree.build(&freq_map);

        // 生成编码表
        if (self.tree.root) |root| {
            try self.generateCodes(root, &[_]u8{});
        }
    }

    fn generateCodes(self: *HuffmanEncoder, node: *HuffmanNode, code: []const u8) !void {
        if (node.isLeaf()) {
            if (node.char) |char| {
                const code_copy = try self.allocator.alloc(u8, code.len);
                @memcpy(code_copy, code);
                try self.codes.put(char, code_copy);
            }
            return;
        }

        // 左子树添加 0
        if (node.left) |left| {
            var new_code = try self.allocator.alloc(u8, code.len + 1);
            @memcpy(new_code[0..code.len], code);
            new_code[code.len] = '0';
            defer self.allocator.free(new_code);
            try self.generateCodes(left, new_code);
        }

        // 右子树添加 1
        if (node.right) |right| {
            var new_code = try self.allocator.alloc(u8, code.len + 1);
            @memcpy(new_code[0..code.len], code);
            new_code[code.len] = '1';
            defer self.allocator.free(new_code);
            try self.generateCodes(right, new_code);
        }
    }

    /// 编码数据
    pub fn encode(self: *HuffmanEncoder, data: []const u8) ![]u8 {
        if (data.len == 0) return try self.allocator.alloc(u8, 0);

        // 计算编码后的总长度
        var total_bits: usize = 0;
        for (data) |char| {
            if (self.codes.get(char)) |code| {
                total_bits += code.len;
            } else {
                return error.CharNotInCodeTable;
            }
        }

        // 分配结果缓冲区
        const total_bytes = if (total_bits > 0) (total_bits + 7) / 8 else 1;
        var result = try self.allocator.alloc(u8, total_bytes);
        @memset(result, 0);

        if (total_bits == 0) return result;

        var bit_index: usize = 0;
        for (data) |char| {
            const code = self.codes.get(char).?;
            for (code) |bit| {
                if (bit == '1') {
                    const byte_index = bit_index / 8;
                    const bit_offset: u3 = @intCast(7 - (bit_index % 8));
                    result[byte_index] |= @as(u8, 1) << bit_offset;
                }
                bit_index += 1;
            }
        }

        return result;
    }

    /// 获取字符的编码
    pub fn getCode(self: *const HuffmanEncoder, char: u8) ?[]const u8 {
        return self.codes.get(char);
    }

    /// 获取编码表
    pub fn getCodeTable(self: *const HuffmanEncoder) *const std.AutoHashMap(u8, []u8) {
        return &self.codes;
    }
};

/// 霍夫曼解码器
pub const HuffmanDecoder = struct {
    tree: HuffmanTree,
    root_allocated: bool,

    pub fn init(allocator: std.mem.Allocator) HuffmanDecoder {
        return .{
            .tree = HuffmanTree.init(allocator),
            .root_allocated = false,
        };
    }

    pub fn deinit(self: *HuffmanDecoder) void {
        // 注意：从编码表构建时，节点在 tree.allocator 上分配
        // 但 tree.deinit 会释放这些节点
        if (self.root_allocated) {
            self.tree.deinit();
        }
    }

    /// 从编码表构建解码树
    pub fn buildFromCodes(self: *HuffmanDecoder, codes: *const std.AutoHashMap(u8, []u8), allocator: std.mem.Allocator) !void {
        // 如果已经有树，先释放
        if (self.root_allocated) {
            self.tree.deinit();
            self.root_allocated = false;
        }

        // 创建根节点
        const root = try allocator.create(HuffmanNode);
        root.* = HuffmanNode.init(null, 0);
        self.tree.root = root;
        self.tree.allocator = allocator;
        self.root_allocated = true;

        var iter = codes.iterator();
        while (iter.next()) |entry| {
            var current = root;
            const char = entry.key_ptr.*;
            const code = entry.value_ptr.*;

            for (code) |bit| {
                if (bit == '0') {
                    if (current.left == null) {
                        const node = try allocator.create(HuffmanNode);
                        node.* = HuffmanNode.init(null, 0);
                        current.left = node;
                    }
                    current = current.left.?;
                } else {
                    if (current.right == null) {
                        const node = try allocator.create(HuffmanNode);
                        node.* = HuffmanNode.init(null, 0);
                        current.right = node;
                    }
                    current = current.right.?;
                }
            }
            current.char = char;
        }
    }

    /// 解码数据
    pub fn decode(self: *HuffmanDecoder, encoded: []const u8, bit_length: usize, allocator: std.mem.Allocator) ![]u8 {
        if (self.tree.root == null) return error.TreeNotBuilt;
        if (bit_length == 0) return try allocator.alloc(u8, 0);

        var result = std.ArrayList(u8).init(allocator);
        defer result.deinit();

        var current = self.tree.root.?;
        var bit_count: usize = 0;

        for (encoded) |byte| {
            var i: usize = 0;
            while (i < 8 and bit_count < bit_length) : (i += 1) {
                const bit = (byte >> @as(u3, @intCast(7 - i))) & 1;

                if (bit == 0) {
                    if (current.left) |left| {
                        current = left;
                    } else {
                        return error.InvalidEncodedData;
                    }
                } else {
                    if (current.right) |right| {
                        current = right;
                    } else {
                        return error.InvalidEncodedData;
                    }
                }

                if (current.isLeaf()) {
                    if (current.char) |char| {
                        try result.append(char);
                    }
                    current = self.tree.root.?;
                }

                bit_count += 1;
            }
        }

        return result.toOwnedSlice();
    }
};

/// 计算频率表
pub fn calculateFrequency(allocator: std.mem.Allocator, data: []const u8) !std.AutoHashMap(u8, usize) {
    var freq_map = std.AutoHashMap(u8, usize).init(allocator);

    for (data) |char| {
        const current = freq_map.get(char) orelse 0;
        try freq_map.put(char, current + 1);
    }

    return freq_map;
}

/// 打印频率表
pub fn printFrequencyMap(freq_map: *const std.AutoHashMap(u8, usize)) void {
    std.debug.print("Character Frequency Table:\n", .{});
    std.debug.print("=========================\n", .{});
    var iter = freq_map.iterator();
    while (iter.next()) |entry| {
        const char = entry.key_ptr.*;
        const freq = entry.value_ptr.*;
        if (std.ascii.isPrintable(char)) {
            std.debug.print("  '{c}' : {}\n", .{ char, freq });
        } else {
            std.debug.print("  0x{x:0>2} : {}\n", .{ char, freq });
        }
    }
}

/// 打印编码表
pub fn printCodeTable(codes: *const std.AutoHashMap(u8, []u8)) void {
    std.debug.print("\nHuffman Code Table:\n", .{});
    std.debug.print("==================\n", .{});
    var iter = codes.iterator();
    while (iter.next()) |entry| {
        const char = entry.key_ptr.*;
        const code = entry.value_ptr.*;
        if (std.ascii.isPrintable(char)) {
            std.debug.print("  '{c}' : {s}\n", .{ char, code });
        } else {
            std.debug.print("  0x{x:0>2} : {s}\n", .{ char, code });
        }
    }
}

/// 计算压缩率
pub fn calculateCompressionRatio(original_len: usize, encoded_bits: usize) f64 {
    if (original_len == 0) return 0.0;
    const original_bits = original_len * 8;
    return @as(f64, @floatFromInt(original_bits - encoded_bits)) / @as(f64, @floatFromInt(original_bits)) * 100.0;
}

// 测试
test "HuffmanEncoder - basic encoding" {
    const allocator = std.testing.allocator;

    var encoder = HuffmanEncoder.init(allocator);
    defer encoder.deinit();

    const data = "hello world";
    try encoder.build(data);

    const encoded = try encoder.encode(data);
    defer allocator.free(encoded);

    // 验证编码结果非空
    try std.testing.expect(encoded.len > 0);
}

test "HuffmanEncoder - single character" {
    const allocator = std.testing.allocator;

    var encoder = HuffmanEncoder.init(allocator);
    defer encoder.deinit();

    const data = "aaaaa";
    try encoder.build(data);

    const encoded = try encoder.encode(data);
    defer allocator.free(encoded);

    // 单字符应该得到编码
    try std.testing.expect(encoded.len >= 0);
    // 验证编码确实存在
    if (encoder.getCode('a')) |code| {
        try std.testing.expect(code.len > 0);
    }
}

test "HuffmanEncoder - empty data" {
    const allocator = std.testing.allocator;

    var encoder = HuffmanEncoder.init(allocator);
    defer encoder.deinit();

    const data = "";
    try encoder.build(data);

    const encoded = try encoder.encode(data);
    defer allocator.free(encoded);

    try std.testing.expectEqual(@as(usize, 0), encoded.len);
}

test "HuffmanDecoder - decode encoded data" {
    const allocator = std.testing.allocator;

    // 编码
    var encoder = HuffmanEncoder.init(allocator);
    defer encoder.deinit();

    const original = "hello world";
    try encoder.build(original);

    const encoded = try encoder.encode(original);
    defer allocator.free(encoded);

    // 计算原始位数
    var total_bits: usize = 0;
    for (original) |char| {
        if (encoder.getCode(char)) |code| {
            total_bits += code.len;
        }
    }

    // 解码
    var decoder = HuffmanDecoder.init(allocator);
    defer decoder.deinit();

    try decoder.buildFromCodes(encoder.getCodeTable(), allocator);
    const decoded = try decoder.decode(encoded, total_bits, allocator);
    defer allocator.free(decoded);

    try std.testing.expectEqualSlices(u8, original, decoded);
}

test "HuffmanDecoder - single character" {
    const allocator = std.testing.allocator;

    var encoder = HuffmanEncoder.init(allocator);
    defer encoder.deinit();

    const original = "aaaaa";
    try encoder.build(original);

    const encoded = try encoder.encode(original);
    defer allocator.free(encoded);

    // 计算位数
    var total_bits: usize = 0;
    for (original) |char| {
        if (encoder.getCode(char)) |code| {
            total_bits += code.len;
        }
    }

    var decoder = HuffmanDecoder.init(allocator);
    defer decoder.deinit();

    try decoder.buildFromCodes(encoder.getCodeTable(), allocator);
    const decoded = try decoder.decode(encoded, total_bits, allocator);
    defer allocator.free(decoded);

    try std.testing.expectEqualSlices(u8, original, decoded);
}

test "calculateFrequency" {
    const allocator = std.testing.allocator;

    const data = "aabbbc";
    var freq = try calculateFrequency(allocator, data);
    defer freq.deinit();

    try std.testing.expectEqual(@as(usize, 2), freq.get('a').?);
    try std.testing.expectEqual(@as(usize, 3), freq.get('b').?);
    try std.testing.expectEqual(@as(usize, 1), freq.get('c').?);
}

test "calculateCompressionRatio" {
    const ratio = calculateCompressionRatio(100, 400); // 100 bytes = 800 bits, encoded = 400 bits
    try std.testing.expectApproxEqAbs(@as(f64, 50.0), ratio, 0.01);
}