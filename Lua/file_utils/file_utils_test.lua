#!/usr/bin/env lua
---
-- File Utilities Test Suite
-- 文件工具函数测试套件
--
-- 覆盖场景:
-- - 路径处理 (normalize_path, get_directory, get_filename, get_extension, get_basename, join, is_absolute, relative_path)
-- - 文件读取 (read_file, read_lines, read_binary)
-- - 文件写入 (write_file, append_file, write_binary, copy_file)
-- - 文件信息 (exists, is_directory, get_file_size, format_file_size, get_mime_type)
-- - 目录操作 (create_directory, list_directory, list_directory_recursive, remove_directory)
-- - 文件操作 (delete_file, rename_file, get_mtime, delete_files_by_pattern)
-- - 临时文件 (temp_name, create_temp_file)
-- - 文件搜索 (search_in_file, find_files)
-- - 工具函数 (load_table, save_table, serialize_table, get_current_directory, is_readable, is_writable, get_file_hash)
--
-- Author: AllToolkit
-- Version: 1.0.0

local path = arg and arg[0] and arg[0]:match("(.*/)") or ""
local mod_path = path .. "mod.lua"

-- 加载模块
local FileUtils = dofile(mod_path)

-- 测试统计
local tests_run = 0
local tests_passed = 0
local tests_failed = 0
local failures = {}

--- 断言函数
local function assert_eq(actual, expected, message)
    tests_run = tests_run + 1
    if actual == expected then
        tests_passed = tests_passed + 1
        return true
    else
        tests_failed = tests_failed + 1
        local msg = message or ("Expected %s, got %s"):format(tostring(expected), tostring(actual))
        table.insert(failures, msg)
        print("  ❌ FAIL: " .. msg)
        return false
    end
end

--- 断言真值
local function assert_true(condition, message)
    tests_run = tests_run + 1
    if condition then
        tests_passed = tests_passed + 1
        return true
    else
        tests_failed = tests_failed + 1
        local msg = message or "Expected true"
        table.insert(failures, msg)
        print("  ❌ FAIL: " .. msg)
        return false
    end
end

--- 断言假值
local function assert_false(condition, message)
    tests_run = tests_run + 1
    if not condition then
        tests_passed = tests_passed + 1
        return true
    else
        tests_failed = tests_failed + 1
        local msg = message or "Expected false"
        table.insert(failures, msg)
        print("  ❌ FAIL: " .. msg)
        return false
    end
end

--- 打印测试组标题
local function test_group(title)
    print("\n" .. string.rep("=", 60))
    print("📋 " .. title)
    print(string.rep("=", 60))
end

-------------------------------------------------------------------------------
-- 路径处理测试
-------------------------------------------------------------------------------
local function test_path_functions()
    test_group("路径处理函数")
    
    -- normalize_path
    print("\n1. normalize_path")
    assert_eq(FileUtils.normalize_path("/a/b/../c"), "/a/c", "处理 ../")
    assert_eq(FileUtils.normalize_path("/a/./b"), "/a/b", "处理 ./")
    assert_eq(FileUtils.normalize_path("a//b///c"), "a/b/c", "移除重复斜杠")
    assert_eq(FileUtils.normalize_path(""), ".", "空路径")
    assert_eq(FileUtils.normalize_path("a\\b\\c"), "a/b/c", "反斜杠转正斜杠")
    
    -- get_directory
    print("\n2. get_directory")
    assert_eq(FileUtils.get_directory("/a/b/c.txt"), "/a/b", "获取目录")
    assert_eq(FileUtils.get_directory("c.txt"), ".", "当前目录")
    assert_eq(FileUtils.get_directory("/a/b/"), "/a/b", "目录路径")
    
    -- get_filename
    print("\n3. get_filename")
    assert_eq(FileUtils.get_filename("/a/b/c.txt"), "c.txt", "获取文件名")
    assert_eq(FileUtils.get_filename("/a/b/"), "", "目录路径无文件名")
    assert_eq(FileUtils.get_filename("c.txt"), "c.txt", "仅文件名")
    
    -- get_extension
    print("\n4. get_extension")
    assert_eq(FileUtils.get_extension("/a/b/c.txt"), ".txt", "获取扩展名")
    assert_eq(FileUtils.get_extension("/a/b/c"), "", "无扩展名")
    assert_eq(FileUtils.get_extension("/a/b/c.tar.gz"), ".gz", "多重扩展名")
    
    -- get_basename
    print("\n5. get_basename")
    assert_eq(FileUtils.get_basename("/a/b/c.txt"), "c", "获取 basename")
    assert_eq(FileUtils.get_basename("/a/b/c"), "c", "无扩展名")
    assert_eq(FileUtils.get_basename("/a/b/c.tar.gz"), "c.tar", "多重扩展名")
    
    -- join
    print("\n6. join")
    assert_eq(FileUtils.join("/a", "b", "c"), "/a/b/c", "拼接路径")
    assert_eq(FileUtils.join("/a/", "/b/"), "/a/b", "处理多余斜杠")
    assert_eq(FileUtils.join("a", "b"), "a/b", "相对路径")
    
    -- is_absolute
    print("\n7. is_absolute")
    assert_true(FileUtils.is_absolute("/a/b"), "绝对路径 Unix")
    assert_true(FileUtils.is_absolute("C:/a/b"), "绝对路径 Windows")
    assert_false(FileUtils.is_absolute("a/b"), "相对路径")
    
    -- relative_path
    print("\n8. relative_path")
    assert_eq(FileUtils.relative_path("/a/b/c", "/a/b/d"), "../d", "同级目录")
    assert_eq(FileUtils.relative_path("/a/b", "/a/b/c/d"), "c/d", "子目录")
    assert_eq(FileUtils.relative_path("/a/b/c", "/a/b"), "..", "父目录")
