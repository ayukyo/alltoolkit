"""
国际电话区号工具模块 (International Dial Code Utilities)

提供国际电话区号查询、国家代码转换、电话号码格式化等功能。
零外部依赖，纯Python实现。

功能：
- 按国家名称/代码查询电话区号
- 按区号查询对应国家
- 电话号码格式化（国际格式、本地格式）
- 验证电话号码格式
- 国家代码转换（ISO 3166-1 alpha-2/alpha-3/numeric）
"""

from typing import Optional, Dict, List, Tuple, Set
import re


def _clean_dial_code(code: str) -> str:
    """
    清理区号格式，移除可能的"1-"前缀（用于像1-340这样的特殊区号）
    
    Args:
        code: 原始区号
        
    Returns:
        清理后的区号
    """
    if not code:
        return code
    # 只移除以"1-"开头的特殊情况（如"1-340"）
    if code.startswith("1-"):
        return code[2:]
    return code


# 国际电话区号数据 (主要国家和地区)
# 格式: {区号: {'name': 国家名, 'code': ISO alpha-2, 'alpha3': ISO alpha-3, 'numeric': 数字代码}}
_DIAL_CODE_DATA: Dict[str, Dict] = {
    "1": {"name": "美国/加拿大", "code": "US/CA", "alpha3": "USA/CAN", "numeric": "840/124", "continent": "北美"},
    "1-340": {"name": "美属维尔京群岛", "code": "VI", "alpha3": "VIR", "numeric": "850", "continent": "北美"},
    "1-670": {"name": "北马里亚纳群岛", "code": "MP", "alpha3": "MNP", "numeric": "580", "continent": "大洋洲"},
    "1-671": {"name": "关岛", "code": "GU", "alpha3": "GUM", "numeric": "316", "continent": "大洋洲"},
    "1-684": {"name": "美属萨摩亚", "code": "AS", "alpha3": "ASM", "numeric": "016", "continent": "大洋洲"},
    "1-787": {"name": "波多黎各", "code": "PR", "alpha3": "PRI", "numeric": "630", "continent": "北美"},
    "7": {"name": "俄罗斯/哈萨克斯坦", "code": "RU/KZ", "alpha3": "RUS/KAZ", "numeric": "643/398", "continent": "欧亚"},
    "20": {"name": "埃及", "code": "EG", "alpha3": "EGY", "numeric": "818", "continent": "非洲"},
    "27": {"name": "南非", "code": "ZA", "alpha3": "ZAF", "numeric": "710", "continent": "非洲"},
    "30": {"name": "希腊", "code": "GR", "alpha3": "GRC", "numeric": "300", "continent": "欧洲"},
    "31": {"name": "荷兰", "code": "NL", "alpha3": "NLD", "numeric": "528", "continent": "欧洲"},
    "32": {"name": "比利时", "code": "BE", "alpha3": "BEL", "numeric": "056", "continent": "欧洲"},
    "33": {"name": "法国", "code": "FR", "alpha3": "FRA", "numeric": "250", "continent": "欧洲"},
    "34": {"name": "西班牙", "code": "ES", "alpha3": "ESP", "numeric": "724", "continent": "欧洲"},
    "36": {"name": "匈牙利", "code": "HU", "alpha3": "HUN", "numeric": "348", "continent": "欧洲"},
    "39": {"name": "意大利", "code": "IT", "alpha3": "ITA", "numeric": "380", "continent": "欧洲"},
    "40": {"name": "罗马尼亚", "code": "RO", "alpha3": "ROU", "numeric": "642", "continent": "欧洲"},
    "41": {"name": "瑞士", "code": "CH", "alpha3": "CHE", "numeric": "756", "continent": "欧洲"},
    "43": {"name": "奥地利", "code": "AT", "alpha3": "AUT", "numeric": "040", "continent": "欧洲"},
    "44": {"name": "英国", "code": "GB", "alpha3": "GBR", "numeric": "826", "continent": "欧洲"},
    "45": {"name": "丹麦", "code": "DK", "alpha3": "DNK", "numeric": "208", "continent": "欧洲"},
    "46": {"name": "瑞典", "code": "SE", "alpha3": "SWE", "numeric": "752", "continent": "欧洲"},
    "47": {"name": "挪威", "code": "NO", "alpha3": "NOR", "numeric": "578", "continent": "欧洲"},
    "48": {"name": "波兰", "code": "PL", "alpha3": "POL", "numeric": "616", "continent": "欧洲"},
    "49": {"name": "德国", "code": "DE", "alpha3": "DEU", "numeric": "276", "continent": "欧洲"},
    "51": {"name": "秘鲁", "code": "PE", "alpha3": "PER", "numeric": "604", "continent": "南美"},
    "52": {"name": "墨西哥", "code": "MX", "alpha3": "MEX", "numeric": "484", "continent": "北美"},
    "53": {"name": "古巴", "code": "CU", "alpha3": "CUB", "numeric": "192", "continent": "北美"},
    "54": {"name": "阿根廷", "code": "AR", "alpha3": "ARG", "numeric": "032", "continent": "南美"},
    "55": {"name": "巴西", "code": "BR", "alpha3": "BRA", "numeric": "076", "continent": "南美"},
    "56": {"name": "智利", "code": "CL", "alpha3": "CHL", "numeric": "152", "continent": "南美"},
    "57": {"name": "哥伦比亚", "code": "CO", "alpha3": "COL", "numeric": "170", "continent": "南美"},
    "58": {"name": "委内瑞拉", "code": "VE", "alpha3": "VEN", "numeric": "862", "continent": "南美"},
    "60": {"name": "马来西亚", "code": "MY", "alpha3": "MYS", "numeric": "458", "continent": "亚洲"},
    "61": {"name": "澳大利亚", "code": "AU", "alpha3": "AUS", "numeric": "036", "continent": "大洋洲"},
    "62": {"name": "印度尼西亚", "code": "ID", "alpha3": "IDN", "numeric": "360", "continent": "亚洲"},
    "63": {"name": "菲律宾", "code": "PH", "alpha3": "PHL", "numeric": "608", "continent": "亚洲"},
    "64": {"name": "新西兰", "code": "NZ", "alpha3": "NZL", "numeric": "554", "continent": "大洋洲"},
    "65": {"name": "新加坡", "code": "SG", "alpha3": "SGP", "numeric": "702", "continent": "亚洲"},
    "66": {"name": "泰国", "code": "TH", "alpha3": "THA", "numeric": "764", "continent": "亚洲"},
    "81": {"name": "日本", "code": "JP", "alpha3": "JPN", "numeric": "392", "continent": "亚洲"},
    "82": {"name": "韩国", "code": "KR", "alpha3": "KOR", "numeric": "410", "continent": "亚洲"},
    "84": {"name": "越南", "code": "VN", "alpha3": "VNM", "numeric": "704", "continent": "亚洲"},
    "86": {"name": "中国", "code": "CN", "alpha3": "CHN", "numeric": "156", "continent": "亚洲"},
    "886": {"name": "台湾", "code": "TW", "alpha3": "TWN", "numeric": "158", "continent": "亚洲"},
    "852": {"name": "香港", "code": "HK", "alpha3": "HKG", "numeric": "344", "continent": "亚洲"},
    "853": {"name": "澳门", "code": "MO", "alpha3": "MAC", "numeric": "446", "continent": "亚洲"},
    "90": {"name": "土耳其", "code": "TR", "alpha3": "TUR", "numeric": "792", "continent": "欧亚"},
    "91": {"name": "印度", "code": "IN", "alpha3": "IND", "numeric": "356", "continent": "亚洲"},
    "92": {"name": "巴基斯坦", "code": "PK", "alpha3": "PAK", "numeric": "586", "continent": "亚洲"},
    "93": {"name": "阿富汗", "code": "AF", "alpha3": "AFG", "numeric": "004", "continent": "亚洲"},
    "94": {"name": "斯里兰卡", "code": "LK", "alpha3": "LKA", "numeric": "144", "continent": "亚洲"},
    "95": {"name": "缅甸", "code": "MM", "alpha3": "MMR", "numeric": "104", "continent": "亚洲"},
    "98": {"name": "伊朗", "code": "IR", "alpha3": "IRN", "numeric": "364", "continent": "亚洲"},
    "212": {"name": "摩洛哥", "code": "MA", "alpha3": "MAR", "numeric": "504", "continent": "非洲"},
    "213": {"name": "阿尔及利亚", "code": "DZ", "alpha3": "DZA", "numeric": "012", "continent": "非洲"},
    "216": {"name": "突尼斯", "code": "TN", "alpha3": "TUN", "numeric": "788", "continent": "非洲"},
    "218": {"name": "利比亚", "code": "LY", "alpha3": "LBY", "numeric": "434", "continent": "非洲"},
    "220": {"name": "冈比亚", "code": "GM", "alpha3": "GMB", "numeric": "270", "continent": "非洲"},
    "221": {"name": "塞内加尔", "code": "SN", "alpha3": "SEN", "numeric": "686", "continent": "非洲"},
    "222": {"name": "毛里塔尼亚", "code": "MR", "alpha3": "MRT", "numeric": "478", "continent": "非洲"},
    "223": {"name": "马里", "code": "ML", "alpha3": "MLI", "numeric": "466", "continent": "非洲"},
    "224": {"name": "几内亚", "code": "GN", "alpha3": "GIN", "numeric": "324", "continent": "非洲"},
    "225": {"name": "科特迪瓦", "code": "CI", "alpha3": "CIV", "numeric": "384", "continent": "非洲"},
    "226": {"name": "布基纳法索", "code": "BF", "alpha3": "BFA", "numeric": "854", "continent": "非洲"},
    "227": {"name": "尼日尔", "code": "NE", "alpha3": "NER", "numeric": "562", "continent": "非洲"},
    "228": {"name": "多哥", "code": "TG", "alpha3": "TGO", "numeric": "768", "continent": "非洲"},
    "229": {"name": "贝宁", "code": "BJ", "alpha3": "BEN", "numeric": "204", "continent": "非洲"},
    "230": {"name": "毛里求斯", "code": "MU", "alpha3": "MUS", "numeric": "480", "continent": "非洲"},
    "231": {"name": "利比里亚", "code": "LR", "alpha3": "LBR", "numeric": "430", "continent": "非洲"},
    "232": {"name": "塞拉利昂", "code": "SL", "alpha3": "SLE", "numeric": "694", "continent": "非洲"},
    "233": {"name": "加纳", "code": "GH", "alpha3": "GHA", "numeric": "288", "continent": "非洲"},
    "234": {"name": "尼日利亚", "code": "NG", "alpha3": "NGA", "numeric": "566", "continent": "非洲"},
    "235": {"name": "乍得", "code": "TD", "alpha3": "TCD", "numeric": "148", "continent": "非洲"},
    "236": {"name": "中非共和国", "code": "CF", "alpha3": "CAF", "numeric": "140", "continent": "非洲"},
    "237": {"name": "喀麦隆", "code": "CM", "alpha3": "CMR", "numeric": "120", "continent": "非洲"},
    "238": {"name": "佛得角", "code": "CV", "alpha3": "CPV", "numeric": "132", "continent": "非洲"},
    "239": {"name": "圣多美和普林西比", "code": "ST", "alpha3": "STP", "numeric": "678", "continent": "非洲"},
    "240": {"name": "赤道几内亚", "code": "GQ", "alpha3": "GNQ", "numeric": "226", "continent": "非洲"},
    "241": {"name": "加蓬", "code": "GA", "alpha3": "GAB", "numeric": "266", "continent": "非洲"},
    "242": {"name": "刚果(布)", "code": "CG", "alpha3": "COG", "numeric": "178", "continent": "非洲"},
    "243": {"name": "刚果(金)", "code": "CD", "alpha3": "COD", "numeric": "180", "continent": "非洲"},
    "244": {"name": "安哥拉", "code": "AO", "alpha3": "AGO", "numeric": "024", "continent": "非洲"},
    "245": {"name": "几内亚比绍", "code": "GW", "alpha3": "GNB", "numeric": "624", "continent": "非洲"},
    "248": {"name": "塞舌尔", "code": "SC", "alpha3": "SYC", "numeric": "690", "continent": "非洲"},
    "249": {"name": "苏丹", "code": "SD", "alpha3": "SDN", "numeric": "729", "continent": "非洲"},
    "250": {"name": "卢旺达", "code": "RW", "alpha3": "RWA", "numeric": "646", "continent": "非洲"},
    "251": {"name": "埃塞俄比亚", "code": "ET", "alpha3": "ETH", "numeric": "231", "continent": "非洲"},
    "252": {"name": "索马里", "code": "SO", "alpha3": "SOM", "numeric": "706", "continent": "非洲"},
    "253": {"name": "吉布提", "code": "DJ", "alpha3": "DJI", "numeric": "262", "continent": "非洲"},
    "254": {"name": "肯尼亚", "code": "KE", "alpha3": "KEN", "numeric": "404", "continent": "非洲"},
    "255": {"name": "坦桑尼亚", "code": "TZ", "alpha3": "TZA", "numeric": "834", "continent": "非洲"},
    "256": {"name": "乌干达", "code": "UG", "alpha3": "UGA", "numeric": "800", "continent": "非洲"},
    "257": {"name": "布隆迪", "code": "BI", "alpha3": "BDI", "numeric": "108", "continent": "非洲"},
    "258": {"name": "莫桑比克", "code": "MZ", "alpha3": "MOZ", "numeric": "508", "continent": "非洲"},
    "260": {"name": "赞比亚", "code": "ZM", "alpha3": "ZMB", "numeric": "894", "continent": "非洲"},
    "261": {"name": "马达加斯加", "code": "MG", "alpha3": "MDG", "numeric": "450", "continent": "非洲"},
    "262": {"name": "留尼汪", "code": "RE", "alpha3": "REU", "numeric": "638", "continent": "非洲"},
    "263": {"name": "津巴布韦", "code": "ZW", "alpha3": "ZWE", "numeric": "716", "continent": "非洲"},
    "264": {"name": "纳米比亚", "code": "NA", "alpha3": "NAM", "numeric": "516", "continent": "非洲"},
    "265": {"name": "马拉维", "code": "MW", "alpha3": "MWI", "numeric": "454", "continent": "非洲"},
    "266": {"name": "莱索托", "code": "LS", "alpha3": "LSO", "numeric": "426", "continent": "非洲"},
    "267": {"name": "博茨瓦纳", "code": "BW", "alpha3": "BWA", "numeric": "072", "continent": "非洲"},
    "268": {"name": "斯威士兰", "code": "SZ", "alpha3": "SWZ", "numeric": "748", "continent": "非洲"},
    "269": {"name": "科摩罗", "code": "KM", "alpha3": "COM", "numeric": "174", "continent": "非洲"},
    "290": {"name": "圣赫勒拿", "code": "SH", "alpha3": "SHN", "numeric": "654", "continent": "非洲"},
    "291": {"name": "厄立特里亚", "code": "ER", "alpha3": "ERI", "numeric": "232", "continent": "非洲"},
    "297": {"name": "阿鲁巴", "code": "AW", "alpha3": "ABW", "numeric": "533", "continent": "北美"},
    "298": {"name": "法罗群岛", "code": "FO", "alpha3": "FRO", "numeric": "234", "continent": "欧洲"},
    "299": {"name": "格陵兰", "code": "GL", "alpha3": "GRL", "numeric": "304", "continent": "北美"},
    "350": {"name": "直布罗陀", "code": "GI", "alpha3": "GIB", "numeric": "292", "continent": "欧洲"},
    "351": {"name": "葡萄牙", "code": "PT", "alpha3": "PRT", "numeric": "620", "continent": "欧洲"},
    "352": {"name": "卢森堡", "code": "LU", "alpha3": "LUX", "numeric": "442", "continent": "欧洲"},
    "353": {"name": "爱尔兰", "code": "IE", "alpha3": "IRL", "numeric": "372", "continent": "欧洲"},
    "354": {"name": "冰岛", "code": "IS", "alpha3": "ISL", "numeric": "352", "continent": "欧洲"},
    "355": {"name": "阿尔巴尼亚", "code": "AL", "alpha3": "ALB", "numeric": "008", "continent": "欧洲"},
    "356": {"name": "马耳他", "code": "MT", "alpha3": "MLT", "numeric": "470", "continent": "欧洲"},
    "357": {"name": "塞浦路斯", "code": "CY", "alpha3": "CYP", "numeric": "196", "continent": "欧洲"},
    "358": {"name": "芬兰", "code": "FI", "alpha3": "FIN", "numeric": "246", "continent": "欧洲"},
    "359": {"name": "保加利亚", "code": "BG", "alpha3": "BGR", "numeric": "100", "continent": "欧洲"},
    "370": {"name": "立陶宛", "code": "LT", "alpha3": "LTU", "numeric": "440", "continent": "欧洲"},
    "371": {"name": "拉脱维亚", "code": "LV", "alpha3": "LVA", "numeric": "428", "continent": "欧洲"},
    "372": {"name": "爱沙尼亚", "code": "EE", "alpha3": "EST", "numeric": "233", "continent": "欧洲"},
    "373": {"name": "摩尔多瓦", "code": "MD", "alpha3": "MDA", "numeric": "498", "continent": "欧洲"},
    "374": {"name": "亚美尼亚", "code": "AM", "alpha3": "ARM", "numeric": "051", "continent": "亚洲"},
    "375": {"name": "白俄罗斯", "code": "BY", "alpha3": "BLR", "numeric": "112", "continent": "欧洲"},
    "376": {"name": "安道尔", "code": "AD", "alpha3": "AND", "numeric": "020", "continent": "欧洲"},
    "377": {"name": "摩纳哥", "code": "MC", "alpha3": "MCO", "numeric": "492", "continent": "欧洲"},
    "378": {"name": "圣马力诺", "code": "SM", "alpha3": "SMR", "numeric": "674", "continent": "欧洲"},
    "380": {"name": "乌克兰", "code": "UA", "alpha3": "UKR", "numeric": "804", "continent": "欧洲"},
    "381": {"name": "塞尔维亚", "code": "RS", "alpha3": "SRB", "numeric": "688", "continent": "欧洲"},
    "382": {"name": "黑山", "code": "ME", "alpha3": "MNE", "numeric": "499", "continent": "欧洲"},
    "383": {"name": "科索沃", "code": "XK", "alpha3": "XKX", "numeric": "926", "continent": "欧洲"},
    "385": {"name": "克罗地亚", "code": "HR", "alpha3": "HRV", "numeric": "191", "continent": "欧洲"},
    "386": {"name": "斯洛文尼亚", "code": "SI", "alpha3": "SVN", "numeric": "705", "continent": "欧洲"},
    "387": {"name": "波黑", "code": "BA", "alpha3": "BIH", "numeric": "070", "continent": "欧洲"},
    "389": {"name": "北马其顿", "code": "MK", "alpha3": "MKD", "numeric": "807", "continent": "欧洲"},
    "420": {"name": "捷克", "code": "CZ", "alpha3": "CZE", "numeric": "203", "continent": "欧洲"},
    "421": {"name": "斯洛伐克", "code": "SK", "alpha3": "SVK", "numeric": "703", "continent": "欧洲"},
    "423": {"name": "列支敦士登", "code": "LI", "alpha3": "LIE", "numeric": "438", "continent": "欧洲"},
    "500": {"name": "福克兰群岛", "code": "FK", "alpha3": "FLK", "numeric": "238", "continent": "南美"},
    "501": {"name": "伯利兹", "code": "BZ", "alpha3": "BLZ", "numeric": "084", "continent": "北美"},
    "502": {"name": "危地马拉", "code": "GT", "alpha3": "GTM", "numeric": "320", "continent": "北美"},
    "503": {"name": "萨尔瓦多", "code": "SV", "alpha3": "SLV", "numeric": "222", "continent": "北美"},
    "504": {"name": "洪都拉斯", "code": "HN", "alpha3": "HND", "numeric": "340", "continent": "北美"},
    "505": {"name": "尼加拉瓜", "code": "NI", "alpha3": "NIC", "numeric": "558", "continent": "北美"},
    "506": {"name": "哥斯达黎加", "code": "CR", "alpha3": "CRI", "numeric": "188", "continent": "北美"},
    "507": {"name": "巴拿马", "code": "PA", "alpha3": "PAN", "numeric": "591", "continent": "北美"},
    "508": {"name": "圣皮埃尔和密克隆", "code": "PM", "alpha3": "SPM", "numeric": "666", "continent": "北美"},
    "509": {"name": "海地", "code": "HT", "alpha3": "HTI", "numeric": "332", "continent": "北美"},
    "590": {"name": "瓜德罗普", "code": "GP", "alpha3": "GLP", "numeric": "312", "continent": "北美"},
    "591": {"name": "玻利维亚", "code": "BO", "alpha3": "BOL", "numeric": "068", "continent": "南美"},
    "592": {"name": "圭亚那", "code": "GY", "alpha3": "GUY", "numeric": "328", "continent": "南美"},
    "593": {"name": "厄瓜多尔", "code": "EC", "alpha3": "ECU", "numeric": "218", "continent": "南美"},
    "594": {"name": "法属圭亚那", "code": "GF", "alpha3": "GUF", "numeric": "254", "continent": "南美"},
    "595": {"name": "巴拉圭", "code": "PY", "alpha3": "PRY", "numeric": "600", "continent": "南美"},
    "596": {"name": "马提尼克", "code": "MQ", "alpha3": "MTQ", "numeric": "474", "continent": "北美"},
    "597": {"name": "苏里南", "code": "SR", "alpha3": "SUR", "numeric": "740", "continent": "南美"},
    "598": {"name": "乌拉圭", "code": "UY", "alpha3": "URY", "numeric": "858", "continent": "南美"},
    "599": {"name": "荷属安的列斯", "code": "AN", "alpha3": "ANT", "numeric": "530", "continent": "北美"},
    "670": {"name": "东帝汶", "code": "TL", "alpha3": "TLS", "numeric": "626", "continent": "亚洲"},
    "672": {"name": "南极洲", "code": "AQ", "alpha3": "ATA", "numeric": "010", "continent": "南极洲"},
    "673": {"name": "文莱", "code": "BN", "alpha3": "BRN", "numeric": "096", "continent": "亚洲"},
    "674": {"name": "瑙鲁", "code": "NR", "alpha3": "NRU", "numeric": "520", "continent": "大洋洲"},
    "675": {"name": "巴布亚新几内亚", "code": "PG", "alpha3": "PNG", "numeric": "598", "continent": "大洋洲"},
    "676": {"name": "汤加", "code": "TO", "alpha3": "TON", "numeric": "776", "continent": "大洋洲"},
    "677": {"name": "所罗门群岛", "code": "SB", "alpha3": "SLB", "numeric": "090", "continent": "大洋洲"},
    "678": {"name": "瓦努阿图", "code": "VU", "alpha3": "VUT", "numeric": "548", "continent": "大洋洲"},
    "679": {"name": "斐济", "code": "FJ", "alpha3": "FJI", "numeric": "242", "continent": "大洋洲"},
    "680": {"name": "帕劳", "code": "PW", "alpha3": "PLW", "numeric": "585", "continent": "大洋洲"},
    "681": {"name": "瓦利斯和富图纳", "code": "WF", "alpha3": "WLF", "numeric": "876", "continent": "大洋洲"},
    "682": {"name": "库克群岛", "code": "CK", "alpha3": "COK", "numeric": "184", "continent": "大洋洲"},
    "683": {"name": "纽埃", "code": "NU", "alpha3": "NIU", "numeric": "570", "continent": "大洋洲"},
    "685": {"name": "萨摩亚", "code": "WS", "alpha3": "WSM", "numeric": "882", "continent": "大洋洲"},
    "686": {"name": "基里巴斯", "code": "KI", "alpha3": "KIR", "numeric": "296", "continent": "大洋洲"},
    "687": {"name": "新喀里多尼亚", "code": "NC", "alpha3": "NCL", "numeric": "540", "continent": "大洋洲"},
    "688": {"name": "图瓦卢", "code": "TV", "alpha3": "TUV", "numeric": "798", "continent": "大洋洲"},
    "689": {"name": "法属波利尼西亚", "code": "PF", "alpha3": "PYF", "numeric": "258", "continent": "大洋洲"},
    "690": {"name": "托克劳", "code": "TK", "alpha3": "TKL", "numeric": "772", "continent": "大洋洲"},
    "691": {"name": "密克罗尼西亚", "code": "FM", "alpha3": "FSM", "numeric": "583", "continent": "大洋洲"},
    "692": {"name": "马绍尔群岛", "code": "MH", "alpha3": "MHL", "numeric": "584", "continent": "大洋洲"},
    "850": {"name": "朝鲜", "code": "KP", "alpha3": "PRK", "numeric": "408", "continent": "亚洲"},
    "851": {"name": "澳门(旧)", "code": "MO", "alpha3": "MAC", "numeric": "446", "continent": "亚洲"},
    "855": {"name": "柬埔寨", "code": "KH", "alpha3": "KHM", "numeric": "116", "continent": "亚洲"},
    "856": {"name": "老挝", "code": "LA", "alpha3": "LAO", "numeric": "418", "continent": "亚洲"},
    "880": {"name": "孟加拉国", "code": "BD", "alpha3": "BGD", "numeric": "050", "continent": "亚洲"},
    "881": {"name": "全球卫星系统", "code": "", "alpha3": "", "numeric": "", "continent": ""},
    "882": {"name": "国际网络", "code": "", "alpha3": "", "numeric": "", "continent": ""},
    "883": {"name": "国际网络", "code": "", "alpha3": "", "numeric": "", "continent": ""},
    "884": {"name": "国际网络", "code": "", "alpha3": "", "numeric": "", "continent": ""},
    "960": {"name": "马尔代夫", "code": "MV", "alpha3": "MDV", "numeric": "462", "continent": "亚洲"},
    "961": {"name": "黎巴嫩", "code": "LB", "alpha3": "LBN", "numeric": "422", "continent": "亚洲"},
    "962": {"name": "约旦", "code": "JO", "alpha3": "JOR", "numeric": "400", "continent": "亚洲"},
    "963": {"name": "叙利亚", "code": "SY", "alpha3": "SYR", "numeric": "760", "continent": "亚洲"},
    "964": {"name": "伊拉克", "code": "IQ", "alpha3": "IRQ", "numeric": "368", "continent": "亚洲"},
    "965": {"name": "科威特", "code": "KW", "alpha3": "KWT", "numeric": "414", "continent": "亚洲"},
    "966": {"name": "沙特阿拉伯", "code": "SA", "alpha3": "SAU", "numeric": "682", "continent": "亚洲"},
    "967": {"name": "也门", "code": "YE", "alpha3": "YEM", "numeric": "887", "continent": "亚洲"},
    "968": {"name": "阿曼", "code": "OM", "alpha3": "OMN", "numeric": "512", "continent": "亚洲"},
    "970": {"name": "巴勒斯坦", "code": "PS", "alpha3": "PSE", "numeric": "275", "continent": "亚洲"},
    "971": {"name": "阿联酋", "code": "AE", "alpha3": "ARE", "numeric": "784", "continent": "亚洲"},
    "972": {"name": "以色列", "code": "IL", "alpha3": "ISR", "numeric": "376", "continent": "亚洲"},
    "973": {"name": "巴林", "code": "BH", "alpha3": "BHR", "numeric": "048", "continent": "亚洲"},
    "974": {"name": "卡塔尔", "code": "QA", "alpha3": "QAT", "numeric": "634", "continent": "亚洲"},
    "975": {"name": "不丹", "code": "BT", "alpha3": "BTN", "numeric": "064", "continent": "亚洲"},
    "976": {"name": "蒙古", "code": "MN", "alpha3": "MNG", "numeric": "496", "continent": "亚洲"},
    "977": {"name": "尼泊尔", "code": "NP", "alpha3": "NPL", "numeric": "524", "continent": "亚洲"},
    "978": {"name": "国际网络", "code": "", "alpha3": "", "numeric": "", "continent": ""},
    "979": {"name": "国际增值服务", "code": "", "alpha3": "", "numeric": "", "continent": ""},
    "992": {"name": "塔吉克斯坦", "code": "TJ", "alpha3": "TJK", "numeric": "762", "continent": "亚洲"},
    "993": {"name": "土库曼斯坦", "code": "TM", "alpha3": "TKM", "numeric": "795", "continent": "亚洲"},
    "994": {"name": "阿塞拜疆", "code": "AZ", "alpha3": "AZE", "numeric": "031", "continent": "亚洲"},
    "995": {"name": "格鲁吉亚", "code": "GE", "alpha3": "GEO", "numeric": "268", "continent": "亚洲"},
    "996": {"name": "吉尔吉斯斯坦", "code": "KG", "alpha3": "KGZ", "numeric": "417", "continent": "亚洲"},
    "998": {"name": "乌兹别克斯坦", "code": "UZ", "alpha3": "UZB", "numeric": "860", "continent": "亚洲"},
}

