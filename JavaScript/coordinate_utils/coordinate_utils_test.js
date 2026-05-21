/**
 * Coordinate Utilities Test Suite
 * JavaScript 地理坐标工具模块测试
 */

const CoordinateUtils = require('./mod.js');

// 测试工具函数
function assert(condition, message) {
  if (!condition) {
    throw new Error(`Assertion failed: ${message}`);
  }
}

function assertEqual(actual, expected, message) {
  if (actual !== expected) {
    throw new Error(`${message}\nExpected: ${expected}\nActual: ${actual}`);
  }
}

function assertAlmostEqual(actual, expected, tolerance, message) {
  if (Math.abs(actual - expected) > tolerance) {
    throw new Error(`${message}\nExpected: ${expected} (±${tolerance})\nActual: ${actual}`);
  }
}

function assertValidPoint(point, message) {
  if (!CoordinateUtils.isValid(point.lat, point.lng)) {
    throw new Error(`${message}\nInvalid point: lat=${point.lat}, lng=${point.lng}`);
  }
}

let passed = 0;
let failed = 0;

function test(name, fn) {
  try {
    fn();
    console.log(`✓ ${name}`);
    passed++;
  } catch (e) {
    console.error(`✗ ${name}`);
    console.error(`  ${e.message}`);
    failed++;
  }
}

console.log('Running CoordinateUtils tests...\n');

// ==================== 基础验证测试 ====================
test('isValid - 有效坐标', () => {
  assert(CoordinateUtils.isValid(40.7128, -74.0060), '纽约坐标应该有效');
  assert(CoordinateUtils.isValid(0, 0), '零坐标应该有效');
  assert(CoordinateUtils.isValid(-90, -180), '边界坐标应该有效');
  assert(CoordinateUtils.isValid(90, 180), '边界坐标应该有效');
});

test('isValid - 无效坐标', () => {
  assert(!CoordinateUtils.isValid(91, 0), '超出纬度范围应该无效');
  assert(!CoordinateUtils.isValid(-91, 0), '低于纬度范围应该无效');
  assert(!CoordinateUtils.isValid(0, 181), '超出经度范围应该无效');
  assert(!CoordinateUtils.isValid(0, -181), '低于经度范围应该无效');
  assert(!CoordinateUtils.isValid('40', -74), '字符串类型应该无效');
  assert(!CoordinateUtils.isValid(null, null), 'null 应该无效');
});

// ==================== 角度弧度转换测试 ====================
test('toRadians - 角度转弧度', () => {
  assertAlmostEqual(CoordinateUtils.toRadians(0), 0, 0.001, '0度应该是0弧度');
  assertAlmostEqual(CoordinateUtils.toRadians(180), Math.PI, 0.001, '180度应该是π弧度');
  assertAlmostEqual(CoordinateUtils.toRadians(90), Math.PI / 2, 0.001, '90度应该是π/2弧度');
});

test('toDegrees - 弧度转角度', () => {
  assertAlmostEqual(CoordinateUtils.toDegrees(0), 0, 0.001, '0弧度应该是0度');
  assertAlmostEqual(CoordinateUtils.toDegrees(Math.PI), 180, 0.001, 'π弧度应该是180度');
  assertAlmostEqual(CoordinateUtils.toDegrees(Math.PI / 2), 90, 0.001, 'π/2弧度应该是90度');
});

// ==================== 经纬度规范化测试 ====================
test('normalizeLongitude - 经度规范化', () => {
  assertAlmostEqual(CoordinateUtils.normalizeLongitude(190), -170, 0.001, '190应该规范化为-170');
  assertAlmostEqual(CoordinateUtils.normalizeLongitude(-190), 170, 0.001, '-190应该规范化为170');
  assertAlmostEqual(CoordinateUtils.normalizeLongitude(360), 0, 0.001, '360应该规范化为0');
});

test('normalizeLatitude - 纬度规范化', () => {
  assertAlmostEqual(CoordinateUtils.normalizeLatitude(100), 80, 0.001, '100应该规范化为80');
  assertAlmostEqual(CoordinateUtils.normalizeLatitude(-100), -80, 0.001, '-100应该规范化为-80');
});

