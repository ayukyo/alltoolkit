"""
AllToolkit - Python Notification Utilities Test Suite

Comprehensive tests for the notification module.
"""

import sys
import os
import time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    Notification, NotificationStatus, NotificationStats,
    Priority, RateLimiter, DesktopNotifier, WebhookSender,
    EmailNotifier, NotificationRouter, NotificationUtils,
    notify, notify_desktop, notify_webhook, notify_slack, notify_discord
)


class TestNotification:
    """Test cases for Notification class."""
    
    @staticmethod
    def run_all_tests():
        """Run all test cases."""
        tests = [
            TestNotification.test_notification_creation,
            TestNotification.test_notification_to_dict,
            TestNotification.test_notification_from_dict,
            TestNotification.test_notification_default_values,
            TestNotification.test_notification_with_metadata,
        ]
        
        passed = 0
        failed = 0
        
        for test in tests:
            try:
                test()
                print(f"✓ {test.__name__}")
                passed += 1
            except AssertionError as e:
                print(f"✗ {test.__name__}: {e}")
                failed += 1
            except Exception as e:
                print(f"✗ {test.__name__}: Unexpected error: {e}")
                failed += 1
        
        print(f"\n{passed} passed, {failed} failed")
        return failed == 0
    
    @staticmethod
    def test_notification_creation():
        """Test basic notification creation."""
        n = Notification(title="Test", message="Hello")
        assert n.title == "Test"
        assert n.message == "Hello"
        assert n.priority == Priority.NORMAL
        assert n.status == NotificationStatus.PENDING
    
    @staticmethod
    def test_notification_to_dict():
        """Test notification to dictionary conversion."""
        n = Notification(title="Test", message="Hello", priority=Priority.HIGH)
        d = n.to_dict()
        assert d["title"] == "Test"
        assert d["message"] == "Hello"
        assert d["priority"] == "HIGH"
        assert "timestamp" in d
    
    @staticmethod
    def test_notification_from_dict():
        """Test notification from dictionary creation."""
        d = {
            "title": "Test",
            "message": "Hello",
            "priority": "URGENT",
            "channel": "test",
            "status": "SENT"
        }
        n = Notification.from_dict(d)
        assert n.title == "Test"
        assert n.priority == Priority.URGENT
        assert n.channel == "test"
        assert n.status == NotificationStatus.SENT
    
    @staticmethod
    def test_notification_default_values():
        """Test notification default values."""
        n = Notification(title="Test", message="Hello")
        assert n.channel == "default"
        assert n.metadata == {}
        assert n.error is None
    
    @staticmethod
    def test_notification_with_metadata():
        """Test notification with metadata."""
        n = Notification(
            title="Test",
            message="Hello",
            metadata={"user_id": 123, "action": "test"}
        )
        assert n.metadata["user_id"] == 123
        assert n.metadata["action"] == "test"


class TestPriority:
    """Test cases for Priority enum."""
    
    @staticmethod
    def run_all_tests():
        """Run all test cases."""
        tests = [
            TestPriority.test_priority_values,
            TestPriority.test_priority_ordering,
        ]
        
        passed = 0
        failed = 0
        
        for test in tests:
            try:
                test()
                print(f"✓ {test.__name__}")
                passed += 1
            except AssertionError as e:
                print(f"✗ {test.__name__}: {e}")
                failed += 1
        
        return failed == 0
    
    @staticmethod
    def test_priority_values():
        """Test priority enum values."""
        assert Priority.LOW == 0
        assert Priority.NORMAL == 1
        assert Priority.HIGH == 2
        assert Priority.URGENT == 3
        assert Priority.CRITICAL == 4
    
    @staticmethod
    def test_priority_ordering():
        """Test priority ordering."""
        assert Priority.LOW < Priority.NORMAL
        assert Priority.NORMAL < Priority.HIGH
        assert Priority.HIGH < Priority.URGENT
        assert Priority.URGENT < Priority.CRITICAL


