---
-- File Utilities Module
-- Lua 文件操作工具函数库
--
-- @module file_utils
-- @author AllToolkit
-- @version 1.0.0
-- @copyright MIT License

local FileUtils = {}

-- 导出所有公共函数
local mod = require("mod")
for k, v in pairs(mod) do
    FileUtils[k] = v
end

return FileUtils
