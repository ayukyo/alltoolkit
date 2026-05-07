"""
SWIFT/BIC Utilities - SWIFT银行代码验证工具模块

提供SWIFT/BIC代码的完整验证、解析和生成功能。
SWIFT代码（也称BIC代码）是国际银行识别的标准代码。
零依赖，仅使用 Python 标准库。

Author: AllToolkit
Version: 1.0.0
"""

from typing import Optional, Dict, List, Tuple, Any
from enum import Enum
import re


class SwiftCodeType(Enum):
    """SWIFT代码类型"""
    PRIMARY = "主要办公机构"
    BRANCH = "特定分行"
    GENERAL = "通用代码"


class SwiftNetworkStatus(Enum):
    """SWIFT网络状态"""
    ACTIVE = "活跃"
    PASSIVE = "被动"
    TEST = "测试"
    DELETED = "已删除"


# 国家代码数据（ISO 3166-1 alpha-2）
_COUNTRY_DATA: Dict[str, Tuple[str, str, str]] = {
    "AD": ("安道尔", "Andorra", "EUR"),
    "AE": ("阿联酋", "United Arab Emirates", "AED"),
    "AF": ("阿富汗", "Afghanistan", "AFN"),
    "AG": ("安提瓜和巴布达", "Antigua and Barbuda", "XCD"),
    "AI": ("安圭拉", "Anguilla", "XCD"),
    "AL": ("阿尔巴尼亚", "Albania", "ALL"),
    "AM": ("亚美尼亚", "Armenia", "AMD"),
    "AO": ("安哥拉", "Angola", "AOA"),
    "AQ": ("南极洲", "Antarctica", ""),
    "AR": ("阿根廷", "Argentina", "ARS"),
    "AS": ("美属萨摩亚", "American Samoa", "USD"),
    "AT": ("奥地利", "Austria", "EUR"),
    "AU": ("澳大利亚", "Australia", "AUD"),
    "AW": ("阿鲁巴", "Aruba", "AWG"),
    "AX": ("奥兰群岛", "Åland Islands", "EUR"),
    "AZ": ("阿塞拜疆", "Azerbaijan", "AZN"),
    "BA": ("波黑", "Bosnia and Herzegovina", "BAM"),
    "BB": ("巴巴多斯", "Barbados", "BBD"),
    "BD": ("孟加拉", "Bangladesh", "BDT"),
    "BE": ("比利时", "Belgium", "EUR"),
    "BF": ("布基纳法索", "Burkina Faso", "XOF"),
    "BG": ("保加利亚", "Bulgaria", "BGN"),
    "BH": ("巴林", "Bahrain", "BHD"),
    "BI": ("布隆迪", "Burundi", "BIF"),
    "BJ": ("贝宁", "Benin", "XOF"),
    "BL": ("圣巴泰勒米", "Saint Barthélemy", "EUR"),
    "BM": ("百慕大", "Bermuda", "BMD"),
    "BN": ("文莱", "Brunei", "BND"),
    "BO": ("玻利维亚", "Bolivia", "BOB"),
    "BQ": ("荷兰加勒比", "Caribbean Netherlands", "USD"),
    "BR": ("巴西", "Brazil", "BRL"),
    "BS": ("巴哈马", "Bahamas", "BSD"),
    "BT": ("不丹", "Bhutan", "BTN"),
    "BV": ("布韦岛", "Bouvet Island", "NOK"),
    "BW": ("博茨瓦纳", "Botswana", "BWP"),
    "BY": ("白俄罗斯", "Belarus", "BYN"),
    "BZ": ("伯利兹", "Belize", "BZD"),
    "CA": ("加拿大", "Canada", "CAD"),
    "CC": ("科科斯群岛", "Cocos Islands", "AUD"),
    "CD": ("刚果（金）", "Democratic Republic of the Congo", "CDF"),
    "CF": ("中非共和国", "Central African Republic", "XAF"),
    "CG": ("刚果（布）", "Republic of the Congo", "XAF"),
    "CH": ("瑞士", "Switzerland", "CHF"),
    "CI": ("科特迪瓦", "Côte d'Ivoire", "XOF"),
    "CK": ("库克群岛", "Cook Islands", "NZD"),
    "CL": ("智利", "Chile", "CLP"),
    "CM": ("喀麦隆", "Cameroon", "XAF"),
    "CN": ("中国", "China", "CNY"),
    "CO": ("哥伦比亚", "Colombia", "COP"),
    "CR": ("哥斯达黎加", "Costa Rica", "CRC"),
    "CU": ("古巴", "Cuba", "CUP"),
    "CV": ("佛得角", "Cape Verde", "CVE"),
    "CW": ("库拉索", "Curaçao", "ANG"),
    "CX": ("圣诞岛", "Christmas Island", "AUD"),
    "CY": ("塞浦路斯", "Cyprus", "EUR"),
    "CZ": ("捷克", "Czech Republic", "CZK"),
    "DE": ("德国", "Germany", "EUR"),
    "DJ": ("吉布提", "Djibouti", "DJF"),
    "DK": ("丹麦", "Denmark", "DKK"),
    "DM": ("多米尼克", "Dominica", "XCD"),
    "DO": ("多米尼加", "Dominican Republic", "DOP"),
    "DZ": ("阿尔及利亚", "Algeria", "DZD"),
    "EC": ("厄瓜多尔", "Ecuador", "USD"),
    "EE": ("爱沙尼亚", "Estonia", "EUR"),
    "EG": ("埃及", "Egypt", "EGP"),
    "EH": ("西撒哈拉", "Western Sahara", "MAD"),
    "ER": ("厄立特里亚", "Eritrea", "ERN"),
    "ES": ("西班牙", "Spain", "EUR"),
    "ET": ("埃塞俄比亚", "Ethiopia", "ETB"),
    "FI": ("芬兰", "Finland", "EUR"),
    "FJ": ("斐济", "Fiji", "FJD"),
    "FK": ("福克兰群岛", "Falkland Islands", "FKP"),
    "FM": ("密克罗尼西亚", "Micronesia", "USD"),
    "FO": ("法罗群岛", "Faroe Islands", "DKK"),
    "FR": ("法国", "France", "EUR"),
    "GA": ("加蓬", "Gabon", "XAF"),
    "GB": ("英国", "United Kingdom", "GBP"),
    "GD": ("格林纳达", "Grenada", "XCD"),
    "GE": ("格鲁吉亚", "Georgia", "GEL"),
    "GF": ("法属圭亚那", "French Guiana", "EUR"),
    "GG": ("根西", "Guernsey", "GBP"),
    "GH": ("加纳", "Ghana", "GHS"),
    "GI": ("直布罗陀", "Gibraltar", "GIP"),
    "GL": ("格陵兰", "Greenland", "DKK"),
    "GM": ("冈比亚", "Gambia", "GMD"),
    "GN": ("几内亚", "Guinea", "GNF"),
    "GP": ("瓜德罗普", "Guadeloupe", "EUR"),
    "GQ": ("赤道几内亚", "Equatorial Guinea", "XAF"),
    "GR": ("希腊", "Greece", "EUR"),
    "GS": ("南乔治亚岛", "South Georgia", "GBP"),
    "GT": ("危地马拉", "Guatemala", "GTQ"),
    "GU": ("关岛", "Guam", "USD"),
    "GW": ("几内亚比绍", "Guinea-Bissau", "XOF"),
    "GY": ("圭亚那", "Guyana", "GYD"),
    "HK": ("香港", "Hong Kong", "HKD"),
    "HM": ("赫德岛", "Heard Island", "AUD"),
    "HN": ("洪都拉斯", "Honduras", "HNL"),
    "HR": ("克罗地亚", "Croatia", "EUR"),
    "HT": ("海地", "Haiti", "HTG"),
    "HU": ("匈牙利", "Hungary", "HUF"),
    "ID": ("印尼", "Indonesia", "IDR"),
    "IE": ("爱尔兰", "Ireland", "EUR"),
    "IL": ("以色列", "Israel", "ILS"),
    "IM": ("马恩岛", "Isle of Man", "GBP"),
    "IN": ("印度", "India", "INR"),
    "IO": ("英属印度洋领地", "British Indian Ocean Territory", "USD"),
    "IQ": ("伊拉克", "Iraq", "IQD"),
    "IR": ("伊朗", "Iran", "IRR"),
    "IS": ("冰岛", "Iceland", "ISK"),
    "IT": ("意大利", "Italy", "EUR"),
    "JE": ("泽西", "Jersey", "GBP"),
    "JM": ("牙买加", "Jamaica", "JMD"),
    "JO": ("约旦", "Jordan", "JOD"),
    "JP": ("日本", "Japan", "JPY"),
    "KE": ("肯尼亚", "Kenya", "KES"),
    "KG": ("吉尔吉斯斯坦", "Kyrgyzstan", "KGS"),
    "KH": ("柬埔寨", "Cambodia", "KHR"),
    "KI": ("基里巴斯", "Kiribati", "AUD"),
    "KM": ("科摩罗", "Comoros", "KMF"),
    "KN": ("圣基茨和尼维斯", "Saint Kitts and Nevis", "XCD"),
    "KP": ("朝鲜", "North Korea", "KPW"),
    "KR": ("韩国", "South Korea", "KRW"),
    "KW": ("科威特", "Kuwait", "KWD"),
    "KY": ("开曼群岛", "Cayman Islands", "KYD"),
    "KZ": ("哈萨克斯坦", "Kazakhstan", "KZT"),
    "LA": ("老挝", "Laos", "LAK"),
    "LB": ("黎巴嫩", "Lebanon", "LBP"),
    "LC": ("圣卢西亚", "Saint Lucia", "XCD"),
    "LI": ("列支敦士登", "Liechtenstein", "CHF"),
    "LK": ("斯里兰卡", "Sri Lanka", "LKR"),
    "LR": ("利比里亚", "Liberia", "LRD"),
    "LS": ("莱索托", "Lesotho", "LSL"),
    "LT": ("立陶宛", "Lithuania", "EUR"),
    "LU": ("卢森堡", "Luxembourg", "EUR"),
    "LV": ("拉脱维亚", "Latvia", "EUR"),
    "LY": ("利比亚", "Libya", "LYD"),
    "MA": ("摩洛哥", "Morocco", "MAD"),
    "MC": ("摩纳哥", "Monaco", "EUR"),
    "MD": ("摩尔多瓦", "Moldova", "MDL"),
    "ME": ("黑山", "Montenegro", "EUR"),
    "MF": ("法属圣马丁", "Saint Martin", "EUR"),
    "MG": ("马达加斯加", "Madagascar", "MGA"),
    "MH": ("马绍尔群岛", "Marshall Islands", "USD"),
    "MK": ("北马其顿", "North Macedonia", "MKD"),
    "ML": ("马里", "Mali", "XOF"),
    "MM": ("缅甸", "Myanmar", "MMK"),
    "MN": ("蒙古", "Mongolia", "MNT"),
    "MO": ("澳门", "Macau", "MOP"),
    "MP": ("北马里亚纳群岛", "Northern Mariana Islands", "USD"),
    "MQ": ("马提尼克", "Martinique", "EUR"),
    "MR": ("毛里塔尼亚", "Mauritania", "MRU"),
    "MS": ("蒙特塞拉特", "Montserrat", "XCD"),
    "MT": ("马耳他", "Malta", "EUR"),
    "MU": ("毛里求斯", "Mauritius", "MUR"),
    "MV": ("马尔代夫", "Maldives", "MVR"),
    "MW": ("马拉维", "Malawi", "MWK"),
    "MX": ("墨西哥", "Mexico", "MXN"),
    "MY": ("马来西亚", "Malaysia", "MYR"),
    "MZ": ("莫桑比克", "Mozambique", "MZN"),
    "NA": ("纳米比亚", "Namibia", "NAD"),
    "NC": ("新喀里多尼亚", "New Caledonia", "XPF"),
    "NE": ("尼日尔", "Niger", "XOF"),
    "NF": ("诺福克岛", "Norfolk Island", "AUD"),
    "NG": ("尼日利亚", "Nigeria", "NGN"),
    "NI": ("尼加拉瓜", "Nicaragua", "NIO"),
    "NL": ("荷兰", "Netherlands", "EUR"),
    "NO": ("挪威", "Norway", "NOK"),
    "NP": ("尼泊尔", "Nepal", "NPR"),
    "NR": ("瑙鲁", "Nauru", "AUD"),
    "NU": ("纽埃", "Niue", "NZD"),
    "NZ": ("新西兰", "New Zealand", "NZD"),
    "OM": ("阿曼", "Oman", "OMR"),
    "PA": ("巴拿马", "Panama", "PAB"),
    "PE": ("秘鲁", "Peru", "PEN"),
    "PF": ("法属波利尼西亚", "French Polynesia", "XPF"),
    "PG": ("巴布亚新几内亚", "Papua New Guinea", "PGK"),
    "PH": ("菲律宾", "Philippines", "PHP"),
    "PK": ("巴基斯坦", "Pakistan", "PKR"),
    "PL": ("波兰", "Poland", "PLN"),
    "PM": ("圣皮埃尔和密克隆", "Saint Pierre and Miquelon", "EUR"),
    "PN": ("皮特凯恩群岛", "Pitcairn Islands", "NZD"),
    "PR": ("波多黎各", "Puerto Rico", "USD"),
    "PS": ("巴勒斯坦", "Palestine", "ILS"),
    "PT": ("葡萄牙", "Portugal", "EUR"),
    "PW": ("帕劳", "Palau", "USD"),
    "PY": ("巴拉圭", "Paraguay", "PYG"),
    "QA": ("卡塔尔", "Qatar", "QAR"),
    "RE": ("留尼汪", "Réunion", "EUR"),
    "RO": ("罗马尼亚", "Romania", "RON"),
    "RS": ("塞尔维亚", "Serbia", "RSD"),
    "RU": ("俄罗斯", "Russia", "RUB"),
    "RW": ("卢旺达", "Rwanda", "RWF"),
    "SA": ("沙特阿拉伯", "Saudi Arabia", "SAR"),
    "SB": ("所罗门群岛", "Solomon Islands", "SBD"),
    "SC": ("塞舌尔", "Seychelles", "SCR"),
    "SD": ("苏丹", "Sudan", "SDG"),
    "SE": ("瑞典", "Sweden", "SEK"),
    "SG": ("新加坡", "Singapore", "SGD"),
    "SH": ("圣赫勒拿", "Saint Helena", "SHP"),
    "SI": ("斯洛文尼亚", "Slovenia", "EUR"),
    "SJ": ("斯瓦尔巴", "Svalbard", "NOK"),
    "SK": ("斯洛伐克", "Slovakia", "EUR"),
    "SL": ("塞拉利昂", "Sierra Leone", "SLL"),
    "SM": ("圣马力诺", "San Marino", "EUR"),
    "SN": ("塞内加尔", "Senegal", "XOF"),
    "SO": ("索马里", "Somalia", "SOS"),
    "SR": ("苏里南", "Suriname", "SRD"),
    "SS": ("南苏丹", "South Sudan", "SSP"),
    "ST": ("圣多美和普林西比", "São Tomé and Príncipe", "STN"),
    "SV": ("萨尔瓦多", "El Salvador", "USD"),
    "SX": ("荷属圣马丁", "Sint Maarten", "ANG"),
    "SY": ("叙利亚", "Syria", "SYP"),
    "SZ": ("斯威士兰", "Swaziland", "SZL"),
    "TC": ("特克斯和凯科斯群岛", "Turks and Caicos Islands", "USD"),
    "TD": ("乍得", "Chad", "XAF"),
    "TF": ("法属南部领地", "French Southern Territories", "EUR"),
    "TG": ("多哥", "Togo", "XOF"),
    "TH": ("泰国", "Thailand", "THB"),
    "TJ": ("塔吉克斯坦", "Tajikistan", "TJS"),
    "TK": ("托克劳", "Tokelau", "NZD"),
    "TL": ("东帝汶", "Timor-Leste", "USD"),
    "TM": ("土库曼斯坦", "Turkmenistan", "TMT"),
    "TN": ("突尼斯", "Tunisia", "TND"),
    "TO": ("汤加", "Tonga", "TOP"),
    "TR": ("土耳其", "Turkey", "TRY"),
    "TT": ("特立尼达和多巴哥", "Trinidad and Tobago", "TTD"),
    "TV": ("图瓦卢", "Tuvalu", "AUD"),
    "TW": ("台湾", "Taiwan", "TWD"),
    "TZ": ("坦桑尼亚", "Tanzania", "TZS"),
    "UA": ("乌克兰", "Ukraine", "UAH"),
    "UG": ("乌干达", "Uganda", "UGX"),
    "UM": ("美国本土外小岛屿", "United States Minor Outlying Islands", "USD"),
    "US": ("美国", "United States", "USD"),
    "UY": ("乌拉圭", "Uruguay", "UYU"),
    "UZ": ("乌兹别克斯坦", "Uzbekistan", "UZS"),
    "VA": ("梵蒂冈", "Vatican City", "EUR"),
    "VC": ("圣文森特和格林纳丁斯", "Saint Vincent and the Grenadines", "XCD"),
    "VE": ("委内瑞拉", "Venezuela", "VES"),
    "VG": ("英属维尔京群岛", "British Virgin Islands", "USD"),
    "VI": ("美属维尔京群岛", "United States Virgin Islands", "USD"),
    "VN": ("越南", "Vietnam", "VND"),
    "VU": ("瓦努阿图", "Vanuatu", "VUV"),
    "WF": ("瓦利斯和富图纳", "Wallis and Futuna", "XPF"),
    "WS": ("萨摩亚", "Samoa", "WST"),
    "YE": ("也门", "Yemen", "YER"),
    "YT": ("马约特", "Mayotte", "EUR"),
    "ZA": ("南非", "South Africa", "ZAR"),
    "ZM": ("赞比亚", "Zambia", "ZMW"),
    "ZW": ("津巴布韦", "Zimbabwe", "ZWL"),
}

