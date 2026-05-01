"""
User-Agent 解析和生成工具
========================

零外部依赖的 User-Agent 解析器，支持：
- 解析 User-Agent 字符串，提取浏览器、操作系统、设备信息
- 生成常见 User-Agent 字符串
- 设备类型检测（桌面、移动、平板、爬虫）
- 浏览器和操作系统版本提取

作者: AllToolkit
日期: 2026-05-02
"""

import re
from dataclasses import dataclass
from typing import Optional, List, Dict
from enum import Enum


class DeviceType(Enum):
    """设备类型枚举"""
    DESKTOP = "desktop"
    MOBILE = "mobile"
    TABLET = "tablet"
    TV = "tv"
    BOT = "bot"
    UNKNOWN = "unknown"


@dataclass
class BrowserInfo:
    """浏览器信息"""
    name: str
    version: Optional[str] = None
    engine: Optional[str] = None
    engine_version: Optional[str] = None


@dataclass
class OSInfo:
    """操作系统信息"""
    name: str
    version: Optional[str] = None
    architecture: Optional[str] = None


@dataclass
class DeviceInfo:
    """设备信息"""
    type: DeviceType
    brand: Optional[str] = None
    model: Optional[str] = None


@dataclass
class UserAgentResult:
    """User-Agent 解析结果"""
    original: str
    browser: Optional[BrowserInfo] = None
    os: Optional[OSInfo] = None
    device: Optional[DeviceInfo] = None
    is_bot: bool = False
    is_mobile: bool = False


def _get_windows_version(nt_version: str) -> str:
    """将 Windows NT 版本转换为友好名称"""
    version_map = {
        '10.0': '10/11',
        '6.3': '8.1',
        '6.2': '8',
        '6.1': '7',
        '6.0': 'Vista',
        '5.1': 'XP',
        '5.2': 'Server 2003',
        '5.0': '2000',
    }
    return version_map.get(nt_version, nt_version)


def _extract_version(pattern: str, ua_string: str) -> Optional[str]:
    """从字符串中提取版本号"""
    match = re.search(pattern, ua_string)
    return match.group(1) if match else None


# 浏览器识别规则（按优先级排序）
BROWSER_PATTERNS = [
    # 特殊浏览器优先
    (r'Edg(e|A|iOS)?/(\d+\.\d+\.\d+\.\d+|\d+\.\d+)', 'Edge', 'Edg'),
    (r'CriOS/(\d+\.\d+\.\d+\.\d+|\d+\.\d+)', 'Chrome', 'Blink'),
    (r'FxiOS/(\d+\.\d+)', 'Firefox', 'Blink'),
    (r'Opera Mini/(\d+\.\d+)', 'Opera Mini', 'Presto'),
    (r'Opera Tablet/(\d+\.\d+)', 'Opera Tablet', 'Presto'),
    (r'OPR/(\d+\.\d+\.\d+\.\d+|\d+\.\d+)', 'Opera', 'Blink'),
    (r'Opera/(\d+\.\d+)', 'Opera', 'Presto'),
    (r'Vivaldi/(\d+\.\d+\.\d+\.\d+|\d+\.\d+)', 'Vivaldi', 'Blink'),
    (r'Brave/(\d+\.\d+\.\d+\.\d+|\d+\.\d+)', 'Brave', 'Blink'),
    (r'YaBrowser/(\d+\.\d+\.\d+\.\d+|\d+\.\d+)', 'Yandex', 'Blink'),
    (r'SamsungBrowser/(\d+\.\d+)', 'Samsung Internet', 'Blink'),
    (r'UCBrowser/(\d+\.\d+\.\d+\.\d+|\d+\.\d+)', 'UC Browser', 'Blink'),
    (r'QQBrowser/(\d+\.\d+\.\d+\.\d+|\d+\.\d+)', 'QQ Browser', 'Blink'),
    (r'Quark/(\d+\.\d+\.\d+\.\d+|\d+\.\d+)', 'Quark', 'Blink'),
    (r'Whale/(\d+\.\d+\.\d+\.\d+|\d+\.\d+)', 'Whale', 'Blink'),
    (r'Maxthon/(\d+\.\d+)', 'Maxthon', 'Blink'),
    (r'Sleipnir/(\d+\.\d+)', 'Sleipnir', 'Blink'),
    # 主流浏览器
    (r'Chrome/(\d+\.\d+\.\d+\.\d+|\d+\.\d+)', 'Chrome', 'Blink'),
    (r'Chromium/(\d+\.\d+\.\d+\.\d+|\d+\.\d+)', 'Chromium', 'Blink'),
    (r'Firefox/(\d+\.\d+)', 'Firefox', 'Gecko'),
    (r'Safari/(\d+\.\d+)', 'Safari', 'WebKit'),
    (r'MSIE (\d+\.\d+)', 'Internet Explorer', 'Trident'),
    (r'Trident/.*rv:(\d+\.\d+)', 'Internet Explorer', 'Trident'),
    # 移动端浏览器
    (r'Mobile Safari/(\d+\.\d+)', 'Mobile Safari', 'WebKit'),
    (r'Android.*Chrome/(\d+\.\d+\.\d+\.\d+|\d+\.\d+)', 'Chrome Mobile', 'Blink'),
    (r'Version/(\d+\.\d+).*Safari', 'Safari', 'WebKit'),
]

