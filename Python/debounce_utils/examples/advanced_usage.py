"""
AllToolkit - Debounce Utilities Advanced Usage Examples

Demonstrates advanced patterns: multi-key debouncing, real-world scenarios.
"""

import time
import threading
from mod import (
    MultiKeyDebouncer,
    MultiKeyThrottler,
    DebouncedFunction,
    ThrottledFunction,
    Debouncer,
    Throttler,
)


def example_multi_key_debounce():
    """Multi-key debouncer - independent debouncing per key."""
    print("\n=== Multi-Key Debouncer ===")
    
    saves = {}
    
    def save_user(user_id, data):
        """Save user data."""
        saves[user_id] = data
        print(f"  Saved user {user_id}: {data}")
    
    debouncer = MultiKeyDebouncer(wait_seconds=0.3)
    
    # Multiple users editing simultaneously
    # Each user has independent debounce
    print("Multiple users editing:")
    
    # User 1 edits
    debouncer.call("user_1", save_user, "user_1", {"name": "Alice"})
    debouncer.call("user_1", save_user, "user_1", {"name": "Alice v2"})
    debouncer.call("user_1", save_user, "user_1", {"name": "Alice final"})
    
    # User 2 edits
    debouncer.call("user_2", save_user, "user_2", {"name": "Bob"})
    debouncer.call("user_2", save_user, "user_2", {"name": "Bob updated"})
    
    # User 3 edits once
    debouncer.call("user_3", save_user, "user_3", {"name": "Charlie"})
    
    time.sleep(0.4)
    
    print(f"  Final saves: {saves}")
    print(f"  Pending keys: {debouncer.pending_keys()}")


def example_multi_key_throttle():
    """Multi-key throttler - independent throttling per key."""
    print("\n=== Multi-Key Throttler ===")
    
    api_log = {}
    
    def call_api(api_name, endpoint):
        """Simulate API call."""
        if api_name not in api_log:
            api_log[api_name] = []
        api_log[api_name].append(endpoint)
        print(f"  {api_name}: called {endpoint}")
    
    throttler = MultiKeyThrottler(interval_seconds=0.2)
    
    # Different APIs have independent throttling
    print("Calling multiple APIs:")
    
    throttler.call("github", call_api, "github", "/repos")
    throttler.call("github", call_api, "github", "/users")  # Throttled
    throttler.call("slack", call_api, "slack", "/messages")  # Different key - executes
    throttler.call("github", call_api, "github", "/issues")  # Throttled
    throttler.call("slack", call_api, "slack", "/channels")  # Throttled
    
    time.sleep(0.25)
    
    throttler.call("github", call_api, "github", "/commits")  # Now executes
    throttler.call("slack", call_api, "slack", "/team")      # Now executes
    
    time.sleep(0.25)
    
    print(f"  GitHub calls: {api_log.get('github', [])}")
    print(f"  Slack calls: {api_log.get('slack', [])}")


def example_search_input():
    """Real-world: Debounced search input."""
    print("\n=== Search Input Debounce ===")
    
    search_history = []
    
    def perform_search(query):
        """Simulate search API call."""
        print(f"  🔍 Searching for: '{query}'")
        search_history.append(query)
        # Would return search results here
        return f"Results for '{query}'"
    
    # 300ms debounce is typical for search
    debounced_search = DebouncedFunction(perform_search, wait_seconds=0.3)
    
    # Simulate typing
    print("User typing: 'typescript tutorial'")
    
    for char in "typescript tutorial":
        partial = search_history[-1] if search_history else ""
        # Actually we're simulating incremental typing
        pass
    
    # More realistic: user typing partial queries
    queries = ["t", "ty", "typ", "types", "typesc", "typescript", "typescript t", "typescript tutorial"]
    
    for q in queries:
        debounced_search(q)
    
    print("  (User stopped typing, search executes...)")
    time.sleep(0.4)
    
    print(f"  Searches performed: {search_history}")
    print(f"  Suppressed {len(queries) - len(search_history)} intermediate searches")