// ==================== 距离计算测试 ====================
test('distance - 基本距离计算', () => {
  const ny = { lat: 40.7128, lng: -74.0060 };
  const la = { lat: 34.0522, lng: -118.2437 };
  
  // 纽约到洛杉矶约 3940 km
  const dist = CoordinateUtils.distance(ny, la, 'km');
  assertAlmostEqual(dist, 3940, 50, `纽约到洛杉矶距离应该约3940km，实际是${dist}km`);
});

test('distance - 不同单位', () => {
  const ny = { lat: 40.7128, lng: -74.0060 };
  const la = { lat: 34.0522, lng: -118.2437 };
  
  const distKm = CoordinateUtils.distance(ny, la, 'km');
  const distMi = CoordinateUtils.distance(ny, la, 'mi');
  
  // 1 km ≈ 0.621371 mi
  assertAlmostEqual(distMi, distKm * 0.621371, 30, '公里和英里转换应该正确');
});

test('distance - 同一点距离为零', () => {
  const point = { lat: 40.7128, lng: -74.0060 };
  const dist = CoordinateUtils.distance(point, point);
  assertAlmostEqual(dist, 0, 0.001, '同一点距离应该为0');
});

test('distance - 南北距离', () => {
  // 从赤道到北极点
  const equator = { lat: 0, lng: 0 };
  const northPole = { lat: 90, lng: 0 };
  
  const dist = CoordinateUtils.distance(equator, northPole, 'km');
  // 地球半径约 6371 km，四分之一周长约 10000 km
  assertAlmostEqual(dist, 10000, 100, `赤道到北极距离应该约10000km`);
});

test('distance - 东西距离', () => {
  // 赤道上的东西距离
  const east = { lat: 0, lng: 0 };
  const west = { lat: 0, lng: 90 };
  
  const dist = CoordinateUtils.distance(east, west, 'km');
  // 赤道上的90度经度差约 10000 km
  assertAlmostEqual(dist, 10000, 100, `赤道90度经度差距离应该约10000km`);
});

// ==================== 总距离测试 ====================
test('totalDistance - 多点总距离', () => {
  const points = [
    { lat: 0, lng: 0 },
    { lat: 0, lng: 90 },
    { lat: 0, lng: 180 }
  ];
  
  const total = CoordinateUtils.totalDistance(points, 'km');
  // 应该是约 20000 km
  assertAlmostEqual(total, 20000, 200, `总距离应该约20000km`);
});

// ==================== 方位角测试 ====================
test('bearing - 方位角计算', () => {
  const ny = { lat: 40.7128, lng: -74.0060 };
  const la = { lat: 34.0522, lng: -118.2437 };
  
  const bearing = CoordinateUtils.bearing(ny, la);
  // 纽约到洛杉矶约 274 度（西偏南）
  assertAlmostEqual(bearing, 274, 5, `方位角应该约274度，实际是${bearing}度`);
});

test('bearing - 正北方位角', () => {
  const south = { lat: 0, lng: 0 };
  const north = { lat: 10, lng: 0 };
  
  const bearing = CoordinateUtils.bearing(south, north);
  assertAlmostEqual(bearing, 0, 1, '正北方位角应该是0度');
});

test('reverseBearing - 反方位角', () => {
  const ny = { lat: 40.7128, lng: -74.0060 };
  const la = { lat: 34.0522, lng: -118.2437 };
  
  const bearing = CoordinateUtils.bearing(ny, la);
  const reverse = CoordinateUtils.reverseBearing(ny, la);
  
  assertAlmostEqual(reverse, (bearing + 180) % 360, 1, '反方位角应该相差180度');
});

// ==================== 目标点计算测试 ====================
test('destination - 计算目标点', () => {
  const start = { lat: 40.7128, lng: -74.0060 };
  
  // 向北100km
  const dest = CoordinateUtils.destination(start, 0, 100, 'km');
  
  // 纬度应该增加约0.9度
  assertAlmostEqual(dest.lat, 40.7128 + 0.9, 0.1, '向北100km纬度应该增加约0.9度');
  assertAlmostEqual(dest.lng, -74.0060, 0.01, '向北经度应该基本不变');
});

test('destination - 向东目标点', () => {
  const start = { lat: 0, lng: 0 };
  
  // 向东100km（赤道）
  const dest = CoordinateUtils.destination(start, 90, 100, 'km');
  
  // 经度应该增加约0.9度
  assertAlmostEqual(dest.lng, 0.9, 0.1, '向东100km经度应该增加约0.9度');
  assertAlmostEqual(dest.lat, 0, 0.01, '向东纬度应该基本不变');
});

