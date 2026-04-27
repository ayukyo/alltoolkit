# Mime Utils


MIME 类型工具模块
================

提供 MIME 类型的查询、检测和判断功能。
零外部依赖，纯 Python 实现。

功能：
- 根据文件扩展名获取 MIME 类型
- 根据 MIME 类型获取文件扩展名
- 判断文件类型（图片、视频、音频、文档、压缩包等）
- 通过魔数（Magic Bytes）检测文件真实 MIME 类型
- 生成安全的 Content-Disposition 头


## 功能

### 类

- **MimeTypeDetector**: MIME 类型检测器类

提供链式调用和缓存功能
  方法: detect, detect_file, clear_cache

### 函数

- **get_mime_type(extension, default**) - 根据文件扩展名获取 MIME 类型
- **get_extensions(mime_type**) - 根据 MIME 类型获取文件扩展名列表
- **get_primary_extension(mime_type, default**) - 根据 MIME 类型获取首选扩展名
- **detect_mime_from_content(data, default**) - 通过魔数（Magic Bytes）检测文件的 MIME 类型
- **detect_mime_from_file(file_path, default**) - 通过读取文件内容检测 MIME 类型
- **detect_mime_from_fileobj(file_obj, default**) - 通过读取文件对象检测 MIME 类型
- **is_image(mime_type**) - 判断是否为图片类型
- **is_video(mime_type**) - 判断是否为视频类型
- **is_audio(mime_type**) - 判断是否为音频类型
- **is_document(mime_type**) - 判断是否为文档类型

... 共 25 个函数

## 使用示例

```python
from mod import get_mime_type

# 使用 get_mime_type
result = get_mime_type()
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
