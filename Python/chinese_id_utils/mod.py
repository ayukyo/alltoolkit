"""
中国身份证工具模块 (Chinese ID Card Utilities)

提供中国大陆居民身份证号码的验证、解析和信息提取功能。

功能:
- 身份证号码格式验证
- 校验码计算与验证
- 地区码解析（省市区）
- 出生日期提取
- 性别判断
- 年龄计算
- 十五位转十八位
- 身份证信息批量解析
"""

from datetime import datetime, date
from typing import Optional, Dict, List, Tuple, NamedTuple


# 校验码权重
CHECKSUM_WEIGHTS = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]

# 校验码对照表
CHECKSUM_CODES = ['1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2']

# 省份代码映射
PROVINCE_CODES = {
    '11': '北京市', '12': '天津市', '13': '河北省', '14': '山西省', '15': '内蒙古自治区',
    '21': '辽宁省', '22': '吉林省', '23': '黑龙江省',
    '31': '上海市', '32': '江苏省', '33': '浙江省', '34': '安徽省', '35': '福建省',
    '36': '江西省', '37': '山东省',
    '41': '河南省', '42': '湖北省', '43': '湖南省', '44': '广东省', '45': '广西壮族自治区',
    '46': '海南省',
    '50': '重庆市', '51': '四川省', '52': '贵州省', '53': '云南省', '54': '西藏自治区',
    '61': '陕西省', '62': '甘肃省', '63': '青海省', '64': '宁夏回族自治区', '65': '新疆维吾尔自治区',
    '71': '台湾省', '81': '香港特别行政区', '82': '澳门特别行政区',
    # 常见的城市代码
    '1101': '北京市市辖区', '1201': '天津市市辖区', '1301': '石家庄市',
    '1401': '太原市', '1501': '呼和浩特市', '2101': '沈阳市', '2102': '大连市',
    '2201': '长春市', '2301': '哈尔滨市', '3101': '上海市市辖区',
    '3201': '南京市', '3202': '无锡市', '3205': '苏州市',
    '3301': '杭州市', '3302': '宁波市', '3401': '合肥市',
    '3501': '福州市', '3502': '厦门市', '3601': '南昌市',
    '3701': '济南市', '3702': '青岛市', '4101': '郑州市',
    '4201': '武汉市', '4301': '长沙市', '4401': '广州市',
    '4403': '深圳市', '4404': '珠海市', '4501': '南宁市',
    '4601': '海口市', '4602': '三亚市', '5001': '重庆市市辖区',
    '5101': '成都市', '5201': '贵阳市', '5301': '昆明市',
    '5401': '拉萨市', '6101': '西安市', '6201': '兰州市',
    '6301': '西宁市', '6401': '银川市', '6501': '乌鲁木齐市',
}

# 部分区县代码（常见城市的主要区）
DISTRICT_CODES = {
    # 北京市
    '110101': '东城区', '110102': '西城区', '110105': '朝阳区', '110106': '丰台区',
    '110107': '石景山区', '110108': '海淀区', '110109': '门头沟区', '110111': '房山区',
    '110112': '通州区', '110113': '顺义区', '110114': '昌平区', '110115': '大兴区',
    '110116': '怀柔区', '110117': '平谷区', '110118': '密云区', '110119': '延庆区',
    # 上海市
    '310101': '黄浦区', '310104': '徐汇区', '310105': '长宁区', '310106': '静安区',
    '310107': '普陀区', '310109': '虹口区', '310110': '杨浦区', '310112': '闵行区',
    '310113': '宝山区', '310114': '嘉定区', '310115': '浦东新区', '310116': '金山区',
    '310117': '松江区', '310118': '青浦区', '310120': '奉贤区', '310151': '崇明区',
    # 广州市
    '440103': '荔湾区', '440104': '越秀区', '440105': '海珠区', '440106': '天河区',
    '440111': '白云区', '440112': '黄埔区', '440113': '番禺区', '440114': '花都区',
    '440115': '南沙区', '440117': '从化区', '440118': '增城区',
    # 深圳市
    '440303': '罗湖区', '440304': '福田区', '440305': '南山区', '440306': '宝安区',
    '440307': '龙岗区', '440308': '盐田区', '440309': '龙华区', '440310': '坪山区',
    '440311': '光明区',
    # 杭州市
    '330102': '上城区', '330103': '下城区', '330104': '江干区', '330105': '拱墅区',
    '330106': '西湖区', '330108': '滨江区', '330109': '萧山区', '330110': '余杭区',
    '330111': '富阳区', '330112': '临安区',
    # 成都市
    '510104': '锦江区', '510105': '青羊区', '510106': '金牛区', '510107': '武侯区',
    '510108': '成华区', '510112': '龙泉驿区', '510113': '青白江区', '510114': '新都区',
    '510115': '温江区', '510116': '双流区', '510117': '郫都区',
}


