/**
 * Color Parser Utilities for TypeScript
 * 
 * A comprehensive color parsing, conversion, and manipulation library.
 * Supports multiple color formats: HEX, RGB, HSL, HSV, CMYK, LAB, XYZ.
 * 
 * Features:
 * - Parse colors from various formats (hex, rgb, hsl, css named colors)
 * - Convert between color spaces
 * - Calculate color contrast and accessibility
 * - Generate color palettes and gradients
 * - Zero external dependencies
 * 
 * @module color_parser_utils
 */

// ============================================================================
// Type Definitions
// ============================================================================

export interface RGB {
  r: number; // 0-255
  g: number; // 0-255
  b: number; // 0-255
  a?: number; // 0-1 (optional alpha)
}

export interface HSL {
  h: number; // 0-360
  s: number; // 0-100
  l: number; // 0-100
  a?: number; // 0-1 (optional alpha)
}

export interface HSV {
  h: number; // 0-360
  s: number; // 0-100
  v: number; // 0-100
  a?: number; // 0-1 (optional alpha)
}

export interface CMYK {
  c: number; // 0-100
  m: number; // 0-100
  y: number; // 0-100
  k: number; // 0-100
}

export interface XYZ {
  x: number; // 0-95.047
  y: number; // 0-100
  z: number; // 0-108.883
}

export interface LAB {
  l: number; // 0-100
  a: number; // -128 to 127
  b: number; // -128 to 127
}

export type ColorFormat = 'hex' | 'rgb' | 'hsl' | 'hsv' | 'cmyk' | 'lab' | 'xyz';

export interface ParseResult {
  format: ColorFormat;
  rgb: RGB;
  hsl: HSL;
  hsv: HSV;
  hex: string;
  alpha: number;
}

// ============================================================================
// CSS Named Colors
// ============================================================================

