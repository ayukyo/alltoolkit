const std = @import("std");

pub fn build(b: *std.Build) void {
    const target = b.standardTargetOptions(.{});
    const optimize = b.standardOptimizeOption(.{});

    // Tests
    const unit_tests = b.addTest(.{
        .root_source_file = b.path("src/temperature_converter.zig"),
        .target = target,
        .optimize = optimize,
    });

    const run_unit_tests = b.addRunArtifact(unit_tests);
    const test_step = b.step("test", "Run unit tests");
    test_step.dependOn(&run_unit_tests.step);

    // Examples
    const example_exe = b.addExecutable(.{
        .name = "temperature_converter_example",
        .root_source_file = b.path("examples/basic_usage.zig"),
        .target = target,
        .optimize = optimize,
    });
    example_exe.root_module.addImport("temperature_converter", b.createModule(.{
        .root_source_file = b.path("src/temperature_converter.zig"),
    }));

    const run_example = b.addRunArtifact(example_exe);
    const example_step = b.step("example", "Run example");
    example_step.dependOn(&run_example.step);
}