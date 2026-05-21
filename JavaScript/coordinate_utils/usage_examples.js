/**
 * Coordinate Utilities - 使用示例
 * JavaScript 地理坐标工具模块
 */

const CoordinateUtils = require('./mod.js');

console.log('=== Coordinate Utilities 使用示例 ===\n');

// ==================== 1. 基础验证 ====================
console.log('1. 基础验证');
console.log('-------------------');

const isValid = CoordinateUtils.isValid(40.7128, -74.0060);
console.log(`坐标 (40.7128, -74.0060) 是否有效: ${isValid}`);

const invalid = CoordinateUtils.isValid(91, 0);
console.log(`坐标 (91, 0) 是否有效: ${invalid}`);

console.log('\n');

// ==================== 2. 距离计算 ====================
console.log('2. 距离计算');
console.log('-------------------');

const newYork = { lat: 40.7128, lng: -74.0060 };
const losAngeles = { lat: 34.0522, lng: -118.2437 };
const london = { lat: 51.5074, lng: -0.1278 };

const distNYtoLA = CoordinateUtils.distance(newYork, losAngeles, 'km');
console.log(`纽约到洛杉矶距离: ${distNYtoLA.toFixed(2)} km`);

const distNYtoLondon = CoordinateUtils.distance(newYork, london, 'km');
console.log(`纽约到伦敦距离: ${distNYtoLondon.toFixed(2)} km`);

const distInMiles = CoordinateUtils.distance(newYork, losAngeles, 'mi');
console.log(`纽约到洛杉矶距离: ${distInMiles.toFixed(2)} 英里`);

console.log('\n');

// ==================== 3. 方位角计算 ====================
console.log('3. 方位角计算');
console.log('-------------------');

const bearing = CoordinateUtils.bearing(newYork, losAngeles);
console.log(`纽约到洛杉矶的方位角: ${bearing.toFixed(2)}°`);

const direction = CoordinateUtils.getDirection(newYork, losAngeles);
console.log(`方向: ${direction.direction} (${direction.abbreviation}), 方位角: ${direction.bearing.toFixed(2)}°`);

console.log('\n');

// ==================== 4. 目标点计算 ====================
console.log('4. 目标点计算');
console.log('-------------------');

// 从纽约向北100km
const northPoint = CoordinateUtils.destination(newYork, 0, 100, 'km');
console.log(`从纽约向北100km: (${northPoint.lat.toFixed(4)}, ${northPoint.lng.toFixed(4)})`);

// 从纽约向东50km
const eastPoint = CoordinateUtils.destination(newYork, 90, 50, 'km');
console.log(`从纽约向东50km: (${eastPoint.lat.toFixed(4)}, ${eastPoint.lng.toFixed(4)})`);

console.log('\n');

// ==================== 5. 中点计算 ====================
console.log('5. 中点计算');
console.log('-------------------');

const midpoint = CoordinateUtils.midpoint(newYork, losAngeles);
console.log(`纽约和洛杉矶的中点: (${midpoint.lat.toFixed(4)}, ${midpoint.lng.toFixed(4)})`);

const formatMid = CoordinateUtils.format(midpoint);
console.log(`格式化中点: ${formatMid}`);

console.log('\n');

// ==================== 6. 边界框计算 ====================
console.log('6. 边界框计算');
console.log('-------------------');

const cities = [
  newYork,
  losAngeles,
  { lat: 41.8781, lng: -87.6298 }, // Chicago
  { lat: 29.7604, lng: -95.3698 }  // Houston
];

const bbox = CoordinateUtils.boundingBox(cities);
console.log('美国四城市边界框:');
console.log(`  最小纬度: ${bbox.minLat.toFixed(4)}°`);
console.log(`  最大纬度: ${bbox.maxLat.toFixed(4)}°`);
console.log(`  最小经度: ${bbox.minLng.toFixed(4)}°`);
console.log(`  最大经度: ${bbox.maxLng.toFixed(4)}°`);

const bboxCenter = CoordinateUtils.boundingBoxCenter(bbox);
console.log(`边界框中心: (${bboxCenter.lat.toFixed(4)}, ${bboxCenter.lng.toFixed(4)})`);

console.log('\n');

// ==================== 7. 度分秒转换 ====================
console.log('7. 度分秒转换');
console.log('-------------------');

// 度分秒转十进制
const decimal = CoordinateUtils.dmsToDecimal(40, 26, 46, 'N');
console.log(`40°26'46"N = ${decimal.toFixed(6)}°`);

// 十进制转度分秒
const dms = CoordinateUtils.decimalToDms(40.446, 'lat');
console.log(`40.446° = ${CoordinateUtils.formatDms(dms)}`);