export const CSS_NAMED_COLORS: Record<string, string> = {
  // Basic colors
  'black': '#000000',
  'white': '#FFFFFF',
  'red': '#FF0000',
  'green': '#008000',
  'blue': '#0000FF',
  'yellow': '#FFFF00',
  'cyan': '#00FFFF',
  'magenta': '#FF00FF',
  
  // Extended colors
  'aliceblue': '#F0F8FF',
  'antiquewhite': '#FAEBD7',
  'aqua': '#00FFFF',
  'aquamarine': '#7FFFD4',
  'azure': '#F0FFFF',
  'beige': '#F5F5DC',
  'bisque': '#FFE4C4',
  'blanchedalmond': '#FFEBCD',
  'blueviolet': '#8A2BE2',
  'brown': '#A52A2A',
  'burlywood': '#DEB887',
  'cadetblue': '#5F9EA0',
  'chartreuse': '#7FFF00',
  'chocolate': '#D2691E',
  'coral': '#FF7F50',
  'cornflowerblue': '#6495ED',
  'cornsilk': '#FFF8DC',
  'crimson': '#DC143C',
  'darkblue': '#00008B',
  'darkcyan': '#008B8B',
  'darkgoldenrod': '#B8860B',
  'darkgray': '#A9A9A9',
  'darkgreen': '#006400',
  'darkgrey': '#A9A9A9',
  'darkkhaki': '#BDB76B',
  'darkmagenta': '#8B008B',
  'darkolivegreen': '#556B2F',
  'darkorange': '#FF8C00',
  'darkorchid': '#9932CC',
  'darkred': '#8B0000',
  'darksalmon': '#E9967A',
  'darkseagreen': '#8FBC8F',
  'darkslateblue': '#483D8B',
  'darkslategray': '#2F4F4F',
  'darkslategrey': '#2F4F4F',
  'darkturquoise': '#00CED1',
  'darkviolet': '#9400D3',
  'deeppink': '#FF1493',
  'deepskyblue': '#00BFFF',
  'dimgray': '#696969',
  'dimgrey': '#696969',
  'dodgerblue': '#1E90FF',
  'firebrick': '#B22222',
  'floralwhite': '#FFFAF0',
  'forestgreen': '#228B22',
  'fuchsia': '#FF00FF',
  'gainsboro': '#DCDCDC',
  'ghostwhite': '#F8F8FF',
  'gold': '#FFD700',
  'goldenrod': '#DAA520',
  'gray': '#808080',
  'greenyellow': '#ADFF2F',
  'grey': '#808080',
  'honeydew': '#F0FFF0',
  'hotpink': '#FF69B4',
  'indianred': '#CD5C5C',
  'indigo': '#4B0082',
  'ivory': '#FFFFF0',
  'khaki': '#F0E68C',
  'lavender': '#E6E6FA',
  'lavenderblush': '#FFF0F5',
  'lawngreen': '#7CFC00',
  'lemonchiffon': '#FFFACD',
  'lightblue': '#ADD8E6',
  'lightcoral': '#F08080',
  'lightcyan': '#E0FFFF',
  'lightgoldenrodyellow': '#FAFAD2',
  'lightgray': '#D3D3D3',
  'lightgreen': '#90EE90',
  'lightgrey': '#D3D3D3',
  'lightpink': '#FFB6C1',
  'lightsalmon': '#FFA07A',
  'lightseagreen': '#20B2AA',
  'lightskyblue': '#87CEFA',
  'lightslategray': '#778899',
  'lightslategrey': '#778899',
  'lightsteelblue': '#B0C4DE',
  'lightyellow': '#FFFFE0',
  'lime': '#00FF00',
  'limegreen': '#32CD32',
  'linen': '#FAF0E6',
  'maroon': '#800000',
  'mediumaquamarine': '#66CDAA',
  'mediumblue': '#0000CD',
  'mediumorchid': '#BA55D3',
  'mediumpurple': '#9370DB',
  'mediumseagreen': '#3CB371',
  'mediumslateblue': '#7B68EE',
  'mediumspringgreen': '#00FA9A',
  'mediumturquoise': '#48D1CC',
  'mediumvioletred': '#C71585',
  'midnightblue': '#191970',
  'mintcream': '#F5FFFA',
  'mistyrose': '#FFE4E1',
  'moccasin': '#FFE4B5',
  'navajowhite': '#FFDEAD',
  'navy': '#000080',
  'oldlace': '#FDF5E6',
  'olive': '#808000',
  'olivedrab': '#6B8E23',
  'orange': '#FFA500',
  'orangered': '#FF4500',
  'orchid': '#DA70D6',
  'palegoldenrod': '#EEE8AA',
  'palegreen': '#98FB98',
  'paleturquoise': '#AFEEEE',
  'palevioletred': '#DB7093',
  'papayawhip': '#FFEFD5',
  'peachpuff': '#FFDAB9',
  'peru': '#CD853F',
  'pink': '#FFC0CB',
  'plum': '#DDA0DD',
  'powderblue': '#B0E0E6',
  'purple': '#800080',
  'rebeccapurple': '#663399',
  'rosybrown': '#BC8F8F',
  'royalblue': '#4169E1',
  'saddlebrown': '#8B4513',
  'salmon': '#FA8072',
  'sandybrown': '#F4A460',
  'seagreen': '#2E8B57',
  'seashell': '#FFF5EE',
  'sienna': '#A0522D',
  'silver': '#C0C0C0',
  'skyblue': '#87CEEB',
  'slateblue': '#6A5ACD',
  'slategray': '#708090',
  'slategrey': '#708090',
  'snow': '#FFFAFA',
  'springgreen': '#00FF7F',
  'steelblue': '#4682B4',
  'tan': '#D2B48C',
  'teal': '#008080',
  'thistle': '#D8BFD8',
  'tomato': '#FF6347',
  'turquoise': '#40E0D0',
  'violet': '#EE82EE',
  'wheat': '#F5DEB3',
  'whitesmoke': '#F5F5F5',
  'yellowgreen': '#9ACD32',
};

// ============================================================================
// Parsing Functions
// ============================================================================

/**
 * Parse a hex color string to RGB
 */
export function parseHex(hex: string): RGB | null {
  // Remove # prefix and whitespace
  hex = hex.trim().replace(/^#/, '').toUpperCase();
  
  // Handle shorthand hex (#RGB or #RGBA)
  if (hex.length === 3 || hex.length === 4) {
    hex = hex.split('').map(c => c + c).join('');
  }
  
  // Validate hex format
  if (!/^[0-9A-F]{6}$/.test(hex) && !/^[0-9A-F]{8}$/.test(hex)) {
    return null;
  }
  
  const r = parseInt(hex.substring(0, 2), 16);
  const g = parseInt(hex.substring(2, 4), 16);
  const b = parseInt(hex.substring(4, 6), 16);
  
  let a: number | undefined = undefined;
  if (hex.length === 8) {
    a = Math.round((parseInt(hex.substring(6, 8), 16) / 255) * 1000) / 1000;
  }
  
  return { r, g, b, a: a ?? 1 };
}

/**
 * Parse an RGB/RGBA string to RGB object
 */
export function parseRgbString(rgb: string): RGB | null {
  const match = rgb.match(/rgba?\s*\(\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})\s*(?:,\s*([\d.]+)\s*)?\)/i);
  if (!match) return null;
  
  const r = Math.min(255, Math.max(0, parseInt(match[1])));
  const g = Math.min(255, Math.max(0, parseInt(match[2])));
  const b = Math.min(255, Math.max(0, parseInt(match[3])));
  const a = match[4] !== undefined ? Math.min(1, Math.max(0, parseFloat(match[4]))) : 1;
  
  return { r, g, b, a };
}