# 引擎版本提取规则
ENGINE_VERSION_PATTERNS = [
    (r'AppleWebKit/(\d+\.?\d*)', 'WebKit'),
    (r'Gecko/(\d+)', 'Gecko'),
    (r'Presto/(\d+\.?\d*)', 'Presto'),
    (r'Trident/(\d+\.?\d*)', 'Trident'),
    (r'Blink', 'Blink'),
]

# 操作系统识别规则（按优先级排序，特殊系统优先）
OS_PATTERNS = [
    (r'Windows NT (\d+\.\d+)', 'Windows', _get_windows_version),
    (r'Windows Phone OS? (\d+\.\d+)', 'Windows Phone', lambda v: v),
    (r'Android (\d+(\.\d+)?)', 'Android', lambda v: v),
    (r'iPhone OS (\d+_\d+(_\d+)?)', 'iOS', lambda v: v.replace('_', '.')),
    (r'iPad.*OS (\d+_\d+(_\d+)?)', 'iOS', lambda v: v.replace('_', '.')),
    (r'Mac OS X (\d+[._]\d+([._]\d+)?)', 'macOS', lambda v: v.replace('_', '.')),
    (r'CrOS (\d+\.\d+\.\d+)', 'Chrome OS', lambda v: v),
    (r'Ubuntu(?:/(\d+\.\d+\.\d+)?)?', 'Ubuntu', lambda v: v or ''),
    (r'Fedora/(\d+)', 'Fedora', lambda v: v),
    (r'FreeBSD (\d+\.\d+)', 'FreeBSD', lambda v: v),
    (r'OpenBSD (\d+\.\d+)', 'OpenBSD', lambda v: v),
    (r'Linux(?: (\d+\.\d+\.\d+)?)?', 'Linux', lambda v: v or ''),
]

# 爬虫识别规则
BOT_PATTERNS = [
    r'Googlebot',
    r'Bingbot',
    r'Slurp',
    r'DuckDuckBot',
    r'Baiduspider',
    r'YandexBot',
    r'Sogou',
    r'Exabot',
    r'facebot',
    r'facebookexternalhit',
    r'Twitterbot',
    r'LinkedInBot',
    r'Pinterest',
    r'applebot',
    r'SemrushBot',
    r'AhrefsBot',
    r'MJ12bot',
    r'DotBot',
    r'PetalBot',
    r'Bytespider',
    r'crawler',
    r'spider',
    r'bot(?!(?i:cent))',
    r'scraper',
    r'crawling',
]

# 移动设备品牌和型号
MOBILE_DEVICES = [
    (r'iPhone(?: (\d+,\d+))?', 'Apple', 'iPhone'),
    (r'iPad(?: Pro)?(?: (\d+,\d+))?', 'Apple', 'iPad'),
    (r'Samsung SM-([A-Za-z0-9]+)', 'Samsung', 'Galaxy'),
    (r'Samsung', 'Samsung', None),
    (r'Pixel(?: (\d+))?', 'Google', 'Pixel'),
    (r'Nexus(?: (\d+|[A-Za-z]+))?', 'Google', 'Nexus'),
    (r'OnePlus(?: ([A-Za-z0-9]+))?', 'OnePlus', None),
    (r'Xiaomi', 'Xiaomi', None),
    (r'Redmi', 'Xiaomi', 'Redmi'),
    (r'Huawei', 'Huawei', None),
    (r'Honor', 'Huawei', 'Honor'),
    (r'OPPO', 'OPPO', None),
    (r'vivo', 'vivo', None),
    (r'Motorola', 'Motorola', None),
    (r'LG', 'LG', None),
    (r'Sony', 'Sony', None),
    (r'HTC', 'HTC', None),
    (r'Nokia', 'Nokia', None),
]


