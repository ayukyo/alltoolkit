const std = @import("std");

pub fn build(b: *std.Build) void {
    const target = b.standardTargetOptions(.{});
    const optimize = b.standardOptimizeOption(.{});

    // Module
    const quadtree_module = b.addModule("quadtree", .{
        .root_source_file = b.path("src/quadtree.zig"),
        .target = target,
        .optimize = optimize,
    });

    // Tests
    const unit_tests = b.addTest(.{
        .root_source_file = b.path("src/quadtree.zig"),
        .target = target,
        .optimize = optimize,
    });

    const run_unit_tests = b.addRunArtifact(unit_tests);

    // Test step
    const test_step = b.step("test", "Run unit tests");
    test_step.dependOn(&run_unit_tests.step);

    // Example: Basic usage
    const example_basic = b.addExecutable(.{
        .name = "basic_example",
        .root_source_file = b.path("examples/basic.zig"),
        .target = target,
        .optimize = optimize,
    });
    example_basic.root_module.addImport("quadtree", quadtree_module);

    const run_example_basic = b.addRunArtifact(example_basic);
    const example_basic_step = b.step("example-basic", "Run basic example");
    example_basic_step.dependOn(&run_example_basic.step);

    // Example: Spatial query
    const example_query = b.addExecutable(.{
        .name = "query_example",
        .root_source_file = b.path("examples/query.zig"),
        .target = target,
        .optimize = optimize,
    });
    example_query.root_module.addImport("quadtree", quadtree_module);

    const run_example_query = b.addRunArtifact(example_query);
    const example_query_step = b.step("example-query", "Run spatial query example");
    example_query_step.dependOn(&run_example_query.step);

    // Example: Nearest neighbor
    const example_nearest = b.addExecutable(.{
        .name = "nearest_example",
        .root_source_file = b.path("examples/nearest.zig"),
        .target = target,
        .optimize = optimize,
    });
    example_nearest.root_module.addImport("quadtree", quadtree_module);

    const run_example_nearest = b.addRunArtifact(example_nearest);
    const example_nearest_step = b.step("example-nearest", "Run nearest neighbor example");
    example_nearest_step.dependOn(&run_example_nearest.step);

    // Example: City locations
    const example_cities = b.addExecutable(.{
        .name = "cities_example",
        .root_source_file = b.path("examples/cities.zig"),
        .target = target,
        .optimize = optimize,
    });
    example_cities.root_module.addImport("quadtree", quadtree_module);

    const run_example_cities = b.addRunArtifact(example_cities);
    const example_cities_step = b.step("example-cities", "Run cities location example");
    example_cities_step.dependOn(&run_example_cities.step);

    // Example: Collision detection
    const example_collision = b.addExecutable(.{
        .name = "collision_example",
        .root_source_file = b.path("examples/collision.zig"),
        .target = target,
        .optimize = optimize,
    });
    example_collision.root_module.addImport("quadtree", quadtree_module);

    const run_example_collision = b.addRunArtifact(example_collision);
    const example_collision_step = b.step("example-collision", "Run collision detection example");
    example_collision_step.dependOn(&run_example_collision.step);
}