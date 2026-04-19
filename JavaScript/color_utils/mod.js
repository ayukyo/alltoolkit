/**
 * Color Utils - 颜色处理工具库
 * 零外部依赖的 JavaScript 颜色处理工具
 * 
 * 功能：
 * - 颜色格式转换（HEX、RGB、HSL、HSV、CMYK、LAB）
 * - 颜色混合与渐变
 * - 亮度/饱和度/透明度调整
 * - 对比度计算与 WCAG 合规检查
 * - 随机颜色生成
 * - 颜色解析与验证
 * - 调色板生成
 */

'use strict';

// ==================== 类型定义 ====================

/**
 * @typedef {Object} RGB - RGB 颜色对象
 * @property {number} r - 红色通道 (0-255)
 * @property {number} g - 绿色通道 (0-255)
 * @property {number} b - 蓝色通道 (0-255)
 * @property {number} [a] - Alpha 通道 (0-1)
 */

/**
 * @typedef {Object} HSL - HSL 颜色对象
 * @property {number} h - 色相 (0-360)
 * @property {number} s - 饱和度 (0-100)
 * @property {number} l - 亮度 (0-100)
 * @property {number} [a] - Alpha 通道 (0-1)
 */

/**
 * @typedef {Object} HSV - HSV 颜色对象
 * @property {number} h - 色相 (0-360)
 * @property {number} s - 饱和度 (0-100)
 * @property {number} v - 明度 (0-100)
 * @property {number} [a] - Alpha 通道 (0-1)
 */

/**
 * @typedef {Object} CMYK - CMYK 颜色对象
 * @property {number} c - 青色 (0-100)
 * @property {number} m - 品红 (0-100)
 * @property {number} y - 黄色 (0-100)
 * @property {number} k - 黑色 (0-100)
 */

/**
 * @typedef {Object} LAB - LAB 颜色对象
 * @property {number} l - 亮度 (0-100)
 * @property {number} a - 绿红轴 (-128 到 127)
 * @property {number} b - 蓝黄轴 (-128 到 127)
 */

// ==================== 常量 ====================

const NAMED_COLORS = {
  'transparent': '#00000000',
  'black': '#000000',
  'white': '#ffffff',
  'red': '#ff0000',
  'green': '#008000',
  'blue': '#0000ff',
  'yellow': '#ffff00',
  'cyan': '#00ffff',
  'magenta': '#ff00ff',
  'gray': '#808080',
  'grey': '#808080',
  'silver': '#c0c0c0',
  'maroon': '#800000',
  'olive': '#808000',
  'lime': '#00ff00',
  'aqua': '#00ffff',
  'teal': '#008080',
  'navy': '#000080',
  'fuchsia': '#ff00ff',
  'purple': '#800080',
  'orange': '#ffa500',
  'pink': '#ffc0cb',
  'coral': '#ff7f50',
  'salmon': '#fa8072',
  'tomato': '#ff6347',
  'gold': '#ffd700',
  'khaki': '#f0e68c',
  'violet': '#ee82ee',
  'indigo': '#4b0082',
  'crimson': '#dc143c',
  'chocolate': '#d2691e',
  'tan': '#d2b48c',
  'sienna': '#a0522d',
  'brown': '#a52a2a',
  'beige': '#f5f5dc',
  'ivory': '#fffff0',
  'lavender': '#e6e6fa',
  'linen': '#faf0e6',
  'wheat': '#f5deb3',
  'azure': '#f0ffff',
  'mintcream': '#f5fffa',
  'snow': '#fffafa',
  'seashell': '#fff5ee'
};

// ==================== 解析函数 ====================

/**
 * 解析颜色字符串为 RGB 对象
 * 支持格式：HEX、RGB、RGBA、HSL、HSLA、颜色名称
 * @param {string} color - 颜色字符串
 * @returns {RGB|null} RGB 颜色对象或 null
 */
function parseColor(color) {
  if (typeof color !== 'string') return null;
  
  const trimmed = color.trim().toLowerCase();
  
  // 检查命名颜色
  if (NAMED_COLORS[trimmed]) {
    return parseHex(NAMED_COLORS[trimmed]);
  }
  
  // HEX 格式
  if (trimmed.startsWith('#')) {
    return parseHex(trimmed);
  }
  
  // RGB/RGBA 格式
  if (trimmed.startsWith('rgb')) {
    return parseRgb(trimmed);
  }
  
  // HSL/HSLA 格式
  if (trimmed.startsWith('hsl')) {
    return parseHsl(trimmed);
  }
  
  return null;
}

/**
 * 解析 HEX 颜色
 * @param {string} hex - HEX 颜色字符串
 * @returns {RGB|null}
 */
function parseHex(hex) {
  if (typeof hex !== 'string') return null;
  
  let h = hex.trim().toLowerCase();
  if (h.startsWith('#')) h = h.slice(1);
  
  // 扩展简写格式
  if (h.length === 3) {
    h = h[0] + h[0] + h[1] + h[1] + h[2] + h[2];
  } else if (h.length === 4) {
    h = h[0] + h[0] + h[1] + h[1] + h[2] + h[2] + h[3] + h[3];
  }
  
  if (!/^[0-9a-f]{6}([0-9a-f]{2})?$/i.test(h)) return null;
  
  const r = parseInt(h.slice(0, 2), 16);
  const g = parseInt(h.slice(2, 4), 16);
  const b = parseInt(h.slice(4, 6), 16);
  const a = h.length === 8 ? parseInt(h.slice(6, 8), 16) / 255 : 1;
  
  return { r, g, b, a };
}