class UserAgentParser:
    """User-Agent 解析器"""
    
    def __init__(self):
        pass
    
    def parse(self, user_agent: str) -> UserAgentResult:
        """
        解析 User-Agent 字符串
        
        Args:
            user_agent: User-Agent 字符串
            
        Returns:
            UserAgentResult 对象，包含解析后的信息
        """
        result = UserAgentResult(original=user_agent)
        
        # 检测是否为爬虫
        result.is_bot = self._is_bot(user_agent)
        if result.is_bot:
            result.device = DeviceInfo(type=DeviceType.BOT)
        
        # 解析浏览器信息
        result.browser = self._parse_browser(user_agent)
        
        # 解析操作系统信息
        result.os = self._parse_os(user_agent)
        
        # 解析设备信息
        result.device = self._parse_device(user_agent, result.is_bot)
        
        # 设置移动端标志
        result.is_mobile = result.device.type in (DeviceType.MOBILE, DeviceType.TABLET)
        
        return result
    
    def _is_bot(self, user_agent: str) -> bool:
        """检测是否为爬虫"""
        ua_lower = user_agent.lower()
        for pattern in BOT_PATTERNS:
            if re.search(pattern, user_agent, re.IGNORECASE):
                # 进一步确认不是误判
                if 'bot' in ua_lower or 'crawler' in ua_lower or 'spider' in ua_lower:
                    return True
                # 检查是否在已知爬虫列表中
                known_bots = ['googlebot', 'bingbot', 'slurp', 'duckduckbot', 
                             'baiduspider', 'yandexbot', 'facebook', 'twitter']
                if any(bot in ua_lower for bot in known_bots):
                    return True
        return False
    
    def _parse_browser(self, user_agent: str) -> Optional[BrowserInfo]:
        """解析浏览器信息"""
        for pattern, name, engine in BROWSER_PATTERNS:
            match = re.search(pattern, user_agent)
            if match:
                # 获取最后一个捕获组的值作为版本
                version = match.group(match.lastindex) if match.lastindex else None
                
                # 获取引擎版本
                engine_version = None
                for eng_pattern, eng_name in ENGINE_VERSION_PATTERNS:
                    eng_match = re.search(eng_pattern, user_agent)
                    if eng_match:
                        engine = eng_name
                        if eng_match.lastindex:
                            engine_version = eng_match.group(1)
                        break
                
                return BrowserInfo(
                    name=name,
                    version=version,
                    engine=engine,
                    engine_version=engine_version
                )
        return None
    
    def _parse_os(self, user_agent: str) -> Optional[OSInfo]:
        """解析操作系统信息"""
        for pattern, name, version_func in OS_PATTERNS:
            match = re.search(pattern, user_agent, re.IGNORECASE)
            if match:
                version = match.group(1) if match.lastindex else None
                version = version_func(version) if version else None
                
                # 检测架构
                arch = None
                if 'x86_64' in user_agent or 'x64' in user_agent or 'Win64' in user_agent:
                    arch = 'x64'
                elif 'i686' in user_agent or 'i386' in user_agent:
                    arch = 'x86'
                elif 'ARM' in user_agent or 'arm' in user_agent:
                    arch = 'ARM'
                elif 'aarch64' in user_agent:
                    arch = 'ARM64'
                
                return OSInfo(
                    name=name,
                    version=version,
                    architecture=arch
                )
        return None
    
    def _parse_device(self, user_agent: str, is_bot: bool) -> DeviceInfo:
        """解析设备信息"""
        if is_bot:
            return DeviceInfo(type=DeviceType.BOT)
        
        # 检测平板
        tablet_indicators = ['iPad', 'Tablet', 'PlayBook', 'Silk', 'Kindle']
        if any(indicator in user_agent for indicator in tablet_indicators):
            device_type = DeviceType.TABLET
        # 检测移动设备
        elif any(m in user_agent for m in ['Mobile', 'Android', 'iPhone', 'iPod', 'Phone']):
            device_type = DeviceType.MOBILE
        # 检测智能电视
        elif any(tv in user_agent for tv in ['SmartTV', 'TV', 'Netflix', 'Roku', 'AppleTV']):
            device_type = DeviceType.TV
        else:
            device_type = DeviceType.DESKTOP
        
        # 提取设备品牌和型号
        brand = None
        model = None
        for pattern, b, m in MOBILE_DEVICES:
            if re.search(pattern, user_agent, re.IGNORECASE):
                brand = b
                model = m
                break
        
        return DeviceInfo(type=device_type, brand=brand, model=model)