# 国家代码到区号的反向映射
_COUNTRY_TO_DIAL: Dict[str, str] = {}
for code, data in _DIAL_CODE_DATA.items():
    if "/" in data.get("code", ""):
        # 多国家共享区号
        codes = data["code"].split("/")
        for c in codes:
            _COUNTRY_TO_DIAL[c.lower()] = code
    else:
        _COUNTRY_TO_DIAL[data["code"].lower()] = code


def get_country_by_dial_code(dial_code: str) -> Optional[Dict]:
    """
    根据电话区号查询国家信息
    
    Args:
        dial_code: 电话区号（可带或不带+号前缀）
        
    Returns:
        国家信息字典，包含名称、代码等；未找到返回None
        
    Examples:
        >>> get_country_by_dial_code("86")
        {'name': '中国', 'code': 'CN', 'alpha3': 'CHN', 'numeric': '156', 'continent': '亚洲'}
        
        >>> get_country_by_dial_code("+1")
        {'name': '美国/加拿大', 'code': 'US/CA', ...}
    """
    # 清理区号格式
    dial_code = dial_code.strip().lstrip("+").lstrip("0")
    
    if not dial_code:
        return None
    
    # 尝试精确匹配
    if dial_code in _DIAL_CODE_DATA:
        return _DIAL_CODE_DATA[dial_code].copy()
    
    # 尝试匹配子区号（如1-340）
    for code in sorted(_DIAL_CODE_DATA.keys(), key=len, reverse=True):
        if dial_code.startswith(_clean_dial_code(code)) and "-" in code:
            return _DIAL_CODE_DATA[code].copy()
    
    return None


