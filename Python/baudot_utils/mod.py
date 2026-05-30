"""
baudot_utils - 博多码 (Baudot/ITA2) 编解码工具

提供博多码（ITA2 / International Telegraph Alphabet No.2）的编码和解码功能。
博多码是 1870 年代由埃米尔·博多发明的 5 单位电码，曾广泛用于电报和电传打字机。

支持：
- ASCII 文本与博多码（5 位二进制）互转
- ASCII 模式与 FIG 模式（数字/特殊符号）的切换
- 博多码与二进制/十六进制字符串互转
- 比特流解析与错误检测

零外部依赖，纯 Python 实现。

Author: AllToolkit
Date: 2026-05-31
"""

from typing import List, Tuple, Optional, Dict


# =============================================================================
# 博多码表 (ITA2) - 标准索引版
# 每个索引 i (0–31) 对应 5 位码值 b4b3b2b1b0，按 MSB→LSB 排列。
#
# 两套字符集，通过移档键切换：
#   LTRS (31/0x1F): 字母模式
#   FIG  (27/0x1B): 数字/符号模式
#
# 索引到码字对照（b4b3b2b1b0 → 整数值）：
#   0=b00000, 1=b00001, 2=b00010, 3=b00011
#   4=b00100, 5=b00101, 6=b00110, 7=b00111
#   8=b01000, 9=b01001,10=b01010,11=b01011
#  12=b01100,13=b01101,14=b01110,15=b01111
#  16=b10000,17=b10001,18=b10010,19=b10011
#  20=b10100,21=b10101,22=b10110,23=b10111
#  24=b11000,25=b11001,26=b11010,27=b11011
#  28=b11100,29=b11101,30=b11110,31=b11111
# =============================================================================

# LTRS (字母模式) — 码表索引 → 字符
# 对照 ITU F.1 标准:
#   01=T  02=CR  03=O  04=SP  05=H
#   06=N  07=M  08=LF  09=L  0A=R
#   0B=W  0C=I  0D=P  0E=Q  0F=S
#   10=U  11=V  12=Z  13=E  14=D
#   15=B  16=F  17=X  18=C  19=K
#   1A= Unassigned  1B=A  1C=Y  1D=G
#   1E=J  1F=LTRS shift
LTRS_TABLE: Tuple[str, ...] = (
    "",      # 0x00 — NUL / blank
    "T",    # 0x01
    "\r",   # 0x02 — carriage return
    "O",    # 0x03
    " ",    # 0x04 — space
    "H",    # 0x05
    "N",    # 0x06
    "M",    # 0x07
    "\n",   # 0x08 — line feed
    "L",    # 0x09
    "R",    # 0x0A
    "W",    # 0x0B
    "I",    # 0x0C
    "P",    # 0x0D
    "Q",    # 0x0E
    "S",    # 0x0F
    "U",    # 0x10
    "V",    # 0x11
    "Z",    # 0x12
    "E",    # 0x13
    "D",    # 0x14
    "B",    # 0x15
    "F",    # 0x16
    "X",    # 0x17
    "C",    # 0x18
    "K",    # 0x19
    "",      # 0x1A — unassigned
    "A",    # 0x1B
    "Y",    # 0x1C
    "G",    # 0x1D
    "J",    # 0x1E
    "",     # 0x1F — LTRS shift (31)
)

# FIG (数字/符号模式) — 码表索引 → 字符
# 对照 ITU F.1 标准:
#   01=5  02=CR  03=9  04=SP  05=£
#   06=,  07=.  08=LF  09=)  0A=4
#   0B= WRU/BEL  0C=:  0D=3  0E='
#   0F=  -  10=7  11=8  12="/'  13=,
#   14=$  15=?  16="  17=6  18=(  19=2
#   1A= Unassigned  1B= FIG shift (27)  1C=1
#   1D=&  1E=BACKSPACE  1F=
FIG_TABLE: Tuple[str, ...] = (
    "",      # 0x00
    "5",    # 0x01
    "\r",   # 0x02
    "9",    # 0x03
    " ",    # 0x04
    "\xa3", # 0x05 — £ (pound sign)
    ",",    # 0x06
    ".",    # 0x07
    "\n",   # 0x08
    ")",    # 0x09
    "4",    # 0x0A
    "\a",   # 0x0B — BEL (bell)
    ":",    # 0x0C
    "3",    # 0x0D
    "'",    # 0x0E
    "-",    # 0x0F
    "7",    # 0x10
    "8",    # 0x11
    '"',    # 0x12 — double quote / proprietary
    ",",    # 0x13
    "$",    # 0x14
    "?",    # 0x15
    '"',    # 0x16 — apostrophe / proprietary
    "6",    # 0x17
    "(",    # 0x18
    "2",    # 0x19
    "",      # 0x1A
    "",      # 0x1B — FIG shift (27)
    "1",    # 0x1C
    "&",    # 0x1D
    "\b",   # 0x1E — backspace
    "",     # 0x1F
)