// 解析坐标字符串
const parsed = CoordinateUtils.parseCoordinate("40°26'46\"N");
console.log(`解析 "40°26'46"N": ${parsed.toFixed(6)}°`);

console.log('\n');

// ==================== 8. 查找最近点 ====================
console.log('8. 查找最近点');
console.log('-------------------');

const target = { lat: 41.0, lng: -75.0 };
const nearby = CoordinateUtils.findNearest(target, cities, 'km');
console.log(`离 (41.0, -75.0) 最近的城市索引: ${nearby.index}`);
console.log(`距离: ${nearby.distance.toFixed(2)} km`);

// 查找半径内的点
const withinRadius = CoordinateUtils.findWithinRadius(newYork, 500, cities, 'km');
console.log(`纽约500km半径内的城市: ${withinRadius.length}个`);
withinRadius.forEach(item => {
  console.log(`  距离 ${item.distance.toFixed(2)} km`);
});

console.log('\n');

// ==================== 9. 多边形操作 ====================
console.log('9. 多边形操作');
console.log('-------------------');

const triangle = [
  { lat: 40.0, lng: -74.0 },
  { lat: 40.5, lng: -74.0 },
  { lat: 40.25, lng: -73.5 }
];

const area = CoordinateUtils.polygonArea(triangle, 'km2');
console.log(`三角形面积: ${area.toFixed(2)} km²`);

const perimeter = CoordinateUtils.polygonPerimeter(triangle, 'km');
console.log(`三角形周长: ${perimeter.toFixed(2)} km`);

// 检查点是否在多边形内
const insidePoint = { lat: 40.25, lng: -73.75 };
const isInside = CoordinateUtils.isPointInPolygon(insidePoint, triangle);
console.log(`点 (40.25, -73.75) 是否在三角形内: ${isInside}`);

console.log('\n');

// ==================== 10. 创建几何形状 ====================
console.log('10. 创建几何形状');
console.log('-------------------');

// 创建圆形
const circle = CoordinateUtils.createCircle(newYork, 5, 12, 'km');
console.log(`以纽约为中心5km的圆形: ${circle.length}个点`);
circle.forEach((p, i) => {
  console.log(`  点${i + 1}: (${p.lat.toFixed(4)}, ${p.lng.toFixed(4)})`);
});

// 创建矩形
const rectangle = CoordinateUtils.createRectangle({ lat: 40, lng: -74 }, 10, 10, 'km');
console.log(`中心在(40, -74)的10x10km矩形: ${rectangle.length}个顶点`);

console.log('\n');

// ==================== 11. Vincenty精确距离 ====================
console.log('11. Vincenty精确距离');
console.log('-------------------');

const haversineDist = CoordinateUtils.distance(newYork, london, 'km');
const vincentyDist = CoordinateUtils.vincentyDistance(newYork, london, 'km');
console.log(`纽约到伦敦 Haversine距离: ${haversineDist.toFixed(4)} km`);
console.log(`纽约到伦敦 Vincenty距离: ${vincentyDist.toFixed(4)} km`);
console.log(`差异: ${(vincentyDist - haversineDist).toFixed(4)} km`);

console.log('\n');

// ==================== 12. 坐标格式化 ====================
console.log('12. 坐标格式化');
console.log('-------------------');

// 十进制格式
console.log(`十进制格式: ${CoordinateUtils.format(newYork, { precision: 4 })}`);

// 度分秒格式
console.log(`度分秒格式: ${CoordinateUtils.format(newYork, { format: 'dms' })}`);

// 不同分隔符
console.log(`自定义分隔符: ${CoordinateUtils.format(newYork, { separator: ' | ', precision: 2 })}`);

console.log('\n');

// ==================== 13. 网格点生成 ====================
console.log('13. 网格点生成');
console.log('-------------------');

const gridBounds = { minLat: 40, maxLat: 41, minLng: -74, maxLng: -73 };
const grid = CoordinateUtils.gridPoints(gridBounds, 3, 3);
console.log(`3x3网格点 (${grid.length}个点):`);
grid.forEach(p => {
  console.log(`  (${p.lat.toFixed(2)}, ${p.lng.toFixed(2)}) - row=${p.row}, col=${p.col}`);
});

console.log('\n');

// ==================== 14. 坐标排序 ====================
console.log('14. 坐标排序');
console.log('-------------------');

const sortedCities = CoordinateUtils.sortByDistance(newYork, cities, 'km', 'asc');
console.log('按距离纽约排序的城市:');
sortedCities.forEach((item, i) => {
  console.log(`  ${i + 1}. 距离 ${item.distance.toFixed(2)} km`);
});

console.log('\n=== 示例完成 ===\n');