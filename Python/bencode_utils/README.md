# Bencode Utils


AllToolkit - Python Bencode Utilities

A zero-dependency, production-ready Bencode encoding/decoding utility module.
Bencode is the encoding format used by the BitTorrent protocol.

Supports:
- String encoding/decoding
- Integer encoding/decoding
- List encoding/decoding
- Dictionary encoding/decoding
- Nested structures
- File I/O operations
- Torrent file parsing (basic .torrent file support)

Author: AllToolkit
License: MIT


## 功能

### 类

- **BencodeError**: Base exception for bencode operations
- **BencodeEncodeError**: Error during encoding
- **BencodeDecodeError**: Error during decoding
- **BencodeTypeError**: Invalid type for bencode operation
- **Bencoder**: Bencode encoder/decoder class
  方法: encode, decode, decode_to_str_dict, encode_to_file, decode_file ... (9 个方法)

### 函数

- **encode(data**) - Encode data to bencode format.
- **decode(data**) - Decode bencode data.
- **decode_to_str_dict(data**) - Decode bencode data to dictionary with string keys.
- **encode_to_file(data, filepath**) - Encode data and write to file.
- **decode_file(filepath**) - Decode a bencode file.
- **decode_file_to_str_dict(filepath**) - Decode a bencode file to dictionary with string keys.
- **parse_torrent_info(filepath**) - Parse basic info from a .torrent file.
- **get_torrent_files(filepath**) - Get list of files in a torrent.
- **get_torrent_total_size(filepath**) - Get total size of files in a torrent.
- **bencode_size(data**) - Calculate the size of encoded data without actually encoding.

... 共 23 个函数

## 使用示例

```python
from mod import encode

# 使用 encode
result = encode()
```

## 测试

运行测试：

```bash
python *_test.py
```

## 文件结构

```
{module_name}/
├── mod.py              # 主模块
├── *_test.py           # 测试文件
├── README.md           # 本文档
└── examples/           # 示例代码
    └── usage_examples.py
```

---

**Last updated**: 2026-04-28
