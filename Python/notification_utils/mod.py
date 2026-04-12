"""
AllToolkit - Python Notification Utilities

A zero-dependency, production-ready notification utility module.
Supports multiple notification channels: desktop, log, webhook, email, and console.
Features priority levels, rate limiting, batching, and notification routing.

Author: AllToolkit
License: MIT
"""

import os
import sys
import time
import socket
import hashlib
import logging
from typing import Dict, List, Optional, Callable, Any, Union
from enum import IntEnum
from dataclasses import dataclass, field
from datetime import datetime
import json


class Priority(IntEnum):
    """Notification priority levels."""
    LOW = 0
    NORMAL = 1
    HIGH = 2
    URGENT = 3
    CRITICAL = 4


class NotificationStatus(IntEnum):
    """Notification delivery status."""
    PENDING = 0
    SENT = 1
    FAILED = 2
    SKIPPED = 3
    RATE_LIMITED = 4


@dataclass
class Notification:
    """Represents a notification message."""
    title: str
    message: str
    priority: Priority = Priority.NORMAL
    channel: str = "default"
    timestamp: float = field(default_factory=time.time)
    metadata: Dict[str, Any] = field(default_factory=dict)
    status: NotificationStatus = NotificationStatus.PENDING
    error: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert notification to dictionary."""
        return {
            "title": self.title,
            "message": self.message,
            "priority": self.priority.name,
            "channel": self.channel,
            "timestamp": self.timestamp,
            "metadata": self.metadata,
            "status": self.status.name,
            "error": self.error
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Notification":
        """Create notification from dictionary."""
        return cls(
            title=data.get("title", ""),
            message=data.get("message", ""),
            priority=Priority[data.get("priority", "NORMAL")],
            channel=data.get("channel", "default"),
            timestamp=data.get("timestamp", time.time()),
            metadata=data.get("metadata", {}),
            status=NotificationStatus[data.get("status", "PENDING")],
            error=data.get("error")
        )


@dataclass
class NotificationStats:
    """Statistics for notification delivery."""
    total_sent: int = 0
    total_failed: int = 0
    total_skipped: int = 0
    total_rate_limited: int = 0
    by_channel: Dict[str, int] = field(default_factory=dict)
    by_priority: Dict[str, int] = field(default_factory=dict)
    
    def record(self, status: NotificationStatus, channel: str, priority: Priority):
        """Record a notification delivery."""
        if status == NotificationStatus.SENT:
            self.total_sent += 1
        elif status == NotificationStatus.FAILED:
            self.total_failed += 1
        elif status == NotificationStatus.SKIPPED:
            self.total_skipped += 1
        elif status == NotificationStatus.RATE_LIMITED:
            self.total_rate_limited += 1
        
        channel_key = f"{channel}_{status.name}"
        self.by_channel[channel_key] = self.by_channel.get(channel_key, 0) + 1
        
        priority_key = f"{priority.name}_{status.name}"
        self.by_priority[priority_key] = self.by_priority.get(priority_key, 0) + 1
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert stats to dictionary."""
        return {
            "total_sent": self.total_sent,
            "total_failed": self.total_failed,
            "total_skipped": self.total_skipped,
            "total_rate_limited": self.total_rate_limited,
            "success_rate": self.total_sent / max(1, self.total_sent + self.total_failed) * 100,
            "by_channel": self.by_channel,
            "by_priority": self.by_priority
        }


