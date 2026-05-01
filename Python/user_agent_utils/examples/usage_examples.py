"""
User-Agent 工具使用示例
======================

演示 User-Agent 解析和生成的各种用法。
"""

import sys
import os

# 添加父目录到路径，以便导入 mod
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    UserAgentParser,
    UserAgentGenerator,
    parse,
    generate,
    is_bot,
    is_mobile,
    get_browser_name,
    get_os_name,
    get_device_type,
    COMMON_USER_AGENTS,
)


def example_parse_user_agent():
    """示例：解析 User-Agent 字符串"""
    print("=" * 60)
    print("示例 1: 解析 User-Agent 字符串")
    print("=" * 60)
    
    # 创建解析器
    parser = UserAgentParser()
    
    # 示例 User-Agent 列表
    user_agents = [
        # Chrome Windows
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        
        # Firefox macOS
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0',
        
        # Safari iOS
        'Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1',
        
        # Chrome Android
        'Mozilla/5.0 (Linux; Android 13; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
        
        # Edge
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
        
        # Googlebot
        'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
    ]
    
    for ua in user_agents:
        print(f"\n📱 User-Agent: {ua[:50]}...")
        result = parser.parse(ua)
        
        # 浏览器信息
        if result.browser:
            print(f"   🌐 浏览器: {result.browser.name} {result.browser.version or ''}")
            if result.browser.engine:
                print(f"      引擎: {result.browser.engine} {result.browser.engine_version or ''}")
        
        # 操作系统信息
        if result.os:
            print(f"   💻 操作系统: {result.os.name} {result.os.version or ''}")
            if result.os.architecture:
                print(f"      架构: {result.os.architecture}")
        
        # 设备信息
        if result.device:
            print(f"   📱 设备类型: {result.device.type.value}")
            if result.device.brand:
                print(f"      品牌: {result.device.brand}")
        
        # 特殊标识
        if result.is_bot:
            print("   🤖 这是爬虫!")
        if result.is_mobile:
            print("   📱 这是移动设备!")


def example_generate_user_agent():
    """示例：生成 User-Agent 字符串"""
    print("\n" + "=" * 60)
    print("示例 2: 生成 User-Agent 字符串")
    print("=" * 60)
    
    gen = UserAgentGenerator()
    
    # 生成各种 User-Agent
    print("\n🌐 Chrome:")
    print(f"   Windows: {gen.chrome_desktop()}")
    print(f"   Mac: {gen.chrome_mac()}")
    print(f"   Android: {gen.chrome_android()}")
    print(f"   iOS: {gen.chrome_ios()}")
    
    print("\n🦊 Firefox:")
    print(f"   Windows: {gen.firefox_desktop()}")
    print(f"   Mac: {gen.firefox_mac()}")
    print(f"   Android: {gen.firefox_android()}")
    print(f"   iOS: {gen.firefox_ios()}")
    
    print("\n🧭 Safari:")
    print(f"   Mac: {gen.safari_desktop()}")
    print(f"   iOS: {gen.safari_ios()}")
    
    print("\n🔷 Edge:")
    print(f"   Windows: {gen.edge_desktop()}")
    print(f"   Mac: {gen.edge_mac()}")
    
    print("\n🤖 爬虫:")
    print(f"   Googlebot: {gen.googlebot()}")
    print(f"   Googlebot Mobile: {gen.googlebot_smartphone()}")
    print(f"   Bingbot: {gen.bingbot()}")
    
    print("\n🔧 工具:")
    print(f"   curl: {gen.curl()}")
    print(f"   wget: {gen.wget()}")
    print(f"   Python requests: {gen.python_requests()}")


def example_convenience_functions():
    """示例：使用便捷函数"""
    print("\n" + "=" * 60)
    print("示例 3: 使用便捷函数")
    print("=" * 60)
    
    # 测试 User-Agent
    test_uas = [
        'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) Safari/604.1',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0',
        'Googlebot/2.1 (+http://www.google.com/bot.html)',
    ]
    
    for ua in test_uas:
        print(f"\n📝 {ua[:50]}...")
        print(f"   浏览器: {get_browser_name(ua)}")
        print(f"   操作系统: {get_os_name(ua)}")
        print(f"   设备类型: {get_device_type(ua)}")
        print(f"   是爬虫: {is_bot(ua)}")
        print(f"   是移动设备: {is_mobile(ua)}")


