"""
AllToolkit - Python Webhook Utilities

A zero-dependency, production-ready webhook utility module.
Supports sending webhooks with retry, HMAC signature verification, and async support.

Author: AllToolkit
License: MIT
"""

import json
import time
import hmac
import hashlib
import threading
import urllib.request
import urllib.error
from typing import Optional, Dict, List, Any, Callable, TypeVar, Union
from dataclasses import dataclass, field
from collections import deque
from functools import wraps
from contextlib import contextmanager
from datetime import datetime
from enum import Enum
import base64
import ssl


T = TypeVar('T')


class WebhookError(Exception):
    """Base exception for webhook errors."""
    pass


class WebhookSendError(WebhookError):
    """Error sending webhook."""
    pass


class WebhookVerificationError(WebhookError):
    """Error verifying webhook signature."""
    pass


class RetryStrategy(Enum):
    """Retry strategy for failed webhooks."""
    NONE = "none"
    FIXED = "fixed"
    EXPONENTIAL = "exponential"
    LINEAR = "linear"


@dataclass
class WebhookConfig:
    """Configuration for a webhook endpoint."""
    url: str
    secret: Optional[str] = None
    headers: Dict[str, str] = field(default_factory=dict)
    timeout: float = 30.0
    max_retries: int = 3
    retry_strategy: RetryStrategy = RetryStrategy.EXPONENTIAL
    retry_delay: float = 1.0
    verify_ssl: bool = True
    
    def __post_init__(self):
        if not self.url:
            raise ValueError("Webhook URL is required")
        if self.max_retries < 0:
            raise ValueError("Max retries must be non-negative")
        if self.retry_delay <= 0:
            raise ValueError("Retry delay must be positive")


@dataclass
class WebhookResult:
    """Result of a webhook send operation."""
    success: bool
    status_code: Optional[int] = None
    response_body: Optional[str] = None
    error: Optional[str] = None
    attempts: int = 1
    duration_ms: float = 0.0
    url: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'success': self.success,
            'status_code': self.status_code,
            'response_body': self.response_body,
            'error': self.error,
            'attempts': self.attempts,
            'duration_ms': self.duration_ms,
            'url': self.url,
        }
    
    def __bool__(self) -> bool:
        return self.success


@dataclass
class WebhookEvent:
    """A webhook event to be sent."""
    event_type: str
    payload: Dict[str, Any]
    id: Optional[str] = None
    timestamp: Optional[float] = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = time.time()
        if self.id is None:
            self.id = f"wh_{int(self.timestamp * 1000)}_{id(self)}"
    
    def to_json(self) -> str:
        """Convert event to JSON string."""
        return json.dumps({
            'id': self.id,
            'type': self.event_type,
            'timestamp': self.timestamp,
            'data': self.payload,
        }, separators=(',', ':'))


class WebhookSigner:
    """
    HMAC-based webhook signature generator and verifier.
    
    Example:
        signer = WebhookSigner("my-secret-key")
        
        # Sign a payload
        signature = signer.sign('{"event": "user.created"}')
        
        # Verify a signature
        is_valid = signer.verify('{"event": "user.created"}', signature)
    """
    
    def __init__(self, secret: str, algorithm: str = "sha256"):
        """
        Initialize signer.
        
        Args:
            secret: Secret key for HMAC
            algorithm: Hash algorithm (sha256, sha512, md5)
        """
        if not secret:
            raise ValueError("Secret key is required")
        
        self._secret = secret.encode('utf-8')
        self._algorithm = algorithm
    
    @property
    def algorithm(self) -> str:
        """Get hash algorithm."""
        return self._algorithm
    
    def sign(self, payload: Union[str, bytes, Dict]) -> str:
        """
        Sign a payload.
        
        Args:
            payload: Data to sign (string, bytes, or dict)
        
        Returns:
            Hex-encoded signature
        """
        if isinstance(payload, dict):
            payload = json.dumps(payload, separators=(',', ':'), sort_keys=True)
        if isinstance(payload, str):
            payload = payload.encode('utf-8')
        
        signature = hmac.new(self._secret, payload, self._algorithm).hexdigest()
        return signature
    
    def sign_base64(self, payload: Union[str, bytes, Dict]) -> str:
        """
        Sign a payload and return base64-encoded signature.
        
        Args:
            payload: Data to sign
        
        Returns:
            Base64-encoded signature
        """
        if isinstance(payload, dict):
            payload = json.dumps(payload, separators=(',', ':'), sort_keys=True)
        if isinstance(payload, str):
            payload = payload.encode('utf-8')
        
        signature = hmac.new(self._secret, payload, self._algorithm).digest()
        return base64.b64encode(signature).decode('utf-8')
    
    def verify(self, payload: Union[str, bytes, Dict], signature: str) -> bool:
        """
        Verify a signature.
        
        Args:
            payload: Original data
            signature: Signature to verify
        
        Returns:
            True if signature is valid
        """
        expected = self.sign(payload)
        return hmac.compare_digest(expected, signature)
    
    def verify_base64(self, payload: Union[str, bytes, Dict], signature: str) -> bool:
        """
        Verify a base64-encoded signature.
        
        Args:
            payload: Original data
            signature: Base64-encoded signature to verify
        
        Returns:
            True if signature is valid
        """
        try:
            expected = self.sign_base64(payload)
            return hmac.compare_digest(expected, signature)
        except Exception:
            return False
    
    def get_signature_header(self, payload: Union[str, bytes, Dict], 
                            header_name: str = "X-Webhook-Signature") -> Dict[str, str]:
        """
        Get signature ready for HTTP headers.
        
        Args:
            payload: Data to sign
            header_name: Name of the signature header
        
        Returns:
            Dictionary with signature header
        """
        signature = self.sign(payload)
        return {
            header_name: f"{self._algorithm}={signature}",
        }


