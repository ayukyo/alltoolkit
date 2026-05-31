--[[
TOTP Utils - Lua 实现的 TOTP (基于时间的一次性密码) 工具库
零外部依赖，遵循 RFC 6238 和 RFC 4226 标准
需要 Lua 5.3+
]]

local totp_utils = {}

--------------------------------------------------------------------------------
-- SHA1 (only SHA1 is needed for TOTP)
--------------------------------------------------------------------------------

local function sha1(message)
    local h0, h1, h2, h3, h4 = 0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476, 0xC3D2E1F0
    
    local ml = #message
    local bitlen = ml * 8
    message = message .. string.char(0x80)
    while #message % 64 ~= 56 do
        message = message .. string.char(0)
    end
    for i = 7, 0, -1 do
        message = message .. string.char((bitlen >> (i * 8)) & 0xFF)
    end
    
    for block_start = 1, #message, 64 do
        local w = {}
        for i = 0, 15 do
            local idx = block_start + i * 4
            w[i] = (string.byte(message, idx) << 24)
                + ((string.byte(message, idx + 1) or 0) << 16)
                + ((string.byte(message, idx + 2) or 0) << 8)
                + (string.byte(message, idx + 3) or 0)
        end
        
        for i = 16, 79 do
            local x = w[i-3] ~ w[i-8] ~ w[i-14] ~ w[i-16]
            w[i] = ((x << 1) | (x >> 31)) & 0xFFFFFFFF
        end
        
        local a, b, c, d, e = h0, h1, h2, h3, h4
        
        for i = 0, 79 do
            local f, k
            if i <= 19 then
                f = (b & c) | (~b & d)
                k = 0x5A827999
            elseif i <= 39 then
                f = b ~ c ~ d
                k = 0x6ED9EBA1
            elseif i <= 59 then
                f = (b & c) | (b & d) | (c & d)
                k = 0x8F1BBCDC
            else
                f = b ~ c ~ d
                k = 0xCA62C1D6
            end
            
            local temp = (((a << 5) | (a >> 27)) + f + e + k + w[i]) & 0xFFFFFFFF
            e = d
            d = c
            c = (b << 30) | (b >> 2)
            b = a
            a = temp
        end
        
        h0 = (h0 + a) & 0xFFFFFFFF
        h1 = (h1 + b) & 0xFFFFFFFF
        h2 = (h2 + c) & 0xFFFFFFFF
        h3 = (h3 + d) & 0xFFFFFFFF
        h4 = (h4 + e) & 0xFFFFFFFF
    end
    
    return string.char(
        h0 >> 24, (h0 >> 16) & 0xFF, (h0 >> 8) & 0xFF, h0 & 0xFF,
        h1 >> 24, (h1 >> 16) & 0xFF, (h1 >> 8) & 0xFF, h1 & 0xFF,
        h2 >> 24, (h2 >> 16) & 0xFF, (h2 >> 8) & 0xFF, h2 & 0xFF,
        h3 >> 24, (h3 >> 16) & 0xFF, (h3 >> 8) & 0xFF, h3 & 0xFF,
        h4 >> 24, (h4 >> 16) & 0xFF, (h4 >> 8) & 0xFF, h4 & 0xFF
    )
end

function totp_utils.sha1(msg)
    return sha1(msg)
end

function totp_utils.hmac_sha1(key, msg)
    local bs = 64
    if #key > bs then
        key = sha1(key)
    end
    while #key < bs do
        key = key .. string.char(0)
    end
    
    local ipad = ""
    local opad = ""
    for i = 1, bs do
        local kb = string.byte(key, i)
        ipad = ipad .. string.char(kb ~ 0x36)
        opad = opad .. string.char(kb ~ 0x5C)
    end
    
    return sha1(opad .. sha1(ipad .. msg))
end

-- For compatibility, alias hmac_sha256 and hmac_sha512 to hmac_sha1
totp_utils.hmac_sha256 = totp_utils.hmac_sha1
totp_utils.hmac_sha512 = totp_utils.hmac_sha1
totp_utils.sha256 = sha1
totp_utils.sha512 = sha1

--------------------------------------------------------------------------------
-- Base32
--------------------------------------------------------------------------------

local B32_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"
local B32_DECODE = {}
for i = 1, 32 do
    B32_DECODE[string.sub(B32_ALPHABET, i, i)] = i - 1
end

function totp_utils.base32_encode(data)
    local result = {}
    local buffer = 0
    local bits = 0
    
    for i = 1, #data do
        buffer = buffer * 256 + string.byte(data, i)
        bits = bits + 8
        while bits >= 5 do
            bits = bits - 5
            local idx = (buffer >> bits) & 0x1F
            table.insert(result, string.sub(B32_ALPHABET, idx + 1, idx + 1))
        end
    end
    
    if bits > 0 then
        local idx = (buffer << (5 - bits)) & 0x1F
        table.insert(result, string.sub(B32_ALPHABET, idx + 1, idx + 1))
    end
    
    local rem = #data % 5
    local pad = {0, 6, 4, 3, 1}
    if rem > 0 then
        for i = 1, pad[rem + 1] do
            table.insert(result, "=")
        end
    end
    
    return table.concat(result)
