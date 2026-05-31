--[[
XML Utils 📄
Lua XML 解析与序列化工具库 - 零依赖，生产就绪

提供完整的 XML 解析、编码、格式化、查询等功能。
纯 Lua 标准库实现，无需任何外部依赖。

功能列表:
- 解析: SAX 流式解析 + DOM 树解析
- 编码: Lua 表转 XML 字符串
- 格式化: 美化输出 / 压缩输出
- 查询: CSS 选择器风格元素查找
- 构建: 程序化创建 XML 元素

@author AllToolkit
@version 1.0.0
@license MIT
]]

local XmlUtils = {}
XmlUtils.__index = XmlUtils

-- 版本信息
XmlUtils.VERSION = "1.0.0"

--------------------------------------------------------------------------------
-- 错误定义
--------------------------------------------------------------------------------

XmlUtils.Error = {
    ParseError = "XML parse error",
    InvalidInput = "Invalid input",
    InvalidNode = "Invalid node type",
    EncodingError = "XML encoding error",
    MaxDepthExceeded = "Maximum nesting depth exceeded",
}

--------------------------------------------------------------------------------
-- 配置
--------------------------------------------------------------------------------

XmlUtils.Config = {
    max_depth = 200,
    indent = "  ",
    pretty = true,
    xml_decl = true,
    root_element = nil,
    attr_quote = '"',
    encode_entities = true,
}

--------------------------------------------------------------------------------
-- 内部工具函数
--------------------------------------------------------------------------------

local type = type
local tostring = tostring
local pairs = pairs
local ipairs = ipairs
local table_concat = table.concat
local string_sub = string.sub
local string_find = string.find
local string_match = string.match
local string_gmatch = string.gmatch
local string_gsub = string.gsub
local string_char = string.char
local string_rep = string.rep
local table_insert = table.insert
local table_sort = table.sort
local math_max = math.max
local table_remove = table.remove

-- HTML 实体编码映射
local ENTITIES = {
    ["&"] = "&amp;",
    ["<"] = "&lt;",
    [">"] = "&gt;",
    ['"'] = "&quot;",
    ["'"] = "&apos;",
}

-- 反向映射（解码时用）
local DECODE_ENTITIES = {}
for k, v in pairs(ENTITIES) do
    DECODE_ENTITIES[v] = k
end

--------------------------------------------------------------------------------
-- 实体编码/解码
--------------------------------------------------------------------------------

--- 编码 XML 特殊字符
local function encodeEntities(str)
    if not str then return "" end
    str = tostring(str)
    return string_gsub(str, "[&<>\"']", ENTITIES)
end

--- 解码 XML 实体
local function decodeEntities(str)
    if not str then return "" end
    str = tostring(str)
    for entity, char in pairs(DECODE_ENTITIES) do
        str = string_gsub(str, entity, char)
    end
    -- 处理数值实体
    str = string_gsub(str, "&#(%d+);", function(n)
        local code = tonumber(n)
        if code then return string_char(code) end
        return entity
    end)
    str = string_gsub(str, "&#x([%da-fA-F]+);", function(n)
        local code = tonumber(n, 16)
        if code then return string_char(code) end
        return entity
    end)
    return str
end

--------------------------------------------------------------------------------
-- DOM 节点类
--------------------------------------------------------------------------------

--- 创建新的 XML 节点
local function newNode(name)
    return {
        type = "element",
        name = name,
        attrs = {},
        children = {},
        parent = nil,
        text = nil,
        comment = nil,
    }
end

--------------------------------------------------------------------------------
-- SAX 解析器
--------------------------------------------------------------------------------

