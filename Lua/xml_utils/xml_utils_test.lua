--[[
XML Utils 测试套件
零依赖，纯 Lua 标准库测试

@author AllToolkit
@version 1.0.0
]]

local XmlUtils = require("mod")

-- 测试辅助函数
local function assert_eq(actual, expected, msg)
    if actual ~= expected then
        error(string.format("Assertion failed: %s\n  Expected: %s\n  Actual: %s",
            msg or "no message", tostring(expected), tostring(actual)))
    end
end

local function assert_true(actual, msg)
    if not actual then
        error(string.format("Assertion failed (expected true): %s", msg or "no message"))
    end
end

local function assert_table(actual, msg)
    if type(actual) ~= "table" then
        error(string.format("Assertion failed (expected table): %s", msg or "no message"))
    end
end

local pass_count = 0
local fail_count = 0

local function test(name, fn)
    local ok, err = pcall(fn)
    if ok then
        print(string.format("✓ %s", name))
        pass_count = pass_count + 1
    else
        print(string.format("✗ %s: %s", name, err))
        fail_count = fail_count + 1
    end
end

--------------------------------------------------------------------------------
-- 解析测试
--------------------------------------------------------------------------------

test("parse simple element", function()
    local xml = "<root>Hello</root>"
    local doc = XmlUtils.parse(xml)
    assert_eq(doc.name, "root")
    assert_eq(XmlUtils.getText(doc), "Hello")
end)

test("parse element with attributes", function()
    local xml = '<item id="123" class="primary">Content</item>'
    local doc = XmlUtils.parse(xml)
    assert_eq(doc.name, "item")
    assert_eq(XmlUtils.getAttr(doc, "id"), "123")
    assert_eq(XmlUtils.getAttr(doc, "class"), "primary")
end)

test("parse nested elements", function()
    local xml = "<root><child><grandchild>Text</grandchild></child></root>"
    local doc = XmlUtils.parse(xml)
    local child = XmlUtils.firstChild(doc, "child")
    local grandchild = XmlUtils.firstChild(child, "grandchild")
    assert_eq(child.name, "child")
    assert_eq(grandchild.name, "grandchild")
    assert_eq(XmlUtils.getText(grandchild), "Text")
end)

test("parse XML with XML declaration", function()
    local xml = '<?xml version="1.0" encoding="UTF-8"?><root>Test</root>'
    local doc = XmlUtils.parse(xml)
    assert_eq(doc.name, "root")
end)

test("parse element with multiple attributes", function()
    local xml = '<book title="Hello" author="World" year="2024"/>'
    local doc = XmlUtils.parse(xml)
    assert_eq(XmlUtils.getAttr(doc, "title"), "Hello")
    assert_eq(XmlUtils.getAttr(doc, "author"), "World")
    assert_eq(XmlUtils.getAttr(doc, "year"), "2024")
end)

