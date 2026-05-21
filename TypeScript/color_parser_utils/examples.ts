/**
 * Color Parser Utilities - Usage Examples
 * 
 * This file demonstrates various use cases for the color parsing library.
 */

import {
  parseColor,
  rgbToHex,
  hexToRgb,
  rgbToHsl,
  hslToRgb,
  rgbToHsv,
  hsvToRgb,
  rgbToCmyk,
  cmykToRgb,
  rgbToLab,
  labToRgb,
  lighten,
  darken,
  saturate,
  desaturate,
  adjustHue,
  setAlpha,
  mix,
  invert,
  grayscale,
  sepia,
  getLuminance,
  getContrastRatio,
  meetsWCAG,
  getWCAGRating,
  isLight,
  complement,
  analogous,
  triadic,
  tetradic,
  splitComplementary,
  rgbDistance,
  deltaE2000,
  gradient,
  monochromatic,
  shades,
  tints,
  random,
  randomPastel,
  randomVibrant,
  closestNamedColor,
  toString,
  isValidColor,
  getColorInfo,
  equals,
  modify,
  CSS_NAMED_COLORS,
} from './color_parser';

console.log('='.repeat(60));
console.log('Color Parser Utilities - Examples');
console.log('='.repeat(60));

// ============================================================================
// 1. Basic Color Parsing
// ============================================================================

console.log('\n--- 1. Basic Color Parsing ---\n');

// Parse various color formats
const colors = [
  '#FF5733',           // 6-digit hex
  '#F53',              // 3-digit shorthand
  '#FF573380',         // 8-digit hex with alpha
  'rgb(255, 87, 51)',  // RGB
  'rgba(255, 87, 51, 0.5)', // RGBA
  'hsl(10, 100%, 60%)', // HSL
  'red',               // Named color
  'Cornflower Blue',   // Named color with spaces
];

for (const color of colors) {
  const parsed = parseColor(color);
  if (parsed) {
    console.log(`${color.padEnd(25)} → ${parsed.hex}`);
  }
}

// ============================================================================
// 2. Color Space Conversions
// ============================================================================

console.log('\n--- 2. Color Space Conversions ---\n');

const coral = '#FF7F50';

console.log('Original:', coral);

// RGB
const rgb = hexToRgb(coral);
console.log('RGB:', rgb);

// HSL
const hsl = rgbToHsl(rgb!);
console.log('HSL:', hsl);

// HSV
const hsv = rgbToHsv(rgb!);
console.log('HSV:', hsv);

// CMYK
const cmyk = rgbToCmyk(rgb!);
console.log('CMYK:', cmyk);

// LAB
const lab = rgbToLab(rgb!);
console.log('LAB:', lab);

// Roundtrip back
console.log('RGB from HSL:', rgbToHex(hslToRgb(hsl)));
console.log('RGB from HSV:', rgbToHex(hsvToRgb(hsv)));
console.log('RGB from CMYK:', rgbToHex(cmykToRgb(cmyk)));
console.log('RGB from LAB:', rgbToHex(labToRgb(lab)));

// ============================================================================
// 3. Color Manipulation
// ============================================================================

console.log('\n--- 3. Color Manipulation ---\n');

const baseColor = '#3498db';

console.log('Base:', baseColor);
console.log('Lighter:', lighten(baseColor, 20));
console.log('Darker:', darken(baseColor, 20));
console.log('Saturated:', saturate(baseColor, 30));
console.log('Desaturated:', desaturate(baseColor, 30));
console.log('Hue +60°:', adjustHue(baseColor, 60));
console.log('Hue -60°:', adjustHue(baseColor, -60));
console.log('With 50% alpha:', setAlpha(baseColor, 0.5));
console.log('Inverted:', invert(baseColor));
console.log('Grayscale:', grayscale(baseColor));
console.log('Sepia:', sepia(baseColor));

// Mix colors
console.log('\nMixing colors:');
console.log('Red + Green (50%):', mix('#FF0000', '#00FF00', 0.5));
console.log('Red + Blue (25%):', mix('#FF0000', '#0000FF', 0.25));
console.log('Black + White (50%):', mix('#000000', '#FFFFFF', 0.5));

// ============================================================================
// 4. Color Harmony
// ============================================================================