class IDInfo(NamedTuple):
    """身份证解析结果"""
    valid: bool
    id_number: str
    province: Optional[str]
    city: Optional[str]
    district: Optional[str]
    birth_date: Optional[date]
    gender: Optional[str]  # '男' or '女'
    age: Optional[int]
    checksum_valid: bool
    format_valid: bool
    error_message: Optional[str]


def validate_format(id_number: str) -> Tuple[bool, str]:
    """
    验证身份证号码格式
    
    Args:
        id_number: 身份证号码（15位或18位）
    
    Returns:
        (是否有效, 错误信息)
    """
    if not id_number:
        return False, "身份证号码不能为空"
    
    id_number = id_number.strip().upper()
    
    # 检查长度
    if len(id_number) not in (15, 18):
        return False, "身份证号码长度应为15位或18位"
    
    # 检查字符
    if len(id_number) == 18:
        if not id_number[:-1].isdigit() or id_number[-1] not in '0123456789X':
            return False, "身份证号码包含非法字符"
    else:  # 15位
        if not id_number.isdigit():
            return False, "身份证号码包含非法字符"
    
    return True, ""


def calculate_checksum(id_number_17: str) -> str:
    """
    根据前17位计算校验码
    
    Args:
        id_number_17: 身份证号码前17位
    
    Returns:
        第18位校验码
    """
    if len(id_number_17) != 17 or not id_number_17.isdigit():
        return ''
    
    weighted_sum = sum(int(id_number_17[i]) * CHECKSUM_WEIGHTS[i] for i in range(17))
    remainder = weighted_sum % 11
    return CHECKSUM_CODES[remainder]


def validate_checksum(id_number: str) -> bool:
    """
    验证身份证校验码
    
    Args:
        id_number: 18位身份证号码
    
    Returns:
        校验码是否正确
    """
    if len(id_number) != 18:
        return False
    
    id_number = id_number.upper()
    expected = calculate_checksum(id_number[:17])
    return id_number[-1] == expected


def convert_15_to_18(id_number_15: str) -> str:
    """
    将15位身份证号码转换为18位
    
    Args:
        id_number_15: 15位身份证号码
    
    Returns:
        18位身份证号码
    """
    if len(id_number_15) != 15:
        return id_number_15
    
    # 15位身份证出生年份为2位，转换为18位时补全为4位
    # 15位身份证一般是19xx年发的
    id_17 = id_number_15[:6] + '19' + id_number_15[6:]
    checksum = calculate_checksum(id_17)
    return id_17 + checksum


def extract_birth_date(id_number: str) -> Optional[date]:
    """
    从身份证号码提取出生日期
    
    Args:
        id_number: 身份证号码
    
    Returns:
        出生日期，解析失败返回None
    """
    id_number = id_number.strip()
    
    if len(id_number) == 15:
        # 15位身份证：年份为2位（1900-1999）
        year = int('19' + id_number[6:8])
        month = int(id_number[8:10])
        day = int(id_number[10:12])
    elif len(id_number) == 18:
        year = int(id_number[6:10])
        month = int(id_number[10:12])
        day = int(id_number[12:14])
    else:
        return None
    
    try:
        return date(year, month, day)
    except ValueError:
        return None


def extract_gender(id_number: str) -> Optional[str]:
    """
    从身份证号码判断性别
    
    Args:
        id_number: 身份证号码
    
    Returns:
        '男' 或 '女'，解析失败返回None
    """
    id_number = id_number.strip()
    
    if len(id_number) == 15:
        gender_digit = int(id_number[14])
    elif len(id_number) == 18:
        gender_digit = int(id_number[16])
    else:
        return None
    
    return '男' if gender_digit % 2 == 1 else '女'


def calculate_age(birth_date: date, reference_date: Optional[date] = None) -> int:
    """
    计算年龄
    
    Args:
        birth_date: 出生日期
        reference_date: 参考日期，默认为今天
    
    Returns:
        年龄（周岁）
    """
    if reference_date is None:
        reference_date = date.today()
    
    age = reference_date.year - birth_date.year
    
    # 如果今年生日还没过，年龄减1
    if (reference_date.month, reference_date.day) < (birth_date.month, birth_date.day):
        age -= 1
    
    return max(0, age)