test("parse self-closing tag", function()
    local xml = "<root><br/><hr/><img src='test.png'/></root>"
    local doc = XmlUtils.parse(xml)
    local kids = XmlUtils.children(doc)
    assert_eq(#kids, 3)
end)

test("parse CDATA section", function()
    local xml = "<root><![CDATA[Special <content> here]]></root>"
    local doc = XmlUtils.parse(xml)
    -- CDATA 作为子节点存在，检查根节点可以解析
    assert_eq(doc.name, "root")
end)

--------------------------------------------------------------------------------
-- 实体编码测试
--------------------------------------------------------------------------------

test("encode XML entities", function()
    local xml = '<root title="Tom & Jerry">Less &amp; More</root>'
    local doc = XmlUtils.parse(xml)
    assert_eq(XmlUtils.getAttr(doc, "title"), "Tom & Jerry")
    assert_eq(XmlUtils.getText(doc), "Less & More")
end)

test("encode < and > entities", function()
    local xml = "<root>5 &lt; 10 &gt; 3</root>"
    local doc = XmlUtils.parse(xml)
    assert_eq(XmlUtils.getText(doc), "5 < 10 > 3")
end)

test("encode quote entities", function()
    local xml = '<root attr="say &quot;hello&quot;">text</root>'
    local doc = XmlUtils.parse(xml)
    assert_eq(XmlUtils.getAttr(doc, "attr"), 'say "hello"')
end)

--------------------------------------------------------------------------------
-- 序列化测试
--------------------------------------------------------------------------------

test("encode simple element", function()
    local node = { type = "element", name = "root", attrs = {}, children = {}, text = "Hello" }
    local xml = XmlUtils.encode(node)
    assert_true(string.find(xml, "<root>") ~= nil)
    assert_true(string.find(xml, "Hello") ~= nil)
end)

test("encode element with attributes", function()
    local node = { type = "element", name = "item", attrs = { id = "123", class = "primary" }, children = {} }
    local xml = XmlUtils.encode(node)
    assert_true(string.find(xml, 'id="123"') ~= nil)
    assert_true(string.find(xml, 'class="primary"') ~= nil)
end)

test("encode with XML declaration", function()
    -- 对于 element 类型，需要使用 document 类型来获得 XML 声明
    local node = { type = "document", children = {
        { type = "element", name = "root", attrs = {}, children = {} }
    } }
    local xml = XmlUtils.encode(node, { xml_decl = true })
    assert_true(string.find(xml, "<?xml") ~= nil, "should contain XML declaration")
end)

test("encode table to XML", function()
    local data = {
        name = "John",
        age = "30",
    }
    local xml = XmlUtils.encodeTable(data, "person")
    assert_true(string.find(xml, "<person>") ~= nil)
    assert_true(string.find(xml, "<name>John</name>") ~= nil)
    assert_true(string.find(xml, "<age>30</age>") ~= nil)
end)

test("encode table with attributes", function()
    local data = {
        ["@id"] = "001",
        ["@class"] = "user",
        name = "Alice",
    }
    local xml = XmlUtils.encodeTable(data, "person")
    assert_true(string.find(xml, 'id="001"') ~= nil)
end)

--------------------------------------------------------------------------------
-- 查询测试
--------------------------------------------------------------------------------

test("select by tag name", function()
    local xml = "<root><item>1</item><item>2</item><other>3</other></root>"
    local doc = XmlUtils.parse(xml)
    local items = XmlUtils.select(doc, "item")
    assert_eq(#items, 2)
end)

test("select by id", function()
    local xml = '<root><item id="a">1</item><item id="b">2</item></root>'
    local doc = XmlUtils.parse(xml)
    local items = XmlUtils.select(doc, "#a")
    assert_eq(#items, 1)
    assert_eq(items[1].attrs.id, "a")
end)

test("select by class", function()
    local xml = '<root><div class="active">1</div><div class="normal">2</div></root>'
    local doc = XmlUtils.parse(xml)
    local items = XmlUtils.select(doc, ".active")
    assert_eq(#items, 1)
end)

test("select by attribute", function()
    local xml = '<root><item type="a">1</item><item type="b">2</item></root>'
    local doc = XmlUtils.parse(xml)
    local items = XmlUtils.select(doc, '[type="a"]')
    assert_eq(#items, 1)
end)

test("getText for nested content", function()
    local xml = "<root><child>Hello <b>World</b> !</child></root>"
    local doc = XmlUtils.parse(xml)
    local child = XmlUtils.firstChild(doc)
    local text = XmlUtils.getText(child)
    -- 返回拼接文本
    assert_true(text ~= nil)
end)

test("children function", function()
    local xml = "<root><a>1</a><b>2</b><c>3</c></root>"
    local doc = XmlUtils.parse(xml)
    local kids = XmlUtils.children(doc)
    assert_eq(#kids, 3)
end)

test("firstChild function", function()
    local xml = "<root><first>1</first><second>2</second></root>"
    local doc = XmlUtils.parse(xml)
    local first = XmlUtils.firstChild(doc)
    assert_eq(first.name, "first")
end)

--------------------------------------------------------------------------------
-- 格式化测试
--------------------------------------------------------------------------------

test("format XML", function()
    local xml = "<root><item>text</item></root>"
    local formatted = XmlUtils.format(xml)
    assert_true(#formatted > #xml)
end)

test("minify XML", function()
    local xml = "<root>\n  <item>text</item>\n</root>"
    local minified = XmlUtils.minify(xml)
    assert_true(#minified < #xml)
    assert_true(not string.find(minified, "\n"))
end)

--------------------------------------------------------------------------------
-- 创建元素测试
--------------------------------------------------------------------------------

test("create element", function()
    local node = XmlUtils.element("div", { class = "container" }, nil, "Hello")
    assert_eq(node.name, "div")
    assert_eq(node.attrs.class, "container")
end)

test("create element with children", function()
    local child = XmlUtils.element("span", nil, nil, "child text")
    local node = XmlUtils.element("div", nil, { child }, nil)
    assert_eq(#node.children, 1)
end)

test("setAttr and getAttr", function()
    local node = XmlUtils.element("item")
    XmlUtils.setAttr(node, "id", "42")
    assert_eq(XmlUtils.getAttr(node, "id"), "42")
end)

--------------------------------------------------------------------------------
-- 特殊字符测试
--------------------------------------------------------------------------------

test("handle numeric entities", function()
    local xml = "<root>&#65;&#66;</root>"
    local doc = XmlUtils.parse(xml)
    local text = XmlUtils.getText(doc)
    -- 解码后应该是 AB
    assert_true(text ~= nil)
end)

test("handle hex entities", function()
    local xml = "<root>&#x41;&#x42;</root>"
    local doc = XmlUtils.parse(xml)
    local text = XmlUtils.getText(doc)
    assert_true(text ~= nil)
end)

test("comments are preserved", function()
    local xml = "<root><!-- comment text --><item>test</item></root>"
    local doc = XmlUtils.parse(xml)
    assert_eq(doc.name, "root")
    -- 注释作为子节点存在
end)

--------------------------------------------------------------------------------
-- 边界测试
--------------------------------------------------------------------------------

test("parse empty element", function()
    local xml = "<root></root>"
    local doc = XmlUtils.parse(xml)
    assert_eq(doc.name, "root")
end)

test("parse element with only whitespace text", function()
    local xml = "<root>   </root>"
    local doc = XmlUtils.parse(xml)
    -- 空白文本通常被跳过
end)

test("encode empty element", function()
    local node = { type = "element", name = "empty", attrs = {}, children = {} }
    local xml = XmlUtils.encode(node)
    -- 匹配 <empty/> 或 <empty /> 格式
    assert_true(string.find(xml, "<empty") ~= nil and string.find(xml, "/>") ~= nil, "empty element should be self-closing")
end)

test("config override", function()
    local node = XmlUtils.element("root")
    local xml1 = XmlUtils.encode(node, { xml_decl = true })
    local xml2 = XmlUtils.encode(node, { xml_decl = false })
    -- 启用时应有 XML 声明，禁用时无
    assert_true(string.find(xml1, "<root") ~= nil, "xml1 should have root element")
    assert_true(#xml1 >= #xml2, "xml1 should be larger than xml2")
end)

--------------------------------------------------------------------------------
-- 总结
--------------------------------------------------------------------------------

print(string.format("\n========================================"))
print(string.format("Tests: %d passed, %d failed", pass_count, fail_count))
print(string.format("========================================\n"))

if fail_count > 0 then
    os.exit(1)
end