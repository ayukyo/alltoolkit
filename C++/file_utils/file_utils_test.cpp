/**
 * @file file_utils_test.cpp
 * @brief Unit tests for C++ File Utilities
 * @version 1.0.0
 *
 * Comprehensive test suite covering all FileUtils functionality.
 * Run with: g++ -std=c++11 -o file_utils_test file_utils_test.cpp && ./file_utils_test
 */

#include <cassert>
#include <iostream>
#include <cstdio>
#include "mod.hpp"

using namespace alltoolkit;

// Test counter
int tests_run = 0;
int tests_passed = 0;

#define TEST(name) void test_##name()
#define RUN_TEST(name) do { \
    tests_run++; \
    std::cout << "Running " #name "... "; \
    try { \
        test_##name(); \
        tests_passed++; \
        std::cout << "PASSED" << std::endl; \
    } catch (const std::exception& e) { \
        std::cout << "FAILED: " << e.what() << std::endl; \
    } \
} while(0)

#define ASSERT_TRUE(expr) do { \
    if (!(expr)) throw std::runtime_error("Assertion failed: " #expr); \
} while(0)

#define ASSERT_FALSE(expr) ASSERT_TRUE(!(expr))
#define ASSERT_EQ(a, b) ASSERT_TRUE((a) == (b))
#define ASSERT_NE(a, b) ASSERT_TRUE((a) != (b))

// Test: File existence checks
TEST(file_exists) {
    // Create a test file
    FileUtils::writeText("/tmp/test_file_exists.txt", "test content");
    ASSERT_TRUE(FileUtils::exists("/tmp/test_file_exists.txt"));
    ASSERT_TRUE(FileUtils::isFile("/tmp/test_file_exists.txt"));
    ASSERT_FALSE(FileUtils::isDirectory("/tmp/test_file_exists.txt"));
    ASSERT_FALSE(FileUtils::exists("/tmp/nonexistent_file_xyz.txt"));
    FileUtils::remove("/tmp/test_file_exists.txt");
}

// Test: Directory existence checks
TEST(directory_exists) {
    FileUtils::ensureDirectory("/tmp/test_dir_exists");
    ASSERT_TRUE(FileUtils::exists("/tmp/test_dir_exists"));
    ASSERT_TRUE(FileUtils::isDirectory("/tmp/test_dir_exists"));
    ASSERT_FALSE(FileUtils::isFile("/tmp/test_dir_exists"));
    FileUtils::removeDirectory("/tmp/test_dir_exists");
}

// Test: Read and write text file
TEST(read_write_text) {
    std::string content = "Hello, World!\nThis is a test.";
    auto writeResult = FileUtils::writeText("/tmp/test_read_write.txt", content);
    ASSERT_TRUE(writeResult);

    auto readResult = FileUtils::readText("/tmp/test_read_write.txt");
    ASSERT_TRUE(readResult);
    ASSERT_EQ(readResult.value, content);

    FileUtils::remove("/tmp/test_read_write.txt");
}

// Test: Read and write binary file
TEST(read_write_binary) {
    std::vector<unsigned char> data = {0x00, 0x01, 0x02, 0xFF, 0xFE};
    auto writeResult = FileUtils::writeBinary("/tmp/test_binary.bin", data);
    ASSERT_TRUE(writeResult);

    auto readResult = FileUtils::readBinary("/tmp/test_binary.bin");
    ASSERT_TRUE(readResult);
    ASSERT_EQ(readResult.value.size(), data.size());
    for (size_t i = 0; i < data.size(); ++i) {
        ASSERT_EQ(readResult.value[i], data[i]);
    }

    FileUtils::remove("/tmp/test_binary.bin");
}

// Test: Read and write lines
TEST(read_write_lines) {
    std::vector<std::string> lines = {"Line 1", "Line 2", "Line 3"};
    auto writeResult = FileUtils::writeLines("/tmp/test_lines.txt", lines);
    ASSERT_TRUE(writeResult);

    auto readResult = FileUtils::readLines("/tmp/test_lines.txt");
    ASSERT_TRUE(readResult);
    ASSERT_EQ(readResult.value.size(), lines.size());
    for (size_t i = 0; i < lines.size(); ++i) {
        ASSERT_EQ(readResult.value[i], lines[i]);
    }

    FileUtils::remove("/tmp/test_lines.txt");
}

// Test: Append text to file
TEST(append_text) {
    FileUtils::writeText("/tmp/test_append.txt", "First line\n");
    auto appendResult = FileUtils::appendText("/tmp/test_append.txt", "Second line\n");
    ASSERT_TRUE(appendResult);

    auto readResult = FileUtils::readText("/tmp/test_append.txt");
    ASSERT_TRUE(readResult);
    ASSERT_EQ(readResult.value, "First line\nSecond line\n");

    FileUtils::remove("/tmp/test_append.txt");
}