def get_province(region_code: str) -> Optional[str]:
    """
    根据地区码获取省份名称
    
    Args:
        region_code: 地区码（2位或更多位）
    
    Returns:
        省份名称
    """
    province_code = region_code[:2]
    return PROVINCE_CODES.get(province_code)


def get_city(region_code: str) -> Optional[str]:
    """
    根据地区码获取城市名称
    
    Args:
        region_code: 地区码（4位或更多位）
    
    Returns:
        城市名称
    """
    city_code = region_code[:4]
    return PROVINCE_CODES.get(city_code)


def get_district(region_code: str) -> Optional[str]:
    """
    根据地区码获取区县名称
    
    Args:
        region_code: 地区码（6位）
    
    Returns:
        区县名称
    """
    return DISTRICT_CODES.get(region_code[:6])


def parse_id(id_number: str, reference_date: Optional[date] = None) -> IDInfo:
    """
    解析身份证号码，返回完整信息
    
    Args:
        id_number: 身份证号码
        reference_date: 参考日期（用于计算年龄），默认为今天
    
    Returns:
        IDInfo 命名元组，包含所有解析结果
    """
    id_number = id_number.strip().upper()
    
    # 格式验证
    format_valid, error_msg = validate_format(id_number)
    if not format_valid:
        return IDInfo(
            valid=False, id_number=id_number, province=None, city=None,
            district=None, birth_date=None, gender=None, age=None,
            checksum_valid=False, format_valid=False, error_message=error_msg
        )
    
    # 如果是15位，先转换为18位
    if len(id_number) == 15:
        id_number = convert_15_to_18(id_number)
    
    # 校验码验证
    checksum_valid = validate_checksum(id_number)
    
    # 提取地区码
    region_code = id_number[:6]
    province = get_province(region_code)
    city = get_city(region_code)
    district = get_district(region_code)
    
    if province is None:
        return IDInfo(
            valid=False, id_number=id_number, province=None, city=None,
            district=None, birth_date=None, gender=None, age=None,
            checksum_valid=checksum_valid, format_valid=True,
            error_message="无效的地区码"
        )
    
    # 提取出生日期
    birth_date = extract_birth_date(id_number)
    if birth_date is None:
        return IDInfo(
            valid=False, id_number=id_number, province=province, city=city,
            district=district, birth_date=None, gender=None, age=None,
            checksum_valid=checksum_valid, format_valid=True,
            error_message="无效的出生日期"
        )
    
    # 检查出生日期是否合理
    today = reference_date or date.today()
    if birth_date > today:
        return IDInfo(
            valid=False, id_number=id_number, province=province, city=city,
            district=district, birth_date=birth_date, gender=None, age=None,
            checksum_valid=checksum_valid, format_valid=True,
            error_message="出生日期不能晚于当前日期"
        )
    
    if birth_date.year < 1900:
        return IDInfo(
            valid=False, id_number=id_number, province=province, city=city,
            district=district, birth_date=birth_date, gender=None, age=None,
            checksum_valid=checksum_valid, format_valid=True,
            error_message="出生年份不合理"
        )
    
    # 提取性别
    gender = extract_gender(id_number)
    
    # 计算年龄
    age = calculate_age(birth_date, reference_date)
    
    # 综合有效性判断
    valid = checksum_valid and format_valid
    
    return IDInfo(
        valid=valid,
        id_number=id_number,
        province=province,
        city=city,
        district=district,
        birth_date=birth_date,
        gender=gender,
        age=age,
        checksum_valid=checksum_valid,
        format_valid=format_valid,
        error_message=None if valid else "校验码错误"
    )


def is_valid_id(id_number: str) -> bool:
    """
    快速验证身份证号码是否有效
    
    Args:
        id_number: 身份证号码
    
    Returns:
        是否有效
    """
    result = parse_id(id_number)
    return result.valid


