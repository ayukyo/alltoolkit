---
-- JSON Utilities - Advanced Usage Examples
-- 高级使用示例
--
-- 展示嵌套路径、深度克隆、合并等高级功能
--

local JsonUtils = require("mod")

print("=== JSON Utilities Advanced Usage ===\n")

-------------------------------------------------------------------------------
-- 1. 嵌套路径访问
-------------------------------------------------------------------------------

print("1. Nested Path Access")
print("---------------------")

local config = {
    database = {
        primary = {
            host = "localhost",
            port = 3306,
            credentials = {
                username = "admin",
                password = "secret"
            }
        },
        replica = {
            host = "replica.example.com",
            port = 3306
        }
    },
    app = {
        name = "MyApp",
        version = "2.0.0"
    }
}

-- 安全获取嵌套值
local host = JsonUtils.get(config, "database.primary.host")
print("Database host:", host)

local port = JsonUtils.get(config, "database.primary.port")
print("Database port:", port)

local username = JsonUtils.get(config, "database.primary.credentials.username")
print("Username:", username)

-- 路径不存在，返回默认值
local timeout = JsonUtils.get(config, "database.timeout", 30)
print("Timeout (with default):", timeout)

local ssl = JsonUtils.get(config, "database.ssl.enabled", false)
print("SSL enabled (with default):", ssl)

-- 使用数组路径
local pathArr = {"database", "primary", "credentials", "password"}
local password = JsonUtils.get(config, pathArr)
print("Password:", password)

print("")

-------------------------------------------------------------------------------
-- 2. 嵌套路径设置
-------------------------------------------------------------------------------

print("2. Nested Path Setting")
print("----------------------")

local settings = {}

-- 设置嵌套值（自动创建中间表）
JsonUtils.set(settings, "user.profile.name", "Alice")
JsonUtils.set(settings, "user.profile.age", 30)
JsonUtils.set(settings, "user.preferences.theme", "dark")
JsonUtils.set(settings, "user.preferences.language", "en")

print("Settings after set:")
print(JsonUtils.encode_pretty(settings))

print("")

-------------------------------------------------------------------------------
-- 3. 深度克隆
-------------------------------------------------------------------------------

print("3. Deep Clone")
print("-------------")

local original = {
    name = "Original",
    nested = {
        level1 = {
            level2 = {
                value = "deep data"
            }
        }
    },
    array = {1, 2, 3}
}

local clone = JsonUtils.deep_clone(original)

-- 验证克隆独立性
clone.name = "Modified"
clone.nested.level1.level2.value = "modified deep"
clone.array[1] = 100

print("Original after modification:")
print(JsonUtils.encode_pretty(original))
print("\nClone:")
print(JsonUtils.encode_pretty(clone))

print("")

-------------------------------------------------------------------------------
-- 4. 表合并
-------------------------------------------------------------------------------

print("4. Table Merge")
print("--------------")

local target = {
    name = "Target",
    settings = {
        theme = "light",
        language = "en"
    },
    values = {1, 2}
}

local source = {
    age = 25,
    settings = {
        notifications = true
    },
    values = {3, 4}
}

-- 浅合并
local shallow = JsonUtils.merge(target, source)
print("Shallow merge:")
print(JsonUtils.encode_pretty(shallow))

-- 深合并
local target2 = {
    name = "Target",
    config = {
        database = {
            host = "localhost"
        }
    }
}

local source2 = {
    config = {
        database = {
            port = 3306
        },
        cache = {
            enabled = true
        }
    }
}

local deep = JsonUtils.merge(target2, source2, true)
print("\nDeep merge:")
print(JsonUtils.encode_pretty(deep))

print("")

-------------------------------------------------------------------------------
-- 5. 深度比较
-------------------------------------------------------------------------------

print("5. Deep Comparison")
print("------------------")

local a = {
    name = "Test",
    values = {1, 2, 3},
    nested = {
        level1 = {
            level2 = 42
        }
    }
}

local b = {
    name = "Test",
    values = {1, 2, 3},
    nested = {
        level1 = {
            level2 = 42
        }
    }
}

local c = {
    name = "Different",
    values = {1, 2, 3}
}

print("a equals b:", JsonUtils.equals(a, b))
print("a equals c:", JsonUtils.equals(a, c))

print("")

-------------------------------------------------------------------------------
-- 6. 序列化检查
-------------------------------------------------------------------------------

print("6. Serializability Check")
print("------------------------")

print("nil:", JsonUtils.is_json_serializable(nil))
print("boolean:", JsonUtils.is_json_serializable(true))
print("number:", JsonUtils.is_json_serializable(42))
print("string:", JsonUtils.is_json_serializable("hello"))