console.log('\n--- 4. Color Harmony ---\n');

const base = '#E74C3C';

console.log('Base:', base);
console.log('\nComplementary:');
console.log(' ', complement(base));

console.log('\nAnalogous (±30°):');
console.log(' ', analogous(base, 30).join(' '));

console.log('\nTriadic:');
console.log(' ', triadic(base).join(' '));

console.log('\nTetradic:');
console.log(' ', tetradic(base).join(' '));

console.log('\nSplit Complementary:');
console.log(' ', splitComplementary(base).join(' '));

// ============================================================================
// 5. Accessibility & Contrast
// ============================================================================

console.log('\n--- 5. Accessibility & Contrast ---\n');

const textColors = [
  { fg: '#FFFFFF', bg: '#000000', name: 'White on Black' },
  { fg: '#000000', bg: '#FFFFFF', name: 'Black on White' },
  { fg: '#777777', bg: '#FFFFFF', name: 'Gray on White' },
  { fg: '#FFFFFF', bg: '#3498DB', name: 'White on Blue' },
  { fg: '#E74C3C', bg: '#FFFFFF', name: 'Red on White' },
];

console.log('Contrast Ratios & WCAG Compliance:');
console.log('-'.repeat(60));

for (const { fg, bg, name } of textColors) {
  const ratio = getContrastRatio(fg, bg);
  const rating = getWCAGRating(fg, bg);
  const aaPass = meetsWCAG(fg, bg, 'AA');
  const aaaPass = meetsWCAG(fg, bg, 'AAA');
  
  console.log(`\n${name}:`);
  console.log(`  Contrast: ${ratio.toFixed(2)}:1`);
  console.log(`  Rating: ${rating}`);
  console.log(`  AA Pass: ${aaPass ? '✓' : '✗'}`);
  console.log(`  AAA Pass: ${aaaPass ? '✓' : '✗'}`);
}

// ============================================================================
// 6. Palette Generation
// ============================================================================

console.log('\n--- 6. Palette Generation ---\n');

const primary = '#2ECC71';

console.log('Base:', primary);

console.log('\nGradient (5 steps to darker):');
const gradientPalette = gradient(primary, darken(primary, 50), 5);
console.log(' ', gradientPalette.join(' '));

console.log('\nMonochromatic (5 steps):');
console.log(' ', monochromatic(primary, 5).join(' '));

console.log('\nShades (5 steps):');
console.log(' ', shades(primary, 5).join(' '));

console.log('\nTints (5 steps):');
console.log(' ', tints(primary, 5).join(' '));

console.log('\nRandom Colors:');
console.log('  Random:', random());
console.log('  Pastel:', randomPastel());
console.log('  Vibrant:', randomVibrant());

// ============================================================================
// 7. Color Analysis
// ============================================================================

console.log('\n--- 7. Color Analysis ---\n');

const testColors = ['#FFFFFF', '#000000', '#FF0000', '#00FF00', '#0000FF', '#808080'];

console.log('Luminance & Lightness:');
for (const color of testColors) {
  const lum = getLuminance(color);
  const light = isLight(color);
  console.log(`  ${color}: luminance=${lum.toFixed(3)}, isLight=${light}`);
}

console.log('\nColor Distance:');
const colorPairs = [
  ['#FF0000', '#FF0000'],
  ['#FF0000', '#FF0101'],
  ['#FF0000', '#FF4444'],
  ['#FF0000', '#00FF00'],
  ['#FF0000', '#0000FF'],
];

for (const [c1, c2] of colorPairs) {
  const rgbDist = rgbDistance(c1, c2);
  const deltaE = deltaE2000(c1, c2);
  console.log(`  ${c1} ↔ ${c2}: RGB=${rgbDist.toFixed(1)}, ΔE=${deltaE.toFixed(2)}`);
}

console.log('\nClosest Named Colors:');
const findNames = ['#FF5733', '#3498DB', '#E74C3C', '#27AE60', '#9B59B6'];
for (const color of findNames) {
  const name = closestNamedColor(color);
  console.log(`  ${color} → ${name}`);
}

// ============================================================================
// 8. Complete Color Info
// ============================================================================

console.log('\n--- 8. Complete Color Info ---\n');

const detailedColor = '#3498DB';
const info = getColorInfo(detailedColor);

