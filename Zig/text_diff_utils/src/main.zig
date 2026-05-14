const std = @import("std");

pub const DiffOp = @import("text_diff.zig").DiffOp;
pub const DiffItem = @import("text_diff.zig").DiffItem;
pub const DiffStats = @import("text_diff.zig").DiffStats;
pub const DiffResult = @import("text_diff.zig").DiffResult;
pub const UnifiedDiffOptions = @import("text_diff.zig").UnifiedDiffOptions;

pub const diffLines = @import("text_diff.zig").diffLines;
pub const diffChars = @import("text_diff.zig").diffChars;
pub const unifiedDiff = @import("text_diff.zig").unifiedDiff;
pub const similarity = @import("text_diff.zig").similarity;
pub const applyPatch = @import("text_diff.zig").applyPatch;

test {
    _ = @import("text_diff.zig");
}