/**
 * @file mod.hpp
 * @brief C++ File Utilities - Zero-dependency file operations library
 * @version 1.0.0
 *
 * A comprehensive file utility module providing common file operations
 * with zero external dependencies. Uses only C++11 standard library.
 */

#ifndef ALLTOOLKIT_FILE_UTILS_HPP
#define ALLTOOLKIT_FILE_UTILS_HPP

#include <algorithm>
#include <cctype>
#include <cerrno>
#include <chrono>
#include <cstdio>
#include <cstring>
#include <ctime>
#include <dirent.h>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <sstream>
#include <stack>
#include <string>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>
#include <utime.h>
#include <vector>

namespace alltoolkit {

/**
 * @brief File information structure
 */
struct FileInfo {
    std::string path;
    std::string name;
    std::string extension;
    std::string directory;
    std::size_t size;
    std::time_t modified;
    std::time_t accessed;
    std::time_t created;
    bool isDirectory;
    bool isFile;
    bool isSymlink;
    bool readable;
    bool writable;
    bool executable;

    FileInfo() : size(0), modified(0), accessed(0), created(0),
                 isDirectory(false), isFile(false), isSymlink(false),
                 readable(false), writable(false), executable(false) {}
};

/**
 * @brief Result type for file operations
 */
template<typename T>
struct FileResult {
    bool success;
    T value;
    std::string error;

    FileResult() : success(false) {}
    FileResult(T v) : success(true), value(v) {}
    FileResult(bool s, const std::string& e) : success(s), error(e) {}

    operator bool() const { return success; }
};

/**
 * @brief File utilities class
 */
class FileUtils {
public:
    //=========================================================================
    // Path Utilities (declared first for use by other methods)
    //=========================================================================

    static std::string joinPath(const std::string& base, const std::string& path) {
        if (base.empty()) return path;
        if (path.empty()) return base;
        if (path[0] == '/') return base + path;
        if (base[base.size() - 1] == '/') return base + path;
        return base + "/" + path;
    }

    static std::string getDirectory(const std::string& filepath) {
        size_t pos = filepath.find_last_of("/");
        if (pos == std::string::npos) return ".";
        if (pos == 0) return "/";
        return filepath.substr(0, pos);
    }

    static std::string getFilename(const std::string& filepath) {
        size_t pos = filepath.find_last_of("/");
        if (pos == std::string::npos) return filepath;
        return filepath.substr(pos + 1);
    }

    static std::string getBasename(const std::string& filepath) {
        std::string filename = getFilename(filepath);
        size_t pos = filename.find_last_of(".");
        if (pos == std::string::npos || pos == 0) return filename;
        return filename.substr(0, pos);
    }

    static std::string getExtension(const std::string& filepath) {
        std::string filename = getFilename(filepath);
        size_t pos = filename.find_last_of(".");
        if (pos == std::string::npos || pos == 0) return "";
        std::string ext = filename.substr(pos + 1);
        std::transform(ext.begin(), ext.end(), ext.begin(), ::tolower);
        return ext;
    }

    static std::string normalizePath(const std::string& filepath) {
        std::string result;
        std::vector<std::string> parts;
        std::istringstream stream(filepath);
        std::string part;
        while (std::getline(stream, part, '/')) {
            if (part == ".." && !parts.empty() && parts.back() != "..") {
                parts.pop_back();
            } else if (!part.empty() && part != ".") {
                parts.push_back(part);
            }
        }
        for (size_t i = 0; i < parts.size(); ++i) {
            if (i > 0 || filepath[0] == '/') result += "/";
            result += parts[i];
        }
        if (result.empty()) return ".";
        if (filepath[0] == '/' && result[0] != '/') result = "/" + result;
        return result;
    }

    static bool isAbsolutePath(const std::string& filepath) {
        return !filepath.empty() && filepath[0] == '/';
    }

    //=========================================================================
    // Directory Operations (declared early for use by file writing)
    //=========================================================================

    static bool ensureDirectory(const std::string& dirpath, mode_t mode = 0755) {
        if (dirpath.empty() || exists(dirpath)) return true;
        std::string parent = getDirectory(dirpath);
        if (!parent.empty() && parent != dirpath) {
            if (!ensureDirectory(parent, mode)) return false;
        }
        return mkdir(dirpath.c_str(), mode) == 0 || errno == EEXIST;
    }

    //=========================================================================
    // File Reading Operations
    //=========================================================================

    static FileResult<std::string> readText(const std::string& filepath) {
        std::ifstream file(filepath, std::ios::in | std::ios::binary);
        if (!file.is_open()) {
            return FileResult<std::string>(false, "Failed to open file: " + filepath);
        }
        std::string content((std::istreambuf_iterator<char>(file)),
                            std::istreambuf_iterator<char>());
        file.close();
        return FileResult<std::string>(content);
    }

    static FileResult<std::vector<std::string>> readLines(const std::string& filepath) {
        auto result = readText(filepath);
        if (!result) return FileResult<std::vector<std::string>>(false, result.error);
        std::vector<std::string> lines;
        std::istringstream stream(result.value);
        std::string line;
        while (std::getline(stream, line)) lines.push_back(line);
        return FileResult<std::vector<std::string>>(lines);
    }