class TestRateLimiter:
    """Test cases for RateLimiter class."""
    
    @staticmethod
    def run_all_tests():
        """Run all test cases."""
        tests = [
            TestRateLimiter.test_rate_limiter_basic,
            TestRateLimiter.test_rate_limiter_limit,
            TestRateLimiter.test_rate_limiter_window,
            TestRateLimiter.test_rate_limiter_multiple_keys,
            TestRateLimiter.test_rate_limiter_reset,
            TestRateLimiter.test_rate_limiter_wait_time,
        ]
        
        passed = 0
        failed = 0
        
        for test in tests:
            try:
                test()
                print(f"✓ {test.__name__}")
                passed += 1
            except AssertionError as e:
                print(f"✗ {test.__name__}: {e}")
                failed += 1
            except Exception as e:
                print(f"✗ {test.__name__}: Unexpected error: {e}")
                failed += 1
        
        return failed == 0
    
    @staticmethod
    def test_rate_limiter_basic():
        """Test basic rate limiting."""
        limiter = RateLimiter(max_notifications=3, window_seconds=1.0)
        assert limiter.is_allowed("test")
        assert limiter.is_allowed("test")
        assert limiter.is_allowed("test")
        assert not limiter.is_allowed("test")
    
    @staticmethod
    def test_rate_limiter_limit():
        """Test rate limit enforcement."""
        limiter = RateLimiter(max_notifications=1, window_seconds=1.0)
        assert limiter.is_allowed("test")
        
        # Should be rate limited
        for _ in range(5):
            assert not limiter.is_allowed("test")
    
    @staticmethod
    def test_rate_limiter_window():
        """Test rate limit window expiration."""
        limiter = RateLimiter(max_notifications=1, window_seconds=0.1)
        assert limiter.is_allowed("test")
        assert not limiter.is_allowed("test")
        
        # Wait for window to expire
        time.sleep(0.15)
        assert limiter.is_allowed("test")
    
    @staticmethod
    def test_rate_limiter_multiple_keys():
        """Test rate limiting with multiple keys."""
        limiter = RateLimiter(max_notifications=1, window_seconds=1.0)
        assert limiter.is_allowed("key1")
        assert limiter.is_allowed("key2")
        assert not limiter.is_allowed("key1")
        assert not limiter.is_allowed("key2")
    
    @staticmethod
    def test_rate_limiter_reset():
        """Test rate limit reset."""
        limiter = RateLimiter(max_notifications=1, window_seconds=1.0)
        assert limiter.is_allowed("test")
        assert not limiter.is_allowed("test")
        
        limiter.reset("test")
        assert limiter.is_allowed("test")
    
    @staticmethod
    def test_rate_limiter_wait_time():
        """Test wait time calculation."""
        limiter = RateLimiter(max_notifications=1, window_seconds=1.0)
        assert limiter.get_wait_time("test") == 0.0
        
        limiter.is_allowed("test")
        wait_time = limiter.get_wait_time("test")
        assert wait_time > 0.0
        assert wait_time <= 1.0


class TestNotificationStats:
    """Test cases for NotificationStats class."""
    
    @staticmethod
    def run_all_tests():
        """Run all test cases."""
        tests = [
            TestNotificationStats.test_stats_initialization,
            TestNotificationStats.test_stats_record,
            TestNotificationStats.test_stats_to_dict,
            TestNotificationStats.test_stats_success_rate,
        ]
        
        passed = 0
        failed = 0
        
        for test in tests:
            try:
                test()
                print(f"✓ {test.__name__}")
                passed += 1
            except AssertionError as e:
                print(f"✗ {test.__name__}: {e}")
                failed += 1
        
        return failed == 0
    
    @staticmethod
    def test_stats_initialization():
        """Test stats initialization."""
        stats = NotificationStats()
        assert stats.total_sent == 0
        assert stats.total_failed == 0
        assert stats.total_skipped == 0
        assert stats.total_rate_limited == 0
    
    @staticmethod
    def test_stats_record():
        """Test stats recording."""
        stats = NotificationStats()
        stats.record(NotificationStatus.SENT, "console", Priority.NORMAL)
        stats.record(NotificationStatus.SENT, "console", Priority.HIGH)
        stats.record(NotificationStatus.FAILED, "webhook", Priority.NORMAL)
        
        assert stats.total_sent == 2
        assert stats.total_failed == 1
        assert stats.by_channel.get("console_SENT") == 2
        assert stats.by_channel.get("webhook_FAILED") == 1
    
    @staticmethod
    def test_stats_to_dict():
        """Test stats to dictionary conversion."""
        stats = NotificationStats()
        stats.record(NotificationStatus.SENT, "console", Priority.NORMAL)
        d = stats.to_dict()
        
        assert "total_sent" in d
        assert "total_failed" in d
        assert "success_rate" in d
        assert "by_channel" in d
        assert "by_priority" in d
    
    @staticmethod
    def test_stats_success_rate():
        """Test success rate calculation."""
        stats = NotificationStats()
        stats.record(NotificationStatus.SENT, "console", Priority.NORMAL)
        stats.record(NotificationStatus.SENT, "console", Priority.NORMAL)
        stats.record(NotificationStatus.FAILED, "console", Priority.NORMAL)
        
        d = stats.to_dict()
        assert 60.0 <= d["success_rate"] <= 70.0