local function parseSAX(xml, callbacks, config)
    config = config or {}
    local pos = 1
    local len = #xml
    local _ = config

    local function skipWhitespace()
        while pos <= len do
            local c = string_sub(xml, pos, pos)
            if c ~= " " and c ~= "\t" and c ~= "\r" and c ~= "\n" then
                break
            end
            pos = pos + 1
        end
    end

    local function findTagEnd()
        return string_find(xml, ">", pos, true)
    end

    local function parseAttributes(tagStart, tagEnd)
        local attrs = {}
        local tagContent = string_sub(xml, tagStart, tagEnd - 1)

        -- 逐个解析属性: name="value" 或 name='value'
        local pos = 1
        local tagLen = #tagContent

        while pos <= tagLen do
            -- 跳过空白
            while pos <= tagLen and string_sub(tagContent, pos, pos):match("%s") do
                pos = pos + 1
            end
            if pos > tagLen then break end

            -- 读取属性名
            local nameStart = pos
            while pos <= tagLen and string_sub(tagContent, pos, pos):match("[_%:%w%-]") do
                pos = pos + 1
            end
            local attrName = string_sub(tagContent, nameStart, pos - 1)
            if attrName == "" then break end

            -- 跳过空白查找 =
            while pos <= tagLen and string_sub(tagContent, pos, pos):match("%s") do
                pos = pos + 1
            end

            if pos <= tagLen and string_sub(tagContent, pos, pos) == "=" then
                pos = pos + 1
                -- 跳过空白
                while pos <= tagLen and string_sub(tagContent, pos, pos):match("%s") do
                    pos = pos + 1
                end

                -- 读取值
                local quote = ""
                if pos <= tagLen and (string_sub(tagContent, pos, pos) == '"' or string_sub(tagContent, pos, pos) == "'") then
                    quote = string_sub(tagContent, pos, pos)
                    pos = pos + 1
                end

                local valueStart = pos
                if quote ~= "" then
                    -- 引号值，找配对引号
                    while pos <= tagLen and string_sub(tagContent, pos, pos) ~= quote do
                        pos = pos + 1
                    end
                else
                    -- 无引号值，到空白或 /> 停止
                    while pos <= tagLen and not string_sub(tagContent, pos, pos):match("%s") and string_sub(tagContent, pos, pos + 1) ~= "/>" do
                        pos = pos + 1
                    end
                end

                local attrValue = string_sub(tagContent, valueStart, pos - 1)
                if quote ~= "" then
                    pos = pos + 1  -- 跳过结束引号
                end

                attrs[attrName] = decodeEntities(attrValue)
            end
        end

        return attrs
    end

    while pos <= len do
        skipWhitespace()
        if pos > len then break end

        if string_sub(xml, pos, pos) == "<" then
            if string_sub(xml, pos, pos + 2) == "<?xml" then
                local tagEnd = string_find(xml, "?>", pos, true)
                if tagEnd then
                    if callbacks.xmlDecl then
                        callbacks.xmlDecl(string_sub(xml, pos, tagEnd + 1))
                    end
                    pos = tagEnd + 2
                end
            elseif string_sub(xml, pos, pos + 3) == "<!--" then
                local tagEnd = string_find(xml, "-->", pos, true)
                if tagEnd then
                    local comment = string_sub(xml, pos + 4, tagEnd - 1)
                    if callbacks.comment then
                        callbacks.comment(comment)
                    end
                    pos = tagEnd + 3
                end
            elseif string_sub(xml, pos, pos + 8) == "<![CDATA[" then
                local tagEnd = string_find(xml, "]]>", pos, true)
                if tagEnd then
                    local cdata = string_sub(xml, pos + 9, tagEnd - 1)
                    if callbacks.cdata then
                        callbacks.cdata(cdata)
                    end
                    pos = tagEnd + 3
                end
            elseif string_sub(xml, pos, pos + 1) == "</" then
                local tagEnd = findTagEnd()
                if tagEnd then
                    local tag = string_sub(xml, pos + 2, tagEnd - 1)
                    local name = string_match(tag, "^%s*([_%a][_%:%w%-]*)")
                    if name then
                        if callbacks.endElement then
                            callbacks.endElement(name)
                        end
                    end
                    pos = tagEnd + 1
                end
            else
                local tagEnd = findTagEnd()
                if tagEnd then
                    local tag = string_sub(xml, pos + 1, tagEnd - 1)
                    local selfClose = string_sub(tag, -1) == "/"
                    if selfClose then
                        tag = string_sub(tag, 1, -2)
                    end

                    local name = string_match(tag, "^%s*([_%a][_%:%w%-]*)")
                    if name then
                        -- Position right after the name in original XML
                        local attrStartPos = pos + string_find(tag, name) + #name
                        local attrs = parseAttributes(attrStartPos, tagEnd)
                        if callbacks.startElement then
                            callbacks.startElement(name, attrs)
                        end
                        if callbacks.endElement and selfClose then
                            callbacks.endElement(name)
                        end
                    end
                    pos = tagEnd + 1
                end
            end
        else
            local textStart = pos
            while pos <= len and string_sub(xml, pos, pos) ~= "<" do
                pos = pos + 1
            end
            local text = string_sub(xml, textStart, pos - 1)
            -- 去除首尾空白但保留内部空白结构
            text = string_match(text, "^%s*(.-)%s*$")
            if text ~= "" and callbacks.text then
                callbacks.text(decodeEntities(text))
            end
        end
    end