// Test: File size
TEST(file_size) {
    std::string content = "Hello, World!";
    FileUtils::writeText("/tmp/test_size.txt", content);
    ASSERT_EQ(FileUtils::getSize("/tmp/test_size.txt"), content.size());
    ASSERT_EQ(FileUtils::getSize("/tmp/nonexistent.txt"), 0);
    FileUtils::remove("/tmp/test_size.txt");
}

// Test: File info
TEST(file_info) {
    FileUtils::writeText("/tmp/test_info.txt", "test content");
    FileInfo info = FileUtils::getInfo("/tmp/test_info.txt");

    ASSERT_EQ(info.name, "test_info.txt");
    ASSERT_EQ(info.extension, "txt");
    ASSERT_EQ(info.size, 12); // "test content"
    ASSERT_TRUE(info.isFile);
    ASSERT_FALSE(info.isDirectory);
    ASSERT_TRUE(info.readable);

    FileUtils::remove("/tmp/test_info.txt");
}

// Test: Copy file
TEST(copy_file) {
    FileUtils::writeText("/tmp/test_copy_src.txt", "copy me");
    auto copyResult = FileUtils::copy("/tmp/test_copy_src.txt", "/tmp/test_copy_dst.txt");
    ASSERT_TRUE(copyResult);
    ASSERT_TRUE(FileUtils::exists("/tmp/test_copy_dst.txt"));

    auto readResult = FileUtils::readText("/tmp/test_copy_dst.txt");
    ASSERT_EQ(readResult.value, "copy me");

    FileUtils::remove("/tmp/test_copy_src.txt");
    FileUtils::remove("/tmp/test_copy_dst.txt");
}

// Test: Move file
TEST(move_file) {
    FileUtils::writeText("/tmp/test_move_src.txt", "move me");
    auto moveResult = FileUtils::move("/tmp/test_move_src.txt", "/tmp/test_move_dst.txt");
    ASSERT_TRUE(moveResult);
    ASSERT_FALSE(FileUtils::exists("/tmp/test_move_src.txt"));
    ASSERT_TRUE(FileUtils::exists("/tmp/test_move_dst.txt"));

    auto readResult = FileUtils::readText("/tmp/test_move_dst.txt");
    ASSERT_EQ(readResult.value, "move me");

    FileUtils::remove("/tmp/test_move_dst.txt");
}

// Test: Remove file
TEST(remove_file) {
    FileUtils::writeText("/tmp/test_remove.txt", "delete me");
    ASSERT_TRUE(FileUtils::exists("/tmp/test_remove.txt"));

    auto removeResult = FileUtils::remove("/tmp/test_remove.txt");
    ASSERT_TRUE(removeResult);
    ASSERT_FALSE(FileUtils::exists("/tmp/test_remove.txt"));
}

// Test: Touch file
TEST(touch_file) {
    // Create new file
    auto touchResult = FileUtils::touch("/tmp/test_touch.txt");
    ASSERT_TRUE(touchResult);
    ASSERT_TRUE(FileUtils::exists("/tmp/test_touch.txt"));

    // Update existing file
    std::time_t before = FileUtils::getModifiedTime("/tmp/test_touch.txt");
    sleep(1);
    FileUtils::touch("/tmp/test_touch.txt");
    std::time_t after = FileUtils::getModifiedTime("/tmp/test_touch.txt");
    ASSERT_TRUE(after >= before);

    FileUtils::remove("/tmp/test_touch.txt");
}

// Test: Ensure directory
TEST(ensure_directory) {
    ASSERT_TRUE(FileUtils::ensureDirectory("/tmp/test_nested/deep/dir"));
    ASSERT_TRUE(FileUtils::exists("/tmp/test_nested/deep/dir"));
    ASSERT_TRUE(FileUtils::isDirectory("/tmp/test_nested/deep/dir"));

    FileUtils::removeDirectory("/tmp/test_nested", true);
}

// Test: List directory entries
TEST(list_entries) {
    FileUtils::ensureDirectory("/tmp/test_list");
    FileUtils::writeText("/tmp/test_list/file1.txt", "1");
    FileUtils::writeText("/tmp/test_list/file2.txt", "2");
    FileUtils::ensureDirectory("/tmp/test_list/subdir");

    auto entries = FileUtils::listEntries("/tmp/test_list");
    ASSERT_EQ(entries.size(), 3);

    auto files = FileUtils::listFiles("/tmp/test_list");
    ASSERT_EQ(files.size(), 2);

    auto dirs = FileUtils::listDirectories("/tmp/test_list");
    ASSERT_EQ(dirs.size(), 1);

    FileUtils::removeDirectory("/tmp/test_list", true);
}

