/**
 * @file file_utils_example.cpp
 * @brief Example usage of C++ File Utilities
 * @version 1.0.0
 *
 * Demonstrates various file operations using the FileUtils class.
 * Compile with: g++ -std=c++11 -o file_utils_example file_utils_example.cpp
 */

#include <iostream>
#include "../file_utils/mod.hpp"

using namespace alltoolkit;

int main() {
    std::cout << "========================================" << std::endl;
    std::cout << "C++ File Utilities - Example Usage" << std::endl;
    std::cout << "========================================" << std::endl;
    std::cout << std::endl;

    // Example 1: Write and read text file
    std::cout << "Example 1: Write and Read Text File" << std::endl;
    std::cout << "------------------------------------" << std::endl;
    {
        std::string content = "Hello, World!\nThis is a sample text file.\n";
        auto result = FileUtils::writeText("/tmp/example_text.txt", content);
        if (result) {
            std::cout << "✓ File written successfully" << std::endl;

            auto readResult = FileUtils::readText("/tmp/example_text.txt");
            if (readResult) {
                std::cout << "✓ File content:" << std::endl;
                std::cout << readResult.value << std::endl;
            }
        }
        FileUtils::remove("/tmp/example_text.txt");
    }
    std::cout << std::endl;

    // Example 2: Write and read lines
    std::cout << "Example 2: Write and Read Lines" << std::endl;
    std::cout << "--------------------------------" << std::endl;
    {
        std::vector<std::string> lines = {
            "First line",
            "Second line",
            "Third line"
        };
        auto result = FileUtils::writeLines("/tmp/example_lines.txt", lines);
        if (result) {
            std::cout << "✓ Lines written successfully" << std::endl;

            auto readResult = FileUtils::readLines("/tmp/example_lines.txt");
            if (readResult) {
                std::cout << "✓ Lines read:" << std::endl;
                for (size_t i = 0; i < readResult.value.size(); ++i) {
                    std::cout << "  " << (i + 1) << ": " << readResult.value[i] << std::endl;
                }
            }
        }
        FileUtils::remove("/tmp/example_lines.txt");
    }
    std::cout << std::endl;

    // Example 3: File existence and info
    std::cout << "Example 3: File Existence and Info" << std::endl;
    std::cout << "-----------------------------------" << std::endl;
    {
        FileUtils::writeText("/tmp/example_info.txt", "Sample content for info test");

        if (FileUtils::exists("/tmp/example_info.txt")) {
            std::cout << "✓ File exists" << std::endl;
        }

        if (FileUtils::isFile("/tmp/example_info.txt")) {
            std::cout << "✓ Path is a file" << std::endl;
        }

        std::size_t size = FileUtils::getSize("/tmp/example_info.txt");
        std::cout << "✓ File size: " << size << " bytes" << std::endl;

        FileInfo info = FileUtils::getInfo("/tmp/example_info.txt");
        std::cout << "✓ File info:" << std::endl;
        std::cout << "  - Name: " << info.name << std::endl;
        std::cout << "  - Extension: " << info.extension << std::endl;
        std::cout << "  - Directory: " << info.directory << std::endl;
        std::cout << "  - Size: " << info.size << " bytes" << std::endl;
        std::cout << "  - Readable: " << (info.readable ? "Yes" : "No") << std::endl;
        std::cout << "  - Writable: " << (info.writable ? "Yes" : "No") << std::endl;

        FileUtils::remove("/tmp/example_info.txt");
    }
    std::cout << std::endl;

    // Example 4: Copy and move files
    std::cout << "Example 4: Copy and Move Files" << std::endl;
    std::cout << "-------------------------------" << std::endl;
    {
        FileUtils::writeText("/tmp/example_source.txt", "Original content");

        // Copy file
        auto copyResult = FileUtils::copy("/tmp/example_source.txt", "/tmp/example_copy.txt");
        if (copyResult) {
            std::cout << "✓ File copied successfully" << std::endl;
            auto content = FileUtils::readText("/tmp/example_copy.txt");
            std::cout << "  Copy content: " << content.value << std::endl;
        }

        // Move file
        auto moveResult = FileUtils::move("/tmp/example_copy.txt", "/tmp/example_moved.txt");
        if (moveResult) {
            std::cout << "✓ File moved successfully" << std::endl;
            std::cout << "  Original exists: " << (FileUtils::exists("/tmp/example_copy.txt") ? "Yes" : "No") << std::endl;
            std::cout << "  Moved exists: " << (FileUtils::exists("/tmp/example_moved.txt") ? "Yes" : "No") << std::endl;
        }

        FileUtils::remove("/tmp/example_source.txt");
        FileUtils::remove("/tmp/example_moved.txt");
    }
    std::cout << std::endl;

    // Example 5: Directory operations
    std::cout << "Example 5: Directory Operations" << std::endl;
    std::cout << "--------------------------------" << std::endl;
    {
        // Create nested directory
        if (FileUtils::ensureDirectory("/tmp/example_nested/deep/dir")) {
            std::cout << "✓ Nested directory created" << std::endl;
        }

        // Create some files
        FileUtils::writeText("/tmp/example_nested/file1.txt", "File 1");
        FileUtils::writeText("/tmp/example_nested/file2.txt", "File 2");
        FileUtils::writeText("/tmp/example_nested/deep/file3.txt", "File 3");

        // List directory contents
        auto entries = FileUtils::listEntries("/tmp/example_nested");
        std::cout << "✓ Directory entries:" << std::endl;
        for (const auto& entry : entries) {
            std::cout << "  - " << entry << std::endl;
        }

        auto files = FileUtils::listFiles("/tmp/example_nested");
        std::cout << "✓ Files only:" << std::endl;
        for (const auto& file : files) {
            std::cout << "  - " << file << std::endl;
        }

        // Clean up
        FileUtils::removeDirectory("/tmp/example_nested", true);
        std::cout << "✓ Directory removed recursively" << std::endl;
    }
    std::cout << std::endl;

    // Example 6: Path utilities
    std::cout << "Example 6: Path Utilities" << std::endl;
    std::cout << "--------------------------" << std::endl;
    {
        std::string path = "/home/user/documents/file.txt";

        std::cout << "Path: " << path << std::endl;
        std::cout << "  Directory: " << FileUtils::getDirectory(path) << std::endl;
        std::cout << "  Filename: " << FileUtils::getFilename(path) << std::endl;
        std::cout << "  Basename: " << FileUtils::getBasename(path) << std::endl;
        std::cout << "  Extension: " << FileUtils::getExtension(path) << std::endl;

        std::string path1 = "/home/user";
        std::string path2 = "documents/file.txt";
        std::cout << "Join '" << path1 << "' + '" << path2 << "': "
                  << FileUtils::joinPath(path1, path2) << std::endl;

        std::string normalized = FileUtils::normalizePath("/home/../user/./documents");
        std::cout << "Normalized '/home/../user/./documents': " << normalized << std::endl;
    }
    std::cout << std::endl;

    // Example 7: Binary file operations
    std::cout << "Example 7: Binary File Operations" << std::endl;
    std::cout << "----------------------------------" << std::endl;
    {
        std::vector<unsigned char> data = {0x48, 0x65, 0x6C, 0x6C, 0x6F}; // "Hello" in ASCII
        auto writeResult = FileUtils::writeBinary("/tmp/example_binary.bin", data);
        if (writeResult) {
            std::cout << "✓ Binary file written (" << data.size() << " bytes)" << std::endl;

            auto readResult = FileUtils::readBinary("/tmp/example_binary.bin");
            if (readResult) {
                std::cout << "✓ Binary file read (" << readResult.value.size() << " bytes)" << std::endl;
                std::cout << "  Bytes: ";
                for (auto byte : readResult.value) {
                    std::cout << std::hex << std::uppercase << (int)byte << " ";
                }
                std::cout << std::dec << std::endl;
            }
        }
        FileUtils::remove("/tmp/example_binary.bin");
    }
    std::cout << std::endl;

    // Example 8: File size formatting
    std::cout << "Example 8: File Size Formatting" << std::endl;
    std::cout << "--------------------------------" << std::endl;
    {
        std::cout << "  0 bytes = " << FileUtils::formatSize(0) << std::endl;
        std::cout << "  512 bytes = " << FileUtils::formatSize(512) << std::endl;
        std::cout << "  1024 bytes = " << FileUtils::formatSize(1024) << std::endl;
        std::cout << "  1536 bytes = " << FileUtils::formatSize(1536) << std::endl;
        std::cout << "  1048576 bytes = " << FileUtils::formatSize(1048576) << std::endl;
        std::cout << "  1073741824 bytes = " << FileUtils::formatSize(1073741824) << std::endl;
    }
    std::cout << std::endl;

    // Example 9: Error handling
    std::cout << "Example 9: Error Handling" << std::endl;
    std::cout << "--------------------------" << std::endl;
    {
        auto result = FileUtils::readText("/tmp/nonexistent_file_xyz.txt");
        if (!result) {
            std::cout << "✓ Error handled: " << result.error << std::endl;
        }

        auto copyResult = FileUtils::copy("/tmp/nonexistent_source.txt", "/tmp/dest.txt");
        if (!copyResult) {
            std::cout << "✓ Copy error handled: " << copyResult.error << std::endl;
        }
    }
    std::cout << std::endl;

    // Example 10: Append to file
    std::cout << "Example 10: Append to File" << std::endl;
    std::cout << "---------------------------" << std::endl;
    {
        FileUtils::writeText("/tmp/example_append.txt", "First line\n");
        FileUtils::appendText("/tmp/example_append.txt", "Second line\n");
        FileUtils::appendText("/tmp/example_append.txt", "Third line\n");

        auto content = FileUtils::readText("/tmp/example_append.txt");
        if (content) {
            std::cout << "✓ Appended file content:" << std::endl;
            std::cout << content.value;
        }
        FileUtils::remove("/tmp/example_append.txt");
    }
    std::cout << std::endl;

    std::cout << "========================================" << std::endl;
    std::cout << "All examples completed successfully!" << std::endl;
    std::cout << "========================================" << std::endl;

    return 0;
}
