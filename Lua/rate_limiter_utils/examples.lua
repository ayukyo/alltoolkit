--[[
rate_limiter_utils_examples.lua - Usage examples for rate_limiter_utils
]]

local RateLimiterUtils = require("mod")

print("========================================")
print("Rate Limiter Utils - Usage Examples")
print("========================================")
print("")

--------------------------------------------------------------------------------
-- 1. Token Bucket Example - API Rate Limiting
--------------------------------------------------------------------------------

print("--- Example 1: Token Bucket for API Rate Limiting ---")
print("")

-- Create a token bucket: 100 requests per second, burst capacity of 500
local api_limiter = RateLimiterUtils.token_bucket(100, 500)

-- Simulate API calls
local function simulate_api_call()
    local allowed, remaining, retry_after = api_limiter:acquire()
    if allowed then
        print(string.format("  [OK] Request allowed. Remaining tokens: %.0f", remaining))
    else
        print(string.format("  [RATE LIMITED] Retry after %.2f seconds", retry_after))
    end
end

-- Simulate 10 rapid requests
for i = 1, 10 do
    io.write(string.format("Request %d: ", i))
    simulate_api_call()
end

print("")

-- Check status
local status = api_limiter:status()
print(string.format("Current Status - Capacity: %d, Remaining: %.0f, Refill rate: %d/s",
    status.capacity, status.remaining, status.refill_rate))
print("")

--------------------------------------------------------------------------------
-- 2. Sliding Window Example - User Request Tracking
--------------------------------------------------------------------------------

print("--- Example 2: Sliding Window for User Request Tracking ---")
print("")

-- Create a sliding window: 10 requests per minute
local user_limiter = RateLimiterUtils.sliding_window(10, 60)

local function simulate_user_request(username)
    local allowed, remaining, retry_after = user_limiter:acquire()
    if allowed then
        print(string.format("  [OK] User '%s' request allowed. Remaining: %d", username, remaining))
    else
        print(string.format("  [RATE LIMITED] User '%s' must wait %.0f seconds", username, retry_after))
    end
end

-- Simulate user making requests
simulate_user_request("alice")
simulate_user_request("alice")
simulate_user_request("alice")
simulate_user_request("bob")

print("")

--------------------------------------------------------------------------------
-- 3. Fixed Window Example - Daily Limit
--------------------------------------------------------------------------------

print("--- Example 3: Fixed Window for Daily Limits ---")
print("")

-- Create a fixed window: 100 requests per hour
local daily_limiter = RateLimiterUtils.fixed_window(100, 3600)

for i = 1, 5 do
    local allowed, remaining = daily_limiter:acquire()
    print(string.format("  Request %d: allowed=%s, remaining=%d", i, tostring(allowed), remaining))
end

print("")

--------------------------------------------------------------------------------
-- 4. Leaky Bucket Example - Traffic Shaping
--------------------------------------------------------------------------------

print("--- Example 4: Leaky Bucket for Traffic Shaping ---")
print("")

-- Create a leaky bucket: processes 5 requests per second, capacity of 20
local traffic_limiter = RateLimiterUtils.leaky_bucket(5, 20)

for i = 1, 5 do
    local allowed, remaining = traffic_limiter:acquire()
    print(string.format("  Request %d: allowed=%s, remaining capacity: %d", i, tostring(allowed), remaining))
end

print("")

--------------------------------------------------------------------------------
-- 5. Multi-Limiter Example - Multiple Dimensions
--------------------------------------------------------------------------------

print("--- Example 5: Multi-Limiter for Multiple Rate Limit Dimensions ---")
print("")

-- Create limiters for different dimensions
local per_ip_limiter = RateLimiterUtils.sliding_window(100, 60)       -- 100 per minute per IP
local per_user_limiter = RateLimiterUtils.token_bucket(10, 50)         -- 10 per second per user
local per_api_limiter = RateLimiterUtils.fixed_window(1000, 3600)       -- 1000 per hour globally

-- Combine into multi-limiter
local multi_limiter = RateLimiterUtils.multi_limiter({
    ip = per_ip_limiter,
    user = per_user_limiter,
    api = per_api_limiter
})

local function check_request(ip, user)
    local allowed, results, failed = multi_limiter:acquire()
    if allowed then
        print(string.format("  [OK] Request from IP=%s, User=%s allowed", ip, user))
    else
        print(string.format("  [DENIED] Request blocked by limiters: %s", table.concat(failed, ", ")))
    end
end

check_request("192.168.1.1", "alice")
check_request("192.168.1.1", "alice")
check_request("192.168.1.1", "alice")

