"""
AllToolkit - Webhook Utils Test Suite

Comprehensive tests for webhook utilities.
Run with: python webhook_utils_test.py
"""

import unittest
import json
import time
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    WebhookConfig,
    WebhookResult,
    WebhookEvent,
    WebhookSigner,
    WebhookLogger,
    WebhookSender,
    WebhookManager,
    WebhookError,
    WebhookSendError,
    WebhookVerificationError,
    RetryStrategy,
    WebhookSigner,
    AsyncWebhookSender,
    WebhookFuture,
    sign_payload,
    verify_signature,
    init_webhook,
    send_webhook,
    register_endpoint,
    send_to_endpoint,
    broadcast_event,
    webhook_decorator,
)


# Test HTTP server for webhook testing
class TestWebhookHandler(BaseHTTPRequestHandler):
    """Test webhook receiver."""
    
    received_requests = []
    response_code = 200
    response_body = '{"status": "ok"}'
    
    def log_message(self, format, *args):
        pass  # Suppress logging
    
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8')
        
        TestWebhookHandler.received_requests.append({
            'path': self.path,
            'headers': dict(self.headers),
            'body': body,
        })
        
        self.send_response(TestWebhookHandler.response_code)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(TestWebhookHandler.response_body.encode())
    
    @classmethod
    def reset(cls):
        cls.received_requests = []
        cls.response_code = 200
        cls.response_body = '{"status": "ok"}'


class TestWebhookEvent(unittest.TestCase):
    """Test WebhookEvent class."""
    
    def test_create_event(self):
        """Test creating a basic event."""
        event = WebhookEvent(
            event_type="user.created",
            payload={"user_id": 123},
        )
        
        self.assertEqual(event.event_type, "user.created")
        self.assertEqual(event.payload, {"user_id": 123})
        self.assertIsNotNone(event.id)
        self.assertIsNotNone(event.timestamp)
    
    def test_event_id_generation(self):
        """Test that event IDs are unique."""
        events = [WebhookEvent("test", {}) for _ in range(100)]
        ids = [e.id for e in events]
        
        self.assertEqual(len(ids), len(set(ids)))  # All unique
    
    def test_event_to_json(self):
        """Test JSON serialization."""
        event = WebhookEvent(
            event_type="order.completed",
            payload={"order_id": "ORD-123"},
            id="custom-id",
        )
        
        json_str = event.to_json()
        data = json.loads(json_str)
        
        self.assertEqual(data['id'], "custom-id")
        self.assertEqual(data['type'], "order.completed")
        self.assertEqual(data['data'], {"order_id": "ORD-123"})
        self.assertIn('timestamp', data)
    
    def test_custom_timestamp(self):
        """Test custom timestamp."""
        custom_ts = 1234567890.0
        event = WebhookEvent(
            event_type="test",
            payload={},
            timestamp=custom_ts,
        )
        
        self.assertEqual(event.timestamp, custom_ts)


