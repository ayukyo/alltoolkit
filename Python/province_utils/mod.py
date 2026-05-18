"""
province_utils - 中国省份信息工具

功能:
- 省份查询（按名称、简称、代码）
- 城市查询
- 区号和邮编查询
- 省份相邻关系
- 行政区划层级关系
- 省份统计信息

零依赖，仅使用 Python 标准库
"""

from typing import Dict, List, Optional, Tuple, Set
from dataclasses import dataclass
from enum import Enum


class RegionType(Enum):
    """行政区划类型"""
    PROVINCE = "province"           # 省
    MUNICIPALITY = "municipality"   # 直辖市
    AUTONOMOUS_REGION = "autonomous_region"  # 自治区
    SPECIAL_ADMINISTRATIVE_REGION = "sar"    # 特别行政区


@dataclass
class Province:
    """省份信息"""
    name: str                       # 全称，如"北京市"
    short_name: str                 # 简称，如"京"
    code: str                       # 行政代码，如"110000"
    capital: str                    # 省会/首府
    region_type: RegionType         # 行政区划类型
    area_km2: int                  # 面积（平方公里）
    population: Optional[int]       # 人口（万人）
    cities: List[str]               # 下辖市
    area_codes: List[str]           # 电话区号
    neighbors: List[str]            # 相邻省份简称
    iso_code: Optional[str] = None  # ISO代码（港澳有）


