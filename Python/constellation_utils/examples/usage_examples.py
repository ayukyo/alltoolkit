"""
Constellation Utilities 使用示例

展示星座和生肖工具的各种使用场景
"""

from datetime import date
from mod import (
    Zodiac, Element, Quality, ChineseZodiac,
    get_zodiac, get_zodiac_from_date, get_zodiac_info,
    get_element, get_quality, get_ruling_planet,
    calculate_compatibility,
    get_chinese_zodiac, get_chinese_zodiac_info,
    calculate_chinese_compatibility,
    estimate_rising_sign,
    get_daily_horoscope,
    get_all_zodiacs, get_all_chinese_zodiacs,
    get_zodiac_by_chinese_name, get_chinese_zodiac_by_name,
    get_element_relationship,
    calculate_triple_harmony, calculate_six_harm,
)


def example_basic_zodiac():
    """基础星座判断示例"""
    print("=" * 50)
    print("基础星座判断")
    print("=" * 50)
    
    # 根据月份和日期判断星座
    zodiac = get_zodiac(8, 15)
    print(f"8月15日的星座: {zodiac.value}")
    
    # 根据日期对象判断星座
    birth_date = date(1990, 5, 25)
    zodiac = get_zodiac_from_date(birth_date)
    print(f"1990年5月25日的星座: {zodiac.value}")
    
    # 根据中文名称获取星座
    zodiac = get_zodiac_by_chinese_name("天蝎座")
    print(f"天蝎座对应的枚举: {zodiac}")
    print()


def example_zodiac_info():
    """星座详细信息示例"""
    print("=" * 50)
    print("星座详细信息")
    print("=" * 50)
    
    # 获取狮子座的详细信息
    leo_info = get_zodiac_info(Zodiac.LEO)
    print(f"星座: {leo_info.zodiac.value}")
    print(f"日期范围: {leo_info.date_range}")
    print(f"元素: {leo_info.element.value}")
    print(f"特质: {leo_info.quality.value}")
    print(f"守护星: {leo_info.ruling_planet}")
    print(f"幸运数字: {leo_info.lucky_numbers}")
    print(f"幸运颜色: {leo_info.lucky_colors}")
    print(f"优点: {', '.join(leo_info.strengths)}")
    print(f"缺点: {', '.join(leo_info.weaknesses)}")
    print(f"最佳配对: {', '.join([z.value for z in leo_info.compatible_signs])}")
    print()
    
    # 快捷获取元素和特质
    zodiac = Zodiac.ARIES
    print(f"{zodiac.value}的元素: {get_element(zodiac).value}")
    print(f"{zodiac.value}的特质: {get_quality(zodiac).value}")
    print(f"{zodiac.value}的守护星: {get_ruling_planet(zodiac)}")
    print()


def example_zodiac_compatibility():
    """星座配对示例"""
    print("=" * 50)
    print("星座配对分析")
    print("=" * 50)
    
    # 计算白羊座和狮子座的配对
    result = calculate_compatibility(Zodiac.ARIES, Zodiac.LEO)
    print(f"{result['zodiac1']} 与 {result['zodiac2']}")
    print(f"配对指数: {result['score']}分")
    print(f"配对描述: {result['description']}")
    print(f"元素匹配: {'是' if result['element_match'] else '否'}")
    print(f"最佳配对: {'是' if result['compatible'] else '否'}")
    print()
    
    # 计算金牛座和天蝎座的配对
    result = calculate_compatibility(Zodiac.TAURUS, Zodiac.SCORPIO)
    print(f"{result['zodiac1']} 与 {result['zodiac2']}")
    print(f"配对指数: {result['score']}分")
    print(f"配对描述: {result['description']}")
    print()


def example_element_relationship():
    """元素关系示例"""
    print("=" * 50)
    print("元素关系分析")
    print("=" * 50)
    
    # 同元素
    print(f"火象与火象: {get_element_relationship(Element.FIRE, Element.FIRE)}")
    print()
    
    # 和谐元素（火-风）
    print(f"火象与风象: {get_element_relationship(Element.FIRE, Element.AIR)}")
    print()
    
    # 冲突元素（火-水）
    print(f"火象与水象: {get_element_relationship(Element.FIRE, Element.WATER)}")
    print()