class TestWebhookSigner(unittest.TestCase):
    """Test WebhookSigner class."""
    
    def test_create_signer(self):
        """Test creating a signer."""
        signer = WebhookSigner("my-secret")
        self.assertEqual(signer.algorithm, "sha256")
    
    def test_create_signer_custom_algorithm(self):
        """Test creating signer with custom algorithm."""
        signer = WebhookSigner("secret", "sha512")
        self.assertEqual(signer.algorithm, "sha512")
    
    def test_sign_empty_secret_raises(self):
        """Test that empty secret raises error."""
        with self.assertRaises(ValueError):
            WebhookSigner("")
    
    def test_sign_string(self):
        """Test signing a string."""
        signer = WebhookSigner("secret")
        signature = signer.sign("hello world")
        
        self.assertIsInstance(signature, str)
        self.assertEqual(len(signature), 64)  # SHA256 hex length
    
    def test_sign_dict(self):
        """Test signing a dictionary."""
        signer = WebhookSigner("secret")
        payload = {"key": "value"}
        
        sig1 = signer.sign(payload)
        sig2 = signer.sign(payload)
        
        self.assertEqual(sig1, sig2)  # Consistent
    
    def test_sign_consistency(self):
        """Test that signing is consistent."""
        signer = WebhookSigner("secret")
        
        for _ in range(10):
            sig = signer.sign("test data")
            self.assertEqual(sig, signer.sign("test data"))
    
    def test_verify_valid_signature(self):
        """Test verifying a valid signature."""
        signer = WebhookSigner("secret")
        payload = "test data"
        signature = signer.sign(payload)
        
        self.assertTrue(signer.verify(payload, signature))
    
    def test_verify_invalid_signature(self):
        """Test verifying an invalid signature."""
        signer = WebhookSigner("secret")
        payload = "test data"
        
        self.assertFalse(signer.verify(payload, "invalid_signature"))
    
    def test_verify_tampered_payload(self):
        """Test that tampered payload fails verification."""
        signer = WebhookSigner("secret")
        payload = "original data"
        signature = signer.sign(payload)
        
        self.assertFalse(signer.verify("tampered data", signature))
    
    def test_sign_base64(self):
        """Test base64 signature."""
        signer = WebhookSigner("secret")
        signature = signer.sign_base64("test")
        
        self.assertIsInstance(signature, str)
        self.assertTrue(signer.verify_base64("test", signature))
    
    def test_verify_base64_invalid(self):
        """Test base64 verification with invalid signature."""
        signer = WebhookSigner("secret")
        
        self.assertFalse(signer.verify_base64("test", "invalid"))
    
    def test_get_signature_header(self):
        """Test getting signature header."""
        signer = WebhookSigner("secret")
        headers = signer.get_signature_header({"key": "value"})
        
        self.assertIn("X-Webhook-Signature", headers)
        self.assertTrue(headers["X-Webhook-Signature"].startswith("sha256="))
    
    def test_different_secrets_different_signatures(self):
        """Test that different secrets produce different signatures."""
        signer1 = WebhookSigner("secret1")
        signer2 = WebhookSigner("secret2")
        
        sig1 = signer1.sign("data")
        sig2 = signer2.sign("data")
        
        self.assertNotEqual(sig1, sig2)


class TestWebhookConfig(unittest.TestCase):
    """Test WebhookConfig class."""
    
    def test_create_config(self):
        """Test creating basic config."""
        config = WebhookConfig(url="https://example.com/webhook")
        
        self.assertEqual(config.url, "https://example.com/webhook")
        self.assertIsNone(config.secret)
        self.assertEqual(config.timeout, 30.0)
        self.assertEqual(config.max_retries, 3)
    
    def test_create_config_with_secret(self):
        """Test config with secret."""
        config = WebhookConfig(
            url="https://example.com/webhook",
            secret="my-secret",
            timeout=10.0,
        )
        
        self.assertEqual(config.secret, "my-secret")
        self.assertEqual(config.timeout, 10.0)
    
    def test_empty_url_raises(self):
        """Test that empty URL raises error."""
        with self.assertRaises(ValueError):
            WebhookConfig(url="")
    
    def test_negative_retries_raises(self):
        """Test that negative retries raises error."""
        with self.assertRaises(ValueError):
            WebhookConfig(url="https://example.com", max_retries=-1)
    
    def test_custom_headers(self):
        """Test custom headers."""
        config = WebhookConfig(
            url="https://example.com",
            headers={"X-Custom": "value"},
        )
        
        self.assertEqual(config.headers["X-Custom"], "value")


