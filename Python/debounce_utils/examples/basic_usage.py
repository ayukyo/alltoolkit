"""
AllToolkit - Debounce Utilities Basic Usage Examples

Demonstrates basic debounce and throttle functionality.
"""

import time
from mod import Debouncer, Throttler, debounce, throttle


def example_basic_debounce():
    """Basic debounce example - wait for user to stop typing."""
    print("\n=== Basic Debounce ===")
    
    search_results = []
    
    def perform_search(query):
        """Simulates a search operation."""
        print(f"  Searching for: '{query}'")
        search_results.append(query)
    
    debouncer = Debouncer(wait_seconds=0.3)
    
    # Simulate rapid typing
    print("User typing 'hello'...")
    debouncer.call(perform_search, "h")
    debouncer.call(perform_search, "he")
    debouncer.call(perform_search, "hel")
    debouncer.call(perform_search, "hell")
    debouncer.call(perform_search, "hello")
    
    print("  (Waiting 0.3s for debounce...)")
    time.sleep(0.4)
    
    print(f"  Results: {search_results}")
    # Only 'hello' was searched, others were debounced away


def example_leading_debounce():
    """Leading edge debounce - execute immediately on first call."""
    print("\n=== Leading Edge Debounce ===")
    
    clicks = []
    
    def handle_click(button):
        """Simulates handling a button click."""
        print(f"  Click handled: {button}")
        clicks.append(button)
        return button
    
    debouncer = Debouncer(wait_seconds=0.5, leading=True, trailing=False)
    
    # First click executes immediately
    result = debouncer.call(handle_click, "submit")
    print(f"  Immediate result: {result}")
    
    # Rapid subsequent clicks within wait time are ignored
    debouncer.call(handle_click, "submit")  # Ignored
    debouncer.call(handle_click, "submit")  # Ignored
    
    print(f"  Total clicks processed: {clicks}")


def example_trailing_debounce():
    """Trailing edge debounce - execute after wait time."""
    print("\n=== Trailing Edge Debounce ===")
    
    saves = []
    
    def auto_save(content):
        """Simulates auto-save operation."""
        print(f"  Auto-saved: '{content}'")
        saves.append(content)
    
    debouncer = Debouncer(wait_seconds=0.5, leading=False, trailing=True)
    
    # Rapid edits - only last version is saved
    debouncer.call(auto_save, "version 1")
    debouncer.call(auto_save, "version 2")
    debouncer.call(auto_save, "version 3")
    
    print("  (User stopped editing, waiting for auto-save...)")
    time.sleep(0.6)
    
    print(f"  Saved versions: {saves}")
    # Only 'version 3' was saved


def example_leading_trailing_debounce():
    """Both leading and trailing edge."""
    print("\n=== Leading + Trailing Debounce ===")
    
    events = []
    
    def log_event(action):
        print(f"  Event: {action}")
        events.append(action)
        return action
    
    debouncer = Debouncer(wait_seconds=0.3, leading=True, trailing=True)
    
    # First call executes immediately (leading)
    result = debouncer.call(log_event, "scroll_start")
    print(f"  Immediate: {result}")
    
    # More events during wait time
    debouncer.call(log_event, "scrolling...")
    debouncer.call(log_event, "scroll_end")
    
    print("  (Waiting for trailing edge...)")
    time.sleep(0.4)
    
    # Both leading and trailing were logged
    print(f"  All events: {events}")


def example_debounce_decorator():
    """Using the debounce decorator."""
    print("\n=== Debounce Decorator ===")
    
    notifications = []
    
    @debounce(wait_seconds=0.2)
    def send_notification(message):
        """Simulates sending a notification."""
        print(f"  Notification sent: '{message}'")
        notifications.append(message)
    
    # Decorated function is debounced automatically
    send_notification("Hello")
    send_notification("Hello World")
    send_notification("Hello World!!!")
    
    time.sleep(0.3)
    
    print(f"  Notifications sent: {notifications}")


