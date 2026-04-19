/**
 * Color Utils 使用示例
 * 运行: node usage_examples.js
 */

'use strict';

const colorUtils = require('../mod.js');

console.log('\n========================================');
console.log('  Color Utils 使用示例');
console.log('========================================\n');

// ==================== 颜色解析 ====================

console.log('--- 颜色解析 ---');

console.log('解析 HEX 颜色:');
console.log('  "#ff0000" ->', colorUtils.parseColor('#ff0000'));
console.log('  "#f00" ->', colorUtils.parseColor('#f00'));
console.log('  "#ff000080" (带透明度) ->', colorUtils.parseColor('#ff000080'));

console.log('\n解析 RGB 颜色:');
console.log('  "rgb(255, 128, 64)" ->', colorUtils.parseColor('rgb(255, 128, 64)'));
console.log('  "rgba(255, 0, 0, 0.5)" ->', colorUtils.parseColor('rgba(255, 0, 0, 0.5)'));

console.log('\n解析 HSL 颜色:');
console.log('  "hsl(120, 100%, 50%)" ->', colorUtils.parseColor('hsl(120, 100%, 50%)'));
console.log('  "hsla(240, 100%, 50%, 0.5)" ->', colorUtils.parseColor('hsla(240, 100%, 50%, 0.5)'));

console.log('\n解析命名颜色:');
console.log('  "red" ->', colorUtils.parseColor('red'));
console.log('  "coral" ->', colorUtils.parseColor('coral'));
console.log('  "transparent" ->', colorUtils.parseColor('transparent'));

// ==================== 格式转换 ====================

console.log('\n--- 格式转换 ---');

const red = { r: 255, g: 0, b: 0 };

console.log('RGB 转其他格式:');
console.log('  RGB(255, 0, 0) -> HEX:', colorUtils.rgbToHex(red));
console.log('  RGB(255, 0, 0) -> HSL:', colorUtils.rgbToHsl(red));
console.log('  RGB(255, 0, 0) -> HSV:', colorUtils.rgbToHsv(red));
console.log('  RGB(255, 0, 0) -> CMYK:', colorUtils.rgbToCmyk(red));
console.log('  RGB(255, 0, 0) -> LAB:', colorUtils.rgbToLab(red));

console.log('\nHSL 转 RGB:');
const lime = { h: 120, s: 100, l: 50 };
console.log('  HSL(120, 100%, 50%) -> RGB:', colorUtils.hslToRgb(lime));

console.log('\nCMYK 转 RGB:');
const cyan = { c: 100, m: 0, y: 0, k: 0 };
console.log('  CMYK(100, 0, 0, 0) -> RGB:', colorUtils.cmykToRgb(cyan));

// ==================== 颜色操作 ====================

console.log('\n--- 颜色操作 ---');

console.log('混合颜色:');
const mixed = colorUtils.mixColors('#ff0000', '#0000ff', 0.5);
console.log('  #ff0000 + #0000ff (50:50) ->', colorUtils.toCssString(mixed, 'hex'));

console.log('\n调整亮度:');
const lighter = colorUtils.adjustBrightness('#333333', 30);
const darker = colorUtils.adjustBrightness('#cccccc', -30);
console.log('  #333333 +30% ->', colorUtils.toCssString(lighter, 'hex'));
console.log('  #cccccc -30% ->', colorUtils.toCssString(darker, 'hex'));

console.log('\n调整饱和度:');
const vivid = colorUtils.adjustSaturation('#999999', 50);
console.log('  #999999 +50% 饱和度 ->', colorUtils.toCssString(vivid, 'hex'));

console.log('\n调整色相:');
const rotated = colorUtils.adjustHue('#ff0000', 120);
console.log('  #ff0000 旋转 120° ->', colorUtils.toCssString(rotated, 'hex'));

console.log('\n反转颜色:');
const inverted = colorUtils.invertColor('#ff0000');
console.log('  #ff0000 反转 ->', colorUtils.toCssString(inverted, 'hex'));

console.log('\n灰度化:');
const gray = colorUtils.grayscaleColor('#ff0000');
console.log('  #ff0000 灰度化 ->', colorUtils.toCssString(gray, 'hex'));

console.log('\n互补色:');
const complement = colorUtils.complementColor('#ff0000');
console.log('  #ff0000 互补色 ->', colorUtils.toCssString(complement, 'hex'));

