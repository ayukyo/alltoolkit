# Chess Utils


chess_utils - 国际象棋工具模块

功能：
- FEN 字符串解析与生成
- 棋盘表示与操作
- 走法生成与验证
- 特殊走法处理（王车易位、吃过路兵、兵升变）
- 棋局状态检测（将军、将死、和棋）
- PGN 格式支持

零外部依赖，纯 Python 实现


## 功能

### 类

- **PieceType**: 棋子类型
- **Color**: 棋子颜色
  方法: opposite
- **Piece**: 棋子
  方法: from_symbol, to_symbol
- **Square**: 棋盘位置（0-7, 0-7 对应 a1-h8）
  方法: to_algebraic, from_algebraic, offset, is_valid
- **Move**: 走法
  方法: to_uci, from_uci, to_san
- **Board**: 棋盘
  方法: copy, from_fen, to_fen, starting_position, get_piece ... (16 个方法)
- **Game**: 游戏状态管理
  方法: make_move, undo_move, get_result, is_game_over
- **PGN**: PGN 格式支持
  方法: export

### 函数

- **create_board(fen**) - 创建棋盘
- **create_game(fen**) - 创建游戏
- **san_to_uci(board, san**) - 将 SAN 转换为 UCI
- **uci_to_move(board, uci**) - 将 UCI 转换为 Move 对象
- **opposite(self**)
- **from_symbol(cls, symbol**) - 从符号创建棋子
- **to_symbol(self**) - 转换为符号
- **to_algebraic(self**) - 转换为代数记号 (e.g., 'e4')
- **from_algebraic(cls, notation**) - 从代数记号创建
- **offset(self, df, dr**) - 偏移位置，返回 None 如果越界

... 共 35 个函数

## 使用示例

```python
from mod import create_board

# 使用 create_board
result = create_board()
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
