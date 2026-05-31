#!/usr/bin/env lua
--[[
XML Utils 示例
展示 xml_utils 模块的主要功能
]]

local XmlUtils = require("mod")

print("========================================")
print("XML Utils - 示例程序")
print("========================================\n")

--------------------------------------------------------------------------------
-- 1. 解析 XML
--------------------------------------------------------------------------------

print("--- 1. 解析 XML ---")

local xml1 = [[<?xml version="1.0" encoding="UTF-8"?>
<catalog>
    <book id="1" category="fiction">
        <title>The Great Gatsby</title>
        <author>F. Scott Fitzgerald</author>
        <year>1925</year>
    </book>
    <book id="2" category="tech">
        <title>Programming in Lua</title>
        <author>Roberto Ierusalimschy</author>
        <year>2016</year>
    </book>
</catalog>]]

local doc = XmlUtils.parse(xml1)
print("Root element:", doc.name)

local books = XmlUtils.select(doc, "book")
print("Found", #books, "books")

for i, book in ipairs(books) do
    local title = XmlUtils.select(book, "title")[1]
    local author = XmlUtils.select(book, "author")[1]
    print(string.format("  Book %d: %s by %s", i, XmlUtils.getText(title), XmlUtils.getText(author)))
end

--------------------------------------------------------------------------------
-- 2. 编码 Lua 表为 XML
--------------------------------------------------------------------------------

print("\n--- 2. 编码 Lua 表为 XML ---")

local data = {
    person = {
        ["@id"] = "001",
        ["@class"] = "user developer",
        name = "Alice",
        email = "alice@example.com",
        roles = {
            role = { "admin", "developer" }
        }
    }
}

local xml2 = XmlUtils.encodeTable(data, "person", { xml_decl = true, pretty = true })
print(xml2)

--------------------------------------------------------------------------------
-- 3. 程序化创建 XML
--------------------------------------------------------------------------------

print("\n--- 3. 程序化创建 XML ---")

local root = XmlUtils.element("div", { class = "container" }, nil, nil)
local h1 = XmlUtils.element("h1", nil, nil, "Hello World")
local p = XmlUtils.element("p", { style = "color: blue;" }, nil, "This is a paragraph")
local ul = XmlUtils.element("ul", nil, {
    XmlUtils.element("li", nil, nil, "Item 1"),
    XmlUtils.element("li", nil, nil, "Item 2"),
    XmlUtils.element("li", nil, nil, "Item 3"),
})

root.children = { h1, p, ul }
local xml3 = XmlUtils.encode(root, { xml_decl = true, pretty = true })
print(xml3)

--------------------------------------------------------------------------------
-- 4. CSS 选择器查询
--------------------------------------------------------------------------------

print("\n--- 4. CSS 选择器查询 ---")

local xml4 = [[<html>
<body>
    <header id="main-header" class="header top">
        <h1>Welcome</h1>
    </header>
    <div class="content">
        <div class="article featured">Article 1</div>
        <div class="article">Article 2</div>
    </div>
    <footer class="footer header">Footer</footer>
</body>
</html>]]

local doc2 = XmlUtils.parse(xml4)

-- 按标签查询
local divs = XmlUtils.select(doc2, "div")
print("Found", #divs, "div elements")

-- 按 ID 查询
local header = XmlUtils.select(doc2, "#main-header")[1]
print("Header element:", header and header.name)

-- 按类查询
local featured = XmlUtils.select(doc2, ".featured")[1]
print("Featured article:", featured and XmlUtils.getText(featured))

-- 按属性查询
local footer = XmlUtils.select(doc2, "[class=\"footer\"]")[1]
print("Footer found:", footer ~= nil)

--------------------------------------------------------------------------------
-- 5. 格式化和压缩
--------------------------------------------------------------------------------

print("\n--- 5. 格式化和压缩 ---")

local xml5 = "<root><item>text</item><item>more</item></root>"
print("Original:", xml5)
print("Formatted:", XmlUtils.format(xml5))
print("Minified:", XmlUtils.minify(xml5))

--------------------------------------------------------------------------------
-- 6. 实体编码
--------------------------------------------------------------------------------

print("\n--- 6. 实体编码 ---")

local xml6 = '<root attr="a & b < c > d \'quotes\'">5 &lt; 10</root>'
local doc3 = XmlUtils.parse(xml6)
print("Parsed attr:", XmlUtils.getAttr(doc3, "attr"))
print("Parsed text:", XmlUtils.getText(doc3))

print("\n========================================")
print("示例完成")
print("========================================")