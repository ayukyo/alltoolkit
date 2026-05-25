const std = @import("std");
const bandwidth = @import("bandwidth_calculator");

pub fn main() !void {
    const allocator = std.heap.page_allocator;

    std.debug.print("=== Bandwidth Calculator 示例 ===\n\n", .{});

    // 1. 带宽单位转换
    std.debug.print("1. 带宽单位转换:\n", .{});
    const bw = bandwidth.Bandwidth.init(100.0, .Mbps);
    std.debug.print("   原始: 100 Mbps\n", .{});

    const kbps = bw.to(.Kbps);
    std.debug.print("   转换为 Kbps: {d:.2} Kbps\n", .{kbps.value});

    const gbps = bw.to(.Gbps);
    std.debug.print("   转换为 Gbps: {d:.4} Gbps\n", .{gbps.value});

    const bps = bw.to(.bps);
    std.debug.print("   转换为 bps: {d:.0} bps\n\n", .{bps.value});

    // 2. 数据大小单位转换
    std.debug.print("2. 数据大小单位转换:\n", .{});
    const size = bandwidth.DataSize.init(1.0, .GB);
    std.debug.print("   原始: 1 GB\n", .{});

    const mb = size.to(.MB);
    std.debug.print("   转换为 MB: {d:.0} MB\n", .{mb.value});

    const kb = size.to(.KB);
    std.debug.print("   转换为 KB: {d:.0} KB\n", .{kb.value});

    const bytes = size.to(.Byte);
    std.debug.print("   转换为 bytes: {d:.0} bytes\n\n", .{bytes.value});

    // 3. 计算下载时间
    std.debug.print("3. 计算下载时间:\n", .{});
    const file_size = bandwidth.DataSize.init(4.7, .GB);
    const connection_speed = bandwidth.Bandwidth.init(50.0, .Mbps);
    const download_time = bandwidth.calculateTransferTime(file_size, connection_speed);

    const time_str = try bandwidth.formatDuration(download_time, allocator);
    defer allocator.free(time_str);
    std.debug.print("   文件大小: 4.7 GB\n", .{});
    std.debug.print("   网络速度: 50 Mbps\n", .{});
    std.debug.print("   下载时间: {s}\n\n", .{time_str});

    // 4. 计算所需带宽
    std.debug.print("4. 计算所需带宽:\n", .{});
    const required_size = bandwidth.DataSize.init(1.0, .GB);
    const time_limit = bandwidth.Duration.init(2.0, .minutes);
    const required_bw = bandwidth.calculateRequiredBandwidth(required_size, time_limit);
    const required_mbps = required_bw.to(.Mbps);

    std.debug.print("   数据大小: 1 GB\n", .{});
    std.debug.print("   时间限制: 2 分钟\n", .{});
    std.debug.print("   所需带宽: {d:.2} Mbps\n\n", .{required_mbps.value});

    // 5. 计算传输数据量
    std.debug.print("5. 计算传输数据量:\n", .{});
    const upload_speed = bandwidth.Bandwidth.init(10.0, .Mbps);
    const upload_duration = bandwidth.Duration.init(1.0, .hours);
    const transferred = bandwidth.calculateTransferSize(upload_speed, upload_duration);
    const transferred_gb = transferred.to(.GB);

    std.debug.print("   上传速度: 10 Mbps\n", .{});
    std.debug.print("   上传时长: 1 小时\n", .{});
    std.debug.print("   传输数据: {d:.2} GB\n\n", .{transferred_gb.value});

    // 6. 自动格式化显示
    std.debug.print("6. 自动格式化显示:\n", .{});

    const bw1 = bandwidth.Bandwidth.init(1500000.0, .bps);
    const bw1_str = try bandwidth.formatBandwidth(bw1, allocator);
    defer allocator.free(bw1_str);
    std.debug.print("   1500000 bps -> {s}\n", .{bw1_str});

    const bw2 = bandwidth.Bandwidth.init(1500000000.0, .bps);
    const bw2_str = try bandwidth.formatBandwidth(bw2, allocator);
    defer allocator.free(bw2_str);
    std.debug.print("   1500000000 bps -> {s}\n", .{bw2_str});

    const ds1 = bandwidth.DataSize.init(1536.0, .MB);
    const ds1_str = try bandwidth.formatDataSize(ds1, allocator);
    defer allocator.free(ds1_str);
    std.debug.print("   1536 MB -> {s}\n", .{ds1_str});

    const dur1 = bandwidth.Duration.init(3665.0, .seconds);
    const dur1_str = try bandwidth.formatDuration(dur1, allocator);
    defer allocator.free(dur1_str);
    std.debug.print("   3665 秒 -> {s}\n\n", .{dur1_str});

    // 7. 解析字符串
    std.debug.print("7. 解析字符串:\n", .{});

    const parsed_size = try bandwidth.parseDataSize("4.7GB");
    std.debug.print("   解析 \"4.7GB\": {d:.1} GB\n", .{parsed_size.value});

    const parsed_bw = try bandwidth.parseBandwidth("100Mbps");
    std.debug.print("   解析 \"100Mbps\": {d:.0} Mbps\n\n", .{parsed_bw.value});

    // 8. 实际应用场景
    std.debug.print("8. 实际应用场景:\n", .{});

    // 场景1: 流媒体带宽计算
    std.debug.print("   场景1 - 流媒体带宽需求:\n", .{});
    const video_size_per_min = bandwidth.DataSize.init(50.0, .MB);
    const stream_bw = bandwidth.calculateRequiredBandwidth(video_size_per_min, bandwidth.Duration.init(1.0, .minutes));
    const stream_bw_mbps = stream_bw.to(.Mbps);
    std.debug.print("     视频大小: 50 MB/分钟\n", .{});
    std.debug.print("     所需带宽: {d:.2} Mbps\n", .{stream_bw_mbps.value});

    // 场景2: 云存储上传时间估算
    std.debug.print("   场景2 - 云存储上传时间:\n", .{});
    const backup_size = bandwidth.DataSize.init(100.0, .GB);
    const upload_speed_real = bandwidth.Bandwidth.init(20.0, .Mbps);
    const backup_time = bandwidth.calculateTransferTime(backup_size, upload_speed_real);
    const backup_hours = backup_time.to(.hours);
    std.debug.print("     备份大小: 100 GB\n", .{});
    std.debug.print("     上传速度: 20 Mbps\n", .{});
    std.debug.print("     预计时间: {d:.1} 小时\n", .{backup_hours.value});

    // 场景3: 网络升级决策
    std.debug.print("   场景3 - 网络升级决策:\n", .{});
    const work_file = bandwidth.DataSize.init(5.0, .GB);
    const current_speed = bandwidth.Bandwidth.init(25.0, .Mbps);
    const current_time = bandwidth.calculateTransferTime(work_file, current_speed);
    const upgraded_speed = bandwidth.Bandwidth.init(100.0, .Mbps);
    const upgraded_time = bandwidth.calculateTransferTime(work_file, upgraded_speed);
    const time_saved_min = current_time.to(.minutes).value - upgraded_time.to(.minutes).value;
    std.debug.print("     工作文件: 5 GB\n", .{});
    std.debug.print("     当前网络 (25 Mbps): {d:.1} 分钟\n", .{current_time.to(.minutes).value});
    std.debug.print("     升级网络 (100 Mbps): {d:.1} 分钟\n", .{upgraded_time.to(.minutes).value});
    std.debug.print("     节省时间: {d:.1} 分钟\n", .{time_saved_min});

    std.debug.print("\n=== 示例完成 ===\n", .{});
}