def example_auto_save():
    """Real-world: Auto-save with max_wait."""
    print("\n=== Auto-Save with Max Wait ===")
    
    saves = []
    
    def save_document(content):
        """Save document to server."""
        print(f"  💾 Saved: '{content[:30]}...'")
        saves.append(content)
    
    # 2 second debounce, but force save after 10 seconds max
    debouncer = Debouncer(wait_seconds=2.0, max_wait=10.0)
    
    # User continuously editing
    print("User continuously editing for 12 seconds...")
    
    for i in range(15):
        content = f"Document content - edit #{i}"
        debouncer.call(save_document, content)
        time.sleep(0.8)  # Editing every 0.8s
    
    time.sleep(2.5)  # Let final save complete
    
    print(f"  Total saves: {len(saves)}")
    print(f"  Saves happened at intervals due to max_wait")


def example_rate_limiting_api():
    """Real-world: Throttled API calls."""
    print("\n=== API Rate Limiting ===")
    
    responses = []
    
    def fetch_data(endpoint):
        """Fetch data from API."""
        print(f"  📡 Fetching: {endpoint}")
        responses.append(endpoint)
        return {"data": f"Response from {endpoint}"}
    
    # API allows 10 requests per second = 0.1s interval
    # But we want to be conservative: 1 per 0.2s
    throttler = Throttler(interval_seconds=0.2, leading=True, trailing=False)
    
    # Application trying to make many requests
    endpoints = [
        "/users/1",
        "/users/2",
        "/users/3",
        "/products",
        "/orders",
        "/analytics",
    ]
    
    print("Application requesting 6 endpoints rapidly:")
    
    for endpoint in endpoints:
        throttler.call(fetch_data, endpoint)
    
    # Only first executes, rest are throttled
    print(f"  Immediate responses: {responses}")
    
    # Need to wait for throttle interval
    remaining = [e for e in endpoints if e not in responses]
    
    while remaining:
        time.sleep(0.25)
        endpoint = remaining.pop(0)
        throttler.call(fetch_data, endpoint)
    
    print(f"  All responses: {responses}")


def example_event_handler():
    """Real-world: Window resize handler."""
    print("\n=== Window Resize Handler ===")
    
    resize_events = []
    
    def handle_resize(width, height):
        """Recalculate layout after resize."""
        print(f"  🖥️  Layout recalculated for {width}x{height}")
        resize_events.append((width, height))
    
    # Debounce resize events - wait for user to finish resizing
    debouncer = Debouncer(wait_seconds=0.15)
    
    # Simulate rapid resize events
    print("User resizing window rapidly:")
    
    sizes = [
        (800, 600),
        (820, 600),
        (850, 620),
        (900, 650),
        (950, 700),
        (1000, 750),
        (1024, 768),  # Final size
    ]
    
    for w, h in sizes:
        debouncer.call(handle_resize, w, h)
    
    print("  (User stopped resizing...)")
    time.sleep(0.2)
    
    print(f"  Layout calculations: {len(resize_events)}")
    print(f"  Final layout: {resize_events[-1] if resize_events else None}")


def example_form_validation():
    """Real-world: Form validation debounce."""
    print("\n=== Form Validation ===")
    
    validations = []
    
    def validate_field(field_name, value):
        """Validate form field."""
        is_valid = len(value) >= 3
        print(f"  ✓ Validating {field_name}='{value}': {is_valid}")
        validations.append((field_name, value, is_valid))
        return is_valid
    
    # Debounce validation - wait for user to finish typing field
    debouncer = Debouncer(wait_seconds=0.3, leading=False, trailing=True)
    
    # User filling form fields
    print("User filling form:")
    
    # Name field
    debouncer.call(validate_field, "name", "J")
    debouncer.call(validate_field, "name", "Jo")
    debouncer.call(validate_field, "name", "John")
    
    # Email field (after name validated)
    time.sleep(0.4)
    
    debouncer.call(validate_field, "email", "j")
    debouncer.call(validate_field, "email", "john@")
    debouncer.call(validate_field, "email", "john@example")
    debouncer.call(validate_field, "email", "john@example.com")
    
    time.sleep(0.4)
    
    print(f"  Validations performed: {len(validations)}")
    for field, value, valid in validations:
        print(f"    - {field}: valid={valid}")


