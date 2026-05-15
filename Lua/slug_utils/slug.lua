--[[
    slug_utils - URL Friendly String Generator for Lua
    
    A lightweight, zero-dependency module for converting strings into
    URL-friendly slugs. Handles Unicode transliteration, special characters,
    and customizable separators.
    
    Features:
    - Unicode to ASCII transliteration
    - Special character handling
    - Configurable separator
    - Case conversion options
    - Duplicate separator removal
    - Leading/trailing separator trimming
    
    License: MIT
]]

local slug_utils = {}

-- Unicode to ASCII transliteration table (common characters)
local transliteration_map = {
    -- Latin extended
    ["à"] = "a", ["á"] = "a", ["â"] = "a", ["ã"] = "a", ["ä"] = "a", ["å"] = "a",
    ["æ"] = "ae", ["ç"] = "c",
    ["è"] = "e", ["é"] = "e", ["ê"] = "e", ["ë"] = "e",
    ["ì"] = "i", ["í"] = "i", ["î"] = "i", ["ï"] = "i",
    ["ð"] = "d", ["ñ"] = "n",
    ["ò"] = "o", ["ó"] = "o", ["ô"] = "o", ["õ"] = "o", ["ö"] = "o", ["ø"] = "o",
    ["ù"] = "u", ["ú"] = "u", ["û"] = "u", ["ü"] = "u",
    ["ý"] = "y", ["ÿ"] = "y", ["þ"] = "th",
    ["ß"] = "ss",
    
    -- Uppercase versions
    ["À"] = "A", ["Á"] = "A", ["Â"] = "A", ["Ã"] = "A", ["Ä"] = "A", ["Å"] = "A",
    ["Æ"] = "AE", ["Ç"] = "C",
    ["È"] = "E", ["É"] = "E", ["Ê"] = "E", ["Ë"] = "E",
    ["Ì"] = "I", ["Í"] = "I", ["Î"] = "I", ["Ï"] = "I",
    ["Ð"] = "D", ["Ñ"] = "N",
    ["Ò"] = "O", ["Ó"] = "O", ["Ô"] = "O", ["Õ"] = "O", ["Ö"] = "O", ["Ø"] = "O",
    ["Ù"] = "U", ["Ú"] = "U", ["Û"] = "U", ["Ü"] = "U",
    ["Ý"] = "Y", ["Ÿ"] = "Y", ["Þ"] = "TH",
    
    -- Cyrillic (basic - lowercase)
    ["а"] = "a", ["б"] = "b", ["в"] = "v", ["г"] = "g", ["д"] = "d",
    ["е"] = "e", ["ё"] = "yo", ["ж"] = "zh", ["з"] = "z", ["и"] = "i",
    ["й"] = "y", ["к"] = "k", ["л"] = "l", ["м"] = "m", ["н"] = "n",
    ["о"] = "o", ["п"] = "p", ["р"] = "r", ["с"] = "s", ["т"] = "t",
    ["у"] = "u", ["ф"] = "f", ["х"] = "kh", ["ц"] = "ts", ["ч"] = "ch",
    ["ш"] = "sh", ["щ"] = "shch", ["ъ"] = "", ["ы"] = "y", ["ь"] = "",
    ["э"] = "e", ["ю"] = "yu", ["я"] = "ya",
    -- Cyrillic (basic - uppercase)
    ["А"] = "A", ["Б"] = "B", ["В"] = "V", ["Г"] = "G", ["Д"] = "D",
    ["Е"] = "E", ["Ё"] = "Yo", ["Ж"] = "Zh", ["З"] = "Z", ["И"] = "I",
    ["Й"] = "Y", ["К"] = "K", ["Л"] = "L", ["М"] = "M", ["Н"] = "N",
    ["О"] = "O", ["П"] = "P", ["Р"] = "R", ["С"] = "S", ["Т"] = "T",
    ["У"] = "U", ["Ф"] = "F", ["Х"] = "Kh", ["Ц"] = "Ts", ["Ч"] = "Ch",
    ["Ш"] = "Sh", ["Щ"] = "Shch", ["Ъ"] = "", ["Ы"] = "Y", ["Ь"] = "",
    ["Э"] = "E", ["Ю"] = "Yu", ["Я"] = "Ya",
    
    -- Greek
    ["α"] = "a", ["β"] = "b", ["γ"] = "g", ["δ"] = "d", ["ε"] = "e",
    ["ζ"] = "z", ["η"] = "i", ["θ"] = "th", ["ι"] = "i", ["κ"] = "k",
    ["λ"] = "l", ["μ"] = "m", ["ν"] = "n", ["ξ"] = "x", ["ο"] = "o",
    ["π"] = "p", ["ρ"] = "r", ["σ"] = "s", ["τ"] = "t", ["υ"] = "y",
    ["φ"] = "f", ["χ"] = "ch", ["ψ"] = "ps", ["ω"] = "o",
    
    -- German umlauts
    ["ä"] = "ae", ["ö"] = "oe", ["ü"] = "ue",
    ["Ä"] = "Ae", ["Ö"] = "Oe", ["Ü"] = "Ue",
    
    -- Chinese number words to pinyin (common ones)
    ["一"] = "yi", ["二"] = "er", ["三"] = "san", ["四"] = "si",
    ["五"] = "wu", ["六"] = "liu", ["七"] = "qi", ["八"] = "ba",
    ["九"] = "jiu", ["十"] = "shi",
}

