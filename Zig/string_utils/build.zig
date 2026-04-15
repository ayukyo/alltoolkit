const std = @import("std");

pub fn build(b: *std.Build) void {
    const target = b.standardTargetOptions(.{});
    const optimize = b.standardOptimizeOption(.{});

    // Module
    const string_utils_mod = b.addModule("string_utils", .{
        .root_source_file = b.path("src/string_utils.zig"),
        .target = target,
        .optimize = optimize,
    });

    // Tests
    const lib_tests = b.addTest(.{
        .root_source_file = b.path("src/string_utils.zig"),
        .target = target,
        .optimize = optimize,
    });

    const run_lib_tests = b.addRunArtifact(lib_tests);

    const test_step = b.step("test", "Run unit tests");
    test_step.dependOn(&run_lib_tests.step);

    // Example executable
    const example_exe = b.addExecutable(.{
        .name = "string_utils_example",
        .root_source_file = b.path("examples/usage_example.zig"),
        .target = target,
        .optimize = optimize,
    });
    example_exe.root_module.addImport("string_utils", string_utils_mod);

    const run_example = b.addRunArtifact(example_exe);
    run_example.step.dependOn(b.getInstallStep());

    const example_step = b.step("example", "Run the example");
    example_step.dependOn(&run_example.step);
}