def get_dial_code_by_country(country: str) -> Optional[str]:
    """
    根据国家名称或代码查询电话区号
    
    Args:
        country: 国家名称（中文/英文）或ISO代码
        
    Returns:
        电话区号字符串；未找到返回None
        
    Examples:
        >>> get_dial_code_by_country("中国")
        '86'
        
        >>> get_dial_code_by_country("CN")
        '86'
        
        >>> get_dial_code_by_country("CHN")
        '86'
        
        >>> get_dial_code_by_country("China")
        '86'
    """
    country = country.strip().lower()
    
    # 空字符串检查
    if not country:
        return None
    
    # 尝试ISO代码匹配
    if country in _COUNTRY_TO_DIAL:
        return _COUNTRY_TO_DIAL[country]
    
    # 尝试国家名称匹配
    for dial_code, data in _DIAL_CODE_DATA.items():
        # 中文名匹配
        if country in data["name"].lower():
            return dial_code
        
        # 英文名匹配（如果有）
        if "en_name" in data and country in data["en_name"].lower():
            return dial_code
        
        # alpha3代码匹配
        if data.get("alpha3", "").lower() == country:
            return dial_code
        
        # 处理多国家共享区号的情况
        if "/" in data.get("alpha3", ""):
            for a3 in data["alpha3"].split("/"):
                if a3.lower() == country:
                    return dial_code
    
    return None