def generate_random_id(
    province_code: str = '11',
    birth_date: Optional[date] = None,
    gender: str = '男',
    sequence: Optional[int] = None
) -> str:
    """
    生成随机的身份证号码（用于测试）
    
    Args:
        province_code: 省份代码（6位，默认北京）
        birth_date: 出生日期，默认为2000年1月1日
        gender: 性别，'男' 或 '女'
        sequence: 顺序码（3位），不指定则随机生成
    
    Returns:
        18位身份证号码
    """
    import random
    
    # 处理出生日期
    if birth_date is None:
        birth_date = date(2000, 1, 1)
    
    birth_str = birth_date.strftime('%Y%m%d')
    
    # 处理顺序码
    if sequence is None:
        base = random.randint(0, 499)
        if gender == '男':
            sequence = base * 2 + 1  # 奇数为男
        else:
            sequence = base * 2  # 偶数为女
    else:
        # 调整顺序码以匹配性别
        if gender == '男' and sequence % 2 == 0:
            sequence += 1
        elif gender == '女' and sequence % 2 == 1:
            sequence -= 1
    
    sequence_str = f'{sequence:03d}'
    
    # 补全地区码到6位
    if len(province_code) == 2:
        province_code = province_code + '01' + '01'  # 默认省会城市第一个区
    elif len(province_code) == 4:
        province_code = province_code + '01'
    
    # 构建前17位
    id_17 = province_code + birth_str + sequence_str
    
    # 计算校验码
    checksum = calculate_checksum(id_17)
    
    return id_17 + checksum


def batch_parse(id_numbers: List[str], reference_date: Optional[date] = None) -> List[IDInfo]:
    """
    批量解析身份证号码
    
    Args:
        id_numbers: 身份证号码列表
        reference_date: 参考日期
    
    Returns:
        IDInfo列表
    """
    return [parse_id(id_num, reference_date) for id_num in id_numbers]


def get_zodiac(birth_date: date) -> str:
    """
    根据出生日期获取星座
    
    Args:
        birth_date: 出生日期
    
    Returns:
        星座名称
    """
    month, day = birth_date.month, birth_date.day
    
    zodiac_dates = [
        ((1, 20), (2, 18), '水瓶座'),
        ((2, 19), (3, 20), '双鱼座'),
        ((3, 21), (4, 19), '白羊座'),
        ((4, 20), (5, 20), '金牛座'),
        ((5, 21), (6, 21), '双子座'),
        ((6, 22), (7, 22), '巨蟹座'),
        ((7, 23), (8, 22), '狮子座'),
        ((8, 23), (9, 22), '处女座'),
        ((9, 23), (10, 23), '天秤座'),
        ((10, 24), (11, 22), '天蝎座'),
        ((11, 23), (12, 21), '射手座'),
        ((12, 22), (12, 31), '摩羯座'),
    ]
    
    for (start_m, start_d), (end_m, end_d), zodiac in zodiac_dates:
        if (month == start_m and day >= start_d) or (month == end_m and day <= end_d):
            return zodiac
    
    # 摩羯座跨年特殊处理
    if month == 1 and day <= 19:
        return '摩羯座'
    
    return '未知'


def get_chinese_zodiac(birth_date: date) -> str:
    """
    根据出生日期获取生肖
    
    Args:
        birth_date: 出生日期
    
    Returns:
        生肖名称
    """
    # 1900年是鼠年，生肖顺序：鼠牛虎兔龙蛇马羊猴鸡狗猪
    zodiacs = ['鼠', '牛', '虎', '兔', '龙', '蛇', '马', '羊', '猴', '鸡', '狗', '猪']
    return zodiacs[(birth_date.year - 1900) % 12]


def format_id_info(info: IDInfo) -> str:
    """
    格式化身份证信息为可读字符串
    
    Args:
        info: IDInfo对象
    
    Returns:
        格式化后的字符串
    """
    if not info.valid:
        return f"无效身份证: {info.error_message}"
    
    lines = [
        f"身份证号码: {info.id_number}",
        f"省份: {info.province or '未知'}",
    ]
    
    if info.city:
        lines.append(f"城市: {info.city}")
    if info.district:
        lines.append(f"区县: {info.district}")
    
    lines.extend([
        f"出生日期: {info.birth_date}",
        f"性别: {info.gender}",
        f"年龄: {info.age}岁",
        f"星座: {get_zodiac(info.birth_date)}",
        f"生肖: {get_chinese_zodiac(info.birth_date)}",
        f"校验码: {'正确' if info.checksum_valid else '错误'}",
    ])
    
    return '\n'.join(lines)


if __name__ == '__main__':
    # 示例用法
    test_ids = [
        '11010519491231002X',  # 有效身份证
        '11010519900307888X',  # 另一个有效身份证
        '440305199001011234',  # 深圳
        '320102198508150512',  # 南京
        '123456789012345678',  # 无效
    ]
    
    print("=" * 50)
    print("中国身份证验证工具示例")
    print("=" * 50)
    
    for id_num in test_ids:
        info = parse_id(id_num)
        print(f"\n身份证: {id_num}")
        print("-" * 30)
        print(format_id_info(info))