def example_generate_with_params():
    """示例：使用参数生成 User-Agent"""
    print("\n" + "=" * 60)
    print("示例 4: 使用参数生成 User-Agent")
    print("=" * 60)
    
    # 使用 generate 函数
    print("\n🎯 使用 generate() 函数:")
    print(f"   Chrome Desktop: {generate('chrome', 'desktop')}")
    print(f"   Chrome Mac: {generate('chrome', 'mac')}")
    print(f"   Chrome Android: {generate('chrome', 'android')}")
    print(f"   Chrome iOS: {generate('chrome', 'ios')}")
    print(f"   Firefox Desktop: {generate('firefox', 'desktop')}")
    print(f"   Safari iOS: {generate('safari', 'ios')}")
    print(f"   Edge Desktop: {generate('edge', 'desktop')}")
    
    # 自定义版本
    print("\n🔢 自定义版本:")
    print(f"   Chrome 999: {generate('chrome', 'desktop', '999.0.0.0')}")
    print(f"   Firefox 200: {generate('firefox', 'desktop', '200.0')}")
    print(f"   Safari 100: {generate('safari', 'mac', '100.0')}")


def example_random_user_agent():
    """示例：生成随机 User-Agent"""
    print("\n" + "=" * 60)
    print("示例 5: 生成随机 User-Agent")
    print("=" * 60)
    
    gen = UserAgentGenerator()
    
    print("\n🎲 随机桌面 UA:")
    for i in range(3):
        print(f"   {i+1}. {gen.random_desktop()[:60]}...")
    
    print("\n🎲 随机移动 UA:")
    for i in range(3):
        print(f"   {i+1}. {gen.random_mobile()[:60]}...")
    
    print("\n🎲 完全随机 UA:")
    for i in range(3):
        print(f"   {i+1}. {gen.random()[:60]}...")


def example_common_user_agents():
    """示例：使用预定义的常用 User-Agent"""
    print("\n" + "=" * 60)
    print("示例 6: 预定义的常用 User-Agent")
    print("=" * 60)
    
    print("\n📚 常用 UA 列表:")
    for name, ua in COMMON_USER_AGENTS.items():
        print(f"   {name}: {ua[:50]}...")


def example_detect_crawlers():
    """示例：检测爬虫"""
    print("\n" + "=" * 60)
    print("示例 7: 检测爬虫")
    print("=" * 60)
    
    crawler_uas = [
        'Googlebot/2.1 (+http://www.google.com/bot.html)',
        'Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)',
        'Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)',
        'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)',
        'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X) Chrome/119.0.0.0 Mobile Safari/537.36 (compatible; Googlebot/2.1)',
    ]
    
    print("\n🤖 爬虫检测:")
    for ua in crawler_uas:
        result = parse(ua)
        status = "✅ 是爬虫" if result.is_bot else "❌ 不是爬虫"
        print(f"   {status}: {ua[:50]}...")


