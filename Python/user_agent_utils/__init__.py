"""
User-Agent 解析和生成工具
========================

零外部依赖的 User-Agent 解析器，支持：
- 解析 User-Agent 字符串，提取浏览器、操作系统、设备信息
- 生成常见 User-Agent 字符串
- 设备类型检测（桌面、移动、平板、爬虫）
- 浏览器和操作系统版本提取
"""

from mod import (
    UserAgentParser,
    UserAgentGenerator,
    UserAgentResult,
    BrowserInfo,
    OSInfo,
    DeviceInfo,
    DeviceType,
    parse,
    generate,
    is_bot,
    is_mobile,
    get_browser_name,
    get_os_name,
    get_device_type,
    COMMON_USER_AGENTS,
)

__all__ = [
    'UserAgentParser',
    'UserAgentGenerator',
    'UserAgentResult',
    'BrowserInfo',
    'OSInfo',
    'DeviceInfo',
    'DeviceType',
    'parse',
    'generate',
    'is_bot',
    'is_mobile',
    'get_browser_name',
    'get_os_name',
    'get_device_type',
    'COMMON_USER_AGENTS',
]

__version__ = '1.0.0'