# 中国省份数据（34个省级行政区）
PROVINCES: Dict[str, Province] = {
    # 直辖市
    "京": Province(
        name="北京市",
        short_name="京",
        code="110000",
        capital="北京",
        region_type=RegionType.MUNICIPALITY,
        area_km2=16410,
        population=2189,
        cities=["东城区", "西城区", "朝阳区", "丰台区", "石景山区", "海淀区",
                "门头沟区", "房山区", "通州区", "顺义区", "昌平区", "大兴区",
                "怀柔区", "平谷区", "密云区", "延庆区"],
        area_codes=["010"],
        neighbors=["津", "冀"]
    ),
    "津": Province(
        name="天津市",
        short_name="津",
        code="120000",
        capital="天津",
        region_type=RegionType.MUNICIPALITY,
        area_km2=11966,
        population=1387,
        cities=["和平区", "河东区", "河西区", "南开区", "河北区", "红桥区",
                "东丽区", "西青区", "津南区", "北辰区", "武清区", "宝坻区",
                "滨海新区", "宁河区", "静海区", "蓟州区"],
        area_codes=["022"],
        neighbors=["京", "冀"]
    ),
    "冀": Province(
        name="河北省",
        short_name="冀",
        code="130000",
        capital="石家庄市",
        region_type=RegionType.PROVINCE,
        area_km2=188800,
        population=7461,
        cities=["石家庄市", "唐山市", "秦皇岛市", "邯郸市", "邢台市", "保定市",
                "张家口市", "承德市", "沧州市", "廊坊市", "衡水市"],
        area_codes=["0311", "0315", "0335", "0310", "0319", "0312",
                    "0313", "0314", "0317", "0316", "0318"],
        neighbors=["京", "津", "辽", "蒙", "晋", "豫", "鲁"]
    ),
    "晋": Province(
        name="山西省",
        short_name="晋",
        code="140000",
        capital="太原市",
        region_type=RegionType.PROVINCE,
        area_km2=156700,
        population=3492,
        cities=["太原市", "大同市", "阳泉市", "长治市", "晋城市", "朔州市",
                "晋中市", "运城市", "忻州市", "临汾市", "吕梁市"],
        area_codes=["0351", "0352", "0353", "0355", "0356", "0349",
                    "0354", "0359", "0350", "0357", "0358"],
        neighbors=["冀", "蒙", "陕", "豫"]
    ),
    "蒙": Province(
        name="内蒙古自治区",
        short_name="蒙",
        code="150000",
        capital="呼和浩特市",
        region_type=RegionType.AUTONOMOUS_REGION,
        area_km2=1183000,
        population=2405,
        cities=["呼和浩特市", "包头市", "乌海市", "赤峰市", "通辽市", "鄂尔多斯市",
                "呼伦贝尔市", "巴彦淖尔市", "乌兰察布市", "兴安盟", "锡林郭勒盟",
                "阿拉善盟"],
        area_codes=["0471", "0472", "0473", "0476", "0475", "0477",
                    "0470", "0478", "0474", "0482", "0479", "0483"],
        neighbors=["黑", "吉", "辽", "冀", "晋", "陕", "宁", "甘"]
    ),
    "辽": Province(
        name="辽宁省",
        short_name="辽",
        code="210000",
        capital="沈阳市",
        region_type=RegionType.PROVINCE,
        area_km2=148000,
        population=4259,
        cities=["沈阳市", "大连市", "鞍山市", "抚顺市", "本溪市", "丹东市",
                "锦州市", "营口市", "阜新市", "辽阳市", "盘锦市", "铁岭市",
                "朝阳市", "葫芦岛市"],
        area_codes=["024", "0411", "0412", "0413", "0414", "0415",
                    "0416", "0417", "0418", "0419", "0427", "0410",
                    "0421", "0429"],
        neighbors=["吉", "蒙", "冀"]
    ),
    "吉": Province(
        name="吉林省",
        short_name="吉",
        code="220000",
        capital="长春市",
        region_type=RegionType.PROVINCE,
        area_km2=191000,
        population=2407,
        cities=["长春市", "吉林市", "四平市", "辽源市", "通化市", "白山市",
                "松原市", "白城市", "延边朝鲜族自治州"],
        area_codes=["0431", "0432", "0434", "0437", "0435", "0439",
                    "0438", "0436", "0433"],
        neighbors=["黑", "蒙", "辽"]
    ),
    "黑": Province(
        name="黑龙江省",
        short_name="黑",
        code="230000",
        capital="哈尔滨市",
        region_type=RegionType.PROVINCE,
        area_km2=473000,
        population=3125,
        cities=["哈尔滨市", "齐齐哈尔市", "鸡西市", "鹤岗市", "双鸭山市", "大庆市",
                "伊春市", "佳木斯市", "七台河市", "牡丹江市", "黑河市", "绥化市",
                "大兴安岭地区"],
        area_codes=["0451", "0452", "0467", "0468", "0469", "0459",
                    "0458", "0454", "0464", "0453", "0456", "0455", "0457"],
        neighbors=["吉", "蒙"]
    ),
    "沪": Province(
        name="上海市",
        short_name="沪",
        code="310000",
        capital="上海",
        region_type=RegionType.MUNICIPALITY,
        area_km2=6341,
        population=2487,
        cities=["黄浦区", "徐汇区", "长宁区", "静安区", "普陀区", "虹口区",
                "杨浦区", "闵行区", "宝山区", "嘉定区", "浦东新区", "金山区",
                "松江区", "青浦区", "奉贤区", "崇明区"],
        area_codes=["021"],
        neighbors=["苏", "浙"]
    ),
    "苏": Province(
        name="江苏省",
        short_name="苏",
        code="320000",
        capital="南京市",
        region_type=RegionType.PROVINCE,
        area_km2=107200,
        population=8505,
        cities=["南京市", "无锡市", "徐州市", "常州市", "苏州市", "南通市",
                "连云港市", "淮安市", "盐城市", "扬州市", "镇江市", "泰州市",
                "宿迁市"],
        area_codes=["025", "0510", "0516", "0519", "0512", "0513",
                    "0518", "0517", "0515", "0514", "0511", "0523", "0527"],
        neighbors=["鲁", "皖", "浙", "沪"]
    ),
    "浙": Province(
        name="浙江省",
        short_name="浙",
        code="330000",
        capital="杭州市",
        region_type=RegionType.PROVINCE,
        area_km2=105500,
        population=6540,
        cities=["杭州市", "宁波市", "温州市", "嘉兴市", "湖州市", "绍兴市",
                "金华市", "衢州市", "舟山市", "台州市", "丽水市"],
        area_codes=["0571", "0574", "0577", "0573", "0572", "0575",
                    "0579", "0570", "0580", "0576", "0578"],
        neighbors=["沪", "苏", "皖", "赣", "闽"]
    ),
    "皖": Province(
        name="安徽省",
        short_name="皖",
        code="340000",
        capital="合肥市",
        region_type=RegionType.PROVINCE,
        area_km2=140100,
        population=6103,
        cities=["合肥市", "芜湖市", "蚌埠市", "淮南市", "马鞍山市", "淮北市",
                "铜陵市", "安庆市", "黄山市", "滁州市", "阜阳市", "宿州市",
                "六安市", "亳州市", "池州市", "宣城市"],
        area_codes=["0551", "0553", "0552", "0554", "0555", "0561",
                    "0562", "0556", "0559", "0550", "0558", "0557",
                    "0564", "0558", "0566", "0563"],
        neighbors=["苏", "鲁", "豫", "鄂", "赣", "浙"]
    ),
    "闽": Province(
        name="福建省",
        short_name="闽",
        code="350000",
        capital="福州市",
        region_type=RegionType.PROVINCE,
        area_km2=124000,
        population=4154,
        cities=["福州市", "厦门市", "莆田市", "三明市", "泉州市", "漳州市",
                "南平市", "龙岩市", "宁德市"],
        area_codes=["0591", "0592", "0594", "0598", "0595", "0596",
                    "0599", "0597", "0593"],
        neighbors=["浙", "赣", "粤", "台"]
    ),
    "赣": Province(
        name="江西省",
        short_name="赣",
        code="360000",
        capital="南昌市",
        region_type=RegionType.PROVINCE,
        area_km2=166900,
        population=4519,
        cities=["南昌市", "景德镇市", "萍乡市", "九江市", "新余市", "鹰潭市",
                "赣州市", "吉安市", "宜春市", "抚州市", "上饶市"],
        area_codes=["0791", "0798", "0799", "0792", "0790", "0701",
                    "0797", "0796", "0795", "0794", "0793"],
        neighbors=["鄂", "皖", "浙", "闽", "粤", "湘"]
    ),
    "鲁": Province(
        name="山东省",
        short_name="鲁",
        code="370000",
        capital="济南市",
        region_type=RegionType.PROVINCE,
        area_km2=157900,
        population=10153,
        cities=["济南市", "青岛市", "淄博市", "枣庄市", "东营市", "烟台市",
                "潍坊市", "济宁市", "泰安市", "威海市", "日照市", "临沂市",
                "德州市", "聊城市", "滨州市", "菏泽市"],
        area_codes=["0531", "0532", "0533", "0632", "0546", "0535",
                    "0536", "0537", "0538", "0631", "0633", "0539",
                    "0534", "0635", "0543", "0530"],
        neighbors=["冀", "豫", "皖", "苏"]
    ),
    "豫": Province(
        name="河南省",
        short_name="豫",
        code="410000",
        capital="郑州市",
        region_type=RegionType.PROVINCE,
        area_km2=167000,
        population=9883,
        cities=["郑州市", "开封市", "洛阳市", "平顶山市", "安阳市", "鹤壁市",
                "新乡市", "焦作市", "濮阳市", "许昌市", "漯河市", "三门峡市",
                "南阳市", "商丘市", "信阳市", "周口市", "驻马店市", "济源市"],
        area_codes=["0371", "0378", "0379", "0375", "0372", "0392",
                    "0373", "0391", "0393", "0374", "0395", "0398",
                    "0377", "0370", "0376", "0394", "0396", "0391"],
        neighbors=["冀", "晋", "陕", "鄂", "皖", "鲁"]
    ),
    "鄂": Province(
        name="湖北省",
        short_name="鄂",
        code="420000",
        capital="武汉市",
        region_type=RegionType.PROVINCE,
        area_km2=185900,
        population=5775,
        cities=["武汉市", "黄石市", "十堰市", "宜昌市", "襄阳市", "鄂州市",
                "荆门市", "孝感市", "荆州市", "黄冈市", "咸宁市", "随州市",
                "恩施土家族苗族自治州", "仙桃市", "潜江市", "天门市", "神农架林区"],
        area_codes=["027", "0714", "0719", "0717", "0710", "0711",
                    "0724", "0712", "0716", "0713", "0715", "0722",
                    "0718", "0728", "0728", "0728", "0719"],
        neighbors=["陕", "渝", "湘", "赣", "皖", "豫"]
    ),
    "湘": Province(
        name="湖南省",
        short_name="湘",
        code="430000",
        capital="长沙市",
        region_type=RegionType.PROVINCE,
        area_km2=211800,
        population=6622,
        cities=["长沙市", "株洲市", "湘潭市", "衡阳市", "邵阳市", "岳阳市",
                "常德市", "张家界市", "益阳市", "郴州市", "永州市", "怀化市",
                "娄底市", "湘西土家族苗族自治州"],
        area_codes=["0731", "0733", "0732", "0734", "0739", "0730",
                    "0736", "0744", "0737", "0735", "0746", "0745",
                    "0738", "0743"],
        neighbors=["鄂", "赣", "粤", "桂", "黔", "渝"]
    ),
    "粤": Province(
        name="广东省",
        short_name="粤",
        code="440000",
        capital="广州市",
        region_type=RegionType.PROVINCE,
        area_km2=179800,
        population=12684,
        cities=["广州市", "韶关市", "深圳市", "珠海市", "汕头市", "佛山市",
                "江门市", "湛江市", "茂名市", "肇庆市", "惠州市", "梅州市",
                "汕尾市", "河源市", "阳江市", "清远市", "东莞市", "中山市",
                "潮州市", "揭阳市", "云浮市"],
        area_codes=["020", "0751", "0755", "0756", "0754", "0757",
                    "0750", "0759", "0668", "0758", "0752", "0753",
                    "0660", "0762", "0662", "0763", "0769", "0760",
                    "0768", "0663", "0766"],
        neighbors=["闽", "赣", "湘", "桂", "港", "澳"]
    ),
    "桂": Province(
        name="广西壮族自治区",
        short_name="桂",
        code="450000",
        capital="南宁市",
        region_type=RegionType.AUTONOMOUS_REGION,
        area_km2=237600,
        population=5013,
        cities=["南宁市", "柳州市", "桂林市", "梧州市", "北海市", "防城港市",
                "钦州市", "贵港市", "玉林市", "百色市", "贺州市", "河池市",
                "来宾市", "崇左市"],
        area_codes=["0771", "0772", "0773", "0774", "0779", "0770",
                    "0777", "0775", "0775", "0776", "0774", "0778",
                    "0772", "0771"],
        neighbors=["湘", "粤", "黔", "滇"]
    ),
    "琼": Province(
        name="海南省",
        short_name="琼",
        code="460000",
        capital="海口市",
        region_type=RegionType.PROVINCE,
        area_km2=35400,
        population=1008,
        cities=["海口市", "三亚市", "三沙市", "儋州市", "五指山市", "琼海市",
                "文昌市", "万宁市", "东方市"],
        area_codes=["0898", "0899", "0898", "0898"],
        neighbors=[]
    ),
    "渝": Province(
        name="重庆市",
        short_name="渝",
        code="500000",
        capital="重庆",
        region_type=RegionType.MUNICIPALITY,
        area_km2=82400,
        population=3212,
        cities=["万州区", "涪陵区", "渝中区", "大渡口区", "江北区", "沙坪坝区",
                "九龙坡区", "南岸区", "北碚区", "綦江区", "大足区", "渝北区",
                "巴南区", "黔江区", "长寿区", "江津区", "合川区", "永川区",
                "南川区", "璧山区", "铜梁区", "潼南区", "荣昌区", "开州区",
                "梁平区", "武隆区"],
        area_codes=["023"],
        neighbors=["川", "黔", "鄂", "湘", "陕"]
    ),
    "川": Province(
        name="四川省",
        short_name="川",
        code="510000",
        capital="成都市",
        region_type=RegionType.PROVINCE,
        area_km2=486000,
        population=8367,
        cities=["成都市", "自贡市", "攀枝花市", "泸州市", "德阳市", "绵阳市",
                "广元市", "遂宁市", "内江市", "乐山市", "南充市", "眉山市",
                "宜宾市", "广安市", "达州市", "雅安市", "巴中市", "资阳市",
                "阿坝藏族羌族自治州", "甘孜藏族自治州", "凉山彝族自治州"],
        area_codes=["028", "0813", "0812", "0830", "0838", "0816",
                    "0839", "0825", "0832", "0833", "0817", "0833",
                    "0831", "0826", "0818", "0835", "0827", "0832",
                    "0837", "0836", "0834"],
        neighbors=["青", "甘", "陕", "渝", "黔", "滇", "藏"]
    ),
    "黔": Province(
        name="贵州省",
        short_name="黔",
        code="520000",
        capital="贵阳市",
        region_type=RegionType.PROVINCE,
        area_km2=176100,
        population=3856,
        cities=["贵阳市", "六盘水市", "遵义市", "安顺市", "毕节市", "铜仁市",
                "黔西南布依族苗族自治州", "黔东南苗族侗族自治州", "黔南布依族苗族自治州"],
        area_codes=["0851", "0858", "0852", "0853", "0857", "0856",
                    "0859", "0855", "0854"],
        neighbors=["川", "滇", "桂", "湘", "渝"]
    ),
    "滇": Province(
        name="云南省",
        short_name="滇",
        code="530000",
        capital="昆明市",
        region_type=RegionType.PROVINCE,
        area_km2=394000,
        population=4721,
        cities=["昆明市", "曲靖市", "玉溪市", "保山市", "昭通市", "丽江市",
                "普洱市", "临沧市", "楚雄彝族自治州", "红河哈尼族彝族自治州",
                "文山壮族苗族自治州", "西双版纳傣族自治州", "大理白族自治州",
                "德宏傣族景颇族自治州", "怒江傈僳族自治州", "迪庆藏族自治州"],
        area_codes=["0871", "0874", "0877", "0875", "0870", "0888",
                    "0879", "0883", "0878", "0873", "0876", "0691",
                    "0872", "0692", "0886", "0887"],
        neighbors=["川", "黔", "桂", "藏"]
    ),
    "藏": Province(
        name="西藏自治区",
        short_name="藏",
        code="540000",
        capital="拉萨市",
        region_type=RegionType.AUTONOMOUS_REGION,
        area_km2=1228400,
        population=366,
        cities=["拉萨市", "日喀则市", "昌都市", "林芝市", "山南市", "那曲市",
                "阿里地区"],
        area_codes=["0891", "0892", "0895", "0894", "0893", "0896", "0897"],
        neighbors=["新", "青", "川", "滇"]
    ),
    "陕": Province(
        name="陕西省",
        short_name="陕",
        code="610000",
        capital="西安市",
        region_type=RegionType.PROVINCE,
        area_km2=205800,
        population=3953,
        cities=["西安市", "铜川市", "宝鸡市", "咸阳市", "渭南市", "延安市",
                "汉中市", "榆林市", "安康市", "商洛市"],
        area_codes=["029", "0919", "0917", "0910", "0913", "0911",
                    "0916", "0912", "0915", "0914"],
        neighbors=["蒙", "晋", "豫", "鄂", "渝", "川", "甘", "宁"]
    ),
    "甘": Province(
        name="甘肃省",
        short_name="甘",
        code="620000",
        capital="兰州市",
        region_type=RegionType.PROVINCE,
        area_km2=453700,
        population=2502,
        cities=["兰州市", "嘉峪关市", "金昌市", "白银市", "天水市", "武威市",
                "张掖市", "平凉市", "酒泉市", "庆阳市", "定西市", "陇南市",
                "临夏回族自治州", "甘南藏族自治州"],
        area_codes=["0931", "0937", "0935", "0943", "0938", "0935",
                    "0936", "0933", "0937", "0934", "0932", "0939",
                    "0930", "0941"],
        neighbors=["蒙", "宁", "陕", "川", "青", "新"]
    ),
    "青": Province(
        name="青海省",
        short_name="青",
        code="630000",
        capital="西宁市",
        region_type=RegionType.PROVINCE,
        area_km2=722000,
        population=592,
        cities=["西宁市", "海东市", "海北藏族自治州", "黄南藏族自治州",
                "海南藏族自治州", "果洛藏族自治州", "玉树藏族自治州",
                "海西蒙古族藏族自治州"],
        area_codes=["0971", "0972", "0970", "0973", "0974", "0975", "0976", "0977"],
        neighbors=["新", "甘", "川", "藏"]
    ),
    "宁": Province(
        name="宁夏回族自治区",
        short_name="宁",
        code="640000",
        capital="银川市",
        region_type=RegionType.AUTONOMOUS_REGION,
        area_km2=66400,
        population=720,
        cities=["银川市", "石嘴山市", "吴忠市", "固原市", "中卫市"],
        area_codes=["0951", "0952", "0953", "0954", "0955"],
        neighbors=["蒙", "甘", "陕"]
    ),
    "新": Province(
        name="新疆维吾尔自治区",
        short_name="新",
        code="650000",
        capital="乌鲁木齐市",
        region_type=RegionType.AUTONOMOUS_REGION,
        area_km2=1664900,
        population=2585,
        cities=["乌鲁木齐市", "克拉玛依市", "吐鲁番市", "哈密市", "昌吉回族自治州",
                "博尔塔拉蒙古自治州", "巴音郭楞蒙古自治州", "阿克苏地区",
                "克孜勒苏柯尔克孜自治州", "喀什地区", "和田地区", "伊犁哈萨克自治州",
                "塔城地区", "阿勒泰地区", "石河子市", "阿拉尔市", "图木舒克市",
                "五家渠市", "北屯市", "铁门关市", "双河市", "可克达拉市",
                "昆玉市", "胡杨河市", "新星市"],
        area_codes=["0991", "0990", "0995", "0902", "0994", "0909",
                    "0996", "0997", "0908", "0998", "0903", "0999",
                    "0901", "0906", "0993", "0997", "0998", "0994"],
        neighbors=["藏", "青", "甘"]
    ),
    "港": Province(
        name="香港特别行政区",
        short_name="港",
        code="810000",
        capital="香港",
        region_type=RegionType.SPECIAL_ADMINISTRATIVE_REGION,
        area_km2=1106,
        population=748,
        cities=["中西区", "湾仔区", "东区", "南区", "油尖旺区", "深水埗区",
                "九龙城区", "黄大仙区", "观塘区", "荃湾区", "屯门区", "元朗区",
                "北区", "大埔区", "西贡区", "沙田区", "葵青区", "离岛区"],
        area_codes=["852"],
        neighbors=["粤"],
        iso_code="HK"
    ),
    "澳": Province(
        name="澳门特别行政区",
        short_name="澳",
        code="820000",
        capital="澳门",
        region_type=RegionType.SPECIAL_ADMINISTRATIVE_REGION,
        area_km2=33,
        population=68,
        cities=["花地玛堂区", "花王堂区", "望德堂区", "大堂区", "风顺堂区",
                "嘉模堂区", "路凼填海区", "圣方济各堂区"],
        area_codes=["853"],
        neighbors=["粤"],
        iso_code="MO"
    ),
    "台": Province(
        name="台湾省",
        short_name="台",
        code="710000",
        capital="台北市",
        region_type=RegionType.PROVINCE,
        area_km2=36000,
        population=2356,
        cities=["台北市", "新北市", "桃园市", "台中市", "台南市", "高雄市",
                "基隆市", "新竹市", "嘉义市", "新竹县", "苗栗县", "彰化县",
                "南投县", "云林县", "嘉义县", "屏东县", "宜兰县", "花莲县",
                "台东县", "澎湖县", "金门县", "连江县"],
        area_codes=["886"],
        neighbors=["闽"],
        iso_code="TW"
    ),
}