/**
 * Parse an HSL/HSLA string to HSL object
 */
export function parseHslString(hsl: string): HSL | null {
  const match = hsl.match(/hsla?\s*\(\s*(\d{1,3})\s*,\s*(\d{1,3})%\s*,\s*(\d{1,3})%\s*(?:,\s*([\d.]+)\s*)?\)/i);
  if (!match) return null;
  
  const h = Math.min(360, Math.max(0, parseInt(match[1]))) % 360;
  const s = Math.min(100, Math.max(0, parseInt(match[2])));
  const l = Math.min(100, Math.max(0, parseInt(match[3])));
  const a = match[4] !== undefined ? Math.min(1, Math.max(0, parseFloat(match[4]))) : 1;
  
  return { h, s, l, a };
}

/**
 * Parse any color string (hex, rgb, hsl, named color)
 */
export function parseColor(color: string): ParseResult | null {
  color = color.trim();
  const lowerColor = color.toLowerCase();
  
  // Check for named colors (handle spaces: convert to lowercase and replace spaces)
  const normalizedName = lowerColor.replace(/\s+/g, '').toLowerCase();
  if (CSS_NAMED_COLORS[normalizedName]) {
    color = CSS_NAMED_COLORS[normalizedName];
  }
  
  let rgb: RGB | null = null;
  let format: ColorFormat = 'hex';
  
  // Try parsing different formats
  if (color.startsWith('#') || /^[0-9A-Fa-f]{3,8}$/.test(color)) {
    rgb = parseHex(color);
    format = 'hex';
  } else if (lowerColor.startsWith('rgb')) {
    rgb = parseRgbString(color);
    format = 'rgb';
  } else if (lowerColor.startsWith('hsl')) {
    const hsl = parseHslString(color);
    if (hsl) {
      rgb = hslToRgb(hsl);
      format = 'hsl';
    }
  }
  
  if (!rgb) return null;
  
  const hsl = rgbToHsl(rgb);
  const hsv = rgbToHsv(rgb);
  
  return {
    format,
    rgb,
    hsl,
    hsv,
    hex: rgbToHex(rgb),
    alpha: rgb.a ?? 1,
  };
}

// ============================================================================
// Conversion Functions
// ============================================================================

/**
 * Convert RGB to HEX string
 */
export function rgbToHex(rgb: RGB, includeAlpha = false): string {
  const toHex = (n: number) => Math.round(n).toString(16).padStart(2, '0');
  let hex = `#${toHex(rgb.r)}${toHex(rgb.g)}${toHex(rgb.b)}`;
  
  if (includeAlpha && rgb.a !== undefined && rgb.a !== 1) {
    hex += toHex(Math.round(rgb.a * 255));
  }
  
  return hex.toUpperCase();
}

/**
 * Convert HEX to RGB
 */
export function hexToRgb(hex: string): RGB | null {
  return parseHex(hex);
}

/**
 * Convert RGB to HSL
 */
export function rgbToHsl(rgb: RGB): HSL {
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
      case r:
        h = ((g - b) / d + (g < b ? 6 : 0)) / 6;
        break;
      case g:
        h = ((b - r) / d + 2) / 6;
        break;
      case b:
        h = ((r - g) / d + 4) / 6;
        break;
    }
  }
  
  return {
    h: Math.round(h * 360),
    s: Math.round(s * 100),
    l: Math.round(l * 100),
    a: rgb.a,
  };
}

/**
 * Convert HSL to RGB
 */
