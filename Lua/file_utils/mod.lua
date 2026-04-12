---
-- File Utilities Module
-- 文件操作工具函数库
--
-- 提供常用的文件处理功能，包括读取、写入、路径处理、文件信息获取等。
-- 仅使用 Lua 标准库，零依赖。
--
-- @author AllToolkit
-- @version 1.0.0
-- @copyright MIT License

local FileUtils = {}
local FileUtilsMT = { __index = FileUtils }

--- 版本号
FileUtils.VERSION = "1.0.0"

--- 错误处理
FileUtils.Error = {
    FileNotFound = "File not found",
    PermissionDenied = "Permission denied",
    InvalidPath = "Invalid path",
    DirectoryNotFound = "Directory not found",
    FileExists = "File already exists",
    ReadError = "Error reading file",
    WriteError = "Error writing file",
}

-------------------------------------------------------------------------------
-- 路径处理函数
-------------------------------------------------------------------------------

--- 规范化路径（处理 ../ 和 ./）
-- @param path 输入路径
-- @return string 规范化后的路径
function FileUtils.normalize_path(path)
    if path == nil then return nil end
    
    -- 处理空路径
    if path == "" then return "." end
    
    -- 替换反斜杠为正斜杠
    path = path:gsub("\\", "/")
    
    -- 移除重复的斜杠
    path = path:gsub("/+", "/")
    
    -- 处理 ../
    local parts = {}
    for part in path:gmatch("[^/]+") do
        if part == ".." then
            if #parts > 0 and parts[#parts] ~= ".." then
                table.remove(parts)
            else
                table.insert(parts, part)
            end
        elseif part ~= "." then
            table.insert(parts, part)
        end
    end
    
    local result = table.concat(parts, "/")
    
    -- 处理绝对路径
    if path:sub(1, 1) == "/" then
        result = "/" .. result
    end
    
    return result == "" and "." or result
end

--- 获取路径的目录部分
-- @param path 文件路径
-- @return string 目录路径
function FileUtils.get_directory(path)
    if path == nil then return nil end
    
    -- 处理反斜杠
    path = path:gsub("\\", "/")
    
    local dir = path:match("(.+)/[^/]*$")
    return dir or "."
end

--- 获取路径的文件名部分
-- @param path 文件路径
-- @return string 文件名
function FileUtils.get_filename(path)
    if path == nil then return nil end
    
    -- 处理反斜杠
    path = path:gsub("\\", "/")
    
    -- 如果路径以 / 结尾，表示是目录，返回空字符串
    if path:sub(-1) == "/" then
        return ""
    end
    
    local filename = path:match("([^/]+)$")
    return filename or ""
end

--- 获取文件扩展名（带点）
-- @param path 文件路径
-- @return string 扩展名（如 ".txt"）
function FileUtils.get_extension(path)
    if path == nil then return nil end
    
    -- 处理反斜杠
    path = path:gsub("\\", "/")
    
    -- 处理空字符串
    if path == "" then return "" end
    
    local filename = path:match("([^/]+)$")
    if not filename or filename == "" then return "" end
    
    local ext = filename:match("%.[^.]+$")
    return ext or ""
end