/**
 * 解析 RGB/RGBA 颜色字符串
 * @param {string} str - RGB/RGBA 字符串
 * @returns {RGB|null}
 */
function parseRgb(str) {
  const match = str.match(/rgba?\s*\(\s*(\d+%?)\s*[,\s]\s*(\d+%?)\s*[,\s]\s*(\d+%?)\s*(?:[,\/]\s*(\d*\.?\d+%?))?\s*\)/i);
  if (!match) return null;
  
  const parseValue = (val, isAlpha = false) => {
    if (!val) return isAlpha ? 1 : undefined;
    if (val.endsWith('%')) {
      return parseFloat(val) / 100;
    }
    return parseFloat(val);
  };
  
  const r = parseValue(match[1]) * (match[1].endsWith('%') ? 255 : 1);
  const g = parseValue(match[2]) * (match[2].endsWith('%') ? 255 : 1);
  const b = parseValue(match[3]) * (match[3].endsWith('%') ? 255 : 1);
  const a = parseValue(match[4], true);
  
  return { 
    r: Math.round(r), 
    g: Math.round(g), 
    b: Math.round(b), 
    a: Math.min(1, Math.max(0, a)) 
  };
}

/**
 * 解析 HSL/HSLA 颜色字符串
 * @param {string} str - HSL/HSLA 字符串
 * @returns {RGB|null}
 */
function parseHsl(str) {
  const match = str.match(/hsla?\s*\(\s*(\d+)\s*[,\s]\s*(\d+)%?\s*[,\s]\s*(\d+)%?\s*(?:[,\/]\s*(\d*\.?\d+%?))?\s*\)/i);
  if (!match) return null;
  
  const h = parseFloat(match[1]);
  const s = parseFloat(match[2]) / 100;
  const l = parseFloat(match[3]) / 100;
  const a = match[4] ? (match[4].endsWith('%') ? parseFloat(match[4]) / 100 : parseFloat(match[4])) : 1;
  
  return hslToRgb({ h, s: s * 100, l: l * 100, a });
}

// ==================== 格式转换函数 ====================

/**
 * RGB 转 HEX
 * @param {RGB} rgb - RGB 颜色对象
 * @param {boolean} includeAlpha - 是否包含 Alpha 通道
 * @returns {string} HEX 颜色字符串
 */
function rgbToHex(rgb, includeAlpha = false) {
  const toHex = (n) => Math.round(Math.min(255, Math.max(0, n))).toString(16).padStart(2, '0');
  
  let hex = '#' + toHex(rgb.r) + toHex(rgb.g) + toHex(rgb.b);
  if (includeAlpha && rgb.a !== undefined && rgb.a !== 1) {
    hex += toHex(Math.round(rgb.a * 255));
  }
  return hex;
}

/**
 * RGB 转 HSL
 * @param {RGB} rgb - RGB 颜色对象
 * @returns {HSL}
 */
function rgbToHsl(rgb) {
  const r = rgb.r / 255;
  const g = rgb.g / 255;
  const b = rgb.b / 255;
  
  const max = Math.max(r, g, b);
  const min = Math.min(r, g, b);
  const d = max - min;
  
  let h = 0;
  let s = 0;
  const l = (max + min) / 2;
  
  if (d !== 0) {
    s = l > 0.5 ? d / (2 - max - min) : d / (max + min);
    
    switch (max) {
      case r: h = ((g - b) / d + (g < b ? 6 : 0)) / 6; break;
      case g: h = ((b - r) / d + 2) / 6; break;
      case b: h = ((r - g) / d + 4) / 6; break;
    }
  }
  
  return { 
    h: Math.round(h * 360), 
    s: Math.round(s * 100), 
    l: Math.round(l * 100),
    a: rgb.a
  };
}

/**
 * HSL 转 RGB
 * @param {HSL} hsl - HSL 颜色对象
 * @returns {RGB}
 */
function hslToRgb(hsl) {
  const h = hsl.h / 360;
  const s = hsl.s / 100;
  const l = hsl.l / 100;
  
  let r, g, b;
  
  if (s === 0) {
    r = g = b = l;
  } else {
    const hue2rgb = (p, q, t) => {
      if (t < 0) t += 1;
      if (t > 1) t -= 1;
      if (t < 1/6) return p + (q - p) * 6 * t;
      if (t < 1/2) return q;
      if (t < 2/3) return p + (q - p) * (2/3 - t) * 6;
      return p;
    };
    
    const q = l < 0.5 ? l * (1 + s) : l + s - l * s;
    const p = 2 * l - q;
    
    r = hue2rgb(p, q, h + 1/3);
    g = hue2rgb(p, q, h);
    b = hue2rgb(p, q, h - 1/3);
  }
  
  return { 
    r: Math.round(r * 255), 
    g: Math.round(g * 255), 
    b: Math.round(b * 255),
    a: hsl.a
  };
}