// ==================== 中点计算测试 ====================
test('midpoint - 两点中点', () => {
  const p1 = { lat: 0, lng: 0 };
  const p2 = { lat: 10, lng: 0 };
  
  const mid = CoordinateUtils.midpoint(p1, p2);
  
  assertAlmostEqual(mid.lat, 5, 0.1, '中点纬度应该是5');
  assertAlmostEqual(mid.lng, 0, 0.1, '中点经度应该是0');
});

test('midpoint - 跨越180度经线', () => {
  const p1 = { lat: 0, lng: 170 };
  const p2 = { lat: 0, lng: -170 };
  
  const mid = CoordinateUtils.midpoint(p1, p2);
  
  // 中点应该在180度或-180度
  assert(Math.abs(mid.lng) > 175, '跨越180度的中点经度应该接近180或-180');
});

// ==================== 中心点计算测试 ====================
test('center - 多点中心', () => {
  const points = [
    { lat: 0, lng: 0 },
    { lat: 10, lng: 10 },
    { lat: 20, lng: 20 }
  ];
  
  const center = CoordinateUtils.center(points);
  
  assertAlmostEqual(center.lat, 10, 1, '中心纬度应该约10');
  assertAlmostEqual(center.lng, 10, 1, '中心经度应该约10');
});

// ==================== 边界框测试 ====================
test('boundingBox - 计算边界框', () => {
  const points = [
    { lat: 10, lng: 10 },
    { lat: 20, lng: 20 },
    { lat: 5, lng: 5 },
    { lat: 30, lng: 30 }
  ];
  
  const bbox = CoordinateUtils.boundingBox(points);
  
  assertEqual(bbox.minLat, 5, '最小纬度应该是5');
  assertEqual(bbox.maxLat, 30, '最大纬度应该是30');
  assertEqual(bbox.minLng, 5, '最小经度应该是5');
  assertEqual(bbox.maxLng, 30, '最大经度应该是30');
});

test('isInBoundingBox - 点在边界框内', () => {
  const bbox = { minLat: 0, maxLat: 20, minLng: 0, maxLng: 20 };
  const inside = { lat: 10, lng: 10 };
  const outside = { lat: 30, lng: 10 };
  
  assert(CoordinateUtils.isInBoundingBox(inside, bbox), '点应该在边界框内');
  assert(!CoordinateUtils.isInBoundingBox(outside, bbox), '点不应该在边界框内');
});

test('boundingBoxFromRadius - 从半径计算边界框', () => {
  const center = { lat: 40, lng: -74 };
  const bbox = CoordinateUtils.boundingBoxFromRadius(center, 10, 'km');
  
  // 边界框应该包含中心点
  assert(CoordinateUtils.isInBoundingBox(center, bbox), '中心点应该在边界框内');
  
  // 边界框大小应该合理
  const latDiff = bbox.maxLat - bbox.minLat;
  const lngDiff = bbox.maxLng - bbox.minLng;
  
  assert(latDiff > 0, '纬度差应该大于0');
  assert(lngDiff > 0, '经度差应该大于0');
});

// ==================== 最近点查找测试 ====================
test('findNearest - 查找最近点', () => {
  const target = { lat: 0, lng: 0 };
  const points = [
    { lat: 10, lng: 10 },
    { lat: 1, lng: 1 },
    { lat: 5, lng: 5 }
  ];
  
  const nearest = CoordinateUtils.findNearest(target, points, 'km');
  
  assertEqual(nearest.index, 1, '最近点索引应该是1');
  assertAlmostEqual(nearest.distance, 157, 20, '最近距离应该约157km');
});

test('findWithinRadius - 查找半径内点', () => {
  const center = { lat: 0, lng: 0 };
  const points = [
    { lat: 0, lng: 1 },    // 约111km
    { lat: 0, lng: 2 },    // 约222km
    { lat: 10, lng: 10 },  // 约1565km
  ];
  
  const within = CoordinateUtils.findWithinRadius(center, 250, points, 'km');
  
  assertEqual(within.length, 2, '应该有2个点在250km半径内');
});