-- Default options
local default_options = {
    separator = "-",
    lowercase = true,
    trim = true,
    transliterate = true,
}

--[[
    Merge two tables (options with defaults)
    @param options table User-provided options
    @param defaults table Default options
    @return table Merged options
]]
local function merge_options(options, defaults)
    local result = {}
    for k, v in pairs(defaults) do
        result[k] = v
    end
    for k, v in pairs(options or {}) do
        result[k] = v
    end
    return result
end

--[[
    Transliterate a character to ASCII
    @param char string Single character
    @return string Transliterated character or original
]]
local function transliterate_char(char)
    return transliteration_map[char] or char
end

--[[
    Check if a character is alphanumeric
    @param char string Single character
    @return boolean True if alphanumeric
]]
local function is_alphanumeric(char)
    local byte = string.byte(char)
    -- 0-9: 48-57, A-Z: 65-90, a-z: 97-122
    return (byte >= 48 and byte <= 57) or
           (byte >= 65 and byte <= 90) or
           (byte >= 97 and byte <= 122)
end

--[[
    Check if a character is a space or separator-like
    @param char string Single character
    @return boolean True if space-like
]]
local function is_space_like(char)
    local space_chars = " \t\n\r_-"
    return space_chars:find(char, 1, true) ~= nil
end