# 移档键码值
LTRS_CODE = 31  # 0x1F — 切换到字母模式
FIG_CODE  = 27  # 0x1B — 切换到数字/符号模式


# =============================================================================
# 辅助函数
# =============================================================================

def _int_to_bits(n: int, width: int = 5) -> str:
    """将整数转为宽度为 width 的二进制字符串（高位在左）。"""
    return format(n, "0{}b".format(width))


def _bits_to_int(bits: str) -> int:
    """将二进制字符串（高位在左）转为整数。"""
    return int(bits, 2)


# =============================================================================
# 核心编码
# =============================================================================

def encode_char(char: str, fig_mode: bool = False) -> Optional[int]:
    """
    编码单个字符为博多码（5 位整数值 0–31）。

    Args:
        char: 单个字符
        fig_mode: 当前是否为FIG模式

    Returns:
        int: 5 位博多码值 (0–31)，或 None（无法编码）
    """
    table = FIG_TABLE if fig_mode else LTRS_TABLE

    # 先在当前表查找
    for code, ch in enumerate(table):
        if ch == char:
            return code

    # FIG 模式找不到，回到 LTRS 表查找
    if fig_mode:
        for code, ch in enumerate(LTRS_TABLE):
            if ch == char:
                return code

    return None


def needs_fig_shift(char: str) -> bool:
    """判断字符是否需要切换到FIG模式（数字/符号）。"""
    if char in ("\n", "\r", " "):
        return False
    # Check if char is in the LTRS table (by index lookup, not tuple membership)
    in_ltrs = char in LTRS_TABLE
    in_fig = char in FIG_TABLE
    if not in_fig:
        return False  # 无法编码的字符
    if not in_ltrs:
        return True   # 仅存在于 FIG，必须切换
    # 存在于两表（共享字符）：不需要切换，编码结果相同
    return False


def encode(text: str) -> List[int]:
    """
    将 ASCII 文本编码为博多码序列。
    自动处理 LTRS/FIG 模式切换。

    Args:
        text: 输入文本

    Returns:
        List[int]: 博多码值列表 (0–31)
    """
    result: List[int] = []
    fig_mode = False

    for char in text:
        # 换行符：先切回 LTRS 模式再编码
        if char == "\n":
            if fig_mode:
                result.append(LTRS_CODE)
                fig_mode = False
            code = encode_char(char, fig_mode)
            if code is not None:
                result.append(code)
            continue

        if char == "\r":
            # CR 保持当前模式
            code = encode_char(char, fig_mode)
            if code is not None:
                result.append(code)
            continue

        # 需要切换到 FIG 模式吗？
        if needs_fig_shift(char):
            if not fig_mode:
                result.append(FIG_CODE)
                fig_mode = True

        code = encode_char(char, fig_mode)
        if code is None:
            continue

        result.append(code)

    # 确保以 LTRS 结尾（电传打字机惯例），便于解码器歧义处理
    if fig_mode:
        result.append(LTRS_CODE)

    return result


