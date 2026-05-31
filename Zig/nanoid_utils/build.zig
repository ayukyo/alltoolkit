const std = @import("std");

pub fn build(b: *std.Build) void {
    const target = b.standardTargetOptions(.{});
    const optimize = b.standardOptimizeOption(.{});

    // Library module
    const nanoid_mod = b.addModule("nanoid_utils", .{
        .root_source_file = b.path("src/main.zig"),
        .target = target,
        .optimize = optimize,
    });

    // Library
    const lib = b.addStaticLibrary(.{
        .name = "nanoid_utils",
        .root_source_file = b.path("src/main.zig"),
        .target = target,
        .optimize = optimize,
    });
    b.installArtifact(lib);

    // Tests
    const lib_unit_tests = b.addTest(.{
        .root_source_file = b.path("src/main.zig"),
        .target = target,
        .optimize = optimize,
    });

    const run_lib_unit_tests = b.addRunArtifact(lib_unit_tests);

    const test_step = b.step("test", "Run unit tests");
    test_step.dependOn(&run_lib_unit_tests.step);

    // Example
    const example_exe = b.addExecutable(.{
        .name = "nanoid_example",
        .root_source_file = b.path("examples/main.zig"),
        .target = target,
        .optimize = optimize,
    });
    example_exe.root_module.addImport("nanoid_utils", nanoid_mod);

    const run_example = b.addRunArtifact(example_exe);
    const example_step = b.step("example", "Run example");
    example_step.dependOn(&run_example.step);
}