# 部分知名银行的SWIFT代码示例（仅用于测试和演示）
_BANK_EXAMPLES: Dict[str, Dict[str, Any]] = {
    "BKCH": {"name": "中国银行", "name_en": "Bank of China", "country": "CN"},
    "ICBK": {"name": "中国工商银行", "name_en": "Industrial and Commercial Bank of China", "country": "CN"},
    "CITI": {"name": "花旗银行", "name_en": "Citibank", "country": "US"},
    "HSBC": {"name": "汇丰银行", "name_en": "HSBC", "country": "GB"},
    "BARC": {"name": "巴克莱银行", "name_en": "Barclays", "country": "GB"},
    "DEUT": {"name": "德意志银行", "name_en": "Deutsche Bank", "country": "DE"},
    "BNPA": {"name": "法国巴黎银行", "name_en": "BNP Paribas", "country": "FR"},
    "BOFA": {"name": "美国银行", "name_en": "Bank of America", "country": "US"},
    "JPMO": {"name": "摩根大通", "name_en": "JPMorgan Chase", "country": "US"},
    "ROYL": {"name": "苏格兰皇家银行", "name_en": "Royal Bank of Scotland", "country": "GB"},
    "UBSW": {"name": "瑞银集团", "name_en": "UBS", "country": "CH"},
    "MIDL": {"name": "渣打银行", "name_en": "Standard Chartered", "country": "GB"},
    "BOJP": {"name": "日本银行", "name_en": "Bank of Japan", "country": "JP"},
    "MHBJ": {"name": "三菱日联银行", "name_en": "MUFG Bank", "country": "JP"},
    "SANW": {"name": "桑坦德银行", "name_en": "Santander", "country": "ES"},
    "NDEA": {"name": "北欧联合银行", "name_en": "Nordea", "country": "SE"},
    "BOIT": {"name": "意大利银行", "name_en": "Bank of Italy", "country": "IT"},
    "CAFR": {"name": "农业信贷银行", "name_en": "Crédit Agricole", "country": "FR"},
    "KBNK": {"name": "韩国银行", "name_en": "Bank of Korea", "country": "KR"},
    "SBIN": {"name": "印度国家银行", "name_en": "State Bank of India", "country": "IN"},
}


