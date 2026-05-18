const std = @import("std");

pub fn build(b: *std.Build) void {
    const target = b.standardTargetOptions(.{});
    const optimize = b.standardOptimizeOption(.{});

    // Library module
    const lib_mod = b.addModule("humanize_utils", .{
        .root_source_file = b.path("src/humanize_utils.zig"),
        .target = target,
        .optimize = optimize,
    });

    // Tests - create a test step that runs the tests directly from source
    const lib_tests = b.addTest(.{
        .root_source_file = b.path("src/humanize_utils.zig"),
        .target = target,
        .optimize = optimize,
    });

    const run_lib_tests = b.addRunArtifact(lib_tests);

    const test_step = b.step("test", "Run unit tests");
    test_step.dependOn(&run_lib_tests.step);

    // Example executable
    const example_exe = b.addExecutable(.{
        .name = "humanize-example",
        .root_source_file = b.path("examples/basic_example.zig"),
        .target = target,
        .optimize = optimize,
    });
    example_exe.root_module.addImport("humanize_utils", lib_mod);

    const run_example = b.addRunArtifact(example_exe);
    run_example.step.dependOn(b.getInstallStep());

    if (b.args) |args| {
        run_example.addArgs(args);
    }

    const example_step = b.step("example", "Run the example");
    example_step.dependOn(&run_example.step);
}