# 索引缓存
_name_index: Dict[str, str] = {}
_code_index: Dict[str, str] = {}
_capital_index: Dict[str, str] = {}


def _build_indexes():
    """构建索引"""
    global _name_index, _code_index, _capital_index
    if _name_index:
        return
    
    for short, prov in PROVINCES.items():
        _name_index[prov.name] = short
        _code_index[prov.code] = short
        _capital_index[prov.capital] = short


def get_all_provinces() -> List[Province]:
    """
    获取所有省份列表
    
    Returns:
        省份列表
    """
    return list(PROVINCES.values())


def get_province_by_short(short_name: str) -> Optional[Province]:
    """
    通过简称获取省份
    
    Args:
        short_name: 省份简称，如"京"、"沪"
    
    Returns:
        省份信息，不存在则返回 None
    """
    return PROVINCES.get(short_name)


def get_province_by_name(name: str) -> Optional[Province]:
    """
    通过全称获取省份
    
    Args:
        name: 省份全称，如"北京市"、"广东省"
    
    Returns:
        省份信息，不存在则返回 None
    """
    _build_indexes()
    short = _name_index.get(name)
    return PROVINCES.get(short) if short else None


def get_province_by_code(code: str) -> Optional[Province]:
    """
    通过行政代码获取省份
    
    Args:
        code: 行政代码，如"110000"、"440000"
    
    Returns:
        省份信息，不存在则返回 None
    """
    _build_indexes()
    short = _code_index.get(code)
    return PROVINCES.get(short) if short else None


