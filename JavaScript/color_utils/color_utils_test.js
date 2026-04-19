/**
 * Color Utils 测试文件
 * 运行: node color_utils_test.js
 */

'use strict';

const assert = require('assert');
const colorUtils = require('./mod.js');

// 测试结果统计
let passed = 0;
let failed = 0;

function test(name, fn) {
  try {
    fn();
    passed++;
    console.log(`✅ ${name}`);
  } catch (e) {
    failed++;
    console.log(`❌ ${name}: ${e.message}`);
  }
}

console.log('\n========== Color Utils 测试 ==========\n');

// ==================== 解析测试 ====================

console.log('--- 解析测试 ---');

test('parseColor - HEX 格式', () => {
  const rgb = colorUtils.parseColor('#ff0000');
  assert.strictEqual(rgb.r, 255);
  assert.strictEqual(rgb.g, 0);
  assert.strictEqual(rgb.b, 0);
  assert.strictEqual(rgb.a, 1);
});

test('parseColor - 简写 HEX 格式', () => {
  const rgb = colorUtils.parseColor('#f00');
  assert.strictEqual(rgb.r, 255);
  assert.strictEqual(rgb.g, 0);
  assert.strictEqual(rgb.b, 0);
});

test('parseColor - 带 Alpha 的 HEX', () => {
  const rgb = colorUtils.parseColor('#ff000080');
  assert.strictEqual(rgb.r, 255);
  assert.strictEqual(rgb.g, 0);
  assert.strictEqual(rgb.b, 0);
  assert.ok(Math.abs(rgb.a - 0.5) < 0.01);
});

test('parseColor - RGB 格式', () => {
  const rgb = colorUtils.parseColor('rgb(255, 128, 64)');
  assert.strictEqual(rgb.r, 255);
  assert.strictEqual(rgb.g, 128);
  assert.strictEqual(rgb.b, 64);
});

test('parseColor - RGBA 格式', () => {
  const rgb = colorUtils.parseColor('rgba(255, 128, 64, 0.5)');
  assert.strictEqual(rgb.r, 255);
  assert.strictEqual(rgb.g, 128);
  assert.strictEqual(rgb.b, 64);
  assert.strictEqual(rgb.a, 0.5);
});

test('parseColor - HSL 格式', () => {
  const rgb = colorUtils.parseColor('hsl(120, 100%, 50%)');
  assert.strictEqual(rgb.r, 0);
  assert.strictEqual(rgb.g, 255);
  assert.strictEqual(rgb.b, 0);
});

test('parseColor - 命名颜色', () => {
  const rgb = colorUtils.parseColor('red');
  assert.strictEqual(rgb.r, 255);
  assert.strictEqual(rgb.g, 0);
  assert.strictEqual(rgb.b, 0);
});

test('parseColor - 无效颜色返回 null', () => {
  assert.strictEqual(colorUtils.parseColor('invalid'), null);
  assert.strictEqual(colorUtils.parseColor(123), null);
});

// ==================== 格式转换测试 ====================

console.log('\n--- 格式转换测试 ---');

test('rgbToHex', () => {
  assert.strictEqual(colorUtils.rgbToHex({ r: 255, g: 0, b: 0 }), '#ff0000');
  assert.strictEqual(colorUtils.rgbToHex({ r: 0, g: 255, b: 0 }), '#00ff00');
  assert.strictEqual(colorUtils.rgbToHex({ r: 0, g: 0, b: 255 }), '#0000ff');
});

test('rgbToHex with alpha', () => {
  const hex = colorUtils.rgbToHex({ r: 255, g: 0, b: 0, a: 0.5 }, true);
  assert.ok(hex.startsWith('#ff0000'));
});

test('rgbToHsl', () => {
  const hsl = colorUtils.rgbToHsl({ r: 255, g: 0, b: 0 });
  assert.strictEqual(hsl.h, 0);
  assert.strictEqual(hsl.s, 100);
  assert.strictEqual(hsl.l, 50);
});

test('hslToRgb', () => {
  const rgb = colorUtils.hslToRgb({ h: 0, s: 100, l: 50 });
  assert.strictEqual(rgb.r, 255);
  assert.strictEqual(rgb.g, 0);
  assert.strictEqual(rgb.b, 0);
});

test('rgbToHsl <-> hslToRgb 双向转换', () => {
  const original = { r: 128, g: 64, b: 200 };
  const hsl = colorUtils.rgbToHsl(original);
  const back = colorUtils.hslToRgb(hsl);
  assert.ok(Math.abs(original.r - back.r) <= 1);
  assert.ok(Math.abs(original.g - back.g) <= 1);
  assert.ok(Math.abs(original.b - back.b) <= 1);
});