/**
 * RGB 转 HSV
 * @param {RGB} rgb - RGB 颜色对象
 * @returns {HSV}
 */
function rgbToHsv(rgb) {
  const r = rgb.r / 255;
  const g = rgb.g / 255;
  const b = rgb.b / 255;
  
  const max = Math.max(r, g, b);
  const min = Math.min(r, g, b);
  const d = max - min;
  
  let h = 0;
  const s = max === 0 ? 0 : d / max;
  const v = max;
  
  if (d !== 0) {
    switch (max) {
      case r: h = ((g - b) / d + (g < b ? 6 : 0)) / 6; break;
      case g: h = ((b - r) / d + 2) / 6; break;
      case b: h = ((r - g) / d + 4) / 6; break;
    }
  }
  
  return { 
    h: Math.round(h * 360), 
    s: Math.round(s * 100), 
    v: Math.round(v * 100),
    a: rgb.a
  };
}

/**
 * HSV 转 RGB
 * @param {HSV} hsv - HSV 颜色对象
 * @returns {RGB}
 */
function hsvToRgb(hsv) {
  const h = hsv.h / 360;
  const s = hsv.s / 100;
  const v = hsv.v / 100;
  
  let r, g, b;
  
  const i = Math.floor(h * 6);
  const f = h * 6 - i;
  const p = v * (1 - s);
  const q = v * (1 - f * s);
  const t = v * (1 - (1 - f) * s);
  
  switch (i % 6) {
    case 0: r = v; g = t; b = p; break;
    case 1: r = q; g = v; b = p; break;
    case 2: r = p; g = v; b = t; break;
    case 3: r = p; g = q; b = v; break;
    case 4: r = t; g = p; b = v; break;
    case 5: r = v; g = p; b = q; break;
  }
  
  return { 
    r: Math.round(r * 255), 
    g: Math.round(g * 255), 
    b: Math.round(b * 255),
    a: hsv.a
  };
}

/**
 * RGB 转 CMYK
 * @param {RGB} rgb - RGB 颜色对象
 * @returns {CMYK}
 */
function rgbToCmyk(rgb) {
  const r = rgb.r / 255;
  const g = rgb.g / 255;
  const b = rgb.b / 255;
  
  const k = 1 - Math.max(r, g, b);
  
  if (k === 1) {
    return { c: 0, m: 0, y: 0, k: 100 };
  }
  
  const c = (1 - r - k) / (1 - k);
  const m = (1 - g - k) / (1 - k);
  const y = (1 - b - k) / (1 - k);
  
  return { 
    c: Math.round(c * 100), 
    m: Math.round(m * 100), 
    y: Math.round(y * 100), 
    k: Math.round(k * 100) 
  };
}

/**
 * CMYK 转 RGB
 * @param {CMYK} cmyk - CMYK 颜色对象
 * @returns {RGB}
 */
function cmykToRgb(cmyk) {
  const k = cmyk.k / 100;
  const c = cmyk.c / 100;
  const m = cmyk.m / 100;
  const y = cmyk.y / 100;
  
  const r = 255 * (1 - c) * (1 - k);
  const g = 255 * (1 - m) * (1 - k);
  const b = 255 * (1 - y) * (1 - k);
  
  return { 
    r: Math.round(r), 
    g: Math.round(g), 
    b: Math.round(b) 
  };
}

/**
 * RGB 转 LAB
 * @param {RGB} rgb - RGB 颜色对象
 * @returns {LAB}
 */
function rgbToLab(rgb) {
  // 先转 XYZ
  let r = rgb.r / 255;
  let g = rgb.g / 255;
  let b = rgb.b / 255;
  
  // sRGB 校正
  r = r > 0.04045 ? Math.pow((r + 0.055) / 1.055, 2.4) : r / 12.92;
  g = g > 0.04045 ? Math.pow((g + 0.055) / 1.055, 2.4) : g / 12.92;
  b = b > 0.04045 ? Math.pow((b + 0.055) / 1.055, 2.4) : b / 12.92;
  
  r *= 100;
  g *= 100;
  b *= 100;
  
  // D65 白点
  const x = r * 0.4124564 + g * 0.3575761 + b * 0.1804375;
  const y = r * 0.2126729 + g * 0.7151522 + b * 0.0721750;
  const z = r * 0.0193339 + g * 0.1191920 + b * 0.9503041;
  
  // XYZ 转 LAB
  const refX = 95.047;
  const refY = 100.000;
  const refZ = 108.883;
  
  const f = (t) => t > 0.008856 ? Math.cbrt(t) : (7.787 * t) + (16 / 116);
  
  const fx = f(x / refX);
  const fy = f(y / refY);
  const fz = f(z / refZ);
  
  const L = (116 * fy) - 16;
  const a = 500 * (fx - fy);
  const bVal = 200 * (fy - fz);
  
  return { 
    l: Math.round(L * 100) / 100, 
    a: Math.round(a * 100) / 100, 
    b: Math.round(bVal * 100) / 100 
  };
}

