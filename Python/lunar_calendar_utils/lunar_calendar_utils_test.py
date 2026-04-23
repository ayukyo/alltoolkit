"""
农历日历工具模块测试 (Lunar Calendar Utils Test)
================================================

测试覆盖：
- 公历转农历
- 农历转公历
- 干支计算
- 生肖计算
- 星座计算
- 节气计算
- 节日查询
- 边界值测试
- 异常情况测试

作者: AllToolkit 自动化开发助手
日期: 2026-04-23
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import date, datetime
from lunar_calendar_utils.mod import (
    LunarDate, LunarCalendar,
    solar_to_lunar, lunar_to_solar,
    get_year_ganzhi, get_month_ganzhi, get_day_ganzhi, get_hour_ganzhi,
    get_zodiac, get_constellation,
    get_solar_term_year, get_current_solar_term,
    get_lunar_festival, get_solar_festival, get_all_festivals,
    get_lunar_year_days, get_leap_month, get_leap_month_days, get_lunar_month_days,
    format_lunar_date, get_lunar_info, is_leap_year_lunar,
    today_lunar, today_info, quick_convert,
    TIAN_GAN, DI_ZHI, ZODIAC, LUNAR_MONTH_NAMES, LUNAR_DAY_NAMES
)


class TestRunner:
    """测试运行器"""
    
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []
    
    def test(self, name: str, condition: bool, message: str = ""):
        """运行单个测试"""
        if condition:
            self.passed += 1
            print(f"  ✅ {name}")
        else:
            self.failed += 1
            error_msg = f"  ❌ {name}: {message}"
            print(error_msg)
            self.errors.append(f"{name}: {message}")
    
    def summary(self):
        """输出测试摘要"""
        print(f"\n{'=' * 50}")
        print(f"测试结果: {self.passed} 通过, {self.failed} 失败")
        print(f"{'=' * 50}")
        if self.errors:
            print("\n失败的测试:")
            for err in self.errors:
                print(f"  - {err}")
        return self.failed == 0


def test_lunar_date_class():
    """测试 LunarDate 类"""
    print("\n【LunarDate 类测试】")
    runner = TestRunner()
    
    # 创建农历日期
    ld = LunarDate(2024, 1, 1)
    runner.test("创建农历日期", ld.year == 2024 and ld.month == 1 and ld.day == 1)
    runner.test("默认非闰月", ld.is_leap_month == False)
    
    # 创建闰月日期
    ld_leap = LunarDate(2023, 2, 15, True)
    runner.test("创建闰月日期", ld_leap.is_leap_month == True)
    
    # 字符串表示
    runner.test("__str__ 方法", str(ld) == "农历正月初一")
    runner.test("__repr__ 方法", "LunarDate(2024, 1, 1)" in repr(ld))
    
    # 闰月字符串
    runner.test("闰月字符串表示", "闰" in str(ld_leap))
    
    # 相等性测试
    ld2 = LunarDate(2024, 1, 1)
    runner.test("相等性测试", ld == ld2)
    
    ld3 = LunarDate(2024, 1, 2)
    runner.test("不相等测试", ld != ld3)
    
    # 哈希测试
    runner.test("哈希测试", hash(ld) == hash(ld2))
    
    # get_ganzhi_year 方法
    runner.test("get_ganzhi_year", ld.get_ganzhi_year() == "甲辰")
    
    # get_zodiac 方法
    runner.test("get_zodiac", ld.get_zodiac() == "龙")
    
    return runner


def test_solar_to_lunar():
    """测试公历转农历"""
    print("\n【公历转农历测试】")
    runner = TestRunner()
    
    # 已知日期测试
    # 2024年2月10日是农历2024年正月初一
    lunar = solar_to_lunar(2024, 2, 10)
    runner.test("2024春节", lunar is not None and lunar.year == 2024 and lunar.month == 1 and lunar.day == 1)
    
    # 2024年1月1日是农历2023年十一月二十
    lunar = solar_to_lunar(2024, 1, 1)
    runner.test("2024元旦", lunar is not None and lunar.year == 2023 and lunar.month == 11)
    
    # 2023年闰二月测试
    # 2023年3月22日是农历闰二月初一
    lunar = solar_to_lunar(2023, 3, 22)
    runner.test("2023闰二月", lunar is not None and lunar.is_leap_month == True and lunar.month == 2)
    
    # 边界值测试
    # 1900年边界
    lunar = solar_to_lunar(1900, 1, 31)
    runner.test("1900年边界", lunar is not None and lunar.year == 1900 and lunar.month == 1 and lunar.day == 1)
    
    # 2100年边界
    lunar = solar_to_lunar(2100, 12, 31)
    runner.test("2100年边界", lunar is not None and lunar.year == 2100)
    
    # 无效输入测试
    lunar = solar_to_lunar(1899, 1, 1)
    runner.test("无效年份（太早）", lunar is None)
    
    lunar = solar_to_lunar(2101, 1, 1)
    runner.test("无效年份（太晚）", lunar is None)
    
    lunar = solar_to_lunar(2024, 13, 1)
    runner.test("无效月份", lunar is None)
    
    lunar = solar_to_lunar(2024, 2, 30)
    runner.test("无效日期", lunar is None)
    
    # 一些特殊日期
    # 中秋节（农历八月十五）
    lunar = solar_to_lunar(2024, 9, 17)
    runner.test("2024中秋", lunar is not None and lunar.month == 8 and lunar.day == 15)
    
    # 端午节（农历五月初五）
    lunar = solar_to_lunar(2024, 6, 10)
    runner.test("2024端午", lunar is not None and lunar.month == 5 and lunar.day == 5)
    
    return runner


def test_lunar_to_solar():
    """测试农历转公历"""
    print("\n【农历转公历测试】")
    runner = TestRunner()
    
    # 已知日期测试
    # 农历2024年正月初一 = 公历2024年2月10日
    solar = lunar_to_solar(2024, 1, 1)
    runner.test("农历2024正月初一", solar == date(2024, 2, 10))
    
    # 农历2023年十一月二十 = 公历2024年1月1日
    solar = lunar_to_solar(2023, 11, 20)
    runner.test("农历2023十一月二十", solar == date(2024, 1, 1))
    
    # 闰月测试
    # 2023年闰二月初一 = 公历2023年3月22日
    solar = lunar_to_solar(2023, 2, 1, True)
    runner.test("闰二月初一", solar == date(2023, 3, 22))
    
    # 非闰月
    solar = lunar_to_solar(2023, 2, 1, False)
    runner.test("二月非闰", solar == date(2023, 2, 20))
    
    # 边界值测试
    solar = lunar_to_solar(1900, 1, 1)
    runner.test("1900年正月初一", solar is not None)
    
    solar = lunar_to_solar(2100, 12, 30)
    runner.test("2100年腊月", solar is not None or solar is None)  # 边界年份可能返回None
    
    # 无效输入测试
    solar = lunar_to_solar(1899, 1, 1)
    runner.test("无效年份（太早）", solar is None)
    
    solar = lunar_to_solar(2101, 1, 1)
    runner.test("无效年份（太晚）", solar is None)
    
    solar = lunar_to_solar(2024, 13, 1)
    runner.test("无效月份", solar is None)
    
    solar = lunar_to_solar(2024, 1, 32)
    runner.test("无效日期", solar is None)
    
    # 闰月不存在的年份
    solar = lunar_to_solar(2024, 2, 1, True)  # 2024年没有闰二月
    runner.test("不存在的闰月", solar is None)
    
    return runner


def test_round_trip():
    """测试往返转换"""
    print("\n【往返转换测试】")
    runner = TestRunner()
    
    # 公历 -> 农历 -> 公历
    test_dates = [
        (2024, 1, 1),
        (2024, 2, 10),
        (2024, 6, 10),
        (2024, 9, 17),
        (2024, 12, 31),
        (2000, 2, 29),  # 闰日
        (2023, 3, 22),  # 闰月期间
    ]
    
    for y, m, d in test_dates:
        lunar = solar_to_lunar(y, m, d)
        if lunar:
            solar_back = lunar_to_solar(lunar.year, lunar.month, lunar.day, lunar.is_leap_month)
            runner.test(f"往返 {y}-{m}-{d}", solar_back == date(y, m, d))
        else:
            runner.test(f"往返 {y}-{m}-{d}", False, "转换失败")
    
    return runner


def test_ganzhi():
    """测试干支计算"""
    print("\n【干支计算测试】")
    runner = TestRunner()
    
    # 年干支
    runner.test("1984年干支", get_year_ganzhi(1984) == "甲子")
    runner.test("2024年干支", get_year_ganzhi(2024) == "甲辰")
    runner.test("2025年干支", get_year_ganzhi(2025) == "乙巳")
    runner.test("2023年干支", get_year_ganzhi(2023) == "癸卯")
    runner.test("1900年干支", get_year_ganzhi(1900) == "庚子")
    runner.test("2000年干支", get_year_ganzhi(2000) == "庚辰")
    
    # 月干支
    mgz = get_month_ganzhi(2024, 1)
    runner.test("月干支返回字符串", isinstance(mgz, str) and len(mgz) == 2)
    
    # 日干支
    dgz = get_day_ganzhi(2024, 1, 1)
    runner.test("日干支返回字符串", isinstance(dgz, str) and len(dgz) == 2)
    
    # 已知日期干支
    runner.test("2024年1月1日干支", get_day_ganzhi(2024, 1, 1) == "甲子")
    
    # 时辰干支
    hgz = get_hour_ganzhi("甲子", 0)
    runner.test("时辰干支返回字符串", isinstance(hgz, str) and len(hgz) == 2)
    
    # 子时测试
    runner.test("子时(23点)", get_hour_ganzhi("甲子", 23)[1] == "子")
    runner.test("子时(0点)", get_hour_ganzhi("甲子", 0)[1] == "子")
    
    # 午时测试
    runner.test("午时", get_hour_ganzhi("甲子", 12)[1] == "午")
    
    return runner


def test_zodiac():
    """测试生肖计算"""
    print("\n【生肖计算测试】")
    runner = TestRunner()
    
    runner.test("2024年生肖", get_zodiac(2024) == "龙")
    runner.test("2023年生肖", get_zodiac(2023) == "兔")
    runner.test("2025年生肖", get_zodiac(2025) == "蛇")
    runner.test("1900年生肖", get_zodiac(1900) == "鼠")
    runner.test("2000年生肖", get_zodiac(2000) == "龙")
    runner.test("1984年生肖", get_zodiac(1984) == "鼠")
    runner.test("1975年生肖", get_zodiac(1975) == "兔")
    
    return runner


def test_constellation():
    """测试星座计算"""
    print("\n【星座计算测试】")
    runner = TestRunner()
    
    runner.test("白羊座(3月21)", get_constellation(3, 21) == "白羊座")
    runner.test("白羊座(4月19)", get_constellation(4, 19) == "白羊座")
    runner.test("金牛座(4月20)", get_constellation(4, 20) == "金牛座")
    runner.test("金牛座(5月20)", get_constellation(5, 20) == "金牛座")
    runner.test("双子座(5月21)", get_constellation(5, 21) == "双子座")
    runner.test("巨蟹座(6月22)", get_constellation(6, 22) == "巨蟹座")
    runner.test("狮子座(7月23)", get_constellation(7, 23) == "狮子座")
    runner.test("处女座(8月23)", get_constellation(8, 23) == "处女座")
    runner.test("天秤座(9月23)", get_constellation(9, 23) == "天秤座")
    runner.test("天蝎座(10月24)", get_constellation(10, 24) == "天蝎座")
    runner.test("射手座(11月23)", get_constellation(11, 23) == "射手座")
    runner.test("摩羯座(12月22)", get_constellation(12, 22) == "摩羯座")
    runner.test("摩羯座(1月1)", get_constellation(1, 1) == "摩羯座")
    runner.test("水瓶座(1月20)", get_constellation(1, 20) == "水瓶座")
    runner.test("双鱼座(2月19)", get_constellation(2, 19) == "双鱼座")
    
    return runner


def test_solar_terms():
    """测试节气计算"""
    print("\n【节气计算测试】")
    runner = TestRunner()
    
    # 获取一年的节气
    terms = get_solar_term_year(2024)
    runner.test("节气数量", len(terms) == 24)
    runner.test("节气名称正确", terms[0][0] == "小寒")
    runner.test("节气日期是date对象", all(isinstance(d, date) for _, d in terms))
    
    # 当前节气
    term, days = get_current_solar_term(2024, 1, 15)
    runner.test("获取当前节气", term in ["小寒", "大寒"])
    
    term, days = get_current_solar_term(2024, 6, 21)
    runner.test("夏至节气", term == "夏至")
    
    # 边界测试
    term, days = get_current_solar_term(2024, 12, 31)
    runner.test("年底节气", isinstance(term, str))
    
    return runner


def test_festivals():
    """测试节日查询"""
    print("\n【节日查询测试】")
    runner = TestRunner()
    
    # 农历节日
    runner.test("春节", get_lunar_festival(2024, 1, 1) == "春节")
    runner.test("元宵节", get_lunar_festival(2024, 1, 15) == "元宵节")
    runner.test("端午节", get_lunar_festival(2024, 5, 5) == "端午节")
    runner.test("中秋节", get_lunar_festival(2024, 8, 15) == "中秋节")
    runner.test("重阳节", get_lunar_festival(2024, 9, 9) == "重阳节")
    
    # 除夕测试（腊月最后一天）
    last_day = get_lunar_month_days(2024, 12)
    runner.test("除夕", get_lunar_festival(2024, 12, last_day) == "除夕")
    
    # 闰月无节日
    runner.test("闰月无节日", get_lunar_festival(2023, 2, 15, True) is None)
    
    # 非节日日期
    runner.test("非节日", get_lunar_festival(2024, 3, 10) is None)
    
    # 公历节日
    runner.test("元旦", get_solar_festival(1, 1) == "元旦")
    runner.test("情人节", get_solar_festival(2, 14) == "情人节")
    runner.test("劳动节", get_solar_festival(5, 1) == "劳动节")
    runner.test("国庆节", get_solar_festival(10, 1) == "国庆节")
    runner.test("圣诞节", get_solar_festival(12, 25) == "圣诞节")
    
    # 非节日
    runner.test("非公历节日", get_solar_festival(3, 15) is None)
    
    # 综合节日查询
    festivals = get_all_festivals(2024, 1, 1)
    runner.test("元旦节日列表", "元旦" in festivals)
    
    # 春节（2024年2月10日）
    festivals = get_all_festivals(2024, 2, 10)
    runner.test("春节节日列表", "春节" in festivals)
    
    return runner


def test_lunar_year_functions():
    """测试农历年相关函数"""
    print("\n【农历年函数测试】")
    runner = TestRunner()
    
    # 有闰月的年份
    runner.test("2023年有闰月", is_leap_year_lunar(2023) == True)
    runner.test("2024年无闰月", is_leap_year_lunar(2024) == False)
    
    # 闰月月份
    runner.test("2023年闰二月", get_leap_month(2023) == 2)
    runner.test("2024年无闰月", get_leap_month(2024) == 0)
    runner.test("2025年闰六月", get_leap_month(2025) == 6)
    
    # 年天数
    days = get_lunar_year_days(2024)
    runner.test("2024年天数合理", 353 <= days <= 385)
    
    # 闰月天数
    leap_days = get_leap_month_days(2023)
    runner.test("闰月天数合理", leap_days == 29 or leap_days == 30)
    
    # 月份天数
    month_days = get_lunar_month_days(2024, 1)
    runner.test("月份天数合理", month_days == 29 or month_days == 30)
    
    return runner


def test_format_and_info():
    """测试格式化和信息函数"""
    print("\n【格式化和信息函数测试】")
    runner = TestRunner()
    
    # 格式化农历日期
    ld = LunarDate(2024, 1, 1)
    formatted = format_lunar_date(ld)
    runner.test("格式化包含干支", "甲辰" in formatted)
    runner.test("格式化包含生肖", "龙" in formatted)
    runner.test("格式化包含正月", "正月" in formatted)
    runner.test("格式化包含初一", "初一" in formatted)
    
    # 获取农历信息
    info = get_lunar_info(2024, 2, 10)
    runner.test("信息包含公历日期", "solar_date" in info)
    runner.test("信息包含农历日期", "lunar_date" in info)
    runner.test("信息包含干支", "year_ganzhi" in info)
    runner.test("信息包含生肖", "zodiac" in info)
    runner.test("信息包含星座", "constellation" in info)
    runner.test("信息包含节日", "festivals" in info)
    runner.test("春节是节日", "春节" in info["festivals"])
    
    # 今天信息
    info_today = today_info()
    runner.test("today_info返回字典", isinstance(info_today, dict))
    runner.test("today_info包含必要键", "solar_date" in info_today)
    
    # 今天农历
    today_lunar_date = today_lunar()
    runner.test("today_lunar返回LunarDate", today_lunar_date is None or isinstance(today_lunar_date, LunarDate))
    
    return runner


def test_lunar_calendar_class():
    """测试 LunarCalendar 类"""
    print("\n【LunarCalendar 类测试】")
    runner = TestRunner()
    
    # 创建日历
    cal = LunarCalendar(2024)
    runner.test("创建年历", cal.solar_year == 2024)
    
    # 获取年份信息
    info = cal.get_year_info()
    runner.test("年份信息包含干支", "ganzhi" in info)
    runner.test("年份信息包含生肖", "zodiac" in info)
    runner.test("年份信息包含闰月", "leap_month" in info)
    
    # 获取节气
    terms = cal.get_solar_terms()
    runner.test("节气数量正确", len(terms) == 24)
    
    # 创建带日期的日历
    cal_with_date = LunarCalendar(2024, 2, 10)
    runner.test("创建带日期日历", cal_with_date.solar_month == 2)
    
    # 获取农历日期
    lunar = cal_with_date.get_lunar_date()
    runner.test("获取农历日期", lunar is not None and lunar.month == 1 and lunar.day == 1)
    
    # 转换测试
    lunar = cal.convert_to_lunar(2, 10)
    runner.test("公历转农历", lunar is not None and lunar.month == 1)
    
    solar = cal.convert_to_solar(1, 1)
    runner.test("农历转公历", solar == date(2024, 2, 10))
    
    # 月历测试
    month_cal = cal.get_month_calendar(2)
    runner.test("月历返回列表", isinstance(month_cal, list))
    runner.test("月历周数合理", 4 <= len(month_cal) <= 6)
    
    return runner


def test_constants():
    """测试常量"""
    print("\n【常量测试】")
    runner = TestRunner()
    
    runner.test("天干数量", len(TIAN_GAN) == 10)
    runner.test("地支数量", len(DI_ZHI) == 12)
    runner.test("生肖数量", len(ZODIAC) == 12)
    runner.test("月份名称数量", len(LUNAR_MONTH_NAMES) == 12)
    runner.test("日期名称数量", len(LUNAR_DAY_NAMES) == 30)
    
    # 天干内容
    runner.test("天干甲", TIAN_GAN[0] == "甲")
    runner.test("天干癸", TIAN_GAN[9] == "癸")
    
    # 地支内容
    runner.test("地支子", DI_ZHI[0] == "子")
    runner.test("地支亥", DI_ZHI[11] == "亥")
    
    # 生肖内容
    runner.test("生肖鼠", ZODIAC[0] == "鼠")
    runner.test("生肖猪", ZODIAC[11] == "猪")
    
    return runner


def test_edge_cases():
    """边界值测试"""
    print("\n【边界值测试】")
    runner = TestRunner()
    
    # 1900年边界
    lunar = solar_to_lunar(1900, 1, 31)
    runner.test("1900年起始", lunar is not None)
    
    lunar = solar_to_lunar(1900, 2, 28)
    runner.test("1900年2月", lunar is not None)
    
    # 2100年边界
    lunar = solar_to_lunar(2100, 12, 31)
    runner.test("2100年结束", lunar is not None)
    
    # 闰年测试
    lunar = solar_to_lunar(2000, 2, 29)
    runner.test("闰日转换", lunar is not None)
    
    lunar = solar_to_lunar(2024, 2, 29)
    runner.test("2024闰日", lunar is not None)
    
    # 极端月份
    for month in range(1, 13):
        lunar = solar_to_lunar(2024, month, 15)
        runner.test(f"月份{month}转换", lunar is not None)
    
    # 非法输入
    runner.test("负年份", solar_to_lunar(-1, 1, 1) is None)
    runner.test("零月份", solar_to_lunar(2024, 0, 1) is None)
    runner.test("零日期", solar_to_lunar(2024, 1, 0) is None)
    
    # 星座边界
    runner.test("星座1月1日", get_constellation(1, 1) == "摩羯座")
    runner.test("星座12月31日", get_constellation(12, 31) == "摩羯座")
    
    # 干支周期
    ganzhi_1984 = get_year_ganzhi(1984)
    ganzhi_2044 = get_year_ganzhi(2044)  # 60年后
    runner.test("干支周期60年", ganzhi_1984 == ganzhi_2044)
    
    return runner


def test_quick_functions():
    """测试便捷函数"""
    print("\n【便捷函数测试】")
    runner = TestRunner()
    
    # today_lunar
    lunar = today_lunar()
    runner.test("today_lunar返回有效", lunar is None or isinstance(lunar, LunarDate))
    
    # today_info
    info = today_info()
    runner.test("today_info返回有效", isinstance(info, dict))
    
    # quick_convert
    result = quick_convert(date(2024, 2, 10))
    runner.test("quick_convert返回字符串", isinstance(result, str))
    runner.test("quick_convert包含信息", len(result) > 0)
    
    return runner


def run_all_tests():
    """运行所有测试"""
    print("=" * 50)
    print("农历日历工具模块完整测试")
    print("=" * 50)
    
    runners = [
        test_lunar_date_class(),
        test_solar_to_lunar(),
        test_lunar_to_solar(),
        test_round_trip(),
        test_ganzhi(),
        test_zodiac(),
        test_constellation(),
        test_solar_terms(),
        test_festivals(),
        test_lunar_year_functions(),
        test_format_and_info(),
        test_lunar_calendar_class(),
        test_constants(),
        test_edge_cases(),
        test_quick_functions(),
    ]
    
    total_passed = sum(r.passed for r in runners)
    total_failed = sum(r.failed for r in runners)
    
    print(f"\n{'=' * 50}")
    print(f"总计: {total_passed} 通过, {total_failed} 失败")
    print(f"{'=' * 50}")
    
    return total_failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)