def example_device_detection():
    """示例：设备类型检测"""
    print("\n" + "=" * 60)
    print("示例 8: 设备类型检测")
    print("=" * 60)
    
    device_uas = [
        ('桌面 - Windows', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0'),
        ('桌面 - Mac', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Safari/604.1'),
        ('桌面 - Linux', 'Mozilla/5.0 (X11; Linux x86_64) Firefox/121.0'),
        ('手机 - iPhone', 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) Safari/604.1'),
        ('手机 - Android', 'Mozilla/5.0 (Linux; Android 13; Pixel 7) Chrome/120.0.0.0 Mobile'),
        ('平板 - iPad', 'Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) Safari/604.1'),
        ('平板 - Android', 'Mozilla/5.0 (Linux; Android 13; SM-T870) Chrome/120.0.0.0 Safari/537.36'),
    ]
    
    print("\n📱 设备类型检测:")
    for name, ua in device_uas:
        result = parse(ua)
        device_type = result.device.type.value if result.device else "unknown"
        is_mob = "📱 移动设备" if result.is_mobile else "🖥️ 桌面设备"
        print(f"   {name}: {device_type} ({is_mob})")


def example_web_scraping():
    """示例：Web 爬虫场景"""
    print("\n" + "=" * 60)
    print("示例 9: Web 爬虫场景应用")
    print("=" * 60)
    
    import random
    
    print("\n🕷️ 模拟爬虫请求头:")
    
    # 模拟真实用户
    print("\n   方式 1: 随机选择真实浏览器 UA")
    real_ua = UserAgentGenerator.random_desktop()
    print(f"   User-Agent: {real_ua}")
    
    # 模拟移动用户
    print("\n   方式 2: 随机移动浏览器 UA")
    mobile_ua = UserAgentGenerator.random_mobile()
    print(f"   User-Agent: {mobile_ua}")
    
    # 使用爬虫 UA（诚实方式）
    print("\n   方式 3: 使用爬虫 UA（诚实标识）")
    bot_ua = UserAgentGenerator.googlebot()
    print(f"   User-Agent: {bot_ua}")
    
    # 轮换策略
    print("\n   方式 4: UA 轮换策略")
    ua_pool = [
        UserAgentGenerator.chrome_desktop(),
        UserAgentGenerator.firefox_desktop(),
        UserAgentGenerator.safari_desktop(),
        UserAgentGenerator.edge_desktop(),
    ]
    for i in range(3):
        selected = random.choice(ua_pool)
        print(f"   请求 {i+1}: {selected[:60]}...")


def example_log_analysis():
    """示例：日志分析场景"""
    print("\n" + "=" * 60)
    print("示例 10: 日志分析场景")
    print("=" * 60)
    
    # 模拟访问日志
    logs = [
        ('192.168.1.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0'),
        ('192.168.1.2', 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0) Safari/604.1'),
        ('192.168.1.3', 'Googlebot/2.1 (+http://www.google.com/bot.html)'),
        ('192.168.1.4', 'Mozilla/5.0 (Linux; Android 13) Chrome/120.0.0.0 Mobile'),
        ('192.168.1.5', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Safari/604.1'),
        ('192.168.1.6', 'Mozilla/5.0 (iPad; CPU OS 17_0) Safari/604.1'),
        ('192.168.1.7', 'bingbot/2.0 (+http://www.bing.com/bingbot.htm)'),
    ]
    
    # 统计
    browsers = {}
    oses = {}
    devices = {'desktop': 0, 'mobile': 0, 'tablet': 0, 'bot': 0}
    
    for ip, ua in logs:
        result = parse(ua)
        
        # 浏览器统计
        if result.browser:
            name = result.browser.name
            browsers[name] = browsers.get(name, 0) + 1
        
        # 操作系统统计
        if result.os:
            name = result.os.name
            oses[name] = oses.get(name, 0) + 1
        
        # 设备统计
        if result.is_bot:
            devices['bot'] += 1
        elif result.device:
            dtype = result.device.type.value
            if dtype in devices:
                devices[dtype] += 1
    
    print("\n📊 浏览器分布:")
    for name, count in sorted(browsers.items(), key=lambda x: -x[1]):
        print(f"   {name}: {count}")
    
    print("\n📊 操作系统分布:")
    for name, count in sorted(oses.items(), key=lambda x: -x[1]):
        print(f"   {name}: {count}")
    
    print("\n📊 设备分布:")
    for name, count in devices.items():
        if count > 0:
            print(f"   {name}: {count}")


if __name__ == '__main__':
    example_parse_user_agent()
    example_generate_user_agent()
    example_convenience_functions()
    example_generate_with_params()
    example_random_user_agent()
    example_common_user_agents()
    example_detect_crawlers()
    example_device_detection()
    example_web_scraping()
    example_log_analysis()
    
    print("\n" + "=" * 60)
    print("✅ 所有示例完成!")
    print("=" * 60)