def get_province_by_capital(capital: str) -> Optional[Province]:
    """
    通过省会获取省份
    
    Args:
        capital: 省会名称，如"广州市"、"成都市"
    
    Returns:
        省份信息，不存在则返回 None
    """
    _build_indexes()
    short = _capital_index.get(capital)
    return PROVINCES.get(short) if short else None


def get_province_by_area_code(area_code: str) -> Optional[Province]:
    """
    通过电话区号获取省份
    
    Args:
        area_code: 电话区号，如"020"、"021"
    
    Returns:
        省份信息，不存在则返回 None
    """
    # 标准化区号（去除前导0，但保留完整匹配）
    area_code = area_code.strip()
    normalized = area_code.lstrip("0") or "0"
    
    for prov in PROVINCES.values():
        for ac in prov.area_codes:
            # 精确匹配（完整区号或去掉前导0后匹配）
            if ac == area_code or ac.lstrip("0") == normalized:
                return prov
    return None


def get_neighbors(short_name: str) -> List[Province]:
    """
    获取相邻省份
    
    Args:
        short_name: 省份简称
    
    Returns:
        相邻省份列表
    """
    prov = PROVINCES.get(short_name)
    if not prov:
        return []
    return [PROVINCES[s] for s in prov.neighbors if s in PROVINCES]


