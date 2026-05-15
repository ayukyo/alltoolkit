--[[
    Test suite for slug_utils
    
    Run with: lua test_slug.lua
]]

package.path = package.path .. ";./?.lua"

local slug_utils = require("slug")

-- Test framework (minimal)
local tests_passed = 0
local tests_failed = 0

local function describe(name)
    print("\n=== " .. name .. " ===")
end

local function it(description, fn)
    local success, err = pcall(fn)
    if success then
        tests_passed = tests_passed + 1
        print("  ✓ " .. description)
    else
        tests_failed = tests_failed + 1
        print("  ✗ " .. description)
        print("    Error: " .. tostring(err))
    end
end

local function assert_equals(expected, actual)
    if expected ~= actual then
        error("Expected: " .. tostring(expected) .. ", got: " .. tostring(actual))
    end
end

local function assert_true(value)
    if not value then
        error("Expected true, got false")
    end
end

local function assert_false(value)
    if value then
        error("Expected false, got true")
    end
end

-- Tests
print("Starting slug_utils tests...")

describe("Basic slug generation")

it("should convert simple strings", function()
    assert_equals("hello-world", slug_utils.slug("Hello World"))
end)

it("should handle lowercase option", function()
    assert_equals("hello-world", slug_utils.slug("Hello World", { lowercase = true }))
    assert_equals("Hello-World", slug_utils.slug("Hello World", { lowercase = false }))
end)

it("should handle multiple spaces", function()
    assert_equals("hello-world", slug_utils.slug("Hello    World"))
end)

it("should handle leading and trailing spaces", function()
    assert_equals("hello-world", slug_utils.slug("   Hello World   "))
end)

it("should handle special characters", function()
    assert_equals("hello-world", slug_utils.slug("Hello @#$% World!"))
end)

it("should handle underscores", function()
    assert_equals("hello-world", slug_utils.slug("Hello_World"))
end)

it("should handle hyphens", function()
    assert_equals("hello-world", slug_utils.slug("Hello-World"))
end)

it("should handle empty string", function()
    assert_equals("", slug_utils.slug(""))
end)

describe("Transliteration")

it("should transliterate Latin extended characters", function()
    assert_equals("cafe", slug_utils.slug("Café"))
    assert_equals("naive", slug_utils.slug("Naïve"))
end)

it("should transliterate German umlauts", function()
    assert_equals("gruesse", slug_utils.slug("Grüße"))
end)

it("should transliterate Cyrillic characters", function()
    assert_equals("privet", slug_utils.slug("Привет"))
end)

it("should transliterate Greek characters", function()
    assert_equals("abg", slug_utils.slug("αβγ"))
end)

describe("Custom separators")

it("should use underscore separator", function()
    assert_equals("hello_world", slug_utils.slug_underscore("Hello World"))
end)

it("should use custom separator", function()
    assert_equals("hello.world", slug_utils.slug_with_separator("Hello World", "."))
end)

it("should handle custom separator in options", function()
    assert_equals("hello+world", slug_utils.slug("Hello World", { separator = "+" }))
end)

describe("Slug validation")

it("should validate correct slugs", function()
    assert_true(slug_utils.is_valid_slug("hello-world"))
    assert_true(slug_utils.is_valid_slug("hello"))
    assert_true(slug_utils.is_valid_slug("hello-world-123"))
end)

it("should reject invalid slugs", function()
    assert_false(slug_utils.is_valid_slug(""))
    assert_false(slug_utils.is_valid_slug("-hello-world"))
    assert_false(slug_utils.is_valid_slug("hello-world-"))
    assert_false(slug_utils.is_valid_slug("hello--world"))
    assert_false(slug_utils.is_valid_slug("Hello World"))
end)

it("should validate with custom separator", function()
    assert_true(slug_utils.is_valid_slug("hello_world", "_"))
    assert_false(slug_utils.is_valid_slug("hello-world", "_"))
end)

describe("Slug parsing")

it("should parse slug into words", function()
    local words = slug_utils.parse_slug("hello-world-test")
    assert_equals(3, #words)
    assert_equals("hello", words[1])
    assert_equals("world", words[2])
    assert_equals("test", words[3])
end)

it("should parse single word slug", function()
    local words = slug_utils.parse_slug("hello")
    assert_equals(1, #words)
    assert_equals("hello", words[1])
end)

it("should parse with custom separator", function()
    local words = slug_utils.parse_slug("hello_world_test", "_")
    assert_equals(3, #words)
end)

it("should handle empty slug", function()
    local words = slug_utils.parse_slug("")
    assert_equals(0, #words)
end)

describe("Unique slugs")

it("should generate slug with suffix", function()
    local result = slug_utils.slug_unique("Hello World", "123")
    assert_equals("hello-world-123", result)
end)

it("should generate slug with random suffix when none provided", function()
    local result = slug_utils.slug_unique("Hello World")
    assert_true(result:match("^hello%-world%-%d+$") ~= nil)
end)

describe("Slug truncation")

it("should truncate slug at word boundaries", function()
    local result = slug_utils.truncate_slug("hello-world-test", 10)
    assert_equals("hello", result)
end)

it("should not modify short slugs", function()
    local result = slug_utils.truncate_slug("hello", 10)
    assert_equals("hello", result)
end)

it("should handle custom separator", function()
    local result = slug_utils.truncate_slug("hello_world_test", 10, "_")
    assert_equals("hello", result)
end)

describe("Edge cases")

it("should handle strings with only special characters", function()
    assert_equals("", slug_utils.slug("@#$%^&*()"))
end)

it("should handle strings with numbers", function()
    assert_equals("hello-123-world", slug_utils.slug("Hello 123 World"))
end)

it("should handle mixed case with preserve option", function()
    local result = slug_utils.slug_preserve_case("Hello World")
    assert_equals("Hello-World", result)
end)

it("should handle consecutive separators", function()
    assert_equals("hello-world", slug_utils.slug("Hello___World"))
end)

it("should handle newlines and tabs", function()
    assert_equals("hello-world", slug_utils.slug("Hello\n\tWorld"))
end)

describe("Error handling")

it("should error on non-string input", function()
    local success = pcall(function()
        slug_utils.slug(123)
    end)
    assert_false(success)
end)

it("should handle nil in parse_slug", function()
    local words = slug_utils.parse_slug(nil)
    assert_equals(0, #words)
end)

-- Summary
print("\n" .. string.rep("=", 40))
print(string.format("Tests passed: %d", tests_passed))
print(string.format("Tests failed: %d", tests_failed))
print(string.rep("=", 40))

if tests_failed > 0 then
    os.exit(1)
else
    print("\nAll tests passed! ✓")
    os.exit(0)
end