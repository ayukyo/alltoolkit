"""
物流追踪号码验证和解析工具
支持多种承运商的追踪号码格式验证、承运商识别和校验位计算

支持的承运商:
- UPS (1Z开头)
- FedEx (Express/Ground/SmartPost)
- USPS (Priority Mail/Express/Signature)
- DHL (Express/ECommerce)
- 顺丰 (SF)
- 中国邮政 (EMS/平邮)
- 京东物流 (JD)
- 圆通速递 (YTO)
- 中通快递 (ZTO)
- 申通快递 (STO)
- 韵达快递 (YD)
- 极兔速递 (JT)

零外部依赖，纯 Python 标准库实现
"""

import re
from dataclasses import dataclass
from enum import Enum
from typing import Optional, List, Tuple


class Carrier(Enum):
    """承运商枚举"""
    UPS = "UPS"
    FEDEX = "FedEx"
    USPS = "USPS"
    DHL = "DHL"
    SF = "顺丰速运"
    CHINA_POST = "中国邮政"
    JD = "京东物流"
    YTO = "圆通速递"
    ZTO = "中通快递"
    STO = "申通快递"
    YD = "韵达快递"
    JT = "极兔速递"
    UNKNOWN = "未知"


@dataclass
class TrackingResult:
    """追踪号码验证结果"""
    is_valid: bool
    tracking_number: str
    carrier: Carrier
    normalized: str
    checksum_valid: bool
    tracking_url: Optional[str]
    message: str