// ==================== 度分秒转换测试 ====================
test('dmsToDecimal - 度分秒转十进制', () => {
  const decimal = CoordinateUtils.dmsToDecimal(40, 26, 46, 'N');
  assertAlmostEqual(decimal, 40.446, 0.001, '度分秒转换应该正确');
});

test('dmsToDecimal - 西/南方向', () => {
  const west = CoordinateUtils.dmsToDecimal(79, 58, 56, 'W');
  assertAlmostEqual(west, -79.982, 0.001, '西方应该是负数');
  
  const south = CoordinateUtils.dmsToDecimal(40, 26, 46, 'S');
  assertAlmostEqual(south, -40.446, 0.001, '南方应该是负数');
});

test('decimalToDms - 十进制转度分秒', () => {
  const dms = CoordinateUtils.decimalToDms(40.446, 'lat');
  
  assertEqual(dms.degrees, 40, '度应该是40');
  assertEqual(dms.minutes, 26, '分应该是26');
  assertAlmostEqual(dms.seconds, 46, 1, '秒应该约46');
  assertEqual(dms.direction, 'N', '方向应该是N');
});

test('formatDms - 格式化度分秒', () => {
  const dms = { degrees: 40, minutes: 26, seconds: 46, direction: 'N' };
  const formatted = CoordinateUtils.formatDms(dms);
  
  assert(formatted.includes('40°'), '格式化应该包含度');
  assert(formatted.includes("26'"), '格式化应该包含分');
  // 秒会被格式化为 46.00（带精度）
  assert(formatted.includes('46') && formatted.includes('"'), '格式化应该包含秒');
  assert(formatted.includes('N'), '格式化应该包含方向');
});

// ==================== 坐标解析测试 ====================
test('parseCoordinate - 解析十进制', () => {
  const result = CoordinateUtils.parseCoordinate('40.446');
  assertAlmostEqual(result, 40.446, 0.001, '应该解析为十进制');
});

test('parseCoordinate - 解析度分秒', () => {
  const result = CoordinateUtils.parseCoordinate("40°26'46\"N");
  assertAlmostEqual(result, 40.446, 0.001, '应该解析度分秒格式');
});

test('parseCoordinate - 解析度分', () => {
  const result = CoordinateUtils.parseCoordinate("40°26.5'N");
  assertAlmostEqual(result, 40.442, 0.001, '应该解析度分格式');
});

test('parseCoordinatePair - 解析坐标对', () => {
  const result = CoordinateUtils.parseCoordinatePair('40.446, -79.982');
  
  assertAlmostEqual(result.lat, 40.446, 0.001, '纬度应该正确');
  assertAlmostEqual(result.lng, -79.982, 0.001, '经度应该正确');
});

// ==================== 格式化测试 ====================
test('format - 十进制格式化', () => {
  const point = { lat: 40.7128, lng: -74.0060 };
  const formatted = CoordinateUtils.format(point);
  
  assert(formatted.includes('40.7128'), '应该包含纬度');
  assert(formatted.includes('-74.0060'), '应该包含经度');
});

test('format - 度分秒格式化', () => {
  const point = { lat: 40.7128, lng: -74.0060 };
  const formatted = CoordinateUtils.format(point, { format: 'dms' });
  
  assert(formatted.includes('°'), '应该包含度符号');
  assert(formatted.includes("'"), '应该包含分符号');
});

// ==================== 多边形测试 ====================
test('polygonArea - 计算多边形面积', () => {
  // 简单三角形
  const triangle = [
    { lat: 0, lng: 0 },
    { lat: 1, lng: 0 },
    { lat: 0, lng: 1 }
  ];
  
  const area = CoordinateUtils.polygonArea(triangle, 'km2');
  assert(area > 0, '面积应该大于0');
  // 约 6000 km²（粗略）
  assertAlmostEqual(area, 6000, 1000, '三角形面积应该约6000km²');
});

test('polygonPerimeter - 计算多边形周长', () => {
  const square = [
    { lat: 0, lng: 0 },
    { lat: 1, lng: 0 },
    { lat: 1, lng: 1 },
    { lat: 0, lng: 1 }
  ];
  
  const perimeter = CoordinateUtils.polygonPerimeter(square, 'km');
  // 每边约111km，总周长约444km
  assertAlmostEqual(perimeter, 444, 50, '周长应该约444km');
});