def search_province(keyword: str) -> List[Province]:
    """
    搜索省份
    
    Args:
        keyword: 搜索关键词（支持名称、简称、省会模糊匹配）
    
    Returns:
        匹配的省份列表
    """
    keyword = keyword.lower()
    results = []
    
    for prov in PROVINCES.values():
        if (keyword in prov.name.lower() or
            keyword in prov.short_name.lower() or
            keyword in prov.capital.lower()):
            results.append(prov)
    
    return results


def get_provinces_by_type(region_type: RegionType) -> List[Province]:
    """
    按行政区划类型获取省份
    
    Args:
        region_type: 行政区划类型
    
    Returns:
        该类型的省份列表
    """
    return [p for p in PROVINCES.values() if p.region_type == region_type]


def get_municipalities() -> List[Province]:
    """
    获取所有直辖市
    
    Returns:
        直辖市列表
    """
    return get_provinces_by_type(RegionType.MUNICIPALITY)


def get_autonomous_regions() -> List[Province]:
    """
    获取所有自治区
    
    Returns:
        自治区列表
    """
    return get_provinces_by_type(RegionType.AUTONOMOUS_REGION)


def get_special_administrative_regions() -> List[Province]:
    """
    获取所有特别行政区
    
    Returns:
        特别行政区列表
    """
    return get_provinces_by_type(RegionType.SPECIAL_ADMINISTRATIVE_REGION)