def decode(code_points: List[int], trim_trailing_ltrs: bool = True) -> str:
    """
    将博多码序列解码为 ASCII 文本。
    自动处理 LTRS/FIG 模式切换。

    处理歧义：码值 0x1B 在 LTRS 模式中可能是字母 'A' 或 FIG 移位键。
    通过扩展前看（前看 + 后顾）解决：

    前看策略：跳过所有移位键和意义相同的码，找到第一个意义不同的码。
      - 若该码在 LTRS 有意义 → 当前码 = 'A'
      - 若该码仅在 FIG 有意义 → 当前码 = FIG 键

    后顾策略：当扩展前看无法区分时（如 0x1B 后紧跟 LTRS_CODE）
      - 若前一个普通字符可确定模式 → 据此判断
      - 若前一个字符是两表共享的 → 无法判断，按 FIG 处理

    Args:
        code_points: 博多码值列表 (0–31)
        trim_trailing_ltrs: 是否去除末尾的 LTRS 移位

    Returns:
        str: 解码后的文本
    """
    result: List[str] = []
    fig_mode = False
    i = 0
    n = len(code_points)

    while i < n:
        code = code_points[i]

        # 歧义处理：0x1B 在 LTRS 模式 = 'A' 或 FIG 键
        if code == FIG_CODE and not fig_mode:
            # --- 扩展前看 ---
            j = i + 1
            while j < n:
                next_code = code_points[j]
                if next_code in (LTRS_CODE, FIG_CODE):
                    j += 1
                    continue
                next_ltrs = LTRS_TABLE[next_code] if next_code < len(LTRS_TABLE) else ""
                next_fig = FIG_TABLE[next_code] if next_code < len(FIG_TABLE) else ""
                if next_ltrs == next_fig:
                    j += 1
                    continue
                if next_ltrs:
                    result.append("A")
                    i += 1
                    break
                else:
                    fig_mode = True
                    i += 1
                    break
            else:
                # --- 扩展前看失败：尝试后顾 ---
                # 找前一个非移位码
                prev_idx = i - 1
                while prev_idx >= 0 and code_points[prev_idx] in (LTRS_CODE, FIG_CODE):
                    prev_idx -= 1
                if prev_idx >= 0:
                    prev_code = code_points[prev_idx]
                    prev_ltrs = LTRS_TABLE[prev_code] if prev_code < len(LTRS_TABLE) else ""
                    prev_fig = FIG_TABLE[prev_code] if prev_code < len(FIG_TABLE) else ""
                    # 如果前一个码在两表中意义相同，无法判断
                    if prev_ltrs == prev_fig:
                        # 无法判断，按 FIG 处理
                        fig_mode = True
                    elif prev_ltrs:
                        # 前一个码在 LTRS 有意义，说明之前是 LTRS 模式，0x1B = 'A'
                        result.append("A")
                    else:
                        # 前一个码仅在 FIG 有意义，说明之前是 FIG 模式，0x1B = FIG
                        fig_mode = True
                else:
                    # 没有前一个码，无法判断，按 FIG 处理
                    fig_mode = True
                i += 1
            continue

        if code == LTRS_CODE:
            fig_mode = False
            i += 1
            continue
        elif code == FIG_CODE:
            fig_mode = True
            i += 1
            continue

        table = FIG_TABLE if fig_mode else LTRS_TABLE
        ch = table[code] if code < len(table) else ""

        if ch:
            result.append(ch)

        i += 1

    return "".join(result)


# =============================================================================
# 格式转换
# =============================================================================

def encode_to_bits(code_points: List[int]) -> str:
    """
    将博多码序列转换为二进制字符串（5 位一组）。

    Args:
        code_points: 博多码值列表

    Returns:
        str: 二进制字符串，如 "11010 10001 ..."
    """
    return " ".join(_int_to_bits(c) for c in code_points)


def decode_from_bits(bit_string: str) -> List[int]:
    """
    从二进制字符串（5 位一组）解析出博多码序列。

    Args:
        bit_string: 空格分隔的二进制字符串，如 "11010 10001"

    Returns:
        List[int]: 博多码值列表
    """
    cleaned = bit_string.replace(" ", "").replace("\n", "").replace("\t", "")
    codes: List[int] = []
    for j in range(0, len(cleaned), 5):
        chunk = cleaned[j:j+5]
        if len(chunk) == 5:
            codes.append(_bits_to_int(chunk))
    return codes


