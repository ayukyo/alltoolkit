"""
中国身份证工具测试模块

测试所有核心功能：
- 格式验证
- 校验码计算
- 15位转18位
- 出生日期提取
- 性别判断
- 年龄计算
- 地区码解析
- 综合解析
- 批量处理
"""

import unittest
from datetime import date, timedelta
from mod import (
    validate_format,
    calculate_checksum,
    validate_checksum,
    convert_15_to_18,
    extract_birth_date,
    extract_gender,
    calculate_age,
    get_province,
    get_city,
    get_district,
    parse_id,
    is_valid_id,
    generate_random_id,
    batch_parse,
    get_zodiac,
    get_chinese_zodiac,
    format_id_info,
    IDInfo,
    CHECKSUM_WEIGHTS,
    CHECKSUM_CODES,
    PROVINCE_CODES,
    DISTRICT_CODES,
)


class TestValidateFormat(unittest.TestCase):
    """测试格式验证功能"""
    
    def test_valid_18_digit_id(self):
        """测试有效的18位身份证"""
        valid, msg = validate_format('11010519491231002X')
        self.assertTrue(valid)
        self.assertEqual(msg, "")
    
    def test_valid_15_digit_id(self):
        """测试有效的15位身份证"""
        valid, msg = validate_format('110105491231002')
        self.assertTrue(valid)
        self.assertEqual(msg, "")
    
    def test_empty_id(self):
        """测试空身份证"""
        valid, msg = validate_format('')
        self.assertFalse(valid)
        self.assertEqual(msg, "身份证号码不能为空")
    
    def test_invalid_length(self):
        """测试无效长度"""
        valid, msg = validate_format('12345678')
        self.assertFalse(valid)
        self.assertEqual(msg, "身份证号码长度应为15位或18位")
        
        valid, msg = validate_format('12345678901234567890')
        self.assertFalse(valid)
        self.assertEqual(msg, "身份证号码长度应为15位或18位")
    
    def test_invalid_characters(self):
        """测试非法字符"""
        valid, msg = validate_format('1101051949123100AB')
        self.assertFalse(valid)
        self.assertEqual(msg, "身份证号码包含非法字符")
    
    def test_lowercase_x_accepted(self):
        """测试小写X会被接受"""
        valid, msg = validate_format('11010519491231002x')
        self.assertTrue(valid)


class TestChecksum(unittest.TestCase):
    """测试校验码功能"""
    
    def test_calculate_checksum_known_values(self):
        """测试已知校验码"""
        # 测试多个已知的有效身份证校验码
        test_cases = [
            ('11010519491231002', 'X'),
            ('11010519900307999', '4'),
            ('44030519900101123', 'X'),
        ]
        
        for id_17, expected_checksum in test_cases:
            result = calculate_checksum(id_17)
            self.assertEqual(result, expected_checksum)
    
    def test_calculate_checksum_invalid_length(self):
        """测试无效长度的校验码计算"""
        result = calculate_checksum('12345678')
        self.assertEqual(result, '')
    
    def test_validate_checksum_correct(self):
        """测试正确的校验码"""
        self.assertTrue(validate_checksum('11010519491231002X'))
    
    def test_validate_checksum_wrong(self):
        """测试错误的校验码"""
        self.assertFalse(validate_checksum('11010519491231002A'))
        self.assertFalse(validate_checksum('11010519491231002Y'))
    
    def test_validate_checksum_15_digit(self):
        """测试15位身份证无校验码验证"""
        # 15位身份证没有校验码
        self.assertFalse(validate_checksum('110105491231002'))


class TestConvert15To18(unittest.TestCase):
    """测试15位转18位功能"""
    
    def test_convert_basic(self):
        """测试基本转换"""
        id_15 = '110105491231002'
        id_18 = convert_15_to_18(id_15)
        self.assertEqual(len(id_18), 18)
        self.assertEqual(id_18[:6], '110105')
        self.assertEqual(id_18[6:10], '1949')
        self.assertEqual(id_18[10:14], '1231')
        self.assertEqual(id_18[14:17], '002')
    
    def test_convert_preserves_original_if_invalid(self):
        """测试无效15位身份证保持不变"""
        id_invalid = '12345'
        result = convert_15_to_18(id_invalid)
        self.assertEqual(result, id_invalid)
    
    def test_convert_all_digit(self):
        """测试转换后校验码正确"""
        id_15 = '320102850815051'
        id_18 = convert_15_to_18(id_15)
        self.assertTrue(validate_checksum(id_18))