// ==================== 对比度与可访问性 ====================

console.log('\n--- 对比度与可访问性 ---');

console.log('计算对比度:');
const ratio = colorUtils.getContrastRatio('#000000', '#ffffff');
console.log('  黑 vs 白 对比度:', ratio);

console.log('\nWCAG 合规检查:');
const wcag = colorUtils.checkContrastWCAG('#333333', '#ffffff', 'AA', false);
console.log('  #333 on #white (AA):', wcag);

console.log('\n自动选择可读文字颜色:');
console.log('  深色背景 #000000 ->', colorUtils.getReadableTextColor('#000000'));
console.log('  浅色背景 #ffffff ->', colorUtils.getReadableTextColor('#ffffff'));
console.log('  中等背景 #ff0000 ->', colorUtils.getReadableTextColor('#ff0000'));

// ==================== 随机颜色生成 ====================

console.log('\n--- 随机颜色生成 ---');

console.log('随机颜色:');
for (let i = 0; i < 3; i++) {
  const rand = colorUtils.randomColor();
  console.log('  ', colorUtils.toCssString(rand, 'hex'));
}

console.log('\n随机鲜艳颜色:');
for (let i = 0; i < 3; i++) {
  const vibrant = colorUtils.randomVibrantColor();
  console.log('  ', colorUtils.toCssString(vibrant, 'hex'));
}

console.log('\n随机柔和颜色:');
for (let i = 0; i < 3; i++) {
  const pastel = colorUtils.randomPastelColor();
  console.log('  ', colorUtils.toCssString(pastel, 'hex'));
}

// ==================== 调色板生成 ====================

console.log('\n--- 调色板生成 ---');

console.log('渐变色 (#ff0000 到 #0000ff, 5 步):');
const gradient = colorUtils.gradientColors('#ff0000', '#0000ff', 5);
gradient.forEach((c, i) => console.log(`  ${i + 1}.`, colorUtils.toCssString(c, 'hex')));

console.log('\n单色配色方案 (#336699, 5 色):');
const mono = colorUtils.monochromaticPalette('#336699', 5);
mono.forEach((c, i) => console.log(`  ${i + 1}.`, colorUtils.toCssString(c, 'hex')));

console.log('\n类似色配色方案 (#ff0000):');
const analogous = colorUtils.analogousPalette('#ff0000');
analogous.forEach((c, i) => console.log(`  ${i + 1}.`, colorUtils.toCssString(c, 'hex')));

console.log('\n三色配色方案 (#ff0000):');
const triadic = colorUtils.triadicPalette('#ff0000');
triadic.forEach((c, i) => console.log(`  ${i + 1}.`, colorUtils.toCssString(c, 'hex')));

console.log('\n四色配色方案 (#ff0000):');
const tetradic = colorUtils.tetradicPalette('#ff0000');
tetradic.forEach((c, i) => console.log(`  ${i + 1}.`, colorUtils.toCssString(c, 'hex')));

console.log('\n互补配色方案 (#ff0000):');
const complementary = colorUtils.complementaryPalette('#ff0000');
complementary.forEach((c, i) => console.log(`  ${i + 1}.`, colorUtils.toCssString(c, 'hex')));

// ==================== 颜色距离 ====================

console.log('\n--- 颜色距离 ---');

console.log('颜色距离 (欧氏):');
console.log('  #ff0000 vs #ff0000:', colorUtils.colorDistance('#ff0000', '#ff0000'));
console.log('  #ff0000 vs #00ff00:', colorUtils.colorDistance('#ff0000', '#00ff00'));
console.log('  #000000 vs #ffffff:', colorUtils.colorDistance('#000000', '#ffffff'));

console.log('\nDelta E 2000 色差:');
console.log('  #ff0000 vs #ff0000:', colorUtils.deltaE2000('#ff0000', '#ff0000'));
console.log('  #ff0000 vs #fe0000:', colorUtils.deltaE2000('#ff0000', '#fe0000'));
console.log('  #ff0000 vs #00ff00:', colorUtils.deltaE2000('#ff0000', '#00ff00'));

console.log('\n查找最接近的颜色:');
const palette = ['#ff0000', '#00ff00', '#0000ff', '#ffff00', '#ff00ff', '#00ffff'];
const target = '#ff1111';
const closest = colorUtils.findClosestColor(target, palette);
console.log(`  目标: ${target}`);
console.log('  调色板:', palette);
console.log('  最接近:', colorUtils.toCssString(closest.color, 'hex'), `(索引: ${closest.index}, 距离: ${closest.distance.toFixed(2)})`);