/**
 * LAB 转 RGB
 * @param {LAB} lab - LAB 颜色对象
 * @returns {RGB}
 */
function labToRgb(lab) {
  // LAB 转 XYZ
  const refX = 95.047;
  const refY = 100.000;
  const refZ = 108.883;
  
  const fy = (lab.l + 16) / 116;
  const fx = lab.a / 500 + fy;
  const fz = fy - lab.b / 200;
  
  const f = (t) => {
    const t3 = t * t * t;
    return t3 > 0.008856 ? t3 : (t - 16 / 116) / 7.787;
  };
  
  const x = refX * f(fx);
  const y = refY * f(fy);
  const z = refZ * f(fz);
  
  // XYZ 转 RGB（使用逆矩阵）
  const r = x * 3.2404542 - y * 1.5371385 - z * 0.4985314;
  const g = -x * 0.9692660 + y * 1.8760108 + z * 0.0415560;
  const b = x * 0.0556434 - y * 0.2040259 + z * 1.0572252;
  
  // 反 sRGB 校正
  const gamma = (c) => c > 0.0031308 ? 1.055 * Math.pow(c, 1 / 2.4) - 0.055 : 12.92 * c;
  
  return { 
    r: Math.round(Math.min(255, Math.max(0, gamma(r / 100) * 255))), 
    g: Math.round(Math.min(255, Math.max(0, gamma(g / 100) * 255))), 
    b: Math.round(Math.min(255, Math.max(0, gamma(b / 100) * 255))) 
  };
}

// ==================== 颜色操作函数 ====================

/**
 * 混合两个颜色
 * @param {string|RGB} color1 - 颜色 1
 * @param {string|RGB} color2 - 颜色 2
 * @param {number} ratio - 混合比例 (0-1)，0 为 color1，1 为 color2
 * @returns {RGB|null}
 */
function mixColors(color1, color2, ratio = 0.5) {
  const rgb1 = typeof color1 === 'string' ? parseColor(color1) : color1;
  const rgb2 = typeof color2 === 'string' ? parseColor(color2) : color2;
  
  if (!rgb1 || !rgb2) return null;
  
  ratio = Math.min(1, Math.max(0, ratio));
  
  return {
    r: Math.round(rgb1.r + (rgb2.r - rgb1.r) * ratio),
    g: Math.round(rgb1.g + (rgb2.g - rgb1.g) * ratio),
    b: Math.round(rgb1.b + (rgb2.b - rgb1.b) * ratio),
    a: rgb1.a + (rgb2.a - rgb1.a) * ratio
  };
}

/**
 * 调整颜色亮度
 * @param {string|RGB} color - 颜色
 * @param {number} amount - 亮度调整量 (-100 到 100)
 * @returns {RGB|null}
 */
function adjustBrightness(color, amount) {
  const rgb = typeof color === 'string' ? parseColor(color) : color;
  if (!rgb) return null;
  
  const hsl = rgbToHsl(rgb);
  hsl.l = Math.min(100, Math.max(0, hsl.l + amount));
  
  return hslToRgb(hsl);
}

/**
 * 调整颜色饱和度
 * @param {string|RGB} color - 颜色
 * @param {number} amount - 饱和度调整量 (-100 到 100)
 * @returns {RGB|null}
 */
function adjustSaturation(color, amount) {
  const rgb = typeof color === 'string' ? parseColor(color) : color;
  if (!rgb) return null;
  
  const hsl = rgbToHsl(rgb);
  hsl.s = Math.min(100, Math.max(0, hsl.s + amount));
  
  return hslToRgb(hsl);
}

/**
 * 调整颜色色相
 * @param {string|RGB} color - 颜色
 * @param {number} degrees - 色相旋转角度 (-360 到 360)
 * @returns {RGB|null}
 */
function adjustHue(color, degrees) {
  const rgb = typeof color === 'string' ? parseColor(color) : color;
  if (!rgb) return null;
  
  const hsl = rgbToHsl(rgb);
  hsl.h = ((hsl.h + degrees) % 360 + 360) % 360;
  
  return hslToRgb(hsl);
}

/**
 * 调整颜色透明度
 * @param {string|RGB} color - 颜色
 * @param {number} alpha - 新的透明度值 (0-1) 或调整量
 * @param {boolean} [relative=false] - 是否为相对调整
 * @returns {RGB|null}
 */
function adjustAlpha(color, alpha, relative = false) {
  const rgb = typeof color === 'string' ? parseColor(color) : color;
  if (!rgb) return null;
  
  const newAlpha = relative ? (rgb.a || 1) + alpha : alpha;
  
  return { ...rgb, a: Math.min(1, Math.max(0, newAlpha)) };
}

/**
 * 反转颜色
 * @param {string|RGB} color - 颜色
 * @returns {RGB|null}
 */
function invertColor(color) {
  const rgb = typeof color === 'string' ? parseColor(color) : color;
  if (!rgb) return null;
  
  return {
    r: 255 - rgb.r,
    g: 255 - rgb.g,
    b: 255 - rgb.b,
    a: rgb.a
  };
}

/**
 * 灰度化颜色
 * @param {string|RGB} color - 颜色
 * @returns {RGB|null}
 */
