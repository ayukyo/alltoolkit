--[[
rate_limiter_utils_test.lua - Test suite for rate_limiter_utils
Run with: lua rate_limiter_utils_test.lua
]]

local RateLimiterUtils = require("mod")

local tests_passed = 0
local tests_failed = 0

local function assert(condition, message)
    if not condition then
        print("FAIL: " .. (message or "assertion failed"))
        tests_failed = tests_failed + 1
        return false
    end
    return true
end

local function assert_equals(actual, expected, message)
    if actual ~= expected then
        print("FAIL: " .. (message or ("expected " .. tostring(expected) .. " but got " .. tostring(actual))))
        tests_failed = tests_failed + 1
        return false
    end
    return true
end

local function test(name, fn)
    print("Testing: " .. name)
    local success = pcall(fn)
    if success then
        tests_passed = tests_passed + 1
        print("  PASS")
    else
        tests_failed = tests_failed + 1
        print("  FAIL: " .. tostring(success))
    end
end

--------------------------------------------------------------------------------
-- Token Bucket Tests
--------------------------------------------------------------------------------

test("TokenBucket: create with default capacity", function()
    local tb = RateLimiterUtils.token_bucket(10, 100)
    assert(tb ~= nil, "TokenBucket should be created")
    assert(tb.capacity == 100, "Default capacity should be 100")
    assert(tb.rate == 10, "Rate should be 10")
end)

test("TokenBucket: acquire tokens when available", function()
    local tb = RateLimiterUtils.token_bucket(10, 100)
    local allowed, remaining, retry_after = tb:acquire(50)
    assert(allowed == true, "Should allow request")
    assert(remaining >= 49, "Should have remaining tokens")
    assert(retry_after == 0, "Should not need retry")
end)

test("TokenBucket: deny when tokens exhausted", function()
    local tb = RateLimiterUtils.token_bucket(1, 10)  -- 1 token per second, capacity 10
    tb:acquire(10)  -- Use all tokens
    
    local status = tb:status()
    assert(status.remaining < 1, "Should have no tokens left")
end)

test("TokenBucket: try_acquire non-blocking", function()
    local tb = RateLimiterUtils.token_bucket(10, 5)
    tb:acquire(5)  -- Exhaust all tokens
    
    local allowed = tb:try_acquire(1)
    assert(allowed == false, "try_acquire should return false when no tokens")
end)

test("TokenBucket: reset restores capacity", function()
    local tb = RateLimiterUtils.token_bucket(10, 100)
    tb:acquire(50)
    tb:reset()
    
    local status = tb:status()
    assert(status.remaining >= 99, "Reset should restore tokens")
end)

test("TokenBucket: status returns correct info", function()
    local tb = RateLimiterUtils.token_bucket(10, 100)
    tb:acquire(30)
    
    local status = tb:status()
    assert(status.capacity == 100, "Capacity should be 100")
    assert(status.refill_rate == 10, "Refill rate should be 10")
    assert(status.remaining < 71, "Should have less than 71 tokens remaining")
end)

--------------------------------------------------------------------------------
-- Sliding Window Tests
--------------------------------------------------------------------------------

test("SlidingWindow: create with parameters", function()
    local sw = RateLimiterUtils.sliding_window(100, 60)
    assert(sw ~= nil, "SlidingWindow should be created")
    assert(sw.max_requests == 100, "Max requests should be 100")
    assert(sw.window_size == 60, "Window size should be 60")
end)

test("SlidingWindow: allow requests within limit", function()
    local sw = RateLimiterUtils.sliding_window(10, 60)
    local allowed, remaining, retry_after = sw:acquire()
    assert(allowed == true, "Should allow first request")
    assert(remaining <= 9, "Should have remaining slots")
end)

test("SlidingWindow: deny when limit exceeded", function()
    local sw = RateLimiterUtils.sliding_window(3, 60)
    sw:acquire()
    sw:acquire()
    sw:acquire()
    
    local allowed = sw:try_acquire()
    assert(allowed == false, "Should deny when limit exceeded")
end)

test("SlidingWindow: reset clears history", function()
    local sw = RateLimiterUtils.sliding_window(5, 60)
    for i = 1, 5 do
        sw:acquire()
    end
    
    sw:reset()
    
    local allowed = sw:try_acquire()
    assert(allowed == true, "Reset should allow new requests")
end)

test("SlidingWindow: status returns correct info", function()
    local sw = RateLimiterUtils.sliding_window(10, 60)
    sw:acquire()
    sw:acquire()
    
    local status = sw:status()
    assert(status.window_size == 60, "Window size should be 60")
    assert(status.remaining <= 8, "Should have 8 or less remaining")
end)

