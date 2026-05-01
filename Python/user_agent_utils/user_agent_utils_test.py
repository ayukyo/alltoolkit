"""
User-Agent 工具测试
"""

import unittest
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
    DeviceType,
    COMMON_USER_AGENTS,
)


class TestUserAgentParser(unittest.TestCase):
    """User-Agent 解析器测试"""
    
    def setUp(self):
        self.parser = UserAgentParser()
    
    def test_parse_chrome_windows(self):
        """测试解析 Chrome Windows"""
        ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        result = self.parser.parse(ua)
        
        self.assertEqual(result.browser.name, 'Chrome')
        self.assertEqual(result.browser.version, '120.0.0.0')
        self.assertEqual(result.os.name, 'Windows')
        self.assertEqual(result.device.type, DeviceType.DESKTOP)
        self.assertFalse(result.is_bot)
    
    def test_parse_firefox_windows(self):
        """测试解析 Firefox Windows"""
        ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0'
        result = self.parser.parse(ua)
        
        self.assertEqual(result.browser.name, 'Firefox')
        self.assertEqual(result.browser.version, '121.0')
        self.assertEqual(result.browser.engine, 'Gecko')
        self.assertEqual(result.os.name, 'Windows')
        self.assertFalse(result.is_bot)
    
    def test_parse_safari_ios(self):
        """测试解析 Safari iOS"""
        ua = 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1'
        result = self.parser.parse(ua)
        
        self.assertEqual(result.browser.name, 'Safari')
        self.assertEqual(result.os.name, 'iOS')
        self.assertEqual(result.os.version, '17.2')
        self.assertEqual(result.device.type, DeviceType.MOBILE)
        self.assertTrue(result.is_mobile)
    
    def test_parse_chrome_android(self):
        """测试解析 Chrome Android"""
        ua = 'Mozilla/5.0 (Linux; Android 13; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36'
        result = self.parser.parse(ua)
        
        self.assertEqual(result.browser.name, 'Chrome')
        self.assertEqual(result.os.name, 'Android')
        self.assertEqual(result.os.version, '13')
        self.assertEqual(result.device.type, DeviceType.MOBILE)
        self.assertTrue(result.is_mobile)
    
    def test_parse_ipad(self):
        """测试解析 iPad"""
        ua = 'Mozilla/5.0 (iPad; CPU OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1'
        result = self.parser.parse(ua)
        
        self.assertEqual(result.os.name, 'iOS')
        self.assertEqual(result.device.type, DeviceType.TABLET)
        self.assertTrue(result.is_mobile)
    
    def test_parse_edge(self):
        """测试解析 Edge"""
        ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0'
        result = self.parser.parse(ua)
        
        self.assertEqual(result.browser.name, 'Edge')
        self.assertEqual(result.browser.version, '120.0.0.0')
    
    def test_parse_macos(self):
        """测试解析 macOS"""
        ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
        result = self.parser.parse(ua)
        
        self.assertEqual(result.os.name, 'macOS')
        self.assertEqual(result.os.version, '10.15.7')
    
    def test_parse_googlebot(self):
        """测试解析 Googlebot"""
        ua = 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
        result = self.parser.parse(ua)
        
        self.assertTrue(result.is_bot)
        self.assertEqual(result.device.type, DeviceType.BOT)
    
    def test_parse_bingbot(self):
        """测试解析 Bingbot"""
        ua = 'Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)'
        result = self.parser.parse(ua)
        
        self.assertTrue(result.is_bot)
    
    def test_parse_linux(self):
        """测试解析 Linux"""
        ua = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        result = self.parser.parse(ua)
        
        self.assertEqual(result.os.name, 'Linux')
        self.assertEqual(result.os.architecture, 'x64')
    
    def test_parse_chrome_mobile_ios(self):
        """测试解析 Chrome iOS"""
        ua = 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/120.0.0.0 Mobile/15E148 Safari/604.1'
        result = self.parser.parse(ua)
        
        self.assertEqual(result.browser.name, 'Chrome')
        self.assertTrue(result.is_mobile)