def example_concurrent_debounce():
    """Concurrent usage with multiple threads."""
    print("\n=== Concurrent Debounce ===")
    
    events = []
    lock = threading.Lock()
    
    def log_event(msg):
        with lock:
            events.append(msg)
            print(f"  📝 {msg}")
    
    debouncer = Debouncer(wait_seconds=0.1)
    
    # Multiple threads calling
    threads = []
    
    for i in range(5):
        def worker(thread_id):
            for j in range(3):
                debouncer.call(log_event, f"Thread-{thread_id} message-{j}")
                time.sleep(0.02)
        
        t = threading.Thread(target=worker, args=(i,))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    time.sleep(0.2)
    
    print(f"  Events logged: {events}")
    print(f"  Total calls: {sum(3 for _ in range(5))} = 15")
    print(f"  Executed calls: {len(events)}")


def example_context_manager():
    """Using debounced function as context manager."""
    print("\n=== Context Manager Usage ===")
    
    operations = []
    
    def critical_operation(data):
        """Critical operation that must complete."""
        print(f"  ⚡ Executing: {data}")
        operations.append(data)
        return data
    
    # With context manager, pending calls are flushed on exit
    print("Using context manager:")
    
    with DebouncedFunction(critical_operation, wait_seconds=1.0) as debounced_op:
        debounced_op("step 1")
        debounced_op("step 2")
        debounced_op("step 3")
        print("  (Context exits, flushing pending...)")
    
    # All operations flushed on exit
    print(f"  Operations executed: {operations}")


def example_scroll_pagination():
    """Real-world: Scroll-based pagination with throttle."""
    print("\n=== Scroll Pagination ===")
    
    loaded_pages = []
    
    def load_page(page_num):
        """Load next page of content."""
        print(f"  📄 Loading page {page_num}")
        loaded_pages.append(page_num)
    
    # Throttle scroll events to prevent excessive page loads
    throttler = Throttler(interval_seconds=0.5, leading=True, trailing=True)
    
    # Simulate scroll positions triggering page loads
    print("User scrolling rapidly:")
    
    scroll_positions = [
        (100, 1),   # Load page 1
        (500, 2),   # Would load page 2 but throttled
        (900, 3),   # Would load page 3 but throttled
        (1300, 4),  # Would load page 4 but throttled
    ]
    
    for position, page in scroll_positions:
        throttler.call(load_page, page)
    
    time.sleep(0.6)
    
    print(f"  Pages loaded: {loaded_pages}")


def example_stats_tracking():
    """Comprehensive statistics tracking."""
    print("\n=== Statistics Tracking ===")
    
    debouncer = Debouncer(wait_seconds=0.1)
    
    def operation(value):
        pass
    
    # Simulate heavy usage
    print("Simulating 50 rapid calls:")
    
    for i in range(50):
        debouncer.call(operation, i)
    
    time.sleep(0.2)
    
    stats = debouncer.stats
    stats_dict = stats.to_dict()
    
    print("  Debouncer Statistics:")
    for key, value in stats_dict.items():
        print(f"    {key}: {value}")


def main():
    """Run all advanced examples."""
    print("=" * 60)
    print("AllToolkit - Debounce Utilities Advanced Examples")
    print("=" * 60)
    
    example_multi_key_debounce()
    example_multi_key_throttle()
    example_search_input()
    example_auto_save()
    example_rate_limiting_api()
    example_event_handler()
    example_form_validation()
    example_concurrent_debounce()
    example_context_manager()
    example_scroll_pagination()
    example_stats_tracking()
    
    print("\n" + "=" * 60)
    print("All advanced examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()