--[[
    Convert a string to a URL-friendly slug
    
    @param str string Input string
    @param options table Optional configuration:
        - separator: string to use as word separator (default: "-")
        - lowercase: boolean to convert to lowercase (default: true)
        - trim: boolean to trim leading/trailing separators (default: true)
        - transliterate: boolean to transliterate Unicode (default: true)
    @return string URL-friendly slug
]]
function slug_utils.slug(str, options)
    if type(str) ~= "string" then
        error("slug_utils.slug: expected string, got " .. type(str))
    end
    
    if str == "" then
        return ""
    end
    
    local opts = merge_options(options, default_options)
    local result = {}
    local last_was_separator = false
    
    -- Process each character
    for char in str:gmatch("[%z\1-\127\194-\244][\128-\191]*") do
        local processed = char
        
        -- Transliterate if enabled
        if opts.transliterate then
            processed = transliterate_char(processed)
        end
        
        -- Handle each character in the processed string
        for c in processed:gmatch(".") do
            if is_alphanumeric(c) then
                if opts.lowercase then
                    c = string.lower(c)
                end
                table.insert(result, c)
                last_was_separator = false
            elseif is_space_like(c) then
                if not last_was_separator then
                    table.insert(result, opts.separator)
                    last_was_separator = true
                end
            end
            -- Non-alphanumeric, non-space characters are ignored
        end
    end
    
    -- Join and trim
    local slug_str = table.concat(result)
    
    if opts.trim then
        -- Remove leading separator
        if slug_str:sub(1, #opts.separator) == opts.separator then
            slug_str = slug_str:sub(#opts.separator + 1)
        end
        -- Remove trailing separator
        if slug_str:sub(-#opts.separator) == opts.separator then
            slug_str = slug_str:sub(1, -#opts.separator - 1)
        end
    end
    
    return slug_str
end

--[[
    Generate a slug with custom separator
    
    @param str string Input string
    @param separator string Custom separator (default: "-")
    @return string URL-friendly slug
]]
function slug_utils.slug_with_separator(str, separator)
    return slug_utils.slug(str, { separator = separator or "-" })
end

--[[
    Generate a slug preserving case
    
    @param str string Input string
    @return string URL-friendly slug with original case
]]
function slug_utils.slug_preserve_case(str)
    return slug_utils.slug(str, { lowercase = false })
end

--[[
    Generate a slug with underscore separator
    
    @param str string Input string
    @return string URL-friendly slug with underscores
]]
function slug_utils.slug_underscore(str)
    return slug_utils.slug(str, { separator = "_" })
end

--[[
    Check if a string is a valid slug
    
    @param str string String to validate
    @param separator string Expected separator (default: "-")
    @return boolean True if valid slug
]]
function slug_utils.is_valid_slug(str, separator)
    if type(str) ~= "string" or str == "" then
        return false
    end
    
    local sep = separator or "-"
    local pattern = "^[%w" .. sep .. "]+$"
    
    -- Check format
    if not str:match(pattern) then
        return false
    end
    
    -- Check no leading/trailing separator
    if str:sub(1, 1) == sep or str:sub(-1) == sep then
        return false
    end
    
    -- Check no consecutive separators
    if str:find(sep .. sep, 1, true) then
        return false
    end
    
    return true
end

--[[
    Parse a slug into words
    
    @param slug string Slug to parse
    @param separator string Separator used (default: "-")
    @return table Array of words
]]
function slug_utils.parse_slug(slug, separator)
    if type(slug) ~= "string" then
        return {}
    end
    
    local sep = separator or "-"
    local words = {}
    
    for word in slug:gmatch("[^" .. sep .. "]+") do
        table.insert(words, word)
    end
    
    return words
end

--[[
    Generate a slug with a unique suffix (useful for avoiding collisions)
    
    @param str string Input string
    @param suffix string Suffix to append (default: random number)
    @param options table Optional slug options
    @return string URL-friendly slug with suffix
]]
function slug_utils.slug_unique(str, suffix, options)
    local base_slug = slug_utils.slug(str, options)
    
    if suffix then
        return base_slug .. "-" .. tostring(suffix)
    else
        -- Generate random suffix
        math.randomseed(os.time())
        local random_suffix = math.random(1000, 9999)
        return base_slug .. "-" .. tostring(random_suffix)
    end
end

--[[
    Truncate a slug to a maximum length (preserves word boundaries)
    
    @param slug string Slug to truncate
    @param max_length number Maximum length
    @param separator string Separator used (default: "-")
    @return string Truncated slug
]]
function slug_utils.truncate_slug(slug, max_length, separator)
    if type(slug) ~= "string" or #slug <= max_length then
        return slug
    end
    
    local sep = separator or "-"
    
    -- Find the last separator before max_length
    local truncated = slug:sub(1, max_length)
    local last_sep = truncated:find(sep .. "[^" .. sep .. "]*$")
    
    if last_sep then
        return truncated:sub(1, last_sep - 1)
    end
    
    return truncated
end

return slug_utils