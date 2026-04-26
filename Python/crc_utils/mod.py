#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - CRC (Cyclic Redundancy Check) Utilities Module
============================================================
A comprehensive CRC computation and validation utility module for Python
with zero external dependencies.

Features:
    - CRC-8, CRC-16, CRC-32, CRC-64 computation
    - Multiple standard CRC algorithms
    - Custom CRC polynomial support
    - File CRC computation
    - Data integrity verification
    - CRC table generation for performance
    - Bit reflection utilities
    - Hex and integer CRC output

Supported Algorithms:
    - CRC-8 (poly 0x07)
    - CRC-8-CCITT (poly 0x07)
    - CRC-8-MAXIM (poly 0x31)
    - CRC-16-IBM (poly 0x8005)
    - CRC-16-CCITT (poly 0x1021)
    - CRC-16-MODBUS (poly 0x8005)
    - CRC-32 (poly 0x04C11DB7) - same as zlib.crc32
    - CRC-32C (poly 0x1EDC6F41) - Castagnoli
    - CRC-64-ECMA (poly 0x42F0E1EBA9EA3693)
    - CRC-64-ISO (poly 0x000000000000001B)

Author: AllToolkit Contributors
License: MIT
"""

from typing import Union, Optional, Dict, Tuple
from functools import lru_cache
import struct


# ============================================================================
# Type Aliases
# ============================================================================

BytesLike = Union[bytes, bytearray, str]
CRCValue = int


# ============================================================================
# Pre-computed CRC Tables
# ============================================================================

# CRC-32 table (reflected polynomial 0xEDB88320)
CRC32_TABLE = (
    0x00000000, 0x77073096, 0xEE0E612C, 0x990951BA, 0x076DC419, 0x706AF48F, 0xE963A535, 0x9E6495A3,
    0x0EDB8832, 0x79DCB8A4, 0xE0D5E91E, 0x97D2D988, 0x09B64C2B, 0x7EB17CBD, 0xE7B82D07, 0x90BF1D91,
    0x1DB71064, 0x6AB020F2, 0xF3B97148, 0x84BE41DE, 0x1ADAD47D, 0x6DDDE4EB, 0xF4D4B551, 0x83D385C7,
    0x136C9856, 0x646BA8C0, 0xFD62F97A, 0x8A65C9EC, 0x14015C4F, 0x63066CD9, 0xFA0F3D63, 0x8D080DF5,
    0x3B6E20C8, 0x4C69105E, 0xD56041E4, 0xA2677172, 0x3C03E4D1, 0x4B04D447, 0xD20D85FD, 0xA50AB56B,
    0x35B5A8FA, 0x42B2986C, 0xDBBBC9D6, 0xACBCF940, 0x32D86CE3, 0x45DF5C75, 0xDCD60DCF, 0xABD13D59,
    0x26D930AC, 0x51DE003A, 0xC8D75180, 0xBFD06116, 0x21B4F4B5, 0x56B3C423, 0xCFBA9599, 0xB8BDA50F,
    0x2802B89E, 0x5F058808, 0xC60CD9B2, 0xB10BE924, 0x2F6F7C87, 0x58684C11, 0xC1611DAB, 0xB6662D3D,
    0x76DC4190, 0x01DB7106, 0x98D220BC, 0xEFD5102A, 0x71B18589, 0x06B6B51F, 0x9FBFE4A5, 0xE8B8D433,
    0x7807C9A2, 0x0F00F934, 0x9609A88E, 0xE10E9818, 0x7F6A0DBB, 0x086D3D2D, 0x91646C97, 0xE6635C01,
    0x6B6B51F4, 0x1C6C6162, 0x856530D8, 0xF262004E, 0x6C0695ED, 0x1B01A57B, 0x8208F4C1, 0xF50FC457,
    0x65B0D9C6, 0x12B7E950, 0x8BBEB8EA, 0xFCB9887C, 0x62DD1DDF, 0x15DA2D49, 0x8CD37CF3, 0xFBD44C65,
    0x4DB26158, 0x3AB551CE, 0xA3BC0074, 0xD4BB30E2, 0x4ADFA541, 0x3DD895D7, 0xA4D1C46D, 0xD3D6F4FB,
    0x4369E96A, 0x346ED9FC, 0xAD678846, 0xDA60B8D0, 0x44042D73, 0x33031DE5, 0xAA0A4C5F, 0xDD0D7CC9,
    0x5005713C, 0x270241AA, 0xBE0B1010, 0xC90C2086, 0x5768B525, 0x206F85B3, 0xB966D409, 0xCE61E49F,
    0x5EDEF90E, 0x29D9C998, 0xB0D09822, 0xC7D7A8B4, 0x59B33D17, 0x2EB40D81, 0xB7BD5C3B, 0xC0BA6CAD,
    0xEDB88320, 0x9ABFB3B6, 0x03B6E20C, 0x74B1D29A, 0xEAD54739, 0x9DD277AF, 0x04DB2615, 0x73DC1683,
    0xE3630B12, 0x94643B84, 0x0D6D6A3E, 0x7A6A5AA8, 0xE40ECF0B, 0x9309FF9D, 0x0A00AE27, 0x7D079EB1,
    0xF00F9344, 0x8708A3D2, 0x1E01F268, 0x6906C2FE, 0xF762575D, 0x806567CB, 0x196C3671, 0x6E6B06E7,
    0xFED41B76, 0x89D32BE0, 0x10DA7A5A, 0x67DD4ACC, 0xF9B9DF6F, 0x8EBEEFF9, 0x17B7BE43, 0x60B08ED5,
    0xD6D6A3E8, 0xA1D1937E, 0x38D8C2C4, 0x4FDFF252, 0xD1BB67F1, 0xA6BC5767, 0x3FB506DD, 0x48B2364B,
    0xD80D2BDA, 0xAF0A1B4C, 0x36034AF6, 0x41047A60, 0xDF60EFC3, 0xA867DF55, 0x316E8EEF, 0x4669BE79,
    0xCB61B38C, 0xBC66831A, 0x256FD2A0, 0x5268E236, 0xCC0C7795, 0xBB0B4703, 0x220216B9, 0x5505262F,
    0xC5BA3BBE, 0xB2BD0B28, 0x2BB45A92, 0x5CB36A04, 0xC2D7FFA7, 0xB5D0CF31, 0x2CD99E8B, 0x5BDEAE1D,
    0x9B64C2B0, 0xEC63F226, 0x756AA39C, 0x026D930A, 0x9C0906A9, 0xEB0E363F, 0x72076785, 0x05005713,
    0x95BF4A82, 0xE2B87A14, 0x7BB12BAE, 0x0CB61B38, 0x92D28E9B, 0xE5D5BE0D, 0x7CDCEFB7, 0x0BDBDF21,
    0x86D3D2D4, 0xF1D4E242, 0x68DDB3F8, 0x1FDA836E, 0x81BE16CD, 0xF6B9265B, 0x6FB077E1, 0x18B74777,
    0x88085AE6, 0xFF0F6A70, 0x66063BCA, 0x11010B5C, 0x8F659EFF, 0xF862AE69, 0x616BFFD3, 0x166CCF45,
    0xA00AE278, 0xD70DD2EE, 0x4E048354, 0x3903B3C2, 0xA7672661, 0xD06016F7, 0x4969474D, 0x3E6E77DB,
    0xAED16A4A, 0xD9D65ADC, 0x40DF0B66, 0x37D83BF0, 0xA9BCAE53, 0xDEBB9EC5, 0x47B2CF7F, 0x30B5FFE9,
    0xBDBDF21C, 0xCABAC28A, 0x53B39330, 0x24B4A3A6, 0xBAD03605, 0xCDD70693, 0x54DE5729, 0x23D967BF,
    0xB3667A2E, 0xC4614AB8, 0x5D681B02, 0x2A6F2B94, 0xB40BBE37, 0xC30C8EA1, 0x5A05DF1B, 0x2D02EF8D,
)

# CRC-16-CCITT (reflected) table
CRC16_CCITT_TABLE = (
    0x0000, 0x1189, 0x2312, 0x329B, 0x4624, 0x57AD, 0x6536, 0x74BF,
    0x8C48, 0x9DC1, 0xAF5A, 0xBED3, 0xCA6C, 0xDBE5, 0xE97E, 0xF8F7,
    0x1081, 0x0108, 0x3393, 0x221A, 0x56A5, 0x472C, 0x75B7, 0x643E,
    0x9CC9, 0x8D40, 0xBFDB, 0xAE52, 0xDAED, 0xCB64, 0xF9FF, 0xE876,
    0x2102, 0x308B, 0x0210, 0x1399, 0x6726, 0x76AF, 0x4434, 0x55BD,
    0xAD4A, 0xBCC3, 0x8E58, 0x9FD1, 0xEB6E, 0xFAE7, 0xC87C, 0xD9F5,
    0x3183, 0x200A, 0x1291, 0x0318, 0x77A7, 0x662E, 0x54B5, 0x453C,
    0xBDCB, 0xAC42, 0x9ED9, 0x8F50, 0xFBEF, 0xEA66, 0xD8FD, 0xC974,
    0x4204, 0x538D, 0x6116, 0x709F, 0x0420, 0x15A9, 0x2732, 0x36BB,
    0xCE4C, 0xDFC5, 0xED5E, 0xFCD7, 0x8868, 0x99E1, 0xAB7A, 0xBAF3,
    0x5285, 0x430C, 0x7197, 0x601E, 0x14A1, 0x0528, 0x37B3, 0x263A,
    0xDECD, 0xCF44, 0xFDDF, 0xEC56, 0x98E9, 0x8960, 0xBBFB, 0xAA72,
    0x6306, 0x728F, 0x4014, 0x519D, 0x2522, 0x34AB, 0x0630, 0x17B9,
    0xEF4E, 0xFEC7, 0xCC5C, 0xDDD5, 0xA96A, 0xB8E3, 0x8A78, 0x9BF1,
    0x7387, 0x620E, 0x5095, 0x411C, 0x35A3, 0x242A, 0x16B1, 0x0738,
    0xFFCF, 0xEE46, 0xDCDD, 0xCD54, 0xB9EB, 0xA862, 0x9AF9, 0x8B70,
    0x8408, 0x9581, 0xA71A, 0xB693, 0xC22C, 0xD3A5, 0xE13E, 0xF0B7,
    0x0840, 0x19C9, 0x2B52, 0x3ADB, 0x4E64, 0x5FED, 0x6D76, 0x7CFF,
    0x9489, 0x8500, 0xB79B, 0xA612, 0xD2AD, 0xC324, 0xF1BF, 0xE036,
    0x18C1, 0x0948, 0x3BD3, 0x2A5A, 0x5EE5, 0x4F6C, 0x7DF7, 0x6C7E,
    0xA50A, 0xB483, 0x8618, 0x9791, 0xE32E, 0xF2A7, 0xC03C, 0xD1B5,
    0x2942, 0x38CB, 0x0A50, 0x1BD9, 0x6F66, 0x7EEF, 0x4C74, 0x5DFD,
    0xB58B, 0xA402, 0x9699, 0x8710, 0xF3AF, 0xE226, 0xD0BD, 0xC134,
    0x39C3, 0x284A, 0x1AD1, 0x0B58, 0x7FE7, 0x6E6E, 0x5CF5, 0x4D7C,
    0xC60C, 0xD785, 0xE51E, 0xF497, 0x8028, 0x91A1, 0xA33A, 0xB2B3,
    0x4A44, 0x5BCD, 0x6956, 0x78DF, 0x0C60, 0x1DE9, 0x2F72, 0x3EFB,
    0xD68D, 0xC704, 0xF59F, 0xE416, 0x90A9, 0x8120, 0xB3BB, 0xA232,
    0x5AC5, 0x4B4C, 0x79D7, 0x685E, 0x1CE1, 0x0D68, 0x3FF3, 0x2E7A,
    0xE70E, 0xF687, 0xC41C, 0xD595, 0xA12A, 0xB0A3, 0x8238, 0x93B1,
    0x6B46, 0x7ACF, 0x4854, 0x59DD, 0x2D62, 0x3CEB, 0x0E70, 0x1FF9,
    0xF78F, 0xE606, 0xD49D, 0xC514, 0xB1AB, 0xA022, 0x92B9, 0x8330,
    0x7BC7, 0x6A4E, 0x58D5, 0x495C, 0x3DE3, 0x2C6A, 0x1EF1, 0x0F78,
)

# CRC-16-MODBUS (reflected 0x8005 -> 0xA001) table  
CRC16_MODBUS_TABLE = tuple([
    0x0000, 0xC0C1, 0xC181, 0x0140, 0xC301, 0x03C0, 0x0280, 0xC241,
    0xC601, 0x06C0, 0x0780, 0xC741, 0x0500, 0xC5C1, 0xC481, 0x0440,
    0xCC01, 0x0CC0, 0x0D80, 0xCD41, 0x0F00, 0xCFC1, 0xCE81, 0x0E40,
    0x0A00, 0xCAC1, 0xCB81, 0x0B40, 0xC901, 0x09C0, 0x0880, 0xC841,
    0xD801, 0x18C0, 0x1980, 0xD941, 0x1B00, 0xDBC1, 0xDA81, 0x1A40,
    0x1E00, 0xDEC1, 0xDF81, 0x1F40, 0xDD01, 0x1DC0, 0x1C80, 0xDC41,
    0x1400, 0xD4C1, 0xD581, 0x1540, 0xD701, 0x17C0, 0x1680, 0xD641,
    0xD201, 0x12C0, 0x1380, 0xD341, 0x1100, 0xD1C1, 0xD081, 0x1040,
    0xF001, 0x30C0, 0x3180, 0xF141, 0x3300, 0xF3C1, 0xF281, 0x3240,
    0x3600, 0xF6C1, 0xF781, 0x3740, 0xF501, 0x35C0, 0x3480, 0xF441,
    0x3C00, 0xFCC1, 0xFD81, 0x3D40, 0xFF01, 0x3FC0, 0x3E80, 0xFE41,
    0xFA01, 0x3AC0, 0x3B80, 0xFB41, 0x3900, 0xF9C1, 0xF881, 0x3840,
    0x2800, 0xE8C1, 0xE981, 0x2940, 0xEB01, 0x2BC0, 0x2A80, 0xEA41,
    0xEE01, 0x2EC0, 0x2F80, 0xEF41, 0x2D00, 0xEDC1, 0xEC81, 0x2C40,
    0xE401, 0x24C0, 0x2580, 0xE541, 0x2700, 0xE7C1, 0xE681, 0x2640,
    0x2200, 0xE2C1, 0xE381, 0x2340, 0xE101, 0x21C0, 0x2080, 0xE041,
    0xA001, 0x60C0, 0x6180, 0xA141, 0x6300, 0xA3C1, 0xA281, 0x6240,
    0x6600, 0xA6C1, 0xA781, 0x6740, 0xA501, 0x65C0, 0x6480, 0xA441,
    0x6C00, 0xACC1, 0xAD81, 0x6D40, 0xAF01, 0x6FC0, 0x6E80, 0xAE41,
    0xAA01, 0x6AC0, 0x6B80, 0xAB41, 0x6900, 0xA9C1, 0xA881, 0x6840,
    0x7800, 0xB8C1, 0xB981, 0x7940, 0xBB01, 0x7BC0, 0x7A80, 0xBA41,
    0xBE01, 0x7EC0, 0x7F80, 0xBF41, 0x7D00, 0xBDC1, 0xBC81, 0x7C40,
    0xB401, 0x74C0, 0x7580, 0xB541, 0x7700, 0xB7C1, 0xB681, 0x7640,
    0x7200, 0xB2C1, 0xB381, 0x7340, 0xB101, 0x71C0, 0x7080, 0xB041,
    0x5000, 0x90C1, 0x9181, 0x5140, 0x9301, 0x53C0, 0x5280, 0x9241,
    0x9601, 0x56C0, 0x5780, 0x9741, 0x5500, 0x95C1, 0x9481, 0x5440,
    0x9C01, 0x5CC0, 0x5D80, 0x9D41, 0x5F00, 0x9FC1, 0x9E81, 0x5E40,
    0x5A00, 0x9AC1, 0x9B81, 0x5B40, 0x9901, 0x59C0, 0x5880, 0x9841,
    0x8801, 0x48C0, 0x4980, 0x8941, 0x4B00, 0x8BC1, 0x8A81, 0x4A40,
    0x4E00, 0x8EC1, 0x8F81, 0x4F40, 0x8D01, 0x4DC0, 0x4C80, 0x8C41,
    0x4400, 0x84C1, 0x8581, 0x4540, 0x8701, 0x47C0, 0x4680, 0x8641,
    0x8201, 0x42C0, 0x4380, 0x8341, 0x4100, 0x81C1, 0x8081, 0x4040,
])

# CRC-8 table (polynomial 0x07)
CRC8_TABLE = tuple([0] + [
    0x07, 0x0E, 0x09, 0x18, 0x1B, 0x1C, 0x15, 0x22, 0x23, 0x24, 0x27,
    0x30, 0x31, 0x36, 0x39, 0x4A, 0x4B, 0x4C, 0x4F, 0x58, 0x59, 0x5E,
    0x63, 0x74, 0x77, 0x78, 0x7D, 0x86, 0x89, 0x8E, 0x93, 0xA4, 0xA7,
    0xA8, 0xAD, 0xB6, 0xB9, 0xBE, 0xC3, 0xD0, 0xD3, 0xD8, 0xDD, 0xE6,
    0xE9, 0xEE, 0xF3, 0
])


# ============================================================================
# CRC Algorithm Definitions
# ============================================================================

CRC_ALGORITHMS: Dict[str, Dict] = {
    'crc-8': {
        'width': 8,
        'poly': 0x07,
        'init': 0x00,
        'refin': False,
        'refout': False,
        'xorout': 0x00,
        'check': 0xF4,
    },
    'crc-8-maxim': {
        'width': 8,
        'poly': 0x31,
        'init': 0x00,
        'refin': True,
        'refout': True,
        'xorout': 0x00,
        'check': 0xA1,
    },
    'crc-16-ibm': {
        'width': 16,
        'poly': 0x8005,
        'init': 0x0000,
        'refin': True,
        'refout': True,
        'xorout': 0x0000,
        'check': 0xBB3D,
    },
    'crc-16-ccitt': {
        'width': 16,
        'poly': 0x1021,
        'init': 0x0000,
        'refin': True,
        'refout': True,
        'xorout': 0x0000,
        'check': 0x2189,
    },
    'crc-16-ccitt-false': {
        'width': 16,
        'poly': 0x1021,
        'init': 0xFFFF,
        'refin': False,
        'refout': False,
        'xorout': 0x0000,
        'check': 0x29B1,
    },
    'crc-16-xmodem': {
        'width': 16,
        'poly': 0x1021,
        'init': 0x0000,
        'refin': False,
        'refout': False,
        'xorout': 0x0000,
        'check': 0x31C3,
    },
    'crc-16-modbus': {
        'width': 16,
        'poly': 0x8005,
        'init': 0xFFFF,
        'refin': True,
        'refout': True,
        'xorout': 0x0000,
        'check': 0x4B37,
    },
    'crc-32': {
        'width': 32,
        'poly': 0x04C11DB7,
        'init': 0xFFFFFFFF,
        'refin': True,
        'refout': True,
        'xorout': 0xFFFFFFFF,
        'check': 0xCBF43926,
    },
    'crc-32c': {
        'width': 32,
        'poly': 0x1EDC6F41,
        'init': 0xFFFFFFFF,
        'refin': True,
        'refout': True,
        'xorout': 0xFFFFFFFF,
        'check': 0xE3069283,
    },
    'crc-32-mpeg': {
        'width': 32,
        'poly': 0x04C11DB7,
        'init': 0xFFFFFFFF,
        'refin': False,
        'refout': False,
        'xorout': 0x00000000,
        'check': 0x0376E6E7,
    },
    'crc-32-bzip2': {
        'width': 32,
        'poly': 0x04C11DB7,
        'init': 0xFFFFFFFF,
        'refin': False,
        'refout': False,
        'xorout': 0xFFFFFFFF,
        'check': 0xFC891918,
    },
    'crc-64-ecma': {
        'width': 64,
        'poly': 0x42F0E1EBA9EA3693,
        'init': 0x0000000000000000,
        'refin': False,
        'refout': False,
        'xorout': 0x0000000000000000,
        'check': 0x6C40DF5F0B497347,
    },
    'crc-64-iso': {
        'width': 64,
        'poly': 0x000000000000001B,
        'init': 0xFFFFFFFFFFFFFFFF,
        'refin': True,
        'refout': True,
        'xorout': 0xFFFFFFFFFFFFFFFF,
        'check': 0xB90956C775A41001,
    },
}


# ============================================================================
# Bit Manipulation Utilities
# ============================================================================

def reflect_bits(value: int, width: int) -> int:
    """
    Reflect (reverse) the bits in a value.
    
    Args:
        value: The value to reflect
        width: The number of bits to reflect
        
    Returns:
        The reflected value
        
    Example:
        >>> reflect_bits(0x31, 8)
        0x8C
        >>> hex(reflect_bits(0x1234, 16))
        '0x2c48'
    """
    result = 0
    for i in range(width):
        if value & (1 << i):
            result |= 1 << (width - 1 - i)
    return result


def reflect_bits_fast(value: int, width: int) -> int:
    """
    Fast bit reflection using byte table.
    
    Args:
        value: The value to reflect
        width: The number of bits to reflect
        
    Returns:
        The reflected value
    """
    BYTE_REFLECT = bytes([
        0x00, 0x80, 0x40, 0xC0, 0x20, 0xA0, 0x60, 0xE0,
        0x10, 0x90, 0x50, 0xD0, 0x30, 0xB0, 0x70, 0xF0,
        0x08, 0x88, 0x48, 0xC8, 0x28, 0xA8, 0x68, 0xE8,
        0x18, 0x98, 0x58, 0xD8, 0x38, 0xB8, 0x78, 0xF8,
        0x04, 0x84, 0x44, 0xC4, 0x24, 0xA4, 0x64, 0xE4,
        0x14, 0x94, 0x54, 0xD4, 0x34, 0xB4, 0x74, 0xF4,
        0x0C, 0x8C, 0x4C, 0xCC, 0x2C, 0xAC, 0x6C, 0xEC,
        0x1C, 0x9C, 0x5C, 0xDC, 0x3C, 0xBC, 0x7C, 0xFC,
        0x02, 0x82, 0x42, 0xC2, 0x22, 0xA2, 0x62, 0xE2,
        0x12, 0x92, 0x52, 0xD2, 0x32, 0xB2, 0x72, 0xF2,
        0x0A, 0x8A, 0x4A, 0xCA, 0x2A, 0xAA, 0x6A, 0xEA,
        0x1A, 0x9A, 0x5A, 0xDA, 0x3A, 0xBA, 0x7A, 0xFA,
        0x06, 0x86, 0x46, 0xC6, 0x26, 0xA6, 0x66, 0xE6,
        0x16, 0x96, 0x56, 0xD6, 0x36, 0xB6, 0x76, 0xF6,
        0x0E, 0x8E, 0x4E, 0xCE, 0x2E, 0xAE, 0x6E, 0xEE,
        0x1E, 0x9E, 0x5E, 0xDE, 0x3E, 0xBE, 0x7E, 0xFE,
        0x01, 0x81, 0x41, 0xC1, 0x21, 0xA1, 0x61, 0xE1,
        0x11, 0x91, 0x51, 0xD1, 0x31, 0xB1, 0x71, 0xF1,
        0x09, 0x89, 0x49, 0xC9, 0x29, 0xA9, 0x69, 0xE9,
        0x19, 0x99, 0x59, 0xD9, 0x39, 0xB9, 0x79, 0xF9,
        0x05, 0x85, 0x45, 0xC5, 0x25, 0xA5, 0x65, 0xE5,
        0x15, 0x95, 0x55, 0xD5, 0x35, 0xB5, 0x75, 0xF5,
        0x0D, 0x8D, 0x4D, 0xCD, 0x2D, 0xAD, 0x6D, 0xED,
        0x1D, 0x9D, 0x5D, 0xDD, 0x3D, 0xBD, 0x7D, 0xFD,
        0x03, 0x83, 0x43, 0xC3, 0x23, 0xA3, 0x63, 0xE3,
        0x13, 0x93, 0x53, 0xD3, 0x33, 0xB3, 0x73, 0xF3,
        0x0B, 0x8B, 0x4B, 0xCB, 0x2B, 0xAB, 0x6B, 0xEB,
        0x1B, 0x9B, 0x5B, 0xDB, 0x3B, 0xBB, 0x7B, 0xFB,
        0x07, 0x87, 0x47, 0xC7, 0x27, 0xA7, 0x67, 0xE7,
        0x17, 0x97, 0x57, 0xD7, 0x37, 0xB7, 0x77, 0xF7,
        0x0F, 0x8F, 0x4F, 0xCF, 0x2F, 0xAF, 0x6F, 0xEF,
        0x1F, 0x9F, 0x5F, 0xDF, 0x3F, 0xBF, 0x7F, 0xFF,
    ])
    
    if width == 8:
        return BYTE_REFLECT[value & 0xFF]
    elif width == 16:
        return (BYTE_REFLECT[value & 0xFF] << 8) | BYTE_REFLECT[(value >> 8) & 0xFF]
    elif width == 32:
        return (BYTE_REFLECT[value & 0xFF] << 24) | \
               (BYTE_REFLECT[(value >> 8) & 0xFF] << 16) | \
               (BYTE_REFLECT[(value >> 16) & 0xFF] << 8) | \
               BYTE_REFLECT[(value >> 24) & 0xFF]
    elif width == 64:
        return (BYTE_REFLECT[value & 0xFF] << 56) | \
               (BYTE_REFLECT[(value >> 8) & 0xFF] << 48) | \
               (BYTE_REFLECT[(value >> 16) & 0xFF] << 40) | \
               (BYTE_REFLECT[(value >> 24) & 0xFF] << 32) | \
               (BYTE_REFLECT[(value >> 32) & 0xFF] << 24) | \
               (BYTE_REFLECT[(value >> 40) & 0xFF] << 16) | \
               (BYTE_REFLECT[(value >> 48) & 0xFF] << 8) | \
               BYTE_REFLECT[(value >> 56) & 0xFF]
    else:
        return reflect_bits(value, width)


# ============================================================================
# Core CRC Functions
# ============================================================================

def crc32(data: BytesLike) -> int:
    """
    Compute CRC-32 checksum (compatible with zlib.crc32).
    
    Args:
        data: Data to process
        
    Returns:
        CRC-32 checksum (unsigned 32-bit integer)
        
    Example:
        >>> crc32(b'Hello, World!')
        3964322768
        >>> hex(crc32(b'123456789'))
        '0xcbf43926'
    """
    if isinstance(data, str):
        data = data.encode('utf-8')
    
    crc = 0xFFFFFFFF
    for byte in data:
        crc = (crc >> 8) ^ CRC32_TABLE[(crc ^ byte) & 0xFF]
    return crc ^ 0xFFFFFFFF


def crc16_ccitt(data: BytesLike) -> int:
    """
    Compute CRC-16-CCITT checksum (reflected variant).
    
    Args:
        data: Data to process
        
    Returns:
        CRC-16-CCITT checksum
        
    Example:
        >>> crc16_ccitt(b'123456789')
        8585
    """
    if isinstance(data, str):
        data = data.encode('utf-8')
    
    crc = 0x0000
    poly_reflected = 0x8408  # Reflected 0x1021
    for byte in data:
        crc = (crc >> 8) ^ CRC16_CCITT_TABLE[(crc ^ byte) & 0xFF]
    return crc


def crc16_modbus(data: BytesLike) -> int:
    """
    Compute CRC-16-MODBUS checksum.
    
    Args:
        data: Data to process
        
    Returns:
        CRC-16-MODBUS checksum
        
    Example:
        >>> hex(crc16_modbus(b'123456789'))
        '0x4b37'
    """
    if isinstance(data, str):
        data = data.encode('utf-8')
    
    crc = 0xFFFF
    for byte in data:
        crc = (crc >> 8) ^ CRC16_MODBUS_TABLE[(crc ^ byte) & 0xFF]
    return crc


def crc16(data: BytesLike, poly: int = 0x1021, init: int = 0xFFFF) -> int:
    """
    Compute CRC-16 checksum (non-reflected).
    
    Args:
        data: Data to process
        poly: Polynomial (default: 0x1021 for CCITT)
        init: Initial value (default: 0xFFFF)
        
    Returns:
        CRC-16 checksum
        
    Example:
        >>> hex(crc16(b'123456789'))
        '0x29b1'
    """
    if isinstance(data, str):
        data = data.encode('utf-8')
    
    crc = init
    for byte in data:
        crc ^= (byte << 8)
        for _ in range(8):
            if crc & 0x8000:
                crc = ((crc << 1) ^ poly) & 0xFFFF
            else:
                crc = (crc << 1) & 0xFFFF
    return crc


def crc8(data: BytesLike) -> int:
    """
    Compute CRC-8 checksum.
    
    Args:
        data: Data to process
        
    Returns:
        CRC-8 checksum
        
    Example:
        >>> crc8(b'123456789')
        244
    """
    if isinstance(data, str):
        data = data.encode('utf-8')
    
    crc = 0x00
    for byte in data:
        crc ^= byte
        for _ in range(8):
            if crc & 0x80:
                crc = ((crc << 1) ^ 0x07) & 0xFF
            else:
                crc = (crc << 1) & 0xFF
    return crc


def crc64(data: BytesLike) -> int:
    """
    Compute CRC-64-ECMA checksum.
    
    Args:
        data: Data to process
        
    Returns:
        CRC-64 checksum
        
    Example:
        >>> hex(crc64(b'123456789'))
        '0x6c40df5f0b497347'
    """
    if isinstance(data, str):
        data = data.encode('utf-8')
    
    crc = 0x0000000000000000
    poly = 0x42F0E1EBA9EA3693
    
    for byte in data:
        crc ^= (byte << 56)
        for _ in range(8):
            if crc & 0x8000000000000000:
                crc = ((crc << 1) ^ poly) & 0xFFFFFFFFFFFFFFFF
            else:
                crc = (crc << 1) & 0xFFFFFFFFFFFFFFFF
    return crc


def _compute_table_entry_reflected(poly_ref: int, width: int, index: int) -> int:
    """Compute reflected table entry."""
    crc = index
    mask = (1 << width) - 1
    for _ in range(8):
        if crc & 1:
            crc = (crc >> 1) ^ poly_ref
        else:
            crc = crc >> 1
    return crc & mask


# ============================================================================
# CRC Class
# ============================================================================

class CRC:
    """
    CRC calculator class supporting multiple algorithms.
    
    Example:
        >>> crc = CRC('crc-32')
        >>> crc.update(b'Hello, World!').hexdigest()
        'ec4ac3d0'
    """
    
    def __init__(self, algorithm: str = 'crc-32'):
        """
        Initialize CRC calculator with specified algorithm.
        
        Args:
            algorithm: Name of the CRC algorithm
        """
        algo_lower = algorithm.lower()
        if algo_lower not in CRC_ALGORITHMS:
            available = ', '.join(sorted(CRC_ALGORITHMS.keys()))
            raise ValueError(f"Unknown algorithm '{algorithm}'. Available: {available}")
        
        self._algo_name = algo_lower
        self._config = CRC_ALGORITHMS[self._algo_name]
        self._width = self._config['width']
        self._poly = self._config['poly']
        self._init = self._config['init']
        self._refin = self._config['refin']
        self._refout = self._config['refout']
        self._xorout = self._config['xorout']
        
        self._crc = self._init
        self._mask = (1 << self._width) - 1
    
    @property
    def width(self) -> int:
        return self._width
    
    @property
    def algorithm(self) -> str:
        return self._algo_name
    
    @property
    def polynomial(self) -> int:
        return self._poly
    
    def update(self, data: BytesLike) -> 'CRC':
        """Update CRC with new data."""
        if isinstance(data, str):
            data = data.encode('utf-8')
        
        if self._algo_name == 'crc-32':
            # Use optimized CRC32 table
            for byte in data:
                self._crc = (self._crc >> 8) ^ CRC32_TABLE[(self._crc ^ byte) & 0xFF]
        elif self._algo_name == 'crc-16-ccitt':
            # Use optimized CRC16-CCITT table
            for byte in data:
                self._crc = (self._crc >> 8) ^ CRC16_CCITT_TABLE[(self._crc ^ byte) & 0xFF]
        elif self._algo_name == 'crc-16-modbus':
            # Use optimized CRC16-MODBUS table
            for byte in data:
                self._crc = (self._crc >> 8) ^ CRC16_MODBUS_TABLE[(self._crc ^ byte) & 0xFF]
        elif self._refin:
            # Generic reflected CRC
            poly_ref = reflect_bits(self._poly, self._width)
            for byte in data:
                index = (self._crc ^ byte) & 0xFF
                self._crc = (self._crc >> 8) ^ _compute_table_entry_reflected(poly_ref, self._width, index)
        else:
            # Non-reflected CRC
            shift = self._width - 8
            for byte in data:
                self._crc ^= (byte << shift)
                for _ in range(8):
                    if self._crc & (1 << (self._width - 1)):
                        self._crc = ((self._crc << 1) ^ self._poly) & self._mask
                    else:
                        self._crc = (self._crc << 1) & self._mask
        
        return self
    
    @property
    def value(self) -> int:
        return self._crc
    
    @property
    def digest(self) -> int:
        crc = self._crc
        # For reflected algorithms (refin=True), we've already processed LSB-first
        # The refout flag in standard CRC notation means to reflect the output
        # But when we use reflected calculation, we don't need to reflect again
        # However, we need to handle non-reflected algorithms that still have refout=True
        if self._refout and not self._refin:
            crc = reflect_bits(crc, self._width)
        return crc ^ self._xorout
    
    def hexdigest(self) -> str:
        width_bytes = (self._width + 7) // 8
        return format(self.digest, f'0{width_bytes * 2}x')
    
    def bytesdigest(self) -> bytes:
        width_bytes = (self._width + 7) // 8
        if self._width == 8:
            return bytes([self.digest])
        elif self._width == 16:
            return struct.pack('>H', self.digest)
        elif self._width == 32:
            return struct.pack('>I', self.digest)
        elif self._width == 64:
            return struct.pack('>Q', self.digest)
        else:
            return self.digest.to_bytes(width_bytes, 'big')
    
    def reset(self) -> 'CRC':
        self._crc = self._init
        return self
    
    def copy(self) -> 'CRC':
        new_crc = CRC(self._algo_name)
        new_crc._crc = self._crc
        return new_crc
    
    def verify(self, data: BytesLike, expected: Union[int, str, bytes]) -> bool:
        self.reset()
        self.update(data)
        
        if isinstance(expected, int):
            return self.digest == expected
        elif isinstance(expected, str):
            return self.hexdigest().upper() == expected.upper().lstrip('0x')
        elif isinstance(expected, bytes):
            return self.bytesdigest() == expected
        return False
    
    # Static methods
    @staticmethod
    def crc8(data: BytesLike) -> int:
        return crc8(data)
    
    @staticmethod
    def crc16(data: BytesLike) -> int:
        return crc16(data)
    
    @staticmethod
    def crc32(data: BytesLike) -> int:
        return crc32(data)
    
    @staticmethod
    def crc64(data: BytesLike) -> int:
        return crc64(data)
    
    @staticmethod
    def compute(algorithm: str, data: BytesLike) -> int:
        crc = CRC(algorithm)
        crc.update(data)
        return crc.digest
    
    @staticmethod
    def compute_hex(algorithm: str, data: BytesLike) -> str:
        crc = CRC(algorithm)
        crc.update(data)
        return crc.hexdigest()


# ============================================================================
# File CRC Utilities
# ============================================================================

def file_crc(file_path: str, algorithm: str = 'crc-32', 
             chunk_size: int = 65536) -> Tuple[int, str]:
    """
    Compute CRC of a file.
    
    Args:
        file_path: Path to the file
        algorithm: CRC algorithm to use
        chunk_size: Size of chunks to read
        
    Returns:
        Tuple of (crc_value, hex_string)
    """
    crc = CRC(algorithm)
    
    with open(file_path, 'rb') as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            crc.update(chunk)
    
    return crc.digest, crc.hexdigest()


def verify_file_crc(file_path: str, expected: Union[int, str],
                    algorithm: str = 'crc-32') -> bool:
    """Verify file CRC against expected value."""
    crc = CRC(algorithm)
    
    with open(file_path, 'rb') as f:
        while True:
            chunk = f.read(65536)
            if not chunk:
                break
            crc.update(chunk)
    
    if isinstance(expected, int):
        return crc.digest == expected
    else:
        expected_clean = expected.upper().lstrip('0x')
        return crc.hexdigest().upper() == expected_clean


# ============================================================================
# Data Integrity Utilities
# ============================================================================

def compute_checksum(data: BytesLike, algorithm: str = 'crc-32') -> str:
    """Compute CRC checksum as hex string."""
    return CRC.compute_hex(algorithm, data)


def verify_checksum(data: BytesLike, checksum: str,
                    algorithm: str = 'crc-32') -> bool:
    """Verify data against CRC checksum."""
    checksum_clean = checksum.upper().lstrip('0x')
    return compute_checksum(data, algorithm).upper() == checksum_clean


# ============================================================================
# Custom CRC Support
# ============================================================================

def custom_crc(data: BytesLike, width: int, poly: int,
               init: int = 0, refin: bool = False, 
               refout: bool = False, xorout: int = 0) -> int:
    """
    Compute CRC with custom parameters.
    
    Args:
        data: Data to process
        width: CRC width in bits
        poly: Polynomial
        init: Initial CRC value
        refin: Reflect input bits
        refout: Reflect output bits
        xorout: Final XOR value
        
    Returns:
        CRC digest
    """
    if isinstance(data, str):
        data = data.encode('utf-8')
    
    mask = (1 << width) - 1
    crc = init
    
    if refin:
        poly_ref = reflect_bits(poly, width)
        for byte in data:
            crc = (crc >> 8) ^ _compute_ref_table_entry(poly_ref, width, (crc ^ byte) & 0xFF)
    else:
        shift = width - 8
        for byte in data:
            crc ^= (byte << shift)
            for _ in range(8):
                if crc & (1 << (width - 1)):
                    crc = ((crc << 1) ^ poly) & mask
                else:
                    crc = (crc << 1) & mask
    
    if refout:
        crc = reflect_bits(crc, width)
    
    return crc ^ xorout


def _compute_ref_table_entry(poly_ref: int, width: int, index: int) -> int:
    """Compute reflected table entry."""
    crc = index
    mask = (1 << width) - 1
    for _ in range(8):
        if crc & 1:
            crc = (crc >> 1) ^ poly_ref
        else:
            crc = crc >> 1
    return crc & mask


# ============================================================================
# Utility Functions
# ============================================================================

def generate_crc_table(poly: int, width: int) -> Tuple[int, ...]:
    """Generate CRC lookup table."""
    table = []
    msb_mask = 1 << (width - 1)
    full_mask = (1 << width) - 1
    
    for byte in range(256):
        crc = byte << (width - 8)
        for _ in range(8):
            if crc & msb_mask:
                crc = ((crc << 1) ^ poly) & full_mask
            else:
                crc = (crc << 1) & full_mask
        table.append(crc)
    
    return tuple(table)


def list_algorithms() -> list:
    """List all available CRC algorithms."""
    return sorted(CRC_ALGORITHMS.keys())


def get_algorithm_info(algorithm: str) -> Dict:
    """Get information about a CRC algorithm."""
    algo = algorithm.lower()
    if algo not in CRC_ALGORITHMS:
        available = ', '.join(sorted(CRC_ALGORITHMS.keys()))
        raise ValueError(f"Unknown algorithm '{algorithm}'. Available: {available}")
    
    config = CRC_ALGORITHMS[algo].copy()
    config['name'] = algo
    return config


def compute_multiple(algorithms: list, data: BytesLike) -> Dict[str, int]:
    """Compute multiple CRC algorithms on the same data."""
    results = {}
    for algo in algorithms:
        try:
            results[algo] = CRC.compute(algo, data)
        except ValueError as e:
            results[algo] = str(e)
    return results


# ============================================================================
# Exports
# ============================================================================

__all__ = [
    'CRC',
    'crc8',
    'crc16',
    'crc16_ccitt',
    'crc16_modbus',
    'crc32',
    'crc64',
    'file_crc',
    'verify_file_crc',
    'compute_checksum',
    'verify_checksum',
    'custom_crc',
    'reflect_bits',
    'reflect_bits_fast',
    'generate_crc_table',
    'list_algorithms',
    'get_algorithm_info',
    'compute_multiple',
    'CRC_ALGORITHMS',
]