end

-------------------------------------------------------------------------------
-- 文件读取测试
-------------------------------------------------------------------------------
local function test_read_functions()
    test_group("文件读取函数")
    
    local test_file = "/tmp/alltoolkit_test_read.txt"
    local test_content = "Line 1\nLine 2\nLine 3\n"
    
    -- 准备测试文件
    local file = io.open(test_file, "w")
    if file then
        file:write(test_content)
        file:close()
    end
    
    -- read_file
    print("\n1. read_file")
    local content, err = FileUtils.read_file(test_file)
    assert_eq(content, test_content, "读取文件内容")
    
    content, err = FileUtils.read_file("/nonexistent/file.txt")
    assert_eq(content, nil, "读取不存在的文件返回 nil")
    
    -- read_lines
    print("\n2. read_lines")
    local lines, err = FileUtils.read_lines(test_file)
    assert_eq(#lines, 3, "读取行数")
    assert_eq(lines[1], "Line 1", "第一行")
    assert_eq(lines[2], "Line 2", "第二行")
    assert_eq(lines[3], "Line 3", "第三行")
    
    -- 清理
    os.remove(test_file)
end

-------------------------------------------------------------------------------
-- 文件写入测试
-------------------------------------------------------------------------------
local function test_write_functions()
    test_group("文件写入函数")
    
    local test_file = "/tmp/alltoolkit_test_write.txt"
    local test_content = "Hello, World!"
    
    -- write_file
    print("\n1. write_file")
    local success, err = FileUtils.write_file(test_file, test_content)
    assert_true(success, "写入文件成功")
    
    -- 验证内容
    local file = io.open(test_file, "r")
    if file then
        local content = file:read("*a")
        file:close()
        assert_eq(content, test_content, "验证写入内容")
    end
    
    -- append_file
    print("\n2. append_file")
    local append_content = "\nAppended line"
    success, err = FileUtils.append_file(test_file, append_content)
    assert_true(success, "追加内容成功")
    
    -- 验证追加
    local content, err = FileUtils.read_file(test_file)
    assert_eq(content, test_content .. append_content, "验证追加内容")
    
    -- copy_file
    print("\n3. copy_file")
    local copy_file = "/tmp/alltoolkit_test_copy.txt"
    success, err = FileUtils.copy_file(test_file, copy_file)
    assert_true(success, "复制文件成功")
    
    local copied_content, err = FileUtils.read_file(copy_file)
    assert_eq(copied_content, content, "验证复制内容")
    
    -- 清理
    os.remove(test_file)
    os.remove(copy_file)
end

-------------------------------------------------------------------------------
-- 文件信息测试
-------------------------------------------------------------------------------
local function test_file_info()
    test_group("文件信息函数")
    
    local test_file = "/tmp/alltoolkit_test_info.txt"
    
    -- 创建测试文件
    FileUtils.write_file(test_file, "Test content")
    
    -- exists
    print("\n1. exists")
    assert_true(FileUtils.exists(test_file), "文件存在")
    assert_false(FileUtils.exists("/nonexistent/file.txt"), "文件不存在")
    
    -- get_file_size
    print("\n2. get_file_size")
    local size, err = FileUtils.get_file_size(test_file)
    assert_true(size ~= nil, "获取文件大小")
    assert_true(size > 0, "文件大小大于 0")
    
    -- format_file_size
    print("\n3. format_file_size")
    assert_eq(FileUtils.format_file_size(512), "512 B", "字节格式化")
    assert_eq(FileUtils.format_file_size(1536), "1.50 KB", "KB 格式化")
    assert_eq(FileUtils.format_file_size(1572864), "1.50 MB", "MB 格式化")
    assert_eq(FileUtils.format_file_size(1610612736), "1.50 GB", "GB 格式化")
    
    -- get_mime_type
    print("\n4. get_mime_type")
    assert_eq(FileUtils.get_mime_type("test.txt"), "text/plain", "txt MIME")
    assert_eq(FileUtils.get_mime_type("test.html"), "text/html", "html MIME")
    assert_eq(FileUtils.get_mime_type("test.png"), "image/png", "png MIME")
    assert_eq(FileUtils.get_mime_type("test.pdf"), "application/pdf", "pdf MIME")
    assert_eq(FileUtils.get_mime_type("test.unknown"), "application/octet-stream", "未知 MIME")
    
    -- 清理
    os.remove(test_file)
end

-------------------------------------------------------------------------------
-- 目录操作测试
-------------------------------------------------------------------------------
local function test_directory_functions()
    test_group("目录操作函数")
    
    local test_dir = "/tmp/alltoolkit_test_dir"
    local nested_dir = test_dir .. "/subdir"
    
    -- create_directory
    print("\n1. create_directory")
    local success, err = FileUtils.create_directory(test_dir)
    assert_true(success, "创建目录成功")
    assert_true(FileUtils.is_directory(test_dir), "目录存在")
    
    -- 创建嵌套目录
    success, err = FileUtils.create_directory(nested_dir)
    assert_true(success, "创建嵌套目录成功")
    
    -- list_directory
    print("\n2. list_directory")
    local entries, err = FileUtils.list_directory(test_dir)
    assert_true(entries ~= nil, "列出目录")
    assert_true(#entries >= 1, "目录包含内容")
    
    -- 创建测试文件
    FileUtils.write_file(test_dir .. "/test1.txt", "content1")
    FileUtils.write_file(test_dir .. "/test2.txt", "content2")
    
    entries, err = FileUtils.list_directory(test_dir)
    assert_true(#entries >= 2, "目录包含测试文件")
    
    -- list_directory_recursive
    print("\n3. list_directory_recursive")
    local all_entries, err = FileUtils.list_directory_recursive(test_dir, {recursive = true})
    assert_true(all_entries ~= nil, "递归列出目录")
    
    -- remove_directory
    print("\n4. remove_directory")
    -- 先删除文件
    FileUtils.delete_file(test_dir .. "/test1.txt")
    FileUtils.delete_file(test_dir .. "/test2.txt")
    
    success, err = FileUtils.remove_directory(nested_dir)
    assert_true(success, "删除空目录成功")
    
    -- 清理
    FileUtils.delete_file(test_dir .. "/test1.txt")
    FileUtils.delete_file(test_dir .. "/test2.txt")
    FileUtils.remove_directory(test_dir)
end

-------------------------------------------------------------------------------
-- 文件操作测试
-------------------------------------------------------------------------------
local function test_file_operations()
    test_group("文件操作函数")
    
    local test_file = "/tmp/alltoolkit_test_ops.txt"
    local rename_file = "/tmp/alltoolkit_test_rename.txt"
    
    -- 创建测试文件
    FileUtils.write_file(test_file, "Test content")
    
    -- delete_file
    print("\n1. delete_file")
    local success, err = FileUtils.delete_file(test_file)
    assert_true(success, "删除文件成功")
    assert_false(FileUtils.exists(test_file), "文件已删除")
    
    -- 重新创建用于重命名测试
    FileUtils.write_file(test_file, "Test content")
    
    -- rename_file
    print("\n2. rename_file")
    success, err = FileUtils.rename_file(test_file, rename_file)
    assert_true(success, "重命名文件成功")
    assert_false(FileUtils.exists(test_file), "原文件不存在")
    assert_true(FileUtils.exists(rename_file), "新文件存在")
    
    -- delete_files_by_pattern
    print("\n3. delete_files_by_pattern")
    FileUtils.write_file("/tmp/test_pattern_1.txt", "content")
    FileUtils.write_file("/tmp/test_pattern_2.txt", "content")
    FileUtils.write_file("/tmp/test_pattern_3.log", "content")
    
    local count, err = FileUtils.delete_files_by_pattern("test_pattern_*.txt", "/tmp")
    assert_true(count >= 2, "批量删除文件")
    
    -- 清理
    FileUtils.delete_file(rename_file)
    FileUtils.delete_file("/tmp/test_pattern_3.log")
end

-------------------------------------------------------------------------------
-- 临时文件测试
-------------------------------------------------------------------------------
local function test_temp_functions()
    test_group("临时文件函数")
    
    -- temp_name
    print("\n1. temp_name")
    local name1 = FileUtils.temp_name("test")
    local name2 = FileUtils.temp_name("test")
    assert_true(name1:match("^test_"), "临时文件名格式正确")
    assert_false(name1 == name2, "临时文件名唯一")
    
    -- create_temp_file
    print("\n2. create_temp_file")
    local temp_path, err = FileUtils.create_temp_file("alltoolkit", "test content")
    assert_true(temp_path ~= nil, "创建临时文件成功")
    assert_true(FileUtils.exists(temp_path), "临时文件存在")
    
    local content, err = FileUtils.read_file(temp_path)
    assert_eq(content, "test content", "临时文件内容正确")
    
    -- 清理
    FileUtils.delete_file(temp_path)
end

-------------------------------------------------------------------------------
-- 文件搜索测试
-------------------------------------------------------------------------------
local function test_search_functions()
    test_group("文件搜索函数")
    
    local test_file = "/tmp/alltoolkit_test_search.txt"
    local test_content = "Line 1: hello\nLine 2: world\nLine 3: hello again\n"
    
    -- 创建测试文件
    FileUtils.write_file(test_file, test_content)
    
    -- search_in_file
    print("\n1. search_in_file")
    local matches, err = FileUtils.search_in_file(test_file, "hello")
    assert_true(matches ~= nil, "搜索文件")
    assert_eq(#matches, 2, "匹配行数")
    assert_eq(matches[1].line_number, 1, "第一行匹配")
    assert_eq(matches[2].line_number, 3, "第三行匹配")
    
    -- find_files
    print("\n2. find_files")
    -- 创建测试文件用于查找
    local find_test_file = "/tmp/alltoolkit_find_test.txt"
    FileUtils.write_file(find_test_file, "test content")
    
    local files, err = FileUtils.find_files("/tmp", "alltoolkit_find_test.txt", false)
    assert_true(files ~= nil, "查找文件")
    assert_true(#files >= 1, "找到测试文件")
    
    -- 清理
    FileUtils.delete_file(test_file)
    FileUtils.delete_file(find_test_file)
end

-------------------------------------------------------------------------------
-- 工具函数测试
-------------------------------------------------------------------------------
local function test_utility_functions()
    test_group("工具函数")
    
    local test_file = "/tmp/alltoolkit_test_table.lua"
    local test_data = {
        name = "Test",
        value = 42,
        nested = {a = 1, b = 2},
        array = {1, 2, 3}
    }
    
    -- save_table
    print("\n1. save_table")
    local success, err = FileUtils.save_table(test_file, test_data, true)
    assert_true(success, "保存表成功")
    
    -- load_table
    print("\n2. load_table")
    local loaded_data, err = FileUtils.load_table(test_file)
    assert_true(loaded_data ~= nil, "加载表成功")
    assert_eq(loaded_data.name, "Test", "name 字段")
    assert_eq(loaded_data.value, 42, "value 字段")
    assert_eq(loaded_data.nested.a, 1, "嵌套表 a 字段")
    assert_eq(loaded_data.array[2], 2, "数组元素")
    
    -- serialize_table
    print("\n3. serialize_table")
    local serialized = FileUtils.serialize_table({a = 1, b = 2})
    assert_true(serialized:match("{"), "序列化包含 {")
    assert_true(serialized:match("}"), "序列化包含 }")
    
    -- get_current_directory
    print("\n4. get_current_directory")
    local cwd = FileUtils.get_current_directory()
    assert_true(cwd ~= nil, "获取当前目录")
    assert_true(#cwd > 0, "当前目录非空")
    
    -- is_readable / is_writable
    print("\n5. is_readable / is_writable")
    FileUtils.write_file(test_file, "test")
    assert_true(FileUtils.is_readable(test_file), "文件可读")
    assert_true(FileUtils.is_writable(test_file), "文件可写")
    
    -- get_file_hash
    print("\n6. get_file_hash")
    local hash, err = FileUtils.get_file_hash(test_file, "md5")
    assert_true(hash ~= nil, "获取 MD5 哈希")
    assert_true(#hash == 32, "MD5 哈希长度正确")
    
    -- 清理
    FileUtils.delete_file(test_file)
end

-------------------------------------------------------------------------------
-- 边界条件测试
-------------------------------------------------------------------------------
local function test_edge_cases()
    test_group("边界条件测试")
    
    -- nil 处理
    print("\n1. nil 参数处理")
    assert_eq(FileUtils.normalize_path(nil), nil, "normalize_path(nil)")
    assert_eq(FileUtils.get_directory(nil), nil, "get_directory(nil)")
    assert_eq(FileUtils.get_filename(nil), nil, "get_filename(nil)")
    assert_eq(FileUtils.read_file(nil), nil, "read_file(nil)")
    assert_eq(FileUtils.write_file(nil, "content"), false, "write_file(nil)")
    assert_eq(FileUtils.exists(nil), false, "exists(nil)")
    
    -- 空字符串处理
    print("\n2. 空字符串处理")
    assert_eq(FileUtils.normalize_path(""), ".", "normalize_path('')")
    assert_eq(FileUtils.get_extension(""), "", "get_extension('')")
    
    -- 特殊路径
    print("\n3. 特殊路径")
    assert_eq(FileUtils.normalize_path("../../../etc"), "../../../etc", "多个 ../")
    assert_eq(FileUtils.join(), "", "join 无参数")
end

-------------------------------------------------------------------------------
-- 运行所有测试
-------------------------------------------------------------------------------
local function run_all_tests()
    print("\n")
    print("╔" .. string.rep("═", 58) .. "╗")
    print("║" .. string.rep(" ", 15) .. "File Utils Test Suite" .. string.rep(" ", 16) .. "║")
    print("╚" .. string.rep("═", 58) .. "╝")
    print("\n📦 AllToolkit Lua - File Utilities")
    print("📍 Version: " .. (FileUtils.VERSION or "unknown"))
    
    test_path_functions()
    test_read_functions()
    test_write_functions()
    test_file_info()
    test_directory_functions()
    test_file_operations()
    test_temp_functions()
    test_search_functions()
    test_utility_functions()
    test_edge_cases()
    
    -- 打印结果
    print("\n")
    print("╔" .. string.rep("═", 58) .. "╗")
    print("║" .. string.rep(" ", 20) .. "Test Results" .. string.rep(" ", 24) .. "║")
    print("╚" .. string.rep("═", 58) .. "╝")
    print("\n")
    print("  Total tests:  " .. tests_run)
    print("  ✅ Passed:     " .. tests_passed)
    print("  ❌ Failed:     " .. tests_failed)
    
    if tests_failed > 0 then
        print("\n  Failures:")
        for i, failure in ipairs(failures) do
            print("    " .. i .. ". " .. failure)
        end
    end
    
    print("\n" .. string.rep("=", 60))
    if tests_failed == 0 then
        print("🎉 All tests passed!")
    else
        print("⚠️  Some tests failed. Please review.")
    end
    print(string.rep("=", 60) .. "\n")
    
    return tests_failed == 0
end

-- 运行测试
local success = run_all_tests()
os.exit(success and 0 or 1)
