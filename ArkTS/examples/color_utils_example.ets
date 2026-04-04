/**
 * Color Utils Example for ArkTS/HarmonyOS
 * 
 * Demonstrates various color manipulation features
 */

import { Color, ColorUtils, BlendMode } from '../color_utils/mod';

function example1_basicColorCreation(): void {
  console.info('\n=== Example 1: Basic Color Creation ===');
  
  // Create colors using RGB values
  const red = new Color(255, 0, 0);
  const green = new Color(0, 255, 0);
  const blue = new Color(0, 0, 255);
  
  console.info(`Red: ${red.toHex()} - ${red.toRgb()}`);
  console.info(`Green: ${green.toHex()} - ${green.toRgb()}`);
  console.info(`Blue: ${blue.toHex()} - ${blue.toRgb()}`);
  
  // Create color with alpha (transparency)
  const semiTransparent = new Color(128, 64, 192, 0.5);
  console.info(`Semi-transparent: ${semiTransparent.toHex()} - ${semiTransparent.toRgb()}`);
}

function example2_parsingColors(): void {
  console.info('\n=== Example 2: Parsing Colors ===');
  
  // Parse HEX colors
  const hexColor = ColorUtils.parseHex('#ff5733');
  if (hexColor) {
    console.info(`Parsed HEX #ff5733: ${hexColor.toRgb()}`);
  }
  
  // Parse RGB strings
  const rgbColor = ColorUtils.parseRgb('rgb(100, 150, 200)');
  if (rgbColor) {
    console.info(`Parsed RGB: ${rgbColor.toHex()}`);
  }
  
  // Parse HSL strings
  const hslColor = ColorUtils.parseHsl('hsl(120, 50%, 50%)');
  if (hslColor) {
    console.info(`Parsed HSL: ${hslColor.toHex()}`);
  }
  
  // Parse named colors
  const namedColor = ColorUtils.parse('orange');
  if (namedColor) {
    console.info(`Parsed 'orange': ${namedColor.toHex()}`);
  }
  
  // Validate colors
  console.info(`Is '#ff0000' valid? ${ColorUtils.isValid('#ff0000')}`);
  console.info(`Is 'invalid' valid? ${ColorUtils.isValid('invalid')}`);
}

function example3_colorConversions(): void {
  console.info('\n=== Example 3: Color Format Conversions ===');
  
  const color = new Color(100, 150, 200);
  
  console.info(`Original RGB: ${color.toRgb()}`);
  console.info(`HEX: ${color.toHex()}`);
  console.info(`HSL: ${color.toHslString()}`);
  
  const hsl = color.toHsl();
  console.info(`HSL Components - H: ${Math.round(hsl.h)}, S: ${Math.round(hsl.s)}%, L: ${Math.round(hsl.l)}%`);
  
  const hsv = color.toHsv();
  console.info(`HSV Components - H: ${Math.round(hsv.h)}, S: ${Math.round(hsv.s)}%, V: ${Math.round(hsv.v)}%`);
  
  const cmyk = color.toCmyk();
  console.info(`CMYK Components - C: ${cmyk.c}%, M: ${cmyk.m}%, Y: ${cmyk.y}%, K: ${cmyk.k}%`);
}

function example4_colorManipulation(): void {
  console.info('\n=== Example 4: Color Manipulation ===');
  
  const baseColor = new Color(100, 100, 200);
  console.info(`Base color: ${baseColor.toHex()}`);
  
  // Lighten and darken
  const lighter = baseColor.lighten(20);
  const darker = baseColor.darken(20);
  console.info(`Lighten 20%: ${lighter.toHex()}`);
  console.info(`Darken 20%: ${darker.toHex()}`);
  
  // Saturate and desaturate
  const moreSaturated = baseColor.saturate(30);
  const lessSaturated = baseColor.desaturate(30);
  console.info(`Saturate 30%: ${moreSaturated.toHex()}`);
  console.info(`Desaturate 30%: ${lessSaturated.toHex()}`);
  
  // Fade (transparency)
  const faded = baseColor.fade(50);
  console.info(`Fade 50%: ${faded.toHex()} (alpha: ${faded.a})`);
  
  // Complementary color
  const complement = baseColor.complement();
  console.info(`Complement: ${complement.toHex()}`);
  
  // Contrast color (black or white)
  const contrast = baseColor.contrast();
  console.info(`Contrast: ${contrast.toHex()}`);
}