export function hslToRgb(hsl: HSL): RGB {
  const h = hsl.h / 360;
  const s = hsl.s / 100;
  const l = hsl.l / 100;
  
  let r, g, b;
  
  if (s === 0) {
    r = g = b = l;
  } else {
    const hue2rgb = (p: number, q: number, t: number) => {
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
    a: hsl.a,
  };
}

/**
 * Convert RGB to HSV
 */
export function rgbToHsv(rgb: RGB): HSV {
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
      case r:
        h = ((g - b) / d + (g < b ? 6 : 0)) / 6;
        break;
      case g:
        h = ((b - r) / d + 2) / 6;
        break;
      case b:
        h = ((r - g) / d + 4) / 6;
        break;
    }
  }
  
  return {
    h: Math.round(h * 360),
    s: Math.round(s * 100),
    v: Math.round(v * 100),
    a: rgb.a,
  };
}

/**
 * Convert HSV to RGB
 */
export function hsvToRgb(hsv: HSV): RGB {
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
    default: r = g = b = v;
  }
  
  return {
    r: Math.round(r * 255),
    g: Math.round(g * 255),
    b: Math.round(b * 255),
    a: hsv.a,
  };
}

/**
 * Convert RGB to CMYK
 */
export function rgbToCmyk(rgb: RGB): CMYK {
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
    k: Math.round(k * 100),
  };
}

/**
 * Convert CMYK to RGB
 */
export function cmykToRgb(cmyk: CMYK): RGB {
  const c = cmyk.c / 100;
  const m = cmyk.m / 100;
  const y = cmyk.y / 100;
  const k = cmyk.k / 100;
  
  return {
    r: Math.round(255 * (1 - c) * (1 - k)),
    g: Math.round(255 * (1 - m) * (1 - k)),
    b: Math.round(255 * (1 - y) * (1 - k)),
  };
}

/**
 * Convert RGB to XYZ
 */
export function rgbToXyz(rgb: RGB): XYZ {
  let r = rgb.r / 255;
  let g = rgb.g / 255;
  let b = rgb.b / 255;
  
  // Apply gamma correction
  r = r > 0.04045 ? Math.pow((r + 0.055) / 1.055, 2.4) : r / 12.92;
  g = g > 0.04045 ? Math.pow((g + 0.055) / 1.055, 2.4) : g / 12.92;
  b = b > 0.04045 ? Math.pow((b + 0.055) / 1.055, 2.4) : b / 12.92;
  
  return {
    x: (r * 0.4124564 + g * 0.3575761 + b * 0.1804375) * 100,
    y: (r * 0.2126729 + g * 0.7151522 + b * 0.0721750) * 100,
    z: (r * 0.0193339 + g * 0.1191920 + b * 0.9503041) * 100,
  };
}

/**
 * Convert XYZ to RGB
 */
export function xyzToRgb(xyz: XYZ): RGB {
  const x = xyz.x / 100;
  const y = xyz.y / 100;
  const z = xyz.z / 100;
  
  let r = x * 3.2404542 + y * -1.5371385 + z * -0.4985314;
  let g = x * -0.9692660 + y * 1.8760108 + z * 0.0415560;
  let b = x * 0.0556434 + y * -0.2040259 + z * 1.0572252;
  
  // Apply inverse gamma correction
  r = r > 0.0031308 ? 1.055 * Math.pow(r, 1/2.4) - 0.055 : 12.92 * r;
  g = g > 0.0031308 ? 1.055 * Math.pow(g, 1/2.4) - 0.055 : 12.92 * g;
  b = b > 0.0031308 ? 1.055 * Math.pow(b, 1/2.4) - 0.055 : 12.92 * b;
  
  return {
    r: Math.min(255, Math.max(0, Math.round(r * 255))),
    g: Math.min(255, Math.max(0, Math.round(g * 255))),
    b: Math.min(255, Math.max(0, Math.round(b * 255))),
  };
}

/**
 * Convert XYZ to LAB
 */
export function xyzToLab(xyz: XYZ): LAB {
  // Reference white D65
  const refX = 95.047;
  const refY = 100.000;
  const refZ = 108.883;
  
  const f = (t: number) => t > 0.008856 ? Math.pow(t, 1/3) : (903.3 * t + 16) / 116;
  
  const x = f(xyz.x / refX);
  const y = f(xyz.y / refY);
  const z = f(xyz.z / refZ);
  
  return {
    l: Math.round((116 * y - 16) * 100) / 100,
    a: Math.round((500 * (x - y)) * 100) / 100,
    b: Math.round((200 * (y - z)) * 100) / 100,
  };
}

/**
 * Convert LAB to XYZ
 */
