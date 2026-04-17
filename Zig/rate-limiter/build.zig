const std = @import("std");

pub fn build(b: *std.Build) void {
    const target = b.standardTargetOptions(.{});
    const optimize = b.standardOptimizeOption(.{});

    // Module
    const mod = b.addModule("rate_limiter", .{
        .root_source_file = b.path("src/rate_limiter.zig"),
        .target = target,
        .optimize = optimize,
    });

    // Tests
    const unit_tests = b.addTest(.{
        .root_source_file = b.path("src/rate_limiter.zig"),
        .target = target,
        .optimize = optimize,
    });
    const run_unit_tests = b.addRunArtifact(unit_tests);
    const test_step = b.step("test", "Run unit tests");
    test_step.dependOn(&run_unit_tests.step);

    // Examples
    const examples = [_]struct { name: []const u8, path: []const u8 }{
        .{ .name = "basic", .path = "examples/basic.zig" },
        .{ .name = "advanced", .path = "examples/advanced.zig" },
    };

    inline for (examples) |example| {
        const exe = b.addExecutable(.{
            .name = example.name,
            .root_source_file = b.path(example.path),
            .target = target,
            .optimize = optimize,
        });
        exe.root_module.addImport("rate_limiter", mod);
        b.installArtifact(exe);

        const run_cmd = b.addRunArtifact(exe);
        run_cmd.step.dependOn(b.getInstallStep());
        const run_step = b.step(example.name, "Run " ++ example.name ++ " example");
        run_step.dependOn(&run_cmd.step);
    }
}