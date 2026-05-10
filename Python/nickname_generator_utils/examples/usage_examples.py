"""
昵称生成器使用示例
展示各种昵称生成功能的使用方法
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    NicknameGenerator,
    UsernameGenerator,
    GameIdGenerator,
    PetNameGenerator,
    TeamNameGenerator,
    FantasyNameGenerator,
    NameStyle,
    generate_nickname,
    generate_username,
    generate_game_id,
    generate_pet_name,
    generate_team_name,
    generate_fantasy_name,
    generate_names_bulk
)


def example_basic_nicknames():
    """基础昵称生成示例"""
    print("=" * 60)
    print("【基础昵称生成】")
    print("=" * 60)
    
    # 使用便捷函数快速生成
    print("\n1. 快速生成昵称:")
    print(f"   可爱风格(中文): {generate_nickname('可爱', 'chinese')}")
    print(f"   酷炫风格(中文): {generate_nickname('酷炫', 'chinese')}")
    print(f"   神秘风格(中文): {generate_nickname('神秘', 'chinese')}")
    print(f"   Cute风格(英文): {generate_nickname('cute', 'english')}")
    print(f"   Cool风格(英文): {generate_nickname('cool', 'english')}")
    
    # 使用完整类生成
    print("\n2. 使用生成器类:")
    gen = NicknameGenerator()
    
    # 生成多个昵称
    print("   批量生成可爱昵称:")
    results = gen.generate(NameStyle.CUTE, "chinese", 5)
    for r in results:
        print(f"      - {r.name} (变体: {', '.join(r.alternatives[:3])})")
    
    # 混合风格生成
    print("\n   混合风格生成:")
    results = gen.generate_mixed(6)
    for r in results:
        print(f"      - [{r.style.value}] {r.name}")


def example_all_styles():
    """所有风格示例"""
    print("\n" + "=" * 60)
    print("【所有风格展示】")
    print("=" * 60)
    
    gen = NicknameGenerator()
    
    styles = [
        ("可爱", NameStyle.CUTE),
        ("酷炫", NameStyle.COOL),
        ("搞笑", NameStyle.FUNNY),
        ("神秘", NameStyle.MYSTIC),
        ("英雄", NameStyle.HEROIC),
        ("自然", NameStyle.NATURE),
        ("科技", NameStyle.TECH),
        ("美食", NameStyle.FOOD),
        ("动物", NameStyle.ANIMAL),
        ("奇幻", NameStyle.FANTASY),
    ]
    
    print("\n各风格示例:")
    for name, style in styles:
        result = gen.generate(style, "chinese", 1)[0]
        print(f"   {name}: {result.name}")
        
        result = gen.generate(style, "english", 1)[0]
        print(f"   {name}(英文): {result.name}")


def example_username_generation():
    """用户名生成示例"""
    print("\n" + "=" * 60)
    print("【用户名生成】")
    print("=" * 60)
    
    gen = UsernameGenerator()
    
    # 基本生成
    print("\n1. 基本用户名:")
    names = gen.generate(count=5)
    for n in names:
        print(f"   - {n}")
    
    # 基于基础名生成
    print("\n2. 基于基础名生成:")
    names = gen.generate(base_name="myname", count=5)
    for n in names:
        print(f"   - {n}")
    
    # 不使用数字
    print("\n3. 纯字母用户名:")
    names = gen.generate(use_numbers=False, count=5)
    for n in names:
        print(f"   - {n}")
    
    # 使用特殊字符
    print("\n4. 带特殊字符:")
    names = gen.generate(use_special=True, count=5)
    for n in names:
        print(f"   - {n}")
    
    # 格式验证
    print("\n5. 用户名格式验证:")
    test_names = ["valid_user", "ab", "123start", "user@name"]
    for n in test_names:
        valid, errors = gen.check_availability_format(n)
        status = "有效" if valid else f"无效({errors[0] if errors else ''})"
        print(f"   {n}: {status}")


def example_game_id():
    """游戏ID生成示例"""
    print("\n" + "=" * 60)
    print("【游戏ID生成】")
    print("=" * 60)
    
    gen = GameIdGenerator()
    
    # 不同游戏类型
    print("\n1. 不同游戏类型:")
    game_types = ["fps", "moba", "mmorpg", "casual", "strategy"]
    for gt in game_types:
        id_ = gen.generate(gt, count=1)[0]
        print(f"   {gt}: {id_}")
    
    # 带战队前缀
    print("\n2. 带战队前缀:")
    ids = gen.generate("fps", include_clan=True, count=5)
    for id_ in ids:
        print(f"   - {id_}")
    
    # 自定义战队名
    print("\n3. 自定义战队名:")
    ids = gen.generate("moba", include_clan=True, clan_name="Elite", count=3)
    for id_ in ids:
        print(f"   - {id_}")


def example_pet_names():
    """宠物名字示例"""
    print("\n" + "=" * 60)
    print("【宠物名字生成】")
    print("=" * 60)
    
    gen = PetNameGenerator()
    
    # 不同宠物类型
    print("\n1. 中文宠物名:")
    pet_types = ["dog", "cat", "rabbit", "hamster", "bird", "fish"]
    for pt in pet_types:
        names = gen.generate(pt, "chinese", 3)
        print(f"   {pt}: {', '.join(names)}")
    
    print("\n2. 英文宠物名:")
    for pt in pet_types:
        names = gen.generate(pt, "english", 3)
        print(f"   {pt}: {', '.join(names)}")
    
    # 可爱组合名
    print("\n3. 可爱组合名:")
    names = gen.generate_cute_combo(5)
    for n in names:
        print(f"   - {n}")


def example_team_names():
    """团队名称示例"""
    print("\n" + "=" * 60)
    print("【团队名称生成】")
    print("=" * 60)
    
    gen = TeamNameGenerator()
    
    # 不同团队类型
    print("\n1. 中文团队名:")
    team_types = ["tech", "creative", "business", "gaming", "academic"]
    for tt in team_types:
        names = gen.generate(tt, "chinese", 3)
        print(f"   {tt}: {', '.join(names)}")
    
    print("\n2. 英文团队名:")
    for tt in team_types:
        names = gen.generate(tt, "english", 3)
        print(f"   {tt}: {', '.join(names)}")
    
    # 带领导名字
    print("\n3. 带领导名字的团队:")
    names = gen.generate_with_name("张三", "tech")
    for n in names:
        print(f"   - {n}")


def example_fantasy_names():
    """奇幻角色名示例"""
    print("\n" + "=" * 60)
    print("【奇幻角色名生成】")
    print("=" * 60)
    
    gen = FantasyNameGenerator()
    
    # 不同种族
    print("\n1. 英文奇幻名:")
    races = ["elven", "dwarven", "human", "demonic", "angelic"]
    for race in races:
        names = gen.generate(race, "english", 5)
        print(f"   {race}: {', '.join(names)}")
    
    print("\n2. 中文奇幻名:")
    for race in races:
        names = gen.generate(race, "chinese", 3)
        print(f"   {race}: {', '.join(names)}")
    
    # 全名
    print("\n3. 奇幻全名:")
    print(f"   精灵(英文): {gen.generate_full_name('elven', 'english')}")
    print(f"   精灵(中文): {gen.generate_full_name('elven', 'chinese')}")
    print(f"   恶魔(英文): {gen.generate_full_name('demonic', 'english')}")


def example_bulk_generation():
    """批量生成示例"""
    print("\n" + "=" * 60)
    print("【批量生成】")
    print("=" * 60)
    
    print("\n批量生成50个昵称:")
    names = generate_names_bulk("可爱", "chinese", 50)
    
    # 显示前20个
    print("\n前20个:")
    for i, name in enumerate(names[:20], 1):
        print(f"   {i:2d}. {name}")
    
    print(f"\n总共生成: {len(names)}个昵称")


def example_with_prefix_suffix():
    """带前缀后缀示例"""
    print("\n" + "=" * 60)
    print("【带前缀后缀的昵称】")
    print("=" * 60)
    
    gen = NicknameGenerator()
    
    print("\n酷炫风格带前缀后缀:")
    for _ in range(5):
        result = gen.generate_with_prefix_suffix(NameStyle.COOL, "english")
        print(f"   - {result.name} (组成: {result.components})")
    
    print("\n科技风格带前缀后缀:")
    for _ in range(5):
        result = gen.generate_with_prefix_suffix(NameStyle.TECH, "english")
        print(f"   - {result.name} (组成: {result.components})")


def main():
    """运行所有示例"""
    print("\n")
    print("*" * 60)
    print("*       昵称生成器使用示例                      *")
    print("*" * 60)
    
    example_basic_nicknames()
    example_all_styles()
    example_username_generation()
    example_game_id()
    example_pet_names()
    example_team_names()
    example_fantasy_names()
    example_bulk_generation()
    example_with_prefix_suffix()
    
    print("\n" + "=" * 60)
    print("示例展示完成!")
    print("=" * 60)


if __name__ == "__main__":
    main()