test('isPointInPolygon - 点在多边形内', () => {
  const polygon = [
    { lat: 0, lng: 0 },
    { lat: 10, lng: 0 },
    { lat: 10, lng: 10 },
    { lat: 0, lng: 10 }
  ];
  
  const inside = { lat: 5, lng: 5 };
  const outside = { lat: 15, lng: 5 };
  
  assert(CoordinateUtils.isPointInPolygon(inside, polygon), '点应该在多边形内');
  assert(!CoordinateUtils.isPointInPolygon(outside, polygon), '点不应该在多边形内');
});

test('polygonsIntersect - 多边形相交', () => {
  const poly1 = [
    { lat: 0, lng: 0 },
    { lat: 10, lng: 0 },
    { lat: 10, lng: 10 },
    { lat: 0, lng: 10 }
  ];
  
  const poly2 = [
    { lat: 5, lng: 5 },
    { lat: 15, lng: 5 },
    { lat: 15, lng: 15 },
    { lat: 5, lng: 15 }
  ];
  
  const poly3 = [
    { lat: 20, lng: 20 },
    { lat: 30, lng: 20 },
    { lat: 30, lng: 30 },
    { lat: 20, lng: 30 }
  ];
  
  assert(CoordinateUtils.polygonsIntersect(poly1, poly2), '相邻多边形应该相交');
  assert(!CoordinateUtils.polygonsIntersect(poly1, poly3), '远离的多边形不应该相交');
});

// ==================== 路径插值测试 ====================
test('interpolatePath - 路径插值', () => {
  const path = [
    { lat: 0, lng: 0 },
    { lat: 0, lng: 2 }
  ];
  
  const interpolated = CoordinateUtils.interpolatePath(path, 50, 'km');
  
  // 应该在约222km的路径上插入约4个点
  assert(interpolated.length >= 5, '应该插入多个点');
});

// ==================== 随机坐标测试 ====================
test('randomPoint - 生成随机点', () => {
  const point = CoordinateUtils.randomPoint();
  assertValidPoint(point, '随机点应该有效');
});

test('randomPoint - 边界内随机点', () => {
  const bounds = { minLat: 0, maxLat: 10, minLng: 0, maxLng: 10 };
  const point = CoordinateUtils.randomPoint(bounds);
  
  assert(point.lat >= 0 && point.lat <= 10, '纬度应该在边界内');
  assert(point.lng >= 0 && point.lng <= 10, '经度应该在边界内');
});

test('randomPoints - 生成多个随机点', () => {
  const points = CoordinateUtils.randomPoints(10);
  assertEqual(points.length, 10, '应该生成10个点');
  
  for (const point of points) {
    assertValidPoint(point, '所有点应该有效');
  }
});

// ==================== 网格点测试 ====================
test('gridPoints - 生成网格点', () => {
  const bounds = { minLat: 0, maxLat: 10, minLng: 0, maxLng: 10 };
  const grid = CoordinateUtils.gridPoints(bounds, 3, 3);
  
  assertEqual(grid.length, 9, '应该生成9个网格点');
  assertEqual(grid[0].row, 0, '第一个点row应该是0');
  assertEqual(grid[0].col, 0, '第一个点col应该是0');
});

// ==================== 坐标偏移测试 ====================
test('offsetByMeters - 米偏移', () => {
  const point = { lat: 40.7128, lng: -74.0060 };
  const offset = CoordinateUtils.offsetByMeters(point, 1000, 1000);
  
  // 向北向东各1000米
  assert(offset.lat > point.lat, '纬度应该增加');
  assert(offset.lng > point.lng, '经度应该增加');
});

// ==================== 方向测试 ====================
test('getDirection - 方向计算', () => {
  const ny = { lat: 40.7128, lng: -74.0060 };
  const north = { lat: 50, lng: -74.0060 };
  
  const direction = CoordinateUtils.getDirection(ny, north);
  assert(direction.direction === 'North', '方向应该是North');
  assertAlmostEqual(direction.bearing, 0, 5, '方位角应该约0度');
});