class TestExtractBirthDate(unittest.TestCase):
    """测试出生日期提取功能"""
    
    def test_extract_from_18_digit(self):
        """测试从18位身份证提取"""
        birth = extract_birth_date('11010519491231002X')
        self.assertEqual(birth, date(1949, 12, 31))
    
    def test_extract_from_15_digit(self):
        """测试从15位身份证提取"""
        # 15位身份证年份为2位，默认补19
        birth = extract_birth_date('110105491231002')
        self.assertEqual(birth, date(1949, 12, 31))
    
    def test_extract_invalid_date(self):
        """测试无效日期"""
        birth = extract_birth_date('11010519999999999X')
        self.assertIsNone(birth)
    
    def test_extract_invalid_length(self):
        """测试无效长度"""
        birth = extract_birth_date('12345')
        self.assertIsNone(birth)
    
    def test_extract_various_dates(self):
        """测试各种日期"""
        test_cases = [
            ('11010519900101123', date(1990, 1, 1)),
            ('11010519850228123', date(1985, 2, 28)),
            ('11010520000101123', date(2000, 1, 1)),
        ]
        
        for id_num, expected in test_cases:
            birth = extract_birth_date(id_num + '4')
            self.assertEqual(birth, expected)


class TestExtractGender(unittest.TestCase):
    """测试性别判断功能"""
    
    def test_male_odd_sequence(self):
        """测试奇数顺序码为男性"""
        gender = extract_gender('11010519491231001X')  # 001 奇数
        self.assertEqual(gender, '男')
    
    def test_female_even_sequence(self):
        """测试偶数顺序码为女性"""
        gender = extract_gender('11010519491231002X')  # 002 奇数
        self.assertEqual(gender, '女')
    
    def test_gender_from_15_digit(self):
        """测试从15位身份证提取性别"""
        gender = extract_gender('110105491231003')  # 003 奇数
        self.assertEqual(gender, '男')
    
    def test_gender_invalid_length(self):
        """测试无效长度返回None"""
        gender = extract_gender('12345')
        self.assertIsNone(gender)


class TestCalculateAge(unittest.TestCase):
    """测试年龄计算功能"""
    
    def test_age_birthday_passed(self):
        """测试生日已过的年龄"""
        birth = date(1990, 6, 15)
        ref = date(2020, 12, 1)
        age = calculate_age(birth, ref)
        self.assertEqual(age, 30)
    
    def test_age_birthday_not_passed(self):
        """测试生日未过的年龄"""
        birth = date(1990, 6, 15)
        ref = date(2020, 5, 1)
        age = calculate_age(birth, ref)
        self.assertEqual(age, 29)
    
    def test_age_same_day(self):
        """测试生日当天"""
        birth = date(1990, 6, 15)
        ref = date(2020, 6, 15)
        age = calculate_age(birth, ref)
        self.assertEqual(age, 30)
    
    def test_age_today_default(self):
        """测试默认使用今天"""
        birth = date(2000, 1, 1)
        age = calculate_age(birth)
        expected = date.today().year - 2000
        # 调整预期值考虑是否过生日
        today = date.today()
        if (today.month, today.day) < (1, 1):
            expected -= 1
        self.assertEqual(age, expected)
    
    def test_age_negative_returns_zero(self):
        """测试未来出生返回0"""
        birth = date.today() + timedelta(days=1)
        age = calculate_age(birth)
        self.assertEqual(age, 0)