class TestWebhookResult(unittest.TestCase):
    """Test WebhookResult class."""
    
    def test_create_success_result(self):
        """Test creating a success result."""
        result = WebhookResult(
            success=True,
            status_code=200,
            url="https://example.com",
        )
        
        self.assertTrue(result)
        self.assertTrue(result.success)
    
    def test_create_error_result(self):
        """Test creating an error result."""
        result = WebhookResult(
            success=False,
            error="Connection failed",
            url="https://example.com",
        )
        
        self.assertFalse(result)
        self.assertFalse(result.success)
    
    def test_to_dict(self):
        """Test converting to dictionary."""
        result = WebhookResult(
            success=True,
            status_code=200,
            response_body='{"ok": true}',
            attempts=1,
            duration_ms=50.0,
            url="https://example.com",
        )
        
        d = result.to_dict()
        
        self.assertTrue(d['success'])
        self.assertEqual(d['status_code'], 200)
        self.assertEqual(d['attempts'], 1)


class TestWebhookLogger(unittest.TestCase):
    """Test WebhookLogger class."""
    
    def test_create_logger(self):
        """Test creating a logger."""
        logger = WebhookLogger()
        self.assertIsNotNone(logger)
    
    def test_log_success(self):
        """Test logging success."""
        logger = WebhookLogger()
        result = WebhookResult(success=True, status_code=200, url="https://example.com")
        
        logger.log_success(result)
        
        stats = logger.get_stats()
        self.assertEqual(stats['total_sent'], 1)
        self.assertEqual(stats['total_success'], 1)
    
    def test_log_error(self):
        """Test logging error."""
        logger = WebhookLogger()
        
        logger.log_error("Connection failed", url="https://example.com")
        
        stats = logger.get_stats()
        self.assertEqual(stats['total_sent'], 1)
        self.assertEqual(stats['total_failed'], 1)
    
    def test_get_stats(self):
        """Test getting statistics."""
        logger = WebhookLogger()
        
        for i in range(5):
            result = WebhookResult(success=True, status_code=200, url="https://example.com")
            logger.log_success(result)
        
        for i in range(3):
            logger.log_error("Error", url="https://example.com")
        
        stats = logger.get_stats()
        
        self.assertEqual(stats['total_sent'], 8)
        self.assertEqual(stats['total_success'], 5)
        self.assertEqual(stats['total_failed'], 3)
        self.assertAlmostEqual(stats['success_rate'], 5/8)
    
    def test_get_recent(self):
        """Test getting recent events."""
        logger = WebhookLogger()
        
        for i in range(20):
            result = WebhookResult(success=True, status_code=200, url="https://example.com")
            logger.log_success(result)
        
        recent = logger.get_recent(limit=5)
        
        self.assertEqual(len(recent), 5)
    
    def test_max_events_limit(self):
        """Test max events limit."""
        logger = WebhookLogger(max_events=10)
        
        for i in range(100):
            result = WebhookResult(success=True, status_code=200, url="https://example.com")
            logger.log_success(result)
        
        recent = logger.get_recent(limit=100)
        
        self.assertEqual(len(recent), 10)  # Limited to max_events
    
    def test_clear(self):
        """Test clearing logger."""
        logger = WebhookLogger()
        
        logger.log_success(WebhookResult(success=True, status_code=200, url="https://example.com"))
        logger.clear()
        
        stats = logger.get_stats()
        self.assertEqual(stats['total_sent'], 0)


