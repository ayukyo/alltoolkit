# nickname_generator_utils - 昵称生成器工具集

多风格昵称生成、用户名建议、游戏ID生成等功能。零外部依赖，纯 Python 标准库实现。

## 功能列表

| 类名 | 功能 | 适用场景 |
|------|------|----------|
| `NicknameGenerator` | 多风格昵称生成 | 社交平台、即时通讯 |
| `UsernameGenerator` | 用户名生成（格式规范） | 账号注册、系统登录名 |
| `GameIdGenerator` | 游戏ID生成 | 游戏平台昵称 |
| `PetNameGenerator` | 宠物名字生成 | 宠物命名 |
| `TeamNameGenerator` | 团队/小组名称生成 | 团队、工作室、小组 |
| `FantasyNameGenerator` | 奇幻角色名生成 | 小说、游戏角色 |

## 支持风格

- **可爱风格** (`CUTE`) - 软萌、甜美
- **酷炫风格** (`COOL`) - 霸气、炫酷
- **搞笑风格** (`FUNNY`) - 逗比、沙雕
- **神秘风格** (`MYSTIC`) - 暗影、幽深
- **英雄风格** (`HEROIC`) - 王者、传奇
- **自然风格** (`NATURE`) - 清新、淡雅
- **科技风格** (`TECH`) - 智能、极速
- **美食风格** (`FOOD`) - 美味、香甜
- **奇幻风格** (`FANTASY`) - 魔幻、玄幻
- **中文风格** (`CHINESE`) - 古风、诗意
- **简约风格** (`MINIMAL`) - 简单、精致

## 快速使用

```python
from nickname_generator_utils.mod import (
    generate_nickname,
    generate_username,
    generate_game_id,
    generate_pet_name,
    generate_team_name,
    generate_fantasy_name,
    NicknameGenerator,
    NameStyle
)

# 快速生成昵称
nickname = generate_nickname(style="可爱", language="chinese")
print(nickname)  # 例如: "萌萌小猫"

# 指定风格生成
gen = NicknameGenerator(seed=42)  # 可选随机种子
names = gen.generate(NameStyle.COOL, language="english", count=5)
for name in names:
    print(name.name)  # 例如: "ShadowKing", "DarkBlade"

# 生成用户名
username = generate_username(base="张三")
print(username)  # 例如: "zhangsan42"

# 生成游戏ID
game_id = generate_game_id(game_type="moba")
print(game_id)  # 例如: "HeroWarrior88"

# 生成宠物名
pet_name = generate_pet_name(pet_type="cat")
print(pet_name)  # 例如: "咪咪", "奶茶"

# 生成团队名
team_name = generate_team_name(team_type="tech")
print(team_name)  # 例如: "智能实验室", "DigitalLab"

# 生成奇幻角色名
fantasy_name = generate_fantasy_name(race="elven")
print(fantasy_name)  # 例如: "Aeldriel", "Elrion"
```

## 详细示例

### 昵称生成器

```python
from nickname_generator_utils.mod import NicknameGenerator, NameStyle

gen = NicknameGenerator()

# 生成中文可爱风格昵称
cute_names = gen.generate(NameStyle.CUTE, "chinese", count=3)
for name in cute_names:
    print(f"昵称: {name.name}")
    print(f"含义: {name.meaning}")
    print(f"变体: {name.alternatives}")

# 生成英文酷炫风格昵称
cool_names = gen.generate(NameStyle.COOL, "english", count=3)

# 生成混合风格
mixed_names = gen.generate_mixed(count=5)

# 带前缀/后缀
special_name = gen.generate_with_prefix_suffix(NameStyle.MYSTIC, "english")
print(special_name.name)  # 例如: "ShadowWalker", "PhantomHunter"
```

### 用户名生成器

```python
from nickname_generator_utils.mod import UsernameGenerator

gen = UsernameGenerator()

# 基于基础名生成
usernames = gen.generate(base_name="John", use_numbers=True, count=5)
print(usernames)  # 例如: ["John42", "John_007", "John123", ...]

# 随机生成
random_names = gen.generate(min_length=6, max_length=20, use_numbers=True)

# 格式验证
is_valid, errors = gen.check_availability_format("john_123")
print(f"有效: {is_valid}, 问题: {errors}")
```

### 游戏ID生成器