class TestRegionCodes(unittest.TestCase):
    """测试地区码解析功能"""
    
    def test_get_province_valid(self):
        """测试有效省份码"""
        province = get_province('11')
        self.assertEqual(province, '北京市')
        
        province = get_province('44')
        self.assertEqual(province, '广东省')
    
    def test_get_province_invalid(self):
        """测试无效省份码"""
        province = get_province('99')
        self.assertIsNone(province)
    
    def test_get_city_valid(self):
        """测试有效城市码"""
        city = get_city('4403')
        self.assertEqual(city, '深圳市')
        
        city = get_city('3201')
        self.assertEqual(city, '南京市')
    
    def test_get_city_invalid(self):
        """测试无效城市码"""
        city = get_city('9999')
        self.assertIsNone(city)
    
    def test_get_district_valid(self):
        """测试有效区县码"""
        district = get_district('110105')
        self.assertEqual(district, '朝阳区')
        
        district = get_district('310115')
        self.assertEqual(district, '浦东新区')
    
    def test_get_district_invalid(self):
        """测试无效区县码"""
        district = get_district('999999')
        self.assertIsNone(district)


class TestParseId(unittest.TestCase):
    """测试综合解析功能"""
    
    def test_parse_valid_id(self):
        """测试解析有效身份证"""
        # 构造一个有效身份证
        info = parse_id('11010519491231002X')
        self.assertTrue(info.valid)
        self.assertEqual(info.province, '北京市')
        self.assertEqual(info.birth_date, date(1949, 12, 31))
        self.assertEqual(info.gender, '女')
        self.assertTrue(info.checksum_valid)
    
    def test_parse_invalid_format(self):
        """测试解析无效格式"""
        info = parse_id('12345')
        self.assertFalse(info.valid)
        self.assertFalse(info.format_valid)
    
    def test_parse_invalid_checksum(self):
        """测试解析错误校验码"""
        info = parse_id('11010519491231002A')  # 错误校验码
        self.assertFalse(info.valid)
        self.assertFalse(info.checksum_valid)
    
    def test_parse_invalid_region(self):
        """测试解析无效地区码"""
        info = parse_id('999999194912310024')
        self.assertFalse(info.valid)
        self.assertEqual(info.error_message, "无效的地区码")
    
    def test_parse_invalid_birth_date(self):
        """测试解析无效出生日期"""
        info = parse_id('110105199913310024')
        self.assertFalse(info.valid)
        self.assertEqual(info.error_message, "无效的出生日期")
    
    def test_parse_future_birth_date(self):
        """测试未来出生日期"""
        future_year = date.today().year + 1
        info = parse_id(f'110105{future_year}0101' + '1234')
        self.assertFalse(info.valid)
        self.assertEqual(info.error_message, "出生日期不能晚于当前日期")
    
    def test_parse_15_digit_id(self):
        """测试解析15位身份证"""
        info = parse_id('110105491231002')
        # 15位会被转换为18位
        self.assertEqual(len(info.id_number), 18)
    
    def test_parse_with_reference_date(self):
        """测试使用参考日期计算年龄"""
        info = parse_id('110105199001011234', reference_date=date(2020, 6, 1))
        self.assertEqual(info.age, 30)


class TestIsValidId(unittest.TestCase):
    """测试快速验证功能"""
    
    def test_valid_id_true(self):
        """测试有效身份证返回True"""
        # 生成一个有效的测试身份证
        test_id = generate_random_id(province_code='110105', birth_date=date(1990, 1, 1), gender='男')
        self.assertTrue(is_valid_id(test_id))
    
    def test_invalid_id_false(self):
        """测试无效身份证返回False"""
        self.assertFalse(is_valid_id('12345'))
        self.assertFalse(is_valid_id('999999194912310024'))


