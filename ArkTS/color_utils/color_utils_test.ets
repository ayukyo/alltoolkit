/**
 * Color Utils Test Suite for ArkTS/HarmonyOS
 */

import { Color, ColorUtils, BlendMode } from './mod';

class TestRunner {
  private passed = 0;
  private failed = 0;

  assertEqual(actual: any, expected: any, message: string): void {
    if (actual === expected) {
      this.passed++;
      console.info(`[PASS] ${message}`);
    } else {
      this.failed++;
      console.error(`[FAIL] ${message}`);
      console.error(`       Expected: ${expected}, Actual: ${actual}`);
    }
  }

  assertTrue(value: boolean, message: string): void {
    this.assertEqual(value, true, message);
  }

  assertFalse(value: boolean, message: string): void {
    this.assertEqual(value, false, message);
  }

  assertNotNull(value: any, message: string): void {
    if (value !== null) {
      this.passed++;
      console.info(`[PASS] ${message}`);
    } else {
      this.failed++;
      console.error(`[FAIL] ${message}`);
    }
  }

  assertNull(value: any, message: string): void {
    if (value === null) {
      this.passed++;
      console.info(`[PASS] ${message}`);
    } else {
      this.failed++;
      console.error(`[FAIL] ${message}`);
    }
  }

  summary(): void {
    console.info(`\n========== Test Summary ==========`);
    console.info(`Passed: ${this.passed}`);
    console.info(`Failed: ${this.failed}`);
    console.info(`Total:  ${this.passed + this.failed}`);
    console.info(this.failed === 0 ? 'All tests passed!' : `${this.failed} test(s) failed!`);
  }
}

export function runTests(): void {
  const test = new TestRunner();

  console.info('=== Color Class Tests ===');

  // Constructor tests
  const color = new Color(255, 128, 64);
  test.assertEqual(color.r, 255, 'Constructor sets red correctly');
  test.assertEqual(color.g, 128, 'Constructor sets green correctly');
  test.assertEqual(color.b, 64, 'Constructor sets blue correctly');
  test.assertEqual(color.a, 1, 'Constructor defaults alpha to 1');

  // Clamp tests
  const clampedColor = new Color(300, -50, 128, 2);
  test.assertEqual(clampedColor.r, 255, 'Red is clamped to max 255');
  test.assertEqual(clampedColor.g, 0, 'Green is clamped to min 0');
  test.assertEqual(clampedColor.a, 1, 'Alpha is clamped to max 1');

  // HEX conversion tests
  const red = new Color(255, 0, 0);
  test.assertEqual(red.toHex(), '#ff0000', 'Red converts to #ff0000');
  test.assertEqual(new Color(0, 255, 0).toHex(), '#00ff00', 'Green converts to #00ff00');
  test.assertEqual(new Color(0, 0, 255).toHex(), '#0000ff', 'Blue converts to #0000ff');

  // RGB conversion tests
  test.assertEqual(red.toRgb(), 'rgb(255, 0, 0)', 'Red toRgb works');
  test.assertEqual(new Color(255, 128, 64, 0.5).toRgb(), 'rgba(255, 128, 64, 0.5)', 'RGBA toRgb works');

  // Lightness tests
  test.assertTrue(new Color(50, 50, 50).isDark(), 'Dark color is detected as dark');
  test.assertTrue(new Color(200, 200, 200).isLight(), 'Light color is detected as light');

  // Parse HEX tests
  const parsed1 = ColorUtils.parseHex('#ff0000');
  test.assertNotNull(parsed1, 'Parses #ff0000');
  if (parsed1) {
    test.assertEqual(parsed1.r, 255, 'Parsed red is 255');
    test.assertEqual(parsed1.g, 0, 'Parsed green is 0');
    test.assertEqual(parsed1.b, 0, 'Parsed blue is 0');
  }

  const parsed2 = ColorUtils.parseHex('00ff00');
  test.assertNotNull(parsed2, 'Parses 00ff00 without #');

  const parsed3 = ColorUtils.parseHex('#f00');
  test.assertNotNull(parsed3, 'Parses short HEX #f00');

  const invalidHex = ColorUtils.parseHex('invalid');
  test.assertNull(invalidHex, 'Invalid HEX returns null');

  // Parse RGB tests
  const parsedRgb = ColorUtils.parseRgb('rgb(255, 128, 64)');
  test.assertNotNull(parsedRgb, 'Parses RGB string');

  // Validation tests
  test.assertTrue(ColorUtils.isValid('#ff0000'), 'Valid HEX is recognized');
  test.assertTrue(ColorUtils.isValid('rgb(255, 0, 0)'), 'Valid RGB is recognized');
  test.assertTrue(ColorUtils.isValid('red'), 'Named color is recognized');
  test.assertFalse(ColorUtils.isValid('invalid'), 'Invalid color is rejected');

  // HSL conversion tests
  const hslColor = red.toHsl();
  test.assertEqual(Math.round(hslColor.h), 0, 'Red HSL hue is 0');
  test.assertEqual(Math.round(hslColor.s), 100, 'Red HSL saturation is 100');
  test.assertEqual(Math.round(hslColor.l), 50, 'Red HSL lightness is 50');

  // Lighten/Darken tests
  const darkened = red.darken(20);
  test.assertTrue(darkened.toHsl().l < 50, 'Darkened color has lower lightness');
  const lightened = red.lighten(20);
  test.assertTrue(lightened.toHsl().l > 50, 'Lightened color has higher lightness');

  // Gradient tests
  const gradient = ColorUtils.gradient(red, new Color(0, 0, 255), 3);
  test.assertEqual(gradient.length, 3, 'Gradient has correct number of steps');

  // Contrast ratio tests
  const contrastRatio = ColorUtils.contrastRatio(new Color(0, 0, 0), new Color(255, 255, 255));
  test.assertEqual(Math.round(contrastRatio), 21, 'Black/White contrast ratio is 21');

  test.summary();
}

// Run tests if executed directly
runTests();
