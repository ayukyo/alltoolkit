const std = @import("std");

pub fn build(b: *std.Build) void {
    const target = b.standardTargetOptions(.{});
    const optimize = b.standardOptimizeOption(.{});

    // Library module
    const ring_buffer_mod = b.addModule("ring-buffer", .{
        .root_source_file = b.path("src/ring_buffer.zig"),
        .target = target,
        .optimize = optimize,
    });

    // Library
    const lib = b.addStaticLibrary(.{
        .name = "ring-buffer",
        .root_source_file = b.path("src/ring_buffer.zig"),
        .target = target,
        .optimize = optimize,
    });
    b.installArtifact(lib);

    // Basic example
    const basic_exe = b.addExecutable(.{
        .name = "rb-basic",
        .root_source_file = b.path("examples/basic.zig"),
        .target = target,
        .optimize = optimize,
    });
    basic_exe.root_module.addImport("ring-buffer", ring_buffer_mod);
    b.installArtifact(basic_exe);

    const run_basic = b.addRunArtifact(basic_exe);
    const run_basic_step = b.step("run-basic", "Run the basic example");
    run_basic_step.dependOn(&run_basic.step);

    // Advanced example
    const advanced_exe = b.addExecutable(.{
        .name = "rb-advanced",
        .root_source_file = b.path("examples/advanced.zig"),
        .target = target,
        .optimize = optimize,
    });
    advanced_exe.root_module.addImport("ring-buffer", ring_buffer_mod);
    b.installArtifact(advanced_exe);

    const run_advanced = b.addRunArtifact(advanced_exe);
    const run_advanced_step = b.step("run-advanced", "Run the advanced example");
    run_advanced_step.dependOn(&run_advanced.step);

    // Test step
    const unit_tests = b.addTest(.{
        .root_source_file = b.path("src/ring_buffer.zig"),
        .target = target,
        .optimize = optimize,
    });

    const run_unit_tests = b.addRunArtifact(unit_tests);
    const test_step = b.step("test", "Run unit tests");
    test_step.dependOn(&run_unit_tests.step);
}