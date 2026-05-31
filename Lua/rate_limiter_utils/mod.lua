--[[
rate_limiter_utils.lua - A comprehensive rate limiting utility library for Lua
Provides multiple rate limiting algorithms for API control, crawler throttling, traffic shaping, etc.

Algorithms included:
- TokenBucket: Token bucket algorithm (allows burst traffic)
- SlidingWindow: Sliding window algorithm (precise control)
- FixedWindow: Fixed window algorithm (simple and efficient)
- LeakyBucket: Leaky bucket algorithm (smooth traffic)

Zero external dependencies - uses only Lua standard library
]]

local RateLimiterUtils = {}
RateLimiterUtils.__index = RateLimiterUtils

-- Constants
local SECONDS_IN_MINUTE = 60
local SECONDS_IN_HOUR = 3600
local SECONDS_IN_DAY = 86400

--------------------------------------------------------------------------------
-- Token Bucket Rate Limiter
--------------------------------------------------------------------------------

local TokenBucket = {}
TokenBucket.__index = TokenBucket

--- Create a new TokenBucket rate limiter
-- @param rate_tokens Number of tokens added per second ( refill rate )
-- @param capacity Maximum number of tokens in the bucket
-- @return TokenBucket instance
function RateLimiterUtils.token_bucket(rate_tokens, capacity)
    local self = setmetatable({}, TokenBucket)
    self.rate = rate_tokens
    self.capacity = capacity
    self.tokens = capacity
    self.last_update = os.time()
    self.locked = false
    return self
end

--- Consume tokens from the bucket
-- @param self TokenBucket instance
-- @param tokens Number of tokens to consume
-- @return boolean, number, number true if allowed, remaining tokens, retry_after seconds
function TokenBucket:acquire(tokens)
    tokens = tokens or 1
    local now = os.time()
    local elapsed = now - self.last_update
    self.last_update = now
    
    -- Refill tokens based on elapsed time
    self.tokens = math.min(self.capacity, self.tokens + elapsed * self.rate)
    
    if self.tokens >= tokens then
        self.tokens = self.tokens - tokens
        return true, self.capacity - self.tokens, 0
    else
        local retry_after = (tokens - self.tokens) / self.rate
        return false, 0, retry_after
    end
end

--- Try to acquire tokens without blocking
-- @param self TokenBucket instance
-- @param tokens Number of tokens to consume
-- @return boolean, number, number true if allowed, remaining tokens, retry_after seconds
function TokenBucket:try_acquire(tokens)
    tokens = tokens or 1
    
    if self.tokens >= tokens then
        self.tokens = self.tokens - tokens
        return true, self.capacity - self.tokens, 0
    else
        return false, 0, 0
    end
end

--- Get current status
-- @param self TokenBucket instance
-- @return table status information
function TokenBucket:status()
    local now = os.time()
    local elapsed = now - self.last_update
    local current_tokens = math.min(self.capacity, self.tokens + elapsed * self.rate)
    
    return {
        allowed = current_tokens >= 1,
        remaining = current_tokens,
        capacity = self.capacity,
        refill_rate = self.rate,
        retry_after = current_tokens < 1 and (1 - current_tokens) / self.rate or 0
    }
end

--- Reset the bucket
-- @param self TokenBucket instance
function TokenBucket:reset()
    self.tokens = self.capacity
    self.last_update = os.time()
end

--------------------------------------------------------------------------------
-- Sliding Window Rate Limiter
--------------------------------------------------------------------------------

local SlidingWindow = {}
SlidingWindow.__index = SlidingWindow

--- Create a new SlidingWindow rate limiter
-- @param max_requests Maximum requests allowed in the window
-- @param window_size_seconds Size of the sliding window in seconds
-- @return SlidingWindow instance
function RateLimiterUtils.sliding_window(max_requests, window_size_seconds)
    local self = setmetatable({}, SlidingWindow)
    self.max_requests = max_requests
    self.window_size = window_size_seconds
    self.requests = {}
    self.locked = false
    return self
end

--- Record a request and check if allowed
-- @param self SlidingWindow instance
-- @return boolean, number, number true if allowed, remaining requests, retry_after seconds
function SlidingWindow:acquire()
    local now = os.time()
    local window_start = now - self.window_size
    
    -- Remove expired requests
    local valid_requests = {}
    for _, req_time in ipairs(self.requests) do
        if req_time > window_start then
            table.insert(valid_requests, req_time)
        end
    end
    self.requests = valid_requests
    
    if #self.requests < self.max_requests then
        table.insert(self.requests, now)
        return true, self.max_requests - #self.requests, 0
    else
        local oldest = self.requests[1]
        local retry_after = oldest + self.window_size - now
        return false, 0, retry_after
    end
end