class RateLimiter:
    """Rate limiter for notifications."""
    
    def __init__(self, max_notifications: int = 10, window_seconds: float = 60.0):
        """
        Initialize rate limiter.
        
        Args:
            max_notifications: Maximum notifications per window
            window_seconds: Time window in seconds
        """
        self.max_notifications = max_notifications
        self.window_seconds = window_seconds
        self._timestamps: Dict[str, List[float]] = {}
    
    def is_allowed(self, key: str = "default") -> bool:
        """Check if notification is allowed under rate limit."""
        now = time.time()
        window_start = now - self.window_seconds
        
        if key not in self._timestamps:
            self._timestamps[key] = []
        
        # Remove old timestamps
        self._timestamps[key] = [ts for ts in self._timestamps[key] if ts > window_start]
        
        # Check if under limit
        if len(self._timestamps[key]) < self.max_notifications:
            self._timestamps[key].append(now)
            return True
        
        return False
    
    def get_wait_time(self, key: str = "default") -> float:
        """Get time to wait before next notification is allowed."""
        now = time.time()
        window_start = now - self.window_seconds
        
        if key not in self._timestamps:
            return 0.0
        
        valid_timestamps = [ts for ts in self._timestamps[key] if ts > window_start]
        
        if len(valid_timestamps) < self.max_notifications:
            return 0.0
        
        # Wait until oldest timestamp expires
        oldest = min(valid_timestamps)
        return max(0.0, oldest + self.window_seconds - now)
    
    def reset(self, key: str = "default"):
        """Reset rate limit for a key."""
        if key in self._timestamps:
            del self._timestamps[key]


