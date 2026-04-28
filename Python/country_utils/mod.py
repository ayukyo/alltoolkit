#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AllToolkit - Country Utilities Module

ISO 3166 country codes and utilities with zero external dependencies.
Provides country lookup, validation, and information retrieval.

Features:
- ISO 3166-1 alpha-2, alpha-3, and numeric codes
- Country names in English and Chinese
- Continent/region information
- Phone calling codes
- Currency codes
- Country search and validation
- Flag emoji generation

Author: AllToolkit
License: MIT
"""

from typing import Dict, List, Optional, Tuple, Set
from dataclasses import dataclass


# =============================================================================
# Country Data Structure
# =============================================================================

@dataclass
class Country:
    """Country information data class"""
    alpha2: str           # ISO 3166-1 alpha-2 code (e.g., "US")
    alpha3: str           # ISO 3166-1 alpha-3 code (e.g., "USA")
    numeric: str          # ISO 3166-1 numeric code (e.g., "840")
    name_en: str          # English name
    name_zh: str          # Chinese name
    continent: str        # Continent
    region: str           # Region
    calling_code: str     # International calling code
    currency: str         # ISO 4217 currency code
    flag_emoji: str       # Flag emoji
    
    def __repr__(self) -> str:
        return f"Country({self.alpha2}, {self.name_en})"
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            'alpha2': self.alpha2,
            'alpha3': self.alpha3,
            'numeric': self.numeric,
            'name_en': self.name_en,
            'name_zh': self.name_zh,
            'continent': self.continent,
            'region': self.region,
            'calling_code': self.calling_code,
            'currency': self.currency,
            'flag_emoji': self.flag_emoji
        }


# =============================================================================
# ISO 3166-1 Country Data
# =============================================================================

# Complete ISO 3166-1 country data
# Format: (alpha2, alpha3, numeric, name_en, name_zh, continent, region, calling_code, currency)
_COUNTRIES_DATA: Tuple[Tuple[str, str, str, str, str, str, str, str, str], ...] = (
    # Asia - East Asia
    ("CN", "CHN", "156", "China", "中国", "Asia", "East Asia", "+86", "CNY"),
    ("JP", "JPN", "392", "Japan", "日本", "Asia", "East Asia", "+81", "JPY"),
    ("KR", "KOR", "410", "South Korea", "韩国", "Asia", "East Asia", "+82", "KRW"),
    ("KP", "PRK", "408", "North Korea", "朝鲜", "Asia", "East Asia", "+850", "KPW"),
    ("TW", "TWN", "158", "Taiwan", "台湾", "Asia", "East Asia", "+886", "TWD"),
    ("HK", "HKG", "344", "Hong Kong", "香港", "Asia", "East Asia", "+852", "HKD"),
    ("MO", "MAC", "446", "Macau", "澳门", "Asia", "East Asia", "+853", "MOP"),
    ("MN", "MNG", "496", "Mongolia", "蒙古", "Asia", "East Asia", "+976", "MNT"),
    
    # Asia - Southeast Asia
    ("VN", "VNM", "704", "Vietnam", "越南", "Asia", "Southeast Asia", "+84", "VND"),
    ("TH", "THA", "764", "Thailand", "泰国", "Asia", "Southeast Asia", "+66", "THB"),
    ("MY", "MYS", "458", "Malaysia", "马来西亚", "Asia", "Southeast Asia", "+60", "MYR"),
    ("SG", "SGP", "702", "Singapore", "新加坡", "Asia", "Southeast Asia", "+65", "SGD"),
    ("ID", "IDN", "360", "Indonesia", "印度尼西亚", "Asia", "Southeast Asia", "+62", "IDR"),
    ("PH", "PHL", "608", "Philippines", "菲律宾", "Asia", "Southeast Asia", "+63", "PHP"),
    ("MM", "MMR", "104", "Myanmar", "缅甸", "Asia", "Southeast Asia", "+95", "MMK"),
    ("LA", "LAO", "418", "Laos", "老挝", "Asia", "Southeast Asia", "+856", "LAK"),
    ("KH", "KHM", "116", "Cambodia", "柬埔寨", "Asia", "Southeast Asia", "+855", "KHR"),
    ("BN", "BRN", "096", "Brunei", "文莱", "Asia", "Southeast Asia", "+673", "BND"),
    ("TL", "TLS", "626", "Timor-Leste", "东帝汶", "Asia", "Southeast Asia", "+670", "USD"),
    
    # Asia - South Asia
    ("IN", "IND", "356", "India", "印度", "Asia", "South Asia", "+91", "INR"),
    ("PK", "PAK", "586", "Pakistan", "巴基斯坦", "Asia", "South Asia", "+92", "PKR"),
    ("BD", "BGD", "050", "Bangladesh", "孟加拉国", "Asia", "South Asia", "+880", "BDT"),
    ("LK", "LKA", "144", "Sri Lanka", "斯里兰卡", "Asia", "South Asia", "+94", "LKR"),
    ("NP", "NPL", "524", "Nepal", "尼泊尔", "Asia", "South Asia", "+977", "NPR"),
    ("BT", "BTN", "064", "Bhutan", "不丹", "Asia", "South Asia", "+975", "BTN"),
    ("MV", "MDV", "462", "Maldives", "马尔代夫", "Asia", "South Asia", "+960", "MVR"),
    
    # Asia - Central Asia
    ("KZ", "KAZ", "398", "Kazakhstan", "哈萨克斯坦", "Asia", "Central Asia", "+7", "KZT"),
    ("UZ", "UZB", "860", "Uzbekistan", "乌兹别克斯坦", "Asia", "Central Asia", "+998", "UZS"),
    ("KG", "KGZ", "417", "Kyrgyzstan", "吉尔吉斯斯坦", "Asia", "Central Asia", "+996", "KGS"),
    ("TJ", "TJK", "762", "Tajikistan", "塔吉克斯坦", "Asia", "Central Asia", "+992", "TJS"),
    ("TM", "TKM", "795", "Turkmenistan", "土库曼斯坦", "Asia", "Central Asia", "+993", "TMT"),
    
    # Asia - West Asia / Middle East
    ("SA", "SAU", "682", "Saudi Arabia", "沙特阿拉伯", "Asia", "West Asia", "+966", "SAR"),
    ("AE", "ARE", "784", "United Arab Emirates", "阿联酋", "Asia", "West Asia", "+971", "AED"),
    ("IL", "ISR", "376", "Israel", "以色列", "Asia", "West Asia", "+972", "ILS"),
    ("TR", "TUR", "792", "Turkey", "土耳其", "Asia", "West Asia", "+90", "TRY"),
    ("IR", "IRN", "364", "Iran", "伊朗", "Asia", "West Asia", "+98", "IRR"),
    ("IQ", "IRQ", "368", "Iraq", "伊拉克", "Asia", "West Asia", "+964", "IQD"),
    ("JO", "JOR", "400", "Jordan", "约旦", "Asia", "West Asia", "+962", "JOD"),
    ("LB", "LBN", "422", "Lebanon", "黎巴嫩", "Asia", "West Asia", "+961", "LBP"),
    ("SY", "SYR", "760", "Syria", "叙利亚", "Asia", "West Asia", "+963", "SYP"),
    ("PS", "PSE", "275", "Palestine", "巴勒斯坦", "Asia", "West Asia", "+970", "ILS"),
    ("YE", "YEM", "887", "Yemen", "也门", "Asia", "West Asia", "+967", "YER"),
    ("OM", "OMN", "512", "Oman", "阿曼", "Asia", "West Asia", "+968", "OMR"),
    ("KW", "KWT", "414", "Kuwait", "科威特", "Asia", "West Asia", "+965", "KWD"),
    ("QA", "QAT", "634", "Qatar", "卡塔尔", "Asia", "West Asia", "+974", "QAR"),
    ("BH", "BHR", "048", "Bahrain", "巴林", "Asia", "West Asia", "+973", "BHD"),
    ("CY", "CYP", "196", "Cyprus", "塞浦路斯", "Asia", "West Asia", "+357", "EUR"),
    ("GE", "GEO", "268", "Georgia", "格鲁吉亚", "Asia", "West Asia", "+995", "GEL"),
    ("AM", "ARM", "051", "Armenia", "亚美尼亚", "Asia", "West Asia", "+374", "AMD"),
    ("AZ", "AZE", "031", "Azerbaijan", "阿塞拜疆", "Asia", "West Asia", "+994", "AZN"),
    
    # Europe - Northern Europe
    ("GB", "GBR", "826", "United Kingdom", "英国", "Europe", "Northern Europe", "+44", "GBP"),
    ("IE", "IRL", "372", "Ireland", "爱尔兰", "Europe", "Northern Europe", "+353", "EUR"),
    ("SE", "SWE", "752", "Sweden", "瑞典", "Europe", "Northern Europe", "+46", "SEK"),
    ("NO", "NOR", "578", "Norway", "挪威", "Europe", "Northern Europe", "+47", "NOK"),
    ("DK", "DNK", "208", "Denmark", "丹麦", "Europe", "Northern Europe", "+45", "DKK"),
    ("FI", "FIN", "246", "Finland", "芬兰", "Europe", "Northern Europe", "+358", "EUR"),
    ("IS", "ISL", "352", "Iceland", "冰岛", "Europe", "Northern Europe", "+354", "ISK"),
    ("EE", "EST", "233", "Estonia", "爱沙尼亚", "Europe", "Northern Europe", "+372", "EUR"),
    ("LV", "LVA", "428", "Latvia", "拉脱维亚", "Europe", "Northern Europe", "+371", "EUR"),
    ("LT", "LTU", "440", "Lithuania", "立陶宛", "Europe", "Northern Europe", "+370", "EUR"),
    
    # Europe - Western Europe
    ("DE", "DEU", "276", "Germany", "德国", "Europe", "Western Europe", "+49", "EUR"),
    ("FR", "FRA", "250", "France", "法国", "Europe", "Western Europe", "+33", "EUR"),
    ("NL", "NLD", "528", "Netherlands", "荷兰", "Europe", "Western Europe", "+31", "EUR"),
    ("BE", "BEL", "056", "Belgium", "比利时", "Europe", "Western Europe", "+32", "EUR"),
    ("LU", "LUX", "442", "Luxembourg", "卢森堡", "Europe", "Western Europe", "+352", "EUR"),
    ("AT", "AUT", "040", "Austria", "奥地利", "Europe", "Western Europe", "+43", "EUR"),
    ("CH", "CHE", "756", "Switzerland", "瑞士", "Europe", "Western Europe", "+41", "CHF"),
    ("LI", "LIE", "438", "Liechtenstein", "列支敦士登", "Europe", "Western Europe", "+423", "CHF"),
    ("MC", "MCO", "492", "Monaco", "摩纳哥", "Europe", "Western Europe", "+377", "EUR"),
    
    # Europe - Southern Europe
    ("IT", "ITA", "380", "Italy", "意大利", "Europe", "Southern Europe", "+39", "EUR"),
    ("ES", "ESP", "724", "Spain", "西班牙", "Europe", "Southern Europe", "+34", "EUR"),
    ("PT", "PRT", "620", "Portugal", "葡萄牙", "Europe", "Southern Europe", "+351", "EUR"),
    ("GR", "GRC", "300", "Greece", "希腊", "Europe", "Southern Europe", "+30", "EUR"),
    ("MT", "MLT", "470", "Malta", "马耳他", "Europe", "Southern Europe", "+356", "EUR"),
    ("VA", "VAT", "336", "Vatican City", "梵蒂冈", "Europe", "Southern Europe", "+379", "EUR"),
    ("SM", "SMR", "674", "San Marino", "圣马力诺", "Europe", "Southern Europe", "+378", "EUR"),
    ("AD", "AND", "020", "Andorra", "安道尔", "Europe", "Southern Europe", "+376", "EUR"),
    
    # Europe - Eastern Europe
    ("PL", "POL", "616", "Poland", "波兰", "Europe", "Eastern Europe", "+48", "PLN"),
    ("CZ", "CZE", "203", "Czech Republic", "捷克", "Europe", "Eastern Europe", "+420", "CZK"),
    ("SK", "SVK", "703", "Slovakia", "斯洛伐克", "Europe", "Eastern Europe", "+421", "EUR"),
    ("HU", "HUN", "348", "Hungary", "匈牙利", "Europe", "Eastern Europe", "+36", "HUF"),
    ("RO", "ROU", "642", "Romania", "罗马尼亚", "Europe", "Eastern Europe", "+40", "RON"),
    ("BG", "BGR", "100", "Bulgaria", "保加利亚", "Europe", "Eastern Europe", "+359", "BGN"),
    ("UA", "UKR", "804", "Ukraine", "乌克兰", "Europe", "Eastern Europe", "+380", "UAH"),
    ("BY", "BLR", "112", "Belarus", "白俄罗斯", "Europe", "Eastern Europe", "+375", "BYN"),
    ("MD", "MDA", "498", "Moldova", "摩尔多瓦", "Europe", "Eastern Europe", "+373", "MDL"),
    ("RU", "RUS", "643", "Russia", "俄罗斯", "Europe", "Eastern Europe", "+7", "RUB"),
    ("SI", "SVN", "705", "Slovenia", "斯洛文尼亚", "Europe", "Eastern Europe", "+386", "EUR"),
    ("HR", "HRV", "191", "Croatia", "克罗地亚", "Europe", "Eastern Europe", "+385", "EUR"),
    ("RS", "SRB", "688", "Serbia", "塞尔维亚", "Europe", "Eastern Europe", "+381", "RSD"),
    ("BA", "BIH", "070", "Bosnia and Herzegovina", "波黑", "Europe", "Eastern Europe", "+387", "BAM"),
    ("ME", "MNE", "499", "Montenegro", "黑山", "Europe", "Eastern Europe", "+382", "EUR"),
    ("MK", "MKD", "807", "North Macedonia", "北马其顿", "Europe", "Eastern Europe", "+389", "MKD"),
    ("AL", "ALB", "008", "Albania", "阿尔巴尼亚", "Europe", "Eastern Europe", "+355", "ALL"),
    ("XK", "XKX", "383", "Kosovo", "科索沃", "Europe", "Eastern Europe", "+383", "EUR"),
    
    # North America
    ("US", "USA", "840", "United States", "美国", "North America", "North America", "+1", "USD"),
    ("CA", "CAN", "124", "Canada", "加拿大", "North America", "North America", "+1", "CAD"),
    ("MX", "MEX", "484", "Mexico", "墨西哥", "North America", "North America", "+52", "MXN"),
    ("GT", "GTM", "320", "Guatemala", "危地马拉", "North America", "Central America", "+502", "GTQ"),
    ("BZ", "BLZ", "084", "Belize", "伯利兹", "North America", "Central America", "+501", "BZD"),
    ("SV", "SLV", "222", "El Salvador", "萨尔瓦多", "North America", "Central America", "+503", "USD"),
    ("HN", "HND", "340", "Honduras", "洪都拉斯", "North America", "Central America", "+504", "HNL"),
    ("NI", "NIC", "558", "Nicaragua", "尼加拉瓜", "North America", "Central America", "+505", "NIO"),
    ("CR", "CRI", "188", "Costa Rica", "哥斯达黎加", "North America", "Central America", "+506", "CRC"),
    ("PA", "PAN", "591", "Panama", "巴拿马", "North America", "Central America", "+507", "PAB"),
    ("CU", "CUB", "192", "Cuba", "古巴", "North America", "Caribbean", "+53", "CUP"),
    ("JM", "JAM", "388", "Jamaica", "牙买加", "North America", "Caribbean", "+1", "JMD"),
    ("HT", "HTI", "332", "Haiti", "海地", "North America", "Caribbean", "+509", "HTG"),
    ("DO", "DOM", "214", "Dominican Republic", "多米尼加", "North America", "Caribbean", "+1", "DOP"),
    ("PR", "PRI", "630", "Puerto Rico", "波多黎各", "North America", "Caribbean", "+1", "USD"),
    ("BS", "BHS", "044", "Bahamas", "巴哈马", "North America", "Caribbean", "+1", "BSD"),
    ("TT", "TTO", "780", "Trinidad and Tobago", "特立尼达和多巴哥", "North America", "Caribbean", "+1", "TTD"),
    
    # South America
    ("BR", "BRA", "076", "Brazil", "巴西", "South America", "South America", "+55", "BRL"),
    ("AR", "ARG", "032", "Argentina", "阿根廷", "South America", "South America", "+54", "ARS"),
    ("CL", "CHL", "152", "Chile", "智利", "South America", "South America", "+56", "CLP"),
    ("PE", "PER", "604", "Peru", "秘鲁", "South America", "South America", "+51", "PEN"),
    ("CO", "COL", "170", "Colombia", "哥伦比亚", "South America", "South America", "+57", "COP"),
    ("VE", "VEN", "862", "Venezuela", "委内瑞拉", "South America", "South America", "+58", "VES"),
    ("EC", "ECU", "218", "Ecuador", "厄瓜多尔", "South America", "South America", "+593", "USD"),
    ("BO", "BOL", "068", "Bolivia", "玻利维亚", "South America", "South America", "+591", "BOB"),
    ("PY", "PRY", "600", "Paraguay", "巴拉圭", "South America", "South America", "+595", "PYG"),
    ("UY", "URY", "858", "Uruguay", "乌拉圭", "South America", "South America", "+598", "UYU"),
    ("GY", "GUY", "328", "Guyana", "圭亚那", "South America", "South America", "+592", "GYD"),
    ("SR", "SUR", "740", "Suriname", "苏里南", "South America", "South America", "+597", "SRD"),
    
    # Africa - Northern Africa
    ("EG", "EGY", "818", "Egypt", "埃及", "Africa", "Northern Africa", "+20", "EGP"),
    ("LY", "LBY", "434", "Libya", "利比亚", "Africa", "Northern Africa", "+218", "LYD"),
    ("TN", "TUN", "788", "Tunisia", "突尼斯", "Africa", "Northern Africa", "+216", "TND"),
    ("DZ", "DZA", "012", "Algeria", "阿尔及利亚", "Africa", "Northern Africa", "+213", "DZD"),
    ("MA", "MAR", "504", "Morocco", "摩洛哥", "Africa", "Northern Africa", "+212", "MAD"),
    ("SD", "SDN", "729", "Sudan", "苏丹", "Africa", "Northern Africa", "+249", "SDG"),
    
    # Africa - Western Africa
    ("NG", "NGA", "566", "Nigeria", "尼日利亚", "Africa", "Western Africa", "+234", "NGN"),
    ("GH", "GHA", "288", "Ghana", "加纳", "Africa", "Western Africa", "+233", "GHS"),
    ("CI", "CIV", "384", "Ivory Coast", "科特迪瓦", "Africa", "Western Africa", "+225", "XOF"),
    ("SN", "SEN", "686", "Senegal", "塞内加尔", "Africa", "Western Africa", "+221", "XOF"),
    ("ML", "MLI", "466", "Mali", "马里", "Africa", "Western Africa", "+223", "XOF"),
    ("BF", "BFA", "854", "Burkina Faso", "布基纳法索", "Africa", "Western Africa", "+226", "XOF"),
    ("NE", "NER", "562", "Niger", "尼日尔", "Africa", "Western Africa", "+227", "XOF"),
    
    # Africa - Eastern Africa
    ("KE", "KEN", "404", "Kenya", "肯尼亚", "Africa", "Eastern Africa", "+254", "KES"),
    ("ET", "ETH", "231", "Ethiopia", "埃塞俄比亚", "Africa", "Eastern Africa", "+251", "ETB"),
    ("TZ", "TZA", "834", "Tanzania", "坦桑尼亚", "Africa", "Eastern Africa", "+255", "TZS"),
    ("UG", "UGA", "800", "Uganda", "乌干达", "Africa", "Eastern Africa", "+256", "UGX"),
    ("RW", "RWA", "646", "Rwanda", "卢旺达", "Africa", "Eastern Africa", "+250", "RWF"),
    ("SO", "SOM", "706", "Somalia", "索马里", "Africa", "Eastern Africa", "+252", "SOS"),
    
    # Africa - Southern Africa
    ("ZA", "ZAF", "710", "South Africa", "南非", "Africa", "Southern Africa", "+27", "ZAR"),
    ("ZW", "ZWE", "716", "Zimbabwe", "津巴布韦", "Africa", "Southern Africa", "+263", "ZWL"),
    ("ZW", "ZWE", "716", "Zimbabwe", "津巴布韦", "Africa", "Southern Africa", "+263", "ZWL"),
    ("ZM", "ZMB", "894", "Zambia", "赞比亚", "Africa", "Southern Africa", "+260", "ZMW"),
    ("BW", "BWA", "072", "Botswana", "博茨瓦纳", "Africa", "Southern Africa", "+267", "BWP"),
    ("NA", "NAM", "516", "Namibia", "纳米比亚", "Africa", "Southern Africa", "+264", "NAD"),
    ("MZ", "MOZ", "508", "Mozambique", "莫桑比克", "Africa", "Southern Africa", "+258", "MZN"),
    ("AO", "AGO", "024", "Angola", "安哥拉", "Africa", "Southern Africa", "+244", "AOA"),
    
    # Oceania
    ("AU", "AUS", "036", "Australia", "澳大利亚", "Oceania", "Oceania", "+61", "AUD"),
    ("NZ", "NZL", "554", "New Zealand", "新西兰", "Oceania", "Oceania", "+64", "NZD"),
    ("PG", "PNG", "598", "Papua New Guinea", "巴布亚新几内亚", "Oceania", "Oceania", "+675", "PGK"),
    ("FJ", "FJI", "242", "Fiji", "斐济", "Oceania", "Oceania", "+679", "FJD"),
    ("NC", "NCL", "540", "New Caledonia", "新喀里多尼亚", "Oceania", "Oceania", "+687", "XPF"),
    ("PF", "PYF", "258", "French Polynesia", "法属波利尼西亚", "Oceania", "Oceania", "+689", "XPF"),
    ("WS", "WSM", "882", "Samoa", "萨摩亚", "Oceania", "Oceania", "+685", "WST"),
    ("TO", "TON", "776", "Tonga", "汤加", "Oceania", "Oceania", "+676", "TOP"),
    ("VU", "VUT", "548", "Vanuatu", "瓦努阿图", "Oceania", "Oceania", "+678", "VUV"),
    ("SB", "SLB", "090", "Solomon Islands", "所罗门群岛", "Oceania", "Oceania", "+677", "SBD"),
    
    # Additional countries
    ("AF", "AFG", "004", "Afghanistan", "阿富汗", "Asia", "South Asia", "+93", "AFN"),
    ("AL", "ALB", "008", "Albania", "阿尔巴尼亚", "Europe", "Eastern Europe", "+355", "ALL"),
    ("DZ", "DZA", "012", "Algeria", "阿尔及利亚", "Africa", "Northern Africa", "+213", "DZD"),
    ("AO", "AGO", "024", "Angola", "安哥拉", "Africa", "Southern Africa", "+244", "AOA"),
    ("AG", "ATG", "028", "Antigua and Barbuda", "安提瓜和巴布达", "North America", "Caribbean", "+1", "XCD"),
    ("BB", "BRB", "052", "Barbados", "巴巴多斯", "North America", "Caribbean", "+1", "BBD"),
    ("BJ", "BEN", "204", "Benin", "贝宁", "Africa", "Western Africa", "+229", "XOF"),
    ("BT", "BTN", "064", "Bhutan", "不丹", "Asia", "South Asia", "+975", "BTN"),
    ("BO", "BOL", "068", "Bolivia", "玻利维亚", "South America", "South America", "+591", "BOB"),
    ("BA", "BIH", "070", "Bosnia and Herzegovina", "波黑", "Europe", "Eastern Europe", "+387", "BAM"),
    ("BW", "BWA", "072", "Botswana", "博茨瓦纳", "Africa", "Southern Africa", "+267", "BWP"),
    ("BN", "BRN", "096", "Brunei", "文莱", "Asia", "Southeast Asia", "+673", "BND"),
    ("BF", "BFA", "854", "Burkina Faso", "布基纳法索", "Africa", "Western Africa", "+226", "XOF"),
    ("BI", "BDI", "108", "Burundi", "布隆迪", "Africa", "Eastern Africa", "+257", "BIF"),
    ("CV", "CPV", "132", "Cabo Verde", "佛得角", "Africa", "Western Africa", "+238", "CVE"),
    ("CF", "CAF", "140", "Central African Republic", "中非", "Africa", "Central Africa", "+236", "XAF"),
    ("TD", "TCD", "148", "Chad", "乍得", "Africa", "Central Africa", "+235", "XAF"),
    ("KM", "COM", "174", "Comoros", "科摩罗", "Africa", "Eastern Africa", "+269", "KMF"),
    ("CG", "COG", "178", "Congo", "刚果（布）", "Africa", "Central Africa", "+242", "XAF"),
    ("CD", "COD", "180", "DR Congo", "刚果（金）", "Africa", "Central Africa", "+243", "CDF"),
    ("DJ", "DJI", "262", "Djibouti", "吉布提", "Africa", "Eastern Africa", "+253", "DJF"),
    ("DM", "DMA", "212", "Dominica", "多米尼克", "North America", "Caribbean", "+1", "XCD"),
    ("GQ", "GNQ", "226", "Equatorial Guinea", "赤道几内亚", "Africa", "Central Africa", "+240", "XAF"),
    ("ER", "ERI", "232", "Eritrea", "厄立特里亚", "Africa", "Eastern Africa", "+291", "ERN"),
    ("SZ", "SWZ", "748", "Eswatini", "斯威士兰", "Africa", "Southern Africa", "+268", "SZL"),
    ("FJ", "FJI", "242", "Fiji", "斐济", "Oceania", "Oceania", "+679", "FJD"),
    ("GA", "GAB", "266", "Gabon", "加蓬", "Africa", "Central Africa", "+241", "XAF"),
    ("GM", "GMB", "270", "Gambia", "冈比亚", "Africa", "Western Africa", "+220", "GMD"),
    ("GD", "GRD", "308", "Grenada", "格林纳达", "North America", "Caribbean", "+1", "XCD"),
    ("GN", "GIN", "324", "Guinea", "几内亚", "Africa", "Western Africa", "+224", "GNF"),
    ("GW", "GNB", "624", "Guinea-Bissau", "几内亚比绍", "Africa", "Western Africa", "+245", "XOF"),
    ("GY", "GUY", "328", "Guyana", "圭亚那", "South America", "South America", "+592", "GYD"),
    ("HT", "HTI", "332", "Haiti", "海地", "North America", "Caribbean", "+509", "HTG"),
    ("IS", "ISL", "352", "Iceland", "冰岛", "Europe", "Northern Europe", "+354", "ISK"),
    ("KI", "KIR", "296", "Kiribati", "基里巴斯", "Oceania", "Oceania", "+686", "AUD"),
    ("XK", "XKX", "383", "Kosovo", "科索沃", "Europe", "Eastern Europe", "+383", "EUR"),
    ("KG", "KGZ", "417", "Kyrgyzstan", "吉尔吉斯斯坦", "Asia", "Central Asia", "+996", "KGS"),
    ("LA", "LAO", "418", "Laos", "老挝", "Asia", "Southeast Asia", "+856", "LAK"),
    ("LS", "LSO", "426", "Lesotho", "莱索托", "Africa", "Southern Africa", "+266", "LSL"),
    ("LR", "LBR", "430", "Liberia", "利比里亚", "Africa", "Western Africa", "+231", "LRD"),
    ("LU", "LUX", "442", "Luxembourg", "卢森堡", "Europe", "Western Europe", "+352", "EUR"),
    ("MG", "MDG", "450", "Madagascar", "马达加斯加", "Africa", "Eastern Africa", "+261", "MGA"),
    ("MW", "MWI", "454", "Malawi", "马拉维", "Africa", "Eastern Africa", "+265", "MWK"),
    ("MV", "MDV", "462", "Maldives", "马尔代夫", "Asia", "South Asia", "+960", "MVR"),
    ("ML", "MLI", "466", "Mali", "马里", "Africa", "Western Africa", "+223", "XOF"),
    ("MR", "MRT", "478", "Mauritania", "毛里塔尼亚", "Africa", "Western Africa", "+222", "MRU"),
    ("MU", "MUS", "480", "Mauritius", "毛里求斯", "Africa", "Eastern Africa", "+230", "MUR"),
    ("FM", "FSM", "583", "Micronesia", "密克罗尼西亚", "Oceania", "Oceania", "+691", "USD"),
    ("MD", "MDA", "498", "Moldova", "摩尔多瓦", "Europe", "Eastern Europe", "+373", "MDL"),
    ("MC", "MCO", "492", "Monaco", "摩纳哥", "Europe", "Western Europe", "+377", "EUR"),
    ("ME", "MNE", "499", "Montenegro", "黑山", "Europe", "Eastern Europe", "+382", "EUR"),
    ("MA", "MAR", "504", "Morocco", "摩洛哥", "Africa", "Northern Africa", "+212", "MAD"),
    ("MZ", "MOZ", "508", "Mozambique", "莫桑比克", "Africa", "Southern Africa", "+258", "MZN"),
    ("MM", "MMR", "104", "Myanmar", "缅甸", "Asia", "Southeast Asia", "+95", "MMK"),
    ("NA", "NAM", "516", "Namibia", "纳米比亚", "Africa", "Southern Africa", "+264", "NAD"),
    ("NR", "NRU", "520", "Nauru", "瑙鲁", "Oceania", "Oceania", "+674", "AUD"),
    ("NP", "NPL", "524", "Nepal", "尼泊尔", "Asia", "South Asia", "+977", "NPR"),
    ("NI", "NIC", "558", "Nicaragua", "尼加拉瓜", "North America", "Central America", "+505", "NIO"),
    ("NE", "NER", "562", "Niger", "尼日尔", "Africa", "Western Africa", "+227", "XOF"),
    ("KP", "PRK", "408", "North Korea", "朝鲜", "Asia", "East Asia", "+850", "KPW"),
    ("MK", "MKD", "807", "North Macedonia", "北马其顿", "Europe", "Eastern Europe", "+389", "MKD"),
    ("NO", "NOR", "578", "Norway", "挪威", "Europe", "Northern Europe", "+47", "NOK"),
    ("OM", "OMN", "512", "Oman", "阿曼", "Asia", "West Asia", "+968", "OMR"),
    ("PK", "PAK", "586", "Pakistan", "巴基斯坦", "Asia", "South Asia", "+92", "PKR"),
    ("PW", "PLW", "585", "Palau", "帕劳", "Oceania", "Oceania", "+680", "USD"),
    ("PS", "PSE", "275", "Palestine", "巴勒斯坦", "Asia", "West Asia", "+970", "ILS"),
    ("PA", "PAN", "591", "Panama", "巴拿马", "North America", "Central America", "+507", "PAB"),
    ("PG", "PNG", "598", "Papua New Guinea", "巴布亚新几内亚", "Oceania", "Oceania", "+675", "PGK"),
    ("PY", "PRY", "600", "Paraguay", "巴拉圭", "South America", "South America", "+595", "PYG"),
    ("PE", "PER", "604", "Peru", "秘鲁", "South America", "South America", "+51", "PEN"),
    ("PH", "PHL", "608", "Philippines", "菲律宾", "Asia", "Southeast Asia", "+63", "PHP"),
    ("QA", "QAT", "634", "Qatar", "卡塔尔", "Asia", "West Asia", "+974", "QAR"),
    ("RW", "RWA", "646", "Rwanda", "卢旺达", "Africa", "Eastern Africa", "+250", "RWF"),
    ("KN", "KNA", "659", "Saint Kitts and Nevis", "圣基茨和尼维斯", "North America", "Caribbean", "+1", "XCD"),
    ("LC", "LCA", "662", "Saint Lucia", "圣卢西亚", "North America", "Caribbean", "+1", "XCD"),
    ("VC", "VCT", "670", "Saint Vincent and the Grenadines", "圣文森特和格林纳丁斯", "North America", "Caribbean", "+1", "XCD"),
    ("WS", "WSM", "882", "Samoa", "萨摩亚", "Oceania", "Oceania", "+685", "WST"),
    ("SM", "SMR", "674", "San Marino", "圣马力诺", "Europe", "Southern Europe", "+378", "EUR"),
    ("ST", "STP", "678", "Sao Tome and Principe", "圣多美和普林西比", "Africa", "Central Africa", "+239", "STN"),
    ("SA", "SAU", "682", "Saudi Arabia", "沙特阿拉伯", "Asia", "West Asia", "+966", "SAR"),
    ("SN", "SEN", "686", "Senegal", "塞内加尔", "Africa", "Western Africa", "+221", "XOF"),
    ("RS", "SRB", "688", "Serbia", "塞尔维亚", "Europe", "Eastern Europe", "+381", "RSD"),
    ("SC", "SYC", "690", "Seychelles", "塞舌尔", "Africa", "Eastern Africa", "+248", "SCR"),
    ("SL", "SLE", "694", "Sierra Leone", "塞拉利昂", "Africa", "Western Africa", "+232", "SLL"),
    ("SG", "SGP", "702", "Singapore", "新加坡", "Asia", "Southeast Asia", "+65", "SGD"),
    ("SX", "SXM", "534", "Sint Maarten", "荷属圣马丁", "North America", "Caribbean", "+1", "ANG"),
    ("SK", "SVK", "703", "Slovakia", "斯洛伐克", "Europe", "Eastern Europe", "+421", "EUR"),
    ("SI", "SVN", "705", "Slovenia", "斯洛文尼亚", "Europe", "Eastern Europe", "+386", "EUR"),
    ("SB", "SLB", "090", "Solomon Islands", "所罗门群岛", "Oceania", "Oceania", "+677", "SBD"),
    ("SO", "SOM", "706", "Somalia", "索马里", "Africa", "Eastern Africa", "+252", "SOS"),
    ("SS", "SSD", "728", "South Sudan", "南苏丹", "Africa", "Eastern Africa", "+211", "SSP"),
    ("LK", "LKA", "144", "Sri Lanka", "斯里兰卡", "Asia", "South Asia", "+94", "LKR"),
    ("SD", "SDN", "729", "Sudan", "苏丹", "Africa", "Northern Africa", "+249", "SDG"),
    ("SR", "SUR", "740", "Suriname", "苏里南", "South America", "South America", "+597", "SRD"),
    ("SZ", "SWZ", "748", "Eswatini", "斯威士兰", "Africa", "Southern Africa", "+268", "SZL"),
    ("SE", "SWE", "752", "Sweden", "瑞典", "Europe", "Northern Europe", "+46", "SEK"),
    ("CH", "CHE", "756", "Switzerland", "瑞士", "Europe", "Western Europe", "+41", "CHF"),
    ("SY", "SYR", "760", "Syria", "叙利亚", "Asia", "West Asia", "+963", "SYP"),
    ("TW", "TWN", "158", "Taiwan", "台湾", "Asia", "East Asia", "+886", "TWD"),
    ("TJ", "TJK", "762", "Tajikistan", "塔吉克斯坦", "Asia", "Central Asia", "+992", "TJS"),
    ("TZ", "TZA", "834", "Tanzania", "坦桑尼亚", "Africa", "Eastern Africa", "+255", "TZS"),
    ("TL", "TLS", "626", "Timor-Leste", "东帝汶", "Asia", "Southeast Asia", "+670", "USD"),
    ("TG", "TGO", "768", "Togo", "多哥", "Africa", "Western Africa", "+228", "XOF"),
    ("TO", "TON", "776", "Tonga", "汤加", "Oceania", "Oceania", "+676", "TOP"),
    ("TT", "TTO", "780", "Trinidad and Tobago", "特立尼达和多巴哥", "North America", "Caribbean", "+1", "TTD"),
    ("TN", "TUN", "788", "Tunisia", "突尼斯", "Africa", "Northern Africa", "+216", "TND"),
    ("TR", "TUR", "792", "Turkey", "土耳其", "Asia", "West Asia", "+90", "TRY"),
    ("TM", "TKM", "795", "Turkmenistan", "土库曼斯坦", "Asia", "Central Asia", "+993", "TMT"),
    ("TV", "TUV", "798", "Tuvalu", "图瓦卢", "Oceania", "Oceania", "+688", "AUD"),
    ("UG", "UGA", "800", "Uganda", "乌干达", "Africa", "Eastern Africa", "+256", "UGX"),
    ("UA", "UKR", "804", "Ukraine", "乌克兰", "Europe", "Eastern Europe", "+380", "UAH"),
    ("AE", "ARE", "784", "United Arab Emirates", "阿联酋", "Asia", "West Asia", "+971", "AED"),
    ("UY", "URY", "858", "Uruguay", "乌拉圭", "South America", "South America", "+598", "UYU"),
    ("UZ", "UZB", "860", "Uzbekistan", "乌兹别克斯坦", "Asia", "Central Asia", "+998", "UZS"),
    ("VU", "VUT", "548", "Vanuatu", "瓦努阿图", "Oceania", "Oceania", "+678", "VUV"),
    ("VA", "VAT", "336", "Vatican City", "梵蒂冈", "Europe", "Southern Europe", "+379", "EUR"),
    ("VE", "VEN", "862", "Venezuela", "委内瑞拉", "South America", "South America", "+58", "VES"),
    ("VN", "VNM", "704", "Vietnam", "越南", "Asia", "Southeast Asia", "+84", "VND"),
    ("YE", "YEM", "887", "Yemen", "也门", "Asia", "West Asia", "+967", "YER"),
    ("ZM", "ZMB", "894", "Zambia", "赞比亚", "Africa", "Southern Africa", "+260", "ZMW"),
    ("ZW", "ZWE", "716", "Zimbabwe", "津巴布韦", "Africa", "Southern Africa", "+263", "ZWL"),
)


# =============================================================================
# Helper Functions
# =============================================================================

def _alpha2_to_flag_emoji(alpha2: str) -> str:
    """Convert alpha-2 code to flag emoji"""
    if len(alpha2) != 2:
        return ""
    # Convert each letter to regional indicator symbol
    # A = 🇦 (U+1F1E6), B = 🇧 (U+1F1E7), etc.
    base = 0x1F1E6 - ord('A')
    return chr(base + ord(alpha2[0].upper())) + chr(base + ord(alpha2[1].upper()))


def _build_country(data: Tuple) -> Country:
    """Build Country object from tuple data"""
    alpha2, alpha3, numeric, name_en, name_zh, continent, region, calling_code, currency = data
    flag_emoji = _alpha2_to_flag_emoji(alpha2)
    return Country(
        alpha2=alpha2,
        alpha3=alpha3,
        numeric=numeric,
        name_en=name_en,
        name_zh=name_zh,
        continent=continent,
        region=region,
        calling_code=calling_code,
        currency=currency,
        flag_emoji=flag_emoji
    )


# =============================================================================
# Data Indexing (built once at module load)
# =============================================================================

# Build country indexes
_BY_ALPHA2: Dict[str, Country] = {}
_BY_ALPHA3: Dict[str, Country] = {}
_BY_NUMERIC: Dict[str, Country] = {}
_BY_NAME_EN: Dict[str, Country] = {}
_BY_NAME_ZH: Dict[str, Country] = {}

_all_countries: List[Country] = []

for data in _COUNTRIES_DATA:
    country = _build_country(data)
    _all_countries.append(country)
    _BY_ALPHA2[country.alpha2] = country
    _BY_ALPHA3[country.alpha3] = country
    _BY_NUMERIC[country.numeric] = country
    _BY_NAME_EN[country.name_en.lower()] = country
    _BY_NAME_ZH[country.name_zh] = country

# Remove duplicates (some countries appear twice in data)
_all_countries = list({c.alpha2: c for c in _all_countries}.values())


# =============================================================================
# Main API Functions
# =============================================================================

def get_country(code: str) -> Optional[Country]:
    """
    Get country by code (alpha-2, alpha-3, or numeric).
    
    Args:
        code: Country code (e.g., "US", "USA", "840")
        
    Returns:
        Country object if found, None otherwise
        
    Examples:
        >>> get_country("US")
        Country(US, United States)
        >>> get_country("CHN")
        Country(CN, China)
        >>> get_country("840")
        Country(US, United States)
    """
    code = code.upper().strip()
    
    # Try alpha-2
    if len(code) == 2 and code in _BY_ALPHA2:
        return _BY_ALPHA2[code]
    
    # Try alpha-3
    if len(code) == 3 and code in _BY_ALPHA3:
        return _BY_ALPHA3[code]
    
    # Try numeric
    if code in _BY_NUMERIC:
        return _BY_NUMERIC[code]
    
    return None


def get_by_alpha2(alpha2: str) -> Optional[Country]:
    """
    Get country by ISO 3166-1 alpha-2 code.
    
    Args:
        alpha2: 2-letter country code (e.g., "US", "CN", "JP")
        
    Returns:
        Country object if found, None otherwise
        
    Examples:
        >>> get_by_alpha2("US").name_en
        'United States'
        >>> get_by_alpha2("cn").name_zh
        '中国'
    """
    return _BY_ALPHA2.get(alpha2.upper())


def get_by_alpha3(alpha3: str) -> Optional[Country]:
    """
    Get country by ISO 3166-1 alpha-3 code.
    
    Args:
        alpha3: 3-letter country code (e.g., "USA", "CHN", "JPN")
        
    Returns:
        Country object if found, None otherwise
        
    Examples:
        >>> get_by_alpha3("USA").alpha2
        'US'
        >>> get_by_alpha3("JPN").flag_emoji
        '🇯🇵'
    """
    return _BY_ALPHA3.get(alpha3.upper())


def get_by_numeric(numeric: str) -> Optional[Country]:
    """
    Get country by ISO 3166-1 numeric code.
    
    Args:
        numeric: 3-digit numeric code (e.g., "840", "156", "392")
        
    Returns:
        Country object if found, None otherwise
        
    Examples:
        >>> get_by_numeric("840").name_en
        'United States'
        >>> get_by_numeric("156").name_zh
        '中国'
    """
    return _BY_NUMERIC.get(numeric)


def get_by_name(name: str, lang: str = "en") -> Optional[Country]:
    """
    Get country by name.
    
    Args:
        name: Country name in English or Chinese
        lang: Language preference ("en" or "zh"), default "en"
        
    Returns:
        Country object if found, None otherwise
        
    Examples:
        >>> get_by_name("United States").alpha2
        'US'
        >>> get_by_name("中国").alpha2
        'CN'
        >>> get_by_name("日本").name_en
        'Japan'
    """
    name_lower = name.lower().strip()
    
    # Try English name first
    if name_lower in _BY_NAME_EN:
        return _BY_NAME_EN[name_lower]
    
    # Try Chinese name
    if name in _BY_NAME_ZH:
        return _BY_NAME_ZH[name]
    
    return None


def search_countries(query: str, limit: int = 10) -> List[Country]:
    """
    Search countries by name (supports both English and Chinese).
    
    Args:
        query: Search query (partial match)
        limit: Maximum number of results, default 10
        
    Returns:
        List of matching Country objects
        
    Examples:
        >>> len(search_countries("United"))
        2  # United States, United Kingdom
        >>> search_countries("韩")[0].name_zh
        '韩国'
        >>> search_countries("land", limit=5)  # Countries ending with "land"
        [...]
    """
    query = query.lower().strip()
    results = []
    
    for country in _all_countries:
        if (query in country.name_en.lower() or 
            query in country.name_zh or
            query in country.alpha2.lower() or
            query in country.alpha3.lower()):
            results.append(country)
            if len(results) >= limit:
                break
    
    return results


def get_all_countries() -> List[Country]:
    """
    Get all countries.
    
    Returns:
        List of all Country objects
        
    Examples:
        >>> len(get_all_countries())
        195+
        >>> get_all_countries()[0].alpha2
        'AF'
    """
    return sorted(_all_countries, key=lambda c: c.alpha2)


def get_countries_by_continent(continent: str) -> List[Country]:
    """
    Get all countries in a continent.
    
    Args:
        continent: Continent name (e.g., "Asia", "Europe", "Africa", 
                   "North America", "South America", "Oceania")
        
    Returns:
        List of Country objects in the specified continent
        
    Examples:
        >>> len(get_countries_by_continent("Asia"))
        48
        >>> get_countries_by_continent("Europe")[0].continent
        'Europe'
    """
    continent = continent.strip().title()
    return sorted(
        [c for c in _all_countries if c.continent == continent],
        key=lambda c: c.name_en
    )


def get_countries_by_region(region: str) -> List[Country]:
    """
    Get all countries in a region.
    
    Args:
        region: Region name (e.g., "East Asia", "Southeast Asia", 
                 "Western Europe", "Northern Africa")
        
    Returns:
        List of Country objects in the specified region
        
    Examples:
        >>> len(get_countries_by_region("East Asia"))
        8
        >>> get_countries_by_region("Southeast Asia")[0].region
        'Southeast Asia'
    """
    region = region.strip().title()
    return sorted(
        [c for c in _all_countries if c.region == region],
        key=lambda c: c.name_en
    )


def validate_alpha2(code: str) -> bool:
    """
    Validate if a string is a valid ISO 3166-1 alpha-2 code.
    
    Args:
        code: 2-letter code to validate
        
    Returns:
        True if valid, False otherwise
        
    Examples:
        >>> validate_alpha2("US")
        True
        >>> validate_alpha2("XX")
        False
        >>> validate_alpha2("USA")
        False
    """
    if not code or len(code) != 2:
        return False
    return code.upper() in _BY_ALPHA2


def validate_alpha3(code: str) -> bool:
    """
    Validate if a string is a valid ISO 3166-1 alpha-3 code.
    
    Args:
        code: 3-letter code to validate
        
    Returns:
        True if valid, False otherwise
        
    Examples:
        >>> validate_alpha3("USA")
        True
        >>> validate_alpha3("XXX")
        False
        >>> validate_alpha3("US")
        False
    """
    if not code or len(code) != 3:
        return False
    return code.upper() in _BY_ALPHA3


def validate_numeric(code: str) -> bool:
    """
    Validate if a string is a valid ISO 3166-1 numeric code.
    
    Args:
        code: 3-digit numeric code to validate
        
    Returns:
        True if valid, False otherwise
        
    Examples:
        >>> validate_numeric("840")
        True
        >>> validate_numeric("000")
        False
    """
    if not code or len(code) != 3 or not code.isdigit():
        return False
    return code in _BY_NUMERIC


def get_continents() -> Set[str]:
    """
    Get all continent names.
    
    Returns:
        Set of continent names
        
    Examples:
        >>> sorted(get_continents())
        ['Africa', 'Asia', 'Europe', 'North America', 'Oceania', 'South America']
    """
    return {c.continent for c in _all_countries}


def get_regions() -> Set[str]:
    """
    Get all region names.
    
    Returns:
        Set of region names
        
    Examples:
        >>> 'East Asia' in get_regions()
        True
    """
    return {c.region for c in _all_countries}


def alpha2_to_alpha3(alpha2: str) -> Optional[str]:
    """
    Convert ISO 3166-1 alpha-2 code to alpha-3 code.
    
    Args:
        alpha2: 2-letter country code
        
    Returns:
        3-letter country code if found, None otherwise
        
    Examples:
        >>> alpha2_to_alpha3("US")
        'USA'
        >>> alpha2_to_alpha3("CN")
        'CHN'
    """
    country = get_by_alpha2(alpha2)
    return country.alpha3 if country else None


def alpha3_to_alpha2(alpha3: str) -> Optional[str]:
    """
    Convert ISO 3166-1 alpha-3 code to alpha-2 code.
    
    Args:
        alpha3: 3-letter country code
        
    Returns:
        2-letter country code if found, None otherwise
        
    Examples:
        >>> alpha3_to_alpha2("USA")
        'US'
        >>> alpha3_to_alpha2("CHN")
        'CN'
    """
    country = get_by_alpha3(alpha3)
    return country.alpha2 if country else None


def alpha2_to_numeric(alpha2: str) -> Optional[str]:
    """
    Convert ISO 3166-1 alpha-2 code to numeric code.
    
    Args:
        alpha2: 2-letter country code
        
    Returns:
        3-digit numeric code if found, None otherwise
        
    Examples:
        >>> alpha2_to_numeric("US")
        '840'
        >>> alpha2_to_numeric("CN")
        '156'
    """
    country = get_by_alpha2(alpha2)
    return country.numeric if country else None


def numeric_to_alpha2(numeric: str) -> Optional[str]:
    """
    Convert ISO 3166-1 numeric code to alpha-2 code.
    
    Args:
        numeric: 3-digit numeric code
        
    Returns:
        2-letter country code if found, None otherwise
        
    Examples:
        >>> numeric_to_alpha2("840")
        'US'
        >>> numeric_to_alpha2("156")
        'CN'
    """
    country = get_by_numeric(numeric)
    return country.alpha2 if country else None


def get_flag_emoji(code: str) -> str:
    """
    Get flag emoji for a country code.
    
    Args:
        code: Country code (alpha-2, alpha-3, or numeric)
        
    Returns:
        Flag emoji string, or empty string if not found
        
    Examples:
        >>> get_flag_emoji("US")
        '🇺🇸'
        >>> get_flag_emoji("JP")
        '🇯🇵'
        >>> get_flag_emoji("CN")
        '🇨🇳'
    """
    country = get_country(code)
    return country.flag_emoji if country else ""


def get_calling_code(code: str) -> Optional[str]:
    """
    Get international calling code for a country.
    
    Args:
        code: Country code (alpha-2, alpha-3, or numeric)
        
    Returns:
        Calling code string if found, None otherwise
        
    Examples:
        >>> get_calling_code("US")
        '+1'
        >>> get_calling_code("CN")
        '+86'
        >>> get_calling_code("JP")
        '+81'
    """
    country = get_country(code)
    return country.calling_code if country else None


def get_currency(code: str) -> Optional[str]:
    """
    Get currency code for a country.
    
    Args:
        code: Country code (alpha-2, alpha-3, or numeric)
        
    Returns:
        ISO 4217 currency code if found, None otherwise
        
    Examples:
        >>> get_currency("US")
        'USD'
        >>> get_currency("CN")
        'CNY'
        >>> get_currency("JP")
        'JPY'
    """
    country = get_country(code)
    return country.currency if country else None


# =============================================================================
# Convenience Aliases
# =============================================================================

# Alias for get_country
find = get_country

# Alias for get_all_countries
all_countries = get_all_countries


# =============================================================================
# Module Info
# =============================================================================

__all__ = [
    # Classes
    'Country',
    # Lookup functions
    'get_country',
    'get_by_alpha2',
    'get_by_alpha3',
    'get_by_numeric',
    'get_by_name',
    'search_countries',
    'get_all_countries',
    'get_countries_by_continent',
    'get_countries_by_region',
    # Validation functions
    'validate_alpha2',
    'validate_alpha3',
    'validate_numeric',
    # Conversion functions
    'alpha2_to_alpha3',
    'alpha3_to_alpha2',
    'alpha2_to_numeric',
    'numeric_to_alpha2',
    # Info functions
    'get_flag_emoji',
    'get_calling_code',
    'get_currency',
    'get_continents',
    'get_regions',
    # Aliases
    'find',
    'all_countries',
]


if __name__ == "__main__":
    # Demo usage
    print("=== Country Utils Demo ===\n")
    
    # Get country by different codes
    print("Get by alpha-2:")
    us = get_by_alpha2("US")
    print(f"  US: {us.name_en} ({us.name_zh}) {us.flag_emoji}")
    
    print("\nGet by alpha-3:")
    chn = get_by_alpha3("CHN")
    print(f"  CHN: {chn.name_en} ({chn.name_zh}) {chn.flag_emoji}")
    
    print("\nGet by numeric:")
    jpn = get_by_numeric("392")
    print(f"  392: {jpn.name_en} ({jpn.name_zh}) {jpn.flag_emoji}")
    
    print("\nGet by name:")
    germany = get_by_name("德国")
    print(f"  德国: {germany.alpha2} ({germany.name_en})")
    
    print("\nSearch countries:")
    results = search_countries("United", limit=5)
    for c in results:
        print(f"  {c.flag_emoji} {c.name_en}")
    
    print("\nGet countries by continent:")
    asia = get_countries_by_continent("Asia")
    print(f"  Asia has {len(asia)} countries")
    
    print("\nGet countries by region:")
    east_asia = get_countries_by_region("East Asia")
    for c in east_asia:
        print(f"  {c.flag_emoji} {c.name_en} ({c.name_zh})")
    
    print("\nValidation:")
    print(f"  validate_alpha2('US'): {validate_alpha2('US')}")
    print(f"  validate_alpha3('USA'): {validate_alpha3('USA')}")
    print(f"  validate_numeric('840'): {validate_numeric('840')}")
    
    print("\nCode conversion:")
    print(f"  alpha2_to_alpha3('US'): {alpha2_to_alpha3('US')}")
    print(f"  alpha3_to_alpha2('CHN'): {alpha3_to_alpha2('CHN')}")
    print(f"  alpha2_to_numeric('JP'): {alpha2_to_numeric('JP')}")
    
    print("\nCountry info:")
    print(f"  US flag: {get_flag_emoji('US')}")
    print(f"  CN calling code: {get_calling_code('CN')}")
    print(f"  JP currency: {get_currency('JP')}")
    
    print(f"\nTotal countries: {len(get_all_countries())}")
    print(f"Continents: {sorted(get_continents())}")