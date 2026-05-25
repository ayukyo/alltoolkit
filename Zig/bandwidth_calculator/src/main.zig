pub const BandwidthUnit = @import("bandwidth.zig").BandwidthUnit;
pub const DataUnit = @import("bandwidth.zig").DataUnit;
pub const TimeUnit = @import("bandwidth.zig").TimeUnit;
pub const Bandwidth = @import("bandwidth.zig").Bandwidth;
pub const DataSize = @import("bandwidth.zig").DataSize;
pub const Duration = @import("bandwidth.zig").Duration;
pub const calculateTransferTime = @import("bandwidth.zig").calculateTransferTime;
pub const calculateRequiredBandwidth = @import("bandwidth.zig").calculateRequiredBandwidth;
pub const calculateTransferSize = @import("bandwidth.zig").calculateTransferSize;
pub const formatBandwidth = @import("bandwidth.zig").formatBandwidth;
pub const formatDataSize = @import("bandwidth.zig").formatDataSize;
pub const formatDuration = @import("bandwidth.zig").formatDuration;
pub const parseDataSize = @import("bandwidth.zig").parseDataSize;
pub const parseBandwidth = @import("bandwidth.zig").parseBandwidth;

test {
    _ = @import("bandwidth.zig");
}