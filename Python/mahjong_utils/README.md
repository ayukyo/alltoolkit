# Mahjong Utils - 日本立直麻将工具库

麻将牌操作、和牌检测、役种判断、得分计算等功能的零依赖工具库。

## 功能特性

- ✅ **牌的表示与操作** - 万子、筒子、索子、风牌、三元牌
- ✅ **手牌管理** - 解析、排序、添加、移除牌
- ✅ **和牌检测** - 标准形、七对子、国士无双
- ✅ **役种检测** - 30+役种判断，包括役满
- ✅ **得分计算** - 符数计算、番数对照表
- ✅ **向听数计算** - 标准形/七对子/国士无双向听
- ✅ **进张效率** - 等待牌、最佳切牌计算
- ✅ **牌山模拟** - 洗牌、摸牌、游戏模拟
- 🎯 **零依赖** - 仅使用 Python 标准库

## 快速开始

### 创建牌

```python
from mahjong_utils import create_tile, TileType

# 数牌
man1 = create_tile("1m")  # 一万
pin5 = create_tile("5p")  # 五筒
sou9 = create_tile("9s")  # 九索

# 字牌
east = create_tile("东")  # 东风
green = create_tile("发")  # 发财
red = create_tile("中")   # 红中

# 牌属性
man1.is_terminal        # True - 幺九牌
pin5.is_simple          # True - 中张牌
east.is_honor           # True - 字牌
```

### 手牌操作

```python
from mahjong_utils import parse_hand

# 从字符串解析
hand = parse_hand("123m 456p 789s 11z")
print(hand)  # "123m 456p 789s 11z"
print(len(hand))  # 10张

# 添加和移除牌
hand.add_tile(create_tile("5m"))
hand.remove_tile(create_tile("1m"))

# 排序
hand.sort()
```

### 和牌检测

```python
from mahjong_utils import WinDetector, can_win

# 使用检测器
hand = parse_hand("123m 456m 789m 123p 11s")
detector = WinDetector(hand)

detector.can_win()        # True - 可以和牌
detector.is_standard_win()  # True - 标准形
detector.is_seven_pairs()   # False - 不是七对子

# 获取分解
decomp = detector.get_win_decomposition()
for meld in decomp:
    print(f"{meld.meld_type}: {[str(t) for t in meld.tiles]}")

# 快速检测
tiles = hand.tiles
can_win(tiles)  # True
```

### 向听数计算

```python
from mahjong_utils import TileEfficiency, calculate_shanten

hand = parse_hand("123m 456m 789m 12p 135s")
efficiency = TileEfficiency(hand)

efficiency.get_shanten()  # 1 - 一向听

# 听牌时获取等待牌
hand2 = parse_hand("123m 456m 789m 12p 11s")
efficiency2 = TileEfficiency(hand2)
efficiency2.get_shanten()  # 0 - 听牌

waiting = efficiency2.get_waiting_tiles()
print([str(t) for t in waiting])  # ["1p", "3p"]

# 最佳切牌
best_discard = efficiency.find_best_discard()

# 快速计算
tiles = hand.tiles
calculate_shanten(tiles)  # 1
```

### 役种检测

```python
from mahjong_utils import YakuDetector, detect_yaku, YakuType

hand = parse_hand("234567m 23456p 234s 22s")
win_tile = create_tile("2s")

detector = YakuDetector(hand, win_tile)

for yaku, han in detector.detect_yaku():
    print(f"{yaku.value}: {han}番")

# 带立直
detector2 = YakuDetector(hand, win_tile, 
    is_riichi=True, 
    is_ippatsu=True,
    is_tsumo=True)

# 役满检测
detector.is_yakuman()  # 是否役满
detector.calculate_han()  # 总番数

# 快速检测
detect_yaku(hand.tiles, win_tile)
```

### 得分计算

```python
from mahjong_utils import ScoreCalculator, calculate_score

hand = parse_hand("234567m 23456p 234s 22s")
win_tile = create_tile("2s")

yaku_detector = YakuDetector(hand, win_tile)
calculator = ScoreCalculator(hand, win_tile, 
    yaku_detector=yaku_detector,
    is_dealer=False)

calculator.calculate_fu()  # 符数
calculator.calculate_score()  # {"total": 1000}

# 庄家自摸
calculator2 = ScoreCalculator(hand, win_tile,
    is_tsumo=True,
    is_dealer=True,
    yaku_detector=yaku_detector)

# 快速计算
calculate_score(hand.tiles, win_tile)
```