class WebhookLogger:
    """
    In-memory webhook event logger.
    
    Example:
        logger = WebhookLogger(max_events=1000)
        
        # Log events
        logger.log_success(result)
        logger.log_error(error, payload)
        
        # Get statistics
        stats = logger.get_stats()
        
        # Get recent events
        events = logger.get_recent(limit=10)
    """
    
    def __init__(self, max_events: int = 1000):
        """
        Initialize logger.
        
        Args:
            max_events: Maximum events to keep in memory
        """
        self._max_events = max_events
        self._events: deque = deque(maxlen=max_events)
        self._lock = threading.Lock()
        self._stats = {
            'total_sent': 0,
            'total_success': 0,
            'total_failed': 0,
            'total_retries': 0,
        }
    
    def log_success(self, result: WebhookResult, event: Optional[WebhookEvent] = None):
        """Log successful webhook send."""
        with self._lock:
            self._stats['total_sent'] += 1
            self._stats['total_success'] += 1
            self._stats['total_retries'] += result.attempts - 1
            
            self._events.append({
                'type': 'success',
                'timestamp': time.time(),
                'event_id': event.id if event else None,
                'event_type': event.event_type if event else None,
                'url': result.url,
                'status_code': result.status_code,
                'duration_ms': result.duration_ms,
                'attempts': result.attempts,
            })
    
    def log_error(self, error: str, event: Optional[WebhookEvent] = None,
                  url: str = "", attempts: int = 1):
        """Log failed webhook send."""
        with self._lock:
            self._stats['total_sent'] += 1
            self._stats['total_failed'] += 1
            self._stats['total_retries'] += attempts - 1
            
            self._events.append({
                'type': 'error',
                'timestamp': time.time(),
                'event_id': event.id if event else None,
                'event_type': event.event_type if event else None,
                'url': url,
                'error': error,
                'attempts': attempts,
            })
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics."""
        with self._lock:
            stats = self._stats.copy()
            stats['success_rate'] = (
                stats['total_success'] / stats['total_sent'] 
                if stats['total_sent'] > 0 else 0.0
            )
            return stats
    
    def get_recent(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent events."""
        with self._lock:
            return list(self._events)[-limit:]
    
    def clear(self):
        """Clear all logged events."""
        with self._lock:
            self._events.clear()
            self._stats = {
                'total_sent': 0,
                'total_success': 0,
                'total_failed': 0,
                'total_retries': 0,
            }


