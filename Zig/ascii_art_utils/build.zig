const std = @import("std");

pub fn build(b: *std.Build) void {
    const target = b.standardTargetOptions(.{});
    const optimize = b.standardOptimizeOption(.{});

    // Main library module
    const lib_mod = b.addModule("ascii_art", .{
        .root_source_file = b.path("ascii_art.zig"),
        .target = target,
        .optimize = optimize,
    });

    // Example executable
    const exe = b.addExecutable(.{
        .name = "ascii-art-example",
        .root_source_file = b.path("example.zig"),
        .target = target,
        .optimize = optimize,
    });
    exe.root_module.addImport("ascii_art", lib_mod);

    b.installArtifact(exe);

    // Run step for example
    const run_exe = b.addRunArtifact(exe);
    if (b.args) |args| {
        run_exe.addArgs(args);
    }

    const run_step = b.step("run", "Run the example");
    run_step.dependOn(&run_exe.step);

    // Tests
    const lib_tests = b.addTest(.{
        .root_source_file = b.path("ascii_art.zig"),
        .target = target,
        .optimize = optimize,
    });

    const run_lib_tests = b.addRunArtifact(lib_tests);

    const test_step = b.step("test", "Run library tests");
    test_step.dependOn(&run_lib_tests.step);
}