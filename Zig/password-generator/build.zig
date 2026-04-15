const std = @import("std");

pub fn build(b: *std.Build) void {
    const target = b.standardTargetOptions(.{});
    const optimize = b.standardOptimizeOption(.{});

    // Create module
    const password_generator_module = b.addModule("password-generator", .{
        .root_source_file = b.path("src/main.zig"),
        .target = target,
        .optimize = optimize,
    });

    // Library
    const lib = b.addStaticLibrary(.{
        .name = "password-generator",
        .root_source_file = b.path("src/main.zig"),
        .target = target,
        .optimize = optimize,
    });
    b.installArtifact(lib);

    // Tests
    const unit_tests = b.addTest(.{
        .root_source_file = b.path("tests/main_test.zig"),
        .target = target,
        .optimize = optimize,
    });
    unit_tests.root_module.addImport("password-generator", password_generator_module);
    const run_unit_tests = b.addRunArtifact(unit_tests);
    const test_step = b.step("test", "Run unit tests");
    test_step.dependOn(&run_unit_tests.step);

    // Example
    const exe = b.addExecutable(.{
        .name = "password-generator-example",
        .root_source_file = b.path("examples/example.zig"),
        .target = target,
        .optimize = optimize,
    });
    exe.root_module.addImport("password-generator", password_generator_module);
    b.installArtifact(exe);
    const run_cmd = b.addRunArtifact(exe);
    const run_step = b.step("run", "Run example");
    run_step.dependOn(&run_cmd.step);
}