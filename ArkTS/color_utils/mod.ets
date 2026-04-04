/**
 * Color Utilities Module for ArkTS/HarmonyOS
 * 
 * A comprehensive color manipulation library providing:
 * - Color format conversion (HEX, RGB, RGBA, HSL, HSV, CMYK)
 * - Color manipulation (lighten, darken, saturate, desaturate)
 * - Color blending (mix, blend modes)
 * - Color generation (random, gradient)
 * - Color validation and parsing
 * 
 * Zero dependencies - uses only ArkTS standard library
 * 
 * @module ColorUtils
 * @version 1.0.0
 * @author AllToolkit
 */

/**
 * Represents a color with RGBA components
 */
export class Color {
  r: number;  // Red (0-255)
  g: number;  // Green (0-255)
  b: number;  // Blue (0-255)
  a: number;  // Alpha (0-1)

  constructor(r: number = 0, g: number = 0, b: number = 0, a: number = 1) {
    this.r = ColorUtils.clamp(r, 0, 255);
    this.g = ColorUtils.clamp(g, 0, 255);
    this.b = ColorUtils.clamp(b, 0, 255);
    this.a = ColorUtils.clamp(a, 0, 1);
  }

  /**
   * Convert to HEX string (#RRGGBB or #RRGGBBAA)
   */
  toHex(): string {
    const toHexChannel = (c: number): string => {
      const hex = Math.round(c).toString(16);
      return hex.length === 1 ? '0' + hex : hex;
    };
    
    let hex = `#${toHexChannel(this.r)}${toHexChannel(this.g)}${toHexChannel(this.b)}`;
    if (this.a < 1) {
      hex += toHexChannel(Math.round(this.a * 255));
    }
    return hex.toLowerCase();
  }

  /**
   * Convert to RGB string (rgb(r, g, b) or rgba(r, g, b, a))
   */
  toRgb(): string {
    if (this.a < 1) {
      return `rgba(${Math.round(this.r)}, ${Math.round(this.g)}, ${Math.round(this.b)}, ${this.a})`;
    }
    return `rgb(${Math.round(this.r)}, ${Math.round(this.g)}, ${Math.round(this.b)})`;
  }

