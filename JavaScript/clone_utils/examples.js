/**
 * Clone Utils Examples
 * 
 * 深度克隆、比较、合并工具示例
 */

const {
  shallowClone,
  deepClone,
  deepCompare,
  deepMerge,
  cloneJSON,
  cloneWithCustomizer,
  isDeepEqual,
  structuralClone,
  clonePick,
  cloneOmit
} = require('./mod.js');

console.log('=== Clone Utils Examples ===\n');

// ==================== 1. 浅克隆 ====================
console.log('1. Shallow Clone:');
const original = { a: 1, b: { c: 2 } };
const shallow = shallowClone(original);
shallow.a = 99;
shallow.b.c = 100;
console.log('Original:', original); // { a: 1, b: { c: 100 } } - b.c 被修改了
console.log('Shallow:', shallow);    // { a: 99, b: { c: 100 } }

// ==================== 2. 深克隆 ====================
console.log('\n2. Deep Clone:');
const nested = { 
  user: { name: 'Alice', settings: { theme: 'dark' } },
  items: [1, 2, 3]
};
const deep = deepClone(nested);
deep.user.settings.theme = 'light';
deep.items.push(4);
console.log('Original nested:', nested);      // theme 仍然是 'dark', items 仍然是 [1,2,3]
console.log('Deep cloned:', deep);            // theme 是 'light', items 是 [1,2,3,4]

// ==================== 3. 循环引用 ====================
console.log('\n3. Circular Reference:');
const circular = { name: 'node' };
circular.self = circular;
const clonedCircular = deepClone(circular);
console.log('Circular cloned:', clonedCircular);
console.log('Self reference preserved:', clonedCircular.self === clonedCircular); // true

// ==================== 4. 特殊类型克隆 ====================
console.log('\n4. Special Types:');
const special = {
  date: new Date('2024-01-01'),
  regex: /test/gi,
  map: new Map([['key', 'value']]),
  set: new Set([1, 2, 3]),
  buffer: new Uint8Array([1, 2, 3])
};
const specialCloned = deepClone(special);
console.log('Date cloned:', specialCloned.date.toISOString());
console.log('Regex cloned:', specialCloned.regex.test('TEST')); // true (case insensitive)
console.log('Map cloned:', specialCloned.map.get('key'));
console.log('Set cloned:', specialCloned.set.has(2));

// ==================== 5. 深度比较 ====================
console.log('\n5. Deep Compare:');
const obj1 = { a: 1, b: { c: [1, 2, 3] } };
const obj2 = { a: 1, b: { c: [1, 2, 3] } };
const obj3 = { a: 1, b: { c: [1, 2, 4] } };

const result1 = deepCompare(obj1, obj2);
console.log('obj1 vs obj2:', result1.equal); // true

const result2 = deepCompare(obj1, obj3);
console.log('obj1 vs obj3:', result2.equal); // false
console.log('Differences:', result2.differences);

// ==================== 6. 深度合并 ====================
console.log('\n6. Deep Merge:');
const defaults = {
  api: { host: 'localhost', port: 3000 },
  features: { auth: true, cache: false }
};
const userConfig = {
  api: { port: 8080 },
  features: { cache: true }
};
const merged = deepMerge(defaults, userConfig);
console.log('Merged config:', JSON.stringify(merged, null, 2));
// { api: { host: 'localhost', port: 8080 }, features: { auth: true, cache: true } }

// ==================== 7. JSON 安全克隆 ====================
console.log('\n7. JSON Clone:');
const jsonSafe = { a: 1, b: 'hello' };
const jsonCloned = cloneJSON(jsonSafe);
console.log('JSON cloned:', jsonCloned);

// 注意：JSON 克隆的限制
const withUndefined = { a: 1, b: undefined };
console.log('Original with undefined:', withUndefined);
console.log('JSON cloned (undefined lost):', cloneJSON(withUndefined));

// ==================== 8. 自定义克隆器 ====================
console.log('\n8. Custom Cloner:');
const withDate = { created: new Date(), name: 'test' };
const customCloned = cloneWithCustomizer(withDate, {
  date: (d) => d.toISOString()
});
console.log('Custom cloned:', customCloned);
console.log('Date converted to ISO string:', customCloned.created);

// ==================== 9. 选择性克隆 ====================
console.log('\n9. Pick and Omit:');
const user = { id: 1, name: 'Alice', email: 'alice@example.com', password: 'secret' };

// 只克隆指定字段
const publicUser = clonePick(user, ['id', 'name', 'email']);
console.log('Picked (public user):', publicUser);

// 排除敏感字段
const safeUser = cloneOmit(user, ['password']);
console.log('Omitted (safe user):', safeUser);

// ==================== 10. 深度相等判断 ====================
console.log('\n10. Deep Equality:');
console.log('Equal objects:', isDeepEqual({ a: 1 }, { a: 1 })); // true
console.log('Different nested:', isDeepEqual({ a: { b: 1 } }, { a: { b: 2 } })); // false
console.log('Arrays:', isDeepEqual([1, 2, 3], [1, 2, 3])); // true
console.log('Different types:', isDeepEqual({ a: 1 }, [1])); // false

// ==================== 11. 结构化克隆 ====================
console.log('\n11. Structural Clone:');
const structObj = { 
  num: 42, 
  str: 'hello', 
  arr: [1, 2, 3],
  date: new Date()
};
const structCloned = structuralClone(structObj);
console.log('Structural clone:', structCloned);
console.log('Date preserved:', structCloned.date instanceof Date);

// ==================== 12. 实际应用场景 ====================
console.log('\n12. Practical Use Cases:');

// 场景1：状态快照
console.log('\n--- State Snapshot ---');
const state = { count: 0, items: [] };
const snapshot = deepClone(state);
state.count = 1;
state.items.push('new item');
console.log('Current state:', state);
console.log('Snapshot:', snapshot);

// 场景2：配置默认值合并
console.log('\n--- Config Merge ---');
const defaultSettings = {
  theme: 'light',
  notifications: { email: true, push: false },
  privacy: { public: true }
};
const userSettings = {
  theme: 'dark',
  notifications: { push: true }
};
const finalSettings = deepMerge(defaultSettings, userSettings);
console.log('Final settings:', JSON.stringify(finalSettings, null, 2));

// 场景3：检测变更
console.log('\n--- Change Detection ---');
const before = { a: 1, b: { c: 2 }, d: 3 };
const after = { a: 1, b: { c: 99 }, d: 3 };
const diff = deepCompare(before, after);
if (!diff.equal) {
  console.log('Changes detected:');
  diff.differences.forEach(d => {
    console.log(`  ${d.path}: ${d.valueA} -> ${d.valueB}`);
  });
}

// 场景4：安全地移除敏感数据
console.log('\n--- Safe Data Transfer ---');
const userData = {
  id: 1,
  name: 'Alice',
  email: 'alice@example.com',
  password: 'secret123',
  token: 'abc123xyz',
  creditCard: '1234-5678-9012-3456'
};
const publicData = cloneOmit(userData, ['password', 'token', 'creditCard']);
console.log('Public data (safe for API response):', publicData);

console.log('\n=== Examples Complete ===');