function grayscaleColor(color) {
  const rgb = typeof color === 'string' ? parseColor(color) : color;
  if (!rgb) return null;
  
  // 使用 ITU-R BT.601 标准加权
  const gray = Math.round(0.299 * rgb.r + 0.587 * rgb.g + 0.114 * rgb.b);
  
  return { r: gray, g: gray, b: gray, a: rgb.a };
}

/**
 * 获取对比色（互补色）
 * @param {string|RGB} color - 颜色
 * @returns {RGB|null}
 */
function complementColor(color) {
  const rgb = typeof color === 'string' ? parseColor(color) : color;
  if (!rgb) return null;
  
  return adjustHue(rgb, 180);
}

// ==================== 对比度与可访问性 ====================

/**
 * 计算相对亮度
 * @param {RGB} rgb - RGB 颜色对象
 * @returns {number} 相对亮度 (0-1)
 */
function getLuminance(rgb) {
  const r = rgb.r / 255;
  const g = rgb.g / 255;
  const b = rgb.b / 255;
  
  const R = r <= 0.03928 ? r / 12.92 : Math.pow((r + 0.055) / 1.055, 2.4);
  const G = g <= 0.03928 ? g / 12.92 : Math.pow((g + 0.055) / 1.055, 2.4);
  const B = b <= 0.03928 ? b / 12.92 : Math.pow((b + 0.055) / 1.055, 2.4);
  
  return 0.2126 * R + 0.7152 * G + 0.0722 * B;
}

/**
 * 计算两个颜色的对比度
 * @param {string|RGB} color1 - 颜色 1
 * @param {string|RGB} color2 - 颜色 2
 * @returns {number|null} 对比度 (1-21)
 */
function getContrastRatio(color1, color2) {
  const rgb1 = typeof color1 === 'string' ? parseColor(color1) : color1;
  const rgb2 = typeof color2 === 'string' ? parseColor(color2) : color2;
  
  if (!rgb1 || !rgb2) return null;
  
  const L1 = getLuminance(rgb1);
  const L2 = getLuminance(rgb2);
  
  const lighter = Math.max(L1, L2);
  const darker = Math.min(L1, L2);
  
  return (lighter + 0.05) / (darker + 0.05);
}

/**
 * 检查 WCAG 对比度合规性
 * @param {string|RGB} foreground - 前景色
 * @param {string|RGB} background - 背景色
 * @param {string} [level='AA'] - WCAG 级别 ('AA' 或 'AAA')
 * @param {boolean} [largeText=false] - 是否为大文本
 * @returns {Object|null} 合规性检查结果
 */
function checkContrastWCAG(foreground, background, level = 'AA', largeText = false) {
  const contrast = getContrastRatio(foreground, background);
  if (contrast === null) return null;
  
  // WCAG 2.1 要求
  const requirements = {
    AA: { normal: 4.5, large: 3 },
    AAA: { normal: 7, large: 4.5 }
  };
  
  const requirement = requirements[level]?.[largeText ? 'large' : 'normal'] || 4.5;
  
  return {
    ratio: Math.round(contrast * 100) / 100,
    passes: contrast >= requirement,
    level,
    largeText,
    requirement,
    difference: Math.round((contrast - requirement) * 100) / 100
  };
}

/**
 * 获取适合阅读的文字颜色（黑或白）
 * @param {string|RGB} backgroundColor - 背景色
 * @returns {string} 适合的文字颜色 (#000 或 #fff)
 */
function getReadableTextColor(backgroundColor) {
  const rgb = typeof backgroundColor === 'string' ? parseColor(backgroundColor) : backgroundColor;
  if (!rgb) return '#000000';
  
  const luminance = getLuminance(rgb);
  return luminance > 0.179 ? '#000000' : '#ffffff';
}

// ==================== 颜色生成函数 ====================

/**
 * 生成随机颜色
 * @param {Object} [options] - 选项
 * @param {boolean} [options.alpha=false] - 是否包含透明度
 * @returns {RGB}
 */
function randomColor(options = {}) {
  return {
    r: Math.floor(Math.random() * 256),
    g: Math.floor(Math.random() * 256),
    b: Math.floor(Math.random() * 256),
    a: options.alpha ? Math.random() : 1
  };
}

/**
 * 生成随机 HEX 颜色
 * @param {boolean} [includeAlpha=false] - 是否包含透明度
 * @returns {string}
 */
function randomHex(includeAlpha = false) {
  const rgb = randomColor({ alpha: includeAlpha });
  return rgbToHex(rgb, includeAlpha);
}

/**
 * 生成随机 HSL 颜色（可指定范围）
 * @param {Object} [ranges] - 色相/饱和度/亮度范围
 * @returns {HSL}
 */
function randomHsl(ranges = {}) {
  const { hMin = 0, hMax = 360, sMin = 0, sMax = 100, lMin = 0, lMax = 100 } = ranges;
  
  return {
    h: Math.floor(Math.random() * (hMax - hMin) + hMin),
    s: Math.floor(Math.random() * (sMax - sMin) + sMin),
    l: Math.floor(Math.random() * (lMax - lMin) + lMin)
  };
}