function example5_colorMixing(): void {
  console.info('\n=== Example 5: Color Mixing ===');
  
  const red = new Color(255, 0, 0);
  const blue = new Color(0, 0, 255);
  
  console.info(`Red: ${red.toHex()}`);
  console.info(`Blue: ${blue.toHex()}`);
  
  // Mix with different ratios
  const mix25 = red.mix(blue, 0.25);
  const mix50 = red.mix(blue, 0.5);
  const mix75 = red.mix(blue, 0.75);
  
  console.info(`Mix 25% blue: ${mix25.toHex()}`);
  console.info(`Mix 50% blue: ${mix50.toHex()}`);
  console.info(`Mix 75% blue: ${mix75.toHex()}`);
}

function example6_gradients(): void {
  console.info('\n=== Example 6: Color Gradients ===');
  
  const start = new Color(255, 0, 0);
  const end = new Color(0, 0, 255);
  
  console.info(`Gradient from ${start.toHex()} to ${end.toHex()}:`);
  
  const gradient = ColorUtils.gradient(start, end, 5);
  gradient.forEach((color, index) => {
    console.info(`  Step ${index + 1}: ${color.toHex()}`);
  });
}

function example7_colorSchemes(): void {
  console.info('\n=== Example 7: Color Schemes ===');
  
  const base = new Color(200, 100, 50);
  console.info(`Base color: ${base.toHex()}`);
  
  // Analogous colors
  const analogous = ColorUtils.analogous(base, 3);
  console.info('Analogous colors:');
  analogous.forEach((c, i) => console.info(`  ${i + 1}: ${c.toHex()}`));
  
  // Triadic colors
  const triadic = ColorUtils.triadic(base);
  console.info('Triadic colors:');
  triadic.forEach((c, i) => console.info(`  ${i + 1}: ${c.toHex()}`));
  
  // Monochromatic colors
  const monochromatic = ColorUtils.monochromatic(base, 5);
  console.info('Monochromatic colors:');
  monochromatic.forEach((c, i) => console.info(`  ${i + 1}: ${c.toHex()}`));
}

function example8_randomColors(): void {
  console.info('\n=== Example 8: Random Colors ===');
  
  console.info('Random colors:');
  for (let i = 0; i < 3; i++) {
    const random = ColorUtils.random();
    console.info(`  ${random.toHex()}`);
  }
  
  console.info('Random bright colors:');
  for (let i = 0; i < 3; i++) {
    const bright = ColorUtils.randomBright();
    console.info(`  ${bright.toHex()}`);
  }
  
  console.info('Random pastel colors:');
  for (let i = 0; i < 3; i++) {
    const pastel = ColorUtils.randomPastel();
    console.info(`  ${pastel.toHex()}`);
  }
}

function example9_accessibility(): void {
  console.info('\n=== Example 9: Accessibility (WCAG) ===');
  
  const background = new Color(255, 255, 255);
  const textColor = new Color(50, 50, 50);
  
  const ratio = ColorUtils.contrastRatio(background, textColor);
  console.info(`Contrast ratio: ${ratio.toFixed(2)}`);
  console.info(`Meets WCAG AA: ${ColorUtils.meetsWCAGAA(background, textColor)}`);
  console.info(`Meets WCAG AAA: ${ColorUtils.meetsWCAGAAA(background, textColor)}`);
  
  // Best contrast
  const accent = new Color(200, 100, 50);
  const bestContrast = ColorUtils.bestContrast(accent);
  console.info(`Best contrast for ${accent.toHex()}: ${bestContrast.toHex()}`);
}

function example10_blendModes(): void {
  console.info('\n=== Example 10: Blend Modes ===');
  
  const base = new Color(128, 128, 128);
  const blend = new Color(255, 0, 0);
  
  console.info(`Base: ${base.toHex()}, Blend: ${blend.toHex()}`);
  
  const multiply = ColorUtils.blend(base, blend, BlendMode.MULTIPLY);
  const screen = ColorUtils.blend(base, blend, BlendMode.SCREEN);
  const overlay = ColorUtils.blend(base, blend, BlendMode.OVERLAY);
  
  console.info(`Multiply: ${multiply.toHex()}`);
  console.info(`Screen: ${screen.toHex()}`);
  console.info(`Overlay: ${overlay.toHex()}`);
}

// Run all examples
export function runAllExamples(): void {
  example1_basicColorCreation();
  example2_parsingColors();
  example3_colorConversions();
  example4_colorManipulation();
  example5_colorMixing();
  example6_gradients();
  example7_colorSchemes();
  example8_randomColors();
  example9_accessibility();
  example10_blendModes();
  
  console.info('\n=== All examples completed ===');
}

// Run if executed directly
runAllExamples();
