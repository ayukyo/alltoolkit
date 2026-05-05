"""
护照号码验证和MRZ解析工具
支持多国护照号码格式验证、MRZ(Machine Readable Zone)解析和校验位计算

支持的国家/地区:
- 中国 (P/E/G/D/S护照)
- 美国 (US护照)
- 英国 (UK护照)
- 德国 (D/E/K/KID护照)
- 法国 (F护照)
- 日本 (日本护照)
- 韩国 (韩国护照)
- 俄罗斯 (俄罗斯护照)
- 加拿大 (加拿大护照)
- 澳大利亚 (澳大利亚护照)
- 新西兰 (新西兰护照)
- 新加坡 (新加坡护照)
- 马来西亚 (马来西亚护照)
- 泰国 (泰国护照)
- 印度 (印度护照)
- 巴西 (巴西护照)
- 墨西哥 (墨西哥护照)

功能:
- 护照号码格式验证 (正则匹配)
- MRZ (TD1/TD3) 解析
- 校验位计算 (模10算法)
- 护照类型识别
- 国家代码查询
- 有效期检查
- 零外部依赖，纯 Python 标准库实现
"""

import re
from dataclasses import dataclass
from datetime import datetime, date
from enum import Enum
from typing import Optional, Dict, List, Tuple


class PassportType(Enum):
    """护照类型枚举"""
    ORDINARY = "普通护照"          # P
    DIPLOMATIC = "外交护照"        # D
    OFFICIAL = "公务护照"          # S, E
    EMERGENCY = "紧急护照"         # E
    COLLECTIVE = "集体护照"        # C
    ALIENS_PASSPORT = "外国人护照"  # A
    REFUGEE = "难民旅行证件"       # R
    UNKNOWN = "未知"


class Country(Enum):
    """国家/地区枚举"""
    CHINA = "中国"
    USA = "美国"
    UK = "英国"
    GERMANY = "德国"
    FRANCE = "法国"
    JAPAN = "日本"
    KOREA = "韩国"
    RUSSIA = "俄罗斯"
    CANADA = "加拿大"
    AUSTRALIA = "澳大利亚"
    NEW_ZEALAND = "新西兰"
    SINGAPORE = "新加坡"
    MALAYSIA = "马来西亚"
    THAILAND = "泰国"
    INDIA = "印度"
    BRAZIL = "巴西"
    MEXICO = "墨西哥"
    UNKNOWN = "未知"


@dataclass
class PassportValidationResult:
    """护照验证结果"""
    is_valid: bool
    passport_number: str
    country: Country
    passport_type: PassportType
    normalized: str
    message: str
    format_pattern: str
    has_check_digit: bool


@dataclass
class MRZParseResult:
    """MRZ解析结果"""
    is_valid: bool
    document_type: str
    country_code: str
    document_number: str
    check_digit_doc: str
    check_digit_doc_valid: bool
    optional_data: str
    birth_date: str
    check_digit_birth: str
    check_digit_birth_valid: bool
    sex: str
    expiry_date: str
    check_digit_expiry: str
    check_digit_expiry_valid: bool
    nationality: str
    optional_data_2: str
    check_digit_composite: str
    check_digit_composite_valid: bool
    full_name: str
    given_names: List[str]
    surname: str
    message: str


