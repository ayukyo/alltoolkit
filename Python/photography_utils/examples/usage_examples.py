"""
Photography Utilities 使用示例

演示曝光计算、景深计算、视角计算、闪光灯计算等功能。
"""

import sys
import os

# 设置路径以便导入模块
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

# 导入模块
import mod


def example_exposure():
    """曝光值计算示例"""
    print("=== 曝光值计算 ===\n")
    
    # 基础 EV 计算
    print("1. 基础曝光值计算:")
    ev = mod.calculate_ev(2.8, 1/125, 100)
    print(f"   f/2.8, 1/125s, ISO 100 -> EV {ev}")
    
    ev2 = mod.calculate_ev(8, 1/500, 400)
    print(f"   f/8, 1/500s, ISO 400 -> EV {ev2}")
    
    # 等效曝光调整
    print("\n2. 等效曝光调整:")
    print("   基础设置: f/2.8, 1/125s, ISO 100")
    
    result = mod.adjust_exposure(2.8, 1/125, 100, aperture=4.0)
    print(f"   → 光圈调到 f/4: 快门 {mod.format_shutter_speed(result.shutter_speed)}")
    
    result = mod.adjust_exposure(2.8, 1/125, 100, shutter=1/250)
    print(f"   → 快门调到 1/250s: 光圈 {mod.format_aperture(result.aperture)}")
    
    result = mod.adjust_exposure(2.8, 1/125, 100, iso=400)
    print(f"   → ISO 调到 400: 快门 {mod.format_shutter_speed(result.shutter_speed)}")
    
    # 根据 EV 推荐设置
    print("\n3. 根据 EV 推荐曝光:")
    settings = mod.ev_to_settings(15, 100)
    print(f"   EV 15 (晴天) 推荐设置:")
    for s in settings[:5]:
        print(f"   - {mod.format_aperture(s.aperture)}, {mod.format_shutter_speed(s.shutter_speed)}, ISO {s.iso}")


def example_depth_of_field():
    """景深计算示例"""
    print("\n=== 景深计算 ===\n")
    
    # 基础景深计算
    print("1. 基础景深计算:")
    dof = mod.calculate_dof(50, 2.8, 3, "full_frame")
    print(f"   50mm f/2.8 对焦 3m:")
    print(f"   - 近对焦点: {dof.near_focus:.2f}m")
    print(f"   - 远对焦点: {dof.far_focus:.2f}m")
    print(f"   - 总景深: {dof.total_dof:.2f}m")
    print(f"   - 超焦距: {dof.hyperfocal:.2f}m")
    
    # 不同光圈的景深对比
    print("\n2. 不同光圈景深对比:")
    print("   50mm 对焦 3m:")
    for aperture in [2.8, 5.6, 11]:
        dof = mod.calculate_dof(50, aperture, 3, "full_frame")
        print(f"   - f/{aperture}: 景深 {dof.total_dof:.2f}m")
    
    # 超焦距对焦
    print("\n3. 超焦距对焦:")
    h = mod.calculate_hyperfocal(35, 8, "full_frame")
    print(f"   35mm f/8 超焦距: {h:.2f}m")
    
    dof = mod.calculate_dof(35, 8, h, "full_frame")
    print(f"   在超焦距对焦:")
    print(f"   - 近对焦点: {dof.near_focus:.2f}m (超焦距的一半)")
    print(f"   - 远对焦点: 无穷远")
    
    # 不同传感器对比
    print("\n4. 不同传感器景深对比:")
    print("   50mm f/2.8 对焦 3m:")
    for sensor in ["full_frame", "aps_c", "micro_four_thirds"]:
        dof = mod.calculate_dof(50, 2.8, 3, sensor)
        print(f"   - {sensor}: 景深 {dof.total_dof:.2f}m")