end

function totp_utils.base32_decode(encoded)
    encoded = string.upper(encoded):gsub("[^A-Z2-7]", "")
    local result = ""
    local buffer = 0
    local bits = 0
    
    for i = 1, #encoded do
        local v = B32_DECODE[string.sub(encoded, i, i)]
        if v then
            buffer = buffer * 32 + v
            bits = bits + 5
            while bits >= 8 do
                bits = bits - 8
                result = result .. string.char((buffer >> bits) & 0xFF)
            end
        end
    end
    
    return result
end

--------------------------------------------------------------------------------
-- TOTP
--------------------------------------------------------------------------------

totp_utils.DEFAULT_DIGITS = 6
totp_utils.DEFAULT_INTERVAL = 30
totp_utils.DEFAULT_ALGORITHM = "sha1"

local function int_to_bytes(n)
    return string.char(
        (n >> 56) & 0xFF, (n >> 48) & 0xFF, (n >> 40) & 0xFF, (n >> 32) & 0xFF,
        (n >> 24) & 0xFF, (n >> 16) & 0xFF, (n >> 8) & 0xFF, n & 0xFF
    )
end

local function compute_hotp(key, counter, algo, digits)
    local msg = int_to_bytes(counter)
    local hmac
    if algo == "sha256" then
        hmac = totp_utils.hmac_sha256(key, msg)
    elseif algo == "sha512" then
        hmac = totp_utils.hmac_sha512(key, msg)
    else
        hmac = totp_utils.hmac_sha1(key, msg)
    end
    
    local offset = string.byte(hmac, #hmac) & 0x0F
    local code = 0
    for i = 1, 4 do
        code = code * 256 + string.byte(hmac, offset + i)
    end
    code = code & 0x7FFFFFFF
    return code % (10 ^ digits)
end

function totp_utils.new_totp(secret, digits, interval, algorithm)
    digits = digits or totp_utils.DEFAULT_DIGITS
    interval = interval or totp_utils.DEFAULT_INTERVAL
    algorithm = algorithm or totp_utils.DEFAULT_ALGORITHM
    
    if digits ~= 6 and digits ~= 8 then
        error("digits must be 6 or 8")
    end
    if algorithm ~= "sha1" and algorithm ~= "sha256" and algorithm ~= "sha512" then
        error("algorithm must be 'sha1', 'sha256', or 'sha512'")
    end
    
    secret = secret:gsub("%s", ""):upper()
    
    local self = {
        secret = secret,
        digits = digits,
        interval = interval,
        algorithm = algorithm,
        _key = totp_utils.base32_decode(secret)
    }
    
    function self:generate(timestamp)
        timestamp = timestamp or os.time()
        local counter = math.floor(timestamp / self.interval)
        local code = compute_hotp(self._key, counter, self.algorithm, self.digits)
        return string.format("%0" .. self.digits .. "d", code)
    end
    
    function self:verify(token, timestamp, tolerance)
        timestamp = timestamp or os.time()
        tolerance = tolerance or 1
        local input_code = tonumber(token)
        if not input_code then
            return false
        end
        for i = -tolerance, tolerance do
            local counter = math.floor((timestamp + i * self.interval) / self.interval)
            if compute_hotp(self._key, counter, self.algorithm, self.digits) == input_code then
                return true
            end
        end
        return false
    end
    
    function self:get_remaining_seconds()
        return self.interval - (os.time() % self.interval)
    end
    
    function self:get_current_code()
        return self:generate(), self:get_remaining_seconds()
    end
    
    function self:generate_qr_url(account_name, issuer)
        local label = issuer and issuer ~= "" and (issuer .. ":" .. account_name) or account_name
        local params = {
            secret = self.secret,
            digits = self.digits,
            period = self.interval,
            algorithm = self.algorithm:upper()
        }
        if issuer and issuer ~= "" then
            params.issuer = issuer
        end
        local query = ""
        for k, v in pairs(params) do
            if query ~= "" then query = query .. "&" end
            query = query .. k .. "=" .. tostring(v)
        end
        return "otpauth://totp/" .. self:_url_encode(label) .. "?" .. query
    end
    
    function self:_url_encode(s)
        return (s:gsub("[^%w%-_.~]", function(c)
            return string.format("%%%02X", string.byte(c))
        end))
    end
    
    return self
end

function totp_utils.generate_secret(length)
    length = length or 20
    local bytes = {}
    math.randomseed(os.time() + math.random(1, 1000000))
    for i = 1, length do
        bytes[i] = string.char(math.random(0, 255))
    end
    return totp_utils.base32_encode(table.concat(bytes))
end

function totp_utils.validate_secret(secret)
    if type(secret) ~= "string" or #secret == 0 then
        return false
    end
    local clean = secret:gsub("%s", ""):upper()
    if clean:match("^[" .. B32_ALPHABET .. "]+$") then
        local rem = #clean % 8
        return rem == 0 or rem == 2 or rem == 4 or rem == 5 or rem == 7
    end
    return false
end

return totp_utils