class TestWebhookSender(unittest.TestCase):
    """Test WebhookSender class."""
    
    def setUp(self):
        """Set up test server."""
        TestWebhookHandler.reset()
        self.server = HTTPServer(('localhost', 0), TestWebhookHandler)
        self.port = self.server.server_address[1]
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.daemon = True
        self.server_thread.start()
    
    def tearDown(self):
        """Tear down test server."""
        self.server.shutdown()
    
    def test_send_success(self):
        """Test successful send."""
        sender = WebhookSender()
        config = WebhookConfig(url=f"http://localhost:{self.port}/webhook")
        event = WebhookEvent(event_type="test", payload={"key": "value"})
        
        result = sender.send(event, config)
        
        self.assertTrue(result.success)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.attempts, 1)
    
    def test_send_with_secret(self):
        """Test send with signature."""
        sender = WebhookSender()
        config = WebhookConfig(
            url=f"http://localhost:{self.port}/webhook",
            secret="my-secret",
        )
        event = WebhookEvent(event_type="test", payload={"key": "value"})
        
        result = sender.send(event, config)
        
        self.assertTrue(result.success)
        
        # Check that signature header was sent
        self.assertEqual(len(TestWebhookHandler.received_requests), 1)
        headers = TestWebhookHandler.received_requests[0]['headers']
        self.assertIn('X-Webhook-Signature', headers)
    
    def test_send_custom_headers(self):
        """Test send with custom headers."""
        sender = WebhookSender()
        config = WebhookConfig(
            url=f"http://localhost:{self.port}/webhook",
            headers={"X-Custom-Header": "custom-value"},
        )
        event = WebhookEvent(event_type="test", payload={})
        
        result = sender.send(event, config)
        
        self.assertTrue(result.success)
        
        headers = TestWebhookHandler.received_requests[0]['headers']
        self.assertIn('X-Custom-Header', headers)
    
    def test_send_with_retry_on_failure(self):
        """Test retry on failure."""
        TestWebhookHandler.response_code = 500
        
        sender = WebhookSender()
        config = WebhookConfig(
            url=f"http://localhost:{self.port}/webhook",
            max_retries=2,
            retry_strategy=RetryStrategy.NONE,  # No delay for faster test
        )
        event = WebhookEvent(event_type="test", payload={})
        
        result = sender.send(event, config)
        
        self.assertFalse(result.success)
        self.assertEqual(result.attempts, 3)  # Initial + 2 retries
    
    def test_send_batch(self):
        """Test batch send."""
        sender = WebhookSender()
        config = WebhookConfig(url=f"http://localhost:{self.port}/webhook")
        
        events = [
            WebhookEvent(event_type="test1", payload={"id": 1}),
            WebhookEvent(event_type="test2", payload={"id": 2}),
        ]
        
        results = sender.send_batch(events, config)
        
        self.assertEqual(len(results), 2)
        self.assertTrue(all(r.success for r in results))
    
    def test_get_stats(self):
        """Test getting sender stats."""
        sender = WebhookSender()
        config = WebhookConfig(url=f"http://localhost:{self.port}/webhook")
        
        for i in range(3):
            event = WebhookEvent(event_type="test", payload={})
            sender.send(event, config)
        
        stats = sender.get_stats()
        
        self.assertEqual(stats['total_sent'], 3)


class TestWebhookManager(unittest.TestCase):
    """Test WebhookManager class."""
    
    def setUp(self):
        """Set up test server."""
        TestWebhookHandler.reset()
        self.server = HTTPServer(('localhost', 0), TestWebhookHandler)
        self.port = self.server.server_address[1]
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.daemon = True
        self.server_thread.start()
        
        self.manager = WebhookManager()
    
    def tearDown(self):
        """Tear down test server."""
        self.server.shutdown()
    
    def test_register_endpoint(self):
        """Test registering endpoint."""
        self.manager.register("test", WebhookConfig(url="https://example.com"))
        
        endpoints = self.manager.list_endpoints()
        self.assertIn("test", endpoints)
    
    def test_unregister_endpoint(self):
        """Test unregistering endpoint."""
        self.manager.register("test", WebhookConfig(url="https://example.com"))
        self.manager.unregister("test")
        
        endpoints = self.manager.list_endpoints()
        self.assertNotIn("test", endpoints)
    
    def test_send_to_endpoint(self):
        """Test sending to endpoint."""
        self.manager.register("test", WebhookConfig(url=f"http://localhost:{self.port}/webhook"))
        
        event = WebhookEvent(event_type="test", payload={})
        result = self.manager.send("test", event)
        
        self.assertTrue(result.success)
    
    def test_send_to_unknown_endpoint(self):
        """Test sending to unknown endpoint."""
        event = WebhookEvent(event_type="test", payload={})
        result = self.manager.send("unknown", event)
        
        self.assertFalse(result.success)
        self.assertIn("Unknown endpoint", result.error)
    
    def test_broadcast(self):
        """Test broadcasting to all endpoints."""
        self.manager.register("endpoint1", WebhookConfig(url=f"http://localhost:{self.port}/webhook"))
        self.manager.register("endpoint2", WebhookConfig(url=f"http://localhost:{self.port}/webhook"))
        
        event = WebhookEvent(event_type="test", payload={})
        results = self.manager.broadcast(event)
        
        self.assertEqual(len(results), 2)
        self.assertIn("endpoint1", results)
        self.assertIn("endpoint2", results)