class TestGenerateRandomId(unittest.TestCase):
    """测试随机生成功能"""
    
    def test_generate_basic(self):
        """测试基本生成"""
        id_num = generate_random_id()
        self.assertEqual(len(id_num), 18)
        self.assertTrue(validate_checksum(id_num))
    
    def test_generate_with_province(self):
        """测试指定省份"""
        id_num = generate_random_id(province_code='44')
        self.assertEqual(id_num[:2], '44')
    
    def test_generate_with_birth_date(self):
        """测试指定出生日期"""
        birth = date(1990, 6, 15)
        id_num = generate_random_id(birth_date=birth)
        self.assertEqual(id_num[6:14], '19900615')
    
    def test_generate_male(self):
        """测试生成男性身份证"""
        id_num = generate_random_id(gender='男')
        gender_digit = int(id_num[16])
        self.assertTrue(gender_digit % 2 == 1)
    
    def test_generate_female(self):
        """测试生成女性身份证"""
        id_num = generate_random_id(gender='女')
        gender_digit = int(id_num[16])
        self.assertTrue(gender_digit % 2 == 0)
    
    def test_generate_with_sequence(self):
        """测试指定顺序码"""
        id_num = generate_random_id(sequence=123)
        self.assertEqual(id_num[14:17], '123')
    
    def test_generated_id_is_valid(self):
        """测试生成的身份证都是有效的"""
        for _ in range(10):
            id_num = generate_random_id()
            self.assertTrue(is_valid_id(id_num))


class TestBatchParse(unittest.TestCase):
    """测试批量解析功能"""
    
    def test_batch_parse_multiple(self):
        """测试批量解析多个身份证"""
        ids = [
            '11010519491231002X',
            '440305199001011234',
            '320102198508150512',
        ]
        results = batch_parse(ids)
        self.assertEqual(len(results), 3)
        for result in results:
            self.assertIsInstance(result, IDInfo)
    
    def test_batch_parse_empty(self):
        """测试空列表"""
        results = batch_parse([])
        self.assertEqual(len(results), 0)
    
    def test_batch_parse_with_invalid(self):
        """测试包含无效身份证"""
        ids = ['11010519491231002X', 'invalid', '32010219850815051X']
        results = batch_parse(ids)
        self.assertEqual(len(results), 3)
        self.assertTrue(results[0].valid)
        self.assertFalse(results[1].valid)
        self.assertTrue(results[2].valid)


class TestZodiac(unittest.TestCase):
    """测试星座功能"""
    
    def test_zodiac_capricorn(self):
        """测试摩羯座"""
        self.assertEqual(get_zodiac(date(2000, 1, 1)), '摩羯座')
        self.assertEqual(get_zodiac(date(2000, 12, 25)), '摩羯座')
    
    def test_zodiac_aquarius(self):
        """测试水瓶座"""
        self.assertEqual(get_zodiac(date(2000, 2, 1)), '水瓶座')
    
    def test_zodiac_pisces(self):
        """测试双鱼座"""
        self.assertEqual(get_zodiac(date(2000, 3, 15)), '双鱼座')
    
    def test_zodiac_aries(self):
        """测试白羊座"""
        self.assertEqual(get_zodiac(date(2000, 4, 1)), '白羊座')
    
    def test_zodiac_taurus(self):
        """测试金牛座"""
        self.assertEqual(get_zodiac(date(2000, 5, 10)), '金牛座')
    
    def test_zodiac_gemini(self):
        """测试双子座"""
        self.assertEqual(get_zodiac(date(2000, 6, 10)), '双子座')
    
    def test_zodiac_cancer(self):
        """测试巨蟹座"""
        self.assertEqual(get_zodiac(date(2000, 7, 10)), '巨蟹座')
    
    def test_zodiac_leo(self):
        """测试狮子座"""
        self.assertEqual(get_zodiac(date(2000, 8, 10)), '狮子座')
    
    def test_zodiac_virgo(self):
        """测试处女座"""
        self.assertEqual(get_zodiac(date(2000, 9, 10)), '处女座')
    
    def test_zodiac_libra(self):
        """测试天秤座"""
        self.assertEqual(get_zodiac(date(2000, 10, 10)), '天秤座')
    
    def test_zodiac_scorpio(self):
        """测试天蝎座"""
        self.assertEqual(get_zodiac(date(2000, 11, 10)), '天蝎座')
    
    def test_zodiac_sagittarius(self):
        """测试射手座"""
        self.assertEqual(get_zodiac(date(2000, 12, 10)), '射手座')


