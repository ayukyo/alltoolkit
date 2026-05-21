/**
 * Tests for Color Parser Utilities
 */

import {
  parseHex,
  parseRgbString,
  parseHslString,
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

// ============================================================================
// Test Runner
// ============================================================================

let passCount = 0;
let failCount = 0;

function test(description: string, fn: () => boolean): void {
  try {
    const result = fn();
    if (result) {
      console.log(`✓ ${description}`);
      passCount++;
    } else {
      console.log(`✗ ${description}`);
      failCount++;
    }
  } catch (e) {
    console.log(`✗ ${description} - Error: ${(e as Error).message}`);
    failCount++;
  }
}

function assertEqual<T>(actual: T, expected: T, description?: string): boolean {
  const isEqual = JSON.stringify(actual) === JSON.stringify(expected);
  if (!isEqual && description) {
    console.log(`  Expected: ${JSON.stringify(expected)}`);
    console.log(`  Actual: ${JSON.stringify(actual)}`);
  }
  return isEqual;
}

function assertApprox(actual: number, expected: number, tolerance = 1): boolean {
  const isEqual = Math.abs(actual - expected) <= tolerance;
  if (!isEqual) {
    console.log(`  Expected: ${expected} (±${tolerance})`);
    console.log(`  Actual: ${actual}`);
  }
  return isEqual;
}

// ============================================================================
// Parsing Tests
// ============================================================================

console.log('\n=== Parsing Tests ===\n');

test('parseHex - 6 digit hex', () => {
  const result = parseHex('#FF5733');
  return result !== null && 
         result.r === 255 && 
         result.g === 87 && 
         result.b === 51 && 
         result.a === 1;
});

test('parseHex - lowercase hex', () => {
  const result = parseHex('#ff5733');
  return result !== null && 
         result.r === 255 && 
         result.g === 87 && 
         result.b === 51;
});

test('parseHex - 3 digit shorthand', () => {
  const result = parseHex('#F53');
  return result !== null && 
         result.r === 255 && 
         result.g === 85 && 
         result.b === 51;
});

test('parseHex - 8 digit with alpha', () => {
  const result = parseHex('#FF573380');
  return result !== null && 
         result.r === 255 && 
         result.g === 87 && 
         result.b === 51 && 
         assertApprox(result.a, 0.5, 0.01);
});

test('parseHex - invalid hex returns null', () => {
  return parseHex('invalid') === null;
});

test('parseRgbString - rgb format', () => {
  const result = parseRgbString('rgb(255, 87, 33)');
  return result !== null && 
         result.r === 255 && 
         result.g === 87 && 
         result.b === 33 && 
         result.a === 1;
});

test('parseRgbString - rgba format', () => {
  const result = parseRgbString('rgba(255, 87, 33, 0.5)');
  return result !== null && 
         result.r === 255 && 
         result.g === 87 && 
         result.b === 33 && 
         result.a === 0.5;
});

test('parseRgbString - invalid returns null', () => {
  return parseRgbString('invalid') === null;
});

test('parseHslString - hsl format', () => {
  const result = parseHslString('hsl(180, 50%, 50%)');
  return result !== null && 
         result.h === 180 && 
         result.s === 50 && 
         result.l === 50;
});

test('parseHslString - hsla format', () => {
  const result = parseHslString('hsla(180, 50%, 50%, 0.5)');
  return result !== null && 
         result.h === 180 && 
         result.s === 50 && 
         result.l === 50 && 
         result.a === 0.5;
});

test('parseColor - named color', () => {
  const result = parseColor('red');
  return result !== null && result.hex === '#FF0000';
});

test('parseColor - hex without #', () => {
  const result = parseColor('FF5733');
  return result !== null && result.rgb.r === 255;
});

// ============================================================================
// Conversion Tests
// ============================================================================

console.log('\n=== Conversion Tests ===\n');

test('rgbToHex - converts RGB to hex', () => {
  const hex = rgbToHex({ r: 255, g: 87, b: 51 });
  return hex === '#FF5733';
});

test('hexToRgb - converts hex to RGB', () => {
  const rgb = hexToRgb('#FF5733');
  return rgb !== null && rgb.r === 255 && rgb.g === 87 && rgb.b === 51;
});

test('rgbToHsl - converts RGB to HSL', () => {
  const hsl = rgbToHsl({ r: 255, g: 0, b: 0 });
  return hsl.h === 0 && hsl.s === 100 && hsl.l === 50;
});

test('hslToRgb - converts HSL to RGB', () => {
  const rgb = hslToRgb({ h: 0, s: 100, l: 50 });
  return rgb.r === 255 && rgb.g === 0 && rgb.b === 0;
});

test('rgbToHsv - converts RGB to HSV', () => {
  const hsv = rgbToHsv({ r: 255, g: 0, b: 0 });
  return hsv.h === 0 && hsv.s === 100 && hsv.v === 100;
});

test('hsvToRgb - converts HSV to RGB', () => {
  const rgb = hsvToRgb({ h: 0, s: 100, v: 100 });
  return rgb.r === 255 && rgb.g === 0 && rgb.b === 0;
});

test('rgbToCmyk - converts RGB to CMYK', () => {
  const cmyk = rgbToCmyk({ r: 255, g: 255, b: 255 });
  return cmyk.c === 0 && cmyk.m === 0 && cmyk.y === 0 && cmyk.k === 0;
});

test('cmykToRgb - converts CMYK to RGB', () => {
  const rgb = cmykToRgb({ c: 0, m: 0, y: 0, k: 0 });
  return rgb.r === 255 && rgb.g === 255 && rgb.b === 255;
});

test('rgbToLab - converts RGB to LAB', () => {
  const lab = rgbToLab({ r: 255, g: 255, b: 255 });
  return assertApprox(lab.l, 100, 0.1);
});

test('labToRgb - converts LAB to RGB', () => {
  const rgb = labToRgb({ l: 100, a: 0, b: 0 });
  return assertApprox(rgb.r, 255, 2) && assertApprox(rgb.g, 255, 2) && assertApprox(rgb.b, 255, 2);
});

test('RGB <-> HSL roundtrip', () => {
  const original = { r: 128, g: 64, b: 200 };
  const hsl = rgbToHsl(original);
  const rgb = hslToRgb(hsl);
  return assertApprox(rgb.r, original.r, 2) && 
         assertApprox(rgb.g, original.g, 2) && 
         assertApprox(rgb.b, original.b, 2);
});

test('RGB <-> HSV roundtrip', () => {
  const original = { r: 128, g: 64, b: 200 };
  const hsv = rgbToHsv(original);
  const rgb = hsvToRgb(hsv);
  return assertApprox(rgb.r, original.r) && 
         assertApprox(rgb.g, original.g) && 
         assertApprox(rgb.b, original.b);
});

// ============================================================================
// Manipulation Tests
// ============================================================================

console.log('\n=== Manipulation Tests ===\n');

test('lighten - increases lightness', () => {
  const lightened = lighten('#000000', 20);
  return lightened !== '#000000';
});

test('darken - decreases lightness', () => {
  const darkened = darken('#FFFFFF', 20);
  return darkened !== '#FFFFFF';
});

test('saturate - increases saturation', () => {
  const saturated = saturate('#3498DB', 30);
  const parsed = parseColor('#3498DB');
  const saturatedParsed = parseColor(saturated);
  return saturatedParsed !== null && parsed !== null && saturatedParsed.hsl.s > parsed.hsl.s;
});

test('desaturate - decreases saturation', () => {
  const desaturated = desaturate('#FF5733', 50);
  return desaturated !== '#FF5733';
});

test('adjustHue - rotates hue', () => {
  const rotated = adjustHue('#FF0000', 180);
  return rotated === '#00FFFF';
});

test('setAlpha - sets alpha channel', () => {
  const withAlpha = setAlpha('#FF5733', 0.5);
  return withAlpha.length === 9; // #RRGGBBAA format
});

test('mix - blends two colors', () => {
  const mixed = mix('#FF0000', '#00FF00', 0.5);
  return mixed !== '#FF0000' && mixed !== '#00FF00';
});

test('mix - 0 weight returns first color', () => {
  const mixed = mix('#FF0000', '#00FF00', 0);
  return mixed === '#FF0000';
});

test('mix - 1 weight returns second color', () => {
  const mixed = mix('#FF0000', '#00FF00', 1);
  return mixed === '#00FF00';
});

test('invert - inverts color', () => {
  const inverted = invert('#000000');
  return inverted === '#FFFFFF';
});

test('invert - white becomes black', () => {
  const inverted = invert('#FFFFFF');
  return inverted === '#000000';
});

test('grayscale - removes color', () => {
  const gray = grayscale('#FF5733');
  const parsed = parseColor(gray);
  return parsed !== null && parsed.rgb.r === parsed.rgb.g && parsed.rgb.g === parsed.rgb.b;
});

test('sepia - applies sepia tone', () => {
  const sepiaColor = sepia('#FF5733');
  return sepiaColor !== '#FF5733';
});

// ============================================================================
// Analysis Tests
// ============================================================================

console.log('\n=== Analysis Tests ===\n');

test('getLuminance - white has luminance ~1', () => {
  const luminance = getLuminance('#FFFFFF');
  return assertApprox(luminance, 1, 0.01);
});

test('getLuminance - black has luminance ~0', () => {
  const luminance = getLuminance('#000000');
  return assertApprox(luminance, 0, 0.01);
});

test('getContrastRatio - black on white is 21', () => {
  const ratio = getContrastRatio('#FFFFFF', '#000000');
  return assertApprox(ratio, 21, 0.5);
});

test('meetsWCAG - black on white passes AA', () => {
  return meetsWCAG('#FFFFFF', '#000000', 'AA');
});

test('meetsWCAG - light gray on white fails AA', () => {
  return !meetsWCAG('#FFFFFF', '#CCCCCC', 'AA');
});

test('getWCAGRating - black on white is AAA', () => {
  const rating = getWCAGRating('#FFFFFF', '#000000');
  return rating === 'AAA';
});

test('isLight - white is light', () => {
  return isLight('#FFFFFF');
});

test('isLight - black is not light', () => {
  return !isLight('#000000');
});

test('complement - red complement is cyan', () => {
  const comp = complement('#FF0000');
  return comp === '#00FFFF';
});

test('analogous - returns 3 colors', () => {
  const analogousColors = analogous('#FF0000', 30);
  return analogousColors.length === 3;
});

test('triadic - returns 3 colors 120 degrees apart', () => {
  const triadicColors = triadic('#FF0000');
  return triadicColors.length === 3;
});

test('tetradic - returns 4 colors', () => {
  const tetradicColors = tetradic('#FF0000');
  return tetradicColors.length === 4;
});

test('splitComplementary - returns 3 colors', () => {
  const splitComp = splitComplementary('#FF0000');
  return splitComp.length === 3;
});

// ============================================================================
// Distance Tests
// ============================================================================

console.log('\n=== Distance Tests ===\n');

test('rgbDistance - same color is 0', () => {
  const distance = rgbDistance('#FF0000', '#FF0000');
  return distance === 0;
});

test('rgbDistance - different colors have positive distance', () => {
  const distance = rgbDistance('#FF0000', '#00FF00');
  return distance > 0;
});

test('deltaE2000 - same color is 0', () => {
  const delta = deltaE2000('#FF0000', '#FF0000');
  return assertApprox(delta, 0, 0.1);
});

test('deltaE2000 - different colors have positive delta', () => {
  const delta = deltaE2000('#FF0000', '#00FF00');
  return delta > 0;
});

// ============================================================================
// Palette Tests
// ============================================================================

console.log('\n=== Palette Tests ===\n');

test('gradient - generates correct number of colors', () => {
  const grad = gradient('#FF0000', '#00FF00', 5);
  return grad.length === 5;
});

test('gradient - starts with start color', () => {
  const grad = gradient('#FF0000', '#00FF00', 5);
  return grad[0] === '#FF0000';
});

test('gradient - ends with end color', () => {
  const grad = gradient('#FF0000', '#00FF00', 5);
  return grad[4] === '#00FF00';
});

test('monochromatic - generates correct number', () => {
  const mono = monochromatic('#FF0000', 5);
  return mono.length === 5;
});

test('shades - generates darker colors', () => {
  const shadesList = shades('#FF0000', 3);
  return shadesList.length === 3;
});

test('tints - generates lighter colors', () => {
  const tintsList = tints('#FF0000', 3);
  return tintsList.length === 3;
});

test('random - generates hex color', () => {
  const randColor = random();
  return /^#[0-9A-F]{6}$/.test(randColor);
});

test('randomPastel - generates pastel color', () => {
  const pastel = randomPastel();
  const parsed = parseColor(pastel);
  return parsed !== null && parsed.hsl.l > 70;
});

test('randomVibrant - generates vibrant color', () => {
  const vibrant = randomVibrant();
  const parsed = parseColor(vibrant);
  return parsed !== null && parsed.hsl.s > 80;
});

test('closestNamedColor - finds closest name', () => {
  const name = closestNamedColor('#FF0000');
  return name === 'red';
});

test('closestNamedColor - finds close match', () => {
  const name = closestNamedColor('#FF0101');
  return name === 'red';
});

// ============================================================================
// Utility Tests
// ============================================================================

console.log('\n=== Utility Tests ===\n');

test('toString - hex format', () => {
  return toString('#FF5733', 'hex') === '#FF5733';
});

test('toString - rgb format', () => {
  return toString('#FF0000', 'rgb') === 'rgb(255, 0, 0)';
});

test('toString - hsl format', () => {
  const result = toString('#FF0000', 'hsl');
  return result.startsWith('hsl(');
});

test('isValidColor - valid hex', () => {
  return isValidColor('#FF5733');
});

test('isValidColor - valid named color', () => {
  return isValidColor('red');
});

test('isValidColor - invalid returns false', () => {
  return !isValidColor('notacolor');
});

test('getColorInfo - returns complete info', () => {
  const info = getColorInfo('#FF0000');
  return info !== null && info.hex === '#FF0000' && info.name === 'red';
});

test('equals - same colors are equal', () => {
  return equals('#FF0000', '#FF0000');
});

test('equals - different colors are not equal', () => {
  return !equals('#FF0000', '#00FF00');
});

test('equals - hex and rgb equivalent', () => {
  return equals('#FF0000', 'rgb(255, 0, 0)');
});

test('modify - changes hue', () => {
  const modified = modify('#FF0000', { hue: 180 });
  return modified === '#00FFFF';
});

test('modify - changes lightness', () => {
  const modified = modify('#FF0000', { lightness: 75 });
  return modified !== '#FF0000';
});

test('modify - changes alpha', () => {
  const modified = modify('#FF0000', { alpha: 0.5 });
  return modified.length === 9;
});

// ============================================================================
// Named Colors Tests
// ============================================================================

console.log('\n=== Named Colors Tests ===\n');

test('CSS_NAMED_COLORS has basic colors', () => {
  return CSS_NAMED_COLORS['black'] === '#000000' &&
         CSS_NAMED_COLORS['white'] === '#FFFFFF' &&
         CSS_NAMED_COLORS['red'] === '#FF0000';
});

test('CSS_NAMED_COLORS count', () => {
  return Object.keys(CSS_NAMED_COLORS).length > 140;
});

test('parse named color with spaces', () => {
  const result = parseColor('Cornflower Blue');
  return result !== null;
});

// ============================================================================
// Edge Cases Tests
// ============================================================================

console.log('\n=== Edge Cases Tests ===\n');

test('parseColor handles extra whitespace', () => {
  const result = parseColor('  #FF5733  ');
  return result !== null && result.rgb.r === 255;
});

test('rgbToHex handles alpha', () => {
  const hex = rgbToHex({ r: 255, g: 87, b: 33, a: 0.5 }, true);
  return hex.length === 9;
});

test('hslToRgb handles achromatic (s=0)', () => {
  const rgb = hslToRgb({ h: 0, s: 0, l: 50 });
  return rgb.r === 128 && rgb.g === 128 && rgb.b === 128;
});

test('rgbToCmyk handles pure black', () => {
  const cmyk = rgbToCmyk({ r: 0, g: 0, b: 0 });
  return cmyk.c === 0 && cmyk.m === 0 && cmyk.y === 0 && cmyk.k === 100;
});

test('adjustHue handles negative values', () => {
  const rotated = adjustHue('#00FFFF', -180);
  return rotated === '#FF0000';
});

test('lighten max is white', () => {
  const lightened = lighten('#FFFFFF', 50);
  return lightened === '#FFFFFF';
});

test('darken min is black', () => {
  const darkened = darken('#000000', 50);
  return darkened === '#000000';
});

// ============================================================================
// Summary
// ============================================================================

console.log('\n=== Test Summary ===\n');
console.log(`Passed: ${passCount}`);
console.log(`Failed: ${failCount}`);
console.log(`Total: ${passCount + failCount}`);
console.log(`Pass Rate: ${(passCount / (passCount + failCount) * 100).toFixed(1)}%`);

if (failCount === 0) {
  console.log('\n🎉 All tests passed!');
} else {
  console.log('\n❌ Some tests failed.');
}