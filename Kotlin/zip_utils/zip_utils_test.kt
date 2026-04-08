package zip_utils

import java.io.File
import java.nio.file.Files

/**
 * ZipUtils Test Suite
 * Comprehensive tests for ZIP compression and decompression functionality
 */
fun main() {
    println("Running ZipUtils Tests...")
    println("=".repeat(60))

    var passed = 0
    var failed = 0
    val tempDir = Files.createTempDirectory("zip_test").toFile()

    // Test 1: Zip a single file
    try {
        val testFile = File(tempDir, "test.txt")
        testFile.writeText("Hello, World!")
        val zipFile = File(tempDir, "test.zip")

        val result = zipFile(testFile.absolutePath, zipFile.absolutePath)

        if (result.success && zipFile.exists()) {
            println("✓ Test 1: Zip single file")
            passed++
        } else {
            println("✗ Test 1: Failed - ${result.message}")
            failed++
        }
    } catch (e: Exception) {
        println("✗ Test 1: Exception - ${e.message}")
        failed++
    }

    // Test 2: Unzip a file
    try {
        val testFile = File(tempDir, "test2.txt")
        testFile.writeText("Test content for unzip")
        val zipFile = File(tempDir, "test2.zip")
        val extractDir = File(tempDir, "extracted")

        zipFile(testFile.absolutePath, zipFile.absolutePath)
        val result = unzip(zipFile.absolutePath, extractDir.absolutePath)

        val extractedFile = File(extractDir, "test2.txt")
        if (result.success && extractedFile.exists() && extractedFile.readText() == "Test content for unzip") {
            println("✓ Test 2: Unzip file")
            passed++
        } else {
            println("✗ Test 2: Failed - ${result.message}")
            failed++
        }
    } catch (e: Exception) {
        println("✗ Test 2: Exception - ${e.message}")
        failed++
    }

    // Test 3: Zip non-existent file
    try {
        val result = zipFile("/non/existent/file.txt", File(tempDir, "out.zip").absolutePath)

        if (!result.success) {
            println("✓ Test 3: Handle non-existent file")
            passed++
        } else {
            println("✗ Test 3: Should have failed for non-existent file")
            failed++
        }
    } catch (e: Exception) {
        println("✗ Test 3: Exception - ${e.message}")
        failed++
    }

    // Test 4: Zip directory
    try {
        val sourceDir = File(tempDir, "source_dir")
        sourceDir.mkdirs()
        File(sourceDir, "file1.txt").writeText("Content 1")
        File(sourceDir, "file2.txt").writeText("Content 2")

        val zipFile = File(tempDir, "dir_test.zip")
        val result = zipDirectory(sourceDir.absolutePath, zipFile.absolutePath)

        if (result.success && result.entriesProcessed == 2) {
            println("✓ Test 4: Zip directory")
            passed++
        } else {
            println("✗ Test 4: Failed - ${result.message}")
            failed++
        }
    } catch (e: Exception) {
        println("✗ Test 4: Exception - ${e.message}")
        failed++
    }

    // Test 5: Compression levels
    try {
        val testFile = File(tempDir, "compress_test.txt")
        testFile.writeText("A".repeat(1000))
        val zipFile = File(tempDir, "compress_test.zip")

        val result = zipFile(
            testFile.absolutePath,
            zipFile.absolutePath,
            compressionLevel = CompressionLevel.BEST
        )

        if (result.success) {
            println("✓ Test 5: Compression levels")
            passed++
        } else {
            println("✗ Test 5: Failed - ${result.message}")
            failed++
        }
    } catch (e: Exception) {
        println("✗ Test 5: Exception - ${e.message}")
        failed++
    }

    // Test 6: Empty directory handling
    try {
        val emptyDir = File(tempDir, "empty_dir")
        emptyDir.mkdirs()
        val zipFile = File(tempDir, "empty_test.zip")

        val result = zipDirectory(emptyDir.absolutePath, zipFile.absolutePath)

        if (!result.success) {
            println("✓ Test 6: Handle empty directory")
            passed++
        } else {
            println("✗ Test 6: Should report empty directory")
            failed++
        }
    } catch (e: Exception) {
        println("✗ Test 6: Exception - ${e.message}")
        failed++
    }

    // Test 7: Zip multiple files
    try {
        val file1 = File(tempDir, "multi1.txt").apply { writeText("File 1") }
        val file2 = File(tempDir, "multi2.txt").apply { writeText("File 2") }
        val zipFile = File(tempDir, "multi_test.zip")

        val result = zipFiles(
            listOf(file1.absolutePath, file2.absolutePath),
            zipFile.absolutePath
        )

        if (result.success && result.entriesProcessed == 2) {
            println("✓ Test 7: Zip multiple files")
            passed++
        } else {
            println("✗ Test 7: Failed - ${result.message}")
            failed++
        }
    } catch (e: Exception) {
        println("✗ Test 7: Exception - ${e.message}")
        failed++
    }

    // Test 8: Custom entry name
    try {
        val testFile = File(tempDir, "original.txt")
        testFile.writeText("Custom name test")
        val zipFile = File(tempDir, "custom_name.zip")

        val result = zipFile(
            testFile.absolutePath,
            zipFile.absolutePath,
            entryName = "custom/renamed.txt"
        )

        if (result.success) {
            println("✓ Test 8: Custom entry name")
            passed++
        } else {
            println("✗ Test 8: Failed - ${result.message}")
            failed++
        }
    } catch (e: Exception) {
        println("✗ Test 8: Exception - ${e.message}")
        failed++
    }

    // Test 9: Binary file handling
    try {
        val binaryFile = File(tempDir, "binary.dat")
        binaryFile.writeBytes(ByteArray(100) { it.toByte() })
        val zipFile = File(tempDir, "binary_test.zip")

        val result = zipFile(binaryFile.absolutePath, zipFile.absolutePath)

        if (result.success) {
            println("✓ Test 9: Binary file handling")
            passed++
        } else {
            println("✗ Test 9: Failed - ${result.message}")
            failed++
        }
    } catch (e: Exception) {
        println("✗ Test 9: Exception - ${e.message}")
        failed++
    }

    // Test 10: Large file handling
    try {
        val largeFile = File(tempDir, "large.txt")
        largeFile.writeText("X".repeat(100000))
        val zipFile = File(tempDir, "large_test.zip")

        val result = zipFile(largeFile.absolutePath, zipFile.absolutePath)

        if (result.success && result.bytesProcessed == 100000L) {
            println("✓ Test 10: Large file handling")
            passed++
        } else {
            println("✗ Test 10: Failed - ${result.message}")
            failed++
        }
    } catch (e: Exception) {
        println("✗ Test 10: Exception - ${e.message}")
        failed++
    }

    // Test 11: Exclude patterns
    try {
        val sourceDir = File(tempDir, "exclude_dir")
        sourceDir.mkdirs()
        File(sourceDir, "keep.txt").writeText("Keep")
        File(sourceDir, "skip.tmp").writeText("Skip")
        File(sourceDir, "skip.log").writeText("Skip log")

        val zipFile = File(tempDir, "exclude_test.zip")
        val result = zipDirectory(
            sourceDir.absolutePath,
            zipFile.absolutePath,
            excludePatterns = listOf("*.tmp", "*.log")
        )

        if (result.success && result.entriesProcessed == 1) {
            println("✓ Test 11: Exclude patterns")
            passed++
        } else {
            println("✗ Test 11: Failed - processed ${result.entriesProcessed} entries")
            failed++
        }
    } catch (e: Exception) {
        println("✗ Test 11: Exception - ${e.message}")
        failed++
    }

    // Test 12: Unzip non-existent file
    try {
        val result = unzip("/non/existent/file.zip", tempDir.absolutePath)

        if (!result.success) {
            println("✓ Test 12: Handle non-existent zip file")
            passed++
        } else {
            println("✗ Test 12: Should have failed for non-existent file")
            failed++
        }
    } catch (e: Exception) {
        println("✗ Test 12: Exception - ${e.message}")
        failed++
    }

    // Test 13: ZipResult data class
    try {
        val result1 = ZipResult(true, "Success", 5, 1000)
        val result2 = ZipResult(false, "Failed")

        if (result1.success && result1.entriesProcessed == 5 && result1.bytesProcessed == 1000L &&
            !result2.success && result2.entriesProcessed == 0) {
            println("✓ Test 13: ZipResult data class")
            passed++
        } else {
            println("✗ Test 13: ZipResult data class validation failed")
            failed++
        }
    } catch (e: Exception) {
        println("✗ Test 13: Exception - ${e.message}")
        failed++
    }

    // Test 14: CompressionLevel enum
    try {
        val none = CompressionLevel.NONE
        val best = CompressionLevel.BEST

        if (none.level == 0 && best.level == 9) {
            println("✓ Test 14: CompressionLevel enum")
            passed++
        } else {
            println("✗ Test 14: CompressionLevel values incorrect")
            failed++
        }
    } catch (e: Exception) {
        println("✗ Test 14: Exception - ${e.message}")
        failed++
    }

    // Test 15: Preserve paths option
    try {
        val file1 = File(tempDir, "path_test1.txt").apply { writeText("File 1") }
        val file2 = File(tempDir, "path_test2.txt").apply { writeText("File 2") }
        val zipFile = File(tempDir, "preserve_test.zip")

        val result = zipFiles(
            listOf(file1.absolutePath, file2.absolutePath),
            zipFile.absolutePath,
            preservePaths = true
        )

        if (result.success) {
            println("✓ Test 15: Preserve paths option")
            passed++
        } else {
            println("✗ Test 15: Failed - ${result.message}")
            failed++
        }
    } catch (e: Exception) {
        println("✗ Test 15: Exception - ${e.message}")
        failed++
    }

    // Cleanup
    tempDir.deleteRecursively()

    // Report
    println("=".repeat(60))
    println("Tests completed: $passed passed, $failed failed")
    if (failed == 0) {
        println("All tests passed!")
    } else {
        println("$failed test(s) failed.")
    }
    println("=".repeat(60))

    if (failed > 0) {
        kotlin.system.exitProcess(1)
    }
}