def example_angle_of_view():
    """视角计算示例"""
    print("\n=== 视角计算 ===\n")
    
    # 不同焦距视角
    print("1. 不同焦距视角:")
    for focal in [14, 24, 50, 85, 200]:
        aov = mod.calculate_angle_of_view(focal, "full_frame")
        print(f"   {focal}mm: 水平 {aov.horizontal:.1f}°, 垂直 {aov.vertical:.1f}°, 对角 {aov.diagonal:.1f}°")
    
    # 等效焦距
    print("\n2. 等效焦距计算:")
    focal = 35
    for sensor in ["aps_c", "micro_four_thirds", "1_inch"]:
        eq = mod.calculate_equivalent_focal_length(focal, sensor)
        cf = mod.get_crop_factor(sensor)
        print(f"   {sensor} {focal}mm -> 等效 {eq}mm (裁剪系数 {cf})")


def example_flash():
    """闪光灯计算示例"""
    print("\n=== 闪光灯计算 ===\n")
    
    # 闪光距离计算
    print("1. 闪光距离计算:")
    gn = 36
    for aperture in [2.8, 4, 5.6, 8]:
        dist = mod.calculate_flash_distance(gn, aperture, 100)
        print(f"   GN {gn} @ f/{aperture} ISO 100 -> {dist}m")
    
    # ISO 对距离的影响
    print("\n2. ISO 对闪光距离的影响:")
    gn = 36
    aperture = 4
    for iso in [100, 200, 400, 800]:
        dist = mod.calculate_flash_distance(gn, aperture, iso)
        print(f"   ISO {iso}: {dist}m")
    
    # 闪光指数计算
    print("\n3. 计算所需闪光指数:")
    distance = 10
    aperture = 4
    gn = mod.calculate_guide_number(distance, aperture, 100)
    print(f"   距离 {distance}m @ f/{aperture} -> GN {gn}")


def example_sunny_16():
    """阳光16法则示例"""
    print("\n=== 阳光16法则 ===\n")
    
    # 不同光照条件
    print("1. 不同光照条件曝光:")
    for condition, name in [
        ("sunny", "晴天"),
        ("slight_overcast", "轻微阴天"),
        ("overcast", "阴天"),
        ("heavy_overcast", "重度阴天"),
        ("sunset", "日落"),
    ]:
        shutter, iso, ev = mod.sunny_16(condition, 16, 100)
        print(f"   {name}: f/16, {mod.format_shutter_speed(shutter)}, EV {ev:.1f}")
    
    # 不同光圈
    print("\n2. 晴天不同光圈设置:")
    for aperture in [16, 11, 8, 5.6]:
        shutter, iso, ev = mod.sunny_16("sunny", aperture, 100)
        print(f"   f/{aperture}: {mod.format_shutter_speed(shutter)}")


def example_golden_blue_hour():
    """黄金时刻/蓝调时刻示例"""
    print("\n=== 黄金时刻/蓝调时刻 ===\n")
    
    print("1. 黄金时刻判断:")
    for angle in [-5, 0, 2, 5, 8, 15]:
        is_golden, desc = mod.is_golden_hour(angle)
        print(f"   太阳高度 {angle}°: {desc}")
    
    print("\n2. 蓝调时刻判断:")
    for angle in [-8, -4, -2, 0, 3, 8]:
        is_blue, desc = mod.is_blue_hour(angle)
        print(f"   太阳高度 {angle}°: {desc}")


def example_lens_classification():
    """镜头分类示例"""
    print("\n=== 镜头分类 ===\n")
    
    print("常见镜头类型:")
    focal_lengths = [14, 24, 35, 50, 85, 135, 200, 400, 600]
    for focal in focal_lengths:
        type_name = mod.classify_lens(focal)
        aov = mod.calculate_angle_of_view(focal)
        print(f"   {focal}mm: {type_name} (视角 {aov.diagonal:.1f}°)")