def get_province_cities(short_name: str) -> List[str]:
    """
    获取省份下辖城市
    
    Args:
        short_name: 省份简称
    
    Returns:
        城市列表
    """
    prov = PROVINCES.get(short_name)
    return prov.cities if prov else []


def get_province_statistics(short_name: str) -> Dict[str, any]:
    """
    获取省份统计信息
    
    Args:
        short_name: 省份简称
    
    Returns:
        统计信息字典
    """
    prov = PROVINCES.get(short_name)
    if not prov:
        return {}
    
    return {
        "name": prov.name,
        "area_km2": prov.area_km2,
        "population_万": prov.population,
        "city_count": len(prov.cities),
        "neighbor_count": len(prov.neighbors),
        "area_codes": prov.area_codes,
    }


def calculate_distance(short_name1: str, short_name2: str) -> Optional[int]:
    """
    计算两个省份之间的"邻接距离"
    
    相邻省份距离为 1，通过一个中间省份的距离为 2，以此类推。
    
    Args:
        short_name1: 第一个省份简称
        short_name2: 第二个省份简称
    
    Returns:
        邻接距离，无法到达则返回 None
    """
    if short_name1 not in PROVINCES or short_name2 not in PROVINCES:
        return None
    
    if short_name1 == short_name2:
        return 0
    
    # BFS 搜索
    visited = {short_name1}
    queue = [(short_name1, 0)]
    
    while queue:
        current, dist = queue.pop(0)
        
        prov = PROVINCES[current]
        for neighbor in prov.neighbors:
            if neighbor == short_name2:
                return dist + 1
            if neighbor not in visited and neighbor in PROVINCES:
                visited.add(neighbor)
                queue.append((neighbor, dist + 1))
    
    return None  # 无法到达（如海南、台湾）