class TestNotificationRouter:
    """Test cases for NotificationRouter class."""
    
    @staticmethod
    def run_all_tests():
        """Run all test cases."""
        tests = [
            TestNotificationRouter.test_router_creation,
            TestNotificationRouter.test_router_register_channel,
            TestNotificationRouter.test_router_send,
            TestNotificationRouter.test_router_batch_send,
            TestNotificationRouter.test_router_stats,
            TestNotificationRouter.test_router_quiet_hours,
            TestNotificationRouter.test_router_filters,
        ]
        
        passed = 0
        failed = 0
        
        for test in tests:
            try:
                test()
                print(f"✓ {test.__name__}")
                passed += 1
            except AssertionError as e:
                print(f"✗ {test.__name__}: {e}")
                failed += 1
            except Exception as e:
                print(f"✗ {test.__name__}: Unexpected error: {e}")
                failed += 1
        
        return failed == 0
    
    @staticmethod
    def test_router_creation():
        """Test router creation."""
        router = NotificationRouter()
        assert router._channels == {}
        assert router._stats is not None
    
    @staticmethod
    def test_router_register_channel():
        """Test channel registration."""
        router = NotificationRouter()
        
        def handler(n):
            return True
        
        router.register_channel("test", handler)
        assert "test" in router._channels
    
    @staticmethod
    def test_router_send():
        """Test notification sending."""
        router = NotificationRouter()
        
        sent = []
        def handler(n):
            sent.append(n)
            return True
        
        router.register_channel("test", handler)
        
        n = Notification(title="Test", message="Hello", channel="test")
        status = router.send(n)
        
        assert status == NotificationStatus.SENT
        assert len(sent) == 1
        assert sent[0].title == "Test"
    
    @staticmethod
    def test_router_batch_send():
        """Test batch notification sending."""
        router = NotificationRouter()
        
        sent = []
        def handler(n):
            sent.append(n)
            return True
        
        router.register_channel("test", handler)
        
        notifications = [
            Notification(title=f"Test{i}", message=f"Message{i}", channel="test")
            for i in range(3)
        ]
        
        statuses = router.send_batch(notifications)
        
        assert len(statuses) == 3
        assert all(s == NotificationStatus.SENT for s in statuses)
        assert len(sent) == 3
    
    @staticmethod
    def test_router_stats():
        """Test router statistics."""
        router = NotificationRouter()
        
        def handler(n):
            return True
        
        router.register_channel("test", handler)
        
        for i in range(5):
            n = Notification(title="Test", message="Hello", channel="test")
            router.send(n)
        
        stats = router.get_stats()
        assert stats.total_sent == 5
    
    @staticmethod
    def test_router_quiet_hours():
        """Test quiet hours suppression."""
        router = NotificationRouter()
        
        def handler(n):
            return True
        
        router.register_channel("test", handler)
        router.set_quiet_hours(22, 8)  # 10 PM to 8 AM
        
        n = Notification(title="Test", message="Hello", 
                        channel="test", priority=Priority.LOW)
        status = router.send(n)
        
        # Should be skipped during quiet hours (if current time is in range)
        # This test may vary based on current time
        assert status in [NotificationStatus.SENT, NotificationStatus.SKIPPED]
    
    @staticmethod
    def test_router_filters():
        """Test notification filters."""
        router = NotificationRouter()
        
        sent = []
        def handler(n):
            sent.append(n)
            return True
        
        router.register_channel("test", handler)
        
        # Filter out LOW priority
        router.add_filter(lambda n: n.priority >= Priority.NORMAL)
        
        n_low = Notification(title="Low", message="Test", 
                            channel="test", priority=Priority.LOW)
        n_normal = Notification(title="Normal", message="Test", 
                               channel="test", priority=Priority.NORMAL)
        
        status_low = router.send(n_low)
        status_normal = router.send(n_normal)
        
        assert status_low == NotificationStatus.SKIPPED
        assert status_normal == NotificationStatus.SENT
        assert len(sent) == 1


