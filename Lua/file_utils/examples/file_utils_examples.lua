#!/usr/bin/env lua
---
-- File Utilities Examples
-- 文件工具函数使用示例
--
-- Author: AllToolkit
-- Version: 1.0.0

local path = arg and arg[0] and arg[0]:match("(.*/)") or ""
local FileUtils = dofile(path .. "../mod.lua")

print("📁 File Utilities Examples")
print(string.rep("=", 60))

-------------------------------------------------------------------------------
-- 示例 1: 路径处理
-------------------------------------------------------------------------------
print("\n1️⃣ 路径处理")
print("-" .. string.rep("-", 59))

local full_path = FileUtils.join("/home", "user", "documents", "file.txt")
print("拼接路径：" .. full_path)

print("目录部分：" .. FileUtils.get_directory(full_path))
print("文件名：" .. FileUtils.get_filename(full_path))
print("扩展名：" .. FileUtils.get_extension(full_path))
print("basename: " .. FileUtils.get_basename(full_path))

local messy_path = "/a/b/../c/./d//e"
print("\n原始路径：" .. messy_path)
print("规范化后：" .. FileUtils.normalize_path(messy_path))

local abs_path = "/home/user/project"
local rel_path = "/home/user/other"
print("\n绝对路径：" .. abs_path)
print("目标路径：" .. rel_path)
print("相对路径：" .. FileUtils.relative_path(abs_path, rel_path))

-------------------------------------------------------------------------------
-- 示例 2: 文件读写
-------------------------------------------------------------------------------
print("\n2️⃣ 文件读写")
print("-" .. string.rep("-", 59))

local test_file = "/tmp/alltoolkit_example.txt"

-- 写入文件
print("写入文件：" .. test_file)
FileUtils.write_file(test_file, "Hello, AllToolkit!\n这是第二行。\n这是第三行。")

-- 读取整个文件
print("\n读取整个文件:")
local content, err = FileUtils.read_file(test_file)
print(content)

-- 读取行
print("逐行读取:")
local lines, err = FileUtils.read_lines(test_file)
for i, line in ipairs(lines) do
    print("  第 " .. i .. " 行：" .. line)
end

-- 追加内容
print("\n追加内容...")
FileUtils.append_file(test_file, "\n这是追加的第四行。")

-- 再次读取
local new_content, err = FileUtils.read_file(test_file)
print("追加后的内容:")
print(new_content)

-------------------------------------------------------------------------------
-- 示例 3: 文件信息
-------------------------------------------------------------------------------
print("\n3️⃣ 文件信息")
print("-" .. string.rep("-", 59))

print("文件是否存在：" .. tostring(FileUtils.exists(test_file)))

local size, err = FileUtils.get_file_size(test_file)
print("文件大小（字节）: " .. tostring(size))
print("文件大小（格式化）: " .. FileUtils.format_file_size(size))

print("\nMIME 类型示例:")
local files = {
    "document.pdf",
    "image.png",
    "script.lua",
    "data.json",
    "archive.zip"
}
for _, file in ipairs(files) do
    print("  " .. file .. " → " .. FileUtils.get_mime_type(file))
end

-------------------------------------------------------------------------------
-- 示例 4: 目录操作
-------------------------------------------------------------------------------
print("\n4️⃣ 目录操作")
print("-" .. string.rep("-", 59))

local test_dir = "/tmp/alltoolkit_example_dir"
local subdir = test_dir .. "/subdir"

-- 创建目录
print("创建目录：" .. test_dir)
FileUtils.create_directory(test_dir)
print("创建子目录：" .. subdir)
FileUtils.create_directory(subdir)

-- 创建测试文件
FileUtils.write_file(test_dir .. "/file1.txt", "content1")
FileUtils.write_file(test_dir .. "/file2.txt", "content2")
FileUtils.write_file(subdir .. "/file3.txt", "content3")

-- 列出目录
print("\n目录内容:")
local entries, err = FileUtils.list_directory(test_dir)
for i, entry in ipairs(entries) do
    print("  - " .. entry)
end

-- 递归列出
print("\n递归列出所有文件:")
local all_files, err = FileUtils.list_directory_recursive(test_dir, {
    recursive = true,
    include_files = true,
    include_dirs = true
})
for i, file in ipairs(all_files) do
    print("  - " .. file)
end

-- 获取当前目录
print("\n当前工作目录：" .. FileUtils.get_current_directory())

-------------------------------------------------------------------------------
-- 示例 5: 文件搜索
-------------------------------------------------------------------------------
print("\n5️⃣ 文件搜索")
print("-" .. string.rep("-", 59))

-- 在文件中搜索
print("在文件中搜索 'file':")
local matches, err = FileUtils.search_in_file(test_dir .. "/file1.txt", "content")
for _, match in ipairs(matches) do
    print("  第 " .. match.line_number .. " 行：" .. match.content)
end

-- 查找文件
print("\n在 /tmp 中查找 alltoolkit_*.txt:")
local found_files, err = FileUtils.find_files("/tmp", "alltoolkit_*.txt", false)
for i, file in ipairs(found_files) do
    print("  - " .. file)
end

-------------------------------------------------------------------------------
-- 示例 6: 临时文件
-------------------------------------------------------------------------------
print("\n6️⃣ 临时文件")
print("-" .. string.rep("-", 59))

-- 生成临时文件名
print("生成临时文件名:")
for i = 1, 3 do
    print("  " .. FileUtils.temp_name("temp", "tmp"))
end