def find_route(short_name1: str, short_name2: str) -> List[str]:
    """
    查找两个省份之间的最短路径
    
    Args:
        short_name1: 起始省份简称
        short_name2: 目标省份简称
    
    Returns:
        路径上的省份简称列表，无法到达则返回空列表
    """
    if short_name1 not in PROVINCES or short_name2 not in PROVINCES:
        return []
    
    if short_name1 == short_name2:
        return [short_name1]
    
    # BFS 搜索，记录路径
    visited = {short_name1: None}
    queue = [short_name1]
    
    while queue:
        current = queue.pop(0)
        
        prov = PROVINCES[current]
        for neighbor in prov.neighbors:
            if neighbor == short_name2:
                # 构建路径
                path = [short_name2]
                node = current
                while node:
                    path.append(node)
                    node = visited[node]
                return list(reversed(path))
            
            if neighbor not in visited and neighbor in PROVINCES:
                visited[neighbor] = current
                queue.append(neighbor)
    
    return []


def validate_province_name(name: str) -> bool:
    """
    验证省份名称是否有效
    
    Args:
        name: 省份名称或简称
    
    Returns:
        是否有效
    """
    _build_indexes()
    return name in PROVINCES or name in _name_index


def get_province_name_variants(short_name: str) -> Dict[str, str]:
    """
    获取省份名称的各种变体
    
    Args:
        short_name: 省份简称
    
    Returns:
        名称变体字典
    """
    prov = PROVINCES.get(short_name)
    if not prov:
        return {}
    
    result = {
        "short_name": prov.short_name,
        "full_name": prov.name,
        "capital": prov.capital,
        "code": prov.code,
    }
    
    # 添加简称别名（去掉"市"、"省"等后缀）
    if prov.name.endswith("市"):
        result["name_without_suffix"] = prov.name[:-1]
    elif prov.name.endswith("省"):
        result["name_without_suffix"] = prov.name[:-1]
    elif prov.name.endswith("自治区"):
        result["name_without_suffix"] = prov.name[:-3]
    
    if prov.iso_code:
        result["iso_code"] = prov.iso_code
    
    return result


