local XmlUtils = require("mod")
local xml = '<root attr="a & b < c > d \'quotes\'">5 &lt; 10</root>'
print("Input XML:", xml)
print("Length:", #xml)

local doc = XmlUtils.parse(xml)
print("Root name:", doc.name)
print("Root attr:", doc.attrs.attr)
print("Root text:", doc.text or "(nil)")
print("Root full attrs:", doc.attrs)

-- Check direct attribute access
if doc.attrs then
    for k, v in pairs(doc.attrs) do
        print("  attr key:", k, "value:", v)
    end
end