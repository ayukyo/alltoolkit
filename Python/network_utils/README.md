# AllToolkit - Network Utilities Module (Python)

A comprehensive network utility module for Python with **zero external dependencies**.

## Features

### URL Utilities
- URL validation and parsing
- URL building from components
- URL extraction from text
- URL normalization

### IPv4 Address Utilities
- IP validation
- IP ↔ Integer conversion
- Network/broadcast address calculation
- CIDR notation conversion
- IP range checking
- Private/loopback IP detection

### IPv6 Address Utilities
- IPv6 validation
- Address compression (:: shorthand)
- Address expansion (full form)

### Port Utilities
- Port validation
- Common service name lookup
- Port categorization (well-known/registered/dynamic)

### MAC Address Utilities
- MAC validation (colon and dash formats)
- MAC normalization
- MAC generation
- OUI extraction

### HTTP Utilities
- Content-Type parsing
- HTTP status line parsing
- Status code categorization

### Domain Utilities
- Domain validation
- Domain extraction from URLs
- Base domain extraction
- Subdomain checking

### Network Diagnostics
- Hostname resolution
- Reachability testing
- Local hostname detection

### Utility Functions
- Bytes ↔ Human-readable conversion
- Bandwidth formatting
- Transfer time calculation

## Installation

No installation required! Just copy the module to your project:

```bash
cp network_utils/mod.py your_project/
```

## Quick Start

```python
from network_utils.mod import (
    is_valid_url, parse_url, build_url,
    is_valid_ipv4, ip_to_int, int_to_ip,
    is_valid_ipv6, compress_ipv6,
    is_valid_port, get_service_name,
    is_valid_mac, normalize_mac,
    bytes_to_human, human_to_bytes
)

# URL validation
is_valid_url("https://example.com")  # True

# Parse URL
parse_url("https://api.example.com:8080/v1/users?format=json")
# {'scheme': 'https', 'domain': 'api.example.com', 'port': 8080, ...}

# Build URL
build_url("https", "example.com", "/path", port=443, query_params={"key": "value"})
# 'https://example.com:443/path?key=value'

# IP validation
is_valid_ipv4("192.168.1.1")  # True
is_valid_ipv4("256.1.1.1")    # False

# IP conversion
ip_to_int("192.168.1.1")  # 3232235777
int_to_ip(3232235777)     # '192.168.1.1'

# Network calculation
get_network_address("192.168.1.100", "255.255.255.0")   # '192.168.1.0'
get_broadcast_address("192.168.1.100", "255.255.255.0") # '192.168.1.255'

# CIDR conversion
cidr_to_netmask(24)   # '255.255.255.0'
netmask_to_cidr("255.255.255.0")  # 24

# IPv6 compression
compress_ipv6("2001:0db8:0000:0000:0000:0000:0000:0001")
# '2001:db8::1'

# Port utilities
get_service_name(80)    # 'HTTP'
get_service_name(443)   # 'HTTPS'
categorize_port(80)     # 'well-known'
categorize_port(8080)   # 'registered'

# MAC utilities
is_valid_mac("00:1A:2B:3C:4D:5E")  # True
normalize_mac("00-1A-2B-3C-4D-5E", ":")  # '00:1A:2B:3C:4D:5E'
generate_mac()  # Random MAC address

# Domain utilities
is_valid_domain("example.com")  # True
extract_domain("https://www.example.com/path")  # 'www.example.com'
is_subdomain("www.example.com", "example.com")  # True

# HTTP utilities
parse_content_type("application/json; charset=utf-8")
# {'type': 'application', 'subtype': 'json', 'charset': 'utf-8'}
is_json_content_type("application/json")  # True

# Utility functions
bytes_to_human(1572864)      # '1.50 MB'
human_to_bytes("1.5 MB")     # 1572864
format_bandwidth(1500000)    # '1.50 Mbps'
calculate_transfer_time(1048576, 1000000)
# {'seconds': 8.39, 'formatted': '8.39 seconds'}
```

## API Reference

### URL Functions

| Function | Description |
|----------|-------------|
| `is_valid_url(url)` | Validate URL format |
| `parse_url(url)` | Parse URL into components |
| `build_url(scheme, domain, ...)` | Build URL from components |
| `extract_urls(text)` | Extract all URLs from text |
| `normalize_url(url)` | Normalize URL (add scheme, lowercase) |

### IPv4 Functions

| Function | Description |
|----------|-------------|
| `is_valid_ipv4(ip)` | Validate IPv4 address |
| `ip_to_int(ip)` | Convert IP to integer |
| `int_to_ip(num)` | Convert integer to IP |
| `ip_in_range(ip, start, end)` | Check if IP in range |
| `get_network_address(ip, netmask)` | Calculate network address |
| `get_broadcast_address(ip, netmask)` | Calculate broadcast address |
| `cidr_to_netmask(cidr)` | Convert CIDR to netmask |
| `netmask_to_cidr(netmask)` | Convert netmask to CIDR |
| `is_private_ip(ip)` | Check if private IP |
| `is_loopback_ip(ip)` | Check if loopback IP |

### IPv6 Functions

| Function | Description |
|----------|-------------|
| `is_valid_ipv6(ip)` | Validate IPv6 address |
| `compress_ipv6(ip)` | Compress IPv6 (:: shorthand) |
| `expand_ipv6(ip)` | Expand IPv6 to full form |

### Port Functions

| Function | Description |
|----------|-------------|
| `is_valid_port(port)` | Validate port number |
| `get_service_name(port)` | Get service name for port |
| `categorize_port(port)` | Categorize port |

### MAC Functions

| Function | Description |
|----------|-------------|
| `is_valid_mac(mac)` | Validate MAC address |
| `normalize_mac(mac, sep)` | Normalize MAC format |
| `generate_mac()` | Generate random MAC |
| `get_mac_oui(mac)` | Extract OUI from MAC |

### HTTP Functions

| Function | Description |
|----------|-------------|
| `parse_content_type(ct)` | Parse Content-Type header |
| `is_json_content_type(ct)` | Check if JSON content type |
| `is_html_content_type(ct)` | Check if HTML content type |
| `parse_http_status(line)` | Parse HTTP status line |
| `is_success_status(code)` | Check 2xx status |
| `is_server_error_status(code)` | Check 5xx status |

### Domain Functions

| Function | Description |
|----------|-------------|
| `is_valid_domain(domain)` | Validate domain name |
| `extract_domain(url)` | Extract domain from URL |
| `get_base_domain(domain)` | Get base domain |
| `is_subdomain(child, parent)` | Check subdomain relationship |

### Utility Functions

| Function | Description |
|----------|-------------|
| `bytes_to_human(size)` | Convert bytes to readable format |
| `human_to_bytes(str)` | Convert readable format to bytes |
| `format_bandwidth(bps)` | Format bandwidth |
| `calculate_transfer_time(size, bw)` | Calculate transfer time |

## Running Tests

```bash
cd network_utils
python network_utils_test.py
```

## Running Examples

```bash
cd network_utils/examples
python usage_examples.py
```

## License

MIT License - See main AllToolkit LICENSE file.

## Contributing

See main AllToolkit CONTRIBUTING.md for guidelines.