--- 获取不含扩展名的文件名
-- @param path 文件路径
-- @return string 不含扩展名的文件名
function FileUtils.get_basename(path)
    if path == nil then return nil end
    
    local filename = FileUtils.get_filename(path)
    if not filename or filename == "" then return "" end
    
    local ext = FileUtils.get_extension(filename)
    
    if ext and #ext > 0 then
        return filename:sub(1, -#ext - 1)
    end
    return filename
end

--- 拼接路径
-- @param ... 路径片段
-- @return string 拼接后的路径
function FileUtils.join(...)
    local parts = {...}
    local result = ""
    
    for i, part in ipairs(parts) do
        if part and part ~= "" then
            -- 处理反斜杠
            part = part:gsub("\\", "/")
            
            -- 移除开头的斜杠（除了第一个部分）
            if result ~= "" and part:sub(1, 1) == "/" then
                part = part:sub(2)
            end
            
            -- 移除结尾的斜杠
            if part:sub(-1) == "/" then
                part = part:sub(1, -2)
            end
            
            if result == "" then
                result = part
            else
                result = result .. "/" .. part
            end
        end
    end
    
    return result
end

--- 检查路径是否为绝对路径
-- @param path 路径
-- @return boolean 是否为绝对路径
function FileUtils.is_absolute(path)
    if path == nil then return false end
    return path:sub(1, 1) == "/" or path:match("^%a:[/\\]") ~= nil
end

--- 获取相对路径
-- @param base_path 基准路径
-- @param target_path 目标路径
-- @return string 相对路径
function FileUtils.relative_path(base_path, target_path)
    if base_path == nil or target_path == nil then return nil end
    
    base_path = base_path:gsub("\\", "/")
    target_path = target_path:gsub("\\", "/")
    
    -- 规范化路径
    base_path = FileUtils.normalize_path(base_path)
    target_path = FileUtils.normalize_path(target_path)
    
    -- 移除末尾的斜杠
    if base_path:sub(-1) == "/" then
        base_path = base_path:sub(1, -2)
    end
    
    -- 分割路径
    local base_parts = {}
    for part in base_path:gmatch("[^/]+") do
        table.insert(base_parts, part)
    end
    
    local target_parts = {}
    for part in target_path:gmatch("[^/]+") do
        table.insert(target_parts, part)
    end
    
    -- 找到公共前缀
    local common_len = 0
    local min_len = math.min(#base_parts, #target_parts)
    for i = 1, min_len do
        if base_parts[i] == target_parts[i] then
            common_len = common_len + 1
        else
            break
        end
    end
    
    -- 构建相对路径
    local result_parts = {}
    for i = common_len + 1, #base_parts do
        table.insert(result_parts, "..")
    end
    for i = common_len + 1, #target_parts do
        table.insert(result_parts, target_parts[i])
    end
    
    if #result_parts == 0 then
        return "."
    end
    
    return table.concat(result_parts, "/")
end

-------------------------------------------------------------------------------
-- 文件读取函数
-------------------------------------------------------------------------------

--- 读取整个文件内容
-- @param path 文件路径
-- @return string|nil 文件内容，失败返回 nil
-- @return string|nil 错误信息
function FileUtils.read_file(path)
    if path == nil then
        return nil, FileUtils.Error.InvalidPath
    end
    
    local file, err = io.open(path, "r")
    if not file then
        return nil, FileUtils.Error.FileNotFound .. ": " .. (err or "unknown")
    end
    
    local content = file:read("*a")
    file:close()
    
    return content, nil
end

--- 读取文件的行
-- @param path 文件路径
-- @return table 行的数组
-- @return string|nil 错误信息
function FileUtils.read_lines(path)
    if path == nil then
        return nil, FileUtils.Error.InvalidPath
    end
    
    local file, err = io.open(path, "r")
    if not file then
        return nil, FileUtils.Error.FileNotFound .. ": " .. (err or "unknown")
    end
    
    local lines = {}
    for line in file:lines() do
        table.insert(lines, line)
    end
    file:close()
    
    return lines, nil
end

--- 读取文件的二进制内容
-- @param path 文件路径
-- @return string|nil 二进制内容
-- @return string|nil 错误信息
function FileUtils.read_binary(path)
    if path == nil then
        return nil, FileUtils.Error.InvalidPath
    end
    
    local file, err = io.open(path, "rb")
    if not file then
        return nil, FileUtils.Error.FileNotFound .. ": " .. (err or "unknown")
    end
    
    local content = file:read("*a")
    file:close()
    
    return content, nil
end

-------------------------------------------------------------------------------
-- 文件写入函数
-------------------------------------------------------------------------------

--- 写入文件（覆盖模式）
-- @param path 文件路径
-- @param content 内容
-- @return boolean 是否成功
-- @return string|nil 错误信息
function FileUtils.write_file(path, content)
    if path == nil then
        return false, FileUtils.Error.InvalidPath
    end
    
    local file, err = io.open(path, "w")
    if not file then
        return false, FileUtils.Error.WriteError .. ": " .. (err or "unknown")
    end
    
    file:write(content)
    file:close()
    
    return true, nil
end

--- 追加内容到文件
-- @param path 文件路径
-- @param content 内容
-- @return boolean 是否成功
-- @return string|nil 错误信息
function FileUtils.append_file(path, content)
    if path == nil then
        return false, FileUtils.Error.InvalidPath
    end
    
    local file, err = io.open(path, "a")
    if not file then
        return false, FileUtils.Error.WriteError .. ": " .. (err or "unknown")
    end
    
    file:write(content)
    file:close()
    
    return true, nil
end

--- 写入二进制内容到文件
-- @param path 文件路径
-- @param content 二进制内容
-- @return boolean 是否成功
-- @return string|nil 错误信息
function FileUtils.write_binary(path, content)
    if path == nil then
        return false, FileUtils.Error.InvalidPath
    end
    
    local file, err = io.open(path, "wb")
    if not file then
        return false, FileUtils.Error.WriteError .. ": " .. (err or "unknown")
    end
    
    file:write(content)
    file:close()
    
    return true, nil
end

--- 复制文件
-- @param src_path 源文件路径
-- @param dst_path 目标文件路径
-- @return boolean 是否成功
-- @return string|nil 错误信息
function FileUtils.copy_file(src_path, dst_path)
    if src_path == nil or dst_path == nil then
        return false, FileUtils.Error.InvalidPath
    end
    
    local content, err = FileUtils.read_binary(src_path)
    if not content then
        return false, err
    end
    
    return FileUtils.write_binary(dst_path, content)
end

-------------------------------------------------------------------------------
-- 文件信息函数
-------------------------------------------------------------------------------

--- 检查文件是否存在
-- @param path 文件路径
-- @return boolean 是否存在
function FileUtils.exists(path)
    if path == nil then return false end
    
    local file = io.open(path, "r")
    if file then
        file:close()
        return true
    end
    
    -- 检查是否为目录
    return FileUtils.is_directory(path)
end

--- 检查路径是否为目录
-- @param path 路径
-- @return boolean 是否为目录
function FileUtils.is_directory(path)
    if path == nil then return false end
    
    -- 使用 os.execute 检查（跨平台方式有限）
    local result = os.execute('test -d "' .. path .. '" 2>/dev/null')
    return result == 0 or result == true
end

--- 获取文件大小（字节）
-- @param path 文件路径
-- @return number|nil 文件大小
-- @return string|nil 错误信息
function FileUtils.get_file_size(path)
    if path == nil then
        return nil, FileUtils.Error.InvalidPath
    end
    
    local file, err = io.open(path, "r")
    if not file then
        return nil, FileUtils.Error.FileNotFound .. ": " .. (err or "unknown")
    end
    
    local size = file:seek("end")
    file:close()
    
    return size, nil
end

--- 获取人类可读的文件大小
-- @param size 字节数
-- @return string 格式化后的大小（如 "1.5 MB"）
function FileUtils.format_file_size(size)
    if size == nil then return "Unknown" end
    
    local units = {"B", "KB", "MB", "GB", "TB"}
    local unit_index = 1
    local formatted_size = size
    
    while formatted_size >= 1024 and unit_index < #units do
        formatted_size = formatted_size / 1024
        unit_index = unit_index + 1
    end
    
    if unit_index == 1 then
        return string.format("%d %s", math.floor(formatted_size), units[unit_index])
    else
        return string.format("%.2f %s", formatted_size, units[unit_index])
    end
end

--- 获取文件扩展名对应的 MIME 类型（基础版本）
-- @param path 文件路径
-- @return string MIME 类型
function FileUtils.get_mime_type(path)
    if path == nil then return "application/octet-stream" end
    
    local ext = FileUtils.get_extension(path):lower()
    
    local mime_types = {
        [".txt"] = "text/plain",
        [".md"] = "text/markdown",
        [".html"] = "text/html",
        [".htm"] = "text/html",
        [".css"] = "text/css",
        [".js"] = "application/javascript",
        [".json"] = "application/json",
        [".xml"] = "application/xml",
        [".csv"] = "text/csv",
        [".lua"] = "text/x-lua",
        [".py"] = "text/x-python",
        [".rb"] = "text/x-ruby",
        [".java"] = "text/x-java",
        [".c"] = "text/x-c",
        [".cpp"] = "text/x-c++",
        [".h"] = "text/x-c",
        [".go"] = "text/x-go",
        [".rs"] = "text/x-rust",
        [".php"] = "text/x-php",
        [".sh"] = "text/x-sh",
        [".bash"] = "text/x-sh",
        [".sql"] = "application/sql",
        [".yaml"] = "application/x-yaml",
        [".yml"] = "application/x-yaml",
        [".toml"] = "application/x-toml",
        [".ini"] = "text/plain",
        [".conf"] = "text/plain",
        [".log"] = "text/plain",
        
        [".jpg"] = "image/jpeg",
        [".jpeg"] = "image/jpeg",
        [".png"] = "image/png",
        [".gif"] = "image/gif",
        [".bmp"] = "image/bmp",
        [".svg"] = "image/svg+xml",
        [".webp"] = "image/webp",
        [".ico"] = "image/x-icon",
        
        [".pdf"] = "application/pdf",
        [".doc"] = "application/msword",
        [".docx"] = "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        [".xls"] = "application/vnd.ms-excel",
        [".xlsx"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        [".ppt"] = "application/vnd.ms-powerpoint",
        [".pptx"] = "application/vnd.openxmlformats-officedocument.presentationml.presentation",
        
        [".zip"] = "application/zip",
        [".tar"] = "application/x-tar",
        [".gz"] = "application/gzip",
        [".rar"] = "application/vnd.rar",
        [".7z"] = "application/x-7z-compressed",
        
        [".mp3"] = "audio/mpeg",
        [".wav"] = "audio/wav",
        [".ogg"] = "audio/ogg",
        [".flac"] = "audio/flac",
        [".m4a"] = "audio/mp4",
        
        [".mp4"] = "video/mp4",
        [".avi"] = "video/x-msvideo",
        [".mkv"] = "video/x-matroska",
        [".webm"] = "video/webm",
        [".mov"] = "video/quicktime",
        
        [".ttf"] = "font/ttf",
        [".otf"] = "font/otf",
        [".woff"] = "font/woff",
        [".woff2"] = "font/woff2",
    }
    
    return mime_types[ext] or "application/octet-stream"
end

-------------------------------------------------------------------------------
-- 目录操作函数
-------------------------------------------------------------------------------

--- 创建目录（包括父目录）
-- @param path 目录路径
-- @return boolean 是否成功
-- @return string|nil 错误信息
function FileUtils.create_directory(path)
    if path == nil then
        return false, FileUtils.Error.InvalidPath
    end
    
    -- 使用 os.mkdir 创建目录
    local result = os.execute('mkdir -p "' .. path .. '" 2>/dev/null')
    
    if result == 0 or result == true then
        return true, nil
    else
        return false, "Failed to create directory: " .. path
    end
end

--- 列出目录内容
-- @param path 目录路径
-- @return table 文件和目录名的数组
-- @return string|nil 错误信息
function FileUtils.list_directory(path)
    if path == nil then
        return nil, FileUtils.Error.InvalidPath
    end
    
    if not FileUtils.is_directory(path) then
        return nil, FileUtils.Error.DirectoryNotFound
    end
    
    local entries = {}
    
    -- 使用 io.popen 列出目录内容
    local handle = io.popen('ls -1 "' .. path .. '" 2>/dev/null')
    if handle then
        for entry in handle:lines() do
            table.insert(entries, entry)
        end
        handle:close()
    end
    
    return entries, nil
end

--- 递归列出目录内容
-- @param path 目录路径
-- @param options 选项表（可选）
--   - recursive: boolean, 是否递归
--   - include_files: boolean, 是否包含文件
--   - include_dirs: boolean, 是否包含目录
-- @return table 文件路径的数组
-- @return string|nil 错误信息
function FileUtils.list_directory_recursive(path, options)
    options = options or {}
    local recursive = options.recursive ~= false
    local include_files = options.include_files ~= false
    local include_dirs = options.include_dirs ~= false
    
    local result = {}
    
    local function scan(dir, base_path)
        local entries, err = FileUtils.list_directory(dir)
        if not entries then
            return
        end
        
        for _, entry in ipairs(entries) do
            local full_path = FileUtils.join(dir, entry)
            local rel_path = base_path and FileUtils.join(base_path, entry) or entry
            
            if FileUtils.is_directory(full_path) then
                if include_dirs then
                    table.insert(result, rel_path)
                end
                if recursive then
                    scan(full_path, rel_path)
                end
            else
                if include_files then
                    table.insert(result, rel_path)
                end
            end
        end
    end
    
    scan(path)
    
    return result, nil
end

--- 删除空目录
-- @param path 目录路径
-- @return boolean 是否成功
-- @return string|nil 错误信息
function FileUtils.remove_directory(path)
    if path == nil then
        return false, FileUtils.Error.InvalidPath
    end
    
    local result = os.execute('rmdir "' .. path .. '" 2>/dev/null')
    
    if result == 0 or result == true then
        return true, nil
    else
        return false, "Failed to remove directory: " .. path
    end
end

-------------------------------------------------------------------------------
-- 文件操作函数
-------------------------------------------------------------------------------

--- 删除文件
-- @param path 文件路径
-- @return boolean 是否成功
-- @return string|nil 错误信息
function FileUtils.delete_file(path)
    if path == nil then
        return false, FileUtils.Error.InvalidPath
    end
    
    local result = os.execute('rm -f "' .. path .. '" 2>/dev/null')
    
    if result == 0 or result == true then
        return true, nil
    else
        return false, "Failed to delete file: " .. path
    end
end

--- 重命名/移动文件
-- @param old_path 原路径
-- @param new_path 新路径
-- @return boolean 是否成功
-- @return string|nil 错误信息
function FileUtils.rename_file(old_path, new_path)
    if old_path == nil or new_path == nil then
        return false, FileUtils.Error.InvalidPath
    end
    
    local result = os.execute('mv "' .. old_path .. '" "' .. new_path .. '" 2>/dev/null')
    
    if result == 0 or result == true then
        return true, nil
    else
        return false, "Failed to rename file: " .. old_path .. " -> " .. new_path
    end
end

--- 获取文件最后修改时间
-- @param path 文件路径
-- @return number|nil 时间戳
-- @return string|nil 错误信息
function FileUtils.get_mtime(path)
    if path == nil then
        return nil, FileUtils.Error.InvalidPath
    end
    
    -- 使用 stat 命令获取修改时间
    local handle = io.popen('stat -c %Y "' .. path .. '" 2>/dev/null')
    if handle then
        local mtime = handle:read("*a")
        handle:close()
        
        if mtime then
            return tonumber(mtime:match("%d+"))
        end
    end
    
    return nil, "Failed to get modification time"
end

--- 批量删除文件（支持通配符）
-- @param pattern 文件模式（如 "*.txt"）
-- @param directory 目录路径（可选，默认为当前目录）
-- @return number 删除的文件数
-- @return string|nil 错误信息
function FileUtils.delete_files_by_pattern(pattern, directory)
    directory = directory or "."
    
    if pattern == nil then
        return 0, FileUtils.Error.InvalidPath
    end
    
    local full_pattern = FileUtils.join(directory, pattern)
    local count = 0
    
    local handle = io.popen('ls ' .. full_pattern .. ' 2>/dev/null')
    if handle then
        for file in handle:lines() do
            if FileUtils.delete_file(file) then
                count = count + 1
            end
        end
        handle:close()
    end
    
    return count, nil
end

-------------------------------------------------------------------------------
-- 临时文件函数
-------------------------------------------------------------------------------

--- 生成临时文件名
-- @param prefix 前缀（可选）
-- @param extension 扩展名（可选）
-- @return string 临时文件名
function FileUtils.temp_name(prefix, extension)
    prefix = prefix or "tmp"
    extension = extension or ""
    
    if extension ~= "" and extension:sub(1, 1) ~= "." then
        extension = "." .. extension
    end
    
    -- 使用时间戳和随机数生成唯一名称
    local timestamp = os.time()
    local random = math.random(10000, 99999)
    
    return prefix .. "_" .. timestamp .. "_" .. random .. extension
end

--- 创建临时文件
-- @param prefix 前缀（可选）
-- @param content 初始内容（可选）
-- @return string|nil 临时文件路径
-- @return string|nil 错误信息
function FileUtils.create_temp_file(prefix, content)
    local temp_dir = os.getenv("TMPDIR") or os.getenv("TEMP") or "/tmp"
    local temp_name = FileUtils.temp_name(prefix)
    local temp_path = FileUtils.join(temp_dir, temp_name)
    
    local success, err = FileUtils.write_file(temp_path, content or "")
    if not success then
        return nil, err
    end
    
    return temp_path, nil
end

-------------------------------------------------------------------------------
-- 文件搜索函数
-------------------------------------------------------------------------------

--- 在文件中搜索内容
-- @param path 文件路径
-- @param pattern 搜索模式（Lua 模式）
-- @return table 匹配行的数组
-- @return string|nil 错误信息
function FileUtils.search_in_file(path, pattern)
    if path == nil or pattern == nil then
        return nil, FileUtils.Error.InvalidPath
    end
    
    local lines, err = FileUtils.read_lines(path)
    if not lines then
        return nil, err
    end
    
    local matches = {}
    for i, line in ipairs(lines) do
        if line:match(pattern) then
            table.insert(matches, {line_number = i, content = line})
        end
    end
    
    return matches, nil
end

--- 在目录中搜索文件
-- @param directory 目录路径
-- @param pattern 文件名模式
-- @param recursive 是否递归搜索
-- @return table 匹配文件路径的数组
-- @return string|nil 错误信息
function FileUtils.find_files(directory, pattern, recursive)
    if directory == nil or pattern == nil then
        return nil, FileUtils.Error.InvalidPath
    end
    
    local results = {}
    local find_cmd = recursive and 'find "' .. directory .. '" -name "' .. pattern .. '"' or 'find "' .. directory .. '" -maxdepth 1 -name "' .. pattern .. '"'
    
    local handle = io.popen(find_cmd .. ' 2>/dev/null')
    if handle then
        for file in handle:lines() do
            if not FileUtils.is_directory(file) then
                table.insert(results, file)
            end
        end
        handle:close()
    end
    
    return results, nil
end

-------------------------------------------------------------------------------
-- 工具函数
-------------------------------------------------------------------------------

--- 读取文件并解析为 Lua 表（支持 JSON 格式的子集）
-- @param path 文件路径
-- @return table|nil 解析后的表
-- @return string|nil 错误信息
function FileUtils.load_table(path)
    local content, err = FileUtils.read_file(path)
    if not content then
        return nil, err
    end
    
    -- 使用 load 函数安全地加载 Lua 表
    local func, load_err = load("return " .. content)
    if not func then
        return nil, "Failed to parse table: " .. load_err
    end
    
    local success, result = pcall(func)
    if not success then
        return nil, "Failed to load table: " .. result
    end
    
    if type(result) ~= "table" then
        return nil, "File does not contain a table"
    end
    
    return result, nil
end

--- 将 Lua 表写入文件
-- @param path 文件路径
-- @param data Lua 表
-- @param pretty 是否格式化输出
-- @return boolean 是否成功
-- @return string|nil 错误信息
function FileUtils.save_table(path, data, pretty)
    if type(data) ~= "table" then
        return false, "Data must be a table"
    end
    
    local content = FileUtils.serialize_table(data, pretty)
    return FileUtils.write_file(path, content)
end

--- 序列化 Lua 表为字符串
-- @param data Lua 表
-- @param pretty 是否格式化输出
-- @param indent 缩进级别（内部使用）
-- @return string 序列化后的字符串
function FileUtils.serialize_table(data, pretty, indent)
    indent = indent or 0
    pretty = pretty or false
    
    local indent_str = pretty and string.rep("  ", indent) or ""
    local next_indent = pretty and string.rep("  ", indent + 1) or ""
    local newline = pretty and "\n" or ""
    local space = pretty and " " or ""
    
    if type(data) == "table" then
        local items = {}
        local is_array = true
        local expected_index = 1
        
        -- 检查是否为数组
        for k, v in pairs(data) do
            if type(k) ~= "number" or k ~= expected_index then
                is_array = false
                break
            end
            expected_index = expected_index + 1
        end
        
        for k, v in pairs(data) do
            local key_str
            if is_array then
                key_str = ""
            elseif type(k) == "string" and k:match("^[%a_][%w_]*$") then
                key_str = k .. space .. "=" .. space
            else
                key_str = "[" .. FileUtils.serialize_table(k, pretty, indent + 1) .. "]" .. space .. "=" .. space
            end
            
            local value_str = FileUtils.serialize_table(v, pretty, indent + 1)
            table.insert(items, key_str .. value_str)
        end
        
        return "{" .. newline .. table.concat(items, "," .. newline .. next_indent) .. newline .. indent_str .. "}"
    elseif type(data) == "string" then
        -- 转义字符串
        local escaped = data:gsub("\\", "\\\\"):gsub('"', '\\"'):gsub("\n", "\\n"):gsub("\r", "\\r"):gsub("\t", "\\t")
        return '"' .. escaped .. '"'
    elseif type(data) == "number" or type(data) == "boolean" then
        return tostring(data)
    elseif type(data) == "nil" then
        return "nil"
    else
        return "nil" -- 不支持的类型
    end
end

--- 获取当前工作目录
-- @return string 当前工作目录路径
function FileUtils.get_current_directory()
    local handle = io.popen("pwd 2>/dev/null")
    if handle then
        local cwd = handle:read("*a")
        handle:close()
        return cwd:match("^(.-)\n?$") or "."
    end
    return "."
end

--- 检查文件是否可读
-- @param path 文件路径
-- @return boolean 是否可读
function FileUtils.is_readable(path)
    if path == nil then return false end
    
    local file = io.open(path, "r")
    if file then
        file:close()
        return true
    end
    return false
end

--- 检查文件是否可写
-- @param path 文件路径
-- @return boolean 是否可写
function FileUtils.is_writable(path)
    if path == nil then return false end
    
    local file = io.open(path, "a")
    if file then
        file:close()
        return true
    end
    return false
end

--- 获取文件哈希值（使用外部命令）
-- @param path 文件路径
-- @param algorithm 哈希算法（md5, sha1, sha256）
-- @return string|nil 哈希值
-- @return string|nil 错误信息
function FileUtils.get_file_hash(path, algorithm)
    if path == nil then
        return nil, FileUtils.Error.InvalidPath
    end
    
    algorithm = algorithm or "md5"
    local cmd
    
    if algorithm == "md5" then
        cmd = 'md5sum "' .. path .. '" 2>/dev/null'
    elseif algorithm == "sha1" then
        cmd = 'sha1sum "' .. path .. '" 2>/dev/null'
    elseif algorithm == "sha256" then
        cmd = 'sha256sum "' .. path .. '" 2>/dev/null'
    else
        return nil, "Unsupported algorithm: " .. algorithm
    end
    
    local handle = io.popen(cmd)
    if handle then
        local hash = handle:read("*a")
        handle:close()
        
        if hash then
            return hash:match("^%S+")
        end
    end
    
    return nil, "Failed to compute hash"
end

return setmetatable({}, FileUtilsMT)