export function labToXyz(lab: LAB): XYZ {
  const refX = 95.047;
  const refY = 100.000;
  const refZ = 108.883;
  
  const fy = (lab.l + 16) / 116;
  const fx = lab.a / 500 + fy;
  const fz = fy - lab.b / 200;
  
  const f = (t: number) => {
    const t3 = t * t * t;
    return t3 > 0.008856 ? t3 : (116 * t - 16) / 903.3;
  };
  
  return {
    x: f(fx) * refX,
    y: f(fy) * refY,
    z: f(fz) * refZ,
  };
}

/**
 * Convert RGB to LAB
 */
export function rgbToLab(rgb: RGB): LAB {
  return xyzToLab(rgbToXyz(rgb));
}

/**
 * Convert LAB to RGB
 */
export function labToRgb(lab: LAB): RGB {
  return xyzToRgb(labToXyz(lab));
}

// ============================================================================
// Color Manipulation Functions
// ============================================================================

/**
 * Lighten a color
 */
export function lighten(color: string, amount: number): string {
  const parsed = parseColor(color);
  if (!parsed) return color;
  
  const hsl = { ...parsed.hsl };
  hsl.l = Math.min(100, hsl.l + amount);
  
  return rgbToHex(hslToRgb(hsl));
}

/**
 * Darken a color
 */
export function darken(color: string, amount: number): string {
  const parsed = parseColor(color);
  if (!parsed) return color;
  
  const hsl = { ...parsed.hsl };
  hsl.l = Math.max(0, hsl.l - amount);
  
  return rgbToHex(hslToRgb(hsl));
}

/**
 * Saturate a color
 */
export function saturate(color: string, amount: number): string {
  const parsed = parseColor(color);
  if (!parsed) return color;
  
  const hsl = { ...parsed.hsl };
  hsl.s = Math.min(100, hsl.s + amount);
  
  return rgbToHex(hslToRgb(hsl));
}

/**
 * Desaturate a color
 */
export function desaturate(color: string, amount: number): string {
  const parsed = parseColor(color);
  if (!parsed) return color;
  
  const hsl = { ...parsed.hsl };
  hsl.s = Math.max(0, hsl.s - amount);
  
  return rgbToHex(hslToRgb(hsl));
}

/**
 * Adjust hue of a color
 */
export function adjustHue(color: string, degrees: number): string {
  const parsed = parseColor(color);
  if (!parsed) return color;
  
  const hsl = { ...parsed.hsl };
  hsl.h = (hsl.h + degrees) % 360;
  if (hsl.h < 0) hsl.h += 360;
  
  return rgbToHex(hslToRgb(hsl));
}

/**
 * Set alpha channel
 */
export function setAlpha(color: string, alpha: number): string {
  const parsed = parseColor(color);
  if (!parsed) return color;
  
  const rgb = { ...parsed.rgb, a: Math.min(1, Math.max(0, alpha)) };
  return rgbToHex(rgb, true);
}

/**
 * Mix two colors
 */
export function mix(color1: string, color2: string, weight = 0.5): string {
  const parsed1 = parseColor(color1);
  const parsed2 = parseColor(color2);
  
  if (!parsed1 || !parsed2) return color1;
  
  const w = Math.min(1, Math.max(0, weight));
  
  const rgb: RGB = {
    r: Math.round(parsed1.rgb.r * (1 - w) + parsed2.rgb.r * w),
    g: Math.round(parsed1.rgb.g * (1 - w) + parsed2.rgb.g * w),
    b: Math.round(parsed1.rgb.b * (1 - w) + parsed2.rgb.b * w),
    a: parsed1.rgb.a !== undefined || parsed2.rgb.a !== undefined
      ? (parsed1.rgb.a ?? 1) * (1 - w) + (parsed2.rgb.a ?? 1) * w
      : undefined,
  };
  
  return rgbToHex(rgb);
}

/**
 * Invert a color
 */
export function invert(color: string): string {
  const parsed = parseColor(color);
  if (!parsed) return color;
  
  const rgb: RGB = {
    r: 255 - parsed.rgb.r,
    g: 255 - parsed.rgb.g,
    b: 255 - parsed.rgb.b,
    a: parsed.rgb.a,
  };
  
  return rgbToHex(rgb);
}

/**
 * Get grayscale version of a color
 */
export function grayscale(color: string): string {
  const parsed = parseColor(color);
  if (!parsed) return color;
  
  const gray = Math.round(0.299 * parsed.rgb.r + 0.587 * parsed.rgb.g + 0.114 * parsed.rgb.b);
  
  return rgbToHex({ r: gray, g: gray, b: gray, a: parsed.rgb.a });
}

