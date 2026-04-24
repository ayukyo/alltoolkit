"""
Cellular Automata Utils - 使用示例

展示各种元胞自动机的使用方法和应用场景。
"""

import sys
sys.path.insert(0, '/home/admin/.openclaw/workspace/AllToolkit/Python')

from cellular_automata_utils.mod import (
    GameOfLife,
    ElementaryCA,
    LangtonsAnt,
    MultiColorAnt,
    BriansBrain,
    Wireworld,
    HighLife,
    Seeds,
    DayAndNight,
    CustomLife,
    pattern_to_coords,
    rle_decode,
)


def example_game_of_life():
    """生命游戏示例。"""
    print("=" * 60)
    print("Game of Life - 康威生命游戏")
    print("=" * 60)
    
    # 创建 20x20 的世界
    gol = GameOfLife(20, 20, wrap=True)
    
    # 添加经典图案
    gol.add_glider(0, 0)
    gol.add_blinker(10, 10)
    gol.add_pulsar(2, 2)
    
    print("初始状态:")
    print(gol.to_string(alive='█', dead='·'))
    print(f"活细胞数: {gol.count_alive()}")
    print()
    
    # 演化 10 代
    gol.evolve(10)
    print(f"第 {gol.generation} 代:")
    print(gol.to_string(alive='█', dead='·'))
    print(f"活细胞数: {gol.count_alive()}")
    print()


def example_gosper_glider_gun():
    """高斯帕滑翔机枪示例。"""
    print("=" * 60)
    print("Gosper Glider Gun - 高斯帕滑翔机枪")
    print("=" * 60)
    
    gol = GameOfLife(40, 15, wrap=True)
    gol.add_gosper_glider_gun(0, 0)
    
    print("初始:")
    print(gol.to_string(alive='█', dead='·'))
    print()
    
    # 演化到产生滑翔机
    gol.evolve(30)
    print(f"第 {gol.generation} 代 - 已产生滑翔机:")
    print(gol.to_string(alive='█', dead='·'))
    print()


def example_elementary_ca():
    """初等元胞自动机示例。"""
    print("=" * 60)
    print("Elementary CA - 初等元胞自动机")
    print("=" * 60)
    
    # Rule 90 - 谢尔宾斯基三角形
    ca90 = ElementaryCA(63, rule=90, wrap=False)
    ca90.initialize_single()
    history = ca90.run_with_history(31)
    
    print("Rule 90 (谢尔宾斯基三角形):")
    print(ca90.to_string_history(alive='█', dead='·'))
    print()
    
    # Rule 30 - 混沌图案
    ca30 = ElementaryCA(40, rule=30, wrap=False)
    ca30.initialize_single()
    history = ca30.run_with_history(20)
    
    print("Rule 30 (混沌图案):")
    print(ca30.to_string_history(alive='█', dead='·'))
    print()


def example_langtons_ant():
    """兰顿蚂蚁示例。"""
    print("=" * 60)
    print("Langton's Ant - 兰顿蚂蚁")
    print("=" * 60)
    
    ant = LangtonsAnt(30, 30, wrap=True)
    ant.add_ant(15, 15)
    
    print("初始状态（蚂蚁在中央）:")
    print(ant.to_string(alive='█', dead='·'))
    print()
    
    # 演化 100 步
    ant.evolve(100)
    print(f"第 {ant.generation} 步:")
    print(ant.to_string(alive='█', dead='·'))
    print(f"蚂蚁位置: {ant.get_ant_positions()}")
    print()


def example_multicolor_ant():
    """多色蚂蚁示例。"""
    print("=" * 60)
    print("Multi-Color Ant - 多色蚂蚁")
    print("=" * 60)
    
    # LLRR 规则产生有趣的图案
    ant = MultiColorAnt(50, 50, rule='LLRR', wrap=True)
    ant.add_ant(25, 25)
    
    ant.evolve(5000)
    print(f"规则 LLRR，演化 {ant.generation} 步:")
    print(ant.to_string(chars=' .-+=#@'))
    print()


def example_brians_brain():
    """布赖恩大脑示例。"""
    print("=" * 60)
    print("Brian's Brain - 布赖恩大脑")
    print("=" * 60)
    
    bb = BriansBrain(20, 20, wrap=True)
    
    # 创建一些初始活细胞
    import random
    for _ in range(20):
        x = random.randint(0, 19)
        y = random.randint(0, 19)
        bb.set_cell(x, y, BriansBrain.ALIVE)
    
    print("初始状态:")
    print(bb.to_string(chars=' █░'))
    print()
    
    bb.evolve(10)
    print(f"第 {bb.generation} 代:")
    print(bb.to_string(chars=' █░'))
    print()