--- Try to acquire without blocking
-- @param self SlidingWindow instance
-- @return boolean, number, number true if allowed, remaining requests, retry_after seconds
function SlidingWindow:try_acquire()
    local now = os.time()
    local window_start = now - self.window_size
    
    local valid_count = 0
    for _, req_time in ipairs(self.requests) do
        if req_time > window_start then
            valid_count = valid_count + 1
        end
    end
    
    if valid_count < self.max_requests then
        return true, self.max_requests - valid_count, 0
    else
        return false, 0, 0
    end
end

--- Get current status
-- @param self SlidingWindow instance
-- @return table status information
function SlidingWindow:status()
    local now = os.time()
    local window_start = now - self.window_size
    
    local valid_count = 0
    for _, req_time in ipairs(self.requests) do
        if req_time > window_start then
            valid_count = valid_count + 1
        end
    end
    
    return {
        allowed = valid_count < self.max_requests,
        remaining = self.max_requests - valid_count,
        window_size = self.window_size,
        retry_after = valid_count >= self.max_requests and self.requests[1] + self.window_size - now or 0
    }
end

--- Reset the limiter
-- @param self SlidingWindow instance
function SlidingWindow:reset()
    self.requests = {}
end

--------------------------------------------------------------------------------
-- Fixed Window Rate Limiter
--------------------------------------------------------------------------------

local FixedWindow = {}
FixedWindow.__index = FixedWindow

--- Create a new FixedWindow rate limiter
-- @param max_requests Maximum requests allowed in the window
-- @param window_size_seconds Size of the window in seconds
-- @return FixedWindow instance
function RateLimiterUtils.fixed_window(max_requests, window_size_seconds)
    local self = setmetatable({}, FixedWindow)
    self.max_requests = max_requests
    self.window_size = window_size_seconds
    self.window_start = os.time()
    self.count = 0
    self.locked = false
    return self
end

--- Record a request and check if allowed
-- @param self FixedWindow instance
-- @return boolean, number, number true if allowed, remaining requests, retry_after seconds
function FixedWindow:acquire()
    local now = os.time()
    
    -- Check if we need to start a new window
    if now - self.window_start >= self.window_size then
        self.window_start = now
        self.count = 0
    end
    
    if self.count < self.max_requests then
        self.count = self.count + 1
        return true, self.max_requests - self.count, 0
    else
        local retry_after = self.window_start + self.window_size - now
        return false, 0, retry_after
    end
end

--- Try to acquire without blocking
-- @param self FixedWindow instance
-- @return boolean, number, number true if allowed, remaining requests, retry_after seconds
function FixedWindow:try_acquire()
    local now = os.time()
    
    if now - self.window_start >= self.window_size then
        return true, self.max_requests, 0
    end
    
    if self.count < self.max_requests then
        return true, self.max_requests - self.count, 0
    else
        return false, 0, 0
    end
end

--- Get current status
-- @param self FixedWindow instance
-- @return table status information
function FixedWindow:status()
    local now = os.time()
    local in_window = now - self.window_start < self.window_size
    local current_count = in_window and self.count or 0
    
    return {
        allowed = current_count < self.max_requests,
        remaining = self.max_requests - current_count,
        window_size = self.window_size,
        retry_after = in_window and current_count >= self.max_requests and self.window_start + self.window_size - now or 0
    }
end

--- Reset the limiter
-- @param self FixedWindow instance
function FixedWindow:reset()
    self.window_start = os.time()
    self.count = 0
end

--------------------------------------------------------------------------------
-- Leaky Bucket Rate Limiter
--------------------------------------------------------------------------------

local LeakyBucket = {}
LeakyBucket.__index = LeakyBucket

--- Create a new LeakyBucket rate limiter
-- @param rate Leaky rate (requests per second)
-- @param capacity Maximum bucket capacity
-- @return LeakyBucket instance
function RateLimiterUtils.leaky_bucket(rate, capacity)
    local self = setmetatable({}, LeakyBucket)
    self.rate = rate
    self.capacity = capacity
    self.level = 0
    self.last_update = os.time()
    self.locked = false
    return self
end

--- Process a request through the bucket
-- @param self LeakyBucket instance
-- @return boolean, number, number true if allowed, remaining capacity, retry_after seconds
function LeakyBucket:acquire()
    local now = os.time()
    local elapsed = now - self.last_update
    self.last_update = now
    
    -- Leak tokens
    self.level = math.max(0, self.level - elapsed * self.rate)
    
    if self.level < self.capacity then
        self.level = self.level + 1
        return true, self.capacity - self.level, 0
    else
        local retry_after = (self.level + 1 - self.capacity) / self.rate
        return false, 0, retry_after
    end
end

--- Try to acquire without blocking
-- @param self LeakyBucket instance
-- @return boolean, number, number true if allowed, remaining capacity, retry_after seconds
function LeakyBucket:try_acquire()
    if self.level < self.capacity then
        return true, self.capacity - self.level, 0
    else
        return false, 0, 0
    end