--------------------------------------------------------------------------------
-- Fixed Window Tests
--------------------------------------------------------------------------------

test("FixedWindow: create with parameters", function()
    local fw = RateLimiterUtils.fixed_window(100, 60)
    assert(fw ~= nil, "FixedWindow should be created")
    assert(fw.max_requests == 100, "Max requests should be 100")
    assert(fw.window_size == 60, "Window size should be 60")
end)

test("FixedWindow: allow requests within limit", function()
    local fw = RateLimiterUtils.fixed_window(10, 60)
    local allowed, remaining, retry_after = fw:acquire()
    assert(allowed == true, "Should allow request")
    assert(remaining <= 9, "Should have remaining slots")
end)

test("FixedWindow: deny when limit exceeded", function()
    local fw = RateLimiterUtils.fixed_window(3, 60)
    fw:acquire()
    fw:acquire()
    fw:acquire()
    
    local allowed = fw:try_acquire()
    assert(allowed == false, "Should deny when limit exceeded")
end)

test("FixedWindow: reset restarts window", function()
    local fw = RateLimiterUtils.fixed_window(5, 60)
    for i = 1, 5 do
        fw:acquire()
    end
    
    fw:reset()
    
    local allowed = fw:try_acquire()
    assert(allowed == true, "Reset should allow new requests")
end)

test("FixedWindow: status returns correct info", function()
    local fw = RateLimiterUtils.fixed_window(10, 60)
    fw:acquire()
    
    local status = fw:status()
    assert(status.window_size == 60, "Window size should be 60")
end)

--------------------------------------------------------------------------------
-- Leaky Bucket Tests
--------------------------------------------------------------------------------

test("LeakyBucket: create with parameters", function()
    local lb = RateLimiterUtils.leaky_bucket(10, 100)
    assert(lb ~= nil, "LeakyBucket should be created")
    assert(lb.rate == 10, "Rate should be 10")
    assert(lb.capacity == 100, "Capacity should be 100")
end)

test("LeakyBucket: allow requests within capacity", function()
    local lb = RateLimiterUtils.leaky_bucket(10, 10)
    local allowed, remaining, retry_after = lb:acquire()
    assert(allowed == true, "Should allow request")
end)

test("LeakyBucket: deny when bucket is full", function()
    local lb = RateLimiterUtils.leaky_bucket(0.1, 2)  -- Very slow leak rate
    lb:acquire()
    lb:acquire()
    
    -- Wait a bit for some leakage
    -- Even with very slow leak, when full, subsequent requests should be denied
    local allowed = lb:try_acquire()
    -- After 2 requests in a 2-capacity bucket, try_acquire should return false
    assert(allowed == false, "Should deny when bucket is full")
end)

test("LeakyBucket: reset clears bucket", function()
    local lb = RateLimiterUtils.leaky_bucket(10, 10)
    lb:acquire()
    lb:acquire()
    lb:reset()
    
    local status = lb:status()
    assert(status.level == 0, "Reset should clear bucket level")
end)

test("LeakyBucket: status returns correct info", function()
    local lb = RateLimiterUtils.leaky_bucket(10, 100)
    lb:acquire()
    
    local status = lb:status()
    assert(status.capacity == 100, "Capacity should be 100")
    assert(status.rate == 10, "Rate should be 10")
end)

--------------------------------------------------------------------------------
-- MultiLimiter Tests
--------------------------------------------------------------------------------

test("MultiLimiter: create with limiters", function()
    local tb = RateLimiterUtils.token_bucket(10, 100)
    local sw = RateLimiterUtils.sliding_window(50, 60)
    
    local ml = RateLimiterUtils.multi_limiter({
        api = tb,
        user = sw
    })
    
    assert(ml ~= nil, "MultiLimiter should be created")
end)

test("MultiLimiter: allow when all limiters allow", function()
    local ml = RateLimiterUtils.multi_limiter({
        api = RateLimiterUtils.token_bucket(100, 1000),
        ip = RateLimiterUtils.sliding_window(100, 60)
    })
    
    local allowed = ml:acquire()
    assert(allowed == true, "Should allow when all limiters allow")
end)

test("MultiLimiter: deny when any limiter denies", function()
    local ml = RateLimiterUtils.multi_limiter({
        api = RateLimiterUtils.token_bucket(100, 1000),
        ip = RateLimiterUtils.sliding_window(1, 60)  -- Only 1 request per minute
    })
    
    ml:acquire()  -- First request succeeds
    local allowed = ml:acquire()  -- Second request - ip limiter should deny
    assert(allowed == false, "Should deny when any limiter denies")
end)