class UserAgentGenerator:
    """User-Agent 生成器"""
    
    # Chrome 版本库
    CHROME_VERSIONS = ['120.0.0.0', '119.0.0.0', '118.0.0.0', '117.0.0.0', '116.0.0.0']
    
    # Firefox 版本库
    FIREFOX_VERSIONS = ['121.0', '120.0', '119.0', '118.0', '117.0']
    
    # Safari 版本库
    SAFARI_VERSIONS = ['17.2', '17.1', '17.0', '16.6', '16.5']
    
    # Edge 版本库
    EDGE_VERSIONS = ['120.0.0.0', '119.0.0.0', '118.0.0.0']
    
    # WebKit 版本
    WEBKIT_VERSION = '605.1.15'
    
    @classmethod
    def chrome_desktop(cls, version: Optional[str] = None) -> str:
        """生成 Chrome 桌面版 User-Agent"""
        v = version or cls.CHROME_VERSIONS[0]
        return f'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{v} Safari/537.36'
    
    @classmethod
    def chrome_mac(cls, version: Optional[str] = None) -> str:
        """生成 Chrome Mac 版 User-Agent"""
        v = version or cls.CHROME_VERSIONS[0]
        return f'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{v} Safari/537.36'
    
    @classmethod
    def chrome_android(cls, version: Optional[str] = None, android_version: str = '13') -> str:
        """生成 Chrome Android 版 User-Agent"""
        v = version or cls.CHROME_VERSIONS[0]
        return f'Mozilla/5.0 (Linux; Android {android_version}; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{v} Mobile Safari/537.36'
    
    @classmethod
    def chrome_ios(cls, version: Optional[str] = None, ios_version: str = '17.2') -> str:
        """生成 Chrome iOS 版 User-Agent"""
        v = version or cls.CHROME_VERSIONS[0]
        return f'Mozilla/5.0 (iPhone; CPU iPhone OS {ios_version.replace(".", "_")} like Mac OS X) AppleWebKit/{cls.WEBKIT_VERSION} (KHTML, like Gecko) CriOS/{v} Mobile/15E148 Safari/604.1'
    
    @classmethod
    def firefox_desktop(cls, version: Optional[str] = None) -> str:
        """生成 Firefox 桌面版 User-Agent"""
        v = version or cls.FIREFOX_VERSIONS[0]
        return f'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:{v}) Gecko/20100101 Firefox/{v}'
    
    @classmethod
    def firefox_mac(cls, version: Optional[str] = None) -> str:
        """生成 Firefox Mac 版 User-Agent"""
        v = version or cls.FIREFOX_VERSIONS[0]
        return f'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:{v}) Gecko/20100101 Firefox/{v}'
    
    @classmethod
    def firefox_android(cls, version: Optional[str] = None) -> str:
        """生成 Firefox Android 版 User-Agent"""
        v = version or cls.FIREFOX_VERSIONS[0]
        return f'Mozilla/5.0 (Android 13; Mobile; rv:{v}) Gecko/{v} Firefox/{v}'
    
    @classmethod
    def firefox_ios(cls, version: Optional[str] = None) -> str:
        """生成 Firefox iOS 版 User-Agent"""
        v = version or cls.FIREFOX_VERSIONS[0]
        return f'Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/{cls.WEBKIT_VERSION} (KHTML, like Gecko) FxiOS/{v} Mobile/15E148 Safari/604.1'
    
    @classmethod
    def safari_desktop(cls, version: Optional[str] = None, macos_version: str = '10.15.7') -> str:
        """生成 Safari 桌面版 User-Agent"""
        v = version or cls.SAFARI_VERSIONS[0]
        macos_v = macos_version.replace('.', '_')
        return f'Mozilla/5.0 (Macintosh; Intel Mac OS X {macos_v}) AppleWebKit/{cls.WEBKIT_VERSION} (KHTML, like Gecko) Version/{v} Safari/604.1'
    
    @classmethod
    def safari_ios(cls, version: Optional[str] = None, ios_version: str = '17.2') -> str:
        """生成 Safari iOS 版 User-Agent"""
        v = version or cls.SAFARI_VERSIONS[0]
        ios_v = ios_version.replace('.', '_')
        return f'Mozilla/5.0 (iPhone; CPU iPhone OS {ios_v} like Mac OS X) AppleWebKit/{cls.WEBKIT_VERSION} (KHTML, like Gecko) Version/{v} Mobile/15E148 Safari/604.1'
    
    @classmethod
    def edge_desktop(cls, version: Optional[str] = None) -> str:
        """生成 Edge 桌面版 User-Agent"""
        v = version or cls.EDGE_VERSIONS[0]
        return f'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{v} Safari/537.36 Edg/{v}'
    
    @classmethod
    def edge_mac(cls, version: Optional[str] = None) -> str:
        """生成 Edge Mac 版 User-Agent"""
        v = version or cls.EDGE_VERSIONS[0]
        return f'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{v} Safari/537.36 Edg/{v}'
    
    @classmethod
    def googlebot(cls) -> str:
        """生成 Googlebot User-Agent"""
        return 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
    
    @classmethod
    def googlebot_smartphone(cls) -> str:
        """生成 Googlebot 智能手机版 User-Agent"""
        return 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
    
    @classmethod
    def bingbot(cls) -> str:
        """生成 Bingbot User-Agent"""
        return 'Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)'
    
    @classmethod
    def curl(cls, version: str = '8.0') -> str:
        """生成 curl User-Agent"""
        return f'curl/{version}'
    
    @classmethod
    def wget(cls, version: str = '1.21') -> str:
        """生成 wget User-Agent"""
        return f'Wget/{version} (linux-gnu)'
    
    @classmethod
    def python_requests(cls, version: str = '2.31.0') -> str:
        """生成 Python requests User-Agent"""
        return f'python-requests/{version}'
    
    @classmethod
    def random_desktop(cls) -> str:
        """生成随机桌面浏览器 User-Agent"""
        import random
        browsers = [
            cls.chrome_desktop,
            cls.chrome_mac,
            cls.firefox_desktop,
            cls.firefox_mac,
            cls.safari_desktop,
            cls.edge_desktop,
            cls.edge_mac,
        ]
        return random.choice(browsers)()
    
    @classmethod
    def random_mobile(cls) -> str:
        """生成随机移动浏览器 User-Agent"""
        import random
        browsers = [
            cls.chrome_android,
            cls.chrome_ios,
            cls.firefox_android,
            cls.firefox_ios,
            cls.safari_ios,
        ]
        return random.choice(browsers)()
    
    @classmethod
    def random(cls) -> str:
        """生成随机 User-Agent"""
        import random
        return random.choice([cls.random_desktop, cls.random_mobile])()