class TestNotificationUtils:
    """Test cases for NotificationUtils class."""
    
    @staticmethod
    def run_all_tests():
        """Run all test cases."""
        tests = [
            TestNotificationUtils.test_utils_notify,
            TestNotificationUtils.test_utils_get_router,
            TestNotificationUtils.test_utils_stats,
            TestNotificationUtils.test_utils_reset_stats,
            TestNotificationUtils.test_convenience_functions,
        ]
        
        passed = 0
        failed = 0
        
        for test in tests:
            try:
                test()
                print(f"✓ {test.__name__}")
                passed += 1
            except AssertionError as e:
                print(f"✗ {test.__name__}: {e}")
                failed += 1
            except Exception as e:
                print(f"✗ {test.__name__}: Unexpected error: {e}")
                failed += 1
        
        return failed == 0
    
    @staticmethod
    def test_utils_notify():
        """Test NotificationUtils.notify."""
        status = NotificationUtils.notify(
            title="Test",
            message="Hello from tests",
            priority=Priority.NORMAL,
            channel="console"
        )
        assert status in [NotificationStatus.SENT, NotificationStatus.SKIPPED]
    
    @staticmethod
    def test_utils_get_router():
        """Test NotificationUtils.get_router."""
        router = NotificationUtils.get_router()
        assert router is not None
        assert isinstance(router, NotificationRouter)
    
    @staticmethod
    def test_utils_stats():
        """Test NotificationUtils.get_stats."""
        stats = NotificationUtils.get_stats()
        assert isinstance(stats, dict)
        assert "total_sent" in stats
        assert "total_failed" in stats
    
    @staticmethod
    def test_utils_reset_stats():
        """Test NotificationUtils.reset_stats."""
        NotificationUtils.reset_stats()
        stats = NotificationUtils.get_stats()
        assert stats["total_sent"] == 0
        assert stats["total_failed"] == 0
    
    @staticmethod
    def test_convenience_functions():
        """Test convenience functions."""
        # Test notify function
        status = notify("Test", "Message", Priority.NORMAL, "console")
        assert status in [NotificationStatus.SENT, NotificationStatus.SKIPPED]
        
        # Test notify_desktop (may not work in all environments)
        result = notify_desktop("Test", "Message")
        assert isinstance(result, bool)
        
        # Test notify_webhook (will fail without valid URL, but should not crash)
        result = notify_webhook("http://invalid", "Test", "Message")
        assert isinstance(result, bool)


class TestDesktopNotifier:
    """Test cases for DesktopNotifier class."""
    
    @staticmethod
    def run_all_tests():
        """Run all test cases."""
        tests = [
            TestDesktopNotifier.test_send_basic,
        ]
        
        passed = 0
        failed = 0
        
        for test in tests:
            try:
                test()
                print(f"✓ {test.__name__}")
                passed += 1
            except AssertionError as e:
                print(f"✗ {test.__name__}: {e}")
                failed += 1
            except Exception as e:
                print(f"✗ {test.__name__}: Unexpected error: {e}")
                failed += 1
        
        return failed == 0
    
    @staticmethod
    def test_send_basic():
        """Test desktop notification sending."""
        # This may not work in headless environments
        result = DesktopNotifier.send("Test", "Message")
        assert isinstance(result, bool)


class TestWebhookSender:
    """Test cases for WebhookSender class."""
    
    @staticmethod
    def run_all_tests():
        """Run all test cases."""
        tests = [
            TestWebhookSender.test_send_invalid_url,
            TestWebhookSender.test_send_slack_invalid_url,
            TestWebhookSender.test_send_discord_invalid_url,
        ]
        
        passed = 0
        failed = 0
        
        for test in tests:
            try:
                test()
                print(f"✓ {test.__name__}")
                passed += 1
            except AssertionError as e:
                print(f"✗ {test.__name__}: {e}")
                failed += 1
            except Exception as e:
                print(f"✗ {test.__name__}: Unexpected error: {e}")
                failed += 1
        
        return failed == 0
    
    @staticmethod
    def test_send_invalid_url():
        """Test webhook send with invalid URL."""
        result = WebhookSender.send("http://invalid-url-test", {"test": "data"})
        assert result is False
    
    @staticmethod
    def test_send_slack_invalid_url():
        """Test Slack webhook with invalid URL."""
        result = WebhookSender.send_slack("http://invalid-url-test", "message")
        assert result is False
    
    @staticmethod
    def test_send_discord_invalid_url():
        """Test Discord webhook with invalid URL."""
        result = WebhookSender.send_discord("http://invalid-url-test", "title", "message")
        assert result is False


def run_all_tests():
    """Run all test suites."""
    print("=" * 60)
    print("AllToolkit - Python Notification Utilities Test Suite")
    print("=" * 60)
    print()
    
    test_suites = [
        ("Notification", TestNotification.run_all_tests),
        ("Priority", TestPriority.run_all_tests),
        ("RateLimiter", TestRateLimiter.run_all_tests),
        ("NotificationStats", TestNotificationStats.run_all_tests),
        ("NotificationRouter", TestNotificationRouter.run_all_tests),
        ("NotificationUtils", TestNotificationUtils.run_all_tests),
        ("DesktopNotifier", TestDesktopNotifier.run_all_tests),
        ("WebhookSender", TestWebhookSender.run_all_tests),
    ]
    
    all_passed = True
    
    for name, test_func in test_suites:
        print(f"\n{'─' * 60}")
        print(f"Testing: {name}")
        print(f"{'─' * 60}")
        if not test_func():
            all_passed = False
    
    print()
    print("=" * 60)
    if all_passed:
        print("✅ All tests passed!")
    else:
        print("❌ Some tests failed")
    print("=" * 60)
    
    return all_passed


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