end

--------------------------------------------------------------------------------
-- DOM 解析器
--------------------------------------------------------------------------------

local function parseDOM(xml, config)
    config = config or {}
    local root = nil
    local current = nil
    local stack = {}
    local depth = 0

    parseSAX(xml, {
        xmlDecl = function(decl)
            if not root then
                root = { type = "document", children = {}, declaration = decl }
                current = root
            end
        end,
        startElement = function(name, attrs)
            depth = depth + 1
            if config.max_depth and depth > config.max_depth then
                return false, "MaxDepthExceeded"
            end

            local node = newNode(name)
            node.attrs = attrs
            node.parent = current

            if current then
                table_insert(current.children, node)
            end
            table_insert(stack, current)
            current = node

            if not root then
                root = node
            end
        end,
        endElement = function(name)
            if current and current.name == name then
                current = table_remove(stack)
            end
            depth = depth - 1
        end,
        text = function(text)
            if current then
                if current.type == "element" then
                    current.text = (current.text or "") .. text
                end
            end
        end,
        comment = function(content)
            if current then
                local commentNode = { type = "comment", content = content }
                table_insert(current.children, commentNode)
            end
        end,
        cdata = function(content)
            if current then
                local cdataNode = { type = "cdata", content = content }
                table_insert(current.children, cdataNode)
            end
        end,
    }, config)

    return root
end

--------------------------------------------------------------------------------
-- DOM 查询
--------------------------------------------------------------------------------

function XmlUtils.select(root, selector)
    local results = {}

    local function matches(node, sel)
        if not node or node.type ~= "element" then return false end

        -- 检查选择器类型并匹配
        local firstChar = string_sub(sel, 1, 1)

        if firstChar == "#" then
            -- ID 选择器
            local id = string_sub(sel, 2)
            return node.attrs.id == id
        elseif firstChar == "." then
            -- 类选择器
            local class = string_sub(sel, 2)
            local nodeClass = node.attrs.class or ""
            return string_find(nodeClass, class) ~= nil
        elseif firstChar == "[" then
            -- 属性选择器 [attr] 或 [attr=value]
            local inner = string_sub(sel, 2, -2)
            local eqPos = string_find(inner, "=")
            if eqPos then
                local attrName = string_sub(inner, 1, eqPos - 1)
                local attrValue = string_sub(inner, eqPos + 1)
                -- 去除引号
                attrValue = string_match(attrValue, "^[%\'\"](.-)[%\'\"]$") or attrValue
                return node.attrs[attrName] == attrValue
            else
                return node.attrs[inner] ~= nil
            end
        else
            -- 标签选择器
            return node.name == sel
        end
    end

    local function traverse(node)
        if node.type == "element" then
            if matches(node, selector) then
                table_insert(results, node)
            end
            if node.children then
                for _, child in ipairs(node.children) do
                    traverse(child)
                end
            end
        end
    end

    if root then
        traverse(root)
    end

    return results
end