test('rgbToHsv', () => {
  const hsv = colorUtils.rgbToHsv({ r: 255, g: 0, b: 0 });
  assert.strictEqual(hsv.h, 0);
  assert.strictEqual(hsv.s, 100);
  assert.strictEqual(hsv.v, 100);
});

test('hsvToRgb', () => {
  const rgb = colorUtils.hsvToRgb({ h: 0, s: 100, v: 100 });
  assert.strictEqual(rgb.r, 255);
  assert.strictEqual(rgb.g, 0);
  assert.strictEqual(rgb.b, 0);
});

test('rgbToCmyk', () => {
  const cmyk = colorUtils.rgbToCmyk({ r: 255, g: 0, b: 0 });
  assert.strictEqual(cmyk.c, 0);
  assert.strictEqual(cmyk.m, 100);
  assert.strictEqual(cmyk.y, 100);
  assert.strictEqual(cmyk.k, 0);
});

test('cmykToRgb', () => {
  const rgb = colorUtils.cmykToRgb({ c: 0, m: 100, y: 100, k: 0 });
  assert.strictEqual(rgb.r, 255);
  assert.strictEqual(rgb.g, 0);
  assert.strictEqual(rgb.b, 0);
});

test('rgbToLab', () => {
  const lab = colorUtils.rgbToLab({ r: 255, g: 0, b: 0 });
  // 红色的 LAB 值约为 L:53, A:80, B:67
  assert.ok(lab.l > 50 && lab.l < 55);
  assert.ok(lab.a > 70);
  assert.ok(lab.b > 50 && lab.b < 80);
});

test('labToRgb - 基本转换', () => {
  // 测试 LAB 转 RGB 转换功能
  // 使用一个简单的灰色测试
  const grayLab = { l: 50, a: 0, b: 0 };
  const grayRgb = colorUtils.labToRgb(grayLab);
  // 灰色应该在 RGB 各通道相近
  assert.ok(Math.abs(grayRgb.r - grayRgb.g) < 10);
  assert.ok(Math.abs(grayRgb.g - grayRgb.b) < 10);
});

// ==================== 颜色操作测试 ====================

console.log('\n--- 颜色操作测试 ---');

test('mixColors - 等比混合', () => {
  const mixed = colorUtils.mixColors('#ff0000', '#0000ff', 0.5);
  // #ff0000 = r:255, g:0, b:0
  // #0000ff = r:0, g:0, b:255
  // 50:50 mix = r:128, g:0, b:128
  assert.strictEqual(mixed.r, 128);
  assert.strictEqual(mixed.g, 0);
  assert.strictEqual(mixed.b, 128);
});

test('mixColors - 边界值', () => {
  const left = colorUtils.mixColors('#ff0000', '#0000ff', 0);
  assert.strictEqual(left.r, 255);
  
  const right = colorUtils.mixColors('#ff0000', '#0000ff', 1);
  assert.strictEqual(right.b, 255);
});

test('adjustBrightness - 增加亮度', () => {
  const lighter = colorUtils.adjustBrightness('#333333', 50);
  assert.ok(lighter.r > 51);
});

test('adjustBrightness - 降低亮度', () => {
  const darker = colorUtils.adjustBrightness('#999999', -50);
  assert.ok(darker.r < 153);
});

test('adjustSaturation', () => {
  const more = colorUtils.adjustSaturation('#808080', 50);
  const hsl = colorUtils.rgbToHsl(more);
  assert.ok(hsl.s > 0);
});

test('adjustHue', () => {
  const rotated = colorUtils.adjustHue('#ff0000', 120);
  const hsl = colorUtils.rgbToHsl(rotated);
  assert.strictEqual(hsl.h, 120);
});

test('adjustAlpha', () => {
  const withAlpha = colorUtils.adjustAlpha('#ff0000', 0.5);
  assert.strictEqual(withAlpha.a, 0.5);
});

test('invertColor', () => {
  const inverted = colorUtils.invertColor('#000000');
  assert.strictEqual(inverted.r, 255);
  assert.strictEqual(inverted.g, 255);
  assert.strictEqual(inverted.b, 255);
});

test('grayscaleColor', () => {
  const gray = colorUtils.grayscaleColor('#ff0000');
  assert.strictEqual(gray.r, gray.g);
  assert.strictEqual(gray.g, gray.b);
});

