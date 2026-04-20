"""
Throttle Utils - Usage Examples

This module demonstrates various throttling patterns for controlling
the rate of function execution.
"""

import time
import asyncio
import sys
sys.path.insert(0, '..')
from mod import (
    throttle,
    athrottle,
    ThrottleQueue,
    SlidingThrottle,
    TokenBucketThrottle,
    AdaptiveThrottle,
    ThrottleMode,
)


def example_basic_throttle():
    """Basic throttling with leading mode."""
    print("=== Basic Throttle (Leading Mode) ===\n")
    
    call_times = []
    
    @throttle(0.1)  # 100ms interval
    def handle_click(x):
        call_times.append(time.time())
        print(f"  Click handled: {x}")
        return x * 2
    
    # Rapid calls
    start = time.time()
    for i in range(5):
        result = handle_click(i)
        print(f"  Call {i}: result={result}")
        time.sleep(0.02)  # 20ms between calls
    
    elapsed = time.time() - start
    print(f"\n  Total calls made: 5")
    print(f"  Function executed: {len(call_times)} time(s)")
    print(f"  Elapsed time: {elapsed:.3f}s")
    print()


def example_trailing_throttle():
    """Trailing mode - waits for pause before calling."""
    print("=== Trailing Throttle ===\n")
    
    @throttle(0.1, mode='trailing')
    def handle_resize(width, height):
        print(f"  Window resized to {width}x{height}")
        return width * height
    
    print("  Simulating rapid resize events...")
    
    # Rapid resize events
    handle_resize(800, 600)
    handle_resize(900, 700)
    handle_resize(1000, 800)
    handle_resize(1200, 900)
    
    print("  Waiting for trailing call...")
    time.sleep(0.15)
    
    # Need to flush to get the final call
    result = handle_resize.flush()
    print(f"  Final result: {result}")
    print()


def example_both_mode():
    """Both mode - leading AND trailing calls."""
    print("=== Both Mode (Leading + Trailing) ===\n")
    
    @throttle(0.1, mode='both')
    def handle_scroll(position):
        print(f"  Scroll position: {position}")
        return position
    
    print("  First scroll:")
    handle_scroll(100)  # Leading call - executes immediately
    
    print("\n  Rapid scrolls:")
    handle_scroll(200)
    handle_scroll(300)
    handle_scroll(400)
    
    print("\n  Waiting for trailing call...")
    time.sleep(0.15)
    handle_scroll.flush()  # Trailing call with last position (400)
    
    print()


def example_cancel_and_flush():
    """Cancel and flush operations."""
    print("=== Cancel and Flush ===\n")
    
    @throttle(0.1, mode='trailing')
    def save_document(content):
        print(f"  Document saved: {len(content)} chars")
        return True
    
    # Queue up a save
    save_document("Draft content...")
    
    print(f"  Pending save: {save_document.pending()}")
    
    # Cancel the pending save
    print("  Cancelling pending save...")
    save_document.cancel()
    
    print(f"  Pending after cancel: {save_document.pending()}")
    
    # Try flush - should return None since cancelled
    result = save_document.flush()
    print(f"  Flush result: {result}")
    print()


def example_with_parameters():
    """Explicit leading/trailing parameters."""
    print("=== Explicit Parameters ===\n")
    
    # Same as mode='trailing'
    @throttle(0.1, leading=False, trailing=True)
    def delayed_search(query):
        print(f"  Searching for: {query}")
        return f"results for '{query}'"
    
    delayed_search("hel")
    delayed_search("hell")
    delayed_search("hello")
    
    time.sleep(0.15)
    result = delayed_search.flush()
    print(f"  Final search result: {result}")
    print()


def example_throttle_queue():
    """ThrottleQueue for batch processing."""
    print("=== Throttle Queue ===\n")
    
    processed_items = []
    
    def process_item(item):
        processed_items.append(item)
        print(f"  Processed: {item}")
        return item.upper()
    
    queue = ThrottleQueue(process_item, interval=0.05, max_queue_size=10)
    
    print("  Enqueueing items...")
    for i in range(5):
        queue.enqueue(f"item_{i}")
    
    print(f"  Queue size: {queue.size()}")
    
    print("\n  Processing items...")
    results = []
    while not queue.is_empty():
        result = queue.process_next()
        if result:
            results.append(result)
        time.sleep(0.06)  # Wait for throttle interval
    
    print(f"\n  All results: {results}")
    print()


def example_sliding_throttle():
    """SlidingThrottle for precise rate control."""
    print("=== Sliding Throttle ===\n")
    
    throttle = SlidingThrottle(interval=0.1)
    
    print("  Attempting 5 operations:")
    for i in range(5):
        wait_time = throttle.acquire()
        if wait_time == 0:
            print(f"    {i}: Executed immediately")
        else:
            print(f"    {i}: Need to wait {wait_time:.3f}s")
            time.sleep(wait_time)
            throttle.acquire()  # Now we can proceed
            print(f"    {i}: Executed after waiting")
    
    print()


