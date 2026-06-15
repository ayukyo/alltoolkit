# Riddle Utils 🧩

谜语工具库，提供谜语存储、获取、提示和答案验证功能。

## 特性

- ✅ **内置谜语库** - 中英文谜语，按类别分类
- ✅ **随机获取** - 获取随机谜语
- ✅ **渐进提示** - 渐进式提示系统
- ✅ **模糊匹配** - 答案验证支持模糊匹配
- ✅ **谜语生成** - 基于规则的谜语生成
- ✅ **零依赖** - 仅使用 Python 标准库

## 快速开始

```python
from riddle_utils import RiddleManager

manager = RiddleManager()

# 获取随机谜语
riddle = manager.get_random()
print(riddle.question)

# 获取提示
hint = riddle.get_hint(1)  # 第一级提示
print(hint)

# 验证答案
is_correct = manager.check_answer(riddle.id, "答案")
print(is_correct)
```

## API 参考

| 类/函数 | 说明 |
|---------|------|
| `RiddleManager` | 谜语管理器 |
| `Riddle` | 谜语类 |
| `RiddleGenerator` | 谜语生成器 |
| `RiddleCategory` | 谜语分类枚举 |
| `RiddleDifficulty` | 难度枚举 |
