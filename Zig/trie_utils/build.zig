const std = @import("std");

pub fn build(b: *std.Build) void {
    const target = b.standardTargetOptions(.{});
    const optimize = b.standardOptimizeOption(.{});

    // Module
    const trie_module = b.addModule("trie", .{
        .root_source_file = b.path("src/trie.zig"),
        .target = target,
        .optimize = optimize,
    });

    // Tests
    const unit_tests = b.addTest(.{
        .root_source_file = b.path("src/trie.zig"),
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
    example_basic.root_module.addImport("trie", trie_module);

    const run_example_basic = b.addRunArtifact(example_basic);
    const example_basic_step = b.step("example-basic", "Run basic example");
    example_basic_step.dependOn(&run_example_basic.step);

    // Example: Autocomplete
    const example_autocomplete = b.addExecutable(.{
        .name = "autocomplete_example",
        .root_source_file = b.path("examples/autocomplete.zig"),
        .target = target,
        .optimize = optimize,
    });
    example_autocomplete.root_module.addImport("trie", trie_module);

    const run_example_autocomplete = b.addRunArtifact(example_autocomplete);
    const example_autocomplete_step = b.step("example-autocomplete", "Run autocomplete example");
    example_autocomplete_step.dependOn(&run_example_autocomplete.step);

    // Example: Spell checker
    const example_spellcheck = b.addExecutable(.{
        .name = "spellcheck_example",
        .root_source_file = b.path("examples/spellcheck.zig"),
        .target = target,
        .optimize = optimize,
    });
    example_spellcheck.root_module.addImport("trie", trie_module);

    const run_example_spellcheck = b.addRunArtifact(example_spellcheck);
    const example_spellcheck_step = b.step("example-spellcheck", "Run spell check example");
    example_spellcheck_step.dependOn(&run_example_spellcheck.step);

    // Example: Pattern matching
    const example_pattern = b.addExecutable(.{
        .name = "pattern_example",
        .root_source_file = b.path("examples/pattern.zig"),
        .target = target,
        .optimize = optimize,
    });
    example_pattern.root_module.addImport("trie", trie_module);

    const run_example_pattern = b.addRunArtifact(example_pattern);
    const example_pattern_step = b.step("example-pattern", "Run pattern matching example");
    example_pattern_step.dependOn(&run_example_pattern.step);

    // Example: Word frequency
    const example_frequency = b.addExecutable(.{
        .name = "frequency_example",
        .root_source_file = b.path("examples/frequency.zig"),
        .target = target,
        .optimize = optimize,
    });
    example_frequency.root_module.addImport("trie", trie_module);

    const run_example_frequency = b.addRunArtifact(example_frequency);
    const example_frequency_step = b.step("example-frequency", "Run word frequency example");
    example_frequency_step.dependOn(&run_example_frequency.step);
}