    static FileResult<std::vector<unsigned char>> readBinary(const std::string& filepath) {
        std::ifstream file(filepath, std::ios::in | std::ios::binary);
        if (!file.is_open()) {
            return FileResult<std::vector<unsigned char>>(false, "Failed to open file: " + filepath);
        }
        std::vector<unsigned char> data((std::istreambuf_iterator<char>(file)),
                                        std::istreambuf_iterator<char>());
        file.close();
        return FileResult<std::vector<unsigned char>>(data);
    }

    //=========================================================================
    // File Writing Operations
    //=========================================================================

    static FileResult<bool> writeText(const std::string& filepath,
                                       const std::string& content,
                                       bool append = false) {
        ensureDirectory(getDirectory(filepath));
        std::ios::openmode mode = std::ios::out | std::ios::binary;
        if (append) mode |= std::ios::app;
        std::ofstream file(filepath, mode);
        if (!file.is_open()) {
            return FileResult<bool>(false, "Failed to create file: " + filepath);
        }
        file.write(content.c_str(), content.size());
        bool success = file.good();
        file.close();
        return success ? FileResult<bool>(true) : FileResult<bool>(false, "Failed to write to file: " + filepath);
    }

    static FileResult<bool> writeLines(const std::string& filepath,
                                        const std::vector<std::string>& lines,
                                        const std::string& lineEnding = "\n") {
        std::string content;
        for (size_t i = 0; i < lines.size(); ++i) {
            content += lines[i];
            if (i < lines.size() - 1) content += lineEnding;
        }
        return writeText(filepath, content);
    }

    static FileResult<bool> writeBinary(const std::string& filepath,
                                         const std::vector<unsigned char>& data) {
        ensureDirectory(getDirectory(filepath));
        std::ofstream file(filepath, std::ios::out | std::ios::binary);
        if (!file.is_open()) {
            return FileResult<bool>(false, "Failed to create file: " + filepath);
        }
        file.write(reinterpret_cast<const char*>(data.data()), data.size());
        bool success = file.good();
        file.close();
        return success ? FileResult<bool>(true) : FileResult<bool>(false, "Failed to write to file: " + filepath);
    }

    static FileResult<bool> appendText(const std::string& filepath, const std::string& content) {
        return writeText(filepath, content, true);
    }

    //=========================================================================
    // File Checks
    //=========================================================================

    static bool exists(const std::string& filepath) {
        struct stat st;
        return stat(filepath.c_str(), &st) == 0;
    }

    static bool isFile(const std::string& filepath) {
        struct stat st;
        if (stat(filepath.c_str(), &st) != 0) return false;
        return S_ISREG(st.st_mode);
    }

    static bool isDirectory(const std::string& filepath) {
        struct stat st;
        if (stat(filepath.c_str(), &st) != 0) return false;
        return S_ISDIR(st.st_mode);
    }

    static bool isSymlink(const std::string& filepath) {
        struct stat st;
        if (lstat(filepath.c_str(), &st) != 0) return false;
        return S_ISLNK(st.st_mode);
    }

    static bool isReadable(const std::string& filepath) {
        return access(filepath.c_str(), R_OK) == 0;
    }

    static bool isWritable(const std::string& filepath) {
        return access(filepath.c_str(), W_OK) == 0;
    }

    static bool isExecutable(const std::string& filepath) {
        return access(filepath.c_str(), X_OK) == 0;
    }

    //=========================================================================
    // File Info
    //=========================================================================

    static std::size_t getSize(const std::string& filepath) {
        struct stat st;
        if (stat(filepath.c_str(), &st) != 0) return 0;
        return static_cast<std::size_t>(st.st_size);
    }

    static std::time_t getModifiedTime(const std::string& filepath) {
        struct stat st;
        if (stat(filepath.c_str(), &st) != 0) return 0;
        return st.st_mtime;
    }

    static FileInfo getInfo(const std::string& filepath) {
        FileInfo info;
        info.path = filepath;
        info.name = getFilename(filepath);
        info.extension = getExtension(filepath);
        info.directory = getDirectory(filepath);

        struct stat st;
        if (stat(filepath.c_str(), &st) == 0) {
            info.size = static_cast<std::size_t>(st.st_size);
            info.modified = st.st_mtime;
            info.accessed = st.st_atime;
            info.created = st.st_ctime;
            info.isDirectory = S_ISDIR(st.st_mode);
            info.isFile = S_ISREG(st.st_mode);
            info.readable = isReadable(filepath);
            info.writable = isWritable(filepath);
            info.executable = isExecutable(filepath);
        }

        struct stat lst;
        if (lstat(filepath.c_str(), &lst) == 0) {
            info.isSymlink = S_ISLNK(lst.st_mode);
        }

        return info;
    }

    //=========================================================================
    // File Manipulation
    //=========================================================================

