const std = @import("std");
const humanize = @import("humanize_utils");

pub fn main() !void {
    const allocator = std.heap.page_allocator;

    std.debug.print("\n=== Humanize Utils Examples ===\n\n", .{});

    // ==================== File Size Formatting ====================
    std.debug.print("--- File Size Formatting ---\n", .{});
    
    {
        const size1 = humanize.formatBytes(allocator, 500, 2, false) catch return;
        defer allocator.free(size1);
        std.debug.print("500 bytes: {s}\n", .{size1});
    }
    
    {
        const size2 = humanize.formatBytes(allocator, 1024, 2, false) catch return;
        defer allocator.free(size2);
        std.debug.print("1024 bytes: {s}\n", .{size2});
    }
    
    {
        const size3 = humanize.formatBytes(allocator, 1024, 2, true) catch return;
        defer allocator.free(size3);
        std.debug.print("1024 bytes (binary): {s}\n", .{size3});
    }
    
    {
        const size4 = humanize.formatBytes(allocator, 1536000, 2, false) catch return;
        defer allocator.free(size4);
        std.debug.print("1536000 bytes: {s}\n", .{size4});
    }
    
    {
        const size5 = humanize.formatBytes(allocator, 1073741824, 2, true) catch return;
        defer allocator.free(size5);
        std.debug.print("1 GiB: {s}\n", .{size5});
    }
    
    {
        const size6 = humanize.formatBytes(allocator, 1000000000000, 2, false) catch return;
        defer allocator.free(size6);
        std.debug.print("1 TB: {s}\n", .{size6});
    }

    // ==================== Parse Size ====================
    std.debug.print("\n--- Parse Size ---\n", .{});
    
    const parsed1 = humanize.parseSize("1KB") catch return;
    std.debug.print("\"1KB\" -> {} bytes\n", .{parsed1});

    const parsed2 = humanize.parseSize("1KiB") catch return;
    std.debug.print("\"1KiB\" -> {} bytes\n", .{parsed2});

    const parsed3 = humanize.parseSize("1.5MB") catch return;
    std.debug.print("\"1.5MB\" -> {} bytes\n", .{parsed3});

    const parsed4 = humanize.parseSize("2GB") catch return;
    std.debug.print("\"2GB\" -> {} bytes\n", .{parsed4});

    // ==================== Duration Formatting ====================
    std.debug.print("\n--- Duration Formatting ---\n", .{});
    
    {
        const dur1 = humanize.formatDuration(allocator, 3665, .full) catch return;
        defer allocator.free(dur1);
        std.debug.print("3665 seconds (full): {s}\n", .{dur1});
    }
    
    {
        const dur2 = humanize.formatDuration(allocator, 3665, .compact) catch return;
        defer allocator.free(dur2);
        std.debug.print("3665 seconds (compact): {s}\n", .{dur2});
    }
    
    {
        const dur3 = humanize.formatDuration(allocator, 3665, .text) catch return;
        defer allocator.free(dur3);
        std.debug.print("3665 seconds (text): {s}\n", .{dur3});
    }
    
    {
        const dur4 = humanize.formatDuration(allocator, 3665, .text_cn) catch return;
        defer allocator.free(dur4);
        std.debug.print("3665 seconds (Chinese): {s}\n", .{dur4});
    }
    
    {
        const dur5 = humanize.formatDuration(allocator, 90, .compact) catch return;
        defer allocator.free(dur5);
        std.debug.print("90 seconds (compact): {s}\n", .{dur5});
    }
    
    {
        const dur6 = humanize.formatDuration(allocator, 86400, .text) catch return;
        defer allocator.free(dur6);
        std.debug.print("86400 seconds (text): {s}\n", .{dur6});
    }

    // ==================== Number Formatting ====================
    std.debug.print("\n--- Number Formatting ---\n", .{});
    
    {
        const num1 = humanize.formatWithCommas(allocator, 1000000) catch return;
        defer allocator.free(num1);
        std.debug.print("1000000 with commas: {s}\n", .{num1});
    }
    
    {
        const num2 = humanize.formatWithCommas(allocator, 1234567890) catch return;
        defer allocator.free(num2);
        std.debug.print("1234567890 with commas: {s}\n", .{num2});
    }
    
    {
        const num3 = humanize.formatWithCommas(allocator, -1000000) catch return;
        defer allocator.free(num3);
        std.debug.print("-1000000 with commas: {s}\n", .{num3});
    }
    
    {
        const num4 = humanize.formatNumberCompact(allocator, 1500, 1) catch return;
        defer allocator.free(num4);
        std.debug.print("1500 compact: {s}\n", .{num4});
    }
    
    {
        const num5 = humanize.formatNumberCompact(allocator, 1500000, 1) catch return;
        defer allocator.free(num5);
        std.debug.print("1500000 compact: {s}\n", .{num5});
    }
    
    {
        const num6 = humanize.formatNumberCompact(allocator, 1500000000, 1) catch return;
        defer allocator.free(num6);
        std.debug.print("1500000000 compact: {s}\n", .{num6});
    }
    
    {
        const num7 = humanize.formatPercentage(allocator, 0.5, 1, false) catch return;
        defer allocator.free(num7);
        std.debug.print("0.5 as percentage: {s}\n", .{num7});
    }
    
    {
        const num8 = humanize.formatPercentage(allocator, 0.256, 2, false) catch return;
        defer allocator.free(num8);
        std.debug.print("0.256 as percentage: {s}\n", .{num8});
    }
    
    {
        const num9 = humanize.formatPercentage(allocator, 0.75, 1, true) catch return;
        defer allocator.free(num9);
        std.debug.print("0.75 as percentage (with sign): {s}\n", .{num9});
    }

    // ==================== Relative Time ====================
    std.debug.print("\n--- Relative Time ---\n", .{});
    
    {
        const rel1 = humanize.formatRelativeTime(allocator, 30, false) catch return;
        defer allocator.free(rel1);
        std.debug.print("30 seconds ago: {s}\n", .{rel1});
    }
    
    {
        const rel2 = humanize.formatRelativeTime(allocator, 120, false) catch return;
        defer allocator.free(rel2);
        std.debug.print("120 seconds ago: {s}\n", .{rel2});
    }
    
    {
        const rel3 = humanize.formatRelativeTime(allocator, 3600, false) catch return;
        defer allocator.free(rel3);
        std.debug.print("3600 seconds ago: {s}\n", .{rel3});
    }
    
    {
        const rel4 = humanize.formatRelativeTime(allocator, 86400, false) catch return;
        defer allocator.free(rel4);
        std.debug.print("86400 seconds ago: {s}\n", .{rel4});
    }
    
    {
        const rel5 = humanize.formatRelativeTime(allocator, 2592000, false) catch return;
        defer allocator.free(rel5);
        std.debug.print("2592000 seconds ago: {s}\n", .{rel5});
    }
    
    {
        const rel6 = humanize.formatRelativeTime(allocator, 31536000, false) catch return;
        defer allocator.free(rel6);
        std.debug.print("31536000 seconds ago: {s}\n", .{rel6});
    }
    
    {
        const rel7 = humanize.formatRelativeTime(allocator, 120, true) catch return;
        defer allocator.free(rel7);
        std.debug.print("120 seconds ago (Chinese): {s}\n", .{rel7});
    }
    
    {
        const rel8 = humanize.formatRelativeTime(allocator, 3600, true) catch return;
        defer allocator.free(rel8);
        std.debug.print("3600 seconds ago (Chinese): {s}\n", .{rel8});
    }

    // ==================== Text Formatting ====================
    std.debug.print("\n--- Text Formatting ---\n", .{});
    
    {
        const txt1 = humanize.truncateText(allocator, "Hello World", 20, "...") catch return;
        defer allocator.free(txt1);
        std.debug.print("\"Hello World\" (max 20): {s}\n", .{txt1});
    }
    
    {
        const txt2 = humanize.truncateText(allocator, "Hello World", 8, "...") catch return;
        defer allocator.free(txt2);
        std.debug.print("\"Hello World\" (max 8): {s}\n", .{txt2});
    }

    // ==================== Ordinal Formatting ====================
    std.debug.print("\n--- Ordinal Formatting ---\n", .{});
    
    {
        const ord1 = humanize.formatOrdinal(allocator, 1) catch return;
        defer allocator.free(ord1);
        std.debug.print("1 ordinal: {s}\n", .{ord1});
    }
    
    {
        const ord2 = humanize.formatOrdinal(allocator, 2) catch return;
        defer allocator.free(ord2);
        std.debug.print("2 ordinal: {s}\n", .{ord2});
    }
    
    {
        const ord3 = humanize.formatOrdinal(allocator, 3) catch return;
        defer allocator.free(ord3);
        std.debug.print("3 ordinal: {s}\n", .{ord3});
    }
    
    {
        const ord4 = humanize.formatOrdinal(allocator, 11) catch return;
        defer allocator.free(ord4);
        std.debug.print("11 ordinal: {s}\n", .{ord4});
    }
    
    {
        const ord5 = humanize.formatOrdinal(allocator, 21) catch return;
        defer allocator.free(ord5);
        std.debug.print("21 ordinal: {s}\n", .{ord5});
    }
    
    {
        const ord6 = humanize.formatOrdinalChinese(allocator, 1) catch return;
        defer allocator.free(ord6);
        std.debug.print("1 ordinal (Chinese): {s}\n", .{ord6});
    }
    
    {
        const ord7 = humanize.formatOrdinalChinese(allocator, 100) catch return;
        defer allocator.free(ord7);
        std.debug.print("100 ordinal (Chinese): {s}\n", .{ord7});
    }

    // ==================== List Formatting ====================
    std.debug.print("\n--- List Formatting ---\n", .{});
    
    {
        const items1: []const []const u8 = &.{"apple", "banana", "cherry"};
        const list1 = humanize.formatList(allocator, items1, false) catch return;
        defer allocator.free(list1);
        std.debug.print("List (English): {s}\n", .{list1});
    }
    
    {
        const items2: []const []const u8 = &.{"苹果", "香蕉", "樱桃"};
        const list2 = humanize.formatList(allocator, items2, true) catch return;
        defer allocator.free(list2);
        std.debug.print("List (Chinese): {s}\n", .{list2});
    }
    
    {
        const items3: []const []const u8 = &.{"Alice", "Bob"};
        const list3 = humanize.formatList(allocator, items3, false) catch return;
        defer allocator.free(list3);
        std.debug.print("Two items (English): {s}\n", .{list3});
    }
    
    {
        const items4: []const []const u8 = &.{"只", "有", "一", "个"};
        const list4 = humanize.formatList(allocator, items4, true) catch return;
        defer allocator.free(list4);
        std.debug.print("Four items (Chinese): {s}\n", .{list4});
    }

    std.debug.print("\n=== All Examples Completed ===\n\n", .{});
}