if (info) {
  console.log(`Detailed info for ${detailedColor}:`);
  console.log('  HEX:', info.hex);
  console.log('  RGB:', `rgb(${info.rgb.r}, ${info.rgb.g}, ${info.rgb.b})`);
  console.log('  HSL:', `hsl(${info.hsl.h}, ${info.hsl.s}%, ${info.hsl.l}%)`);
  console.log('  HSV:', `hsv(${info.hsv.h}, ${info.hsv.s}%, ${info.hsv.v}%)`);
  console.log('  Alpha:', info.alpha);
  console.log('  Name:', info.name);
  console.log('  Luminance:', info.luminance.toFixed(3));
  console.log('  Is Light:', info.isLight);
}

// ============================================================================
// 9. Format Conversion
// ============================================================================

console.log('\n--- 9. Format Conversion ---\n');

const colorToConvert = '#2ECC71';

console.log(`Convert ${colorToConvert}:`);
console.log('  HEX:', toString(colorToConvert, 'hex'));
console.log('  RGB:', toString(colorToConvert, 'rgb'));
console.log('  HSL:', toString(colorToConvert, 'hsl'));
console.log('  HSV:', toString(colorToConvert, 'hsv'));

// ============================================================================
// 10. Color Modification
// ============================================================================

console.log('\n--- 10. Color Modification ---\n');

const baseColor2 = '#E74C3C';

console.log(`Modify ${baseColor2}:`);
console.log('  Change hue to 180°:', modify(baseColor2, { hue: 180 }));
console.log('  Change saturation to 50%:', modify(baseColor2, { saturation: 50 }));
console.log('  Change lightness to 70%:', modify(baseColor2, { lightness: 70 }));
console.log('  Set alpha to 0.5:', modify(baseColor2, { alpha: 0.5 }));
console.log('  Multiple changes:', modify(baseColor2, { hue: 200, saturation: 80, lightness: 60 }));

// ============================================================================
// 11. Color Validation
// ============================================================================

console.log('\n--- 11. Color Validation ---\n');

const testInputs = [
  '#FF5733',
  '#F53',
  'rgb(255, 87, 51)',
  'rgba(255, 87, 51, 0.5)',
  'hsl(10, 100%, 60%)',
  'red',
  'not a color',
  'FFFFFF',
];

console.log('Color Validation:');
for (const input of testInputs) {
  const valid = isValidColor(input);
  console.log(`  ${input.padEnd(30)} ${valid ? '✓' : '✗'}`);
}

// ============================================================================
// 12. Color Equality
// ============================================================================

console.log('\n--- 12. Color Equality ---\n');

const equalityTests = [
  ['#FF0000', '#FF0000'],
  ['#FF0000', 'red'],
  ['#FF0000', 'rgb(255, 0, 0)'],
  ['#FF0000', '#FF000080'],
  ['#FF0000', '#00FF00'],
];

console.log('Color Equality:');
for (const [c1, c2] of equalityTests) {
  console.log(`  ${c1} === ${c2}: ${equals(c1, c2)}`);
}

// ============================================================================
// 13. Practical Use Cases
// ============================================================================

console.log('\n--- 13. Practical Use Cases ---\n');

// Generate a button color scheme
const buttonBase = '#3498DB';
console.log('Button Color Scheme:');
console.log('  Normal:', buttonBase);
console.log('  Hover:', lighten(buttonBase, 10));
console.log('  Active:', darken(buttonBase, 10));
console.log('  Disabled:', grayscale(buttonBase));

// Generate accessible text color
const background = '#2C3E50';
const textColor = isLight(background) ? '#000000' : '#FFFFFF';
console.log('\nText on', background, ':', textColor);
console.log('Contrast ratio:', getContrastRatio(background, textColor).toFixed(2), ':1');

// Generate theme colors
const themeBase = '#9B59B6';
console.log('\nTheme Generation:');
console.log('  Primary:', themeBase);
console.log('  Secondary:', complement(themeBase));
console.log('  Accent:', adjustHue(themeBase, 30));
console.log('  Background:', darken(themeBase, 40));
console.log('  Surface:', darken(themeBase, 30));

console.log('\n' + '='.repeat(60));
console.log('Examples completed!');
console.log('='.repeat(60));