test("MultiLimiter: add_limiter dynamically", function()
    local ml = RateLimiterUtils.multi_limiter()
    ml:add_limiter("api", RateLimiterUtils.token_bucket(10, 100))
    
    local allowed = ml:acquire()
    assert(allowed == true, "Should work with dynamically added limiter")
end)

test("MultiLimiter: remove_limiter", function()
    local ml = RateLimiterUtils.multi_limiter({
        api = RateLimiterUtils.token_bucket(10, 100)
    })
    
    ml:remove_limiter("api")
    
    local allowed = ml:acquire()
    assert(allowed == true, "Should allow when no limiters")
end)

test("MultiLimiter: reset clears all limiters", function()
    local ml = RateLimiterUtils.multi_limiter({
        api = RateLimiterUtils.token_bucket(10, 100),
        ip = RateLimiterUtils.sliding_window(10, 60)
    })
    
    for i = 1, 10 do
        ml:acquire()  -- Exhaust token bucket
    end
    
    ml:reset()
    
    local allowed = ml:acquire()
    assert(allowed == true, "Reset should allow new requests")
end)

--------------------------------------------------------------------------------
-- Utility Function Tests
--------------------------------------------------------------------------------

test("decorate: wraps function with rate limiting", function()
    local tb = RateLimiterUtils.token_bucket(100, 10)
    local call_count = 0
    
    local function my_function()
        call_count = call_count + 1
        return "success"
    end
    
    local wrapped = RateLimiterUtils.decorate(tb, my_function)
    local result = wrapped()
    
    assert(result == "success", "Function should return correct result")
    assert(call_count == 1, "Function should be called")
end)

test("decorate: returns nil on rate limit", function()
    local tb = RateLimiterUtils.token_bucket(1, 2)  -- Very limited
    tb:acquire(2)  -- Exhaust tokens
    
    local wrapped = RateLimiterUtils.decorate(tb, function() return "success" end)
    local result = wrapped()
    
    assert(result == nil, "Should return nil on rate limit")
end)

test("middleware: returns proper response tuple", function()
    local tb = RateLimiterUtils.token_bucket(100, 10)
    
    local success, result, retry_after = RateLimiterUtils.middleware(tb, function()
        return "hello"
    end)()
    
    assert(success == true, "Success should be true")
    assert(result == "hello", "Result should be hello")
    assert(retry_after == 0, "Retry after should be 0")
end)

test("get_http_headers: returns proper headers", function()
    local tb = RateLimiterUtils.token_bucket(100, 1000)
    
    local headers = RateLimiterUtils.get_http_headers(tb)
    
    assert(headers["X-RateLimit-Limit"] ~= nil, "Should have X-RateLimit-Limit header")
    assert(headers["X-RateLimit-Remaining"] ~= nil, "Should have X-RateLimit-Remaining header")
    assert(headers["X-RateLimit-Retry-After"] ~= nil, "Should have X-RateLimit-Retry-After header")
end)

--------------------------------------------------------------------------------
-- Edge Cases
--------------------------------------------------------------------------------

test("TokenBucket: handle zero rate", function()
    local tb = RateLimiterUtils.token_bucket(0, 2)  -- 2 capacity, zero refill rate
    local allowed1 = tb:try_acquire(1)
    local allowed2 = tb:try_acquire(1)
    local allowed3 = tb:try_acquire(1)
    assert(allowed1 == true, "Should allow first request")
    assert(allowed2 == true, "Should allow second request (capacity is 2)")
    assert(allowed3 == false, "Should deny third request (capacity exhausted)")
end)

test("SlidingWindow: handle empty requests", function()
    local sw = RateLimiterUtils.sliding_window(10, 60)
    
    local status = sw:status()
    assert(status.remaining == 10, "Should show full remaining")
end)

test("MultiLimiter: empty limiter list", function()
    local ml = RateLimiterUtils.multi_limiter()
    
    local allowed, results, failed = ml:acquire()
    assert(allowed == true, "Should allow with no limiters")
    assert(#failed == 0, "Should have no failed limiters")
end)

test("TokenBucket: fractional token consumption", function()
    local tb = RateLimiterUtils.token_bucket(10, 100)
    local allowed1 = tb:try_acquire(0.5)
    local allowed2 = tb:try_acquire(0.5)
    
    -- Should allow both 0.5 token requests
    assert(allowed1 == true, "Should allow first 0.5 token request")
    assert(allowed2 == true, "Should allow second 0.5 token request")
end)

--------------------------------------------------------------------------------
-- Summary
--------------------------------------------------------------------------------

print("")
print("========================================")
print("Test Results:")
print("  Passed: " .. tests_passed)
print("  Failed: " .. tests_failed)
print("========================================")

if tests_failed > 0 then
    os.exit(1)
end