class TestUserAgentGenerator(unittest.TestCase):
    """User-Agent 生成器测试"""
    
    def test_chrome_desktop(self):
        """测试生成 Chrome 桌面版"""
        ua = UserAgentGenerator.chrome_desktop()
        
        self.assertIn('Chrome', ua)
        self.assertIn('Windows', ua)
        self.assertIn('Safari', ua)
    
    def test_chrome_mac(self):
        """测试生成 Chrome Mac 版"""
        ua = UserAgentGenerator.chrome_mac()
        
        self.assertIn('Chrome', ua)
        self.assertIn('Macintosh', ua)
    
    def test_chrome_android(self):
        """测试生成 Chrome Android 版"""
        ua = UserAgentGenerator.chrome_android()
        
        self.assertIn('Chrome', ua)
        self.assertIn('Android', ua)
        self.assertIn('Mobile', ua)
    
    def test_chrome_ios(self):
        """测试生成 Chrome iOS 版"""
        ua = UserAgentGenerator.chrome_ios()
        
        self.assertIn('CriOS', ua)
        self.assertIn('iPhone', ua)
    
    def test_firefox_desktop(self):
        """测试生成 Firefox 桌面版"""
        ua = UserAgentGenerator.firefox_desktop()
        
        self.assertIn('Firefox', ua)
        self.assertIn('Windows', ua)
    
    def test_firefox_android(self):
        """测试生成 Firefox Android 版"""
        ua = UserAgentGenerator.firefox_android()
        
        self.assertIn('Firefox', ua)
        self.assertIn('Android', ua)
    
    def test_safari_desktop(self):
        """测试生成 Safari 桌面版"""
        ua = UserAgentGenerator.safari_desktop()
        
        self.assertIn('Safari', ua)
        self.assertIn('Macintosh', ua)
    
    def test_safari_ios(self):
        """测试生成 Safari iOS 版"""
        ua = UserAgentGenerator.safari_ios()
        
        self.assertIn('Safari', ua)
        self.assertIn('iPhone', ua)
    
    def test_edge_desktop(self):
        """测试生成 Edge 桌面版"""
        ua = UserAgentGenerator.edge_desktop()
        
        self.assertIn('Edg', ua)
        self.assertIn('Windows', ua)
    
    def test_googlebot(self):
        """测试生成 Googlebot"""
        ua = UserAgentGenerator.googlebot()
        
        self.assertIn('Googlebot', ua)
    
    def test_bingbot(self):
        """测试生成 Bingbot"""
        ua = UserAgentGenerator.bingbot()
        
        self.assertIn('bingbot', ua)
    
    def test_curl(self):
        """测试生成 curl UA"""
        ua = UserAgentGenerator.curl()
        
        self.assertIn('curl', ua)
    
    def test_python_requests(self):
        """测试生成 Python requests UA"""
        ua = UserAgentGenerator.python_requests()
        
        self.assertIn('python-requests', ua)
    
    def test_random_desktop(self):
        """测试随机桌面 UA"""
        ua = UserAgentGenerator.random_desktop()
        
        # 应该包含主流浏览器名称之一
        self.assertTrue(
            any(browser in ua for browser in ['Chrome', 'Firefox', 'Safari', 'Edg']),
            f"随机桌面 UA 应包含浏览器名称: {ua}"
        )
    
    def test_random_mobile(self):
        """测试随机移动 UA"""
        ua = UserAgentGenerator.random_mobile()
        
        # 应该包含移动设备标识
        self.assertTrue(
            any(mobile in ua for mobile in ['Mobile', 'iPhone', 'Android']),
            f"随机移动 UA 应包含移动标识: {ua}"
        )
    
    def test_custom_version(self):
        """测试自定义版本"""
        ua = UserAgentGenerator.chrome_desktop(version='999.0.0.0')
        
        self.assertIn('999.0.0.0', ua)