-- Add a new limiter dynamically
print("")
print("Adding new 'endpoint' limiter dynamically...")
multi_limiter:add_limiter("endpoint", RateLimiterUtils.token_bucket(100, 200))

check_request("192.168.1.1", "alice")

print("")

--------------------------------------------------------------------------------
-- 6. Decorator Pattern - Wrap Functions with Rate Limiting
--------------------------------------------------------------------------------

print("--- Example 6: Decorator Pattern ---")
print("")

local call_counter = 0
local limiter = RateLimiterUtils.token_bucket(5, 10)  -- 5 per second, burst 10

local function expensive_api_call(data)
    call_counter = call_counter + 1
    return string.format("Processed request #%d with data: %s", call_counter, data)
end

-- Wrap with rate limiter
local rate_limited_api = RateLimiterUtils.decorate(limiter, expensive_api_call)

-- Simulate multiple calls
for i = 1, 12 do
    local result = rate_limited_api("payload_" .. i)
    if result then
        print(string.format("  [OK] %s", result))
    else
        print(string.format("  [RATE LIMITED] Request %d blocked", i))
    end
end

print("")

--------------------------------------------------------------------------------
-- 7. HTTP Headers Generation
--------------------------------------------------------------------------------

print("--- Example 7: Generate HTTP Rate Limit Headers ---")
print("")

local http_limiter = RateLimiterUtils.token_bucket(1000, 10000)

-- Make a request
http_limiter:acquire()
http_limiter:acquire()
http_limiter:acquire()

-- Get headers for response
local headers = RateLimiterUtils.get_http_headers(http_limiter)

print("HTTP Rate Limit Headers:")
for header, value in pairs(headers) do
    print(string.format("  %s: %s", header, value))
end

print("")

--------------------------------------------------------------------------------
-- 8. Middleware Pattern
--------------------------------------------------------------------------------

print("--- Example 8: Middleware Pattern ---")
print("")

local mw_limiter = RateLimiterUtils.token_bucket(2, 5)

local function process_request(request_id)
    if request_id == 7 then
        error("Simulated error on request 7")
    end
    return string.format("Result for request #%d", request_id)
end

local wrapped = RateLimiterUtils.middleware(mw_limiter, process_request)

for i = 1, 8 do
    local success, result, retry_after = wrapped(i)
    if success then
        print(string.format("  [OK] %s", result))
    elseif result == nil then
        print(string.format("  [RATE LIMITED] Request %d must retry after %.1f seconds", i, retry_after))
    else
        print(string.format("  [ERROR] Request %d failed: %s", i, tostring(result)))
    end
end

print("")

--------------------------------------------------------------------------------
-- 9. Reset and Recovery
--------------------------------------------------------------------------------

print("--- Example 9: Reset and Recovery ---")
print("")

local reset_limiter = RateLimiterUtils.sliding_window(3, 60)

-- Exhaust the limiter
for i = 1, 3 do
    reset_limiter:acquire()
end

local allowed = reset_limiter:try_acquire()
print(string.format("After exhausting (before reset): allowed=%s", tostring(allowed)))

-- Reset
reset_limiter:reset()

allowed = reset_limiter:try_acquire()
print(string.format("After reset: allowed=%s", tostring(allowed)))

print("")

--------------------------------------------------------------------------------
-- 10. Comparing Algorithms
--------------------------------------------------------------------------------

print("--- Example 10: Algorithm Comparison ---")
print("")

print("Simulating burst of 15 requests with different algorithms:")
print("(All configured for ~10 requests/second equivalent)")
print("")

-- Token Bucket - allows burst
local tb = RateLimiterUtils.token_bucket(10, 20)
print("Token Bucket (burst capacity 20):")
for i = 1, 15 do
    local allowed = tb:try_acquire()
    io.write(allowed and "O" or "X")
end
print("\n")

-- Leaky Bucket - smooths out
local lb = RateLimiterUtils.leaky_bucket(10, 20)
print("Leaky Bucket (capacity 20):")
for i = 1, 15 do
    local allowed = lb:try_acquire()
    io.write(allowed and "O" or "X")
end
print("\n")

-- Sliding Window - precise control
local sw = RateLimiterUtils.sliding_window(10, 1)
print("Sliding Window (10 per second):")
for i = 1, 15 do
    local allowed = sw:try_acquire()
    io.write(allowed and "O" or "X")
end
print("\n")

-- Fixed Window - simple counter
local fw = RateLimiterUtils.fixed_window(10, 1)
print("Fixed Window (10 per second):")
for i = 1, 15 do
    local allowed = fw:try_acquire()
    io.write(allowed and "O" or "X")
end
print("\n")

print("========================================")
print("Examples completed!")
print("========================================")