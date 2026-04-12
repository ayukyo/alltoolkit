#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AllToolkit - HTTP Utilities Module

Comprehensive HTTP utilities for Python with zero external dependencies.
Provides HTTP client, simple server, request/response helpers, URL parsing,
header manipulation, and more.

Author: AllToolkit
License: MIT
Version: 1.0.0
"""

import urllib.request
import urllib.error
import urllib.parse
import http.server
import socketserver
import socket
import json
import ssl
import base64
import mimetypes
import threading
import time
import logging
from typing import Optional, Dict, Any, List, Tuple, Union, Callable
from dataclasses import dataclass, field
from enum import Enum
from contextlib import contextmanager
from urllib.parse import urlparse, parse_qs, urlencode, urljoin
from http import HTTPStatus

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# =============================================================================
# Type Aliases
# =============================================================================

Headers = Dict[str, str]
QueryParams = Dict[str, Union[str, List[str]]]
RequestBody = Union[str, bytes, Dict[str, Any], None]
HTTPMethod = str


# =============================================================================
# Constants
# =============================================================================

DEFAULT_TIMEOUT = 30.0
DEFAULT_USER_AGENT = "AllToolkit-HTTP/1.0"
MAX_REDIRECTS = 5
DEFAULT_BUFFER_SIZE = 8192


# =============================================================================
# Enums
# =============================================================================

class Method(Enum):
    """HTTP methods."""
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"


class ContentType(Enum):
    """Common content types."""
    JSON = "application/json"
    HTML = "text/html"
    TEXT = "text/plain"
    XML = "application/xml"
    FORM = "application/x-www-form-urlencoded"
    MULTIPART = "multipart/form-data"
    OCTET_STREAM = "application/octet-stream"


# =============================================================================
# Data Classes
# =============================================================================

@dataclass
class HTTPRequest:
    """Represents an HTTP request."""
    method: str = "GET"
    url: str = ""
    headers: Dict[str, str] = field(default_factory=dict)
    body: Optional[bytes] = None
    timeout: float = DEFAULT_TIMEOUT
    follow_redirects: bool = True
    max_redirects: int = MAX_REDIRECTS
    verify_ssl: bool = True
    
    def __post_init__(self):
        if not self.headers.get("User-Agent"):
            self.headers["User-Agent"] = DEFAULT_USER_AGENT


@dataclass
class HTTPResponse:
    """Represents an HTTP response."""
    status_code: int = 0
    status_text: str = ""
    headers: Dict[str, str] = field(default_factory=dict)
    body: bytes = b""
    url: str = ""
    elapsed_time: float = 0.0
    redirect_count: int = 0
    
    @property
    def ok(self) -> bool:
        """Check if response status is successful (2xx)."""
        return 200 <= self.status_code < 300
    
    @property
    def is_redirect(self) -> bool:
        """Check if response is a redirect (3xx)."""
        return 300 <= self.status_code < 400
    
    @property
    def is_error(self) -> bool:
        """Check if response is an error (4xx or 5xx)."""
        return self.status_code >= 400
    
    def text(self, encoding: str = "utf-8") -> str:
        """Get response body as text."""
        return self.body.decode(encoding, errors="replace")
    
    def json(self) -> Any:
        """Parse response body as JSON."""
        return json.loads(self.body.decode("utf-8"))
    
    def __repr__(self) -> str:
        return f"HTTPResponse(status={self.status_code}, url={self.url})"


@dataclass
class ServerConfig:
    """Configuration for HTTP server."""
    host: str = "localhost"
    port: int = 8080
    timeout: float = DEFAULT_TIMEOUT
    ssl_enabled: bool = False
    ssl_certfile: Optional[str] = None
    ssl_keyfile: Optional[str] = None
    request_handler: Optional[Callable] = None
    static_dir: Optional[str] = None
    cors_enabled: bool = False
    allowed_origins: List[str] = field(default_factory=lambda: ["*"])


@dataclass
class RequestInfo:
    """Parsed request information for handlers."""
    method: str
    path: str
    query: Dict[str, List[str]]
    headers: Dict[str, str]
    body: bytes
    client_address: Tuple[str, int]
    cookies: Dict[str, str] = field(default_factory=dict)
    
    @classmethod
    def from_handler(cls, handler: http.server.BaseHTTPRequestHandler) -> 'RequestInfo':
        """Create RequestInfo from HTTP handler."""
        parsed = urlparse(handler.path)
        query = parse_qs(parsed.query)
        
        # Parse cookies
        cookies = {}
        cookie_header = handler.headers.get("Cookie", "")
        if cookie_header:
            for cookie in cookie_header.split(";"):
                if "=" in cookie:
                    key, value = cookie.split("=", 1)
                    cookies[key.strip()] = value.strip()
        
        # Read body
        content_length = int(handler.headers.get("Content-Length", 0))
        body = handler.rfile.read(content_length) if content_length > 0 else b""
        
        return cls(
            method=handler.command,
            path=parsed.path,
            query=query,
            headers=dict(handler.headers),
            body=body,
            client_address=handler.client_address,
            cookies=cookies
        )


# =============================================================================
# HTTP Client
# =============================================================================

class HTTPClient:
    """High-level HTTP client with zero dependencies."""
    
    def __init__(self, base_url: str = "", default_headers: Optional[Headers] = None,
                 timeout: float = DEFAULT_TIMEOUT, verify_ssl: bool = True):
        self.base_url = base_url.rstrip("/")
        self.default_headers = default_headers or {}
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        self.session = urllib.request.OpenerDirector()
        self._setup_handlers()
    
    def _setup_handlers(self):
        """Setup URL handlers for the session."""
        self.session.add_handler(urllib.request.HTTPHandler())
        self.session.add_handler(urllib.request.HTTPSHandler(
            context=ssl.create_default_context() if self.verify_ssl else None
        ))
        self.session.add_handler(urllib.request.HTTPRedirectHandler())
        self.session.add_handler(urllib.request.HTTPCookieProcessor())
        self.session.add_handler(urllib.request.HTTPErrorProcessor())
    
    def _build_url(self, path: str) -> str:
        """Build full URL from base and path."""
        if path.startswith("http://") or path.startswith("https://"):
            return path
        if self.base_url:
            return f"{self.base_url}/{path.lstrip('/')}"
        return path
    
    def _create_request(self, method: str, url: str, headers: Optional[Headers] = None,
                        data: Optional[bytes] = None) -> urllib.request.Request:
        """Create urllib request object."""
        full_url = self._build_url(url)
        merged_headers = {**self.default_headers, **(headers or {})}
        
        req = urllib.request.Request(full_url, data=data, method=method)
        for key, value in merged_headers.items():
            req.add_header(key, value)
        
        return req
    
    def request(self, method: str, url: str, headers: Optional[Headers] = None,
                data: Optional[RequestBody] = None, timeout: Optional[float] = None,
                json_data: Optional[Dict] = None, params: Optional[QueryParams] = None) -> HTTPResponse:
        """Send HTTP request and return response."""
        start_time = time.time()
        
        # Build URL with query params
        if params:
            url = f"{url}?{urlencode(params, doseq=True)}"
        
        # Prepare body
        body_data = None
        if json_data is not None:
            body_data = json.dumps(json_data).encode("utf-8")
            if not headers:
                headers = {}
            headers["Content-Type"] = ContentType.JSON.value
        elif isinstance(data, dict):
            body_data = urlencode(data).encode("utf-8")
            if not headers:
                headers = {}
            headers["Content-Type"] = ContentType.FORM.value
        elif isinstance(data, str):
            body_data = data.encode("utf-8")
        elif isinstance(data, bytes):
            body_data = data
        
        req = self._create_request(method, url, headers, body_data)
        
        try:
            response = self.session.open(req, timeout=timeout or self.timeout)
            elapsed = time.time() - start_time
            result = HTTPResponse(
                status_code=response.status,
                status_text=response.reason,
                headers=dict(response.headers),
                body=response.read(),
                url=response.url,
                elapsed_time=elapsed
            )
            response.close()
            return result
        except urllib.error.HTTPError as e:
            elapsed = time.time() - start_time
            return HTTPResponse(
                status_code=e.code,
                status_text=e.reason,
                headers=dict(e.headers),
                body=e.read(),
                url=e.url,
                elapsed_time=elapsed
            )
        except urllib.error.URLError as e:
            elapsed = time.time() - start_time
            return HTTPResponse(
                status_code=0,
                status_text=str(e.reason),
                body=b"",
                elapsed_time=elapsed
            )
        except socket.timeout:
            elapsed = time.time() - start_time
            return HTTPResponse(
                status_code=0,
                status_text="Request timed out",
                body=b"",
                elapsed_time=elapsed
            )
    
    def get(self, url: str, **kwargs) -> HTTPResponse:
        """Send GET request."""
        return self.request("GET", url, **kwargs)
    
    def post(self, url: str, **kwargs) -> HTTPResponse:
        """Send POST request."""
        return self.request("POST", url, **kwargs)
    
    def put(self, url: str, **kwargs) -> HTTPResponse:
        """Send PUT request."""
        return self.request("PUT", url, **kwargs)
    
    def delete(self, url: str, **kwargs) -> HTTPResponse:
        """Send DELETE request."""
        return self.request("DELETE", url, **kwargs)
    
    def patch(self, url: str, **kwargs) -> HTTPResponse:
        """Send PATCH request."""
        return self.request("PATCH", url, **kwargs)
    
    def head(self, url: str, **kwargs) -> HTTPResponse:
        """Send HEAD request."""
        return self.request("HEAD", url, **kwargs)
    
    def options(self, url: str, **kwargs) -> HTTPResponse:
        """Send OPTIONS request."""
        return self.request("OPTIONS", url, **kwargs)


# =============================================================================
# HTTP Server
# =============================================================================

class BaseRequestHandler(http.server.BaseHTTPRequestHandler):
    """Base request handler with helper methods."""
    
    server_config: ServerConfig = None
    
    def log_message(self, format: str, *args):
        """Override to use our logger."""
        logger.info("%s - %s", self.client_address[0], format % args)
    
    def _send_cors_headers(self):
        """Send CORS headers if enabled."""
        if self.server_config and self.server_config.cors_enabled:
            origin = self.headers.get("Origin", "*")
            if "*" in self.server_config.allowed_origins or origin in self.server_config.allowed_origins:
                self.send_header("Access-Control-Allow-Origin", origin)
                self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, PATCH, OPTIONS")
                self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
    
    def send_json_response(self, data: Any, status: int = 200, headers: Optional[Headers] = None):
        """Send JSON response."""
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", ContentType.JSON.value)
        self.send_header("Content-Length", str(len(body)))
        self._send_cors_headers()
        if headers:
            for key, value in headers.items():
                self.send_header(key, value)
        self.end_headers()
        self.wfile.write(body)
    
    def send_text_response(self, text: str, status: int = 200, 
                          content_type: str = ContentType.TEXT.value):
        """Send text response."""
        body = text.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self._send_cors_headers()
        self.end_headers()
        self.wfile.write(body)
    
    def send_html_response(self, html: str, status: int = 200):
        """Send HTML response."""
        self.send_text_response(html, status, ContentType.HTML.value)
    
    def send_file_response(self, file_path: str, status: int = 200):
        """Send file response with appropriate content type."""
        try:
            with open(file_path, "rb") as f:
                content = f.read()
            
            content_type, _ = mimetypes.guess_type(file_path)
            if not content_type:
                content_type = ContentType.OCTET_STREAM.value
            
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(content)))
            self._send_cors_headers()
            self.end_headers()
            self.wfile.write(content)
        except FileNotFoundError:
            self.send_error(404, "File not found")
    
    def get_request_info(self) -> RequestInfo:
        """Get parsed request information."""
        return RequestInfo.from_handler(self)
    
    def do_OPTIONS(self):
        """Handle OPTIONS request for CORS preflight."""
        self.send_response(200)
        self._send_cors_headers()
        self.end_headers()


class ThreadedHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    """Thread-per-request HTTP server."""
    daemon_threads = True
    allow_reuse_address = True


class HTTPServer:
    """Simple HTTP server with routing support."""
    
    def __init__(self, config: Optional[ServerConfig] = None):
        self.config = config or ServerConfig()
        self.routes: Dict[str, Dict[str, Callable]] = {}
        self._server: Optional[ThreadedHTTPServer] = None
        self._server_thread: Optional[threading.Thread] = None
    
    def route(self, path: str, methods: Optional[List[str]] = None):
        """Decorator to register route handler."""
        if methods is None:
            methods = ["GET"]
        
        def decorator(func: Callable) -> Callable:
            if path not in self.routes:
                self.routes[path] = {}
            for method in methods:
                self.routes[path][method.upper()] = func
            return func
        return decorator
    
    def _create_handler(self) -> type:
        """Create request handler class with access to server."""
        server = self
        
        class Handler(BaseRequestHandler):
            server_config = server.config
            
            def _handle_request(self, method: str):
                request_info = self.get_request_info()
                
                # Check routes
                handler_func = None
                if request_info.path in server.routes:
                    handler_func = server.routes[request_info.path].get(method)
                
                if handler_func:
                    try:
                        response = handler_func(request_info)
                        if isinstance(response, dict):
                            self.send_json_response(response)
                        elif isinstance(response, str):
                            self.send_text_response(response)
                        elif isinstance(response, tuple):
                            status, body = response
                            if isinstance(body, dict):
                                self.send_json_response(body, status)
                            else:
                                self.send_text_response(str(body), status)
                    except Exception as e:
                        logger.exception("Handler error")
                        self.send_json_response({"error": str(e)}, 500)
                else:
                    self.send_error(404, "Not Found")
            
            def do_GET(self):
                self._handle_request("GET")
            
            def do_POST(self):
                self._handle_request("POST")
            
            def do_PUT(self):
                self._handle_request("PUT")
            
            def do_DELETE(self):
                self._handle_request("DELETE")
            
            def do_PATCH(self):
                self._handle_request("PATCH")
            
            def do_HEAD(self):
                self._handle_request("HEAD")
            
            def do_OPTIONS(self):
                super().do_OPTIONS()
        
        return Handler
    
    def start(self, blocking: bool = True):
        """Start the HTTP server."""
        handler = self._create_handler()
        self._server = ThreadedHTTPServer((self.config.host, self.config.port), handler)
        
        protocol = "https" if self.config.ssl_enabled else "http"
        logger.info(f"Server starting on {protocol}://{self.config.host}:{self.config.port}")
        
        if self.config.ssl_enabled and self.config.ssl_certfile:
            self._server.socket = ssl.wrap_socket(
                self._server.socket,
                certfile=self.config.ssl_certfile,
                keyfile=self.config.ssl_keyfile,
                server_side=True
            )
        
        if blocking:
            self._server.serve_forever()
        else:
            self._server_thread = threading.Thread(target=self._server.serve_forever)
            self._server_thread.daemon = True
            self._server_thread.start()
    
    def stop(self):
        """Stop the HTTP server."""
        if self._server:
            self._server.shutdown()
            self._server.server_close()
            logger.info("Server stopped")


# =============================================================================
# URL Utilities
# =============================================================================

def parse_url(url: str) -> Dict[str, Any]:
    """Parse URL into components."""
    parsed = urlparse(url)
    return {
        "scheme": parsed.scheme,
        "netloc": parsed.netloc,
        "path": parsed.path,
        "params": parsed.params,
        "query": parsed.query,
        "fragment": parsed.fragment,
        "username": parsed.username,
        "password": parsed.password,
        "hostname": parsed.hostname,
        "port": parsed.port
    }


def build_url(scheme: str, hostname: str, path: str = "", port: Optional[int] = None,
              params: Optional[QueryParams] = None, fragment: str = "") -> str:
    """Build URL from components."""
    netloc = hostname
    if port:
        netloc = f"{hostname}:{port}"
    
    url = f"{scheme}://{netloc}/{path.lstrip('/')}"
    
    if params:
        url += f"?{urlencode(params, doseq=True)}"
    
    if fragment:
        url += f"#{fragment}"
    
    return url


def encode_query_params(params: QueryParams) -> str:
    """Encode query parameters to URL string."""
    return urlencode(params, doseq=True)


def decode_query_params(query_string: str) -> Dict[str, List[str]]:
    """Decode query string to dictionary."""
    return parse_qs(query_string)


def url_encode(text: str) -> str:
    """URL encode a string."""
    return urllib.parse.quote(text)


def url_decode(text: str) -> str:
    """URL decode a string."""
    return urllib.parse.unquote(text)


def is_valid_url(url: str) -> bool:
    """Check if URL is valid."""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


def get_domain(url: str) -> str:
    """Extract domain from URL."""
    parsed = urlparse(url)
    return parsed.netloc or parsed.path.split("/")[0]


def normalize_url(url: str) -> str:
    """Normalize URL (add scheme if missing, etc.)."""
    if not url.startswith(("http://", "https://")):
        url = f"http://{url}"
    parsed = urlparse(url)
    return parsed.geturl()


# =============================================================================
# Header Utilities
# =============================================================================

def parse_headers(header_string: str) -> Headers:
    """Parse raw header string to dictionary."""
    headers = {}
    for line in header_string.strip().split("\r\n"):
        if ": " in line:
            key, value = line.split(": ", 1)
            headers[key] = value
    return headers


def format_headers(headers: Headers) -> str:
    """Format headers dictionary to raw string."""
    return "\r\n".join(f"{key}: {value}" for key, value in headers.items())


def get_content_type(filename: str) -> str:
    """Get content type for filename extension."""
    content_type, _ = mimetypes.guess_type(filename)
    return content_type or ContentType.OCTET_STREAM.value


def create_basic_auth_header(username: str, password: str) -> str:
    """Create Basic Auth header value."""
    credentials = f"{username}:{password}"
    encoded = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")
    return f"Basic {encoded}"


def parse_auth_header(auth_header: str) -> Optional[Tuple[str, str]]:
    """Parse Authorization header to (type, credentials)."""
    if " " in auth_header:
        parts = auth_header.split(" ", 1)
        return parts[0], parts[1]
    return None


# =============================================================================
# Cookie Utilities
# =============================================================================

def parse_cookies(cookie_header: str) -> Dict[str, str]:
    """Parse Cookie header to dictionary."""
    cookies = {}
    for cookie in cookie_header.split(";"):
        if "=" in cookie:
            key, value = cookie.split("=", 1)
            cookies[key.strip()] = value.strip()
    return cookies


def format_cookies(cookies: Dict[str, str]) -> str:
    """Format cookies dictionary to Cookie header value."""
    return "; ".join(f"{key}={value}" for key, value in cookies.items())


def create_cookie(name: str, value: str, expires: Optional[str] = None,
                  path: str = "/", domain: str = "", secure: bool = False,
                  httponly: bool = False) -> str:
    """Create Set-Cookie header value."""
    parts = [f"{name}={value}"]
    if expires:
        parts.append(f"Expires={expires}")
    if path:
        parts.append(f"Path={path}")
    if domain:
        parts.append(f"Domain={domain}")
    if secure:
        parts.append("Secure")
    if httponly:
        parts.append("HttpOnly")
    return "; ".join(parts)


# =============================================================================
# Convenience Functions
# =============================================================================

def get(url: str, **kwargs) -> HTTPResponse:
    """Send GET request (convenience function)."""
    client = HTTPClient()
    return client.get(url, **kwargs)


def post(url: str, **kwargs) -> HTTPResponse:
    """Send POST request (convenience function)."""
    client = HTTPClient()
    return client.post(url, **kwargs)


def put(url: str, **kwargs) -> HTTPResponse:
    """Send PUT request (convenience function)."""
    client = HTTPClient()
    return client.put(url, **kwargs)


def delete(url: str, **kwargs) -> HTTPResponse:
    """Send DELETE request (convenience function)."""
    client = HTTPClient()
    return client.delete(url, **kwargs)


def download_file(url: str, save_path: str, chunk_size: int = DEFAULT_BUFFER_SIZE) -> bool:
    """Download file from URL to local path."""
    try:
        with urllib.request.urlopen(url) as response, open(save_path, "wb") as out_file:
            while True:
                chunk = response.read(chunk_size)
                if not chunk:
                    break
                out_file.write(chunk)
        return True
    except Exception as e:
        logger.error(f"Download failed: {e}")
        return False


def fetch_json(url: str, **kwargs) -> Any:
    """Fetch and parse JSON from URL."""
    response = get(url, **kwargs)
    if response.ok:
        return response.json()
    raise ValueError(f"HTTP {response.status_code}: {response.text()}")


def check_url_status(url: str, timeout: float = 5.0) -> int:
    """Quick check URL status code."""
    try:
        response = get(url, timeout=timeout)
        return response.status_code
    except Exception:
        return 0


# =============================================================================
# Version and Features
# =============================================================================

def version() -> str:
    """Return module version."""
    return "1.0.0"


def features() -> List[str]:
    """Return list of available features."""
    return [
        "HTTPClient - Full-featured HTTP client",
        "HTTPServer - Simple HTTP server with routing",
        "URL Utilities - Parse, build, encode, decode URLs",
        "Header Utilities - Parse and format HTTP headers",
        "Cookie Utilities - Parse, format, create cookies",
        "JSON Support - Automatic JSON serialization/deserialization",
        "SSL/TLS Support - Secure HTTP connections",
        "File Download - Download files from URLs",
        "CORS Support - Cross-origin request handling",
        "Threaded Server - Handle multiple requests concurrently"
    ]


# =============================================================================
# CLI Interface
# =============================================================================

if __name__ == "__main__":
    import sys
    
    print(f"AllToolkit HTTP Utils v{version()}")
    print("Features:")
    for feature in features():
        print(f"  - {feature}")
    
    if len(sys.argv) > 1:
        url = sys.argv[1]
        print(f"\nChecking URL: {url}")
        status = check_url_status(url)
        print(f"Status Code: {status}")
        
        if status == 200:
            response = get(url)
            print(f"Content-Type: {response.headers.get('Content-Type', 'Unknown')}")
            print(f"Content Length: {len(response.body)} bytes")