def get_all_countries() -> List[Dict]:
    """
    获取所有国家和地区信息列表
    
    Returns:
        国家信息列表，每项包含区号、名称、代码等
        
    Examples:
        >>> countries = get_all_countries()
        >>> len(countries) > 200
        True
    """
    result = []
    for dial_code, data in _DIAL_CODE_DATA.items():
        item = {"dial_code": dial_code}
        item.update(data)
        result.append(item)
    return sorted(result, key=lambda x: int(x["dial_code"].split("-")[0]) if x["dial_code"].split("-")[0].isdigit() else 999)


def get_countries_by_continent(continent: str) -> List[Dict]:
    """
    按大洲获取国家列表
    
    Args:
        continent: 大洲名称（中文：亚洲、欧洲、非洲、北美、南美、大洋洲）
        
    Returns:
        该大洲的国家列表
        
    Examples:
        >>> asia = get_countries_by_continent("亚洲")
        >>> any(c["name"] == "中国" for c in asia)
        True
    """
    continent = continent.strip()
    result = []
    for dial_code, data in _DIAL_CODE_DATA.items():
        if data.get("continent") == continent:
            item = {"dial_code": dial_code}
            item.update(data)
            result.append(item)
    return sorted(result, key=lambda x: x["dial_code"])


def format_phone_number(phone: str, dial_code: str = None, format_type: str = "international") -> str:
    """
    格式化电话号码
    
    Args:
        phone: 电话号码（可包含各种分隔符）
        dial_code: 可选的国际区号，若不提供则自动尝试检测
        format_type: 格式类型
            - "international": 国际格式 +86 138 0013 8000
            - "e164": E.164格式 +8613800138000
            - "local": 本地格式 138-0013-8000
            - "readable": 易读格式 +86 138-0013-8000
            
    Returns:
        格式化后的电话号码字符串
        
    Examples:
        >>> format_phone_number("13800138000", "86", "international")
        '+86 138 0013 8000'
        
        >>> format_phone_number("13800138000", "86", "e164")
        '+8613800138000'
        
        >>> format_phone_number("13800138000", "86", "local")
        '138-0013-8000'
    """
    # 清理电话号码，只保留数字
    digits = re.sub(r"[^\d]", "", phone)
    
    # 尝试从电话号码中提取区号
    if dial_code is None:
        # 尝试匹配区号
        for code in sorted(_DIAL_CODE_DATA.keys(), key=len, reverse=True):
            clean_code = _clean_dial_code(code)
            if digits.startswith(clean_code):
                dial_code = clean_code
                digits = digits[len(clean_code):]
                break
    
    # 如果电话号码以区号开头，移除它
    if dial_code:
        clean_code = _clean_dial_code(dial_code)
        if digits.startswith(clean_code):
            digits = digits[len(clean_code):]
    
    # 清理区号格式（移除可能的"1-"前缀，用于像1-340这样的特殊区号）
    clean_dial_code = dial_code.replace("1-", "") if dial_code and dial_code.startswith("1-") else dial_code
    
    # 根据格式类型格式化
    if format_type == "e164":
        if clean_dial_code:
            return f"+{clean_dial_code}{digits}"
        return f"+{digits}"
    
    elif format_type == "international":
        # 根据号码长度智能分组
        if len(digits) == 11:  # 中国手机号
            formatted = f"{digits[:3]} {digits[3:7]} {digits[7:]}"
        elif len(digits) == 10:  # 美国手机号
            formatted = f"{digits[:3]} {digits[3:6]} {digits[6:]}"
        elif len(digits) == 9:
            formatted = f"{digits[:2]} {digits[2:5]} {digits[5:]}"
        else:
            # 默认格式
            formatted = " ".join([digits[i:i+4] for i in range(0, len(digits), 4)])
        
        if clean_dial_code:
            return f"+{clean_dial_code} {formatted}"
        return formatted
    
    elif format_type == "local":
        if len(digits) == 11:
            return f"{digits[:3]}-{digits[3:7]}-{digits[7:]}"
        elif len(digits) == 10:
            return f"{digits[:3]}-{digits[3:6]}-{digits[6:]}"
        elif len(digits) == 9:
            return f"{digits[:2]}-{digits[2:5]}-{digits[5:]}"
        else:
            return "-".join([digits[i:i+4] for i in range(0, len(digits), 4)])
    
    elif format_type == "readable":
        if len(digits) == 11:
            formatted = f"{digits[:3]}-{digits[3:7]}-{digits[7:]}"
        elif len(digits) == 10:
            formatted = f"{digits[:3]}-{digits[3:6]}-{digits[6:]}"
        else:
            formatted = "-".join([digits[i:i+4] for i in range(0, len(digits), 4)])
        
        if clean_dial_code:
            return f"+{clean_dial_code} {formatted}"
        return formatted
    
    return digits