function XmlUtils.getText(node)
    if not node then return "" end

    if node.type == "text" then
        return node.content or ""
    elseif node.type == "element" then
        local parts = {}
        if node.text then
            table_insert(parts, node.text)
        end
        if node.children then
            for _, child in ipairs(node.children) do
                local childText = XmlUtils.getText(child)
                if childText ~= "" then
                    table_insert(parts, childText)
                end
            end
        end
        return table_concat(parts, " ")
    end
    return ""
end

function XmlUtils.getAttr(node, attr)
    if node and node.attrs then
        return node.attrs[attr]
    end
    return nil
end

function XmlUtils.setAttr(node, attr, value)
    if node and node.type == "element" then
        node.attrs[attr] = value
    end
end

function XmlUtils.children(node, name)
    local kids = {}
    if node and node.children then
        for _, child in ipairs(node.children) do
            if child.type == "element" then
                if not name or child.name == name then
                    table_insert(kids, child)
                end
            end
        end
    end
    return kids
end

function XmlUtils.firstChild(node, name)
    local kids = XmlUtils.children(node, name)
    return kids[1]
end

--------------------------------------------------------------------------------
-- XML 序列化
--------------------------------------------------------------------------------

local function encodeNode(node, config, level)
    level = level or 0
    config = config or XmlUtils.Config

    if type(node) == "string" then
        return encodeEntities(node)
    end

    if node.type == "text" then
        return encodeEntities(node.content or "")
    end

    if node.type == "comment" then
        if config.pretty then
            return "\n" .. string_rep(config.indent, level) .. "<!--" .. (node.content or "") .. "-->"
        end
        return "<!--" .. (node.content or "") .. "-->"
    end

    if node.type == "cdata" then
        return "<![CDATA[" .. (node.content or "") .. "]]>"
    end

    if node.type == "document" then
        local parts = {}
        if config.xml_decl then
            table_insert(parts, '<?xml version="1.0" encoding="UTF-8"?>')
        end
        if node.children then
            for _, child in ipairs(node.children) do
                local childXml = encodeNode(child, config, level)
                if childXml ~= "" then
                    table_insert(parts, childXml)
                end
            end
        end
        return table_concat(parts, "\n")
    end

    if node.type == "element" then
        local indent = config.pretty and ("\n" .. string_rep(config.indent, level)) or ""
        local name = node.name or ""

        -- 属性字符串
        local attrParts = {}
        if node.attrs then
            for k, v in pairs(node.attrs) do
                table_insert(attrParts, k .. '="' .. encodeEntities(v) .. '"')
            end
        end
        local attrStr = #attrParts > 0 and (" " .. table_concat(attrParts, " ")) or ""

        -- 子内容
        local childXml = ""
        if node.children and #node.children > 0 then
            local childParts = {}
            for _, child in ipairs(node.children) do
                local c = encodeNode(child, config, level + 1)
                if c ~= "" then
                    table_insert(childParts, c)
                end
            end
            childXml = table_concat(childParts, "")
        end

        local text = node.text and encodeEntities(node.text) or ""
        local hasChildren = childXml ~= "" or (node.children and #node.children > 0)
        local isSelfClosing = not hasChildren and text == ""

        if isSelfClosing then
            return indent .. "<" .. name .. attrStr .. " />"
        elseif config.pretty and (hasChildren or text ~= "") then
            return indent .. "<" .. name .. attrStr .. ">" .. text .. childXml .. indent .. "</" .. name .. ">"
        else
            return "<" .. name .. attrStr .. ">" .. text .. childXml .. "</" .. name .. ">"
        end
    end

    if type(node) == "table" then
        local parts = {}
        for k, v in pairs(node) do
            if type(k) == "string" then
                table_insert(parts, tostring(k) .. '="' .. encodeEntities(v) .. '"')
            end
        end
        return table_concat(parts, " ")
    end

    return encodeEntities(tostring(node))
end

function XmlUtils.encode(node, config)
    config = config or {}
    for k, v in pairs(XmlUtils.Config) do
        if config[k] == nil then
            config[k] = v
        end
    end
    return encodeNode(node, config, 0)
end

--------------------------------------------------------------------------------
-- 便捷函数
--------------------------------------------------------------------------------

function XmlUtils.parse(xml, options)
    if type(xml) ~= "string" then
        error("XmlUtils.parse: xml must be a string")
    end

    local config = options or {}
    return parseDOM(xml, config)
end

function XmlUtils.encodeTable(data, rootName, config)
    rootName = rootName or "root"
    config = config or {}

    local function tableToXml(tbl, name, level)
        level = level or 0
        local indent = config.pretty and ("\n" .. string_rep(config.indent or "  ", level)) or ""
        local childIndent = config.pretty and ("\n" .. string_rep(config.indent or "  ", level + 1)) or ""

        if type(tbl) ~= "table" then
            return indent .. "<" .. name .. ">" .. encodeEntities(tostring(tbl)) .. "</" .. name .. ">"
        end

        -- 检查是否为纯数组
        local isArray = true
        for k in pairs(tbl) do
            if type(k) ~= "number" then
                isArray = false
                break
            end
        end

        if isArray then
            local parts = {}
            for _, v in ipairs(tbl) do
                if type(v) == "table" then
                    table_insert(parts, tableToXml(v, name, level + 1))
                else
                    table_insert(parts, childIndent .. "<" .. name .. ">" .. encodeEntities(tostring(v)) .. "</" .. name .. ">")
                end
            end
            return indent .. "<" .. name .. ">" .. table_concat(parts, "") .. indent .. "</" .. name .. ">"
        else
            local parts = {}
            local attrs = {}
            local children = {}

            for k, v in pairs(tbl) do
                if type(k) == "string" then
                    local firstChar = string_sub(k, 1, 1)
                    if firstChar == "@" then
                        local attrName = string_sub(k, 2)
                        table_insert(attrs, attrName .. '="' .. encodeEntities(tostring(v)) .. '"')
                    elseif type(v) == "table" then
                        table_insert(children, tableToXml(v, k, level + 1))
                    else
                        table_insert(children, childIndent .. "<" .. k .. ">" .. encodeEntities(tostring(v)) .. "</" .. k .. ">")
                    end
                end
            end

            local attrStr = #attrs > 0 and (" " .. table_concat(attrs, " ")) or ""
            local childStr = table_concat(children, "")

            if childStr ~= "" and config.pretty then
                return indent .. "<" .. name .. attrStr .. ">" .. childStr .. indent .. "</" .. name .. ">"
            else
                return indent .. "<" .. name .. attrStr .. ">" .. childStr .. "</" .. name .. ">"
            end
        end
    end

    local xmlDecl = '<?xml version="1.0" encoding="UTF-8"?>'
    local rootXml = tableToXml(data, rootName, 0)

    if config.xml_decl == false then
        return rootXml
    end
    return xmlDecl .. "\n" .. rootXml
end

function XmlUtils.format(xml, indent)
    local node = parseDOM(xml, {})
    if not node then return xml end

    local config = {
        pretty = true,
        indent = indent or "  ",
        xml_decl = false,
    }
    return encodeNode(node, config, 0)
end

function XmlUtils.minify(xml)
    xml = string_gsub(xml, "<!--.--->", "")
    xml = string_gsub(xml, "%s+", " ")
    xml = string_gsub(xml, "%s*>%s*<", "><")
    return xml
end

function XmlUtils.element(name, attrs, children, text)
    local node = newNode(name)
    if attrs then
        for k, v in pairs(attrs) do
            node.attrs[k] = v
        end
    end
    if children then
        for _, child in ipairs(children) do
            if type(child) == "table" then
                table_insert(node.children, child)
            else
                table_insert(node.children, { type = "text", content = tostring(child) })
            end
        end
    end
    if text then
        node.text = tostring(text)
    end
    return node
end

--------------------------------------------------------------------------------
-- 导出
--------------------------------------------------------------------------------

return XmlUtils