def example_token_bucket():
    """TokenBucketThrottle for burst control."""
    print("=== Token Bucket Throttle ===\n")
    
    bucket = TokenBucketThrottle(capacity=5, refill_rate=2)  # 5 tokens, 2/sec
    
    print(f"  Initial tokens: {bucket.available()}")
    
    print("\n  Consuming 3 tokens:")
    if bucket.try_consume(3):
        print(f"    Success! Tokens remaining: {bucket.available()}")
    
    print("\n  Consuming 3 more tokens (only 2 available):")
    if bucket.try_consume(3):
        print("    Success!")
    else:
        print("    Not enough tokens!")
    
    print("\n  Waiting 1 second for refill...")
    time.sleep(1.0)
    print(f"  Tokens after refill: {bucket.available():.1f}")
    
    print("\n  Resetting to full capacity...")
    bucket.reset()
    print(f"  Tokens: {bucket.available()}")
    
    print()


def example_adaptive_throttle():
    """AdaptiveThrottle for backpressure handling."""
    print("=== Adaptive Throttle ===\n")
    
    throttle = AdaptiveThrottle(
        initial_interval=0.1,
        min_interval=0.01,
        max_interval=1.0,
        backoff_factor=2.0,
        recovery_factor=0.8
    )
    
    print(f"  Initial interval: {throttle.interval:.3f}s")
    
    print("\n  Simulating failures (backoff):")
    for i in range(4):
        throttle.failure()
        print(f"    After failure {i+1}: {throttle.interval:.3f}s")
    
    print("\n  Simulating successes (recovery):")
    for i in range(4):
        throttle.success()
        print(f"    After success {i+1}: {throttle.interval:.3f}s")
    
    print()


async def example_async_throttle():
    """Async throttling."""
    print("=== Async Throttle ===\n")
    
    @athrottle(0.1, mode='leading')
    async def fetch_data(url):
        print(f"  Fetching: {url}")
        await asyncio.sleep(0.01)  # Simulate network
        return f"data from {url}"
    
    print("  Making rapid async calls:")
    
    # Rapid async calls
    results = []
    for i in range(5):
        result = await fetch_data(f"https://api.example.com/{i}")
        results.append(result)
        await asyncio.sleep(0.02)
    
    print(f"\n  Results: {len(results)}")
    print()


def example_api_rate_limiting():
    """Real-world example: API rate limiting."""
    print("=== API Rate Limiting Example ===\n")
    
    class APIClient:
        def __init__(self, requests_per_second=10):
            self.throttle = SlidingThrottle(1.0 / requests_per_second)
            self.request_count = 0
        
        def request(self, endpoint):
            wait_time = self.throttle.acquire()
            if wait_time > 0:
                print(f"    Rate limited, waiting {wait_time:.3f}s...")
                time.sleep(wait_time)
                self.throttle.acquire()
            
            self.request_count += 1
            print(f"    Request {self.request_count}: {endpoint}")
            return f"response from {endpoint}"
    
    client = APIClient(requests_per_second=5)  # 5 requests per second
    
    print("  Making 10 requests at 5/sec limit:")
    start = time.time()
    for i in range(10):
        client.request(f"/api/data/{i}")
    elapsed = time.time() - start
    
    print(f"\n  Total time: {elapsed:.3f}s")
    print(f"  Expected: ~1.8s for 10 requests at 5/sec")
    print()


def example_scroll_handler():
    """Real-world example: Scroll event handler."""
    print("=== Scroll Event Handler ===\n")
    
    scroll_positions = []
    
    @throttle(0.05, mode='trailing')
    def on_scroll(y_position):
        scroll_positions.append(y_position)
        # Would update UI here
        return y_position
    
    print("  Simulating scroll events:")
    
    # Simulate rapid scrolling
    for y in range(0, 1000, 50):
        on_scroll(y)
    
    print(f"  Scroll events: 20")
    print(f"  Handler called: {len(scroll_positions)} time(s)")
    
    time.sleep(0.1)
    on_scroll.flush()
    
    print(f"  After flush: {len(scroll_positions)} time(s)")
    print()


def example_search_autocomplete():
    """Real-world example: Search autocomplete."""
    print("=== Search Autocomplete ===\n")
    
    search_queries = []
    
    @throttle(0.3, mode='trailing')
    def search(query):
        # Only search after user stops typing
        print(f"  Searching for: '{query}'")
        search_queries.append(query)
        return f"Results for '{query}'"
    
    print("  User typing: 'h' 'he' 'hel' 'hell' 'hello'")
    
    for q in ['h', 'he', 'hel', 'hell', 'hello']:
        search(q)
        print(f"    Typed: '{q}'")
        time.sleep(0.05)
    
    print("\n  Waiting for throttle...")
    time.sleep(0.35)
    result = search.flush()
    
    print(f"\n  Only searched once for: '{search_queries[0]}'")
    print(f"  Result: {result}")
    print()


def main():
    """Run all examples."""
    print("\n" + "=" * 60)
    print("THROTTLE UTILS - USAGE EXAMPLES")
    print("=" * 60 + "\n")
    
    # Basic examples
    example_basic_throttle()
    example_trailing_throttle()
    example_both_mode()
    example_cancel_and_flush()
    example_with_parameters()
    
    # Advanced examples
    example_throttle_queue()
    example_sliding_throttle()
    example_token_bucket()
    example_adaptive_throttle()
    
    # Async example
    print("Running async example...")
    # Python 3.6 compatible async runner
    loop = asyncio.get_event_loop()
    loop.run_until_complete(example_async_throttle())
    
    # Real-world examples
    example_api_rate_limiting()
    example_scroll_handler()
    example_search_autocomplete()
    
    print("=" * 60)
    print("All examples completed!")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()