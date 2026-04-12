const std = @import("std");

pub fn build(b: *std.Build) void {
    const target = b.standardTargetOptions(.{});
    const optimize = b.standardOptimizeOption(.{});

    // Library module
    const url_mod = b.addModule("url", .{
        .root_source_file = b.path("src/main.zig"),
        .target = target,
        .optimize = optimize,
    });

    // Static library
    const lib = b.addStaticLibrary(.{
        .name = "url-parser",
        .root_source_file = b.path("src/main.zig"),
        .target = target,
        .optimize = optimize,
    });
    b.installArtifact(lib);

    // Example executable - basic
    const basic_exe = b.addExecutable(.{
        .name = "url-basic",
        .root_source_file = b.path("examples/basic.zig"),
        .target = target,
        .optimize = optimize,
    });
    basic_exe.root_module.addImport("url", url_mod);

    const basic_run = b.addRunArtifact(basic_exe);
    if (b.args) |args| {
        basic_run.addArgs(args);
    }

    const basic_step = b.step("run-basic", "Run basic example");
    basic_step.dependOn(&basic_run.step);

    // Example executable - advanced
    const advanced_exe = b.addExecutable(.{
        .name = "url-advanced",
        .root_source_file = b.path("examples/advanced.zig"),
        .target = target,
        .optimize = optimize,
    });
    advanced_exe.root_module.addImport("url", url_mod);

    const advanced_run = b.addRunArtifact(advanced_exe);
    if (b.args) |args| {
        advanced_run.addArgs(args);
    }

    const advanced_step = b.step("run-advanced", "Run advanced example");
    advanced_step.dependOn(&advanced_run.step);

    // Run step (default to basic)
    const run_step = b.step("run", "Run basic example");
    run_step.dependOn(&basic_run.step);

    // Unit tests
    const unit_tests = b.addTest(.{
        .root_source_file = b.path("src/main.zig"),
        .target = target,
        .optimize = optimize,
    });

    const run_unit_tests = b.addRunArtifact(unit_tests);
    const test_step = b.step("test", "Run unit tests");
    test_step.dependOn(&run_unit_tests.step);
}