# Captcha Utils - CAPTCHA 生成与验证工具模块

提供文本验证码、ASCII 艺术 CAPTCHA、数学验证码、图像 CAPTCHA 生成功能。零外部依赖核心实现，可选 Pillow 支持图像生成。

## 功能概览

| 功能模块 | 描述 |
|---------|------|
| 文本验证码 | 纯文本验证码生成（数字、字母、混合） |
| ASCII 艺术 | 无外部依赖的 ASCII 艺术验证码 |
| 数学验证码 | 算术运算验证码（加减乘除） |
| 反序验证码 | 反序输入验证码 |
| 图像验证码 | Pillow 支持的图像验证码（可选） |
| 混合验证码 | 随机类型验证码生成 |
| 验证码存储 | 内存存储与自动清理 |
| 批量生成 | 批量验证码生成 |

## 安装使用

```python
from captcha_utils import (
    CaptchaGenerator, CaptchaStore,
    generate_captcha, verify_captcha,
    CaptchaType, CaptchaDifficulty, CaptchaCharset
)

# 快捷生成
captcha = generate_captcha()
print(captcha.captcha)
print(f"答案: {captcha.text}")
```

## 详细功能

### 文本验证码

```python
# 纯文本验证码
gen = CaptchaGenerator()
captcha = gen.generate_text_captcha(
    length=6,
    charset=CaptchaCharset.DIGITS,  # 纯数字
    difficulty=CaptchaDifficulty.MEDIUM,
    expires_in=300.0  # 5分钟过期
)

# charset 类型:
# - DIGITS: 纯数字 (0-9)
# - LOWERCASE: 小写字母 (a-z)
# - UPPERCASE: 大写字母 (A-Z)
# - ALPHANUMERIC: 数字+大写字母
# - MIXED: 数字+大小写字母

# 验证
is_correct = captcha.verify("123456")
```

### ASCII 艺术验证码

```python
# ASCII 艺术验证码（无外部依赖）
captcha = gen.generate_ascii_captcha(
    length=4,
    charset=CaptchaCharset.ALPHANUMERIC,
    difficulty=CaptchaDifficulty.MEDIUM,
    simple_style=False,  # False 使用方块风格，True 使用线条风格
    add_noise=True  # 添加噪声
)

print(captcha.captcha)
# 输出类似:
# ████
# ██    ██
# ██████
# ...

# 答案
print(captcha.text)  # 如 'A3B7'
```

### 不同难度效果

| 难度 | 长度 | 噪声 | 干扰线 |
|-----|-----|-----|-------|
| EASY | 4 | 5% | 无 |
| MEDIUM | 6 | 15% | 无 |
| HARD | 8 | 25% | 有 |
| EXTREME | 8 | 35% | 有 |

### 数学验证码

```python
# 数学验证码
captcha = gen.generate_math_captcha(
    difficulty=CaptchaDifficulty.MEDIUM,
    max_answer=100
)

print(captcha.question)  # 如 '3 + 7 = ?'
print(captcha.answer)    # 10

# 验证（支持数字或字符串）
is_correct = captcha.verify(10)
is_correct = captcha.verify("10")
```

### 反序验证码

```python
# 反序验证码
captcha = gen.generate_reverse_captcha(
    length=6,
    charset=CaptchaCharset.DIGITS
)

print(captcha.captcha)  # 显示 '请输入反转后的文本: 1234'
print(captcha.text)     # 答案是 '4321'
```

### 图像验证码（需要 Pillow）

```python
# 图像验证码
captcha = gen.generate_image_captcha(
    length=4,
    difficulty=CaptchaDifficulty.HARD,
    width=200,
    height=80,
    output_format='base64'  # 输出 Base64 编码
)

# captcha.captcha 是 Base64 编码的 PNG 图像
# 可用于网页: <img src="data:image/png;base64,{captcha.captcha}">
```

### 混合验证码

```python
# 随机类型验证码
captcha = gen.generate_mixed_captcha()
# 可能返回任意类型: TEXT, ASCII_ART, MATH, REVERSE
```

### 验证码存储

```python
# 使用存储器
store = CaptchaStore(max_size=1000)

# 生成并存储
captcha_id = "user_123_captcha"
captcha = gen.generate_ascii_captcha()
store.store(captcha_id, captcha)

# 验证
is_valid = store.verify(captcha_id, "A3B7", case_sensitive=False)

# 获取
stored = store.get(captcha_id)

# 清理
store.clear()
```

### 批量生成

```python
# 批量生成验证码
captchas = generate_batch_captchas(
    count=10,
    captcha_type=CaptchaType.ASCII_ART,
    difficulty=CaptchaDifficulty.MEDIUM
)
```

### 快捷函数

```python
# 快捷生成
captcha = generate_captcha(
    captcha_type=CaptchaType.ASCII_ART,
    difficulty=CaptchaDifficulty.MEDIUM
)

# 快捷存储与验证
captcha = create_and_store_captcha("session_123")
is_valid = verify_captcha("session_123", "用户输入")
```

## 数据类

### CaptchaResult

```python
captcha = generate_captcha()

# 属性
captcha.text              # 验证码文本（答案）
captcha.captcha           # 验证码内容
captcha.captcha_type      # 类型（CaptchaType）
captcha.difficulty        # 难度（CaptchaDifficulty）
captcha.timestamp         # 生成时间戳
captcha.expires_in        # 过期时间（秒）
captcha.hash              # 验证哈希

# 方法
captcha.is_expired()      # 是否过期
captcha.verify("input")   # 验证用户输入
captcha.to_dict()         # 转换为字典
```

### MathCaptchaResult

```python
captcha = generate_captcha(CaptchaType.MATH)

# 属性
captcha.question          # 问题文本
captcha.answer            # 答案（整数）
captcha.captcha           # ASCII 艺术问题
captcha.captcha_type      # MATH

# 方法
captcha.verify(10)        # 验证答案（数字或字符串）
```

## 测试

```bash
python captcha_utils_test.py
```

测试覆盖:
- 文本验证码生成（不同长度、字符集、难度）
- ASCII 艺术验证码（标准风格、简化风格、噪声、干扰线）
- 数学验证码（加减乘除、不同难度）
- 反序验证码生成与验证
- 图像验证码（Pillow 可用时）
- 混合验证码随机生成
- 验证码存储与验证
- 过期检查与自动清理
- 批量生成
- 边界值处理

## 应用场景

- 网站登录/注册验证码
- API 接口防滥用
- CLI/TUI 程序验证
- 终端应用验证码
- 验证码教学演示
- 安全测试

## 设计说明

### 零依赖核心

核心功能（文本、ASCII 艺术、数学、反序验证码）完全使用 Python 标准库实现：
- 无需安装 Pillow
- 无需安装任何第三方库
- 适合受限环境使用

### ASCII 艺术风格

提供两种风格：
- **方块风格**: 使用 █ 字符，视觉效果更醒目
- **线条风格**: 使用 ╭╮╰╯│─ 等字符，更简洁

### 噪声与干扰

根据难度自动添加：
- 随机噪声点（░▒▓·∙•○●）
- 干扰线（─━┄┅╌╍）
- HARD 和 EXTREME 难度添加干扰线

### 数学验证码

支持四种运算：
- **EASY/MEDIUM**: 加法和减法
- **HARD/EXTREME**: 加减乘除（乘法限制范围确保答案合理）

## 许可证

MIT License - 详见项目 LICENSE 文件

---

**作者**: AllToolkit  
**日期**: 2026-05-15