class WebhookSender:
    """
    Webhook sender with retry support.
    
    Example:
        sender = WebhookSender()
        
        config = WebhookConfig(
            url="https://example.com/webhook",
            secret="my-secret",
            max_retries=3,
        )
        
        event = WebhookEvent(
            event_type="user.created",
            payload={"user_id": 123, "email": "test@example.com"},
        )
        
        result = sender.send(event, config)
        if result.success:
            print("Webhook sent successfully!")
    """
    
    def __init__(self, logger: Optional[WebhookLogger] = None):
        """
        Initialize sender.
        
        Args:
            logger: Optional logger for tracking sends
        """
        self._logger = logger or WebhookLogger()
        self._default_timeout = 30.0
    
    def _calculate_retry_delay(self, attempt: int, config: WebhookConfig) -> float:
        """Calculate delay before retry."""
        if config.retry_strategy == RetryStrategy.NONE:
            return 0
        elif config.retry_strategy == RetryStrategy.FIXED:
            return config.retry_delay
        elif config.retry_strategy == RetryStrategy.LINEAR:
            return config.retry_delay * attempt
        elif config.retry_strategy == RetryStrategy.EXPONENTIAL:
            return config.retry_delay * (2 ** (attempt - 1))
        return config.retry_delay
    
    def _create_request(self, event: WebhookEvent, config: WebhookConfig) -> urllib.request.Request:
        """Create HTTP request."""
        payload = event.to_json().encode('utf-8')
        
        headers = {
            'Content-Type': 'application/json',
            'Content-Length': str(len(payload)),
            'User-Agent': 'AllToolkit-Webhook/1.0',
            'X-Webhook-Event': event.event_type,
            'X-Webhook-ID': event.id,
            'X-Webhook-Timestamp': str(int(event.timestamp)),
        }
        
        # Add signature if secret is provided
        if config.secret:
            signer = WebhookSigner(config.secret)
            sig_headers = signer.get_signature_header(payload)
            headers.update(sig_headers)
        
        # Add custom headers
        headers.update(config.headers)
        
        req = urllib.request.Request(
            config.url,
            data=payload,
            headers=headers,
            method='POST',
        )
        
        return req
    
    def _send_request(self, req: urllib.request.Request, config: WebhookConfig) -> tuple:
        """Send HTTP request and return (status_code, body, error)."""
        try:
            # Create SSL context
            if config.verify_ssl:
                context = ssl.create_default_context()
            else:
                context = ssl.create_default_context()
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE
            
            opener = urllib.request.build_opener(
                urllib.request.HTTPSHandler(context=context)
            )
            
            start_time = time.time()
            with opener.open(req, timeout=config.timeout) as response:
                body = response.read().decode('utf-8', errors='replace')
                duration_ms = (time.time() - start_time) * 1000
                return response.status, body, None, duration_ms
                
        except urllib.error.HTTPError as e:
            duration_ms = (time.time() - start_time) * 1000 if 'start_time' in locals() else 0
            try:
                body = e.read().decode('utf-8', errors='replace')
            except Exception:
                body = None
            return e.code, body, str(e), duration_ms
            
        except urllib.error.URLError as e:
            duration_ms = (time.time() - start_time) * 1000 if 'start_time' in locals() else 0
            return None, None, f"Connection error: {e.reason}", duration_ms
            
        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000 if 'start_time' in locals() else 0
            return None, None, str(e), duration_ms
    
    def send(self, event: WebhookEvent, config: WebhookConfig) -> WebhookResult:
        """
        Send a webhook event.
        
        Args:
            event: Event to send
            config: Webhook configuration
        
        Returns:
            Result of the send operation
        """
        last_error = None
        attempts = 0
        status_code = None
        body = None
        duration_ms = 0.0
        
        for attempt in range(config.max_retries + 1):
            attempts = attempt + 1
            try:
                req = self._create_request(event, config)
                status_code, body, error, duration_ms = self._send_request(req, config)
            except Exception as e:
                error = str(e)
                status_code = None
                body = None
            
            if error is None and status_code and 200 <= status_code < 300:
                result = WebhookResult(
                    success=True,
                    status_code=status_code,
                    response_body=body,
                    attempts=attempts,
                    duration_ms=duration_ms,
                    url=config.url,
                )
                self._logger.log_success(result, event)
                return result
            
            last_error = error or f"HTTP {status_code}"
            
            # Retry if not the last attempt
            if attempt < config.max_retries:
                delay = self._calculate_retry_delay(attempt + 1, config)
                if delay > 0:
                    time.sleep(delay)
        
        result = WebhookResult(
            success=False,
            status_code=status_code,
            response_body=body,
            error=last_error,
            attempts=attempts,
            duration_ms=duration_ms,
            url=config.url,
        )
        self._logger.log_error(last_error, event, config.url, attempts)
        return result
    
    def send_batch(self, events: List[WebhookEvent], config: WebhookConfig) -> List[WebhookResult]:
        """
        Send multiple webhook events.
        
        Args:
            events: List of events to send
            config: Webhook configuration
        
        Returns:
            List of results for each event
        """
        results = []
        for event in events:
            result = self.send(event, config)
            results.append(result)
        return results
    
    def get_stats(self) -> Dict[str, Any]:
        """Get send statistics."""
        return self._logger.get_stats()
    
    def get_recent_events(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent webhook events."""
        return self._logger.get_recent(limit)


class WebhookManager:
    """
    Manage multiple webhook endpoints.
    
    Example:
        manager = WebhookManager()
        
        # Register endpoints
        manager.register("slack", WebhookConfig(
            url="https://hooks.slack.com/services/xxx",
        ))
        manager.register("discord", WebhookConfig(
            url="https://discord.com/api/webhooks/xxx",
        ))
        
        # Send to specific endpoint
        event = WebhookEvent("alert", {"message": "Server down!"})
        result = manager.send("slack", event)
        
        # Send to all endpoints
        results = manager.broadcast(event)
    """
    
    def __init__(self):
        """Initialize manager."""
        self._endpoints: Dict[str, WebhookConfig] = {}
        self._sender = WebhookSender()
        self._lock = threading.Lock()
    
    def register(self, name: str, config: WebhookConfig):
        """
        Register a webhook endpoint.
        
        Args:
            name: Endpoint name
            config: Endpoint configuration
        """
        with self._lock:
            self._endpoints[name] = config
    
    def unregister(self, name: str):
        """
        Unregister a webhook endpoint.
        
        Args:
            name: Endpoint name
        """
        with self._lock:
            self._endpoints.pop(name, None)
    
    def get_endpoint(self, name: str) -> Optional[WebhookConfig]:
        """
        Get endpoint configuration.
        
        Args:
            name: Endpoint name
        
        Returns:
            Configuration or None if not found
        """
        with self._lock:
            return self._endpoints.get(name)
    
    def list_endpoints(self) -> List[str]:
        """List registered endpoint names."""
        with self._lock:
            return list(self._endpoints.keys())
    
    def send(self, name: str, event: WebhookEvent) -> WebhookResult:
        """
        Send event to a specific endpoint.
        
        Args:
            name: Endpoint name
            event: Event to send
        
        Returns:
            Result of the send operation
        """
        config = self.get_endpoint(name)
        if not config:
            return WebhookResult(
                success=False,
                error=f"Unknown endpoint: {name}",
                url="",
            )
        return self._sender.send(event, config)
    
    def broadcast(self, event: WebhookEvent) -> Dict[str, WebhookResult]:
        """
        Broadcast event to all registered endpoints.
        
        Args:
            event: Event to send
        
        Returns:
            Dictionary mapping endpoint names to results
        """
        results = {}
        with self._lock:
            endpoints = list(self._endpoints.items())
        
        for name, config in endpoints:
            results[name] = self._sender.send(event, config)
        
        return results
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics for all endpoints."""
        return self._sender.get_stats()


# Convenience functions

_default_manager = WebhookManager()
_default_signer: Optional[WebhookSigner] = None


def init_webhook(secret: str, algorithm: str = "sha256"):
    """Initialize default webhook signer."""
    global _default_signer
    _default_signer = WebhookSigner(secret, algorithm)


def sign_payload(payload: Union[str, bytes, Dict]) -> str:
    """Sign a payload using the default signer."""
    if not _default_signer:
        raise WebhookError("Webhook signer not initialized. Call init_webhook() first.")
    return _default_signer.sign(payload)


def verify_signature(payload: Union[str, bytes, Dict], signature: str) -> bool:
    """Verify a signature using the default signer."""
    if not _default_signer:
        raise WebhookError("Webhook signer not initialized. Call init_webhook() first.")
    return _default_signer.verify(payload, signature)


def send_webhook(url: str, event_type: str, payload: Dict[str, Any],
                secret: Optional[str] = None, **kwargs) -> WebhookResult:
    """
    Send a webhook with default settings.
    
    Args:
        url: Webhook URL
        event_type: Type of event
        payload: Event payload
        secret: Optional signing secret
        **kwargs: Additional config options
    
    Returns:
        Result of the send operation
    """
    config = WebhookConfig(url=url, secret=secret, **kwargs)
    event = WebhookEvent(event_type=event_type, payload=payload)
    sender = WebhookSender()
    return sender.send(event, config)


def register_endpoint(name: str, url: str, secret: Optional[str] = None, **kwargs):
    """Register an endpoint with the default manager."""
    config = WebhookConfig(url=url, secret=secret, **kwargs)
    _default_manager.register(name, config)


def send_to_endpoint(name: str, event_type: str, payload: Dict[str, Any]) -> WebhookResult:
    """Send event to a registered endpoint."""
    event = WebhookEvent(event_type=event_type, payload=payload)
    return _default_manager.send(name, event)


def broadcast_event(event_type: str, payload: Dict[str, Any]) -> Dict[str, WebhookResult]:
    """Broadcast event to all registered endpoints."""
    event = WebhookEvent(event_type=event_type, payload=payload)
    return _default_manager.broadcast(event)


# Decorator for automatic webhook sending

def webhook_decorator(event_type: str, url: str, secret: Optional[str] = None,
                     payload_fn: Optional[Callable] = None, **config_kwargs):
    """
    Decorator to automatically send webhooks when a function is called.
    
    Args:
        event_type: Type of event
        url: Webhook URL
        secret: Optional signing secret
        payload_fn: Function to transform return value to payload
        **config_kwargs: Additional config options
    
    Example:
        @webhook_decorator(
            event_type="user.created",
            url="https://example.com/webhook",
            payload_fn=lambda result: {"user_id": result["id"]},
        )
        def create_user(name, email):
            # Create user logic
            return {"id": 123, "name": name, "email": email}
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Call the original function
            result = func(*args, **kwargs)
            
            # Prepare payload
            if payload_fn:
                payload = payload_fn(result)
            elif isinstance(result, dict):
                payload = result
            else:
                payload = {"result": result}
            
            # Send webhook (non-blocking)
            config = WebhookConfig(url=url, secret=secret, **config_kwargs)
            event = WebhookEvent(event_type=event_type, payload=payload)
            sender = WebhookSender()
            
            # Send in background thread to not block
            thread = threading.Thread(target=sender.send, args=(event, config))
            thread.daemon = True
            thread.start()
            
            return result
        
        return wrapper
    return decorator


# Async support (using threads for compatibility)

class AsyncWebhookSender:
    """
    Async webhook sender using background threads.
    
    Example:
        sender = AsyncWebhookSender()
        
        # Send without blocking
        future = sender.send_async(event, config)
        
        # Wait for result if needed
        result = future.result(timeout=30)
        
        # Or use callback
        def on_complete(result):
            if result.success:
                print("Sent!")
        
        sender.send_async(event, config, callback=on_complete)
    """
    
    def __init__(self, max_workers: int = 10):
        """
        Initialize async sender.
        
        Args:
            max_workers: Maximum concurrent sends
        """
        self._max_workers = max_workers
        self._semaphore = threading.Semaphore(max_workers)
        self._sender = WebhookSender()
    
    def send_async(self, event: WebhookEvent, config: WebhookConfig,
                   callback: Optional[Callable[[WebhookResult], None]] = None) -> 'WebhookFuture':
        """
        Send webhook asynchronously.
        
        Args:
            event: Event to send
            config: Configuration
            callback: Optional callback for when complete
        
        Returns:
            Future object to get result
        """
        future = WebhookFuture()
        
        def worker():
            try:
                result = self._sender.send(event, config)
                future._set_result(result)
                if callback:
                    try:
                        callback(result)
                    except Exception:
                        pass  # Ignore callback errors
            except Exception as e:
                future._set_exception(e)
            finally:
                self._semaphore.release()
        
        self._semaphore.acquire()
        thread = threading.Thread(target=worker)
        thread.daemon = True
        thread.start()
        
        return future


class WebhookFuture:
    """Future object for async webhook operations."""
    
    def __init__(self):
        self._result: Optional[WebhookResult] = None
        self._exception: Optional[Exception] = None
        self._event = threading.Event()
    
    def _set_result(self, result: WebhookResult):
        self._result = result
        self._event.set()
    
    def _set_exception(self, exc: Exception):
        self._exception = exc
        self._event.set()
    
    def result(self, timeout: Optional[float] = None) -> WebhookResult:
        """
        Get result, waiting if necessary.
        
        Args:
            timeout: Maximum time to wait
        
        Returns:
            WebhookResult
        
        Raises:
            Exception: If send failed
        """
        if not self._event.wait(timeout):
            raise TimeoutError("Webhook send timed out")
        
        if self._exception:
            raise self._exception
        
        return self._result
    
    def done(self) -> bool:
        """Check if operation is complete."""
        return self._event.is_set()