class SwiftUtils:
    """SWIFT/BIC代码工具类"""

    # SWIFT代码格式正则表达式
    # 8位格式: BBBBCCSS (银行代码4位 + 国家代码2位 + 地区代码2位)
    # 11位格式: BBBBCCSSBBB (额外3位分行代码)
    _SWIFT_PATTERN = re.compile(r'^[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?$')

    @staticmethod
    def validate(swift_code: str) -> bool:
        """
        验证SWIFT/BIC代码格式
        
        Args:
            swift_code: SWIFT代码（8位或11位）
            
        Returns:
            是否有效
        """
        if not swift_code:
            return False
        
        # 清理输入（去除空格和连字符）
        swift_code = swift_code.strip().upper().replace(" ", "").replace("-", "")
        
        # 检查长度（8位或11位）
        if len(swift_code) not in (8, 11):
            return False
        
        # 检查格式
        if not SwiftUtils._SWIFT_PATTERN.match(swift_code):
            return False
        
        # 检查国家代码是否有效
        country_code = swift_code[4:6]
        if country_code not in _COUNTRY_DATA:
            return False
        
        return True

    @staticmethod
    def validate_strict(swift_code: str) -> Tuple[bool, List[str]]:
        """
        严格验证SWIFT/BIC代码
        
        Args:
            swift_code: SWIFT代码
            
        Returns:
            (是否有效, 错误信息列表)
        """
        errors = []
        
        if not swift_code:
            errors.append("SWIFT代码为空")
            return False, errors
        
        swift_code = swift_code.strip().upper()
        
        # 检查长度
        if len(swift_code) not in (8, 11):
            errors.append(f"SWIFT代码长度应为8位或11位，当前为{len(swift_code)}位")
            return False, errors
        
        # 检查银行代码（前4位）
        bank_code = swift_code[:4]
        if not re.match(r'^[A-Z]{4}$', bank_code):
            errors.append("银行代码（前4位）应为4个大写字母")
        
        # 检查国家代码（第5-6位）
        country_code = swift_code[4:6]
        if not re.match(r'^[A-Z]{2}$', country_code):
            errors.append("国家代码（第5-6位）应为2个大写字母")
        elif country_code not in _COUNTRY_DATA:
            errors.append(f"无效的国家代码: {country_code}")
        
        # 检查地区代码（第7-8位）
        location_code = swift_code[6:8]
        if not re.match(r'^[A-Z0-9]{2}$', location_code):
            errors.append("地区代码（第7-8位）应为2个大写字母或数字")
        
        # 检查分行代码（第9-11位，可选）
        if len(swift_code) == 11:
            branch_code = swift_code[8:11]
            if not re.match(r'^[A-Z0-9]{3}$', branch_code):
                errors.append("分行代码（第9-11位）应为3个大写字母或数字")
        
        return len(errors) == 0, errors

    @staticmethod
    def parse(swift_code: str) -> Dict[str, Any]:
        """
        解析SWIFT/BIC代码
        
        Args:
            swift_code: SWIFT代码
            
        Returns:
            解析结果字典
            
        Raises:
            ValueError: 无效的SWIFT代码
        """
        swift_code = swift_code.strip().upper()
        
        if not SwiftUtils.validate(swift_code):
            raise ValueError(f"无效的SWIFT代码: {swift_code}")
        
        bank_code = swift_code[:4]
        country_code = swift_code[4:6]
        location_code = swift_code[6:8]
        branch_code = swift_code[8:11] if len(swift_code) == 11 else None
        
        # 获取国家信息
        country_info = _COUNTRY_DATA.get(country_code, ("未知", "Unknown", ""))
        
        # 获取银行信息（如果有示例数据）
        bank_info = _BANK_EXAMPLES.get(bank_code, {})
        
        # 解析地区代码中的网络状态
        network_status = SwiftUtils._parse_network_status(location_code[0])
        
        # 解析分行代码含义
        branch_type = SwiftUtils._parse_branch_code(branch_code) if branch_code else SwiftCodeType.PRIMARY
        
        result = {
            "swift_code": swift_code,
            "bank_code": bank_code,
            "country_code": country_code,
            "location_code": location_code,
            "branch_code": branch_code,
            "country_name": country_info[0],
            "country_name_en": country_info[1],
            "country_currency": country_info[2],
            "bank_name": bank_info.get("name", "未知银行"),
            "bank_name_en": bank_info.get("name_en", "Unknown Bank"),
            "network_status": network_status.value if network_status else "未知",
            "code_type": branch_type.value,
            "length": len(swift_code),
            "is_primary": branch_code is None or branch_code == "XXX",
        }
        
        return result

    @staticmethod
    def _parse_network_status(char: str) -> Optional[SwiftNetworkStatus]:
        """
        解析地区代码第一位字符的网络状态
        
        Args:
            char: 地区代码第一位
            
        Returns:
            网络状态
        """
        # 标准SWIFT代码中：
        # 1 = 活跃（Active）
        # 2 = 被动（Passive）
        # 3 = 测试（Test）
        # 其他字母 = 活跃状态
        status_map = {
            '1': SwiftNetworkStatus.ACTIVE,
            '2': SwiftNetworkStatus.PASSIVE,
            '3': SwiftNetworkStatus.TEST,
        }
        
        if char.isdigit():
            return status_map.get(char, SwiftNetworkStatus.ACTIVE)
        
        # 字母通常表示活跃状态
        return SwiftNetworkStatus.ACTIVE

    @staticmethod
    def _parse_branch_code(branch_code: str) -> SwiftCodeType:
        """
        解析分行代码
        
        Args:
            branch_code: 分行代码（3位）
            
        Returns:
            代码类型
        """
        if branch_code == "XXX":
            return SwiftCodeType.PRIMARY
        elif branch_code.isdigit() or branch_code.isalnum():
            return SwiftCodeType.BRANCH
        else:
            return SwiftCodeType.GENERAL

    @staticmethod
    def get_bank_code(swift_code: str) -> str:
        """
        提取银行代码
        
        Args:
            swift_code: SWIFT代码
            
        Returns:
            银行代码（4位）
        """
        swift_code = swift_code.strip().upper()
        if len(swift_code) >= 4:
            return swift_code[:4]
        return ""

    @staticmethod
    def get_country_code(swift_code: str) -> str:
        """
        提取国家代码
        
        Args:
            swift_code: SWIFT代码
            
        Returns:
            国家代码（2位）
        """
        swift_code = swift_code.strip().upper()
        if len(swift_code) >= 6:
            return swift_code[4:6]
        return ""

    @staticmethod
    def get_location_code(swift_code: str) -> str:
        """
        提取地区代码
        
        Args:
            swift_code: SWIFT代码
            
        Returns:
            地区代码（2位）
        """
        swift_code = swift_code.strip().upper()
        if len(swift_code) >= 8:
            return swift_code[6:8]
        return ""

    @staticmethod
    def get_branch_code(swift_code: str) -> Optional[str]:
        """
        提取分行代码
        
        Args:
            swift_code: SWIFT代码
            
        Returns:
            分行代码（3位），8位代码返回None
        """
        swift_code = swift_code.strip().upper()
        if len(swift_code) == 11:
            return swift_code[8:11]
        return None

    @staticmethod
    def get_country_info(country_code: str) -> Dict[str, str]:
        """
        获取国家信息
        
        Args:
            country_code: 国家代码（ISO 3166-1 alpha-2）
            
        Returns:
            国家信息字典
            
        Raises:
            ValueError: 无效的国家代码
        """
        country_code = country_code.strip().upper()
        
        if country_code not in _COUNTRY_DATA:
            raise ValueError(f"无效的国家代码: {country_code}")
        
        info = _COUNTRY_DATA[country_code]
        return {
            "code": country_code,
            "name": info[0],
            "name_en": info[1],
            "currency": info[2],
        }

    @staticmethod
    def get_all_countries() -> List[Dict[str, str]]:
        """
        获取所有国家列表
        
        Returns:
            国家信息列表
        """
        return [
            {"code": code, "name": info[0], "name_en": info[1], "currency": info[2]}
            for code, info in sorted(_COUNTRY_DATA.items(), key=lambda x: x[1][0])
        ]

    @staticmethod
    def format(swift_code: str) -> str:
        """
        格式化SWIFT代码
        
        Args:
            swift_code: SWIFT代码
            
        Returns:
            格式化后的代码（大写，去除空格）
        """
        return swift_code.strip().upper().replace(" ", "").replace("-", "")

    @staticmethod
    def generate_primary(bank_code: str, country_code: str, location_code: str) -> str:
        """
        生成主要办公机构的SWIFT代码（8位）
        
        Args:
            bank_code: 银行代码（4位字母）
            country_code: 国家代码（2位字母）
            location_code: 地区代码（2位字母或数字）
            
        Returns:
            生成的SWIFT代码
            
        Raises:
            ValueError: 参数无效
        """
        bank_code = bank_code.strip().upper()
        country_code = country_code.strip().upper()
        location_code = location_code.strip().upper()
        
        if not re.match(r'^[A-Z]{4}$', bank_code):
            raise ValueError("银行代码应为4个大写字母")
        
        if not re.match(r'^[A-Z]{2}$', country_code):
            raise ValueError("国家代码应为2个大写字母")
        
        if country_code not in _COUNTRY_DATA:
            raise ValueError(f"无效的国家代码: {country_code}")
        
        if not re.match(r'^[A-Z0-9]{2}$', location_code):
            raise ValueError("地区代码应为2个大写字母或数字")
        
        return bank_code + country_code + location_code

    @staticmethod
    def generate_branch(bank_code: str, country_code: str, location_code: str, branch_code: str) -> str:
        """
        生成特定分行的SWIFT代码（11位）
        
        Args:
            bank_code: 银行代码（4位字母）
            country_code: 国家代码（2位字母）
            location_code: 地区代码（2位字母或数字）
            branch_code: 分行代码（3位字母或数字）
            
        Returns:
            生成的SWIFT代码
            
        Raises:
            ValueError: 参数无效
        """
        primary_code = SwiftUtils.generate_primary(bank_code, country_code, location_code)
        
        branch_code = branch_code.strip().upper()
        
        if not re.match(r'^[A-Z0-9]{3}$', branch_code):
            raise ValueError("分行代码应为3个大写字母或数字")
        
        return primary_code + branch_code

    @staticmethod
    def is_primary_office(swift_code: str) -> bool:
        """
        判断是否为主要办公机构
        
        Args:
            swift_code: SWIFT代码
            
        Returns:
            是否为主要办公机构
        """
        swift_code = swift_code.strip().upper()
        
        # 8位代码是主要办公机构
        if len(swift_code) == 8:
            return True
        
        # 11位代码，分行代码为XXX是主要办公机构
        if len(swift_code) == 11:
            return swift_code[8:11] == "XXX"
        
        return False

    @staticmethod
    def get_primary_code(swift_code: str) -> str:
        """
        获取主要办公机构的SWIFT代码
        
        Args:
            swift_code: SWIFT代码
            
        Returns:
            主要办公机构的SWIFT代码（8位）
        """
        swift_code = SwiftUtils.format(swift_code)
        return swift_code[:8]

    @staticmethod
    def compare(swift1: str, swift2: str) -> Dict[str, Any]:
        """
        比较两个SWIFT代码
        
        Args:
            swift1: 第一个SWIFT代码
            swift2: 第二个SWIFT代码
            
        Returns:
            比较结果
        """
        swift1 = SwiftUtils.format(swift1)
        swift2 = SwiftUtils.format(swift2)
        
        same_bank = swift1[:4] == swift2[:4]
        same_country = swift1[4:6] == swift2[4:6]
        same_location = swift1[6:8] == swift2[6:8]
        same_branch = swift1[8:11] == swift2[8:11] if len(swift1) == 11 and len(swift2) == 11 else None
        
        same_bank_system = same_bank and same_country
        
        return {
            "swift1": swift1,
            "swift2": swift2,
            "same_bank": same_bank,
            "same_country": same_country,
            "same_location": same_location,
            "same_branch": same_branch,
            "same_bank_system": same_bank_system,
            "is_related": same_bank_system,
        }

    @staticmethod
    def get_swift_codes_for_bank(bank_code: str) -> List[Dict[str, Any]]:
        """
        获取指定银行的示例SWIFT代码（仅用于演示）
        
        Args:
            bank_code: 银行代码
            
        Returns:
            示例SWIFT代码列表
        """
        bank_code = bank_code.strip().upper()
        
        if bank_code not in _BANK_EXAMPLES:
            return []
        
        bank_info = _BANK_EXAMPLES[bank_code]
        country = bank_info["country"]
        
        # 生成示例代码
        examples = []
        locations = ["CN", "HK", "BJ", "SH"] if country == "CN" else ["XX", "01", "02", "03"]
        
        for loc in locations:
            swift = bank_code + country + loc
            examples.append({
                "swift_code": swift,
                "bank_name": bank_info["name"],
                "country": country,
                "location": loc,
            })
        
        return examples

    @staticmethod
    def get_all_bank_examples() -> Dict[str, Dict[str, Any]]:
        """
        获取所有银行示例数据
        
        Returns:
            银行示例数据字典
        """
        return _BANK_EXAMPLES.copy()

    @staticmethod
    def search_by_country(country_code: str) -> List[Dict[str, Any]]:
        """
        搜索指定国家的银行示例
        
        Args:
            country_code: 国家代码
            
        Returns:
            银行示例列表
        """
        country_code = country_code.strip().upper()
        
        results = []
        for bank_code, info in _BANK_EXAMPLES.items():
            if info["country"] == country_code:
                results.append({
                    "bank_code": bank_code,
                    "bank_name": info["name"],
                    "bank_name_en": info["name_en"],
                    "country": country_code,
                })
        
        return results