```python
from nickname_generator_utils.mod import GameIdGenerator

gen = GameIdGenerator()

# 不同游戏类型
fps_ids = gen.generate(game_type="fps", count=3)      # 第一人称射击
moba_ids = gen.generate(game_type="moba", count=3)    # MOBA游戏
mmorpg_ids = gen.generate(game_type="mmorpg", count=3) # MMORPG

# 带战队前缀
clan_ids = gen.generate(game_type="fps", include_clan=True, clan_name="ProTeam")
print(clan_ids)  # 例如: ["[ProTeam]ShadowKing", ...]
```

### 宠物名字生成器

```python
from nickname_generator_utils.mod import PetNameGenerator

gen = PetNameGenerator()

# 不同宠物类型
dog_names = gen.generate(pet_type="dog", language="chinese")
cat_names = gen.generate(pet_type="cat", language="english")
bird_names = gen.generate(pet_type="bird")

# 可爱组合名
cute_names = gen.generate_cute_combo(count=5)
print(cute_names)  # 例如: ["甜蜜布丁", "软软奶茶", ...]
```

### 团队名称生成器

```python
from nickname_generator_utils.mod import TeamNameGenerator

gen = TeamNameGenerator()

# 不同团队类型
tech_teams = gen.generate(team_type="tech")      # 科技团队
creative_teams = gen.generate(team_type="creative")  # 创意工作室
gaming_teams = gen.generate(team_type="gaming")   # 游戏战队

# 带领导者名字
team_with_leader = gen.generate_with_name("张三", "tech")
print(team_with_leader)  # 例如: ["张三实验室", "张三的实验室"]
```

### 奇幻角色名生成器

```python
from nickname_generator_utils.mod import FantasyNameGenerator

gen = FantasyNameGenerator()

# 不同种族
elven_names = gen.generate(race="elven")      # 精灵族
dwarven_names = gen.generate(race="dwarven")  #矮人族
angelic_names = gen.generate(race="angelic")  # 天使族

# 中文奇幻名
chinese_fantasy = gen.generate(race="elven", language="chinese")
print(chinese_fantasy)  # 例如: ["龙傲剑", "凤凌心", ...]

# 全名（名+姓）
full_name = gen.generate_full_name(race="elven")
print(full_name)  # 例如: "Aeldriel Elrion"
```

## API 参考

### NicknameGenerator

| 方法 | 参数 | 返回值 | 说明 |
|------|------|--------|------|
| `generate(style, language, count)` | 风格、语言、数量 | `List[GeneratedName]` | 生成昵称 |
| `generate_mixed(count)` | 数量 | `List[GeneratedName]` | 生成混合风格昵称 |
| `generate_with_prefix_suffix(style, language)` | 风格、语言 | `GeneratedName` | 带前缀/后缀的昵称 |

### UsernameGenerator

| 方法 | 参数 | 返回值 | 说明 |
|------|------|--------|------|
| `generate(base_name, min_length, max_length, use_numbers, use_special, count)` | 基础名、长度范围、是否用数字/特殊字符、数量 | `List[str]` | 生成用户名 |
| `check_availability_format(username)` | 用户名 | `(bool, List[str])` | 检查格式是否有效 |

### GameIdGenerator

| 方法 | 参数 | 返回值 | 说明 |
|------|------|--------|------|
| `generate(game_type, include_clan, clan_name, count)` | 游戏类型、是否包含战队、战队名、数量 | `List[str]` | 生成游戏ID |

### PetNameGenerator

| 方法 | 参数 | 返回值 | 说明 |
|------|------|--------|------|
| `generate(pet_type, language, count)` | 宠物类型、语言、数量 | `List[str]` | 生成宠物名 |
| `generate_cute_combo(count)` | 数量 | `List[str]` | 生成可爱组合名 |

### TeamNameGenerator

| 方法 | 参数 | 返回值 | 说明 |
|------|------|--------|------|
| `generate(team_type, language, count)` | 团队类型、语言、数量 | `List[str]` | 生成团队名 |
| `generate_with_name(leader_name, team_type)` | 领导者名、团队类型 | `List[str]` | 带领导者名的团队名 |

### FantasyNameGenerator

| 方法 | 参数 | 返回值 | 说明 |
|------|------|--------|------|
| `generate(race, language, count)` | 种族、语言、数量 | `List[str]` | 生成奇幻名 |
| `generate_full_name(race, language)` | 种族、语言 | `str` | 生成全名 |

## 测试

运行测试：

```bash
python nickname_generator_utils/nickname_generator_utils_test.py
```

测试覆盖：
- 47 个测试用例
- 覆盖所有生成器、风格、语言组合
- 边界值测试（空参数、极端参数）

---

**最后更新**: 2026-05-11