def get_national_statistics() -> Dict[str, any]:
    """
    获取全国统计数据
    
    Returns:
        全国统计信息
    """
    provinces = get_provinces_by_type(RegionType.PROVINCE)
    municipalities = get_municipalities()
    autonomous = get_autonomous_regions()
    sars = get_special_administrative_regions()
    
    total_area = sum(p.area_km2 for p in PROVINCES.values())
    total_population = sum(p.population for p in PROVINCES.values() if p.population)
    
    return {
        "total_count": len(PROVINCES),
        "province_count": len(provinces),
        "municipality_count": len(municipalities),
        "autonomous_region_count": len(autonomous),
        "sar_count": len(sars),
        "total_area_km2": total_area,
        "total_population_万": total_population,
        "average_province_area_km2": total_area // len(PROVINCES),
        "average_province_population_万": total_population // len(PROVINCES),
    }


def list_province_short_names() -> List[str]:
    """
    获取所有省份简称列表
    
    Returns:
        省份简称列表
    """
    return list(PROVINCES.keys())


def list_province_names() -> List[str]:
    """
    获取所有省份全称列表
    
    Returns:
        省份全称列表
    """
    return [p.name for p in PROVINCES.values()]


def export_to_dict() -> Dict[str, Dict]:
    """
    导出省份数据为字典
    
    Returns:
        省份数据字典
    """
    result = {}
    for short, prov in PROVINCES.items():
        result[short] = {
            "name": prov.name,
            "short_name": prov.short_name,
            "code": prov.code,
            "capital": prov.capital,
            "region_type": prov.region_type.value,
            "area_km2": prov.area_km2,
            "population": prov.population,
            "cities": prov.cities,
            "area_codes": prov.area_codes,
            "neighbors": prov.neighbors,
            "iso_code": prov.iso_code,
        }
    return result