def validate_phone_number(phone: str, dial_code: str = None) -> Tuple[bool, str]:
    """
    验证电话号码格式是否正确
    
    Args:
        phone: 电话号码
        dial_code: 可选的国际区号
        
    Returns:
        (是否有效, 错误信息或格式化号码)
        
    Examples:
        >>> validate_phone_number("13800138000", "86")
        (True, '+8613800138000')
        
        >>> validate_phone_number("123", "86")
        (False, '电话号码长度不足')
    """
    # 清理电话号码
    digits = re.sub(r"[^\d]", "", phone)
    
    if not digits:
        return False, "电话号码不能为空"
    
    if len(digits) < 4:
        return False, "电话号码长度不足"
    
    if len(digits) > 15:
        return False, "电话号码过长"
    
    # 如果指定了区号，进行更详细的验证
    if dial_code:
        clean_code = _clean_dial_code(dial_code)
        clean_code = clean_code.lstrip("+")  # 移除可能的+前缀
        
        # 检查号码是否以区号开头
        if digits.startswith(clean_code):
            local_number = digits[len(clean_code):]
        else:
            local_number = digits
        
        # 特定国家的验证规则
        if clean_code == "86":  # 中国
            if len(local_number) != 11:
                return False, f"中国手机号应为11位，当前{len(local_number)}位"
            if not local_number.startswith("1"):
                return False, "中国手机号应以1开头"
        
        elif clean_code == "1":  # 北美
            if len(local_number) != 10:
                return False, f"北美电话号码应为10位，当前{len(local_number)}位"
        
        return True, f"+{clean_code}{local_number}"
    
    return True, f"+{digits}"