    static FileResult<bool> copy(const std::string& source, const std::string& dest, bool overwrite = true) {
        if (!exists(source)) {
            return FileResult<bool>(false, "Source file does not exist: " + source);
        }
        if (exists(dest) && !overwrite) {
            return FileResult<bool>(false, "Destination already exists: " + dest);
        }

        auto result = readBinary(source);
        if (!result) return FileResult<bool>(false, result.error);

        return writeBinary(dest, result.value);
    }

    static FileResult<bool> move(const std::string& source, const std::string& dest, bool overwrite = true) {
        if (!exists(source)) {
            return FileResult<bool>(false, "Source file does not exist: " + source);
        }
        if (exists(dest) && !overwrite) {
            return FileResult<bool>(false, "Destination already exists: " + dest);
        }

        ensureDirectory(getDirectory(dest));
        if (std::rename(source.c_str(), dest.c_str()) == 0) {
            return FileResult<bool>(true);
        }

        auto copyResult = copy(source, dest, overwrite);
        if (!copyResult) return copyResult;

        return remove(source);
    }

    static FileResult<bool> remove(const std::string& filepath) {
        if (!exists(filepath)) {
            return FileResult<bool>(false, "File does not exist: " + filepath);
        }
        if (std::remove(filepath.c_str()) == 0) {
            return FileResult<bool>(true);
        }
        return FileResult<bool>(false, "Failed to remove file: " + filepath);
    }

    static FileResult<bool> touch(const std::string& filepath) {
        if (exists(filepath)) {
            struct utimbuf times;
            times.actime = std::time(nullptr);
            times.modtime = std::time(nullptr);
            if (utime(filepath.c_str(), &times) == 0) {
                return FileResult<bool>(true);
            }
        } else {
            return writeText(filepath, "");
        }
        return FileResult<bool>(false, "Failed to touch file: " + filepath);
    }

    //=========================================================================
    // Directory Operations
    //=========================================================================

    static FileResult<bool> removeDirectory(const std::string& dirpath, bool recursive = false) {
        if (!exists(dirpath)) {
            return FileResult<bool>(false, "Directory does not exist: " + dirpath);
        }
        if (!isDirectory(dirpath)) {
            return FileResult<bool>(false, "Not a directory: " + dirpath);
        }

        if (recursive) {
            auto entries = listEntries(dirpath);
            for (const auto& entry : entries) {
                std::string fullPath = joinPath(dirpath, entry);
                if (isDirectory(fullPath)) {
                    auto result = removeDirectory(fullPath, true);
                    if (!result) return result;
                } else {
                    auto result = remove(fullPath);
                    if (!result) return result;
                }
            }
        }

        if (rmdir(dirpath.c_str()) == 0) {
            return FileResult<bool>(true);
        }
        return FileResult<bool>(false, "Failed to remove directory: " + dirpath);
    }

    static std::vector<std::string> listEntries(const std::string& dirpath, bool includeHidden = false) {
        std::vector<std::string> entries;
        DIR* dir = opendir(dirpath.c_str());
        if (!dir) return entries;

        struct dirent* entry;
        while ((entry = readdir(dir)) != nullptr) {
            std::string name(entry->d_name);
            if (name == "." || name == "..") continue;
            if (!includeHidden && name[0] == '.') continue;
            entries.push_back
(name);
        }
        closedir(dir);
        std::sort(entries.begin(), entries.end());
        return entries;
    }

    static std::vector<std::string> listFiles(const std::string& dirpath, bool includeHidden = false) {
        std::vector<std::string> files;
        for (const auto& entry : listEntries(dirpath, includeHidden)) {
            std::string fullPath = joinPath(dirpath, entry);
            if (isFile(fullPath)) files.push_back(entry);
        }
        return files;
    }

    static std::vector<std::string> listDirectories(const std::string& dirpath, bool includeHidden = false) {
        std::vector<std::string> dirs;
        for (const auto& entry : listEntries(dirpath, includeHidden)) {
            std::string fullPath = joinPath(dirpath, entry);
            if (isDirectory(fullPath)) dirs.push_back(entry);
        }
        return dirs;
    }

    //=========================================================================
    // Utility Functions
    //=========================================================================

    static std::string formatSize(std::size_t bytes, int precision = 2) {
        const char* units[] = {"B", "KB", "MB", "GB", "TB"};
        int unitIndex = 0;
        double size = static_cast<double>(bytes);
        while (size >= 1024.0 && unitIndex < 4) {
            size /= 1024.0;
            unitIndex++;
        }
        std::ostringstream oss;
        oss << std::fixed << std::setprecision(precision) << size << " " << units[unitIndex];
        return oss.str();
    }

    static std::string getTempDirectory() {
        const char* tmp = getenv("TMPDIR");
        if (!tmp) tmp = getenv("TMP");
        if (!tmp) tmp = getenv("TEMP");
        if (!tmp) tmp = "/tmp";
        return std::string(tmp);
    }

    static std::string getTempFile(const std::string& prefix = "tmp", const std::string& suffix = "") {
        std::ostringstream oss;
        oss << getTempDirectory() << "/" << prefix << "_" << std::time(nullptr) << "_" << getpid() << suffix;
        return oss.str();
    }
};

} // namespace alltoolkit

#endif // ALLTOOLKIT_FILE_UTILS_HPP