class DesktopNotifier:
    """Cross-platform desktop notifications."""
    
    @staticmethod
    def send(title: str, message: str, urgency: str = "normal") -> bool:
        """
        Send desktop notification.
        
        Args:
            title: Notification title
            message: Notification message
            urgency: "low", "normal", or "critical"
        
        Returns:
            True if sent successfully
        """
        platform = sys.platform
        
        try:
            if platform == "linux":
                return DesktopNotifier._send_linux(title, message, urgency)
            elif platform == "darwin":
                return DesktopNotifier._send_macos(title, message)
            elif platform == "win32":
                return DesktopNotifier._send_windows(title, message)
            else:
                return DesktopNotifier._send_fallback(title, message)
        except Exception:
            return False
    
    @staticmethod
    def _send_linux(title: str, message: str, urgency: str) -> bool:
        """Send notification on Linux using notify-send."""
        import subprocess
        subprocess.Popen([
            "notify-send",
            "-u", urgency,
            title,
            message
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    
    @staticmethod
    def _send_macos(title: str, message: str) -> bool:
        """Send notification on macOS using osascript."""
        import subprocess
        script = f'''
        display notification "{message}" with title "{title}"
        '''
        subprocess.Popen([
            "osascript", "-e", script
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    
    @staticmethod
    def _send_windows(title: str, message: str) -> bool:
        """Send notification on Windows using PowerShell."""
        import subprocess
        script = f'''
        [Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] > $null
        [Windows.Data.Xml.Dom.XmlDocument, Windows.Data.Xml.Dom.XmlDocument, ContentType = WindowsRuntime] > $null
        
        $template = @"
        <toast>
            <visual>
                <binding template="ToastText02">
                    <text id="1">{title}</text>
                    <text id="2">{message}</text>
                </binding>
            </visual>
        </toast>
"@
        
        $xml = New-Object Windows.Data.Xml.Dom.XmlDocument
        $xml.LoadXml($template)
        $toast = [Windows.UI.Notifications.ToastNotification]::new($xml)
        [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier("AllToolkit").Show($toast)
        '''
        try:
            subprocess.Popen([
                "powershell", "-Command", script
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
        except Exception:
            return DesktopNotifier._send_fallback(title, message)
    
    @staticmethod
    def _send_fallback(title: str, message: str) -> bool:
        """Fallback notification using terminal bell."""
        print(f"\a🔔 {title}: {message}")
        return True


class WebhookSender:
    """Send notifications via webhooks."""
    
    @staticmethod
    def send(url: str, payload: Dict[str, Any], timeout: float = 10.0) -> bool:
        """
        Send webhook notification.
        
        Args:
            url: Webhook URL
            payload: JSON payload
            timeout: Request timeout in seconds
        
        Returns:
            True if sent successfully
        """
        try:
            import urllib.request
            import urllib.error
            
            data = json.dumps(payload).encode('utf-8')
            req = urllib.request.Request(
                url,
                data=data,
                headers={'Content-Type': 'application/json'}
            )
            
            with urllib.request.urlopen(req, timeout=timeout) as response:
                return 200 <= response.status < 300
        except Exception:
            return False
    
    @staticmethod
    def send_slack(url: str, message: str, channel: Optional[str] = None, 
                   username: str = "AllToolkit") -> bool:
        """Send Slack webhook notification."""
        payload = {
            "text": message,
            "username": username
        }
        if channel:
            payload["channel"] = channel
        return WebhookSender.send(url, payload)
    
    @staticmethod
    def send_discord(url: str, title: str, message: str, 
                     color: int = 0x0099ff) -> bool:
        """Send Discord webhook notification."""
        payload = {
            "embeds": [{
                "title": title,
                "description": message,
                "color": color,
                "timestamp": datetime.utcnow().isoformat()
            }]
        }
        return WebhookSender.send(url, payload)
    
    @staticmethod
    def send_generic(url: str, title: str, message: str, 
                     priority: Priority = Priority.NORMAL) -> bool:
        """Send generic webhook notification."""
        payload = {
            "title": title,
            "message": message,
            "priority": priority.name,
            "timestamp": datetime.utcnow().isoformat()
        }
        return WebhookSender.send(url, payload)


class EmailNotifier:
    """Send email notifications via SMTP."""
    
    def __init__(self, smtp_host: str, smtp_port: int, 
                 username: str, password: str, use_tls: bool = True):
        """
        Initialize email notifier.
        
        Args:
            smtp_host: SMTP server host
            smtp_port: SMTP server port
            username: SMTP username
            password: SMTP password
            use_tls: Use TLS connection
        """
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.username = username
        self.password = password
        self.use_tls = use_tls
    
    def send(self, to: str, subject: str, body: str, 
             from_name: Optional[str] = None, html: bool = False) -> bool:
        """
        Send email notification.
        
        Args:
            to: Recipient email address
            subject: Email subject
            body: Email body
            from_name: Sender name (optional)
            html: Is body HTML?
        
        Returns:
            True if sent successfully
        """
        try:
            import smtplib
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart
            
            sender = f"{from_name} <{self.username}>" if from_name else self.username
            
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = sender
            msg['To'] = to
            
            content_type = 'html' if html else 'plain'
            part = MIMEText(body, content_type)
            msg.attach(part)
            
            if self.use_tls:
                server = smtplib.SMTP(self.smtp_host, self.smtp_port)
                server.starttls()
            else:
                server = smtplib.SMTP_SSL(self.smtp_host, self.smtp_port)
            
            server.login(self.username, self.password)
            server.sendmail(self.username, [to], msg.as_string())
            server.quit()
            
            return True
        except Exception:
            return False


class NotificationRouter:
    """Route notifications to appropriate channels."""
    
    def __init__(self):
        """Initialize notification router."""
        self._channels: Dict[str, Callable[[Notification], bool]] = {}
        self._rate_limiters: Dict[str, RateLimiter] = {}
        self._stats = NotificationStats()
        self._default_channel = "console"
        self._quiet_hours: Optional[tuple] = None  # (start_hour, end_hour)
        self._filters: List[Callable[[Notification], bool]] = []
    
    def register_channel(self, name: str, handler: Callable[[Notification], bool],
                        rate_limit: Optional[tuple] = None):
        """
        Register a notification channel.
        
        Args:
            name: Channel name
            handler: Function that takes Notification and returns bool
            rate_limit: (max_notifications, window_seconds) tuple
        """
        self._channels[name] = handler
        if rate_limit:
            self._rate_limiters[name] = RateLimiter(rate_limit[0], rate_limit[1])
    
    def add_filter(self, filter_func: Callable[[Notification], bool]):
        """Add a filter function. Returns True to allow notification."""
        self._filters.append(filter_func)
    
    def set_quiet_hours(self, start_hour: int, end_hour: int):
        """
        Set quiet hours during which non-urgent notifications are suppressed.
        
        Args:
            start_hour: Start hour (0-23)
            end_hour: End hour (0-23)
        """
        self._quiet_hours = (start_hour, end_hour)
    
    def send(self, notification: Notification) -> NotificationStatus:
        """
        Send a notification through the appropriate channel.
        
        Args:
            notification: Notification to send
        
        Returns:
            NotificationStatus indicating result
        """
        # Apply filters
        for filter_func in self._filters:
            if not filter_func(notification):
                notification.status = NotificationStatus.SKIPPED
                self._stats.record(NotificationStatus.SKIPPED, notification.channel, 
                                  notification.priority)
                return NotificationStatus.SKIPPED
        
        # Check quiet hours
        if self._quiet_hours:
            current_hour = datetime.now().hour
            start, end = self._quiet_hours
            if start <= current_hour < end:
                if notification.priority < Priority.HIGH:
                    notification.status = NotificationStatus.SKIPPED
                    self._stats.record(NotificationStatus.SKIPPED, notification.channel,
                                      notification.priority)
                    return NotificationStatus.SKIPPED
        
        # Check rate limit
        channel = notification.channel or self._default_channel
        if channel in self._rate_limiters:
            if not self._rate_limiters[channel].is_allowed():
                notification.status = NotificationStatus.RATE_LIMITED
                notification.error = f"Rate limited for channel {channel}"
                self._stats.record(NotificationStatus.RATE_LIMITED, channel,
                                  notification.priority)
                return NotificationStatus.RATE_LIMITED
        
        # Send through channel
        handler = self._channels.get(channel, self._channels.get("console"))
        if handler:
            try:
                success = handler(notification)
                if success:
                    notification.status = NotificationStatus.SENT
                else:
                    notification.status = NotificationStatus.FAILED
                    notification.error = "Handler returned False"
            except Exception as e:
                notification.status = NotificationStatus.FAILED
                notification.error = str(e)
        else:
            notification.status = NotificationStatus.FAILED
            notification.error = f"Unknown channel: {channel}"
        
        self._stats.record(notification.status, channel, notification.priority)
        return notification.status
    
    def send_batch(self, notifications: List[Notification]) -> List[NotificationStatus]:
        """Send multiple notifications."""
        return [self.send(n) for n in notifications]
    
    def get_stats(self) -> NotificationStats:
        """Get notification statistics."""
        return self._stats
    
    def reset_stats(self):
        """Reset statistics."""
        self._stats = NotificationStats()


class NotificationUtils:
    """
    Main notification utility class.
    
    Provides a simple interface for sending notifications through
    various channels with built-in rate limiting and routing.
    """
    
    _default_router: Optional[NotificationRouter] = None
    
    @classmethod
    def get_router(cls) -> NotificationRouter:
        """Get or create default router."""
        if cls._default_router is None:
            cls._default_router = NotificationRouter()
            cls._setup_default_channels(cls._default_router)
        return cls._default_router
    
    @classmethod
    def _setup_default_channels(cls, router: NotificationRouter):
        """Setup default notification channels."""
        # Console channel
        def console_handler(n: Notification) -> bool:
            emoji = {
                Priority.LOW: "📝",
                Priority.NORMAL: "📢",
                Priority.HIGH: "⚠️",
                Priority.URGENT: "🚨",
                Priority.CRITICAL: "🔴"
            }.get(n.priority, "📢")
            
            timestamp = datetime.fromtimestamp(n.timestamp).strftime("%H:%M:%S")
            print(f"[{timestamp}] {emoji} [{n.priority.name}] {n.title}: {n.message}")
            return True
        
        router.register_channel("console", console_handler)
        
        # Desktop channel
        def desktop_handler(n: Notification) -> bool:
            urgency = {
                Priority.LOW: "low",
                Priority.NORMAL: "normal",
                Priority.HIGH: "normal",
                Priority.URGENT: "critical",
                Priority.CRITICAL: "critical"
            }.get(n.priority, "normal")
            return DesktopNotifier.send(n.title, n.message, urgency)
        
        router.register_channel("desktop", desktop_handler, rate_limit=(5, 60))
        
        # Log channel
        def log_handler(n: Notification) -> bool:
            level = {
                Priority.LOW: logging.DEBUG,
                Priority.NORMAL: logging.INFO,
                Priority.HIGH: logging.WARNING,
                Priority.URGENT: logging.ERROR,
                Priority.CRITICAL: logging.CRITICAL
            }.get(n.priority, logging.INFO)
            
            logging.log(level, f"[{n.priority.name}] {n.title}: {n.message}")
            return True
        
        router.register_channel("log", log_handler)
    
    @staticmethod
    def notify(title: str, message: str, priority: Priority = Priority.NORMAL,
               channel: str = "console", metadata: Optional[Dict] = None) -> NotificationStatus:
        """
        Send a notification.
        
        Args:
            title: Notification title
            message: Notification message
            priority: Notification priority
            channel: Target channel
            metadata: Additional metadata
        
        Returns:
            NotificationStatus indicating result
        """
        notification = Notification(
            title=title,
            message=message,
            priority=priority,
            channel=channel,
            metadata=metadata or {}
        )
        
        router = NotificationUtils.get_router()
        return router.send(notification)
    
    @staticmethod
    def notify_desktop(title: str, message: str, 
                      priority: Priority = Priority.NORMAL) -> bool:
        """Send desktop notification."""
        return DesktopNotifier.send(title, message, 
                                   "critical" if priority >= Priority.HIGH else "normal")
    
    @staticmethod
    def notify_webhook(url: str, title: str, message: str,
                      priority: Priority = Priority.NORMAL) -> bool:
        """Send webhook notification."""
        return WebhookSender.send_generic(url, title, message, priority)
    
    @staticmethod
    def notify_slack(url: str, message: str, channel: Optional[str] = None) -> bool:
        """Send Slack notification."""
        return WebhookSender.send_slack(url, message, channel)
    
    @staticmethod
    def notify_discord(url: str, title: str, message: str,
                      priority: Priority = Priority.NORMAL) -> bool:
        """Send Discord notification."""
        colors = {
            Priority.LOW: 0x808080,
            Priority.NORMAL: 0x0099ff,
            Priority.HIGH: 0xffaa00,
            Priority.URGENT: 0xff4500,
            Priority.CRITICAL: 0xff0000
        }
        color = colors.get(priority, 0x0099ff)
        return WebhookSender.send_discord(url, title, message, color)
    
    @staticmethod
    def create_email_notifier(smtp_host: str, smtp_port: int,
                             username: str, password: str,
                             use_tls: bool = True) -> EmailNotifier:
        """Create an email notifier."""
        return EmailNotifier(smtp_host, smtp_port, username, password, use_tls)
    
    @staticmethod
    def register_channel(name: str, handler: Callable[[Notification], bool],
                        rate_limit: Optional[tuple] = None):
        """Register a custom notification channel."""
        router = NotificationUtils.get_router()
        router.register_channel(name, handler, rate_limit)
    
    @staticmethod
    def set_quiet_hours(start_hour: int, end_hour: int):
        """Set quiet hours for non-urgent notifications."""
        router = NotificationUtils.get_router()
        router.set_quiet_hours(start_hour, end_hour)
    
    @staticmethod
    def get_stats() -> Dict[str, Any]:
        """Get notification statistics."""
        router = NotificationUtils.get_router()
        return router.get_stats().to_dict()
    
    @staticmethod
    def reset_stats():
        """Reset notification statistics."""
        router = NotificationUtils.get_router()
        router.reset_stats()


# Convenience functions
def notify(title: str, message: str, priority: Priority = Priority.NORMAL,
           channel: str = "console") -> NotificationStatus:
    """Send a notification."""
    return NotificationUtils.notify(title, message, priority, channel)


def notify_desktop(title: str, message: str, 
                  priority: Priority = Priority.NORMAL) -> bool:
    """Send desktop notification."""
    return NotificationUtils.notify_desktop(title, message, priority)


def notify_webhook(url: str, title: str, message: str,
                  priority: Priority = Priority.NORMAL) -> bool:
    """Send webhook notification."""
    return NotificationUtils.notify_webhook(url, title, message, priority)


def notify_slack(url: str, message: str, channel: Optional[str] = None) -> bool:
    """Send Slack notification."""
    return NotificationUtils.notify_slack(url, message, channel)


def notify_discord(url: str, title: str, message: str,
                  priority: Priority = Priority.NORMAL) -> bool:
    """Send Discord notification."""
    return NotificationUtils.notify_discord(url, title, message, priority)


# Module exports
__all__ = [
    # Classes
    "Notification",
    "NotificationStatus", 
    "NotificationStats",
    "Priority",
    "RateLimiter",
    "DesktopNotifier",
    "WebhookSender",
    "EmailNotifier",
    "NotificationRouter",
    "NotificationUtils",
    
    # Convenience functions
    "notify",
    "notify_desktop",
    "notify_webhook",
    "notify_slack",
    "notify_discord",
]