/**
 * 生成随机鲜艳颜色（高饱和度）
 * @returns {RGB}
 */
function randomVibrantColor() {
  const hsl = randomHsl({ sMin: 70, sMax: 100, lMin: 45, lMax: 55 });
  return hslToRgb(hsl);
}

/**
 * 生成随机柔和颜色
 * @returns {RGB}
 */
function randomPastelColor() {
  const hsl = randomHsl({ sMin: 50, sMax: 80, lMin: 75, lMax: 90 });
  return hslToRgb(hsl);
}

// ==================== 调色板生成 ====================

/**
 * 生成渐变色数组
 * @param {string|RGB} startColor - 起始颜色
 * @param {string|RGB} endColor - 结束颜色
 * @param {number} steps - 步数
 * @returns {RGB[]|null}
 */
function gradientColors(startColor, endColor, steps) {
  const start = typeof startColor === 'string' ? parseColor(startColor) : startColor;
  const end = typeof endColor === 'string' ? parseColor(endColor) : endColor;
  
  if (!start || !end || steps < 2) return null;
  
  const colors = [];
  for (let i = 0; i < steps; i++) {
    colors.push(mixColors(start, end, i / (steps - 1)));
  }
  
  return colors;
}

/**
 * 生成单色配色方案（同一色相的不同明度/饱和度）
 * @param {string|RGB} color - 基础颜色
 * @param {number} [count=5] - 生成颜色数量
 * @returns {RGB[]|null}
 */
function monochromaticPalette(color, count = 5) {
  const rgb = typeof color === 'string' ? parseColor(color) : color;
  if (!rgb) return null;
  
  const hsl = rgbToHsl(rgb);
  const colors = [];
  
  for (let i = 0; i < count; i++) {
    const l = 10 + (80 * i / (count - 1));
    colors.push(hslToRgb({ h: hsl.h, s: hsl.s, l }));
  }
  
  return colors;
}

/**
 * 生成类似色配色方案
 * @param {string|RGB} color - 基础颜色
 * @param {number} [angle=30] - 色相偏移角度
 * @returns {RGB[]|null}
 */
function analogousPalette(color, angle = 30) {
  const rgb = typeof color === 'string' ? parseColor(color) : color;
  if (!rgb) return null;
  
  const hsl = rgbToHsl(rgb);
  
  return [
    hslToRgb({ h: (hsl.h - angle + 360) % 360, s: hsl.s, l: hsl.l }),
    rgb,
    hslToRgb({ h: (hsl.h + angle) % 360, s: hsl.s, l: hsl.l })
  ];
}

/**
 * 生成三色配色方案（色相环等距三色）
 * @param {string|RGB} color - 基础颜色
 * @returns {RGB[]|null}
 */
function triadicPalette(color) {
  const rgb = typeof color === 'string' ? parseColor(color) : color;
  if (!rgb) return null;
  
  const hsl = rgbToHsl(rgb);
  
  return [
    rgb,
    hslToRgb({ h: (hsl.h + 120) % 360, s: hsl.s, l: hsl.l }),
    hslToRgb({ h: (hsl.h + 240) % 360, s: hsl.s, l: hsl.l })
  ];
}

/**
 * 生成四色配色方案（色相环等距四色）
 * @param {string|RGB} color - 基础颜色
 * @returns {RGB[]|null}
 */
function tetradicPalette(color) {
  const rgb = typeof color === 'string' ? parseColor(color) : color;
  if (!rgb) return null;
  
  const hsl = rgbToHsl(rgb);
  
  return [
    rgb,
    hslToRgb({ h: (hsl.h + 90) % 360, s: hsl.s, l: hsl.l }),
    hslToRgb({ h: (hsl.h + 180) % 360, s: hsl.s, l: hsl.l }),
    hslToRgb({ h: (hsl.h + 270) % 360, s: hsl.s, l: hsl.l })
  ];
}

/**
 * 生成互补配色方案
 * @param {string|RGB} color - 基础颜色
 * @returns {RGB[]|null}
 */
function complementaryPalette(color) {
  const rgb = typeof color === 'string' ? parseColor(color) : color;
  if (!rgb) return null;
  
  return [rgb, complementColor(rgb)];
}

/**
 * 生成分裂互补配色方案
 * @param {string|RGB} color - 基础颜色
 * @param {number} [angle=150] - 分裂角度
 * @returns {RGB[]|null}
 */
function splitComplementaryPalette(color, angle = 150) {
  const rgb = typeof color === 'string' ? parseColor(color) : color;
  if (!rgb) return null;
  
  const hsl = rgbToHsl(rgb);
  
  return [
    rgb,
    hslToRgb({ h: (hsl.h + angle) % 360, s: hsl.s, l: hsl.l }),
    hslToRgb({ h: (hsl.h + 360 - angle) % 360, s: hsl.s, l: hsl.l })
  ];
}

// ==================== 颜色距离与比较 ====================

/**
 * 计算两个颜色之间的欧氏距离
 * @param {string|RGB} color1 - 颜色 1
 * @param {string|RGB} color2 - 颜色 2
 * @returns {number|null} 距离 (0-441.67)
 */