def example_triple_harmony():
    """三合星座示例"""
    print("=" * 50)
    print("三合星座")
    print("=" * 50)
    
    # 火象三合
    fire_trine = calculate_triple_harmony(Zodiac.ARIES)
    print(f"白羊座的三合星座: {', '.join([z.value for z in fire_trine])}")
    
    # 水象三合
    water_trine = calculate_triple_harmony(Zodiac.CANCER)
    print(f"巨蟹座的三合星座: {', '.join([z.value for z in water_trine])}")
    print()


def example_six_harm():
    """六害星座示例"""
    print("=" * 50)
    print("六害星座")
    print("=" * 50)
    
    # 白羊座的六害星座
    harm = calculate_six_harm(Zodiac.ARIES)
    print(f"白羊座的六害星座: {harm.value}")
    
    # 金牛座的六害星座
    harm = calculate_six_harm(Zodiac.TAURUS)
    print(f"金牛座的六害星座: {harm.value}")
    print()


def example_chinese_zodiac():
    """生肖基础功能示例"""
    print("=" * 50)
    print("生肖基础功能")
    print("=" * 50)
    
    # 根据年份计算生肖
    zodiac = get_chinese_zodiac(2000)
    print(f"2000年的生肖: {zodiac.value}")
    
    zodiac = get_chinese_zodiac(2024)
    print(f"2024年的生肖: {zodiac.value}")
    
    zodiac = get_chinese_zodiac(1985)
    print(f"1985年的生肖: {zodiac.value}")
    
    # 根据名称获取生肖
    zodiac = get_chinese_zodiac_by_name("龙")
    print(f"'龙'对应的枚举: {zodiac}")
    print()


def example_chinese_zodiac_info():
    """生肖详细信息示例"""
    print("=" * 50)
    print("生肖详细信息")
    print("=" * 50)
    
    # 获取龙的详细信息
    dragon_info = get_chinese_zodiac_info(ChineseZodiac.DRAGON)
    print(f"生肖: {dragon_info.zodiac.value}")
    print(f"年份: {dragon_info.years}")
    print(f"五行: {dragon_info.element}")
    print(f"阴阳: {dragon_info.yin_yang}")
    print(f"幸运数字: {dragon_info.lucky_numbers}")
    print(f"幸运颜色: {dragon_info.lucky_colors}")
    print(f"优点: {', '.join(dragon_info.strengths)}")
    print(f"缺点: {', '.join(dragon_info.weaknesses)}")
    print(f"相合生肖: {', '.join([z.value for z in dragon_info.compatible_signs])}")
    print(f"相冲生肖: {', '.join([z.value for z in dragon_info.incompatible_signs])}")
    print()


def example_chinese_compatibility():
    """生肖配对示例"""
    print("=" * 50)
    print("生肖配对分析")
    print("=" * 50)
    
    # 计算鼠和牛的配对（六合）
    result = calculate_chinese_compatibility(ChineseZodiac.RAT, ChineseZodiac.OX)
    print(f"{result['zodiac1']} 与 {result['zodiac2']}")
    print(f"配对指数: {result['score']}分")
    print(f"配对描述: {result['description']}")
    print(f"相合: {'是' if result['compatible'] else '否'}")
    print(f"相冲: {'是' if result['incompatible'] else '否'}")
    print()
    
    # 计算鼠和马的配对（相冲）
    result = calculate_chinese_compatibility(ChineseZodiac.RAT, ChineseZodiac.HORSE)
    print(f"{result['zodiac1']} 与 {result['zodiac2']}")
    print(f"配对指数: {result['score']}分")
    print(f"配对描述: {result['description']}")
    print()
    
    # 计算龙和猴的配对（三合）
    result = calculate_chinese_compatibility(ChineseZodiac.DRAGON, ChineseZodiac.MONKEY)
    print(f"{result['zodiac1']} 与 {result['zodiac2']}")
    print(f"配对指数: {result['score']}分")
    print(f"配对描述: {result['description']}")
    print()


def example_rising_sign():
    """上升星座估算示例"""
    print("=" * 50)
    print("上升星座估算")
    print("=" * 50)
    
    # 估算上升星座
    sun_zodiac = Zodiac.LEO
    birth_time = (8, 30)  # 8:30 AM
    rising = estimate_rising_sign(birth_time, sun_zodiac)
    print(f"太阳星座: {sun_zodiac.value}")
    print(f"出生时间: {birth_time[0]}:{birth_time[1]}")
    print(f"估算上升星座: {rising.value}")
    print()
    
    # 不同时间的上升星座
    print("狮子座在不同时间的上升星座:")
    for hour in [0, 6, 12, 18]:
        rising = estimate_rising_sign((hour, 0), Zodiac.LEO)
        print(f"  {hour}:00 -> {rising.value}")
    print()
    
    print("注意：这是简化估算，真实上升星座需要精确出生时间和地点")