def example_safe_shutter():
    """安全快门示例"""
    print("\n=== 安全快门 ===\n")
    
    print("1. 基础安全快门:")
    for focal in [24, 50, 85, 200]:
        safe = mod.calculate_safe_shutter(focal)
        print(f"   {focal}mm: {mod.format_shutter_speed(safe)}")
    
    print("\n2. 防抖对安全快门的影响:")
    focal = 200
    for stops in [0, 2, 4, 5]:
        safe = mod.calculate_safe_shutter(focal, "full_frame", stops)
        print(f"   {focal}mm {stops}档防抖: {mod.format_shutter_speed(safe)}")


def example_astrophotography():
    """星空摄影示例"""
    print("\n=== 星空摄影 ===\n")
    
    print("1. 500法则 - 最大曝光时间:")
    for focal in [14, 24, 35, 50]:
        max_exp = mod.calculate_500_rule(focal)
        print(f"   {focal}mm: {max_exp}s")
    
    print("\n2. NPF法则 (更精确):")
    focal = 24
    for aperture in [1.4, 2.0, 2.8]:
        max_exp = mod.calculate_npf_rule(focal, aperture, 4.8)
        print(f"   {focal}mm f/{aperture}: {max_exp}s")
    
    print("\n3. 不同传感器对比:")
    for sensor in ["full_frame", "aps_c", "micro_four_thirds"]:
        max_exp = mod.calculate_500_rule(24, sensor)
        print(f"   {sensor} 24mm: {max_exp}s")


def example_real_world():
    """真实场景应用示例"""
    print("\n=== 真实场景应用 ===\n")
    
    # 人像摄影
    print("1. 人像摄影 (85mm f/1.8):")
    dof = mod.calculate_dof(85, 1.8, 2)
    print(f"   对焦 2m, 景深 {dof.total_dof:.3f}m")
    safe = mod.calculate_safe_shutter(85)
    print(f"   安全快门: {mod.format_shutter_speed(safe)}")
    
    # 风光摄影
    print("\n2. 风光摄影 (24mm f/11):")
    h = mod.calculate_hyperfocal(24, 11)
    print(f"   超焦距: {h:.2f}m")
    dof = mod.calculate_dof(24, 11, h)
    print(f"   在超焦距对焦, 景深从 {dof.near_focus:.2f}m 到无穷远")
    
    # 体育摄影
    print("\n3. 体育摄影 (200mm f/2.8):")
    safe = mod.calculate_safe_shutter(200)
    print(f"   安全快门: {mod.format_shutter_speed(safe)}")
    result = mod.adjust_exposure(2.8, 1/500, 100, shutter=1/1000)
    print(f"   快门 1/1000s -> 光圈 {mod.format_aperture(result.aperture)}")
    
    # 星空摄影
    print("\n4. 星空摄影 (14mm f/1.8):")
    max_exp = mod.calculate_500_rule(14)
    print(f"   最大曝光: {max_exp}s")
    settings = mod.exposure_recommendation(-5, "aperture", 1.8, 3200)
    print(f"   EV -5 推荐: {mod.format_aperture(settings.aperture)}, "
          f"{mod.format_shutter_speed(settings.shutter_speed)}, ISO {settings.iso}")


def example_magnification():
    """放大倍率示例"""
    print("\n=== 放大倍率 ===\n")
    
    print("1. 不同距离放大倍率:")
    focal = 100
    for distance in [0.5, 1, 2, 5]:
        m = mod.calculate_magnification(focal, distance)
        print(f"   {focal}mm @ {distance}m: {m:.4f}x")
    
    print("\n2. 最近对焦距离计算:")
    for magnification in [0.1, 0.25, 0.5, 1.0]:
        dist = mod.calculate_closest_focus_distance(100, magnification)
        print(f"   100mm {magnification}x 放大 -> 最近对焦 {dist:.2f}m")


def main():
    """运行所有示例"""
    example_exposure()
    example_depth_of_field()
    example_angle_of_view()
    example_flash()
    example_sunny_16()
    example_golden_blue_hour()
    example_lens_classification()
    example_safe_shutter()
    example_astrophotography()
    example_magnification()
    example_real_world()


if __name__ == "__main__":
    main()