/**
 * Get sepia version of a color
 */
export function sepia(color: string): string {
  const parsed = parseColor(color);
  if (!parsed) return color;
  
  const { r, g, b } = parsed.rgb;
  
  const sepiaR = Math.min(255, (r * 0.393) + (g * 0.769) + (b * 0.189));
  const sepiaG = Math.min(255, (r * 0.349) + (g * 0.686) + (b * 0.168));
  const sepiaB = Math.min(255, (r * 0.272) + (g * 0.534) + (b * 0.131));
  
  return rgbToHex({ r: sepiaR, g: sepiaG, b: sepiaB, a: parsed.rgb.a });
}

// ============================================================================
// Color Analysis Functions
// ============================================================================

/**
 * Calculate relative luminance (WCAG)
 */
export function getLuminance(color: string): number {
  const parsed = parseColor(color);
  if (!parsed) return 0;
  
  const { r, g, b } = parsed.rgb;
  
  const R = r / 255 <= 0.03928 ? r / 255 / 12.92 : Math.pow(r / 255 / 1.055 + 0.055, 2.4);
  const G = g / 255 <= 0.03928 ? g / 255 / 12.92 : Math.pow(g / 255 / 1.055 + 0.055, 2.4);
  const B = b / 255 <= 0.03928 ? b / 255 / 12.92 : Math.pow(b / 255 / 1.055 + 0.055, 2.4);
  
  return 0.2126 * R + 0.7152 * G + 0.0722 * B;
}

/**
 * Calculate contrast ratio between two colors (WCAG)
 */
export function getContrastRatio(color1: string, color2: string): number {
  const L1 = getLuminance(color1);
  const L2 = getLuminance(color2);
  
  const lighter = Math.max(L1, L2);
  const darker = Math.min(L1, L2);
  
  return (lighter + 0.05) / (darker + 0.05);
}

/**
 * Check if contrast meets WCAG requirements
 */
export function meetsWCAG(color1: string, color2: string, level: 'AA' | 'AAA' = 'AA', largeText = false): boolean {
  const ratio = getContrastRatio(color1, color2);
  
  if (level === 'AAA') {
    return largeText ? ratio >= 4.5 : ratio >= 7;
  }
  
  return largeText ? ratio >= 3 : ratio >= 4.5;
}

/**
 * Get WCAG rating for color pair
 */
export function getWCAGRating(color1: string, color2: string): 'Fail' | 'AA Large' | 'AA' | 'AAA Large' | 'AAA' {
  const ratio = getContrastRatio(color1, color2);
  
  if (ratio >= 7) return 'AAA';
  if (ratio >= 4.5) return 'AA';
  if (ratio >= 3) return 'AA Large';
  if (ratio >= 4.5) return 'AAA Large';
  return 'Fail';
}

/**
 * Determine if a color is light or dark
 */
export function isLight(color: string): boolean {
  return getLuminance(color) > 0.5;
}

/**
 * Get complementary color
 */
export function complement(color: string): string {
  return adjustHue(color, 180);
}

/**
 * Get analogous colors
 */
export function analogous(color: string, angle = 30): string[] {
  return [
    adjustHue(color, -angle),
    color,
    adjustHue(color, angle),
  ];
}

/**
 * Get triadic colors
 */
export function triadic(color: string): string[] {
  return [
    color,
    adjustHue(color, 120),
    adjustHue(color, 240),
  ];
}

/**
 * Get tetradic/square colors
 */
export function tetradic(color: string): string[] {
  return [
    color,
    adjustHue(color, 90),
    adjustHue(color, 180),
    adjustHue(color, 270),
  ];
}

/**
 * Split complementary colors
 */
export function splitComplementary(color: string, angle = 150): string[] {
  return [
    color,
    adjustHue(color, angle),
    adjustHue(color, 360 - angle),
  ];
}

// ============================================================================
// Color Distance Functions
// ============================================================================

/**
 * Calculate Euclidean distance between two colors in RGB space
 */
export function rgbDistance(color1: string, color2: string): number {
  const c1 = parseColor(color1);
  const c2 = parseColor(color2);
  
  if (!c1 || !c2) return Infinity;
  
  const dr = c1.rgb.r - c2.rgb.r;
  const dg = c1.rgb.g - c2.rgb.g;
  const db = c1.rgb.b - c2.rgb.b;
  
  return Math.sqrt(dr * dr + dg * dg + db * db);
}