class TestAsyncWebhookSender(unittest.TestCase):
    """Test AsyncWebhookSender class."""
    
    def setUp(self):
        """Set up test server."""
        TestWebhookHandler.reset()
        self.server = HTTPServer(('localhost', 0), TestWebhookHandler)
        self.port = self.server.server_address[1]
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.daemon = True
        self.server_thread.start()
    
    def tearDown(self):
        """Tear down test server."""
        self.server.shutdown()
    
    def test_send_async(self):
        """Test async send."""
        sender = AsyncWebhookSender()
        config = WebhookConfig(url=f"http://localhost:{self.port}/webhook")
        event = WebhookEvent(event_type="test", payload={})
        
        future = sender.send_async(event, config)
        result = future.result(timeout=10)
        
        self.assertTrue(result.success)
    
    def test_send_async_with_callback(self):
        """Test async send with callback."""
        callback_called = threading.Event()
        callback_result = [None]
        
        def callback(result):
            callback_result[0] = result
            callback_called.set()
        
        sender = AsyncWebhookSender()
        config = WebhookConfig(url=f"http://localhost:{self.port}/webhook")
        event = WebhookEvent(event_type="test", payload={})
        
        sender.send_async(event, config, callback=callback)
        
        callback_called.wait(timeout=10)
        
        self.assertTrue(callback_result[0].success)
    
    def test_future_done(self):
        """Test future done check."""
        sender = AsyncWebhookSender()
        config = WebhookConfig(url=f"http://localhost:{self.port}/webhook")
        event = WebhookEvent(event_type="test", payload={})
        
        future = sender.send_async(event, config)
        
        self.assertFalse(future.done())
        
        future.result(timeout=10)
        
        self.assertTrue(future.done())


class TestConvenienceFunctions(unittest.TestCase):
    """Test convenience functions."""
    
    def setUp(self):
        """Set up test server."""
        TestWebhookHandler.reset()
        self.server = HTTPServer(('localhost', 0), TestWebhookHandler)
        self.port = self.server.server_address[1]
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.daemon = True
        self.server_thread.start()
    
    def tearDown(self):
        """Tear down test server."""
        self.server.shutdown()
    
    def test_init_and_sign(self):
        """Test init_webhook and sign_payload."""
        init_webhook("test-secret")
        
        signature = sign_payload({"key": "value"})
        
        self.assertIsInstance(signature, str)
        self.assertTrue(verify_signature({"key": "value"}, signature))
    
    def test_send_webhook_function(self):
        """Test send_webhook convenience function."""
        result = send_webhook(
            url=f"http://localhost:{self.port}/webhook",
            event_type="test",
            payload={"key": "value"},
            max_retries=0,
        )
        
        self.assertTrue(result.success)
    
    def test_register_and_send_endpoint(self):
        """Test register_endpoint and send_to_endpoint."""
        register_endpoint(
            "test",
            url=f"http://localhost:{self.port}/webhook",
        )
        
        result = send_to_endpoint("test", "test.event", {"key": "value"})
        
        self.assertTrue(result.success)