def example_wireworld():
    """线世界示例。"""
    print("=" * 60)
    print("Wireworld - 线世界")
    print("=" * 60)
    
    ww = Wireworld(30, 10, wrap=False)
    
    # 创建导线
    ww.add_wire([(x, 4) for x in range(20)])
    
    # 添加电子
    ww.add_electron(0, 4)
    
    print("初始状态（电子在导线左端）:")
    print(ww.to_string(chars=' ·●○'))
    print()
    
    # 演化显示电子流动
    for i in range(5):
        ww.step()
        print(f"第 {ww.generation} 步:")
        print(ww.to_string(chars=' ·●○'))
    print()


def example_highlife():
    """HighLife 示例。"""
    print("=" * 60)
    print("HighLife")
    print("=" * 60)
    
    hl = HighLife(30, 30, wrap=True)
    hl.randomize(0.2)
    
    print("随机初始状态:")
    print(hl.to_string(alive='█', dead='·'))
    print(f"密度: {hl.density():.2%}")
    print()
    
    hl.evolve(20)
    print(f"第 {hl.generation} 代:")
    print(hl.to_string(alive='█', dead='·'))
    print()


def example_custom_rules():
    """自定义规则示例。"""
    print("=" * 60)
    print("Custom Life - 自定义规则")
    print("=" * 60)
    
    # 生命游戏
    gol = CustomLife(20, 20, rule="B3/S23", wrap=True)
    gol.add_glider(0, 0)
    gol.evolve(10)
    print("标准生命游戏 B3/S23:")
    print(gol.to_string(alive='█', dead='·'))
    print()
    
    # Day & Night
    dn = CustomLife(20, 20, rule="B3678/S34678", wrap=True)
    dn.randomize(0.4)
    dn.evolve(10)
    print("Day & Night B3678/S34678:")
    print(dn.to_string(alive='█', dead='·'))
    print()
    
    # Seeds
    seeds = CustomLife(20, 20, rule="B2/S", wrap=True)
    seeds.set_pattern([(0, 0, 1), (1, 0, 1), (0, 1, 1)], (10, 10))
    seeds.evolve(5)
    print("Seeds B2/S (爆炸性增长):")
    print(seeds.to_string(alive='█', dead='·'))
    print()


def example_pattern_loading():
    """图案加载示例。"""
    print("=" * 60)
    print("Pattern Loading - 图案加载")
    print("=" * 60)
    
    # 从字符串加载图案
    pattern_str = """
    ###
    # #
    ###
    """
    coords = pattern_to_coords(pattern_str, alive_char='#')
    
    gol = GameOfLife(10, 10)
    gol.set_pattern(coords, (3, 3))
    print("从字符串加载的图案:")
    print(gol.to_string(alive='█', dead='·'))
    print()
    
    # 从 RLE 加载滑翔机
    coords = rle_decode("bo$2bo$3o!")
    gol2 = GameOfLife(10, 10)
    gol2.set_pattern(coords, (2, 2))
    print("从 RLE 加载的滑翔机:")
    print(gol2.to_string(alive='█', dead='·'))
    print()


def example_animate():
    """动画演示示例（使用终端）。"""
    print("=" * 60)
    print("Animation - 动画演示")
    print("=" * 60)
    print("提示: 在终端中使用可以创建实时动画")
    print()
    
    gol = GameOfLife(40, 20, wrap=True)
    gol.add_gosper_glider_gun(0, 0)
    
    # 示例动画代码
    animation_code = '''
import time

gol = GameOfLife(40, 20, wrap=True)
gol.add_gosper_glider_gun(0, 0)

for _ in range(100):
    # 清屏并打印
    print('\\033[2J\\033[H')  # ANSI 清屏
    print(f"Generation {gol.generation}")
    print(gol.to_string(alive='█', dead='·'))
    gol.step()
    time.sleep(0.1)
'''
    print(animation_code)


def main():
    """运行所有示例。"""
    example_game_of_life()
    example_gosper_glider_gun()
    example_elementary_ca()
    example_langtons_ant()
    example_multicolor_ant()
    example_brians_brain()
    example_wireworld()
    example_highlife()
    example_custom_rules()
    example_pattern_loading()
    example_animate()
    
    print("=" * 60)
    print("所有示例完成！")
    print("=" * 60)


if __name__ == '__main__':
    main()