class TestConvenienceFunctions(unittest.TestCase):
    """便捷函数测试"""
    
    def test_parse_function(self):
        """测试 parse 函数"""
        ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36'
        result = parse(ua)
        
        self.assertEqual(result.browser.name, 'Chrome')
        self.assertEqual(result.os.name, 'Windows')
    
    def test_generate_function(self):
        """测试 generate 函数"""
        ua = generate('chrome', 'desktop')
        
        self.assertIn('Chrome', ua)
        self.assertIn('Windows', ua)
    
    def test_generate_firefox(self):
        """测试生成 Firefox UA"""
        ua = generate('firefox', 'desktop')
        
        self.assertIn('Firefox', ua)
    
    def test_generate_safari_ios(self):
        """测试生成 Safari iOS UA"""
        ua = generate('safari', 'ios')
        
        self.assertIn('iPhone', ua)
    
    def test_is_bot_function(self):
        """测试 is_bot 函数"""
        self.assertTrue(is_bot('Googlebot/2.1 (+http://www.google.com/bot.html)'))
        self.assertTrue(is_bot('Mozilla/5.0 (compatible; bingbot/2.0)'))
        self.assertFalse(is_bot('Mozilla/5.0 Chrome/120.0.0.0'))
    
    def test_is_mobile_function(self):
        """测试 is_mobile 函数"""
        self.assertTrue(is_mobile('Mozilla/5.0 (iPhone; CPU iPhone OS 17_0)'))
        self.assertTrue(is_mobile('Mozilla/5.0 (Linux; Android 13)'))
        self.assertFalse(is_mobile('Mozilla/5.0 (Windows NT 10.0; Win64; x64)'))
    
    def test_get_browser_name(self):
        """测试 get_browser_name 函数"""
        self.assertEqual(get_browser_name('Chrome/120.0.0.0'), 'Chrome')
        self.assertEqual(get_browser_name('Firefox/121.0'), 'Firefox')
    
    def test_get_os_name(self):
        """测试 get_os_name 函数"""
        self.assertEqual(get_os_name('Windows NT 10.0'), 'Windows')
        self.assertEqual(get_os_name('Linux x86_64'), 'Linux')
    
    def test_get_device_type(self):
        """测试 get_device_type 函数"""
        self.assertEqual(get_device_type('Windows NT 10.0; Win64; x64'), 'desktop')
        self.assertEqual(get_device_type('iPhone; CPU iPhone OS 17_0'), 'mobile')
        self.assertEqual(get_device_type('iPad; CPU OS 17_0'), 'tablet')


class TestCommonUserAgents(unittest.TestCase):
    """常用 User-Agent 测试"""
    
    def test_common_uas_exist(self):
        """测试常用 UA 字典存在"""
        self.assertIsInstance(COMMON_USER_AGENTS, dict)
        self.assertGreater(len(COMMON_USER_AGENTS), 0)
    
    def test_common_uas_valid(self):
        """测试常用 UA 都是有效的"""
        for name, ua in COMMON_USER_AGENTS.items():
            result = parse(ua)
            # 所有 UA 都应该能被解析
            self.assertIsNotNone(result.original)
    
    def test_chrome_windows_ua(self):
        """测试 Chrome Windows UA"""
        ua = COMMON_USER_AGENTS['chrome_windows']
        result = parse(ua)
        
        self.assertEqual(result.browser.name, 'Chrome')
        self.assertEqual(result.os.name, 'Windows')
        self.assertEqual(result.device.type, DeviceType.DESKTOP)
    
    def test_googlebot_ua(self):
        """测试 Googlebot UA"""
        ua = COMMON_USER_AGENTS['googlebot']
        result = parse(ua)
        
        self.assertTrue(result.is_bot)


class TestEdgeCases(unittest.TestCase):
    """边界情况测试"""
    
    def test_empty_string(self):
        """测试空字符串"""
        result = parse('')
        
        # 应该能处理空字符串
        self.assertEqual(result.original, '')
    
    def test_unknown_browser(self):
        """测试未知浏览器"""
        ua = 'SomeUnknownBrowser/1.0'
        result = parse(ua)
        
        # 浏览器可能为 None
        self.assertIsNotNone(result.original)
    
    def test_malformed_ua(self):
        """测试格式错误的 UA"""
        ua = 'This is not a valid user agent string at all'
        result = parse(ua)
        
        # 应该能处理格式错误的字符串
        self.assertEqual(result.original, ua)


class TestMultipleBrowsers(unittest.TestCase):
    """多浏览器测试"""
    
    def test_opera(self):
        """测试 Opera"""
        ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 OPR/106.0.0.0'
        result = parse(ua)
        
        self.assertEqual(result.browser.name, 'Opera')
    
    def test_samsung_browser(self):
        """测试三星浏览器"""
        ua = 'Mozilla/5.0 (Linux; Android 13; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/23.0 Chrome/115.0.0.0 Mobile Safari/537.36'
        result = parse(ua)
        
        self.assertEqual(result.browser.name, 'Samsung Internet')
    
    def test_uc_browser(self):
        """测试 UC 浏览器"""
        ua = 'Mozilla/5.0 (Linux; U; Android 13; en-US; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/115.0.0.0 Mobile Safari/537.36 UCBrowser/15.5.6.1658'
        result = parse(ua)
        
        self.assertEqual(result.browser.name, 'UC Browser')


if __name__ == '__main__':
    unittest.main()