// ==================== Vincenty距离测试 ====================
test('vincentyDistance - 精确距离', () => {
  const ny = { lat: 40.7128, lng: -74.0060 };
  const la = { lat: 34.0522, lng: -118.2437 };
  
  const haversine = CoordinateUtils.distance(ny, la, 'km');
  const vincenty = CoordinateUtils.vincentyDistance(ny, la, 'km');
  
  // Vincenty应该更精确，但差异应该小于1%
  const diff = Math.abs(haversine - vincenty) / haversine;
  assert(diff < 0.01, `Vincenty和Haversine差异应该小于1%，实际是${diff * 100}%`);
});

// ==================== 相似度测试 ====================
test('similarity - 坐标相似度', () => {
  const p1 = { lat: 40.7128, lng: -74.0060 };
  const p2 = { lat: 40.7130, lng: -74.0062 };  // 非常接近
  const p3 = { lat: 50, lng: -80 };  // 较远
  
  const sim1 = CoordinateUtils.similarity(p1, p2, 10, 'km');
  const sim2 = CoordinateUtils.similarity(p1, p3, 10, 'km');
  
  assert(sim1 > 0, '接近的点相似度应该大于0');
  assertAlmostEqual(sim2, 0, 0.001, '远的点相似度应该为0');
});

// ==================== 距离排序测试 ====================
test('sortByDistance - 按距离排序', () => {
  const origin = { lat: 0, lng: 0 };
  const points = [
    { lat: 10, lng: 10 },
    { lat: 1, lng: 1 },
    { lat: 5, lng: 5 }
  ];
  
  const sorted = CoordinateUtils.sortByDistance(origin, points, 'km', 'asc');
  
  assertEqual(sorted.length, 3, '应该有3个结果');
  assert(sorted[0].distance < sorted[1].distance, '应该升序排列');
  assertAlmostEqual(sorted[0].point.lat, 1, 0.1, '最近的点纬度应该是1');
});

// ==================== 矩形创建测试 ====================
test('createRectangle - 创建矩形', () => {
  const center = { lat: 40, lng: -74 };
  const rect = CoordinateUtils.createRectangle(center, 10, 10, 'km');
  
  assertEqual(rect.length, 4, '矩形应该有4个顶点');
  
  for (const point of rect) {
    assertValidPoint(point, '矩形顶点应该有效');
  }
});

// ==================== 圆形创建测试 ====================
test('createCircle - 创建圆形', () => {
  const center = { lat: 40, lng: -74 };
  const circle = CoordinateUtils.createCircle(center, 5, 12, 'km');
  
  assertEqual(circle.length, 12, '应该有12个点');
  
  // 每个点距离中心应该相同
  for (const point of circle) {
    const dist = CoordinateUtils.distance(center, point, 'km');
    assertAlmostEqual(dist, 5, 0.1, '圆形点距离中心应该约5km');
  }
});

// ==================== 扇形创建测试 ====================
test('createSector - 创建扇形', () => {
  const center = { lat: 40, lng: -74 };
  const sector = CoordinateUtils.createSector(center, 5, 0, 90, 8, 'km');
  
  // 扇形应该包含中心点和边界点
  assert(sector.length >= 10, '扇形应该有足够的点');
  
  // 第一个点应该是中心
  assertAlmostEqual(sector[0].lat, center.lat, 0.001, '扇形起点应该是中心');
  assertAlmostEqual(sector[0].lng, center.lng, 0.001, '扇形起点应该是中心');
});

// ==================== 边界条件测试 ====================
test('边界条件 - 空数组', () => {
  assertEqual(CoordinateUtils.totalDistance([]), 0, '空数组总距离应该是0');
  // 使用 isNaN 检查而不是 assertEqual（因为 NaN !== NaN）
  assert(Number.isNaN(CoordinateUtils.center([]).lat), '空数组中心应该无效');
  assert(Number.isNaN(CoordinateUtils.boundingBox([]).minLat), '空数组边界框应该无效');
});

test('边界条件 - 单点', () => {
  const point = { lat: 40, lng: -74 };
  
  assertAlmostEqual(CoordinateUtils.totalDistance([point]), 0, 0.001, '单点总距离应该是0');
  assertAlmostEqual(CoordinateUtils.center([point]).lat, point.lat, 0.001, '单点中心应该是该点');
});

// 输出测试结果
console.log(`\n========================================`);
console.log(`Results: ${passed} passed, ${failed} failed`);
console.log(`========================================`);

process.exit(failed > 0 ? 1 : 0);