function colorDistance(color1, color2) {
  const rgb1 = typeof color1 === 'string' ? parseColor(color1) : color1;
  const rgb2 = typeof color2 === 'string' ? parseColor(color2) : color2;
  
  if (!rgb1 || !rgb2) return null;
  
  return Math.sqrt(
    Math.pow(rgb1.r - rgb2.r, 2) +
    Math.pow(rgb1.g - rgb2.g, 2) +
    Math.pow(rgb1.b - rgb2.b, 2)
  );
}

/**
 * 计算 CIE Delta E 2000 色差
 * @param {string|RGB|LAB} color1 - 颜色 1
 * @param {string|RGB|LAB} color2 - 颜色 2
 * @returns {number|null} Delta E 值
 */
function deltaE2000(color1, color2) {
  const toLab = (c) => {
    if (typeof c === 'string') return rgbToLab(parseColor(c));
    if ('r' in c) return rgbToLab(c);
    return c;
  };
  
  const lab1 = toLab(color1);
  const lab2 = toLab(color2);
  
  if (!lab1 || !lab2) return null;
  
  const L1 = lab1.l, a1 = lab1.a, b1 = lab1.b;
  const L2 = lab2.l, a2 = lab2.a, b2 = lab2.b;
  
  const kL = 1, kC = 1, kH = 1;
  
  const C1 = Math.sqrt(a1 * a1 + b1 * b1);
  const C2 = Math.sqrt(a2 * a2 + b2 * b2);
  const Cavg = (C1 + C2) / 2;
  
  const G = 0.5 * (1 - Math.sqrt(Math.pow(Cavg, 7) / (Math.pow(Cavg, 7) + Math.pow(25, 7))));
  
  const a1p = a1 * (1 + G);
  const a2p = a2 * (1 + G);
  
  const C1p = Math.sqrt(a1p * a1p + b1 * b1);
  const C2p = Math.sqrt(a2p * a2p + b2 * b2);
  
  const h1p = Math.atan2(b1, a1p) * 180 / Math.PI;
  const h2p = Math.atan2(b2, a2p) * 180 / Math.PI;
  
  const deltaLp = L2 - L1;
  const deltaCp = C2p - C1p;
  
  let deltaHp;
  if (C1p * C2p === 0) {
    deltaHp = 0;
  } else if (Math.abs(h2p - h1p) <= 180) {
    deltaHp = h2p - h1p;
  } else if (h2p - h1p > 180) {
    deltaHp = h2p - h1p - 360;
  } else {
    deltaHp = h2p - h1p + 360;
  }
  
  const deltaHp2 = 2 * Math.sqrt(C1p * C2p) * Math.sin(deltaHp * Math.PI / 360);
  
  const Lp = (L1 + L2) / 2;
  const Cp = (C1p + C2p) / 2;
  
  let Hp;
  if (C1p * C2p === 0) {
    Hp = h1p + h2p;
  } else if (Math.abs(h1p - h2p) <= 180) {
    Hp = (h1p + h2p) / 2;
  } else if (h1p + h2p < 360) {
    Hp = (h1p + h2p + 360) / 2;
  } else {
    Hp = (h1p + h2p - 360) / 2;
  }
  
  const T = 1 - 0.17 * Math.cos((Hp - 30) * Math.PI / 180) +
            0.24 * Math.cos(2 * Hp * Math.PI / 180) +
            0.32 * Math.cos((3 * Hp + 6) * Math.PI / 180) -
            0.20 * Math.cos((4 * Hp - 63) * Math.PI / 180);
  
  const SL = 1 + (0.015 * Math.pow(Lp - 50, 2)) / Math.sqrt(20 + Math.pow(Lp - 50, 2));
  const SC = 1 + 0.045 * Cp;
  const SH = 1 + 0.015 * Cp * T;
  
  const RT = -2 * Math.sqrt(Math.pow(Cp, 7) / (Math.pow(Cp, 7) + Math.pow(25, 7))) *
             Math.sin(60 * Math.exp(-Math.pow((Hp - 275) / 25, 2)) * Math.PI / 180);
  
  const dE = Math.sqrt(
    Math.pow(deltaLp / (kL * SL), 2) +
    Math.pow(deltaCp / (kC * SC), 2) +
    Math.pow(deltaHp2 / (kH * SH), 2) +
    RT * (deltaCp / (kC * SC)) * (deltaHp2 / (kH * SH))
  );
  
  return Math.round(dE * 100) / 100;
}

/**
 * 找出颜色数组中与目标颜色最接近的颜色
 * @param {string|RGB} target - 目标颜色
 * @param {(string|RGB)[]} colors - 颜色数组
 * @returns {Object|null} { color: RGB, index: number, distance: number }
 */
function findClosestColor(target, colors) {
  const targetRgb = typeof target === 'string' ? parseColor(target) : target;
  if (!targetRgb || !colors || !colors.length) return null;
  
  let closest = null;
  let minDistance = Infinity;
  let closestIndex = -1;
  
  for (let i = 0; i < colors.length; i++) {
    const rgb = typeof colors[i] === 'string' ? parseColor(colors[i]) : colors[i];
    if (!rgb) continue;
    
    const dist = colorDistance(targetRgb, rgb);
    if (dist < minDistance) {
      minDistance = dist;
      closest = rgb;
      closestIndex = i;
    }
  }
  
  return closest ? { color: closest, index: closestIndex, distance: minDistance } : null;
}