class PassportUtils:
    """护照工具类"""
    
    # 国家代码映射 (ISO 3166-1 alpha-3)
    COUNTRY_CODES = {
        "CHN": Country.CHINA,
        "USA": Country.USA,
        "GBR": Country.USA,
        "DEU": Country.GERMANY,
        "FRA": Country.FRANCE,
        "JPN": Country.JAPAN,
        "KOR": Country.KOREA,
        "RUS": Country.RUSSIA,
        "CAN": Country.CANADA,
        "AUS": Country.AUSTRALIA,
        "NZL": Country.NEW_ZEALAND,
        "SGP": Country.SINGAPORE,
        "MYS": Country.MALAYSIA,
        "THA": Country.THAILAND,
        "IND": Country.INDIA,
        "BRA": Country.BRAZIL,
        "MEX": Country.MEXICO,
        # 常见的变体和别名
        "D<<": Country.GERMANY,
        "USA<<": Country.USA,
        "GBR<<": Country.UK,
        "CHN<<": Country.CHINA,
    }
    
    # 护照号码格式规则 (国家, 护照类型, 正则表达式, 是否有校验位, 描述)
    PASSPORT_PATTERNS = [
        # 中国护照
        (Country.CHINA, PassportType.ORDINARY, r"^P\d{7}$", False, "中国普通护照 (P+7位数字)"),
        (Country.CHINA, PassportType.OFFICIAL, r"^S\d{7}$", False, "中国公务护照 (S+7位数字)"),
        (Country.CHINA, PassportType.DIPLOMATIC, r"^D\d{7}$", False, "中国外交护照 (D+7位数字)"),
        (Country.CHINA, PassportType.OFFICIAL, r"^E\d{8}$", False, "中国公务普通护照 (E+8位数字)"),
        (Country.CHINA, PassportType.ORDINARY, r"^G\d{8}$", False, "中国旧版普通护照 (G+8位数字)"),
        
        # 美国护照
        (Country.USA, PassportType.ORDINARY, r"^\d{9}$", False, "美国护照 (9位数字)"),
        (Country.USA, PassportType.ORDINARY, r"^[A-Z]\d{8}$", False, "美国护照 (1字母+8位数字)"),
        
        # 英国护照
        (Country.UK, PassportType.ORDINARY, r"^\d{9}$", False, "英国护照 (9位数字)"),
        (Country.UK, PassportType.ORDINARY, r"^[A-Z]{1,2}\d{6,8}GBR?\d{2,3}$", False, "英国护照 (字母+数字)"),
        
        # 德国护照
        (Country.GERMANY, PassportType.ORDINARY, r"^[CDFGHIJK]\d{8,9}$", False, "德国护照 (1字母+8-9位数字)"),
        (Country.GERMANY, PassportType.ORDINARY, r"^[CDFGHIJK]\d{2}[A-Z]{2}\d{5}$", False, "德国护照 (字母+数字+字母)"),
        (Country.GERMANY, PassportType.DIPLOMATIC, r"^D[A-Z]{2}\d{7,8}$", False, "德国外交护照"),
        (Country.GERMANY, PassportType.OFFICIAL, r"^K[A-Z]\d{7,8}$", False, "德国公务护照"),
        
        # 法国护照
        (Country.FRANCE, PassportType.ORDINARY, r"^\d{2}[A-Z]{2}\d{5}$", False, "法国护照 (2数字+2字母+5数字)"),
        (Country.FRANCE, PassportType.ORDINARY, r"^\d{9}[A-Z]{2}\d{2}$", False, "法国护照 (9数字+2字母+2数字)"),
        
        # 日本护照
        (Country.JAPAN, PassportType.ORDINARY, r"^[A-Z]{2}\d{7}$", False, "日本护照 (2字母+7数字)"),
        (Country.JAPAN, PassportType.ORDINARY, r"^T[AB]\d{7}$", False, "日本护照 (TA/TB+7数字)"),
        
        # 韩国护照
        (Country.KOREA, PassportType.ORDINARY, r"^[A-Z]{2}\d{8}$", False, "韩国护照 (2字母+8数字)"),
        (Country.KOREA, PassportType.ORDINARY, r"^M\d{8}$", False, "韩国护照 (M+8数字)"),
        
        # 俄罗斯护照
        (Country.RUSSIA, PassportType.ORDINARY, r"^\d{2}\s?\d{2}\s?\d{6}$", False, "俄罗斯内部护照 (系列+号码)"),
        (Country.RUSSIA, PassportType.ORDINARY, r"^\d{9}$", False, "俄罗斯国际护照 (9数字)"),
        
        # 加拿大护照
        (Country.CANADA, PassportType.ORDINARY, r"^[A-Z]{2}\d{6}$", False, "加拿大护照 (2字母+6数字)"),
        (Country.CANADA, PassportType.ORDINARY, r"^[A-Z]{2}\d{8}$", False, "加拿大护照 (2字母+8数字)"),
        
        # 澳大利亚护照
        (Country.AUSTRALIA, PassportType.ORDINARY, r"^[A-Z]\d{7}$", False, "澳大利亚护照 (1字母+7数字)"),
        (Country.AUSTRALIA, PassportType.ORDINARY, r"^[A-Z]{2}\d{7}$", False, "澳大利亚护照 (2字母+7数字)"),
        
        # 新西兰护照
        (Country.NEW_ZEALAND, PassportType.ORDINARY, r"^[A-Z]{2}\d{6}$", False, "新西兰护照 (2字母+6数字)"),
        (Country.NEW_ZEALAND, PassportType.ORDINARY, r"^[A-Z]{2}\d{7}$", False, "新西兰护照 (2字母+7数字)"),
        
        # 新加坡护照
        (Country.SINGAPORE, PassportType.ORDINARY, r"^E\d{7}[A-Z]$", True, "新加坡护照 (E+7数字+1字母校验位)"),
        (Country.SINGAPORE, PassportType.ORDINARY, r"^S\d{7}[A-Z]$", True, "新加坡护照 (S+7数字+1字母校验位)"),
        
        # 马来西亚护照
        (Country.MALAYSIA, PassportType.ORDINARY, r"^A\d{8}$", False, "马来西亚护照 (A+8数字)"),
        (Country.MALAYSIA, PassportType.ORDINARY, r"^[AHK]\d{8}$", False, "马来西亚护照 (A/H/K+8数字)"),
        
        # 泰国护照
        (Country.THAILAND, PassportType.ORDINARY, r"^[A-Z]\d{8}$", False, "泰国护照 (1字母+8数字)"),
        (Country.THAILAND, PassportType.ORDINARY, r"^[A-Z]{2}\d{7}$", False, "泰国护照 (2字母+7数字)"),
        
        # 印度护照
        (Country.INDIA, PassportType.ORDINARY, r"^[A-Z]\d{7}$", False, "印度护照 (1字母+7数字)"),
        (Country.INDIA, PassportType.ORDINARY, r"^[A-Z]{1,2}\d{6,7}$", False, "印度护照 (1-2字母+6-7数字)"),
        
        # 巴西护照
        (Country.BRAZIL, PassportType.ORDINARY, r"^[A-Z]{2}\d{6}$", False, "巴西护照 (2字母+6数字)"),
        (Country.BRAZIL, PassportType.ORDINARY, r"^[A-Z]{2}\d{7}$", False, "巴西护照 (2字母+7数字)"),
        
        # 墨西哥护照
        (Country.MEXICO, PassportType.ORDINARY, r"^\d{9,10}$", False, "墨西哥护照 (9-10数字)"),
    ]
    
    @classmethod
    def validate_passport_number(
        cls, 
        passport_number: str, 
        country: Optional[Country] = None
    ) -> PassportValidationResult:
        """
        验证护照号码
        
        Args:
            passport_number: 护照号码
            country: 指定国家(可选,如果指定则只验证该国家格式)
        
        Returns:
            PassportValidationResult: 验证结果
        """
        # 清理和标准化
        cleaned = cls._clean_passport_number(passport_number)
        
        if not cleaned:
            return PassportValidationResult(
                is_valid=False,
                passport_number=passport_number,
                country=Country.UNKNOWN,
                passport_type=PassportType.UNKNOWN,
                normalized="",
                message="护照号码为空",
                format_pattern="",
                has_check_digit=False
            )
        
        # 根据指定国家或自动检测进行验证
        if country:
            result = cls._validate_for_country(cleaned, country)
        else:
            result = cls._auto_detect_and_validate(cleaned)
        
        return result
    
    @classmethod
    def _clean_passport_number(cls, passport_number: str) -> str:
        """清理护照号码"""
        if not passport_number:
            return ""
        # 移除空格和常见分隔符
        cleaned = re.sub(r'[\s\-<>]', '', passport_number.upper())
        return cleaned
    
    @classmethod
    def _validate_for_country(
        cls, 
        passport_number: str, 
        country: Country
    ) -> PassportValidationResult:
        """验证指定国家的护照号码"""
        for pattern_country, passport_type, pattern, has_check, desc in cls.PASSPORT_PATTERNS:
            if pattern_country == country:
                if re.match(pattern, passport_number):
                    return PassportValidationResult(
                        is_valid=True,
                        passport_number=passport_number,
                        country=country,
                        passport_type=passport_type,
                        normalized=passport_number,
                        message=f"有效的{desc}",
                        format_pattern=pattern,
                        has_check_digit=has_check
                    )
        
        return PassportValidationResult(
            is_valid=False,
            passport_number=passport_number,
            country=country,
            passport_type=PassportType.UNKNOWN,
            normalized=passport_number,
            message=f"不符合{country.value}护照号码格式",
            format_pattern="",
            has_check_digit=False
        )
    
    @classmethod
    def _auto_detect_and_validate(cls, passport_number: str) -> PassportValidationResult:
        """自动检测国家并验证"""
        for country, passport_type, pattern, has_check, desc in cls.PASSPORT_PATTERNS:
            if re.match(pattern, passport_number):
                return PassportValidationResult(
                    is_valid=True,
                    passport_number=passport_number,
                    country=country,
                    passport_type=passport_type,
                    normalized=passport_number,
                    message=f"有效的{desc}",
                    format_pattern=pattern,
                    has_check_digit=has_check
                )
        
        return PassportValidationResult(
            is_valid=False,
            passport_number=passport_number,
            country=Country.UNKNOWN,
            passport_type=PassportType.UNKNOWN,
            normalized=passport_number,
            message="未识别的护照号码格式",
            format_pattern="",
            has_check_digit=False
        )
    
    @classmethod
    def parse_mrz(cls, mrz_string: str) -> MRZParseResult:
        """
        解析MRZ (Machine Readable Zone)
        
        Args:
            mrz_string: MRZ字符串 (TD1格式44字符或TD3格式88字符)
        
        Returns:
            MRZParseResult: 解析结果
        """
        # 移除换行符和空格
        cleaned = re.sub(r'[\s\n]', '', mrz_string.upper())
        
        # 检测MRZ格式
        if len(cleaned) == 30:
            # TD1格式 (30字符，通常用于身份证)
            return cls._parse_mrz_td1(cleaned)
        elif len(cleaned) == 44:
            # TD1格式 (44字符，某些身份证)
            return cls._parse_mrz_td1_44(cleaned)
        elif len(cleaned) == 88:
            # TD3格式 (88字符，护照)
            return cls._parse_mrz_td3(cleaned)
        else:
            return MRZParseResult(
                is_valid=False,
                document_type="",
                country_code="",
                document_number="",
                check_digit_doc="",
                check_digit_doc_valid=False,
                optional_data="",
                birth_date="",
                check_digit_birth="",
                check_digit_birth_valid=False,
                sex="",
                expiry_date="",
                check_digit_expiry="",
                check_digit_expiry_valid=False,
                nationality="",
                optional_data_2="",
                check_digit_composite="",
                check_digit_composite_valid=False,
                full_name="",
                given_names=[],
                surname="",
                message=f"无效的MRZ长度: {len(cleaned)}字符 (需要30/44/88字符)"
            )
    
    @classmethod
    def _parse_mrz_td1(cls, mrz: str) -> MRZParseResult:
        """解析TD1格式MRZ (30字符)"""
        try:
            # TD1格式 (30字符):
            # 第1行: 文件类型(1) + 国家代码(3) + 文件号码(9) + 校验位(1) + 可选数据(15) + 校验位(1)
            # 第2行: 生日(6) + 校验位(1) + 性别(1) + 有效期(6) + 校验位(1) + 国籍(3) + 可选数据(11)
            
            doc_type = mrz[0]
            country_code = mrz[1:4]
            doc_number = mrz[4:13]
            check_doc = mrz[13]
            optional_data = mrz[14:29]
            check_composite = mrz[29]
            
            return MRZParseResult(
                is_valid=True,
                document_type=doc_type,
                country_code=country_code,
                document_number=doc_number,
                check_digit_doc=check_doc,
                check_digit_doc_valid=cls._verify_check_digit(doc_number, check_doc),
                optional_data=optional_data,
                birth_date="",
                check_digit_birth="",
                check_digit_birth_valid=False,
                sex="",
                expiry_date="",
                check_digit_expiry="",
                check_digit_expiry_valid=False,
                nationality="",
                optional_data_2="",
                check_digit_composite=check_composite,
                check_digit_composite_valid=False,
                full_name="",
                given_names=[],
                surname="",
                message="TD1格式解析成功 (基本解析)"
            )
        except Exception as e:
            return MRZParseResult(
                is_valid=False,
                document_type="",
                country_code="",
                document_number="",
                check_digit_doc="",
                check_digit_doc_valid=False,
                optional_data="",
                birth_date="",
                check_digit_birth="",
                check_digit_birth_valid=False,
                sex="",
                expiry_date="",
                check_digit_expiry="",
                check_digit_expiry_valid=False,
                nationality="",
                optional_data_2="",
                check_digit_composite="",
                check_digit_composite_valid=False,
                full_name="",
                given_names=[],
                surname="",
                message=f"TD1解析错误: {str(e)}"
            )
    
    @classmethod
    def _parse_mrz_td1_44(cls, mrz: str) -> MRZParseResult:
        """解析TD1格式MRZ (44字符)"""
        try:
            # TD1格式 (44字符):
            # 第1行: 文件类型(2) + 国家代码(3) + 文件号码(9) + 校验位(1) + 可选数据(15) + 校验位(1)
            # 第2行: 生日(6) + 校验位(1) + 性别(1) + 有效期(6) + 校验位(1) + 国籍(3) + 可选数据(11)
            
            doc_type = mrz[0:2]
            country_code = mrz[2:5]
            doc_number = mrz[5:14]
            check_doc = mrz[14]
            optional_data_1 = mrz[15:30]
            
            birth_date = mrz[30:36]
            check_birth = mrz[36]
            sex = mrz[37]
            expiry_date = mrz[38:44]
            
            return MRZParseResult(
                is_valid=True,
                document_type=doc_type,
                country_code=country_code,
                document_number=doc_number,
                check_digit_doc=check_doc,
                check_digit_doc_valid=cls._verify_check_digit(doc_number, check_doc),
                optional_data=optional_data_1,
                birth_date=birth_date,
                check_digit_birth=check_birth,
                check_digit_birth_valid=cls._verify_check_digit(birth_date, check_birth),
                sex=sex,
                expiry_date=expiry_date,
                check_digit_expiry="",
                check_digit_expiry_valid=False,
                nationality="",
                optional_data_2="",
                check_digit_composite="",
                check_digit_composite_valid=False,
                full_name="",
                given_names=[],
                surname="",
                message="TD1格式(44字符)解析成功"
            )
        except Exception as e:
            return MRZParseResult(
                is_valid=False,
                document_type="",
                country_code="",
                document_number="",
                check_digit_doc="",
                check_digit_doc_valid=False,
                optional_data="",
                birth_date="",
                check_digit_birth="",
                check_digit_birth_valid=False,
                sex="",
                expiry_date="",
                check_digit_expiry="",
                check_digit_expiry_valid=False,
                nationality="",
                optional_data_2="",
                check_digit_composite="",
                check_digit_composite_valid=False,
                full_name="",
                given_names=[],
                surname="",
                message=f"TD1(44)解析错误: {str(e)}"
            )
    
    @classmethod
    def _parse_mrz_td3(cls, mrz: str) -> MRZParseResult:
        """解析TD3格式MRZ (88字符，标准护照格式)"""
        try:
            # TD3格式 (88字符):
            # 第1行 (44字符): 文件类型(1) + 国家代码(3) + 姓名(39) + 文件号码(9) + 校验位(1) + 国籍(3) + 生日(6) + 校验位(1) + 性别(1) + 有效期(6) + 校验位(1) + 个人号码(14) + 校验位(1)
            # 第2行 (44字符): 文件号码(9) + 校验位(1) + 可选数据(15) + 校验位(1) + 其他数据(18)
            
            # 实际TD3格式通常是:
            # 第1行 (44字符): P<国家代码(3)<<姓名(最多39字符)
            # 第2行 (44字符): 文件号码(9) + 校验位(1) + 国籍(3) + 生日(6) + 校验位(1) + 性别(1) + 有效期(6) + 校验位(1) + 个人号码(14) + 校验位(1)
            
            # 解析姓名行 (第1行)
            # TD3格式: P<COUNTRY_CODE<<SURNAME<<GIVEN_NAMES<<<<FILLER
            # 位置:    0  1-4           5-6  7+...
            line1 = mrz[0:44]
            doc_type = line1[0]
            # Country code在位置2-5 (跳过第一个<)
            country_code = line1[1:4]
            # 检查country_code是否包含<，如果有则需要调整解析
            if '<' in country_code:
                # 实际格式可能是 P<CHN<<NAME...
                # 要从位置2开始提取country_code
                country_code = line1[2:5]
                name_field = line1[6:44]
            else:
                # 标准格式
                name_field = line1[5:44]
            
            # 解析姓名 (格式: 姓<<名<名...)
            name_parts = name_field.split('<<')
            surname = name_parts[0].replace('<', ' ').strip() if name_parts else ""
            given_names = []
            if len(name_parts) > 1:
                given_names = name_parts[1].replace('<', ' ').split()
            
            # 解析数据行 (第2行)
            line2 = mrz[44:88]
            doc_number = line2[0:9]
            check_doc = line2[9]
            nationality = line2[10:13]
            birth_date = line2[13:19]
            check_birth = line2[19]
            sex = line2[20]
            expiry_date = line2[21:27]
            check_expiry = line2[27]
            optional_data_2 = line2[28:42]
            check_composite = line2[42]
            
            # 格式化姓名
            full_name = surname
            if given_names:
                full_name += " " + " ".join(given_names)
            
            # 验证校验位
            check_doc_valid = cls._verify_check_digit(doc_number, check_doc)
            check_birth_valid = cls._verify_check_digit(birth_date, check_birth)
            check_expiry_valid = cls._verify_check_digit(expiry_date, check_expiry)
            
            # 验证复合校验位
            composite_data = doc_number + check_doc + birth_date + check_birth + expiry_date + check_expiry + optional_data_2
            check_composite_valid = cls._verify_check_digit(composite_data, check_composite)
            
            return MRZParseResult(
                is_valid=True,
                document_type=doc_type,
                country_code=country_code,
                document_number=doc_number,
                check_digit_doc=check_doc,
                check_digit_doc_valid=check_doc_valid,
                optional_data="",
                birth_date=cls._format_date(birth_date),
                check_digit_birth=check_birth,
                check_digit_birth_valid=check_birth_valid,
                sex=sex,
                expiry_date=cls._format_date(expiry_date),
                check_digit_expiry=check_expiry,
                check_digit_expiry_valid=check_expiry_valid,
                nationality=nationality,
                optional_data_2=optional_data_2,
                check_digit_composite=check_composite,
                check_digit_composite_valid=check_composite_valid,
                full_name=full_name,
                given_names=given_names,
                surname=surname,
                message="TD3格式解析成功"
            )
        except Exception as e:
            return MRZParseResult(
                is_valid=False,
                document_type="",
                country_code="",
                document_number="",
                check_digit_doc="",
                check_digit_doc_valid=False,
                optional_data="",
                birth_date="",
                check_digit_birth="",
                check_digit_birth_valid=False,
                sex="",
                expiry_date="",
                check_digit_expiry="",
                check_digit_expiry_valid=False,
                nationality="",
                optional_data_2="",
                check_digit_composite="",
                check_digit_composite_valid=False,
                full_name="",
                given_names=[],
                surname="",
                message=f"TD3解析错误: {str(e)}"
            )
    
    @classmethod
    def _verify_check_digit(cls, data: str, check_digit: str) -> bool:
        """
        验证MRZ校验位 (模10算法)
        
        Args:
            data: 数据部分
            check_digit: 校验位
        
        Returns:
            bool: 校验位是否有效
        """
        if not data or not check_digit:
            return False
        
        try:
            calculated = cls._calculate_check_digit(data)
            return calculated == check_digit.upper()
        except:
            return False
    
    @classmethod
    def _calculate_check_digit(cls, data: str) -> str:
        """
        计算MRZ校验位 (模10算法)
        
        权重循环: 7, 3, 1, 7, 3, 1, ...
        
        Args:
            data: 数据部分 (可包含数字和字母)
        
        Returns:
            str: 校验位字符
        """
        # 字符值映射
        char_values = {}
        # 数字 0-9 映射到 0-9
        for i in range(10):
            char_values[str(i)] = i
        # 字母 A-Z 映射到 10-35
        for i, c in enumerate('ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
            char_values[c] = 10 + i
        # 填充符 < 映射到 0
        char_values['<'] = 0
        
        # 权重循环
        weights = [7, 3, 1]
        
        total = 0
        for i, char in enumerate(data.upper()):
            if char not in char_values:
                return '0'
            value = char_values[char]
            weight = weights[i % 3]
            total += value * weight
        
        check_digit = total % 10
        return str(check_digit)
    
    @classmethod
    def _format_date(cls, date_str: str) -> str:
        """
        格式化MRZ日期 (YYMMDD -> YYYY-MM-DD)
        
        Args:
            date_str: YYMMDD格式日期
        
        Returns:
            str: YYYY-MM-DD格式日期
        """
        if len(date_str) != 6:
            return date_str
        
        year = date_str[0:2]
        month = date_str[2:4]
        day = date_str[4:6]
        
        # MRZ年份处理: 00-99映射到1900-1999或2000-2099
        # 通常护照有效期不超过10年，所以可以假设年份
        year_int = int(year)
        if year_int >= 0 and year_int <= 99:
            # 简单处理: 假设当前年份附近
            current_year = datetime.now().year
            current_century = current_year // 100
            
            # 如果日期在未来，使用当前世纪
            # 如果日期在过去，使用上一世纪
            test_year_current = current_century * 100 + year_int
            test_year_prev = (current_century - 1) * 100 + year_int
            
            # 对于生日，通常在过去
            # 对于有效期，通常在未来10年内
            # 这里简化处理，使用当前世纪
            year = f"{test_year_current:04d}"
        
        return f"{year}-{month}-{day}"
    
    @classmethod
    def is_expired(cls, expiry_date: str) -> bool:
        """
        检查护照是否过期
        
        Args:
            expiry_date: 有效期 (YYYY-MM-DD 或 YYMMDD 格式)
        
        Returns:
            bool: 是否过期
        """
        try:
            if '-' in expiry_date:
                exp_date = datetime.strptime(expiry_date, "%Y-%m-%d").date()
            elif len(expiry_date) == 6:
                # YYMMDD格式
                formatted = cls._format_date(expiry_date)
                exp_date = datetime.strptime(formatted, "%Y-%m-%d").date()
            else:
                return False
            
            return exp_date < date.today()
        except:
            return False
    
    @classmethod
    def days_until_expiry(cls, expiry_date: str) -> Optional[int]:
        """
        计算距离过期的天数
        
        Args:
            expiry_date: 有效期 (YYYY-MM-DD 或 YYMMDD 格式)
        
        Returns:
            Optional[int]: 天数 (已过期返回负数，错误返回None)
        """
        try:
            if '-' in expiry_date:
                exp_date = datetime.strptime(expiry_date, "%Y-%m-%d").date()
            elif len(expiry_date) == 6:
                formatted = cls._format_date(expiry_date)
                exp_date = datetime.strptime(formatted, "%Y-%m-%d").date()
            else:
                return None
            
            delta = exp_date - date.today()
            return delta.days
        except:
            return None
    
    @classmethod
    def get_country_by_code(cls, code: str) -> Country:
        """
        根据国家代码获取国家
        
        Args:
            code: ISO 3166-1 alpha-3 国家代码
        
        Returns:
            Country: 国家枚举
        """
        return cls.COUNTRY_CODES.get(code.upper(), Country.UNKNOWN)
    
    @classmethod
    def list_passport_formats(cls, country: Optional[Country] = None) -> List[Dict]:
        """
        列出护照格式
        
        Args:
            country: 指定国家(可选)
        
        Returns:
            List[Dict]: 护照格式列表
        """
        formats = []
        for c, ptype, pattern, has_check, desc in cls.PASSPORT_PATTERNS:
            if country is None or c == country:
                formats.append({
                    "country": c.value,
                    "passport_type": ptype.value,
                    "pattern": pattern,
                    "has_check_digit": has_check,
                    "description": desc
                })
        return formats


# 便捷函数
def validate_passport(passport_number: str, country: Optional[Country] = None) -> PassportValidationResult:
    """
    验证护照号码 (便捷函数)
    
    Args:
        passport_number: 护照号码
        country: 指定国家(可选)
    
    Returns:
        PassportValidationResult: 验证结果
    """
    return PassportUtils.validate_passport_number(passport_number, country)


def parse_mrz(mrz_string: str) -> MRZParseResult:
    """
    解析MRZ (便捷函数)
    
    Args:
        mrz_string: MRZ字符串
    
    Returns:
        MRZParseResult: 解析结果
    """
    return PassportUtils.parse_mrz(mrz_string)


def is_passport_expired(expiry_date: str) -> bool:
    """
    检查护照是否过期 (便捷函数)
    
    Args:
        expiry_date: 有效期
    
    Returns:
        bool: 是否过期
    """
    return PassportUtils.is_expired(expiry_date)


def get_passport_formats(country: Optional[Country] = None) -> List[Dict]:
    """
    获取护照格式列表 (便捷函数)
    
    Args:
        country: 指定国家(可选)
    
    Returns:
        List[Dict]: 格式列表
    """
    return PassportUtils.list_passport_formats(country)


if __name__ == "__main__":
    # 演示用法
    print("=" * 60)
    print("护照号码验证和MRZ解析工具演示")
    print("=" * 60)
    
    # 验证中国护照
    result = validate_passport("P1234567", Country.CHINA)
    print(f"\n中国护照 P1234567:")
    print(f"  有效: {result.is_valid}")
    print(f"  国家: {result.country.value}")
    print(f"  类型: {result.passport_type.value}")
    print(f"  消息: {result.message}")
    
    # 验证新加坡护照 (有校验位)
    result = validate_passport("E1234567A", Country.SINGAPORE)
    print(f"\n新加坡护照 E1234567A:")
    print(f"  有效: {result.is_valid}")
    print(f"  国家: {result.country.value}")
    print(f"  有校验位: {result.has_check_digit}")
    print(f"  消息: {result.message}")
    
    # 验证美国护照
    result = validate_passport("123456789", Country.USA)
    print(f"\n美国护照 123456789:")
    print(f"  有效: {result.is_valid}")
    print(f"  国家: {result.country.value}")
    print(f"  消息: {result.message}")
    
    # 自动检测
    result = validate_passport("TA1234567")
    print(f"\n自动检测 TA1234567:")
    print(f"  有效: {result.is_valid}")
    print(f"  国家: {result.country.value}")
    print(f"  消息: {result.message}")
    
    # 解析MRZ (TD3格式示例)
    mrz_example = "P<CHN张三<<SAN<<<<<<<<<<<<<<<<<<<<<<<\nE12345678CHN9001011M2512310<<<<<<<<<<<<<<00"
    mrz_result = parse_mrz(mrz_example)
    print(f"\nMRZ解析结果:")
    print(f"  有效: {mrz_result.is_valid}")
    print(f"  姓名: {mrz_result.full_name}")
    print(f"  护照号: {mrz_result.document_number}")
    print(f"  生日: {mrz_result.birth_date}")
    print(f"  性别: {mrz_result.sex}")
    print(f"  有效期: {mrz_result.expiry_date}")
    print(f"  国籍: {mrz_result.nationality}")
    print(f"  校验位有效: {mrz_result.check_digit_doc_valid}")
    
    # 列出中国护照格式
    print(f"\n中国护照格式:")
    for fmt in get_passport_formats(Country.CHINA):
        print(f"  - {fmt['description']}")