-- 创建临时文件
print("\n创建临时文件:")
local temp_path, err = FileUtils.create_temp_file("example", "临时文件内容")
print("临时文件路径：" .. temp_path)
print("文件存在：" .. tostring(FileUtils.exists(temp_path)))

-- 读取临时文件
local temp_content, err = FileUtils.read_file(temp_path)
print("临时文件内容：" .. temp_content)

-- 清理临时文件
FileUtils.delete_file(temp_path)
print("已删除临时文件")

-------------------------------------------------------------------------------
-- 示例 7: 数据序列化
-------------------------------------------------------------------------------
print("\n7️⃣ 数据序列化")
print("-" .. string.rep("-", 59))

local config_data = {
    app_name = "MyApp",
    version = "1.0.0",
    debug = true,
    port = 8080,
    database = {
        host = "localhost",
        port = 5432,
        name = "mydb"
    },
    features = {"auth", "api", "cache"}
}

local config_file = "/tmp/alltoolkit_config.lua"

-- 保存表
print("保存配置表到：" .. config_file)
local success, err = FileUtils.save_table(config_file, config_data, true)
print("保存成功：" .. tostring(success))

-- 读取并显示保存的内容
print("\n保存的文件内容:")
local file_content, err = FileUtils.read_file(config_file)
print(file_content)

-- 加载表
print("加载配置表:")
local loaded_config, err = FileUtils.load_table(config_file)
print("  app_name: " .. loaded_config.app_name)
print("  version: " .. loaded_config.version)
print("  debug: " .. tostring(loaded_config.debug))
print("  port: " .. loaded_config.port)
print("  database.host: " .. loaded_config.database.host)
print("  features: " .. table.concat(loaded_config.features, ", "))

-------------------------------------------------------------------------------
-- 示例 8: 文件复制和重命名
-------------------------------------------------------------------------------
print("\n8️⃣ 文件复制和重命名")
print("-" .. string.rep("-", 59))

local source_file = test_dir .. "/original.txt"
local copy_file = test_dir .. "/copy.txt"
local renamed_file = test_dir .. "/renamed.txt"

-- 创建源文件
FileUtils.write_file(source_file, "这是原始文件内容")
print("创建源文件：" .. source_file)

-- 复制文件
print("复制文件到：" .. copy_file)
local success, err = FileUtils.copy_file(source_file, copy_file)
print("复制成功：" .. tostring(success))

-- 验证复制
local copy_content, err = FileUtils.read_file(copy_file)
print("复制文件内容：" .. copy_content)

-- 重命名文件
print("重命名文件到：" .. renamed_file)
success, err = FileUtils.rename_file(copy_file, renamed_file)
print("重命名成功：" .. tostring(success))
print("原文件存在：" .. tostring(FileUtils.exists(copy_file)))
print("新文件存在：" .. tostring(FileUtils.exists(renamed_file)))

-------------------------------------------------------------------------------
-- 示例 9: 批量操作
-------------------------------------------------------------------------------
print("\n9️⃣ 批量操作")
print("-" .. string.rep("-", 59))

-- 创建多个临时文件
local batch_dir = "/tmp/alltoolkit_batch"
FileUtils.create_directory(batch_dir)

print("创建批量测试文件:")
for i = 1, 5 do
    local filename = batch_dir .. "/temp_" .. i .. ".txt"
    FileUtils.write_file(filename, "文件 " .. i .. " 的内容")
    print("  创建：" .. filename)
end

-- 列出文件
print("\n批量目录内容:")
local batch_files, err = FileUtils.list_directory(batch_dir)
for i, file in ipairs(batch_files) do
    print("  - " .. file)
end

-- 批量删除
print("\n批量删除 *.txt 文件...")
local count, err = FileUtils.delete_files_by_pattern("*.txt", batch_dir)
print("删除了 " .. count .. " 个文件")

-- 验证
local remaining, err = FileUtils.list_directory(batch_dir)
print("剩余文件数：" .. #remaining)

-- 清理目录
FileUtils.remove_directory(batch_dir)

-------------------------------------------------------------------------------
-- 示例 10: 文件哈希
-------------------------------------------------------------------------------
print("\n🔟 文件哈希")
print("-" .. string.rep("-", 59))

local hash_file = test_dir .. "/hash_test.txt"
FileUtils.write_file(hash_file, "计算这个文件的哈希值")

print("文件：" .. hash_file)
print("  MD5:    " .. (FileUtils.get_file_hash(hash_file, "md5") or "N/A"))
print("  SHA1:   " .. (FileUtils.get_file_hash(hash_file, "sha1") or "N/A"))
print("  SHA256: " .. (FileUtils.get_file_hash(hash_file, "sha256") or "N/A"))

-------------------------------------------------------------------------------
-- 清理
-------------------------------------------------------------------------------
print("\n" .. string.rep("=", 60))
print("清理测试文件...")

FileUtils.delete_file(test_file)
FileUtils.delete_file(config_file)
FileUtils.delete_file(hash_file)
FileUtils.delete_file(test_dir .. "/file1.txt")
FileUtils.delete_file(test_dir .. "/file2.txt")
FileUtils.delete_file(subdir .. "/file3.txt")
FileUtils.delete_file(test_dir .. "/original.txt")
FileUtils.delete_file(test_dir .. "/renamed.txt")
FileUtils.remove_directory(subdir)
FileUtils.remove_directory(test_dir)

print("✅ 清理完成")
print("\n📁 File Utilities Examples - 结束")
print(string.rep("=", 60))