### 牌山与游戏

```python
from mahjong_utils import Wall, MahjongGame

# 牌山
wall = Wall(seed=42)
print(wall.remaining_count)  # 136

tile = wall.draw()
tiles = wall.draw_multiple(13)

# 游戏模拟
game = MahjongGame(4)
game.start_game(seed=42)

for i in range(4):
    print(f"玩家{i}: {game.get_player_hand(i)}")

# 摸牌和打牌
tile = game.draw_tile(0)
game.discard_tile(0, tile)

# 宝牌
dora = game.get_dora_tiles()
```

## 支持的役种

### 一番
- 立直 (RIICHI)
- 一发 (IPPATSU)
- 断幺九 (TANYAO)
- 平和 (PINFU)
- 一杯口 (IIPETSKO)
- 门前清自摸 (MENZEN_TSUMO)
- 岭上开花 (RINSHAN)

### 二番
- 两立直 (DOUBLE_RIICHI)
- 混全带幺九 (CHANTA)
- 混老头 (HONROUTOU)
- 三色同顺 (SANSHOKU_DOUJUN)
- 一气通贯 (ITTSU)
- 对对和 (TOITOI)
- 三暗刻 (SANANKOU)
- 七对子 (CHIITOU)
- 混一色 (HONITSU)

### 三番
- 纯全带幺九 (JUNCHAN)
- 二杯口 (RYANPEIKOU)

### 六番
- 清一色 (CHINITSU)

### 役满
- 国士无双 (KOKUSHI)
- 国士无双十三面 (KOKUSHI_13)
- 四暗刻 (SUUANKOU)
- 四暗刻单骑 (SUUANKOU_TANKI)
- 大三元 (DAISANGEN)
- 字一色 (TSUUIISOU)
- 小四喜 (SHOUSUUSHI)
- 大四喜 (DAISUUSHI)
- 绿一色 (RYUUIISOU)
- 清老头 (CHINROUTOU)

## API 参考

### Tile
- `Tile(tile_type, number)` - 创建牌
- `Tile.from_string(s)` - 从字符串解析
- `is_honor` - 是否字牌
- `is_terminal` - 是否幺九牌（1或9）
- `is_terminal_or_honor` - 是否幺九牌或字牌
- `is_simple` - 是否中张牌（2-8）
- `is_green` - 是否绿牌

### Hand
- `Hand(tiles)` - 创建手牌
- `Hand.from_string(s)` - 从字符串解析
- `add_tile(tile)` - 添加牌
- `remove_tile(tile)` - 移除牌
- `sort()` - 排序
- `to_tile_string()` - 转为字符串
- `count_tile(tile)` - 计算牌数量

### WinDetector
- `can_win()` - 是否可以和牌
- `is_standard_win()` - 是否标准形
- `is_seven_pairs()` - 是否七对子
- `is_thirteen_orphans()` - 是否国士无双
- `get_win_decomposition()` - 获取和牌分解

### YakuDetector
- `detect_yaku()` - 检测役种列表
- `calculate_han()` - 计算总番数
- `is_yakuman()` - 是否役满

### TileEfficiency
- `get_shanten()` - 获取向听数
- `get_waiting_tiles()` - 获取等待牌
- `calculate_ukeire()` - 计算进张数
- `find_best_discard()` - 找最佳切牌

### ScoreCalculator
- `calculate_fu()` - 计算符数
- `calculate_score()` - 计算得分

## 牌的字符串表示

- 数牌: `1m`（一万）, `5p`（五筒）, `9s`（九索）
- 字牌: `东`（东风）, `南`（南风）, `发`（发财）
- 数字表示: `1234z`（东东南南西北）, `567z`（白发中）
- 手牌: `123m 456p 789s 11z`

## 测试

```bash
python Python/mahjong_utils/mahjong_utils_test.py
```

## 示例

```bash
python Python/mahjong_utils/examples/usage_examples.py
```

## 注意事项

- 本库基于日本立直麻将规则
- 役种检测覆盖常用役种，部分复杂役种可能需要进一步开发
- 得分计算基于标准符数和番数对照表
- 向听数计算考虑标准形、七对子和国士无双三种和牌形式