test('complementColor', () => {
  const comp = colorUtils.complementColor('#ff0000');
  const hsl = colorUtils.rgbToHsl(comp);
  assert.strictEqual(hsl.h, 180);
});

// ==================== 对比度测试 ====================

console.log('\n--- 对比度测试 ---');

test('getLuminance', () => {
  const whiteLum = colorUtils.getLuminance({ r: 255, g: 255, b: 255 });
  const blackLum = colorUtils.getLuminance({ r: 0, g: 0, b: 0 });
  assert.strictEqual(whiteLum, 1);
  assert.strictEqual(blackLum, 0);
});

test('getContrastRatio - 黑白对比度', () => {
  const ratio = colorUtils.getContrastRatio('#000000', '#ffffff');
  assert.strictEqual(ratio, 21);
});

test('getContrastRatio - 相同颜色', () => {
  const ratio = colorUtils.getContrastRatio('#ff0000', '#ff0000');
  assert.strictEqual(ratio, 1);
});

test('checkContrastWCAG - AA 合规', () => {
  const result = colorUtils.checkContrastWCAG('#000000', '#ffffff', 'AA', false);
  assert.strictEqual(result.passes, true);
  assert.strictEqual(result.ratio, 21);
});

test('checkContrastWCAG - AAA 要求更严格', () => {
  const result = colorUtils.checkContrastWCAG('#777777', '#ffffff', 'AAA', false);
  assert.strictEqual(result.passes, false);
  assert.strictEqual(result.requirement, 7);
});

test('getReadableTextColor - 浅色背景', () => {
  const text = colorUtils.getReadableTextColor('#ffffff');
  assert.strictEqual(text, '#000000');
});

test('getReadableTextColor - 深色背景', () => {
  const text = colorUtils.getReadableTextColor('#000000');
  assert.strictEqual(text, '#ffffff');
});

// ==================== 颜色生成测试 ====================

console.log('\n--- 颜色生成测试 ---');

test('randomColor - 生成有效颜色', () => {
  const color = colorUtils.randomColor();
  assert.ok(color.r >= 0 && color.r <= 255);
  assert.ok(color.g >= 0 && color.g <= 255);
  assert.ok(color.b >= 0 && color.b <= 255);
  assert.strictEqual(color.a, 1);
});

test('randomColor - 带透明度', () => {
  const color = colorUtils.randomColor({ alpha: true });
  assert.ok(color.a >= 0 && color.a <= 1);
});