// ==================== 工具函数 ====================

/**
 * 判断颜色是否为深色
 * @param {string|RGB} color - 颜色
 * @returns {boolean|null}
 */
function isDark(color) {
  const rgb = typeof color === 'string' ? parseColor(color) : color;
  if (!rgb) return null;
  
  return getLuminance(rgb) < 0.5;
}

/**
 * 判断颜色是否为浅色
 * @param {string|RGB} color - 颜色
 * @returns {boolean|null}
 */
function isLight(color) {
  const rgb = typeof color === 'string' ? parseColor(color) : color;
  if (!rgb) return null;
  
  return getLuminance(rgb) >= 0.5;
}

/**
 * 将颜色转换为 CSS 字符串
 * @param {RGB} rgb - RGB 颜色对象
 * @param {string} [format='hex'] - 格式 ('hex', 'rgb', 'rgba', 'hsl', 'hsla')
 * @returns {string|null}
 */
function toCssString(rgb, format = 'hex') {
  if (!rgb) return null;
  
  switch (format.toLowerCase()) {
    case 'hex':
      return rgbToHex(rgb);
    case 'hexa':
      return rgbToHex(rgb, true);
    case 'rgb':
      return `rgb(${rgb.r}, ${rgb.g}, ${rgb.b})`;
    case 'rgba':
      return `rgba(${rgb.r}, ${rgb.g}, ${rgb.b}, ${rgb.a !== undefined ? rgb.a : 1})`;
    case 'hsl': {
      const hsl = rgbToHsl(rgb);
      return `hsl(${hsl.h}, ${hsl.s}%, ${hsl.l}%)`;
    }
    case 'hsla': {
      const hsl = rgbToHsl(rgb);
      return `hsla(${hsl.h}, ${hsl.s}%, ${hsl.l}%, ${hsl.a !== undefined ? hsl.a : 1})`;
    }
    default:
      return null;
  }
}

/**
 * 获取颜色名称
 * @param {string|RGB} color - 颜色
 * @returns {string|null} 最接近的颜色名称
 */
function getColorName(color) {
  const rgb = typeof color === 'string' ? parseColor(color) : color;
  if (!rgb) return null;
  
  let closestName = null;
  let minDistance = Infinity;
  
  for (const [name, hex] of Object.entries(NAMED_COLORS)) {
    const namedRgb = parseHex(hex);
    if (!namedRgb) continue;
    
    const dist = colorDistance(rgb, namedRgb);
    if (dist < minDistance) {
      minDistance = dist;
      closestName = name;
    }
  }
  
  return closestName;
}

/**
 * 验证颜色字符串
 * @param {string} color - 颜色字符串
 * @returns {boolean}
 */
function isValidColor(color) {
  return parseColor(color) !== null;
}

/**
 * 克隆颜色对象
 * @param {RGB} rgb - RGB 颜色对象
 * @returns {RGB}
 */
function cloneColor(rgb) {
  if (!rgb) return null;
  return { ...rgb };
}

/**
 * 比较两个颜色是否相等
 * @param {string|RGB} color1 - 颜色 1
 * @param {string|RGB} color2 - 颜色 2
 * @returns {boolean}
 */
function colorsEqual(color1, color2) {
  const rgb1 = typeof color1 === 'string' ? parseColor(color1) : color1;
  const rgb2 = typeof color2 === 'string' ? parseColor(color2) : color2;
  
  if (!rgb1 || !rgb2) return false;
  
  return rgb1.r === rgb2.r && rgb1.g === rgb2.g && rgb1.b === rgb2.b;
}

// ==================== 导出 ====================

module.exports = {
  // 解析
  parseColor,
  parseHex,
  parseRgb,
  parseHsl,
  
  // 格式转换
  rgbToHex,
  rgbToHsl,
  hslToRgb,
  rgbToHsv,
  hsvToRgb,
  rgbToCmyk,
  cmykToRgb,
  rgbToLab,
  labToRgb,
  
  // 颜色操作
  mixColors,
  adjustBrightness,
  adjustSaturation,
  adjustHue,
  adjustAlpha,
  invertColor,
  grayscaleColor,
  complementColor,
  
  // 对比度与可访问性
  getLuminance,
  getContrastRatio,
  checkContrastWCAG,
  getReadableTextColor,
  
  // 颜色生成
  randomColor,
  randomHex,
  randomHsl,
  randomVibrantColor,
  randomPastelColor,
  
  // 调色板生成
  gradientColors,
  monochromaticPalette,
  analogousPalette,
  triadicPalette,
  tetradicPalette,
  complementaryPalette,
  splitComplementaryPalette,
  
  // 颜色距离与比较
  colorDistance,
  deltaE2000,
  findClosestColor,
  
  // 工具函数
  isDark,
  isLight,
  toCssString,
  getColorName,
  isValidColor,
  cloneColor,
  colorsEqual,
  
  // 常量
  NAMED_COLORS
};