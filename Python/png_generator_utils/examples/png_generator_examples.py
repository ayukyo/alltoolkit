# -*- coding: utf-8 -*-
"""
PNG Generator Utils - 使用示例
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from mod import PNGCanvas, solid_png, bar_chart_png, create_canvas


# -------------------------------------------------------------------------
# 示例 1：基础画布与几何图形
# -------------------------------------------------------------------------
print("=== 示例 1：基础画布与几何图形 ===")

canvas = PNGCanvas(300, 200, (248, 248, 248))

# 画矩形背景
canvas.draw_rect(0, 0, 300, 200, (70, 130, 180), fill=True)

# 画几个圆形
canvas.draw_circle(75, 100, 50, (255, 255, 255), fill=False)
canvas.draw_circle(150, 100, 50, (255, 200, 100), fill=True)
canvas.draw_circle(225, 100, 50, (100, 200, 100), fill=False)

# 画三角形
canvas.draw_triangle(150, 170, 100, 190, 200, 190, (255, 100, 100), fill=True)

# 写文字
canvas.draw_text_centered("HELLO PNG", (255, 255, 255), scale=2)

data = canvas.encode()
with open("/tmp/png_demo_basic.png", "wb") as f:
    f.write(data)
print("已保存: /tmp/png_demo_basic.png")


# -------------------------------------------------------------------------
# 示例 2：渐变填充
# -------------------------------------------------------------------------
print("\n=== 示例 2：线性渐变 ===")

canvas2 = PNGCanvas(300, 150, (255, 255, 255))

# 水平渐变
canvas2.fill_gradient_linear(0, 0, 300, 75,
                               (255, 100, 100), (100, 100, 255), angle=0)

# 垂直渐变
canvas2.fill_gradient_linear(0, 75, 300, 75,
                               (100, 255, 100), (255, 200, 100), angle=90)

canvas2.draw_text_centered("GRADIENT", (255, 255, 255), scale=2)

data = canvas2.encode()
with open("/tmp/png_demo_gradient.png", "wb") as f:
    f.write(data)
print("已保存: /tmp/png_demo_gradient.png")


# -------------------------------------------------------------------------
# 示例 3：径向渐变
# -------------------------------------------------------------------------
print("\n=== 示例 3：径向渐变 ===")

canvas3 = PNGCanvas(200, 200, (0, 0, 0))
canvas3.fill_gradient_radial(100, 100, 90,
                              (255, 220, 100), (50, 50, 150))

canvas3.draw_text_centered("RADIAL", (255, 255, 255), scale=2)

data = canvas3.encode()
with open("/tmp/png_demo_radial.png", "wb") as f:
    f.write(data)
print("已保存: /tmp/png_demo_radial.png")


# -------------------------------------------------------------------------
# 示例 4：条形图
# -------------------------------------------------------------------------
print("\n=== 示例 4：条形图 ===")

chart_data = [45, 72, 38, 90, 55, 63, 80]
chart_labels = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

chart = bar_chart_png(
    data=chart_data,
    labels=chart_labels,
    width=450,
    height=300,
    bar_color=(70, 130, 180),
    title="WEEKLY STATS"
)

with open("/tmp/png_demo_bar_chart.png", "wb") as f:
    f.write(chart)
print("已保存: /tmp/png_demo_bar_chart.png")


# -------------------------------------------------------------------------
# 示例 5：纯色图
# -------------------------------------------------------------------------
print("\n=== 示例 5：纯色 PNG ===")

red_png = solid_png(100, 100, (220, 50, 50))
with open("/tmp/png_demo_solid.png", "wb") as f:
    f.write(red_png)
print("已保存: /tmp/png_demo_solid.png")


# -------------------------------------------------------------------------
# 示例 6：快捷函数
# -------------------------------------------------------------------------
print("\n=== 示例 6：快捷函数 ===")

c = create_canvas(100, 100, (200, 200, 200))
c.draw_circle(50, 50, 40, (50, 50, 50))
c.draw_text_centered("TEST", (255, 255, 255), scale=1)

with open("/tmp/png_demo_quick.png", "wb") as f:
    f.write(c.encode())
print("已保存: /tmp/png_demo_quick.png")


# -------------------------------------------------------------------------
# 示例 7：椭圆
# -------------------------------------------------------------------------
print("\n=== 示例 7：椭圆 ===")

canvas7 = PNGCanvas(300, 200, (250, 250, 250))
canvas7.draw_ellipse(100, 100, 80, 40, (180, 70, 130), fill=False)
canvas7.draw_ellipse(200, 100, 60, 30, (70, 130, 180), fill=True)
canvas7.draw_text_centered("ELLIPSE", (50, 50, 50), scale=2)

with open("/tmp/png_demo_ellipse.png", "wb") as f:
    f.write(canvas7.encode())
print("已保存: /tmp/png_demo_ellipse.png")


print("\n所有示例完成！共生成 7 个 PNG 文件于 /tmp/png_demo_*.png")