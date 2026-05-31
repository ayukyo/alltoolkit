local XmlUtils = require("mod")

-- Detailed trace
local xml = "<root><item id=\"a\">1</item></root>"
print("Input XML:", xml)

-- Parse step by step
local function traceSAX(xml, callbacks)
    local pos = 1
    local len = #xml

    local function skipWhitespace()
        while pos <= len do
            local c = string.sub(xml, pos, pos)
            if c ~= " " and c ~= "\t" and c ~= "\r" and c ~= "\n" then
                break
            end
            pos = pos + 1
        end
    end

    local function findTagEnd()
        return string.find(xml, ">", pos, true)
    end

    local function parseAttributes(tagStart, tagEnd)
        local attrs = {}
        local tagContent = string.sub(xml, tagStart, tagEnd - 1)
        print("  parseAttributes: tagContent =", tagContent)

        local pos = 1
        local tagLen = #tagContent

        while pos <= tagLen do
            while pos <= tagLen and string.sub(tagContent, pos, pos):match("%s") do
                pos = pos + 1
            end
            if pos > tagLen then break end

            local nameStart = pos
            while pos <= tagLen and string.sub(tagContent, pos, pos):match("[_%:%w%-]") do
                pos = pos + 1
            end
            local attrName = string.sub(tagContent, nameStart, pos - 1)
            if attrName == "" then break end

            while pos <= tagLen and string.sub(tagContent, pos, pos):match("%s") do
                pos = pos + 1
            end

            if pos <= tagLen and string.sub(tagContent, pos, pos) == "=" then
                pos = pos + 1
                while pos <= tagLen and string.sub(tagContent, pos, pos):match("%s") do
                    pos = pos + 1
                end

                local quote = ""
                if pos <= tagLen and (string.sub(tagContent, pos, pos) == '"' or string.sub(tagContent, pos, pos) == "'") then
                    quote = string.sub(tagContent, pos, pos)
                    pos = pos + 1
                end

                local valueStart = pos
                if quote ~= "" then
                    while pos <= tagLen and string.sub(tagContent, pos, pos) ~= quote do
                        pos = pos + 1
                    end
                else
                    while pos <= tagLen and not string.sub(tagContent, pos, pos):match("%s") and string.sub(tagContent, pos, pos + 1) ~= "/>" do
                        pos = pos + 1
                    end
                end

                local attrValue = string.sub(tagContent, valueStart, pos - 1)
                if quote ~= "" then
                    pos = pos + 1
                end

                print("    Parsed attr:", attrName, "=", attrValue)
                attrs[attrName] = attrValue
            end
        end

        return attrs
    end

    while pos <= len do
        skipWhitespace()
        if pos > len then break end

        if string.sub(xml, pos, pos) == "<" then
            if string.sub(xml, pos, pos + 3) == "<!--" then
                pos = pos + 4
            elseif string.sub(xml, pos, pos + 1) == "</" then
                local tagEnd = findTagEnd()
                if tagEnd then
                    local tag = string.sub(xml, pos + 2, tagEnd - 1)
                    print("End tag:", tag)
                    pos = tagEnd + 1
                end
            else
                local tagEnd = findTagEnd()
                if tagEnd then
                    local tag = string.sub(xml, pos + 1, tagEnd - 1)
                    local selfClose = string.sub(tag, -1) == "/"
                    if selfClose then
                        tag = string.sub(tag, 1, -2)
                    end

                    print("Start tag:", tag)
                    local name = string.match(tag, "^%s*([_%a][_%:%w%-]*)")
                    if name then
                        local namePos = string.find(tag, name)
                        print("  name:", name, "at", namePos)
                        local attrs = parseAttributes(namePos + #name, tagEnd)
                        print("  parsed attrs:", attrs)
                        pos = tagEnd + 1
                    end
                end
            end
        else
            while pos <= len and string.sub(xml, pos, pos) ~= "<" do
                pos = pos + 1
            end
        end
    end
end

traceSAX(xml)