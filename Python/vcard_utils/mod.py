#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Python VCard Utilities

功能完整的 VCard (电子名片) 处理工具模块，支持 VCard 文件的创建、解析、
验证、转换等功能。完全零外部依赖，使用 Python 标准库实现。

支持 VCard 版本：2.1, 3.0, 4.0

Author: AllToolkit
License: MIT
"""

import re
import os
import base64
from typing import Union, Optional, Any, Dict, List, Tuple, BinaryIO
from dataclasses import dataclass, field
from pathlib import Path
from datetime import datetime, date
from io import StringIO


# =============================================================================
# 版本信息
# =============================================================================

__version__ = "1.0.0"
__author__ = "AllToolkit"
__license__ = "MIT"


def get_version() -> str:
    """获取模块版本号。"""
    return __version__


# =============================================================================
# 异常类
# =============================================================================

class VCardUtilsError(Exception):
    """VCard 工具基础异常。"""
    pass


class VCardFileNotFoundError(VCardUtilsError):
    """VCard 文件未找到异常。"""
    pass


class VCardValidationError(VCardUtilsError):
    """VCard 验证失败异常。"""
    pass


class VCardFormatError(VCardUtilsError):
    """VCard 格式错误异常。"""
    pass


# =============================================================================
# 数据类
# =============================================================================

@dataclass
class VCardName:
    """VCard 姓名（N 属性）。"""
    family_name: str = ""  # 姓
    given_name: str = ""   # 名
    additional_names: List[str] = field(default_factory=list)  # 中间名/别名
    honorific_prefixes: List[str] = field(default_factory=list)  # 前缀（如 Dr., Mr.）
    honorific_suffixes: List[str] = field(default_factory=list)  # 后缀（如 Jr., PhD）
    
    def __str__(self) -> str:
        parts = [self.family_name, self.given_name]
        if self.additional_names:
            parts.extend(self.additional_names)
        return " ".join(filter(None, parts))
    
    def to_vcard_format(self) -> str:
        """转换为 VCard N 属性格式。"""
        additional = ",".join(self.additional_names)
        prefixes = ",".join(self.honorific_prefixes)
        suffixes = ",".join(self.honorific_suffixes)
        return f"{self.family_name};{self.given_name};{additional};{prefixes};{suffixes}"


@dataclass
class VCardAddress:
    """VCard 地址（ADR 属性）。"""
    street: str = ""           # 街道地址
    city: str = ""             # 城市
    region: str = ""           # 省/州
    postal_code: str = ""      # 邮政编码
    country: str = ""          # 国家
    po_box: str = ""           # 邮政信箱
    extended_address: str = "" # 扩展地址（公寓、楼层等）
    label: str = ""            # 地址标签
    type: str = ""             # 地址类型（home, work, etc.）
    
    def to_vcard_format(self) -> str:
        """转换为 VCard ADR 属性格式。"""
        return f"{self.po_box};{self.extended_address};{self.street};{self.city};{self.region};{self.postal_code};{self.country}"
    
    def __str__(self) -> str:
        parts = [self.street, self.city, self.region, self.postal_code, self.country]
        return ", ".join(filter(None, parts))


@dataclass
class VCardPhone:
    """VCard 电话号码（TEL 属性）。"""
    number: str = ""
    type: str = "voice"  # 类型：voice, cell, fax, pager, work, home, etc.
    pref: int = 0        # 偏好级别（1-10，1 最高）
    
    def to_vcard_format(self) -> str:
        """转换为 VCard TEL 属性格式。"""
        params = []
        if self.type:
            params.append(f"TYPE={self.type}")
        if self.pref > 0:
            params.append(f"PREF={self.pref}")
        param_str = ";".join(params) if params else ""
        return f"TEL;{param_str}:{self.number}" if param_str else f"TEL:{self.number}"


@dataclass
class VCardEmail:
    """VCard 电子邮件（EMAIL 属性）。"""
    address: str = ""
    type: str = ""  # 类型：work, home, internet
    pref: int = 0   # 偏好级别
    
    def to_vcard_format(self) -> str:
        """转换为 VCard EMAIL 属性格式。"""
        params = []
        if self.type:
            params.append(f"TYPE={self.type}")
        if self.pref > 0:
            params.append(f"PREF={self.pref}")
        param_str = ";".join(params) if params else ""
        return f"EMAIL;{param_str}:{self.address}" if param_str else f"EMAIL:{self.address}"


@dataclass
class VCardOrganization:
    """VCard 组织信息（ORG 属性）。"""
    name: str = ""
    unit: str = ""   # 部门/单位
    title: str = ""  # 职位
    role: str = ""   # 角色
    
    def to_vcard_format(self) -> str:
        """转换为 VCard ORG 属性格式。"""
        return f"{self.name};{self.unit}"


@dataclass
class VCardPhoto:
    """VCard 照片（PHOTO 属性）。"""
    data: bytes = field(default_factory=bytes)
    type: str = "image/jpeg"  # MIME 类型
    encoding: str = "BASE64"  # 编码方式
    
    def to_vcard_format(self, version: str = "3.0") -> str:
        """转换为 VCard PHOTO 属性格式。"""
        encoded = base64.b64encode(self.data).decode('ascii')
        if version == "4.0":
            return f"PHOTO:data:{self.type};base64,{encoded}"
        else:
            return f"PHOTO;TYPE={self.type};ENCODING={self.encoding}:{encoded}"


@dataclass
class VCardURL:
    """VCard 网址（URL 属性）。"""
    url: str = ""
    type: str = ""  # 类型：work, personal, blog, etc.
    
    def to_vcard_format(self) -> str:
        """转换为 VCard URL 属性格式。"""
        if self.type:
            return f"URL;TYPE={self.type}:{self.url}"
        return f"URL:{self.url}"


@dataclass
class VCardSocial:
    """VCard 社交媒体信息（X-SOCIAL 属性）。"""
    platform: str = ""  # 平台：twitter, linkedin, facebook, etc.
    handle: str = ""    # 用户名/ID
    
    def to_vcard_format(self) -> str:
        """转换为 VCard X-SOCIAL 属性格式。"""
        return f"X-{self.platform.upper()}:{self.handle}"


@dataclass
class VCard:
    """VCard 完整联系人对象。"""
    version: str = "3.0"
    name: Optional[VCardName] = None
    full_name: str = ""  # FN 属性（必需）
    phones: List[VCardPhone] = field(default_factory=list)
    emails: List[VCardEmail] = field(default_factory=list)
    addresses: List[VCardAddress] = field(default_factory=list)
    organization: Optional[VCardOrganization] = None
    title: str = ""
    role: str = ""
    photo: Optional[VCardPhoto] = None
    urls: List[VCardURL] = field(default_factory=list)
    socials: List[VCardSocial] = field(default_factory=list)
    birthday: Optional[date] = None
    nickname: str = ""
    note: str = ""
    categories: List[str] = field(default_factory=list)
    timezone: str = ""
    geo: Tuple[float, float] = (0.0, 0.0)  # (latitude, longitude)
    uid: str = ""
    revision: Optional[datetime] = None
    custom_fields: Dict[str, str] = field(default_factory=dict)


# =============================================================================
# VCard 创建功能
# =============================================================================

def create_vcard(
    full_name: str,
    family_name: str = "",
    given_name: str = "",
    organization: str = "",
    title: str = "",
    phones: List[Dict] = None,
    emails: List[Dict] = None,
    addresses: List[Dict] = None,
    urls: List[str] = None,
    birthday: Union[str, date] = None,
    note: str = "",
    version: str = "3.0"
) -> VCard:
    """
    创建 VCard 对象。
    
    Args:
        full_name: 全名（必需）
        family_name: 姓
        given_name: 名
        organization: 组织/公司名
        title: 职位
        phones: 电话列表，每个元素为 {'number': '...', 'type': 'work'}
        emails: 邮箱列表，每个元素为 {'address': '...', 'type': 'work'}
        addresses: 地址列表，每个元素为 {'street': '...', 'city': '...'}
        urls: 网址列表
        birthday: 生日（字符串或日期对象）
        note: 备注
        version: VCard 版本（2.1, 3.0, 4.0）
    
    Returns:
        VCard 对象
    
    Example:
        >>> card = create_vcard("张三", phones=[{"number": "13800138000", "type": "cell"}])
        >>> print(card.full_name)
    """
    # 创建姓名对象
    name = VCardName(
        family_name=family_name,
        given_name=given_name
    )
    
    # 创建 VCard 对象
    vcard = VCard(
        version=version,
        name=name,
        full_name=full_name,
        title=title,
        note=note
    )
    
    # 设置组织
    if organization:
        vcard.organization = VCardOrganization(name=organization, title=title)
    
    # 添加电话
    if phones:
        for phone_data in phones:
            vcard.phones.append(VCardPhone(
                number=phone_data.get('number', ''),
                type=phone_data.get('type', 'voice'),
                pref=phone_data.get('pref', 0)
            ))
    
    # 添加邮箱
    if emails:
        for email_data in emails:
            vcard.emails.append(VCardEmail(
                address=email_data.get('address', ''),
                type=email_data.get('type', 'internet'),
                pref=email_data.get('pref', 0)
            ))
    
    # 添加地址
    if addresses:
        for addr_data in addresses:
            vcard.addresses.append(VCardAddress(
                street=addr_data.get('street', ''),
                city=addr_data.get('city', ''),
                region=addr_data.get('region', ''),
                postal_code=addr_data.get('postal_code', ''),
                country=addr_data.get('country', ''),
                type=addr_data.get('type', '')
            ))
    
    # 添加网址
    if urls:
        for url in urls:
            if isinstance(url, str):
                vcard.urls.append(VCardURL(url=url))
            elif isinstance(url, dict):
                vcard.urls.append(VCardURL(
                    url=url.get('url', ''),
                    type=url.get('type', '')
                ))
    
    # 设置生日
    if birthday:
        if isinstance(birthday, str):
            # 尝试解析日期字符串
            try:
                vcard.birthday = datetime.strptime(birthday, "%Y-%m-%d").date()
            except ValueError:
                # 尝试其他格式
                for fmt in ["%Y/%m/%d", "%d-%m-%Y", "%d/%m/%Y"]:
                    try:
                        vcard.birthday = datetime.strptime(birthday, fmt).date()
                        break
                    except ValueError:
                        continue
        elif isinstance(birthday, date):
            vcard.birthday = birthday
    
    # 生成 UID
    import uuid
    vcard.uid = str(uuid.uuid4())
    
    # 设置修订时间
    vcard.revision = datetime.now()
    
    return vcard


def vcard_to_string(vcard: VCard) -> str:
    """
    将 VCard 对象转换为 VCard 字符串格式。
    
    Args:
        vcard: VCard 对象
    
    Returns:
        VCard 格式的字符串
    
    Example:
        >>> card = create_vcard("张三")
        >>> print(vcard_to_string(card))
    """
    lines = []
    
    # 开始标记
    lines.append("BEGIN:VCARD")
    lines.append(f"VERSION:{vcard.version}")
    
    # 全名（FN）- 必需
    lines.append(f"FN:{vcard.full_name}")
    
    # 姓名（N）
    if vcard.name:
        lines.append(f"N:{vcard.name.to_vcard_format()}")
    
    # 组织（ORG）
    if vcard.organization:
        lines.append(f"ORG:{vcard.organization.to_vcard_format()}")
    
    # 职位（TITLE）
    if vcard.title:
        lines.append(f"TITLE:{vcard.title}")
    
    # 角色（ROLE）
    if vcard.role:
        lines.append(f"ROLE:{vcard.role}")
    
    # 电话（TEL）
    for phone in vcard.phones:
        lines.append(phone.to_vcard_format())
    
    # 邮箱（EMAIL）
    for email in vcard.emails:
        lines.append(email.to_vcard_format())
    
    # 地址（ADR）
    for addr in vcard.addresses:
        type_param = f";TYPE={addr.type}" if addr.type else ""
        lines.append(f"ADR{type_param}:{addr.to_vcard_format()}")
    
    # 网址（URL）
    for url in vcard.urls:
        lines.append(url.to_vcard_format())
    
    # 社交媒体
    for social in vcard.socials:
        lines.append(social.to_vcard_format())
    
    # 照片（PHOTO）
    if vcard.photo:
        photo_lines = vcard.photo.to_vcard_format(vcard.version)
        # 对于长编码数据，分割成多行（每行 75 字符）
        if len(photo_lines) > 75:
            photo_lines = _fold_line(photo_lines)
        lines.append(photo_lines)
    
    # 生日（BDAY）
    if vcard.birthday:
        lines.append(f"BDAY:{vcard.birthday.strftime('%Y-%m-%d')}")
    
    # 昵称（NICKNAME）
    if vcard.nickname:
        lines.append(f"NICKNAME:{vcard.nickname}")
    
    # 备注（NOTE）
    if vcard.note:
        note_text = vcard.note.replace('\n', '\\n')
        lines.append(f"NOTE:{note_text}")
    
    # 分类（CATEGORIES）
    if vcard.categories:
        lines.append(f"CATEGORIES:{','.join(vcard.categories)}")
    
    # 时区（TZ）
    if vcard.timezone:
        lines.append(f"TZ:{vcard.timezone}")
    
    # 地理位置（GEO）
    if vcard.geo[0] != 0.0 or vcard.geo[1] != 0.0:
        lines.append(f"GEO:{vcard.geo[0]};{vcard.geo[1]}")
    
    # UID
    if vcard.uid:
        lines.append(f"UID:{vcard.uid}")
    
    # 修订时间（REV）
    if vcard.revision:
        lines.append(f"REV:{vcard.revision.strftime('%Y-%m-%dT%H:%M:%SZ')}")
    
    # 自定义字段
    for key, value in vcard.custom_fields.items():
        lines.append(f"{key}:{value}")
    
    # 结束标记
    lines.append("END:VCARD")
    
    return "\n".join(lines)


def _fold_line(line: str, max_length: int = 75) -> str:
    """
    将长行分割成多行（VCard 标准要求每行不超过 75 字符）。
    
    Args:
        line: 长行
        max_length: 最大行长度
    
    Returns:
        分割后的多行字符串
    """
    result = []
    while len(line) > max_length:
        result.append(line[:max_length])
        line = " " + line[max_length:]  # 空格表示续行
    result.append(line)
    return "\r\n".join(result)


# =============================================================================
# VCard 解析功能
# =============================================================================

def parse_vcard(source: Union[str, Path, BinaryIO]) -> VCard:
    """
    解析 VCard 文件或字符串。
    
    Args:
        source: 文件路径、文件对象或 VCard 字符串
    
    Returns:
        VCard 对象
    
    Raises:
        VCardFileNotFoundError: 文件不存在
        VCardFormatError: VCard 格式错误
    
    Example:
        >>> card = parse_vcard("contact.vcf")
        >>> print(card.full_name)
    """
    # 获取内容
    if isinstance(source, Path):
        if not source.exists():
            raise VCardFileNotFoundError(f"文件不存在：{source}")
        with open(source, 'r', encoding='utf-8') as f:
            content = f.read()
    elif isinstance(source, str):
        # 判断是否是文件路径还是 VCard 内容
        # VCard 内容以 BEGIN:VCARD 开始
        if source.strip().startswith('BEGIN:VCARD'):
            content = source
        elif source.endswith('.vcf') or source.endswith('.vcard'):
            # 明确是 VCard 文件扩展名
            if not os.path.exists(source):
                raise VCardFileNotFoundError(f"文件不存在：{source}")
            with open(source, 'r', encoding='utf-8') as f:
                content = f.read()
        elif (os.path.sep in source or (os.path.altsep and os.path.altsep in source)) and os.path.exists(source):
            # 是路径且文件存在
            with open(source, 'r', encoding='utf-8') as f:
                content = f.read()
        else:
            # 默认当作 VCard 内容处理
            content = source
    else:
        content = source.read() if hasattr(source, 'read') else str(source)
    
    # 解析内容
    return _parse_vcard_content(content)


def _parse_vcard_content(content: str) -> VCard:
    """解析 VCard 内容。"""
    # 移除续行标记（空格开头的行）
    content = re.sub(r'\r?\n[ \t]', '', content)
    
    # 分割成行
    lines = content.strip().split('\n')
    
    # 验证基本结构
    if not lines or lines[0].strip() != 'BEGIN:VCARD':
        raise VCardFormatError("VCard 必须以 BEGIN:VCARD 开始")
    
    if lines[-1].strip() != 'END:VCARD':
        raise VCardFormatError("VCard 必须以 END:VCARD 结束")
    
    # 创建 VCard 对象
    vcard = VCard()
    
    # 解析每一行
    for line in lines[1:-1]:
        line = line.strip()
        if not line:
            continue
        
        # 解析属性
        key, value = _parse_property(line)
        
        # 处理标准属性
        _handle_property(vcard, key, value)
    
    return vcard


def _parse_property(line: str) -> Tuple[str, str]:
    """
    解析 VCard 属性行。
    
    Returns:
        (属性键, 属性值)
    """
    # 分割键和值
    if ':' in line:
        colon_pos = line.index(':')
        key = line[:colon_pos]
        value = line[colon_pos + 1:]
    else:
        return line, ""
    
    # 处理编码值
    if 'ENCODING=BASE64' in key or 'ENCODING=b' in key:
        try:
            value = base64.b64decode(value).decode('utf-8', errors='replace')
        except Exception:
            pass
    
    # 处理参数
    key = key.split(';')[0]  # 只取属性名
    
    return key.upper(), value


def _handle_property(vcard: VCard, key: str, value: str) -> None:
    """处理单个属性。"""
    if key == 'VERSION':
        vcard.version = value
    elif key == 'FN':
        vcard.full_name = value
    elif key == 'N':
        parts = value.split(';')
        vcard.name = VCardName(
            family_name=parts[0] if len(parts) > 0 else "",
            given_name=parts[1] if len(parts) > 1 else "",
            additional_names=parts[2].split(',') if len(parts) > 2 and parts[2] else [],
            honorific_prefixes=parts[3].split(',') if len(parts) > 3 and parts[3] else [],
            honorific_suffixes=parts[4].split(',') if len(parts) > 4 and parts[4] else []
        )
    elif key == 'TEL':
        vcard.phones.append(VCardPhone(number=value))
    elif key == 'EMAIL':
        vcard.emails.append(VCardEmail(address=value))
    elif key == 'ADR':
        parts = value.split(';')
        vcard.addresses.append(VCardAddress(
            po_box=parts[0] if len(parts) > 0 else "",
            extended_address=parts[1] if len(parts) > 1 else "",
            street=parts[2] if len(parts) > 2 else "",
            city=parts[3] if len(parts) > 3 else "",
            region=parts[4] if len(parts) > 4 else "",
            postal_code=parts[5] if len(parts) > 5 else "",
            country=parts[6] if len(parts) > 6 else ""
        ))
    elif key == 'ORG':
        parts = value.split(';')
        vcard.organization = VCardOrganization(
            name=parts[0] if len(parts) > 0 else "",
            unit=parts[1] if len(parts) > 1 else ""
        )
    elif key == 'TITLE':
        vcard.title = value
    elif key == 'ROLE':
        vcard.role = value
    elif key == 'URL':
        vcard.urls.append(VCardURL(url=value))
    elif key == 'BDAY':
        try:
            vcard.birthday = datetime.strptime(value, '%Y-%m-%d').date()
        except ValueError:
            pass
    elif key == 'NICKNAME':
        vcard.nickname = value
    elif key == 'NOTE':
        vcard.note = value.replace('\\n', '\n')
    elif key == 'CATEGORIES':
        vcard.categories = value.split(',')
    elif key == 'TZ':
        vcard.timezone = value
    elif key == 'GEO':
        parts = value.split(';')
        if len(parts) >= 2:
            try:
                vcard.geo = (float(parts[0]), float(parts[1]))
            except ValueError:
                pass
    elif key == 'UID':
        vcard.uid = value
    elif key == 'REV':
        try:
            vcard.revision = datetime.strptime(value, '%Y-%m-%dT%H:%M:%SZ')
        except ValueError:
            pass
    elif key == 'PHOTO':
        # 照片处理
        if 'data:' in value:
            # 4.0 格式：data:image/jpeg;base64,...
            parts = value.split(',', 1)
            if len(parts) > 1:
                try:
                    vcard.photo = VCardPhoto(
                        data=base64.b64decode(parts[1]),
                        type='image/jpeg'
                    )
                except Exception:
                    pass
        else:
            try:
                vcard.photo = VCardPhoto(
                    data=base64.b64decode(value),
                    type='image/jpeg'
                )
            except Exception:
                pass
    else:
        # 自定义字段
        vcard.custom_fields[key] = value


def parse_vcards(source: Union[str, Path]) -> List[VCard]:
    """
    解析包含多个 VCard 的文件。
    
    Args:
        source: 文件路径或 VCard 字符串
    
    Returns:
        VCard 对象列表
    
    Example:
        >>> cards = parse_vcards("contacts.vcf")
        >>> print(len(cards))
    """
    # 获取内容
    if isinstance(source, Path):
        if not source.exists():
            raise VCardFileNotFoundError(f"文件不存在：{source}")
        with open(source, 'r', encoding='utf-8') as f:
            content = f.read()
    elif isinstance(source, str):
        if os.path.exists(source):
            with open(source, 'r', encoding='utf-8') as f:
                content = f.read()
        else:
            content = source
    else:
        content = str(source)
    
    # 分割多个 VCard
    vcards = []
    start_indices = []
    
    for i, line in enumerate(content.split('\n')):
        if line.strip() == 'BEGIN:VCARD':
            start_indices.append(i)
    
    lines = content.split('\n')
    for start_idx in start_indices:
        # 找到对应的 END:VCARD
        end_idx = start_idx
        for j in range(start_idx + 1, len(lines)):
            if lines[j].strip() == 'END:VCARD':
                end_idx = j
                break
        
        # 提取单个 VCard 内容
        vcard_content = '\n'.join(lines[start_idx:end_idx + 1])
        vcards.append(_parse_vcard_content(vcard_content))
    
    return vcards


# =============================================================================
# VCard 写入功能
# =============================================================================

def save_vcard(vcard: VCard, file_path: Union[str, Path]) -> None:
    """
    将 VCard 保存到文件。
    
    Args:
        vcard: VCard 对象
        file_path: 输出文件路径
    
    Example:
        >>> card = create_vcard("张三")
        >>> save_vcard(card, "contact.vcf")
    """
    content = vcard_to_string(vcard)
    
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)


def save_vcards(vcards: List[VCard], file_path: Union[str, Path]) -> None:
    """
    将多个 VCard 保存到文件。
    
    Args:
        vcards: VCard 对象列表
        file_path: 输出文件路径
    
    Example:
        >>> cards = [create_vcard("张三"), create_vcard("李四")]
        >>> save_vcards(cards, "contacts.vcf")
    """
    content = '\n\n'.join(vcard_to_string(card) for card in vcards)
    
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)


# =============================================================================
# VCard 验证功能
# =============================================================================

def validate_vcard(vcard: VCard) -> Tuple[bool, List[str]]:
    """
    验证 VCard 对象。
    
    Args:
        vcard: VCard 对象
    
    Returns:
        (是否有效，错误消息列表)
    
    Example:
        >>> card = create_vcard("张三")
        >>> valid, errors = validate_vcard(card)
        >>> print(valid)
    """
    errors = []
    
    # 检查必需属性
    if not vcard.full_name:
        errors.append("缺少必需属性：FN（全名）")
    
    # 检查版本
    if vcard.version not in ['2.1', '3.0', '4.0']:
        errors.append(f"不支持的版本：{vcard.version}")
    
    # 检查邮箱格式
    for email in vcard.emails:
        if email.address and not _is_valid_email(email.address):
            errors.append(f"无效邮箱格式：{email.address}")
    
    # 检查电话格式
    for phone in vcard.phones:
        if phone.number and not _is_valid_phone(phone.number):
            errors.append(f"无效电话格式：{phone.number}")
    
    return len(errors) == 0, errors


def _is_valid_email(email: str) -> bool:
    """简单验证邮箱格式。"""
    pattern = r'^[a-zA-Z00-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def _is_valid_phone(phone: str) -> bool:
    """简单验证电话格式。"""
    # 移除非数字字符（保留 +）
    clean = re.sub(r'[^\d+]', '', phone)
    return len(clean) >= 7


def validate_vcard_file(file_path: Union[str, Path]) -> Tuple[bool, List[str]]:
    """
    验证 VCard 文件。
    
    Args:
        file_path: VCard 文件路径
    
    Returns:
        (是否有效，错误消息列表)
    """
    errors = []
    
    try:
        vcard = parse_vcard(file_path)
        return validate_vcard(vcard)
    except VCardFileNotFoundError as e:
        return False, [str(e)]
    except VCardFormatError as e:
        return False, [str(e)]


# =============================================================================
# VCard 转换功能
# =============================================================================

def vcard_to_dict(vcard: VCard) -> Dict[str, Any]:
    """
    将 VCard 转换为字典。
    
    Args:
        vcard: VCard 对象
    
    Returns:
        字典表示
    
    Example:
        >>> card = create_vcard("张三")
        >>> data = vcard_to_dict(card)
        >>> print(data['full_name'])
    """
    data = {
        'version': vcard.version,
        'full_name': vcard.full_name,
        'phones': [{'number': p.number, 'type': p.type} for p in vcard.phones],
        'emails': [{'address': e.address, 'type': e.type} for e in vcard.emails],
        'urls': [{'url': u.url, 'type': u.type} for u in vcard.urls],
        'addresses': [{
            'street': a.street,
            'city': a.city,
            'region': a.region,
            'postal_code': a.postal_code,
            'country': a.country,
            'type': a.type
        } for a in vcard.addresses],
        'note': vcard.note,
        'categories': vcard.categories,
        'uid': vcard.uid,
    }
    
    if vcard.name:
        data['name'] = {
            'family_name': vcard.name.family_name,
            'given_name': vcard.name.given_name,
            'additional_names': vcard.name.additional_names,
        }
    
    if vcard.organization:
        data['organization'] = {
            'name': vcard.organization.name,
            'unit': vcard.organization.unit,
            'title': vcard.title,
        }
    
    if vcard.birthday:
        data['birthday'] = vcard.birthday.strftime('%Y-%m-%d')
    
    return data


def dict_to_vcard(data: Dict[str, Any]) -> VCard:
    """
    从字典创建 VCard。
    
    Args:
        data: 字典数据
    
    Returns:
        VCard 对象
    
    Example:
        >>> data = {'full_name': '张三', 'phones': [{'number': '13800138000'}]}
        >>> card = dict_to_vcard(data)
    """
    vcard = VCard()
    
    vcard.version = data.get('version', '3.0')
    vcard.full_name = data.get('full_name', '')
    
    if 'name' in data:
        name_data = data['name']
        vcard.name = VCardName(
            family_name=name_data.get('family_name', ''),
            given_name=name_data.get('given_name', ''),
            additional_names=name_data.get('additional_names', []),
        )
    
    for phone_data in data.get('phones', []):
        vcard.phones.append(VCardPhone(
            number=phone_data.get('number', ''),
            type=phone_data.get('type', 'voice'),
        ))
    
    for email_data in data.get('emails', []):
        vcard.emails.append(VCardEmail(
            address=email_data.get('address', ''),
            type=email_data.get('type', 'internet'),
        ))
    
    for addr_data in data.get('addresses', []):
        vcard.addresses.append(VCardAddress(
            street=addr_data.get('street', ''),
            city=addr_data.get('city', ''),
            region=addr_data.get('region', ''),
            postal_code=addr_data.get('postal_code', ''),
            country=addr_data.get('country', ''),
            type=addr_data.get('type', ''),
        ))
    
    if 'organization' in data:
        org_data = data['organization']
        vcard.organization = VCardOrganization(
            name=org_data.get('name', ''),
            unit=org_data.get('unit', ''),
        )
        vcard.title = org_data.get('title', '')
    
    for url_data in data.get('urls', []):
        if isinstance(url_data, str):
            vcard.urls.append(VCardURL(url=url_data))
        else:
            vcard.urls.append(VCardURL(
                url=url_data.get('url', ''),
                type=url_data.get('type', ''),
            ))
    
    vcard.note = data.get('note', '')
    vcard.categories = data.get('categories', [])
    vcard.uid = data.get('uid', '')
    
    if 'birthday' in data:
        try:
            vcard.birthday = datetime.strptime(data['birthday'], '%Y-%m-%d').date()
        except ValueError:
            pass
    
    return vcard


# =============================================================================
# 便捷功能
# =============================================================================

def get_contact_summary(vcard: VCard) -> str:
    """
    获取联系人摘要。
    
    Args:
        vcard: VCard 对象
    
    Returns:
        摘要字符串
    
    Example:
        >>> card = create_vcard("张三", phones=[{"number": "13800138000"}])
        >>> print(get_contact_summary(card))
    """
    lines = [f"姓名：{vcard.full_name}"]
    
    if vcard.organization:
        org_str = vcard.organization.name
        if vcard.title:
            org_str += f" - {vcard.title}"
        lines.append(f"组织：{org_str}")
    
    if vcard.phones:
        phone_strs = [f"{p.number} ({p.type})" for p in vcard.phones]
        lines.append(f"电话：{', '.join(phone_strs)}")
    
    if vcard.emails:
        email_strs = [e.address for e in vcard.emails]
        lines.append(f"邮箱：{', '.join(email_strs)}")
    
    if vcard.addresses:
        addr_strs = [str(a) for a in vcard.addresses]
        lines.append(f"地址：{', '.join(addr_strs)}")
    
    return '\n'.join(lines)


def get_supported_versions() -> List[str]:
    """获取支持的 VCard 版本列表。"""
    return ['2.1', '3.0', '4.0']


def get_supported_properties() -> List[str]:
    """获取支持的 VCard 属性列表。"""
    return [
        'FN', 'N', 'TEL', 'EMAIL', 'ADR', 'ORG', 'TITLE', 'ROLE',
        'URL', 'BDAY', 'NICKNAME', 'NOTE', 'CATEGORIES', 'TZ', 'GEO',
        'UID', 'REV', 'PHOTO', 'VERSION'
    ]


def get_module_info() -> Dict[str, Any]:
    """获取模块信息。"""
    return {
        'name': 'vcard_utils',
        'version': __version__,
        'author': __author__,
        'license': __license__,
        'supported_versions': get_supported_versions(),
        'supported_properties': get_supported_properties(),
    }


# =============================================================================
# 快速创建功能
# =============================================================================

def quick_business_card(
    name: str,
    company: str,
    title: str,
    phone: str,
    email: str,
    website: str = ""
) -> VCard:
    """
    快速创建商务名片。
    
    Args:
        name: 姓名
        company: 公司
        title: 职位
        phone: 电话
        email: 雨箱
        website: 网站
    
    Returns:
        VCard 对象
    
    Example:
        >>> card = quick_business_card("张三", "科技公司", "工程师", "13800138000", "test@example.com")
    """
    return create_vcard(
        full_name=name,
        organization=company,
        title=title,
        phones=[{'number': phone, 'type': 'work'}],
        emails=[{'address': email, 'type': 'work'}],
        urls=[website] if website else None
    )


def quick_personal_card(
    name: str,
    phone: str,
    email: str,
    birthday: str = None,
    address: str = None
) -> VCard:
    """
    快速创建个人名片。
    
    Args:
        name: 姓名
        phone: 电话
        email: 雨箱
        birthday: 生日
        address: 地址
    
    Returns:
        VCard 对象
    
    Example:
        >>> card = quick_personal_card("张三", "13800138000", "test@example.com")
    """
    addresses = None
    if address:
        addresses = [{'street': address}]
    
    return create_vcard(
        full_name=name,
        phones=[{'number': phone, 'type': 'cell'}],
        emails=[{'address': email, 'type': 'personal'}],
        birthday=birthday,
        addresses=addresses
    )


# =============================================================================
# 导出
# =============================================================================

__all__ = [
    # 版本信息
    'get_version',
    'get_module_info',
    
    # 异常类
    'VCardUtilsError',
    'VCardFileNotFoundError',
    'VCardValidationError',
    'VCardFormatError',
    
    # 数据类
    'VCard',
    'VCardName',
    'VCardAddress',
    'VCardPhone',
    'VCardEmail',
    'VCardOrganization',
    'VCardPhoto',
    'VCardURL',
    'VCardSocial',
    
    # 创建功能
    'create_vcard',
    'quick_business_card',
    'quick_personal_card',
    
    # 解析功能
    'parse_vcard',
    'parse_vcards',
    
    # 写入功能
    'save_vcard',
    'save_vcards',
    'vcard_to_string',
    
    # 验证功能
    'validate_vcard',
    'validate_vcard_file',
    
    # 转换功能
    'vcard_to_dict',
    'dict_to_vcard',
    
    # 便捷功能
    'get_contact_summary',
    'get_supported_versions',
    'get_supported_properties',
]


# =============================================================================
# 主程序（测试）
# =============================================================================

if __name__ == '__main__':
    print("测试 VCard 工具模块...")
    
    # 创建测试名片
    card = create_vcard(
        full_name="张三",
        organization="科技公司",
        title="软件工程师",
        phones=[
            {'number': '13800138000', 'type': 'cell'},
            {'number': '010-12345678', 'type': 'work'}
        ],
        emails=[
            {'address': 'zhangsan@example.com', 'type': 'work'}
        ],
        urls=['https://example.com'],
        birthday='1990-05-20',
        note='测试联系人'
    )
    
    # 转换为字符串
    vcard_str = vcard_to_string(card)
    print("生成的 VCard：")
    print(vcard_str)
    
    # 解析测试
    parsed = parse_vcard(vcard_str)
    print(f"\n解析结果：{parsed.full_name}")
    
    # 验证测试
    valid, errors = validate_vcard(card)
    print(f"\n验证结果：{valid}, 错误：{errors}")
    
    # 摘要测试
    summary = get_contact_summary(card)
    print(f"\n联系人摘要：\n{summary}")
    
    print("\n所有测试通过！")