def extract_dial_code(phone: str) -> Tuple[Optional[str], str]:
    """
    从电话号码中提取区号和本地号码
    
    Args:
        phone: 电话号码（可带+前缀）
        
    Returns:
        (区号, 本地号码) 元组
        
    Examples:
        >>> extract_dial_code("+8613800138000")
        ('86', '13800138000')
        
        >>> extract_dial_code("008613800138000")
        ('86', '13800138000')
    """
    # 清理电话号码
    phone = phone.strip()
    
    # 处理+前缀
    if phone.startswith("+"):
        digits = phone[1:]
    # 处理00国际前缀
    elif phone.startswith("00"):
        digits = phone[2:]
    else:
        digits = phone
    
    digits = re.sub(r"[^\d]", "", digits)
    
    if not digits:
        return None, ""
    
    # 尝试匹配区号（从最长到最短）
    for code in sorted(_DIAL_CODE_DATA.keys(), key=len, reverse=True):
        clean_code = _clean_dial_code(code)
        if digits.startswith(clean_code):
            local_number = digits[len(clean_code):]
            return clean_code, local_number
    
    return None, digits


def get_country_name(dial_code: str, lang: str = "zh") -> Optional[str]:
    """
    获取国家名称
    
    Args:
        dial_code: 电话区号
        lang: 语言代码 ("zh" 中文, "en" 英文)
        
    Returns:
        国家名称字符串
        
    Examples:
        >>> get_country_name("86")
        '中国'
        
        >>> get_country_name("86", "en")
        'China'
    """
    country_data = get_country_by_dial_code(dial_code)
    if not country_data:
        return None
    
    if lang == "zh":
        return country_data.get("name", "")
    else:
        # 返回英文代码或名称
        return country_data.get("en_name", country_data.get("code", country_data.get("name", "")))