// ==================== CSS 字符串输出 ====================

console.log('\n--- CSS 字符串输出 ---');

const color = { r: 255, g: 128, b: 64, a: 0.8 };
console.log('RGB(255, 128, 64, 0.8) 转换:');
console.log('  HEX:', colorUtils.toCssString(color, 'hex'));
console.log('  HEXA:', colorUtils.toCssString(color, 'hexa'));
console.log('  RGB:', colorUtils.toCssString(color, 'rgb'));
console.log('  RGBA:', colorUtils.toCssString(color, 'rgba'));
console.log('  HSL:', colorUtils.toCssString(color, 'hsl'));
console.log('  HSLA:', colorUtils.toCssString(color, 'hsla'));

// ==================== 工具函数 ====================

console.log('\n--- 工具函数 ---');

console.log('判断明暗:');
console.log('  #000000 isDark:', colorUtils.isDark('#000000'));
console.log('  #ffffff isDark:', colorUtils.isDark('#ffffff'));
console.log('  #000000 isLight:', colorUtils.isLight('#000000'));
console.log('  #ffffff isLight:', colorUtils.isLight('#ffffff'));

console.log('\n获取颜色名称:');
console.log('  #ff0000 ->', colorUtils.getColorName('#ff0000'));
console.log('  #00ff00 ->', colorUtils.getColorName('#00ff00'));
console.log('  #0000ff ->', colorUtils.getColorName('#0000ff'));
console.log('  #ff6347 ->', colorUtils.getColorName('#ff6347')); // tomato

console.log('\n验证颜色:');
console.log('  "#ff0000" isValid:', colorUtils.isValidColor('#ff0000'));
console.log('  "rgb(255,0,0)" isValid:', colorUtils.isValidColor('rgb(255,0,0)'));
console.log('  "red" isValid:', colorUtils.isValidColor('red'));
console.log('  "invalid" isValid:', colorUtils.isValidColor('invalid'));

console.log('\n比较颜色:');
console.log('  #ff0000 === #ff0000:', colorUtils.colorsEqual('#ff0000', '#ff0000'));
console.log('  #ff0000 === #00ff00:', colorUtils.colorsEqual('#ff0000', '#00ff00'));

// ==================== 实用场景示例 ====================

console.log('\n--- 实用场景 ---');

console.log('\n1. 创建按钮配色方案:');
const primaryColor = '#3366cc';
console.log('  主色:', primaryColor);
console.log('  悬停色:', colorUtils.toCssString(colorUtils.adjustBrightness(primaryColor, -10), 'hex'));
console.log('  点击色:', colorUtils.toCssString(colorUtils.adjustBrightness(primaryColor, -20), 'hex'));
console.log('  文字色:', colorUtils.getReadableTextColor(primaryColor));

console.log('\n2. 生成渐变背景:');
const bgGradient = colorUtils.gradientColors('#667eea', '#764ba2', 6);
console.log('  渐变色:', bgGradient.map(c => colorUtils.toCssString(c, 'hex')).join(' -> '));

console.log('\n3. 生成主题调色板:');
const baseColor = '#3498db';
const theme = {
  primary: baseColor,
  secondary: colorUtils.toCssString(colorUtils.adjustHue(baseColor, 30), 'hex'),
  accent: colorUtils.toCssString(colorUtils.complementColor(baseColor), 'hex'),
  light: colorUtils.toCssString(colorUtils.adjustBrightness(baseColor, 30), 'hex'),
  dark: colorUtils.toCssString(colorUtils.adjustBrightness(baseColor, -30), 'hex')
};
console.log('  主题调色板:', theme);

console.log('\n4. WCAG 可访问性检查:');
const fg = '#767676';
const bg = '#ffffff';
const wcagResult = colorUtils.checkContrastWCAG(fg, bg, 'AA', false);
console.log(`  前景: ${fg}, 背景: ${bg}`);
console.log(`  对比度: ${wcagResult.ratio}`);
console.log(`  AA 合规: ${wcagResult.passes ? '✓' : '✗'} (要求: ≥${wcagResult.requirement})`);

console.log('\n========================================');
console.log('  示例演示完成');
console.log('========================================\n');