def example_daily_horoscope():
    """每日运势示例"""
    print("=" * 50)
    print("每日运势")
    print("=" * 50)
    
    # 获取今日运势
    zodiac = Zodiac.VIRGO
    horoscope = get_daily_horoscope(zodiac)
    
    print(f"星座: {horoscope['zodiac']}")
    print(f"综合运势: {horoscope['overall']}")
    print()
    print(f"爱情运势: {horoscope['love']['level']}")
    print(f"  {horoscope['love']['description']}")
    print()
    print(f"事业运势: {horoscope['career']['level']}")
    print(f"  {horoscope['career']['description']}")
    print()
    print(f"财运: {horoscope['wealth']['level']}")
    print(f"  {horoscope['wealth']['description']}")
    print()
    print(f"健康运势: {horoscope['health']['level']}")
    print(f"  {horoscope['health']['description']}")
    print()
    print(f"幸运颜色: {horoscope['lucky_color']}")
    print(f"幸运数字: {horoscope['lucky_number']}")
    print(f"今日提示: {horoscope['tip']}")
    print()
    
    print("注意：运势仅供娱乐参考，请理性看待")


def example_list_all():
    """列出所有星座和生肖"""
    print("=" * 50)
    print("星座和生肖列表")
    print("=" * 50)
    
    # 所有星座
    print("十二星座:")
    for zodiac in get_all_zodiacs():
        info = get_zodiac_info(zodiac)
        print(f"  {zodiac.value} ({info.date_range}) - {info.element.value}")
    print()
    
    # 所有生肖
    print("十二生肖:")
    for zodiac in get_all_chinese_zodiacs():
        info = get_chinese_zodiac_info(zodiac)
        print(f"  {zodiac.value} - 五行:{info.element} 阴阳:{info.yin_yang}")
    print()


def example_user_profile():
    """用户星座档案示例"""
    print("=" * 50)
    print("完整星座档案")
    print("=" * 50)
    
    # 假设用户信息
    birth_date = date(1992, 8, 15)
    birth_year = 1992
    birth_time = (10, 30)
    
    # 计算各种星座信息
    sun_zodiac = get_zodiac_from_date(birth_date)
    chinese_zodiac = get_chinese_zodiac(birth_year)
    rising_sign = estimate_rising_sign(birth_time, sun_zodiac)
    
    print(f"出生日期: {birth_date}")
    print(f"出生年份: {birth_year}")
    print(f"出生时间: {birth_time[0]}:{birth_time[1]}")
    print()
    print("=== 星座档案 ===")
    print(f"太阳星座: {sun_zodiac.value}")
    print(f"上升星座: {rising_sign.value} (估算)")
    print(f"生肖: {chinese_zodiac.value}")
    print()
    
    # 详细信息
    zodiac_info = get_zodiac_info(sun_zodiac)
    print(f"元素: {zodiac_info.element.value}")
    print(f"特质: {zodiac_info.quality.value}")
    print(f"守护星: {zodiac_info.ruling_planet}")
    print()
    
    chinese_info = get_chinese_zodiac_info(chinese_zodiac)
    print(f"五行: {chinese_info.element}")
    print(f"阴阳: {chinese_info.yin_yang}")
    print()
    
    # 三合
    trine = calculate_triple_harmony(sun_zodiac)
    print(f"三合星座: {', '.join([z.value for z in trine])}")
    
    # 六害
    harm = calculate_six_harm(sun_zodiac)
    print(f"六害星座: {harm.value}")
    print()
    
    # 今日运势
    print("=== 今日运势 ===")
    horoscope = get_daily_horoscope(sun_zodiac)
    print(f"综合运势: {horoscope['overall']}")
    print(f"幸运颜色: {horoscope['lucky_color']}")
    print(f"幸运数字: {horoscope['lucky_number']}")
    print()


def main():
    """运行所有示例"""
    example_basic_zodiac()
    example_zodiac_info()
    example_zodiac_compatibility()
    example_element_relationship()
    example_triple_harmony()
    example_six_harm()
    example_chinese_zodiac()
    example_chinese_zodiac_info()
    example_chinese_compatibility()
    example_rising_sign()
    example_daily_horoscope()
    example_list_all()
    example_user_profile()
    
    print("=" * 50)
    print("所有示例完成！")
    print("=" * 50)


if __name__ == "__main__":
    main()