const std = @import("std");

pub const UUID = @import("uuid.zig").UUID;
pub const Generator = @import("uuid.zig").Generator;
pub const Version = @import("uuid.zig").Version;
pub const Variant = @import("uuid.zig").Variant;
pub const UUIDError = @import("uuid.zig").UUIDError;
pub const generateV4 = @import("uuid.zig").generateV4;
pub const generateV4WithSeed = @import("uuid.zig").generateV4WithSeed;
pub const nil = @import("uuid.zig").nil;
pub const isValid = @import("uuid.zig").isValid;

test {
    _ = @import("uuid.zig");
}