end

--- Get current status
-- @param self LeakyBucket instance
-- @return table status information
function LeakyBucket:status()
    local now = os.time()
    local elapsed = now - self.last_update
    local current_level = math.max(0, self.level - elapsed * self.rate)
    
    return {
        allowed = current_level < self.capacity,
        remaining = self.capacity - current_level,
        capacity = self.capacity,
        level = current_level,
        rate = self.rate,
        retry_after = current_level >= self.capacity and 1 / self.rate or 0
    }
end

--- Reset the bucket
-- @param self LeakyBucket instance
function LeakyBucket:reset()
    self.level = 0
    self.last_update = os.time()
end

--------------------------------------------------------------------------------
-- MultiLimiter - Multi-dimensional Rate Limiter
--------------------------------------------------------------------------------

local MultiLimiter = {}
MultiLimiter.__index = MultiLimiter

--- Create a new MultiLimiter
-- @param limits Table of limiters { name = limiter }
-- @return MultiLimiter instance
function RateLimiterUtils.multi_limiter(limits)
    local self = setmetatable({}, MultiLimiter)
    self.limiters = limits or {}
    self.locked = false
    return self
end

--- Add a limiter
-- @param self MultiLimiter instance
-- @param name Limiter name
-- @param limiter Limiter instance
function MultiLimiter:add_limiter(name, limiter)
    self.limiters[name] = limiter
end

--- Remove a limiter
-- @param self MultiLimiter instance
-- @param name Limiter name
function MultiLimiter:remove_limiter(name)
    self.limiters[name] = nil
end

--- Check all limiters
-- @param self MultiLimiter instance
-- @return boolean, table, table true if all allowed, results per limiter, failed limiter names
function MultiLimiter:acquire()
    local results = {}
    local failed = {}
    
    for name, limiter in pairs(self.limiters) do
        local allowed, remaining, retry_after = limiter:acquire()
        results[name] = {
            allowed = allowed,
            remaining = remaining,
            retry_after = retry_after
        }
        
        if not allowed then
            table.insert(failed, name)
        end
    end
    
    local all_allowed = #failed == 0
    return all_allowed, results, failed
end

--- Try to acquire without blocking
-- @param self MultiLimiter instance
-- @return boolean, table, table true if all allowed, results per limiter, failed limiter names
function MultiLimiter:try_acquire()
    local results = {}
    local failed = {}
    
    for name, limiter in pairs(self.limiters) do
        local allowed, remaining, retry_after = limiter:try_acquire()
        results[name] = {
            allowed = allowed,
            remaining = remaining,
            retry_after = retry_after
        }
        
        if not allowed then
            table.insert(failed, name)
        end
    end
    
    local all_allowed = #failed == 0
    return all_allowed, results, failed
end

--- Get status of all limiters
-- @param self MultiLimiter instance
-- @return table status of all limiters
function MultiLimiter:status()
    local status = {}
    for name, limiter in pairs(self.limiters) do
        if limiter.status then
            status[name] = limiter:status()
        end
    end
    return status
end

--- Reset all limiters
-- @param self MultiLimiter instance
function MultiLimiter:reset()
    for _, limiter in pairs(self.limiters) do
        if limiter.reset then
            limiter:reset()
        end
    end
end

--------------------------------------------------------------------------------
-- Utility Functions
--------------------------------------------------------------------------------

--- Create a decorator-style wrapper for a function
-- @param limiter Rate limiter instance
-- @param fn Function to wrap
-- @return function Wrapped function
function RateLimiterUtils.decorate(limiter, fn)
    return function(...)
        local allowed, remaining, retry_after = limiter:acquire()
        if allowed then
            return fn(...)
        else
            return nil, "Rate limit exceeded. Retry after " .. retry_after .. " seconds"
        end
    end
end

--- Create a middleware-style wrapper for Lua functions
-- @param limiter Rate limiter instance
-- @param fn Function to wrap
-- @return function Wrapped function that returns success, result, retry_after
function RateLimiterUtils.middleware(limiter, fn)
    return function(...)
        local allowed, remaining, retry_after = limiter:acquire()
        if allowed then
            local success, result = pcall(fn, ...)
            return success, result, 0
        else
            return false, nil, retry_after
        end
    end
end

--- Get rate limit info for HTTP headers
-- @param limiter Rate limiter instance
-- @return table Headers with limit information
function RateLimiterUtils.get_http_headers(limiter)
    local status = limiter:status()
    return {
        ["X-RateLimit-Limit"] = tostring(status.capacity or status.max_requests or 0),
        ["X-RateLimit-Remaining"] = tostring(status.remaining or 0),
        ["X-RateLimit-Retry-After"] = tostring(math.ceil(status.retry_after or 0))
    }
end

return RateLimiterUtils