class TestChineseZodiac(unittest.TestCase):
    """测试生肖功能"""
    
    def test_chinese_zodiac_cycle(self):
        """测试生肖循环"""
        # 1900年是鼠年，以此类推
        expected_zodiacs = ['鼠', '牛', '虎', '兔', '龙', '蛇', '马', '羊', '猴', '鸡', '狗', '猪']
        for i, zodiac in enumerate(expected_zodiacs):
            self.assertEqual(get_chinese_zodiac(date(1900 + i, 1, 1)), zodiac)
    
    def test_chinese_zodiac_known_years(self):
        """测试已知年份"""
        self.assertEqual(get_chinese_zodiac(date(2000, 1, 1)), '龙')
        self.assertEqual(get_chinese_zodiac(date(2024, 1, 1)), '龙')
        self.assertEqual(get_chinese_zodiac(date(2025, 1, 1)), '蛇')


class TestFormatIdInfo(unittest.TestCase):
    """测试格式化功能"""
    
    def test_format_valid_id(self):
        """测试格式化有效身份证"""
        info = parse_id('11010519491231002X')
        formatted = format_id_info(info)
        self.assertIn('身份证号码', formatted)
        self.assertIn('省份', formatted)
        self.assertIn('出生日期', formatted)
        self.assertIn('性别', formatted)
        self.assertIn('年龄', formatted)
        self.assertIn('星座', formatted)
        self.assertIn('生肖', formatted)
    
    def test_format_invalid_id(self):
        """测试格式化无效身份证"""
        info = parse_id('12345')
        formatted = format_id_info(info)
        self.assertIn('无效身份证', formatted)


class TestConstants(unittest.TestCase):
    """测试常量数据"""
    
    def test_checksum_weights_length(self):
        """测试校验码权重长度"""
        self.assertEqual(len(CHECKSUM_WEIGHTS), 17)
    
    def test_checksum_codes_length(self):
        """测试校验码对照表长度"""
        self.assertEqual(len(CHECKSUM_CODES), 11)
    
    def test_province_codes_complete(self):
        """测试省份代码覆盖"""
        # 测试所有省份代码都有映射
        for code in ['11', '12', '13', '31', '44', '51']:
            self.assertIn(code, PROVINCE_CODES)
    
    def test_district_codes_format(self):
        """测试区县代码格式"""
        for code in DISTRICT_CODES:
            self.assertEqual(len(code), 6)


class TestEdgeCases(unittest.TestCase):
    """测试边界情况"""
    
    def test_very_old_birth_date(self):
        """测试非常老的出生日期"""
        # 构造一个校验码正确的1899年出生身份证（超过126岁，不合理）
        id_17 = '11010518990101123'
        checksum = calculate_checksum(id_17)
        id_18 = id_17 + checksum
        info = parse_id(id_18)
        self.assertFalse(info.valid)
        self.assertEqual(info.error_message, "出生年份不合理")
    
    def test_whitespace_handling(self):
        """测试空格处理"""
        info = parse_id(' 11010519491231002X ')
        self.assertEqual(info.id_number, '11010519491231002X')
    
    def test_today_as_birth_date(self):
        """测试今天出生"""
        today_str = date.today().strftime('%Y%m%d')
        id_17 = '110105' + today_str + '001'
        checksum = calculate_checksum(id_17)
        id_18 = id_17 + checksum
        info = parse_id(id_18)
        self.assertTrue(info.valid)
        self.assertEqual(info.age, 0)
    
    def test_leap_year_birth(self):
        """测试闰年出生"""
        info = parse_id('11010520000229' + '1234')
        # 2000年是闰年，2月29日有效
        if validate_checksum('11010520000229' + '1234'):
            self.assertEqual(info.birth_date, date(2000, 2, 29))
        else:
            # 如果校验码不对，构造正确的
            id_17 = '11010520000229123'
            checksum = calculate_checksum(id_17)
            info = parse_id(id_17 + checksum)
            self.assertEqual(info.birth_date, date(2000, 2, 29))


if __name__ == '__main__':
    unittest.main(verbosity=2)