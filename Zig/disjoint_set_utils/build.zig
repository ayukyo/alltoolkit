const std = @import("std");

pub fn build(b: *std.Build) void {
    const target = b.standardTargetOptions(.{});
    const optimize = b.standardOptimizeOption(.{});

    // Module for other projects to import
    const disjoint_set_mod = b.addModule("disjoint_set", .{
        .root_source_file = b.path("src/disjoint_set.zig"),
        .target = target,
        .optimize = optimize,
    });

    // Library
    const lib = b.addStaticLibrary(.{
        .name = "disjoint_set",
        .root_source_file = b.path("src/disjoint_set.zig"),
        .target = target,
        .optimize = optimize,
    });
    b.installArtifact(lib);

    // Tests
    const main_tests = b.addTest(.{
        .root_source_file = b.path("src/disjoint_set.zig"),
        .target = target,
        .optimize = optimize,
    });

    const run_main_tests = b.addRunArtifact(main_tests);

    const test_step = b.step("test", "Run unit tests");
    test_step.dependOn(&run_main_tests.step);

    // Examples
    const examples = [_]struct { name: []const u8, path: []const u8 }{
        .{ .name = "basic", .path = "examples/basic.zig" },
        .{ .name = "network", .path = "examples/network.zig" },
        .{ .name = "components", .path = "examples/components.zig" },
    };

    const examples_step = b.step("examples", "Build all examples");

    for (examples) |example| {
        const exe = b.addExecutable(.{
            .name = example.name,
            .root_source_file = b.path(example.path),
            .target = target,
            .optimize = optimize,
        });
        exe.root_module.addImport("disjoint_set", disjoint_set_mod);
        b.installArtifact(exe);

        const run_cmd = b.addRunArtifact(exe);
        const run_step = b.step(b.fmt("run-{s}", .{example.name}), b.fmt("Run the {s} example", .{example.name}));
        run_step.dependOn(&run_cmd.step);

        examples_step.dependOn(&exe.step);
    }

    // Documentation generation
    const install_docs = b.addInstallDirectory(.{
        .source_dir = lib.getEmittedDocs(),
        .install_dir = .prefix,
        .install_subdir = "docs",
    });

    const docs_step = b.step("docs", "Generate and install documentation");
    docs_step.dependOn(&install_docs.step);
}