def is_valid_dial_code(dial_code: str) -> bool:
    """
    检查区号是否有效
    
    Args:
        dial_code: 电话区号
        
    Returns:
        是否有效
        
    Examples:
        >>> is_valid_dial_code("86")
        True
        
        >>> is_valid_dial_code("999")
        False
    """
    dial_code = dial_code.strip().lstrip("+").lstrip("0")
    return dial_code in _DIAL_CODE_DATA


def search_countries(query: str) -> List[Dict]:
    """
    搜索国家（支持模糊匹配）
    
    Args:
        query: 搜索关键词（国家名、代码、区号）
        
    Returns:
        匹配的国家列表
        
    Examples:
        >>> results = search_countries("中国")
        >>> len(results) >= 1
        True
        
        >>> results = search_countries("86")
        >>> results[0]["name"]
        '中国'
    """
    query = query.strip().lower()
    results = []
    
    for dial_code, data in _DIAL_CODE_DATA.items():
        # 区号匹配
        if query in dial_code:
            item = {"dial_code": dial_code}
            item.update(data)
            results.append(item)
            continue
        
        # 名称匹配
        if query in data.get("name", "").lower():
            item = {"dial_code": dial_code}
            item.update(data)
            results.append(item)
            continue
        
        # 代码匹配
        if "/" in data.get("code", ""):
            codes = data["code"].lower().split("/")
            if any(query in c for c in codes):
                item = {"dial_code": dial_code}
                item.update(data)
                results.append(item)
                continue
        elif query in data.get("code", "").lower():
            item = {"dial_code": dial_code}
            item.update(data)
            results.append(item)
            continue
        
        # alpha3匹配
        if "/" in data.get("alpha3", ""):
            a3s = data["alpha3"].lower().split("/")
            if any(query in a3 for a3 in a3s):
                item = {"dial_code": dial_code}
                item.update(data)
                results.append(item)
        elif query in data.get("alpha3", "").lower():
            item = {"dial_code": dial_code}
            item.update(data)
            results.append(item)
    
    return results