local serializable = {
    name = "test",
    values = {1, 2, 3}
}
print("table:", JsonUtils.is_json_serializable(serializable))

-- 函数不可序列化
local withFunc = {
    name = "test",
    func = function() return 1 end
}
print("table with function:", JsonUtils.is_json_serializable(withFunc))

-- 循环引用不可序列化
local circular = {}
circular.self = circular
print("circular reference:", JsonUtils.is_json_serializable(circular))

print("")

-------------------------------------------------------------------------------
-- 7. 文件操作
-------------------------------------------------------------------------------

print("7. File Operations")
print("------------------")

-- 创建测试数据
local testData = {
    application = {
        name = "MyApp",
        version = "1.0.0",
        settings = {
            debug = false,
            logLevel = "info"
        }
    },
    users = {
        {id = 1, name = "Alice"},
        {id = 2, name = "Bob"}
    }
}

-- 写入文件
local filename = "test_config.json"
print("Writing to:", filename)
JsonUtils.write_file_pretty(filename, testData)

-- 读取文件
print("\nReading from:", filename)
local loadedData = JsonUtils.read_file(filename)
print("Loaded application name:", loadedData.application.name)
print("Loaded version:", loadedData.application.version)

-- 显示文件内容
print("\nFile contents:")
local file = io.open(filename, "r")
if file then
    print(file:read("*a"))
    file:close()
end

-- 清理
os.remove(filename)

print("")

-------------------------------------------------------------------------------
-- 8. 字符串化（调试）
-------------------------------------------------------------------------------

print("8. Stringify (Debug)")
print("-------------------")

local debugObj = {
    name = "Debug",
    nested = {
        level1 = {
            level2 = {
                level3 = {
                    value = "very deep"
                }
            }
        }
    },
    array = {1, 2, {3, 4}}
}

print("Stringify output:")
print(JsonUtils.stringify(debugObj))

-- 限制深度
print("\nWith max_depth = 2:")
print(JsonUtils.stringify(debugObj, 2))

print("")

-------------------------------------------------------------------------------
-- 9. 错误处理
-------------------------------------------------------------------------------

print("9. Error Handling")
print("-----------------")

-- 无效 JSON
local invalidJsons = {
    '{"key": }',           -- 缺少值
    '{key: "value"}',      -- 键未加引号
    '{"key": "value"',     -- 缺少闭合括号
    '[1, 2, 3,]',          -- 尾随逗号（可能允许）
    'undefined',           -- 非 JSON 类型
}

for i, invalid in ipairs(invalidJsons) do
    local result, err = JsonUtils.decode_safe(invalid)
    if err then
        print("Error for '" .. invalid .. "':")
        print("  " .. err)
    else
        print("Unexpectedly valid: " .. invalid)
    end
end

print("")

-------------------------------------------------------------------------------
-- 10. 循环引用检测
-------------------------------------------------------------------------------

print("10. Circular Reference Detection")
print("--------------------------------")

-- 创建循环引用
local circular = {}
circular.self = circular
circular.data = "some data"

-- 尝试编码
local result, err = JsonUtils.encode_safe(circular)
if err then
    print("Correctly detected circular reference:")
    print("  " .. err)
end

-- 安全处理：先移除循环引用再编码
local safeCopy = JsonUtils.deep_clone(circular)
safeCopy.self = nil  -- 移除循环引用
print("\nSafe encoding after removing circular ref:")
print(JsonUtils.encode(safeCopy))

print("")

-------------------------------------------------------------------------------
-- 11. 性能测试
-------------------------------------------------------------------------------

print("11. Performance Test")
print("--------------------")

-- 大数组
local largeArray = {}
for i = 1, 1000 do
    largeArray[i] = i
end

local start = os.clock()
local encoded = JsonUtils.encode(largeArray)
local encodeTime = os.clock() - start

start = os.clock()
local decoded = JsonUtils.decode(encoded)
local decodeTime = os.clock() - start

print(string.format("Large array (1000 items)"))
print(string.format("  Encode time: %.4f seconds", encodeTime))
print(string.format("  Decode time: %.4f seconds", decodeTime))
print(string.format("  First item: %s", decoded[1]))
print(string.format("  Last item: %s", decoded[1000]))

-- 大对象
local largeObj = {}
for i = 1, 100 do
    largeObj["key" .. i] = "value" .. i
end

start = os.clock()
encoded = JsonUtils.encode(largeObj)
encodeTime = os.clock() - start

start = os.clock()
decoded = JsonUtils.decode(encoded)
decodeTime = os.clock() - start

print(string.format("\nLarge object (100 keys)"))
print(string.format("  Encode time: %.4f seconds", encodeTime))
print(string.format("  Decode time: %.4f seconds", decodeTime))

print("\n=== End of Advanced Usage Examples ===")