class TestWebhookDecorator(unittest.TestCase):
    """Test webhook_decorator."""
    
    def setUp(self):
        """Set up test server."""
        TestWebhookHandler.reset()
        self.server = HTTPServer(('localhost', 0), TestWebhookHandler)
        self.port = self.server.server_address[1]
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.daemon = True
        self.server_thread.start()
    
    def tearDown(self):
        """Tear down test server."""
        self.server.shutdown()
    
    def test_decorator_sends_webhook(self):
        """Test that decorator sends webhook."""
        @webhook_decorator(
            event_type="user.created",
            url=f"http://localhost:{self.port}/webhook",
            max_retries=0,
        )
        def create_user(name):
            return {"id": 123, "name": name}
        
        result = create_user("Alice")
        
        # Give async send time to complete
        time.sleep(0.5)
        
        self.assertEqual(result, {"id": 123, "name": "Alice"})
        self.assertEqual(len(TestWebhookHandler.received_requests), 1)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error handling."""
    
    def test_invalid_url(self):
        """Test handling of invalid URL."""
        sender = WebhookSender()
        config = WebhookConfig(url="not-a-valid-url")
        event = WebhookEvent(event_type="test", payload={})
        
        result = sender.send(event, config)
        
        self.assertFalse(result.success)
        self.assertIsNotNone(result.error)
    
    def test_connection_refused(self):
        """Test handling of connection refused."""
        sender = WebhookSender()
        config = WebhookConfig(url="http://localhost:1", max_retries=0)  # Port 1 is closed
        event = WebhookEvent(event_type="test", payload={})
        
        result = sender.send(event, config)
        
        self.assertFalse(result.success)
    
    def test_empty_payload(self):
        """Test sending empty payload."""
        TestWebhookHandler.reset()
        server = HTTPServer(('localhost', 0), TestWebhookHandler)
        port = server.server_address[1]
        server_thread = threading.Thread(target=server.serve_forever)
        server_thread.daemon = True
        server_thread.start()
        
        try:
            sender = WebhookSender()
            config = WebhookConfig(url=f"http://localhost:{port}/webhook")
            event = WebhookEvent(event_type="test", payload={})
            
            result = sender.send(event, config)
            
            self.assertTrue(result.success)
        finally:
            server.shutdown()
    
    def test_large_payload(self):
        """Test sending large payload."""
        TestWebhookHandler.reset()
        server = HTTPServer(('localhost', 0), TestWebhookHandler)
        port = server.server_address[1]
        server_thread = threading.Thread(target=server.serve_forever)
        server_thread.daemon = True
        server_thread.start()
        
        try:
            sender = WebhookSender()
            config = WebhookConfig(url=f"http://localhost:{port}/webhook")
            
            # Create large payload
            large_data = {"data": "x" * 100000}
            event = WebhookEvent(event_type="test", payload=large_data)
            
            result = sender.send(event, config)
            
            self.assertTrue(result.success)
        finally:
            server.shutdown()
    
    def test_unicode_payload(self):
        """Test sending unicode payload."""
        TestWebhookHandler.reset()
        server = HTTPServer(('localhost', 0), TestWebhookHandler)
        port = server.server_address[1]
        server_thread = threading.Thread(target=server.serve_forever)
        server_thread.daemon = True
        server_thread.start()
        
        try:
            sender = WebhookSender()
            config = WebhookConfig(url=f"http://localhost:{port}/webhook")
            
            event = WebhookEvent(
                event_type="test",
                payload={"message": "你好世界 🌍 Привет мир"}
            )
            
            result = sender.send(event, config)
            
            self.assertTrue(result.success)
        finally:
            server.shutdown()


def run_tests():
    """Run all tests."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    test_classes = [
        TestWebhookEvent,
        TestWebhookSigner,
        TestWebhookConfig,
        TestWebhookResult,
        TestWebhookLogger,
        TestWebhookSender,
        TestWebhookManager,
        TestAsyncWebhookSender,
        TestConvenienceFunctions,
        TestWebhookDecorator,
        TestEdgeCases,
    ]
    
    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