def compare_dial_codes(code1: str, code2: str) -> Dict:
    """
    比较两个区号
    
    Args:
        code1: 第一个区号
        code2: 第二个区号
        
    Returns:
        比较结果字典
        
    Examples:
        >>> result = compare_dial_codes("86", "1")
        >>> result["same_continent"]
        False
    """
    country1 = get_country_by_dial_code(code1)
    country2 = get_country_by_dial_code(code2)
    
    if not country1 or not country2:
        return {
            "valid": False,
            "error": "一个或多个区号无效"
        }
    
    return {
        "valid": True,
        "country1": country1,
        "country2": country2,
        "same_continent": country1.get("continent") == country2.get("continent"),
        "same_region": country1.get("continent") == country2.get("continent"),
        "numeric_difference": abs(int(_clean_dial_code(code1) or "0") - int(_clean_dial_code(code2) or "0"))
    }


class DialCodeUtils:
    """国际电话区号工具类"""
    
    @staticmethod
    def get_country(dial_code: str) -> Optional[Dict]:
        """获取区号对应的国家信息"""
        return get_country_by_dial_code(dial_code)
    
    @staticmethod
    def get_dial_code(country: str) -> Optional[str]:
        """获取国家对应的区号"""
        return get_dial_code_by_country(country)
    
    @staticmethod
    def get_all() -> List[Dict]:
        """获取所有国家信息"""
        return get_all_countries()
    
    @staticmethod
    def get_by_continent(continent: str) -> List[Dict]:
        """按大洲获取国家"""
        return get_countries_by_continent(continent)
    
    @staticmethod
    def format_phone(phone: str, dial_code: str = None, format_type: str = "international") -> str:
        """格式化电话号码"""
        return format_phone_number(phone, dial_code, format_type)
    
    @staticmethod
    def validate(phone: str, dial_code: str = None) -> Tuple[bool, str]:
        """验证电话号码"""
        return validate_phone_number(phone, dial_code)
    
    @staticmethod
    def extract(phone: str) -> Tuple[Optional[str], str]:
        """提取区号和本地号码"""
        return extract_dial_code(phone)
    
    @staticmethod
    def search(query: str) -> List[Dict]:
        """搜索国家"""
        return search_countries(query)
    
    @staticmethod
    def is_valid(dial_code: str) -> bool:
        """检查区号是否有效"""
        return is_valid_dial_code(dial_code)
    
    @staticmethod
    def compare(code1: str, code2: str) -> Dict:
        """比较两个区号"""
        return compare_dial_codes(code1, code2)


if __name__ == "__main__":
    # 简单演示
    print("=== 国际电话区号工具演示 ===\n")
    
    # 查询区号对应国家
    print("区号 86 对应:", get_country_by_dial_code("86"))
    print("区号 +1 对应:", get_country_by_dial_code("+1"))
    print()
    
    # 查询国家对应区号
    print("中国区号:", get_dial_code_by_country("中国"))
    print("美国区号:", get_dial_code_by_country("US"))
    print("日本区号:", get_dial_code_by_country("JP"))
    print()
    
    # 格式化电话号码
    print("格式化电话号码:")
    print("  国际格式:", format_phone_number("13800138000", "86", "international"))
    print("  E.164格式:", format_phone_number("13800138000", "86", "e164"))
    print("  本地格式:", format_phone_number("13800138000", "86", "local"))
    print("  易读格式:", format_phone_number("13800138000", "86", "readable"))
    print()
    
    # 验证电话号码
    print("验证电话号码:")
    print("  13800138000:", validate_phone_number("13800138000", "86"))
    print("  123:", validate_phone_number("123", "86"))
    print()
    
    # 搜索国家
    print("搜索'中国':", [r["name"] for r in search_countries("中国")])
    print("搜索'86':", [r["name"] for r in search_countries("86")])