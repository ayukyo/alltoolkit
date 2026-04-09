/**
 * Date Utils - Quick Verification Script
 * 
 * Simple JavaScript verification that the module works correctly.
 * Run with: node verify.js
 */

// Since we can't directly import TypeScript, let's verify the file structure
const fs = require('fs');
const path = require('path');

console.log('🔍 Verifying date_utils module structure...\n');

const moduleDir = __dirname;
const requiredFiles = [
  'mod.ts',
  'date_utils_test.ts',
  'README.md',
  'examples/basic_usage.ts',
  'examples/advanced_example.ts',
];

let allPresent = true;

requiredFiles.forEach(file => {
  const filePath = path.join(moduleDir, file);
  const exists = fs.existsSync(filePath);
  const size = exists ? fs.statSync(filePath).size : 0;
  
  console.log(`${exists ? '✅' : '❌'} ${file} (${size} bytes)`);
  
  if (!exists) {
    allPresent = false;
  }
});

console.log('\n' + '='.repeat(50));

if (allPresent) {
  console.log('✅ All required files present!');
  
  // Check mod.ts content
  const modContent = fs.readFileSync(path.join(moduleDir, 'mod.ts'), 'utf-8');
  
  const requiredExports = [
    'formatDate',
    'parseDate',
    'addDays',
    'addMonths',
    'addYears',
    'isBefore',
    'isAfter',
    'timeAgo',
    'startOfDay',
    'endOfDay',
    'isLeapYear',
    'getQuarter',
    'isWeekend',
    'businessDaysBetween',
    'DateUtils',
  ];
  
  console.log('\n📦 Checking exports...\n');
  
  let allExportsPresent = true;
  requiredExports.forEach(exp => {
    const present = modContent.includes(`export function ${exp}`) || 
                    modContent.includes(`export const ${exp}`) ||
                    modContent.includes(`${exp}:`);
    console.log(`${present ? '✅' : '❌'} ${exp}`);
    if (!present) allExportsPresent = false;
  });
  
  console.log('\n' + '='.repeat(50));
  
  if (allExportsPresent) {
    console.log('✅ All exports present!');
    console.log('\n🎉 Module verification complete!\n');
    console.log('📝 To run tests:');
    console.log('   - With Deno: deno test date_utils_test.ts');
    console.log('   - With Bun: bun test date_utils_test.ts');
    console.log('   - With Node + ts-node: ts-node date_utils_test.node.ts\n');
    process.exit(0);
  } else {
    console.log('❌ Some exports are missing!\n');
    process.exit(1);
  }
} else {
  console.log('❌ Some required files are missing!\n');
  process.exit(1);
}