# 便捷函数
def parse(user_agent: str) -> UserAgentResult:
    """
    解析 User-Agent 字符串
    
    Args:
        user_agent: User-Agent 字符串
        
    Returns:
        UserAgentResult 对象
        
    Example:
        >>> result = parse('Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0')
        >>> print(result.browser.name)  # 'Chrome'
        >>> print(result.os.name)  # 'Windows'
    """
    parser = UserAgentParser()
    return parser.parse(user_agent)


def generate(browser: str = 'chrome', platform: str = 'desktop', 
             version: Optional[str] = None) -> str:
    """
    生成 User-Agent 字符串
    
    Args:
        browser: 浏览器类型 ('chrome', 'firefox', 'safari', 'edge')
        platform: 平台类型 ('desktop', 'mac', 'android', 'ios')
        version: 浏览器版本（可选）
        
    Returns:
        User-Agent 字符串
        
    Example:
        >>> ua = generate('chrome', 'desktop')
        >>> 'Chrome' in ua
        True
    """
    gen = UserAgentGenerator()
    
    method_map = {
        ('chrome', 'desktop'): gen.chrome_desktop,
        ('chrome', 'mac'): gen.chrome_mac,
        ('chrome', 'android'): gen.chrome_android,
        ('chrome', 'ios'): gen.chrome_ios,
        ('firefox', 'desktop'): gen.firefox_desktop,
        ('firefox', 'mac'): gen.firefox_mac,
        ('firefox', 'android'): gen.firefox_android,
        ('firefox', 'ios'): gen.firefox_ios,
        ('safari', 'desktop'): gen.safari_desktop,
        ('safari', 'mac'): gen.safari_desktop,
        ('safari', 'ios'): gen.safari_ios,
        ('edge', 'desktop'): gen.edge_desktop,
        ('edge', 'mac'): gen.edge_mac,
    }
    
    key = (browser.lower(), platform.lower())
    if key in method_map:
        return method_map[key](version)
    
    # 默认返回 Chrome 桌面版
    return gen.chrome_desktop(version)