def encode_to_hex(code_points: List[int]) -> str:
    """
    将博多码序列转换为紧凑的十六进制字符串。
    每 4 个 5 位码打包成 20 位，用 5 个 hex 字符表示。

    Args:
        code_points: 博多码值列表

    Returns:
        str: 十六进制字符串
    """
    if not code_points:
        return ""

    result_hex = []
    for k in range(0, len(code_points), 4):
        chunk = code_points[k:k+4]
        # 不足 4 个末尾补 0
        while len(chunk) < 4:
            chunk.append(0)

        # 打包为 20 位整数：bits = c3<<15 | c2<<10 | c1<<5 | c0
        packed = (chunk[0] << 15) | (chunk[1] << 10) | (chunk[2] << 5) | chunk[3]
        result_hex.append("{:05X}".format(packed))

    return "".join(result_hex)


def decode_from_hex(hex_string: str) -> List[int]:
    """
    从十六进制字符串解码为博多码序列。

    Args:
        hex_string: encode_to_hex 生成的十六进制字符串

    Returns:
        List[int]: 博多码值列表
    """
    if not hex_string:
        return []

    codes: List[int] = []
    for k in range(0, len(hex_string), 5):
        chunk = hex_string[k:k+5]
        if len(chunk) < 5:
            chunk = chunk.ljust(5, "0")

        packed = int(chunk, 16)
        c0 = (packed >> 0) & 0x1F
        c1 = (packed >> 5) & 0x1F
        c2 = (packed >> 10) & 0x1F
        c3 = (packed >> 15) & 0x1F
        codes.extend([c3, c2, c1, c0])

    # 去除末尾补的 0
    while codes and codes[-1] == 0:
        codes.pop()

    return codes


# =============================================================================
# 比特流分析
# =============================================================================

def bits_to_bauds(bits: str) -> List[int]:
    """
    将连续的比特字符串解析为多个 5 位码值。

    Args:
        bits: 连续的 0/1 字符串

    Returns:
        List[int]: 码值列表
    """
    cleaned = bits.replace(" ", "").replace("\n", "")
    codes: List[int] = []
    for j in range(0, len(cleaned), 5):
        chunk = cleaned[j:j+5]
        if len(chunk) == 5:
            codes.append(_bits_to_int(chunk))
    return codes


def validate_code_point(code: int) -> bool:
    """检查码值是否在有效范围 0–31。"""
    return 0 <= code <= 31


def validate_stream(code_points: List[int]) -> Tuple[bool, List[int]]:
    """
    验证博多码流，检测非法码值。

    Args:
        code_points: 码值列表

    Returns:
        Tuple[bool, List[int]]: (是否有效, 非法码值的索引列表)
    """
    invalid: List[int] = []
    for idx, c in enumerate(code_points):
        if not validate_code_point(c):
            invalid.append(idx)
    return len(invalid) == 0, invalid


# =============================================================================
# 码表查询
# =============================================================================

def get_letters_table() -> Dict[int, str]:
    """获取完整的 LTRS 码表。"""
    return {i: LTRS_TABLE[i] for i in range(32)}


def get_figures_table() -> Dict[int, str]:
    """获取完整的 FIG 码表。"""
    return {i: FIG_TABLE[i] for i in range(32)}


def lookup_code(code: int, fig_mode: bool = False) -> str:
    """
    查询指定码值的字符。

    Args:
        code: 码值 (0–31)
        fig_mode: 是否为FIG模式

    Returns:
        str: 对应字符，空字符串表示未定义
    """
    if not validate_code_point(code):
        return ""
    table = FIG_TABLE if fig_mode else LTRS_TABLE
    return table[code]


# =============================================================================
# 便捷函数
# =============================================================================

def bauds_to_text(code_points: List[int]) -> str:
    """博多码列表转文本（decode 的别名）。"""
    return decode(code_points)


def text_to_bauds(text: str) -> List[int]:
    """文本转博多码列表（encode 的别名）。"""
    return encode(text)


def encode_text_to_bits(text: str) -> str:
    """文本 → 博多码 → 二进制字符串。"""
    return encode_to_bits(encode(text))


def decode_bits_to_text(bits: str) -> str:
    """二进制字符串 → 博多码 → 文本。"""
    return decode(bits_to_bauds(bits))
