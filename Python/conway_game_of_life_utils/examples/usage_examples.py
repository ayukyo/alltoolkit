"""
Conway's Game of Life 使用示例

展示生命游戏各种功能的用法。
"""

from conway_game_of_life_utils.mod import (
    GameOfLife, Rule, Pattern, RULES,
    run_simulation, detect_pattern_type, pattern_to_ascii,
    generate_random_pattern, compare_patterns,
)


def example_basic_game():
    """基本游戏示例"""
    print("=" * 60)
    print("基本游戏示例")
    print("=" * 60)
    
    # 创建游戏
    game = GameOfLife()
    
    # 加载滑翔机模式
    game.load_pattern_by_name('glider', offset=(5, 5))
    
    print(f"\n初始状态 (第 0 代):")
    print(f"活细胞数: {len(game)}")
    print(game.to_string(alive='■', dead='·'))
    
    # 演化 4 代
    game.step(4)
    
    print(f"\n演化后 (第 4 代):")
    print(f"活细胞数: {len(game)}")
    print(game.to_string(alive='■', dead='·'))
    
    # 获取统计
    stats = game.get_statistics()
    print(f"\n统计: {stats}")


def example_patterns():
    """内置模式示例"""
    print("\n" + "=" * 60)
    print("内置模式示例")
    print("=" * 60)
    
    patterns = ['block', 'beehive', 'blinker', 'glider', 'lwss']
    
    for name in patterns:
        game = GameOfLife()
        game.load_pattern_by_name(name)
        
        print(f"\n{name}:")
        print(pattern_to_ascii(Pattern.get(name), alive='■', dead='·'))


def example_oscillators():
    """振荡器示例"""
    print("\n" + "=" * 60)
    print("振荡器示例")
    print("=" * 60)
    
    oscillators = ['blinker', 'toad', 'beacon', 'pulsar']
    
    for name in oscillators:
        game = GameOfLife()
        game.load_pattern_by_name(name)
        
        print(f"\n{name} (周期检测):")
        
        # 检测周期
        initial = game.cells.copy()
        period = 0
        
        for gen in range(20):
            game.step(1)
            if game.cells == initial:
                period = gen + 1
                break
        
        print(f"振荡周期: {period}")
        
        # 显示几个代的状态
        game = GameOfLife()
        game.load_pattern_by_name(name)
        
        for i in range(min(period + 1, 5)):
            print(f"\n第 {i} 代:")
            print(game.to_string(alive='■', dead='·', padding=1))
            if i < period:
                game.step(1)


def example_spaceships():
    """太空船示例"""
    print("\n" + "=" * 60)
    print("太空船示例")
    print("=" * 60)
    
    spaceships = ['glider', 'lwss', 'mwss', 'hwss']
    
    for name in spaceships:
        game = GameOfLife()
        game.load_pattern_by_name(name)
        
        initial_bounds = game.get_bounds()
        print(f"\n{name}:")
        print(f"初始位置: ({initial_bounds[0]}, {initial_bounds[2]})")
        
        # 演化 4 代
        game.step(4)
        
        new_bounds = game.get_bounds()
        print(f"4 代后位置: ({new_bounds[0]}, {new_bounds[2]})")
        print(f"位移: ({new_bounds[0] - initial_bounds[0]}, {new_bounds[2] - initial_bounds[2]})")


def example_glider_gun():
    """滑翔机枪示例"""
    print("\n" + "=" * 60)
    print("滑翔机枪示例 (Gosper Glider Gun)")
    print("=" * 60)
    
    game = GameOfLife()
    game.load_pattern_by_name('glider_gun')
    
    print(f"\n初始状态:")
    print(f"活细胞数: {len(game)}")
    
    # 演化并观察滑翔机产生
    for gen in [0, 30, 60, 90]:
        game = GameOfLife()
        game.load_pattern_by_name('glider_gun')
        game.step(gen)
        
        print(f"\n第 {gen} 代:")
        print(f"活细胞数: {len(game)}")
        
        # 获取边界
        bounds = game.get_bounds()
        print(f"边界: x={bounds[0]}~{bounds[1]}, y={bounds[2]}~{bounds[3]}")


def example_rules():
    """不同规则示例"""
    print("\n" + "=" * 60)
    print("不同规则示例")
    print("=" * 60)
    
    # Conway's Life
    game = GameOfLife(rule=RULES['conway'])
    game.load_pattern_by_name('glider')
    
    print(f"\nConway's Life (B3/S23):")
    print(f"规则: {game.rule}")
    
    game.step(4)
    print(f"4 代后活细胞数: {len(game)}")
    
    # HighLife
    game = GameOfLife(rule=RULES['highlife'])
    game.load_pattern([(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0)])
    
    print(f"\nHighLife (B36/S23):")
    print(f"规则: {game.rule}")
    
    game.step(2)
    print(f"2 代后活细胞数: {len(game)}")
    
    # Seeds
    game = GameOfLife(rule=RULES['seeds'])
    game.load_pattern([(0, 0), (1, 0)])
    
    print(f"\nSeeds (B2/S):")
    print(f"规则: {game.rule}")
    
    game.step(2)
    print(f"2 代后活细胞数: {len(game)}")
    
    # 自定义规则
    custom_rule = Rule({1, 3, 5}, {2, 4}, "Custom")
    game = GameOfLife(rule=custom_rule)
    print(f"\n自定义规则: {custom_rule}")