class TrackingNumberUtils:
    """物流追踪号码工具类"""

    # 承运商官网追踪URL模板
    TRACKING_URLS = {
        Carrier.UPS: "https://www.ups.com/track?tracknum={}",
        Carrier.FEDEX: "https://www.fedex.com/fedextrack/?trknbr={}",
        Carrier.USPS: "https://tools.usps.com/go/TrackConfirmAction?tRef=fullpage&tLabels={}",
        Carrier.DHL: "https://www.dhl.com/cn-zh/home/tracking/tracking-parcel.html?submit=1&tracking-id={}",
        Carrier.SF: "https://www.sf-express.com/cn/sc/dynamic_function/waybill/#search/bill-number/{}",
        Carrier.CHINA_POST: "https://www.ems.com.cn/queryNumber?mailNumber={}",
        Carrier.JD: "https://www.jdl.com/fq/orderDetail?wlNo={}",
        Carrier.YTO: "https://www.yto.net.cn/gw/index/index.html#/waybill_detail/{}",
        Carrier.ZTO: "https://www.zto.com/express.html?bill={}",
        Carrier.STO: "https://www.sto.cn/track/{}.html",
        Carrier.YD: "https://www.yundaex.com/cn/ordersearch.php?orderno={}",
        Carrier.JT: "https://www.jtexpress.cn/search?billNo={}",
    }

    # 承运商识别规则 (正则表达式, 承运商, 长度限制)
    # 注意：顺序很重要！更具体的模式应该放在前面
    CARRIER_PATTERNS = [
        # UPS: 1Z开头，18字符
        (r"^1Z[A-Z0-9]{16}$", Carrier.UPS, 18),

        # 中国快递公司（字母开头，优先匹配）
        # 顺丰: SF开头
        (r"^SF\d{12,14}$", Carrier.SF, None),

        # 京东物流: JD开头或JDX开头 (必须在DHL之前匹配)
        (r"^JDX?\d{12,15}$", Carrier.JD, None),

        # 圆通速递: YT开头
        (r"^YT[OA]?\d{11,13}$", Carrier.YTO, None),

        # 中通快递: ZT开头 (纯数字7开头的单独处理)
        (r"^ZT\d{10,12}$", Carrier.ZTO, None),

        # 申通快递: ST开头
        (r"^ST\d{10,12}$", Carrier.STO, None),

        # 韵达快递: YD开头
        (r"^YD\d{10,12}$", Carrier.YD, None),

        # 极兔速递: JT开头
        (r"^JT\d{11,13}$", Carrier.JT, None),

        # 中国邮政EMS: 两位字母开头，CN结尾的13位
        (r"^[A-Z]{2}\d{9}CN$", Carrier.CHINA_POST, 13),

        # 中国邮政平邮: 以PA开头的14位
        (r"^PA\d{12}$", Carrier.CHINA_POST, 14),

        # DHL ECommerce: GM开头或JD开头
        (r"^GM\d{8}$", Carrier.DHL, 10),
        (r"^JD\d{12}$", Carrier.DHL, 14),

        # USPS Express Mail: 以E开头，以US结尾的13位
        (r"^E[A-Z]\d{9}US$", Carrier.USPS, 13),

        # 纯数字格式（需要按长度和前缀区分）
        # 中通快递: 以7开头的12位数字
        (r"^7\d{11}$", Carrier.ZTO, 12),

        # 申通快递: 以7开头的13位数字
        (r"^7\d{12}$", Carrier.STO, 13),

        # 韵达快递: 以1开头的13位数字
        (r"^1\d{12}$", Carrier.YD, 13),

        # FedEx Express: 12位纯数字 (不是7开头)
        (r"^\d{12}$", Carrier.FEDEX, 12),

        # FedEx Ground: 以2或6开头的15位数字
        (r"^[26]\d{14}$", Carrier.FEDEX, 15),

        # FedEx SmartPost: 92开头的15位或20-22位数字
        (r"^92\d{13}(\d{5,7})?$", Carrier.FEDEX, None),

        # USPS: 以9开头的22位数字
        (r"^9\d{21}$", Carrier.USPS, 22),

        # USPS Priority Mail: 42开头的20位
        (r"^42\d{18}$", Carrier.USPS, 20),

        # DHL Express: 10位数字
        (r"^\d{10}$", Carrier.DHL, 10),

        # DHL: 16位数字
        (r"^\d{16}$", Carrier.DHL, 16),

        # 顺丰纯数字: 15-16位数字
        (r"^\d{15,16}$", Carrier.SF, None),
    ]

    @staticmethod
    def normalize(tracking_number: str) -> str:
        """
        标准化追踪号码（移除空格、连字符等）

        Args:
            tracking_number: 原始追踪号码

        Returns:
            标准化后的追踪号码
        """
        return re.sub(r'[\s\-]', '', tracking_number.upper())

    @staticmethod
    def identify_carrier(tracking_number: str) -> Carrier:
        """
        识别承运商

        Args:
            tracking_number: 追踪号码

        Returns:
            识别出的承运商
        """
        normalized = TrackingNumberUtils.normalize(tracking_number)

        for pattern, carrier, length in TrackingNumberUtils.CARRIER_PATTERNS:
            if re.match(pattern, normalized):
                if length is None or len(normalized) == length:
                    return carrier

        # 特殊检查：顺丰纯数字需要额外验证
        if re.match(r'^\d{15,16}$', normalized):
            # 检查是否为顺丰号码格式
            if TrackingNumberUtils._check_sf_checksum(normalized):
                return Carrier.SF

        return Carrier.UNKNOWN

    @staticmethod
    def _check_ups_checksum(tracking_number: str) -> bool:
        """
        验证UPS追踪号码校验位
        1Z开头的18位追踪号码使用加权求和算法
        """
        if not tracking_number.startswith('1Z') or len(tracking_number) != 18:
            return False

        # UPS使用特殊的校验算法
        total = 0
        for i, char in enumerate(tracking_number[2:]):  # 跳过1Z前缀
            if char.isdigit():
                val = int(char)
            else:
                val = ord(char) - ord('A') + 10

            # 偶数位权重为2，奇数位为1
            if i % 2 == 0:
                val *= 2

            total += val

        check_digit = total % 10
        return check_digit == 0

    @staticmethod
    def _check_fedex_checksum(tracking_number: str) -> bool:
        """
        验证FedEx追踪号码校验位
        使用标准模10校验算法
        """
        length = len(tracking_number)
        if length not in [12, 15, 20, 21, 22]:
            return False

        total = 0
        for i, digit in enumerate(reversed(tracking_number[:-1])):
            weight = 3 if i % 3 == 0 else 1
            total += int(digit) * weight

        check_digit = (10 - (total % 10)) % 10
        return check_digit == int(tracking_number[-1])

    @staticmethod
    def _check_usps_checksum(tracking_number: str) -> bool:
        """
        验证USPS追踪号码校验位
        使用模11或模10算法，取决于号码格式
        """
        length = len(tracking_number)

        # EMS格式: 13位字母数字混合
        if re.match(r'^[A-Z]{2}\d{9}[A-Z]{2}$', tracking_number):
            total = 0
            weights = [8, 6, 4, 2, 3, 5, 9, 7]
            serial = tracking_number[2:10]

            for i, digit in enumerate(serial):
                total += int(digit) * weights[i]

            check = 11 - (total % 11)
            if check == 10:
                check = 0
            elif check == 11:
                check = 5

            return check == int(tracking_number[10])

        # 标准格式: 22位数字
        if length == 22 and tracking_number.isdigit():
            total = 0
            for i, digit in enumerate(tracking_number[:-1]):
                total += int(digit) * (3 if i % 2 == 0 else 1)

            check_digit = (10 - (total % 10)) % 10
            return check_digit == int(tracking_number[-1])

        return True  # 其他格式暂不验证

    @staticmethod
    def _check_sf_checksum(tracking_number: str) -> bool:
        """
        验证顺丰追踪号码校验位
        顺丰单号为15-16位数字，最后一位为校验位
        """
        if not tracking_number.isdigit():
            return False

        length = len(tracking_number)
        if length not in [15, 16]:
            return False

        # 简化的校验：各位数字求和模10
        total = sum(int(d) for d in tracking_number[:-1])
        check_digit = total % 10

        return check_digit == int(tracking_number[-1])

    @staticmethod
    def _check_china_post_checksum(tracking_number: str) -> bool:
        """
        验证中国邮政追踪号码校验位
        EMS使用国际标准S10格式
        """
        # EMS格式: 13位，前2位字母，后2位国家代码
        if re.match(r'^[A-Z]{2}\d{9}[A-Z]{2}$', tracking_number):
            # S10格式校验
            weights = [8, 6, 4, 2, 3, 5, 9, 7]
            serial = tracking_number[2:10]
            total = sum(int(serial[i]) * weights[i] for i in range(8))

            check = 11 - (total % 11)
            if check == 10:
                check = 0
            elif check == 11:
                check = 5

            return check == int(tracking_number[10])

        return True  # 其他格式暂不验证

    @staticmethod
    def _check_dhl_checksum(tracking_number: str) -> bool:
        """
        验证DHL追踪号码校验位
        DHL Express使用模7算法
        """
        if len(tracking_number) == 10 and tracking_number.isdigit():
            # DHL Express 10位数字
            total = sum(int(d) for d in tracking_number[:-1])
            return total % 7 == int(tracking_number[-1])

        return True  # 其他格式暂不验证

    @staticmethod
    def _check_china_courier_checksum(tracking_number: str) -> bool:
        """
        验证中国快递公司追踪号码校验位
        包括京东、圆通、中通、申通、韵达、极兔等
        """
        length = len(tracking_number)

        # 纯数字格式的中国快递使用简单的模校验
        if tracking_number.isdigit() and length in [12, 13, 14, 15]:
            # 大多数中国快递使用最后一位校验
            total = 0
            for i, digit in enumerate(tracking_number[:-1]):
                total += int(digit) * ((length - i) % 10 + 1)

            expected_check = total % 10
            return expected_check == int(tracking_number[-1])

        return True  # 字母开头的格式暂不验证

    @staticmethod
    def validate(tracking_number: str) -> TrackingResult:
        """
        验证追踪号码

        Args:
            tracking_number: 追踪号码

        Returns:
            TrackingResult对象包含验证结果
        """
        if not tracking_number:
            return TrackingResult(
                is_valid=False,
                tracking_number=tracking_number,
                carrier=Carrier.UNKNOWN,
                normalized="",
                checksum_valid=False,
                tracking_url=None,
                message="追踪号码为空"
            )

        normalized = TrackingNumberUtils.normalize(tracking_number)
        carrier = TrackingNumberUtils.identify_carrier(normalized)
        tracking_url = None

        if carrier == Carrier.UNKNOWN:
            return TrackingResult(
                is_valid=False,
                tracking_number=tracking_number,
                carrier=carrier,
                normalized=normalized,
                checksum_valid=False,
                tracking_url=None,
                message="无法识别的追踪号码格式"
            )

        # 根据承运商验证校验位
        checksum_valid = True
        message = "追踪号码有效"

        if carrier == Carrier.UPS:
            checksum_valid = TrackingNumberUtils._check_ups_checksum(normalized)
        elif carrier == Carrier.FEDEX:
            checksum_valid = TrackingNumberUtils._check_fedex_checksum(normalized)
        elif carrier == Carrier.USPS:
            checksum_valid = TrackingNumberUtils._check_usps_checksum(normalized)
        elif carrier == Carrier.DHL:
            checksum_valid = TrackingNumberUtils._check_dhl_checksum(normalized)
        elif carrier == Carrier.SF:
            checksum_valid = TrackingNumberUtils._check_sf_checksum(normalized)
        elif carrier == Carrier.CHINA_POST:
            checksum_valid = TrackingNumberUtils._check_china_post_checksum(normalized)
        elif carrier in [Carrier.JD, Carrier.YTO, Carrier.ZTO, Carrier.STO, Carrier.YD, Carrier.JT]:
            checksum_valid = TrackingNumberUtils._check_china_courier_checksum(normalized)

        if not checksum_valid:
            message = "校验位验证失败，号码可能输入错误"

        # 生成追踪URL
        if carrier in TrackingNumberUtils.TRACKING_URLS:
            tracking_url = TrackingNumberUtils.TRACKING_URLS[carrier].format(normalized)

        return TrackingResult(
            is_valid=True,
            tracking_number=tracking_number,
            carrier=carrier,
            normalized=normalized,
            checksum_valid=checksum_valid,
            tracking_url=tracking_url,
            message=message
        )

    @staticmethod
    def get_tracking_url(tracking_number: str) -> Optional[str]:
        """
        获取追踪URL

        Args:
            tracking_number: 追踪号码

        Returns:
            追踪URL，如果无法识别则返回None
        """
        result = TrackingNumberUtils.validate(tracking_number)
        return result.tracking_url

    @staticmethod
    def batch_validate(tracking_numbers: List[str]) -> List[TrackingResult]:
        """
        批量验证追踪号码

        Args:
            tracking_numbers: 追踪号码列表

        Returns:
            验证结果列表
        """
        return [TrackingNumberUtils.validate(tn) for tn in tracking_numbers]

    @staticmethod
    def extract_from_text(text: str) -> List[Tuple[str, Carrier]]:
        """
        从文本中提取追踪号码

        Args:
            text: 包含追踪号码的文本

        Returns:
            (追踪号码, 承运商)元组列表
        """
        results = []

        # 常见追踪号码正则模式
        patterns = [
            # UPS
            r'\b1Z[A-Z0-9]{6,16}\b',
            # FedEx
            r'\b\d{12}\b',
            r'\b[26]\d{14}\b',
            r'\b92\d{13,21}\b',
            # USPS
            r'\b9\d{21}\b',
            r'\b[A-Z]{2}\d{9}[A-Z]{2}\b',
            # DHL
            r'\bJD\d{12}\b',
            r'\b\d{16}\b',
            # 中国快递
            r'\bSF\d{12,14}\b',
            r'\bJDX?\d{12,15}\b',
            r'\bYT[OA]?\d{11,13}\b',
            r'\bZT\d{10,12}\b',
            r'\bST\d{10,12}\b',
            r'\bYD\d{10,12}\b',
            r'\bJT\d{11,13}\b',
            r'\bPA\d{12}\b',
        ]

        for pattern in patterns:
            matches = re.findall(pattern, text.upper())
            for match in matches:
                carrier = TrackingNumberUtils.identify_carrier(match)
                if carrier != Carrier.UNKNOWN:
                    results.append((match, carrier))

        # 去重
        seen = set()
        unique_results = []
        for tn, carrier in results:
            if tn not in seen:
                seen.add(tn)
                unique_results.append((tn, carrier))

        return unique_results


# 便捷函数
def validate(tracking_number: str) -> TrackingResult:
    """验证追踪号码"""
    return TrackingNumberUtils.validate(tracking_number)


def identify_carrier(tracking_number: str) -> Carrier:
    """识别承运商"""
    return TrackingNumberUtils.identify_carrier(tracking_number)


def get_tracking_url(tracking_number: str) -> Optional[str]:
    """获取追踪URL"""
    return TrackingNumberUtils.get_tracking_url(tracking_number)


def extract_from_text(text: str) -> List[Tuple[str, Carrier]]:
    """从文本中提取追踪号码"""
    return TrackingNumberUtils.extract_from_text(text)