/**
 * Calculate CIE Delta E 2000 distance between two colors
 */
export function deltaE2000(color1: string, color2: string): number {
  const c1 = parseColor(color1);
  const c2 = parseColor(color2);
  
  if (!c1 || !c2) return Infinity;
  
  const lab1 = rgbToLab(c1.rgb);
  const lab2 = rgbToLab(c2.rgb);
  
  const L1 = lab1.l, a1 = lab1.a, b1 = lab1.b;
  const L2 = lab2.l, a2 = lab2.a, b2 = lab2.b;
  
  const C1 = Math.sqrt(a1 * a1 + b1 * b1);
  const C2 = Math.sqrt(a2 * a2 + b2 * b2);
  const Cab = (C1 + C2) / 2;
  
  const G = 0.5 * (1 - Math.sqrt(Math.pow(Cab, 7) / (Math.pow(Cab, 7) + Math.pow(25, 7))));
  
  const a1p = a1 * (1 + G);
  const a2p = a2 * (1 + G);
  
  const C1p = Math.sqrt(a1p * a1p + b1 * b1);
  const C2p = Math.sqrt(a2p * a2p + b2 * b2);
  
  const h1p = Math.atan2(b1, a1p) * 180 / Math.PI;
  const h2p = Math.atan2(b2, a2p) * 180 / Math.PI;
  
  const dLp = L2 - L1;
  const dCp = C2p - C1p;
  
  let dhp = 0;
  if (C1p * C2p !== 0) {
    if (Math.abs(h2p - h1p) <= 180) {
      dhp = h2p - h1p;
    } else if (h2p - h1p > 180) {
      dhp = h2p - h1p - 360;
    } else {
      dhp = h2p - h1p + 360;
    }
  }
  
  const dHp = 2 * Math.sqrt(C1p * C2p) * Math.sin(dhp * Math.PI / 360);
  
  const Lp = (L1 + L2) / 2;
  const Cp = (C1p + C2p) / 2;
  
  let Hp = 0;
  if (C1p * C2p !== 0) {
    if (Math.abs(h1p - h2p) <= 180) {
      Hp = (h1p + h2p) / 2;
    } else if (h1p + h2p < 360) {
      Hp = (h1p + h2p + 360) / 2;
    } else {
      Hp = (h1p + h2p - 360) / 2;
    }
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
  
  const kL = 1, kC = 1, kH = 1;
  
  const dE = Math.sqrt(
    Math.pow(dLp / (kL * SL), 2) +
    Math.pow(dCp / (kC * SC), 2) +
    Math.pow(dHp / (kH * SH), 2) +
    RT * (dCp / (kC * SC)) * (dHp / (kH * SH))
  );
  
  return dE;
}

// ============================================================================
// Palette Generation Functions
// ============================================================================

/**
 * Generate a gradient palette between two colors
 */
export function gradient(start: string, end: string, steps: number): string[] {
  if (steps < 2) return [start];
  
  const colors: string[] = [];
  for (let i = 0; i < steps; i++) {
    colors.push(mix(start, end, i / (steps - 1)));
  }
  
  return colors;
}

/**
 * Generate a monochromatic palette
 */
export function monochromatic(color: string, steps = 5): string[] {
  const parsed = parseColor(color);
  if (!parsed) return [color];
  
  const colors: string[] = [];
  const stepSize = 100 / (steps + 1);
  
  for (let i = 1; i <= steps; i++) {
    const l = stepSize * i;
    const hsl: HSL = { ...parsed.hsl, l };
    colors.push(rgbToHex(hslToRgb(hsl)));
  }
  
  return colors;
}

/**
 * Generate a complementary palette
 */
export function complementaryPalette(color: string): string[] {
  return [color, complement(color)];
}

/**
 * Generate a shades palette
 */
export function shades(color: string, count = 5): string[] {
  const colors: string[] = [];
  const stepSize = 100 / (count + 1);
  
  for (let i = 0; i < count; i++) {
    const l = stepSize * (i + 1);
    colors.push(darken(color, 100 - l));
  }
  
  return colors;
}

/**
 * Generate a tints palette
 */
export function tints(color: string, count = 5): string[] {
  const colors: string[] = [];
  const stepSize = 100 / (count + 1);
  
  for (let i = 0; i < count; i++) {
    const l = stepSize * (i + 1);
    colors.push(lighten(color, l));
  }
  
  return colors;
}

/**
 * Generate random color
 */
export function random(): string {
  const r = Math.floor(Math.random() * 256);
  const g = Math.floor(Math.random() * 256);
  const b = Math.floor(Math.random() * 256);
  return rgbToHex({ r, g, b });
}

/**
 * Generate random pastel color
 */
export function randomPastel(): string {
  const h = Math.random() * 360;
  const s = 40 + Math.random() * 20;
  const l = 70 + Math.random() * 20;
  return rgbToHex(hslToRgb({ h, s, l }));
}

/**
 * Generate random vibrant color
 */
export function randomVibrant(): string {
  const h = Math.random() * 360;
  const s = 80 + Math.random() * 20;
  const l = 45 + Math.random() * 15;
  return rgbToHex(hslToRgb({ h, s, l }));
}

/**
 * Find closest named color
 */
export function closestNamedColor(color: string): string {
  let minDistance = Infinity;
  let closest = 'black';
  
  for (const [name, hex] of Object.entries(CSS_NAMED_COLORS)) {
    const distance = rgbDistance(color, hex);
    if (distance < minDistance) {
      minDistance = distance;
      closest = name;
    }
  }
  
  return closest;
}

// ============================================================================
// Utility Functions
// ============================================================================

/**
 * Convert color to string in specified format
 */
export function toString(color: string, format: 'hex' | 'rgb' | 'hsl' | 'hsv'): string {
  const parsed = parseColor(color);
  if (!parsed) return color;
  
  switch (format) {
    case 'hex':
      return parsed.hex;
    case 'rgb':
      if (parsed.alpha < 1) {
        return `rgba(${parsed.rgb.r}, ${parsed.rgb.g}, ${parsed.rgb.b}, ${parsed.alpha})`;
      }
      return `rgb(${parsed.rgb.r}, ${parsed.rgb.g}, ${parsed.rgb.b})`;
    case 'hsl':
      if (parsed.alpha < 1) {
        return `hsla(${parsed.hsl.h}, ${parsed.hsl.s}%, ${parsed.hsl.l}%, ${parsed.alpha})`;
      }
      return `hsl(${parsed.hsl.h}, ${parsed.hsl.s}%, ${parsed.hsl.l}%)`;
    case 'hsv':
      if (parsed.alpha < 1) {
        return `hsva(${parsed.hsv.h}, ${parsed.hsv.s}%, ${parsed.hsv.v}%, ${parsed.alpha})`;
      }
      return `hsv(${parsed.hsv.h}, ${parsed.hsv.s}%, ${parsed.hsv.v}%)`;
    default:
      return parsed.hex;
  }
}

/**
 * Check if a string is a valid color
 */
export function isValidColor(color: string): boolean {
  return parseColor(color) !== null;
}

/**
 * Get color information object
 */
export function getColorInfo(color: string): ParseResult & { name?: string; isLight: boolean; luminance: number } | null {
  const parsed = parseColor(color);
  if (!parsed) return null;
  
  return {
    ...parsed,
    name: closestNamedColor(color),
    isLight: isLight(color),
    luminance: getLuminance(color),
  };
}

/**
 * Compare two colors for equality
 */
export function equals(color1: string, color2: string): boolean {
  const c1 = parseColor(color1);
  const c2 = parseColor(color2);
  
  if (!c1 || !c2) return false;
  
  return c1.rgb.r === c2.rgb.r &&
         c1.rgb.g === c2.rgb.g &&
         c1.rgb.b === c2.rgb.b &&
         c1.alpha === c2.alpha;
}

/**
 * Clone a color with modifications
 */
export function modify(color: string, options: Partial<{
  hue: number;
  saturation: number;
  lightness: number;
  alpha: number;
}>): string {
  const parsed = parseColor(color);
  if (!parsed) return color;
  
  let hsl = { ...parsed.hsl };
  
  if (options.hue !== undefined) {
    hsl.h = options.hue;
  }
  if (options.saturation !== undefined) {
    hsl.s = Math.min(100, Math.max(0, options.saturation));
  }
  if (options.lightness !== undefined) {
    hsl.l = Math.min(100, Math.max(0, options.lightness));
  }
  
  const rgb = hslToRgb(hsl);
  
  if (options.alpha !== undefined) {
    rgb.a = Math.min(1, Math.max(0, options.alpha));
  }
  
  return rgbToHex(rgb, rgb.a !== undefined && rgb.a !== 1);
}