test('randomHex', () => {
  const hex = colorUtils.randomHex();
  assert.ok(/^#[0-9a-f]{6}$/i.test(hex));
});

test('randomHsl', () => {
  const hsl = colorUtils.randomHsl();
  assert.ok(hsl.h >= 0 && hsl.h <= 360);
  assert.ok(hsl.s >= 0 && hsl.s <= 100);
  assert.ok(hsl.l >= 0 && hsl.l <= 100);
});

test('randomVibrantColor - 高饱和度', () => {
  const rgb = colorUtils.randomVibrantColor();
  const hsl = colorUtils.rgbToHsl(rgb);
  assert.ok(hsl.s >= 70);
});

test('randomPastelColor - 高亮度', () => {
  const rgb = colorUtils.randomPastelColor();
  const hsl = colorUtils.rgbToHsl(rgb);
  assert.ok(hsl.l >= 75);
});

// ==================== 调色板生成测试 ====================

console.log('\n--- 调色板生成测试 ---');

test('gradientColors', () => {
  const gradient = colorUtils.gradientColors('#000000', '#ffffff', 5);
  assert.strictEqual(gradient.length, 5);
  assert.strictEqual(gradient[0].r, 0);
  assert.strictEqual(gradient[4].r, 255);
});

test('monochromaticPalette', () => {
  const palette = colorUtils.monochromaticPalette('#ff0000', 5);
  assert.strictEqual(palette.length, 5);
  const hslValues = palette.map(c => colorUtils.rgbToHsl(c).h);
  hslValues.forEach(h => assert.strictEqual(h, 0));
});

test('analogousPalette', () => {
  const palette = colorUtils.analogousPalette('#ff0000');
  assert.strictEqual(palette.length, 3);
});

test('triadicPalette', () => {
  const palette = colorUtils.triadicPalette('#ff0000');
  assert.strictEqual(palette.length, 3);
});

test('tetradicPalette', () => {
  const palette = colorUtils.tetradicPalette('#ff0000');
  assert.strictEqual(palette.length, 4);
});

test('complementaryPalette', () => {
  const palette = colorUtils.complementaryPalette('#ff0000');
  assert.strictEqual(palette.length, 2);
  const hsl1 = colorUtils.rgbToHsl(palette[0]);
  const hsl2 = colorUtils.rgbToHsl(palette[1]);
  assert.strictEqual(Math.abs(hsl1.h - hsl2.h), 180);
});

test('splitComplementaryPalette', () => {
  const palette = colorUtils.splitComplementaryPalette('#ff0000');
  assert.strictEqual(palette.length, 3);
});

// ==================== 颜色距离测试 ====================

console.log('\n--- 颜色距离测试 ---');

test('colorDistance - 相同颜色', () => {
  const dist = colorUtils.colorDistance('#ff0000', '#ff0000');
  assert.strictEqual(dist, 0);
});

test('colorDistance - 最大距离', () => {
  const dist = colorUtils.colorDistance('#000000', '#ffffff');
  assert.ok(Math.abs(dist - 441.67) < 0.1);
});

test('deltaE2000 - 相同颜色', () => {
  const de = colorUtils.deltaE2000('#ff0000', '#ff0000');
  assert.strictEqual(de, 0);
});

test('deltaE2000 - 不同颜色', () => {
  const de = colorUtils.deltaE2000('#ff0000', '#00ff00');
  assert.ok(de > 50);
});

test('findClosestColor', () => {
  const colors = ['#ff0000', '#00ff00', '#0000ff'];
  const result = colorUtils.findClosestColor('#ff1111', colors);
  assert.strictEqual(result.index, 0);
});

// ==================== 工具函数测试 ====================

console.log('\n--- 工具函数测试 ---');

test('isDark - 黑色', () => {
  assert.strictEqual(colorUtils.isDark('#000000'), true);
});

test('isDark - 白色', () => {
  assert.strictEqual(colorUtils.isDark('#ffffff'), false);
});

test('isLight', () => {
  assert.strictEqual(colorUtils.isLight('#ffffff'), true);
  assert.strictEqual(colorUtils.isLight('#000000'), false);
});

test('toCssString - hex', () => {
  const css = colorUtils.toCssString({ r: 255, g: 0, b: 0 }, 'hex');
  assert.strictEqual(css, '#ff0000');
});

test('toCssString - rgb', () => {
  const css = colorUtils.toCssString({ r: 255, g: 0, b: 0 }, 'rgb');
  assert.strictEqual(css, 'rgb(255, 0, 0)');
});

test('toCssString - rgba', () => {
  const css = colorUtils.toCssString({ r: 255, g: 0, b: 0, a: 0.5 }, 'rgba');
  assert.strictEqual(css, 'rgba(255, 0, 0, 0.5)');
});

test('toCssString - hsl', () => {
  const css = colorUtils.toCssString({ r: 255, g: 0, b: 0 }, 'hsl');
  assert.strictEqual(css, 'hsl(0, 100%, 50%)');
});

test('getColorName', () => {
  assert.strictEqual(colorUtils.getColorName('#ff0000'), 'red');
  assert.strictEqual(colorUtils.getColorName('#00ff00'), 'lime');
});

test('isValidColor', () => {
  assert.strictEqual(colorUtils.isValidColor('#ff0000'), true);
  assert.strictEqual(colorUtils.isValidColor('rgb(255, 0, 0)'), true);
  assert.strictEqual(colorUtils.isValidColor('hsl(0, 100%, 50%)'), true);
  assert.strictEqual(colorUtils.isValidColor('red'), true);
  assert.strictEqual(colorUtils.isValidColor('invalid'), false);
});

test('cloneColor', () => {
  const original = { r: 255, g: 0, b: 0 };
  const cloned = colorUtils.cloneColor(original);
  assert.notStrictEqual(cloned, original);
  assert.deepStrictEqual(cloned, original);
});

test('colorsEqual', () => {
  assert.strictEqual(colorUtils.colorsEqual('#ff0000', '#ff0000'), true);
  assert.strictEqual(colorUtils.colorsEqual('#ff0000', '#00ff00'), false);
  assert.strictEqual(colorUtils.colorsEqual('#ff0000', { r: 255, g: 0, b: 0 }), true);
});

// ==================== 输出测试结果 ====================

console.log('\n========================================');
console.log(`测试结果: ${passed} 通过, ${failed} 失败`);
console.log('========================================\n');

process.exit(failed === 0 ? 0 : 1);