def example_basic_throttle():
    """Basic throttle example - limit execution frequency."""
    print("\n=== Basic Throttle ===")
    
    scroll_events = []
    
    def handle_scroll(position):
        """Simulates handling scroll events."""
        print(f"  Scroll: position={position}")
        scroll_events.append(position)
    
    throttler = Throttler(interval_seconds=0.2)
    
    # Rapid scroll events
    print("Rapid scrolling...")
    throttler.call(handle_scroll, 0)    # Executes immediately (leading)
    throttler.call(handle_scroll, 100)  # Throttled
    throttler.call(handle_scroll, 200)  # Throttled
    throttler.call(handle_scroll, 300)  # Throttled
    
    time.sleep(0.25)
    
    throttler.call(handle_scroll, 400)  # Now executes
    throttler.call(handle_scroll, 500)  # Throttled
    
    time.sleep(0.25)
    
    print(f"  Positions processed: {scroll_events}")


def example_throttle_decorator():
    """Using the throttle decorator."""
    print("\n=== Throttle Decorator ===")
    
    api_calls = []
    
    @throttle(interval_seconds=0.5)
    def call_api(endpoint):
        """Simulates API call (limited to once per 0.5s)."""
        print(f"  API called: {endpoint}")
        api_calls.append(endpoint)
        return endpoint
    
    # Rapid API calls - only first executes immediately
    result = call_api("/data")
    print(f"  Result: {result}")
    
    call_api("/data")  # Throttled
    call_api("/data")  # Throttled
    
    time.sleep(0.6)
    
    result = call_api("/data")  # Executes now
    print(f"  Result: {result}")
    
    print(f"  Total API calls made: {len(api_calls)}")


def example_cancel_and_flush():
    """Cancel and flush operations."""
    print("\n=== Cancel and Flush ===")
    
    saves = []
    
    def save_data(data):
        print(f"  Saved: {data}")
        saves.append(data)
        return data
    
    debouncer = Debouncer(wait_seconds=1.0)
    
    # Start a debounce
    debouncer.call(save_data, "important data")
    
    # Cancel it
    print("  Cancelling save...")
    cancelled = debouncer.cancel()
    print(f"  Cancelled: {cancelled}")
    
    time.sleep(1.1)
    print(f"  Saves after cancel: {saves}")  # Empty - cancelled
    
    # Try flush instead
    debouncer.call(save_data, "urgent data")
    print("  Flushing save...")
    result = debouncer.flush()
    print(f"  Flush result: {result}")
    print(f"  Saves after flush: {saves}")


def example_checking_status():
    """Checking debouncer/throttler status."""
    print("\n=== Checking Status ===")
    
    debouncer = Debouncer(wait_seconds=0.5)
    throttler = Throttler(interval_seconds=0.5)
    
    print(f"  Debouncer pending (before call): {debouncer.is_pending}")
    print(f"  Throttler throttled (before call): {throttler.is_throttled}")
    
    debouncer.call(lambda: None)
    throttler.call(lambda: None)
    
    print(f"  Debouncer pending (after call): {debouncer.is_pending}")
    print(f"  Throttler throttled (after call): {throttler.is_throttled}")
    print(f"  Time until next throttle: {throttler.time_until_next:.2f}s")


def example_statistics():
    """Using statistics tracking."""
    print("\n=== Statistics ===")
    
    debouncer = Debouncer(wait_seconds=0.1)
    
    def callback(value):
        pass
    
    # Multiple calls
    for i in range(10):
        debouncer.call(callback, i)
    
    time.sleep(0.2)
    
    stats = debouncer.stats
    print(f"  Total calls: {stats.total_calls}")
    print(f"  Executed calls: {stats.executed_calls}")
    print(f"  Suppression rate: {stats.suppression_rate:.1%}")
    
    # Reset stats
    stats.reset()
    print(f"  After reset: {stats.total_calls}")


def main():
    """Run all examples."""
    print("=" * 60)
    print("AllToolkit - Debounce Utilities Examples")
    print("=" * 60)
    
    example_basic_debounce()
    example_leading_debounce()
    example_trailing_debounce()
    example_leading_trailing_debounce()
    example_debounce_decorator()
    example_basic_throttle()
    example_throttle_decorator()
    example_cancel_and_flush()
    example_checking_status()
    example_statistics()
    
    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()