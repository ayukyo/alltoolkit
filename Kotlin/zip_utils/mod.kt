package zip_utils

import java.io.*
import java.nio.file.*
import java.util.zip.*

/**
 * ZipUtils - A comprehensive ZIP file compression and decompression utility for Kotlin
 *
 * This module provides functions for creating, extracting, and manipulating ZIP archives
 * with support for compression levels, entry filtering, and various archive operations.
 *
 * Features:
 * - Create ZIP archives from files and directories
 * - Extract ZIP archives with preservation of directory structure
 * - Add/remove/list entries in existing ZIP archives
 * - Support for different compression levels (NONE, FASTEST, DEFAULT, BEST)
 * - Stream-based operations for memory efficiency
 * - Progress tracking for large operations
 * - Entry filtering with glob patterns
 *
 * @author AllToolkit
 * @version 1.0.0
 */

/**
 * Compression level constants
 */
enum class CompressionLevel(val level: Int) {
    NONE(Deflater.NO_COMPRESSION),
    FASTEST(Deflater.BEST_SPEED),
    DEFAULT(Deflater.DEFAULT_COMPRESSION),
    BEST(Deflater.BEST_COMPRESSION)
}

/**
 * Result class for ZIP operations
 */
data class ZipResult(
    val success: Boolean,
    val message: String,
    val entriesProcessed: Int = 0,
    val bytesProcessed: Long = 0
)

/**
 * Entry information class
 */
data class ZipEntryInfo(
    val name: String,
    val size: Long,
    val compressedSize: Long,
    val isDirectory: Boolean,
    val lastModified: Long,
    val crc: Long
)

/**
 * Progress callback interface
 */
fun interface ZipProgressCallback {
    fun onProgress(current: Long, total: Long, entryName: String)
}

/**
 * Create a ZIP archive from a single file
 *
 * @param sourceFile Path to the file to compress
 * @param zipFile Path to the output ZIP file
 * @param compressionLevel Compression level (default: DEFAULT)
 * @param entryName Optional custom entry name in the archive (default: source filename)
 * @return ZipResult with operation status
 */
fun zipFile(
    sourceFile: String,
    zipFile: String,
    compressionLevel: CompressionLevel = CompressionLevel.DEFAULT,
    entryName: String? = null
): ZipResult {
    return try {
        val source = File(sourceFile)
        if (!source.exists()) {
            return ZipResult(false, "Source file does not exist: $sourceFile")
        }
        if (!source.isFile) {
            return ZipResult(false, "Source is not a file: $sourceFile")
        }

        FileOutputStream(zipFile).use { fos ->
            ZipOutputStream(BufferedOutputStream(fos)).use { zos ->
                zos.setLevel(compressionLevel.level)
                val name = entryName ?: source.name
                addFileToZip(source, name, zos)
            }
        }

        ZipResult(true, "File compressed successfully", 1, source.length())
    } catch (e: Exception) {
        ZipResult(false, "Error compressing file: ${e.message}")
    }
}

/**
 * Create a ZIP archive from a directory
 *
 * @param sourceDir Path to the directory to compress
 * @param zipFile Path to the output ZIP file
 * @param compressionLevel Compression level (default: DEFAULT)
 * @param includeRoot Whether to include the root directory name in the archive (default: true)
 * @param excludePatterns List of glob patterns to exclude (e.g., ["*.tmp", "*.log"])
 * @return ZipResult with operation status
 */
fun zipDirectory(
    sourceDir: String,
    zipFile: String,
    compressionLevel: CompressionLevel = CompressionLevel.DEFAULT,
    includeRoot: Boolean = true,
    excludePatterns: List<String> = emptyList()
): ZipResult {
    return try {
        val source = File(sourceDir)
        if (!source.exists()) {
            return ZipResult(false, "Source directory does not exist: $sourceDir")
        }
        if (!source.isDirectory) {
            return ZipResult(false, "Source is not a directory: $sourceDir")
        }

        val files = source.walkTopDown().filter { file ->
            file.isFile && excludePatterns.none { pattern ->
                file.name.matches(Regex(pattern.replace("*", ".*").replace("?", ".")))
            }
        }.toList()

        if (files.isEmpty()) {
            return ZipResult(false, "No files to compress in directory: $sourceDir")
        }

        val totalSize = files.sumOf { it.length() }
        var entryCount = 0

        FileOutputStream(zipFile).use { fos ->
            ZipOutputStream(BufferedOutputStream(fos)).use { zos ->
                zos.setLevel(compressionLevel.level)

                files.forEach { file ->
                    val relativePath = if (includeRoot) {
                        file.relativeTo(source.parentFile ?: source).path
                    } else {
                        file.relativeTo(source).path
                    }.replace(File.separator, "/")

                    addFileToZip(file, relativePath, zos)
                    entryCount++
                }
            }
        }

        ZipResult(true, "Directory compressed successfully", entryCount, totalSize)
    } catch (e: Exception) {
        ZipResult(false, "Error compressing directory: ${e.message}")
    }
}

/**
 * Create a ZIP archive from multiple files
 *
 * @param sourceFiles List of file paths to compress
 * @param zipFile Path to the output ZIP file
 * @param compressionLevel Compression level (default: DEFAULT)
 * @param preservePaths Whether to preserve directory structure (default: false, files stored flat)
 * @return ZipResult with operation status
 */
fun zipFiles(
    sourceFiles: List<String>,
    zipFile: String,
    compressionLevel: CompressionLevel = CompressionLevel.DEFAULT,
    preservePaths: Boolean = false
): ZipResult {
    return try {
        val files = sourceFiles.map { File(it) }.filter { it.exists() && it.isFile }
        if (files.isEmpty()) {
            return ZipResult(false, "No valid files to compress")
        }

        val totalSize = files.sumOf { it.length() }
        var entryCount = 0

        FileOutputStream(zipFile).use { fos ->
            ZipOutputStream(BufferedOutputStream(fos)).use { zos ->
                zos.setLevel(compressionLevel.level)

                files.forEach { file ->
                    val entryName = if (preservePaths) {
                        file.path.replace(File.separator, "/")
                    } else {
                        file.name
                    }
                    addFileToZip(file, entryName, zos)
                    entryCount++
                }
            }
        }

        ZipResult(true, "Files compressed successfully", entryCount, totalSize)
    } catch (e: Exception) {
        ZipResult(false, "Error compressing files: ${e.message}")
    }
}

/**
 * Extract a ZIP archive to a directory
 *
 * @param zipFile Path to the ZIP file
 * @param destDir Path to the destination directory
 * @param overwrite Whether to overwrite existing files (default: true)
 * @param filter Optional filter function to selectively extract entries
 * @return ZipResult with operation status
 */
fun unzip(
    zipFile: String,
    destDir: String,
    overwrite: Boolean = true,
    filter: ((ZipEntryInfo) -> Boolean)? = null
): ZipResult {
    return try {
        val zip = File(zipFile)
        if (!zip.exists()) {
            return ZipResult(false, "ZIP file does not exist: $zipFile")
        }

        val destination = File(destDir)
        destination.mkdirs()

        var entryCount = 0
        var totalBytes = 0L

        ZipInputStream(FileInputStream(zipFile).buffered()).use { zis ->
            var entry: ZipEntry? = zis.nextEntry
            while (entry != null) {
                val entryInfo = ZipEntryInfo(
                    name = entry.name,
                    size = entry.size,
                    compressedSize = entry.compressedSize