def is_bot(user_agent: str) -> bool:
    """
    检测 User-Agent 是否为爬虫
    
    Args:
        user_agent: User-Agent 字符串
        
    Returns:
        是否为爬虫
        
    Example:
        >>> is_bot('Googlebot/2.1')
        True
        >>> is_bot('Mozilla/5.0 Chrome/120.0')
        False
    """
    parser = UserAgentParser()
    result = parser.parse(user_agent)
    return result.is_bot


def is_mobile(user_agent: str) -> bool:
    """
    检测 User-Agent 是否为移动设备
    
    Args:
        user_agent: User-Agent 字符串
        
    Returns:
        是否为移动设备
        
    Example:
        >>> is_mobile('Mozilla/5.0 (iPhone; CPU iPhone OS 17_0)')
        True
        >>> is_mobile('Mozilla/5.0 (Windows NT 10.0; Win64; x64)')
        False
    """
    parser = UserAgentParser()
    result = parser.parse(user_agent)
    return result.is_mobile


def get_browser_name(user_agent: str) -> Optional[str]:
    """获取浏览器名称"""
    result = parse(user_agent)
    return result.browser.name if result.browser else None


def get_os_name(user_agent: str) -> Optional[str]:
    """获取操作系统名称"""
    result = parse(user_agent)
    return result.os.name if result.os else None


def get_device_type(user_agent: str) -> str:
    """获取设备类型"""
    result = parse(user_agent)
    return result.device.type.value if result.device else 'unknown'


# 预定义的常用 User-Agent
COMMON_USER_AGENTS = {
    # Chrome
    'chrome_windows': UserAgentGenerator.chrome_desktop(),
    'chrome_mac': UserAgentGenerator.chrome_mac(),
    'chrome_android': UserAgentGenerator.chrome_android(),
    'chrome_ios': UserAgentGenerator.chrome_ios(),
    
    # Firefox
    'firefox_windows': UserAgentGenerator.firefox_desktop(),
    'firefox_mac': UserAgentGenerator.firefox_mac(),
    'firefox_android': UserAgentGenerator.firefox_android(),
    'firefox_ios': UserAgentGenerator.firefox_ios(),
    
    # Safari
    'safari_mac': UserAgentGenerator.safari_desktop(),
    'safari_ios': UserAgentGenerator.safari_ios(),
    
    # Edge
    'edge_windows': UserAgentGenerator.edge_desktop(),
    'edge_mac': UserAgentGenerator.edge_mac(),
    
    # Bots
    'googlebot': UserAgentGenerator.googlebot(),
    'googlebot_mobile': UserAgentGenerator.googlebot_smartphone(),
    'bingbot': UserAgentGenerator.bingbot(),
    
    # Tools
    'curl': UserAgentGenerator.curl(),
    'wget': UserAgentGenerator.wget(),
    'python_requests': UserAgentGenerator.python_requests(),
}


if __name__ == '__main__':
    # 测试示例
    test_uas = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (Linux; Android 13; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
        'Googlebot/2.1 (+http://www.google.com/bot.html)',
        'Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)',
    ]
    
    for ua in test_uas:
        result = parse(ua)
        print(f"\nUA: {ua[:60]}...")
        print(f"  Browser: {result.browser.name if result.browser else 'Unknown'} {result.browser.version if result.browser else ''}")
        print(f"  OS: {result.os.name if result.os else 'Unknown'} {result.os.version if result.os else ''}")
        print(f"  Device: {result.device.type.value if result.device else 'Unknown'}")
        print(f"  Is Bot: {result.is_bot}")