class BicUtils:
    """BIC（Bank Identifier Code）工具类 - SWIFT代码别名"""

    @staticmethod
    def validate(bic_code: str) -> bool:
        """验证BIC代码"""
        return SwiftUtils.validate(bic_code)

    @staticmethod
    def parse(bic_code: str) -> Dict[str, Any]:
        """解析BIC代码"""
        return SwiftUtils.parse(bic_code)

    @staticmethod
    def get_bank_code(bic_code: str) -> str:
        """获取银行代码"""
        return SwiftUtils.get_bank_code(bic_code)

    @staticmethod
    def get_country_code(bic_code: str) -> str:
        """获取国家代码"""
        return SwiftUtils.get_country_code(bic_code)

    @staticmethod
    def get_location_code(bic_code: str) -> str:
        """获取地区代码"""
        return SwiftUtils.get_location_code(bic_code)

    @staticmethod
    def get_branch_code(bic_code: str) -> Optional[str]:
        """获取分行代码"""
        return SwiftUtils.get_branch_code(bic_code)


# 便捷函数
def validate_swift(swift_code: str) -> bool:
    """验证SWIFT代码"""
    return SwiftUtils.validate(swift_code)


def validate_bic(bic_code: str) -> bool:
    """验证BIC代码"""
    return SwiftUtils.validate(bic_code)


def parse_swift(swift_code: str) -> Dict[str, Any]:
    """解析SWIFT代码"""
    return SwiftUtils.parse(swift_code)


def parse_bic(bic_code: str) -> Dict[str, Any]:
    """解析BIC代码"""
    return SwiftUtils.parse(bic_code)


def get_swift_bank_code(swift_code: str) -> str:
    """获取SWIFT代码的银行代码"""
    return SwiftUtils.get_bank_code(swift_code)


def get_swift_country(swift_code: str) -> str:
    """获取SWIFT代码的国家代码"""
    return SwiftUtils.get_country_code(swift_code)


def is_swift_primary(swift_code: str) -> bool:
    """判断是否为主要办公机构SWIFT代码"""
    return SwiftUtils.is_primary_office(swift_code)


def format_swift(swift_code: str) -> str:
    """格式化SWIFT代码"""
    return SwiftUtils.format(swift_code)