  /**
   * Convert to HSL object
   */
  toHsl(): { h: number; s: number; l: number; a: number } {
    const r = this.r / 255;
    const g = this.g / 255;
    const b = this.b / 255;

    const max = Math.max(r, g, b);
    const min = Math.min(r, g, b);
    let h = 0;
    let s = 0;
    const l = (max + min) / 2;

    if (max !== min) {
      const d = max - min;
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

    return { h: h * 360, s: s * 100, l: l * 100, a: this.a };
  }

  /**
   * Convert to HSL string
   */
  toHslString(): string {
    const hsl = this.toHsl();
    if (this.a < 1) {
      return `hsla(${Math.round(hsl.h)}, ${Math.round(hsl.s)}%, ${Math.round(hsl.l)}%, ${this.a})`;
    }
    return `hsl(${Math.round(hsl.h)}, ${Math.round(hsl.s)}%, ${Math.round(hsl.l)}%)`;
  }

  /**
   * Convert to HSV object
   */
  toHsv(): { h: number; s: number; v: number; a: number } {
    const r = this.r / 255;
    const g = this.g / 255;
    const b = this.b / 255;

    const max = Math.max(r, g, b);
    const min = Math.min(r, g, b);
    const d = max - min;
    
    let h = 0;
    const s = max === 0 ? 0 : d / max;
    const v = max;

    if (max !== min) {
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

    return { h: h * 360, s: s * 100, v: v * 100, a: this.a };
  }

  /**
   * Convert to CMYK object
   */
  toCmyk(): { c: number; m: number; y: number; k: number; a: number } {
    const r = this.r / 255;
    const g = this.g / 255;
    const b = this.b / 255;

    const k = 1 - Math.max(r, g, b);
    const c = k === 1 ? 0 : (1 - r - k) / (1 - k);
    const m = k === 1 ? 0 : (1 - g - k) / (1 - k);
    const y = k === 1 ? 0 : (1 - b - k) / (1 - k);

    return {
      c: Math.round(c * 100),
      m: Math.round(m * 100),
      y: Math.round(y * 100),
      k: Math.round(k * 100),
      a: this.a
    };
  }

  /**
   * Lighten the color by a percentage (0-100)
   */
  lighten(amount: number): Color {
    const hsl = this.toHsl();
    hsl.l = Math.min(100, hsl.l + amount);
    return ColorUtils.hslToRgb(hsl.h, hsl.s, hsl.l, hsl.a);
  }

  /**
   * Darken the color by a percentage (0-100)
   */
  darken(amount: number): Color {
    const hsl = this.toHsl();
    hsl.l = Math.max(0, hsl.l - amount);
    return ColorUtils.hslToRgb(hsl.h, hsl.s, hsl.l, hsl.a);
  }

  /**
   * Saturate the color by a percentage (0-100)
   */
  saturate(amount: number): Color {
    const hsl = this.toHsl();
    hsl.s = Math.min(100, hsl.s + amount);
    return ColorUtils.hslToRgb(hsl.h, hsl.s, hsl.l, hsl.a);
  }

  /**
   * Desaturate the color by a percentage (0-100)
   */
  desaturate(amount: number): Color {
    const hsl = this.toHsl();
    hsl.s = Math.max(0, hsl.s - amount);
    return ColorUtils.hslToRgb(hsl.h, hsl.s, hsl.l, hsl.a);
  }

  /**
   * Fade the color by a percentage (0-100)
   */
  fade(amount: number): Color {
    return new Color(this.r, this.g, this.b, this.a * (1 - amount / 100));
  }

  /**
   * Get grayscale value (0-255)
   */
  grayscale(): number {
    return Math.round(0.299 * this.r + 0.587 * this.g + 0.114 * this.b);
  }

  /**
   * Get brightness value (0-255)
   */
  brightness(): number {
    return Math.round((this.r * 299 + this.g * 587 + this.b * 114) / 1000);
  }

  /**
   * Check if color is light (brightness > 128)
   */
  isLight(): boolean {
    return this.brightness() > 128;
  }

  /**
   * Check if color is dark (brightness <= 128)
   */
  isDark(): boolean {
    return !this.isLight();
  }

  /**
   * Get complementary color
   */
  complement(): Color {
    const hsl = this.toHsl();
    return ColorUtils.hslToRgb((hsl.h + 180) % 360, hsl.s, hsl.l, hsl.a);
  }

  /**
   * Get contrast color (black or white)
   */
  contrast(): Color {
    return this.isLight() ? new Color(0, 0, 0) : new Color(255, 255, 255);
  }

  /**
   * Mix with another color (0-1 ratio)
   */
  mix(other: Color, ratio: number = 0.5): Color {
    const r = this.r * (1 - ratio) + other.r * ratio;
    const g = this.g * (1 - ratio) + other.g * ratio;
    const b = this.b * (1 - ratio) + other.b * ratio;
    const a = this.a * (1 - ratio) + other.a * ratio;
    return new Color(r, g, b, a);
  }

  /**
   * Clone the color
   */
  clone(): Color {
    return new Color(this.r, this.g, this.b, this.a);
  }

  /**
   * Check if equal to another color
   */
  equals(other: Color): boolean {
    return this.r === other.r && this.g === other.g && 
           this.b === other.b && this.a === other.a;
  }
}

/**
 * Color utility functions
 */
export class ColorUtils {
  /**
   * Clamp a value between min and max
   */
  static clamp(value: number, min: number, max: number): number {
    return Math.max(min, Math.min(max, value));
  }

  /**
   * Parse HEX color string
   * Supports: #RGB, #RGBA, #RRGGBB, #RRGGBBAA
   */
  static parseHex(hex: string): Color | null {
    const clean = hex.trim().replace('#', '');
    
    if (!/^[0-9A-Fa-f]+$/.test(clean)) {
      return null;
    }

    let r: number, g: number, b: number, a: number = 1;

    if (clean.length === 3) {
      r = parseInt(clean[0] + clean[0], 16);
      g = parseInt(clean[1] + clean[1], 16);
      b = parseInt(clean[2] + clean[2], 16);
    } else if (clean.length === 4) {
      r = parseInt(clean[0] + clean[0], 16);
      g = parseInt(clean[1] + clean[1], 16);
      b = parseInt(clean[2] + clean[2], 16);
      a = parseInt(clean[3] + clean[3], 16) / 255;
    } else if (clean.length === 6) {
      r = parseInt(clean.substring(0, 2), 16);
      g = parseInt(clean.substring(2, 4), 16);
      b = parseInt(clean.substring(4, 6), 16);
    } else if (clean.length === 8) {
      r = parseInt(clean.substring(0, 2), 16);
      g = parseInt(clean.substring(2, 4), 16);
      b = parseInt(clean.substring(4, 6), 16);
      a = parseInt(clean.substring(6, 8), 16) / 255;
    } else {
      return null;
    }

    return new Color(r, g, b, a);
  }

  /**
   * Parse RGB/RGBA string
   * Supports: rgb(r, g, b), rgba(r, g, b, a)
   */
  static parseRgb(rgb: string): Color | null {
    const rgbaMatch = rgb.match(/rgba?\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*(?:,\s*([\d.]+)\s*)?\)/);
    if (!rgbaMatch) {
      return null;
    }

    const r = parseInt(rgbaMatch[1], 10);
    const g = parseInt(rgbaMatch[2], 10);
    const b = parseInt(rgbaMatch[3], 10);
    const a = rgbaMatch[4] ? parseFloat(rgbaMatch[4]) : 1;

    return new Color(r, g, b, a);
  }

  /**
   * Parse HSL/HSLA string
   * Supports: hsl(h, s%, l%), hsla(h, s%, l%, a)
   */
  static parseHsl(hsl: string): Color | null {
    const hslaMatch = hsl.match(/hsla?\s*\(\s*(\d+)\s*,\s*(\d+)%\s*,\s*(\d+)%\s*(?:,\s*([\d.]+)\s*)?\)/);
    if (!hslaMatch) {
      return null;
    }

    const h = parseInt(hslaMatch[1], 10);
    const s = parseInt(hslaMatch[2], 10);
    const l = parseInt(hslaMatch[3], 10);
    const a = hslaMatch[4] ? parseFloat(hslaMatch[4]) : 1;

    return ColorUtils.hslToRgb(h, s, l, a);
  }

  /**
   * Convert HSL to RGB
   */
  static hslToRgb(h: number, s: number, l: number, a: number = 1): Color {
    h = h % 360 / 360;
    s = s / 100;
    l = l / 100;

    let r: number, g: number, b: number;

    if (s === 0) {
      r = g = b = l;
    } else {
      const hue2rgb = (p: number, q: number, t: number): number => {
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

    return new Color(r * 255, g * 255, b * 255, a);
  }

  /**
   * Convert HSV to RGB
   */
  static hsvToRgb(h: number, s: number, v: number, a: number = 1): Color {
    h = h % 360 / 360;
    s = s / 100;
    v = v / 100;

    let r: number, g: number, b: number;

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
      default: r = g = b = 0;
    }

    return new Color(r * 255, g * 255, b * 255, a);
  }

  /**
   * Convert CMYK to RGB
   */
  static cmykToRgb(c: number, m: number, y: number, k: number, a: number = 1): Color {
    c = c / 100;
    m = m / 100;
    y = y / 100;
    k = k / 100;

    const r = 255 * (1 - c) * (1 - k);
    const g = 255 * (1 - m) * (1 - k);
    const b = 255 * (1 - y) * (1 - k);

    return new Color(r, g, b, a);
  }

  /**
   * Parse any color string (HEX, RGB, RGBA, HSL, HSLA)
   */
  static parse(color: string): Color | null {
    const trimmed = color.trim().toLowerCase();
    
    if (trimmed.startsWith('#')) {
      return ColorUtils.parseHex(trimmed);
    }
    if (trimmed.startsWith('rgb')) {
      return ColorUtils.parseRgb(trimmed);
    }
    if (trimmed.startsWith('hsl')) {
      return ColorUtils.parseHsl(trimmed);
    }
    
    // Named colors
    const namedColors: Record<string, string> = {
      'black': '#000000',
      'white': '#ffffff',
      'red': '#ff0000',
      'green': '#008000',
      'blue': '#0000ff',
      'yellow': '#ffff00',
      'cyan': '#00ffff',
      'magenta': '#ff00ff',
      'silver': '#c0c0c0',
      'gray': '#808080',
      'maroon': '#800000',
      'olive': '#808000',
      'lime': '#00ff00',
      'aqua': '#00ffff',
      'teal': '#008080',
      'navy': '#000080',
      'fuchsia': '#ff00ff',
      'purple': '#800080',
      'orange': '#ffa500'
    };
    
    if (namedColors[trimmed]) {
      return ColorUtils.parseHex(namedColors[trimmed]);
    }
    
    return null;
  }

  /**
   * Validate if string is a valid color
   */
  static isValid(color: string): boolean {
    return ColorUtils.parse(color) !== null;
  }

  /**
   * Generate random color
   */
  static random(alpha: number = 1): Color {
    const r = Math.floor(Math.random() * 256);
    const g = Math.floor(Math.random() * 256);
    const b = Math.floor(Math.random() * 256);
    return new Color(r, g, b, alpha);
  }

  /**
   * Generate random bright color
   */
  static randomBright(): Color {
    const h = Math.random() * 360;
    const s = 70 + Math.random() * 30;
    const l = 50 + Math.random() * 20;
    return ColorUtils.hslToRgb(h, s, l);
  }

  /**
   * Generate random pastel color
   */
  static randomPastel(): Color {
    const h = Math.random() * 360;
    const s = 25 + Math.random() * 25;
    const l = 70 + Math.random() * 20;
    return ColorUtils.hslToRgb(h, s, l);
  }

  /**
   * Generate random dark color
   */
  static randomDark(): Color {
    const h = Math.random() * 360;
    const s = 50 + Math.random() * 50;
    const l = 10 + Math.random() * 20;
    return ColorUtils.hslToRgb(h, s, l);
  }

  /**
   * Generate color gradient
   */
  static gradient(start: Color, end: Color, steps: number): Color[] {
    const colors: Color[] = [];
    for (let i = 0; i < steps; i++) {
      const ratio = i / (steps - 1);
      colors.push(start.mix(end, ratio));
    }
    return colors;
  }

  /**
   * Generate analogous colors
   */
  static analogous(color: Color, count: number = 3): Color[] {
    const hsl = color.toHsl();
    const colors: Color[] = [color.clone()];
    const step = 30;
    
    for (let i = 1; i < count; i++) {
      const offset = ((i + 1) / 2) * step * (i % 2 === 1 ? 1 : -1);
      colors.push(ColorUtils.hslToRgb((hsl.h + offset) % 360, hsl.s, hsl.l, hsl.a));
    }
    
    return colors;
  }

  /**
   * Generate triadic colors
   */
  static triadic(color: Color): Color[] {
    const hsl = color.toHsl();
    return [
      color.clone(),
      ColorUtils.hslToRgb((hsl.h + 120) % 360, hsl.s, hsl.l, hsl.a),
      ColorUtils.hslToRgb((hsl.h + 240) % 360, hsl.s, hsl.l, hsl.a)
    ];
  }

  /**
   * Generate tetradic colors (rectangle)
   */
  static tetradic(color: Color): Color[] {
    const hsl = color.toHsl();
    return [
      color.clone(),
      ColorUtils.hslToRgb((hsl.h + 90) % 360, hsl.s, hsl.l, hsl.a),
      ColorUtils.hslToRgb((hsl.h + 180) % 360, hsl.s, hsl.l, hsl.a),
      ColorUtils.hslToRgb((hsl.h + 270) % 360, hsl.s, hsl.l, hsl.a)
    ];
  }

  /**
   * Generate split complementary colors
   */
  static splitComplementary(color: Color): Color[] {
    const hsl = color.toHsl();
    return [
      color.clone(),
      ColorUtils.hslToRgb((hsl.h + 150) % 360, hsl.s, hsl.l, hsl.a),
      ColorUtils.hslToRgb((hsl.h + 210) % 360, hsl.s, hsl.l, hsl.a)
    ];
  }

  /**
   * Generate monochromatic colors
   */
  static monochromatic(color: Color, count: number = 5): Color[] {
    const hsl = color.toHsl();
    const colors: Color[] = [];
    const step = 100 / (count + 1);
    
    for (let i = 1; i <= count; i++) {
      const l = step * i;
      colors.push(ColorUtils.hslToRgb(hsl.h, hsl.s, l, hsl.a));
    }
    
    return colors;
  }

  /**
   * Blend two colors using different modes
   */
  static blend(color1: Color, color2: Color, mode: BlendMode): Color {
    const r1 = color1.r / 255, g1 = color1.g / 255, b1 = color1.b / 255;
    const r2 = color2.r / 255, g2 = color2.g / 255, b2 = color2.b / 255;
    let r: number, g: number, b: number;

    switch (mode) {
      case BlendMode.MULTIPLY:
        r = r1 * r2;
        g = g1 * g2;
        b = b1 * b2;
        break;
      case BlendMode.SCREEN:
        r = 1 - (1 - r1) * (1 - r2);
        g = 1 - (1 - g1) * (1 - g2);
        b = 1 - (1 - b1) * (1 - b2);
        break;
      case BlendMode.OVERLAY:
        r = r2 < 0.5 ? 2 * r1 * r2 : 1 - 2 * (1 - r1) * (1 - r2);
        g = g2 < 0.5 ? 2 * g1 * g2 : 1 - 2 * (1 - g1) * (1 - g2);
        b = b2 < 0.5 ? 2 * b1 * b2 : 1 - 2 * (1 - b1) * (1 - b2);
        break;
      case BlendMode.DARKEN:
        r = Math.min(r1, r2);
        g = Math.min(g1, g2);
        b = Math.min(b1, b2);
        break;
      case BlendMode.LIGHTEN:
        r = Math.max(r1, r2);
        g = Math.max(g1, g2);
        b = Math.max(b1, b2);
        break;
      case BlendMode.COLOR_DODGE:
        r = r2 === 1 ? 1 : r1 / (1 - r2);
        g = g2 === 1 ? 1 : g1 / (1 - g2);
        b = b2 === 1 ? 1 : b1 / (1 - b2);
        break;
      case BlendMode.COLOR_BURN:
        r = r2 === 0 ? 0 : 1 - (1 - r1) / r2;
        g = g2 === 0 ? 0 : 1 - (1 - g1) / g2;
        b = b2 === 0 ? 0 : 1 - (1 - b1) / b2;
        break;
      case BlendMode.DIFFERENCE:
        r = Math.abs(r1 - r2);
        g = Math.abs(g1 - g2);
        b = Math.abs(b1 - b2);
        break;
      case BlendMode.EXCLUSION:
        r = r1 + r2 - 2 * r1 * r2;
        g = g1 + g2 - 2 * g1 * g2;
        b = b1 + b2 - 2 * b1 * b2;
        break;
      case BlendMode.HARD_LIGHT:
        r = r1 < 0.5 ? 2 * r1 * r2 : 1 - 2 * (1 - r1) * (1 - r2);
        g = g1 < 0.5 ? 2 * g1 * g2 : 1 - 2 * (1 - g1) * (1 - g2);
        b = b1 < 0.5 ? 2 * b1 * b2 : 1 - 2 * (1 - b1) * (1 - b2);
        break;
      case BlendMode.SOFT_LIGHT:
        r = r2 < 0.5 ? 2 * r1 * r2 + r1 * r1 * (1 - 2 * r2) : 2 * r1 * (1 - r2) + Math.sqrt(r1) * (2 * r2 - 1);
        g = g2 < 0.5 ? 2 * g1 * g2 + g1 * g1 * (1 - 2 * g2) : 2 * g1 * (1 - g2) + Math.sqrt(g1) * (2 * g2 - 1);
        b = b2 < 0.5 ? 2 * b1 * b2 + b1 * b1 * (1 - 2 * b2) : 2 * b1 * (1 - b2) + Math.sqrt(b1) * (2 * b2 - 1);
        break;
      default:
        return color1.mix(color2);
    }

    return new Color(r * 255, g * 255, b * 255, (color1.a + color2.a) / 2);
  }

  /**
   * Get luminance of color (0-1)
   */
  static luminance(color: Color): number {
    const r = color.r / 255;
    const g = color.g / 255;
    const b = color.b / 255;
    
    const rLinear = r <= 0.03928 ? r / 12.92 : Math.pow((r + 0.055) / 1.055, 2.4);
    const gLinear = g <= 0.03928 ? g / 12.92 : Math.pow((g + 0.055) / 1.055, 2.4);
    const bLinear = b <= 0.03928 ? b / 12.92 : Math.pow((b + 0.055) / 1.055, 2.4);
    
    return 0.2126 * rLinear + 0.7152 * gLinear + 0.0722 * bLinear;
  }

  /**
   * Calculate contrast ratio between two colors (1-21)
   */
  static contrastRatio(color1: Color, color2: Color): number {
    const lum1 = ColorUtils.luminance(color1);
    const lum2 = ColorUtils.luminance(color2);
    const brightest = Math.max(lum1, lum2);
    const darkest = Math.min(lum1, lum2);
    return (brightest + 0.05) / (darkest + 0.05);
  }

  /**
   * Check if color combination meets WCAG AA standard
   */
  static meetsWCAGAA(color1: Color, color2: Color, largeText: boolean = false): boolean {
    const ratio = ColorUtils.contrastRatio(color1, color2);
    return largeText ? ratio >= 3 : ratio >= 4.5;
  }

  /**
   * Check if color combination meets WCAG AAA standard
   */
  static meetsWCAGAAA(color1: Color, color2: Color, largeText: boolean = false): boolean {
    const ratio = ColorUtils.contrastRatio(color1, color2);
    return largeText ? ratio >= 4.5 : ratio >= 7;
  }

  /**
   * Get best contrast color (black or white)
   */
  static bestContrast(color: Color): Color {
    const black = new Color(0, 0, 0);
    const white = new Color(255, 255, 255);
    const blackContrast = ColorUtils.contrastRatio(color, black);
    const whiteContrast = ColorUtils.contrastRatio(color, white);
    return blackContrast > whiteContrast ? black : white;
  }

  // Common color constants
  static readonly BLACK = new Color(0, 0, 0);
  static readonly WHITE = new Color(255, 255, 255);
  static readonly RED = new Color(255, 0, 0);
  static readonly GREEN = new Color(0, 128, 0);
  static readonly BLUE = new Color(0, 0, 255);
  static readonly YELLOW = new Color(255, 255, 0);
  static readonly CYAN = new Color(0, 255, 255);
  static readonly MAGENTA = new Color(255, 0, 255);
  static readonly TRANSPARENT = new Color(0, 0, 0, 0);
}

/**
 * Blend modes for color blending
 */
export enum BlendMode {
  NORMAL,
  MULTIPLY,
  SCREEN,
  OVERLAY,
  DARKEN,
  LIGHTEN,
  COLOR_DODGE,
  COLOR_BURN,
  DIFFERENCE,
  EXCLUSION,
  HARD_LIGHT,
  SOFT_LIGHT
}