def example_rle():
    """RLE 格式示例"""
    print("\n" + "=" * 60)
    print("RLE 格式示例")
    print("=" * 60)
    
    # 从 RLE 加载
    rle_glider = """
#C Name: Glider
#C The most famous spaceship in Conway's Life
x = 3, y = 3, rule = B3/S23
bo$2bo$3o!
"""
    
    game = GameOfLife()
    game.load_rle(rle_glider)
    
    print("从 RLE 加载的滑翔机:")
    print(game.to_string(alive='■', dead='·'))
    
    # 导出为 RLE
    game = GameOfLife()
    game.load_pattern_by_name('block')
    
    print(f"\n导出 Block 为 RLE:")
    print(game.to_rle())
    
    game = GameOfLife()
    game.load_pattern_by_name('pulsar')
    
    print(f"\n导出 Pulsar 为 RLE:")
    print(game.to_rle()[:500] + "...")


def example_simulation():
    """模拟分析示例"""
    print("\n" + "=" * 60)
    print("模拟分析示例")
    print("=" * 60)
    
    # 分析 Block
    result = run_simulation(Pattern.BLOCK, generations=100)
    print(f"\nBlock 分析:")
    print(f"稳定: {result['stable']}")
    print(f"仍然生命: {result['still_life']}")
    print(f"振荡周期: {result['oscillation_period']}")
    
    # 分析 Blinker
    result = run_simulation(Pattern.BLINKER, generations=100)
    print(f"\nBlinker 分析:")
    print(f"稳定: {result['stable']}")
    print(f"振荡周期: {result['oscillation_period']}")
    
    # 分析 R Pentomino
    result = run_simulation(Pattern.R_PENTOMINO, generations=1000)
    print(f"\nR Pentomino 分析 (1000 代):")
    print(f"稳定: {result['stable']}")
    print(f"最终活细胞数: {result['final_cells']}")


def example_pattern_detection():
    """模式类型检测示例"""
    print("\n" + "=" * 60)
    print("模式类型检测示例")
    print("=" * 60)
    
    patterns = {
        'Block': Pattern.BLOCK,
        'Beehive': Pattern.BEEHIVE,
        'Blinker': Pattern.BLINKER,
        'Glider': Pattern.GLIDER,
    }
    
    for name, pattern in patterns.items():
        cells = set(pattern)
        type_str = detect_pattern_type(cells, max_generations=10)
        print(f"{name}: {type_str}")


def example_random_generation():
    """随机模式生成示例"""
    print("\n" + "=" * 60)
    print("随机模式生成示例")
    print("=" * 60)
    
    # 生成随机模式
    pattern = generate_random_pattern(density=0.3, width=15, height=15, seed=42)
    
    print(f"\n随机模式 (密度 0.3, 15x15):")
    print(f"活细胞数: {len(pattern)}")
    print(pattern_to_ascii(pattern, alive='■', dead='·'))
    
    # 演化观察
    game = GameOfLife()
    game.load_pattern(pattern)
    
    print(f"\n演化 10 代后:")
    game.step(10)
    print(f"活细胞数: {len(game)}")
    print(game.to_string(alive='■', dead='·'))


def example_comparison():
    """模式比较示例"""
    print("\n" + "=" * 60)
    print("模式比较示例")
    print("=" * 60)
    
    p1 = set(Pattern.GLIDER)
    p2 = set(Pattern.GLIDER)
    
    # 相同模式
    result = compare_patterns(p1, p2)
    print(f"\n比较两个相同的 Glider:")
    print(f"相同: {result['identical']}")
    print(f"相似度: {result['similarity']}")
    
    # 偏移后的模式
    p2_offset = set((x + 1, y) for x, y in Pattern.GLIDER)
    result = compare_patterns(p1, p2_offset)
    print(f"\n比较 Glider 和偏移后的 Glider:")
    print(f"相同: {result['identical']}")
    print(f"共同细胞数: {result['cells_in_common']}")
    print(f"相似度: {result['similarity']}")


def example_methuselahs():
    """Methuselah 模式示例（长期不稳定模式）"""
    print("\n" + "=" * 60)
    print("Methuselah 模式示例")
    print("=" * 60)
    
    methuselahs = {
        'R Pentomino': Pattern.R_PENTOMINO,
        'Acorn': Pattern.ACORN,
        'Diehard': Pattern.DIEHARD,
    }
    
    for name, pattern in methuselahs.items():
        game = GameOfLife()
        game.load_pattern(pattern)
        
        initial = len(game)
        print(f"\n{name} (初始 {initial} 细胞):")
        
        # 演化到稳定或特定代数
        history = []
        max_gen = 500
        
        for gen in range(max_gen):
            cells_before = game.cells.copy()
            history.append(cells_before)
            game.step(1)
            
            # 检查稳定
            if game.cells == cells_before:
                print(f"  第 {gen + 1} 代稳定 (静止生命)")
                break
            
            for i, past in enumerate(history[:-1]):
                if game.cells == past:
                    print(f"  第 {gen + 1} 代稳定 (振荡周期 {len(history) - i})")
                    break
        
        print(f"  最终活细胞数: {len(game)}")


def main():
    """运行所有示例"""
    example_basic_game()
    example_patterns()
    example_oscillators()
    example_spaceships()
    example_glider_gun()
    example_rules()
    example_rle()
    example_simulation()
    example_pattern_detection()
    example_random_generation()
    example_comparison()
    example_methuselahs()
    
    print("\n" + "=" * 60)
    print("所有示例完成!")
    print("=" * 60)


if __name__ == '__main__':
    main()