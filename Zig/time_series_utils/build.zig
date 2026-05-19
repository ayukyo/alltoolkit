const std = @import("std");

pub fn build(b: *std.Build) void {
    const target = b.standardTargetOptions(.{});
    const optimize = b.standardOptimizeOption(.{});

    // Library module
    const lib_mod = b.addModule("time_series", .{
        .root_source_file = b.path("time_series.zig"),
        .target = target,
        .optimize = optimize,
    });

    // Library
    const lib = b.addStaticLibrary(.{
        .name = "time_series",
        .root_source_file = b.path("time_series.zig"),
        .target = target,
        .optimize = optimize,
    });
    b.installArtifact(lib);

    // Tests
    const unit_tests = b.addTest(.{
        .root_source_file = b.path("time_series.zig"),
        .target = target,
        .optimize = optimize,
    });
    const run_unit_tests = b.addRunArtifact(unit_tests);

    const test_step = b.step("test", "Run unit tests");
    test_step.dependOn(&run_unit_tests);

    // Example executable
    const exe = b.addExecutable(.{
        .name = "time_series_example",
        .root_source_file = b.path("example.zig"),
        .target = target,
        .optimize = optimize,
    });
    exe.root_module.addImport("time_series", lib_mod);
    b.installArtifact(exe);

    const run_exe = b.addRunArtifact(exe);
    const example_step = b.step("example", "Run the example");
    example_step.dependOn(&run_exe);

    // Install step
    const install_step = b.step("install", "Install the library");
    install_step.dependOn(&lib.step);
}