// Test: Path utilities
TEST(path_utilities) {
    ASSERT_EQ(FileUtils::joinPath("/home", "user"), "/home/user");
    ASSERT_EQ(FileUtils::joinPath("/home/", "user"), "/home/user");
    ASSERT_EQ(FileUtils::joinPath("/home", "/user"), "/home/user");

    ASSERT_EQ(FileUtils::getDirectory("/home/user/file.txt"), "/home/user");
    ASSERT_EQ(FileUtils::getDirectory("file.txt"), ".");
    ASSERT_EQ(FileUtils::getDirectory("/file.txt"), "/");

    ASSERT_EQ(FileUtils::getFilename("/home/user/file.txt"), "file.txt");
    ASSERT_EQ(FileUtils::getFilename("file.txt"), "file.txt");

    ASSERT_EQ(FileUtils::getBasename("/home/user/file.txt"), "file");
    ASSERT_EQ(FileUtils::getBasename("file.tar.gz"), "file.tar");

    ASSERT_EQ(FileUtils::getExtension("/home/user/file.txt"), "txt");
    ASSERT_EQ(FileUtils::getExtension("file.TXT"), "txt"); // lowercase
    ASSERT_EQ(FileUtils::getExtension("file"), "");

    ASSERT_EQ(FileUtils::normalizePath("/home/../user/./file"), "/user/file");
    ASSERT_EQ(FileUtils::normalizePath("./a/b/../c"), "a/c");

    ASSERT_TRUE(FileUtils::isAbsolutePath("/home/user"));
    ASSERT_FALSE(FileUtils::isAbsolutePath("user"));
}

// Test: Format size
TEST(format_size) {
    ASSERT_EQ(FileUtils::formatSize(0), "0.00 B");
    ASSERT_EQ(FileUtils::formatSize(512), "512.00 B");
    ASSERT_EQ(FileUtils::formatSize(1024), "1.00 KB");
    ASSERT_EQ(FileUtils::formatSize(1536), "1.50 KB");
    ASSERT_EQ(FileUtils::formatSize(1024 * 1024), "1.00 MB");
    ASSERT_EQ(FileUtils::formatSize(1024 * 1024 * 1024), "1.00 GB");
}

// Test: Error handling
TEST(error_handling) {
    // Read non-existent file
    auto result = FileUtils::readText("/tmp/nonexistent_xyz.txt");
    ASSERT_FALSE(result);
    ASSERT_FALSE(result.error.empty());

    // Copy non-existent file
    auto copyResult = FileUtils::copy("/tmp/nonexistent_xyz.txt", "/tmp/dest.txt");
    ASSERT_FALSE(copyResult);

    // Remove non-existent file
    auto removeResult = FileUtils::remove("/tmp/nonexistent_xyz.txt");
    ASSERT_FALSE(removeResult);
}

// Test: Remove directory
TEST(remove_directory) {
    FileUtils::ensureDirectory("/tmp/test_remove_dir/sub");
    FileUtils::writeText("/tmp/test_remove_dir/file.txt", "test");
    FileUtils::writeText("/tmp/test_remove_dir/sub/file.txt", "test");

    // Non-recursive should fail (directory not empty)
    auto result = FileUtils::removeDirectory("/tmp/test_remove_dir");
    ASSERT_FALSE(result);

    // Recursive should succeed
    result = FileUtils::removeDirectory("/tmp/test_remove_dir", true);
    ASSERT_TRUE(result);
    ASSERT_FALSE(FileUtils::exists("/tmp/test_remove_dir"));
}

// Test: File permissions
TEST(file_permissions) {
    FileUtils::writeText("/tmp/test_perms.txt", "test");
    ASSERT_TRUE(FileUtils::isReadable("/tmp/test_perms.txt"));
    ASSERT_TRUE(FileUtils::isWritable("/tmp/test_perms.txt"));

    // Check that non-existent file returns false
    ASSERT_FALSE(FileUtils::isReadable("/tmp/nonexistent_xyz.txt"));
    ASSERT_FALSE(FileUtils::isWritable("/tmp/nonexistent_xyz.txt"));

    FileUtils::remove("/tmp/test_perms.txt");
}

int main() {
    std::cout << "========================================" << std::endl;
    std::cout << "C++ File Utilities Test Suite" << std::endl;
    std::cout << "========================================" << std::endl;
    std::cout << std::endl;

    RUN_TEST(file_exists);
    RUN_TEST(directory_exists);
    RUN_TEST(read_write_text);
    RUN_TEST(read_write_binary);
    RUN_TEST(read_write_lines);
    RUN_TEST(append_text);
    RUN_TEST(file_size);
    RUN_TEST(file_info);
    RUN_TEST(copy_file);
    RUN_TEST(move_file);
    RUN_TEST(remove_file);
    RUN_TEST(touch_file);
    RUN_TEST(ensure_directory);
    RUN_TEST(list_entries);
    RUN_TEST(path_utilities);
    RUN_TEST(format_size);
    RUN_TEST(error_handling);
    RUN_TEST(remove_directory);
    RUN_TEST(file_permissions);

    std::cout << std::endl;
    std::cout << "========================================" << std::endl;
    std::cout << "Results: " << tests_passed << "/" << tests_run << " tests passed" << std::endl;
    std::cout << "========================================" << std::endl;

    return (tests_passed == tests_run) ? 0 : 1;
}
