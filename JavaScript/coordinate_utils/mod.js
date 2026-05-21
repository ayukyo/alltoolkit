/**
 * Coordinate Utilities - JavaScript 地理坐标工具模块
 * 
 * 提供地理坐标的转换、距离计算、格式化等功能
 * 零依赖，仅使用 JavaScript 标准库
 * 
 * @module coordinate_utils
 * @version 1.0.0
 */

const CoordinateUtils = {
  // 地球半径（千米）
  EARTH_RADIUS_KM: 6371,
  EARTH_RADIUS_M: 6371000,
  EARTH_RADIUS_MI: 3959,

  /**
   * 角度转弧度
   * @param {number} degrees - 角度值
   * @returns {number} - 弧度值
   */
  toRadians(degrees) {
    return degrees * (Math.PI / 180);
  },

  /**
   * 弧度转角度
   * @param {number} radians - 弧度值
   * @returns {number} - 角度值
   */
  toDegrees(radians) {
    return radians * (180 / Math.PI);
  },

  /**
   * 验证坐标是否有效
   * @param {number} lat - 纬度
   * @param {number} lng - 经度
   * @returns {boolean} - 是否有效
   */
  isValid(lat, lng) {
    return (
      typeof lat === 'number' && 
      typeof lng === 'number' &&
      lat >= -90 && lat <= 90 &&
      lng >= -180 && lng <= 180
    );
  },

  /**
   * 规范化经度到 -180 到 180 范围
   * @param {number} lng - 经度
   * @returns {number} - 规范化后的经度
   */
  normalizeLongitude(lng) {
    while (lng > 180) lng -= 360;
    while (lng < -180) lng += 360;
    return lng;
  },

  /**
   * 规范化纬度到 -90 到 90 范围
   * @param {number} lat - 纬度
   * @returns {number} - 规范化后的纬度
   */
  normalizeLatitude(lat) {
    if (lat > 90) return 90 - (lat - 90);
    if (lat < -90) return -90 - (lat + 90);
    return lat;
  },

  /**
   * 计算两点之间的距离（Haversine 公式）
   * @param {Object} point1 - 第一个点 { lat, lng }
   * @param {Object} point2 - 第二个点 { lat, lng }
   * @param {string} [unit='km'] - 单位 'km' | 'm' | 'mi' | 'ft'
   * @returns {number} - 距离
   */
  distance(point1, point2, unit = 'km') {
    if (!this.isValid(point1.lat, point1.lng) || !this.isValid(point2.lat, point2.lng)) {
      return NaN;
    }

    const lat1 = this.toRadians(point1.lat);
    const lat2 = this.toRadians(point2.lat);
    const deltaLat = this.toRadians(point2.lat - point1.lat);
    const deltaLng = this.toRadians(point2.lng - point1.lng);

    const a = Math.sin(deltaLat / 2) ** 2 +
              Math.cos(lat1) * Math.cos(lat2) * Math.sin(deltaLng / 2) ** 2;
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));

    const radius = this.getRadius(unit);
    return radius * c;
  },

  /**
   * 获取指定单位的地球半径
   * @param {string} unit - 单位
   * @returns {number} - 半径值
   */
  getRadius(unit) {
    const radii = {
      km: this.EARTH_RADIUS_KM,
      m: this.EARTH_RADIUS_M,
      mi: this.EARTH_RADIUS_MI,
      ft: this.EARTH_RADIUS_MI * 5280
    };
    return radii[unit] || radii.km;
  },

  /**
   * 计算多点之间的总距离
   * @param {Array} points - 点数组 [{ lat, lng }, ...]
   * @param {string} [unit='km'] - 单位
   * @returns {number} - 总距离
   */
  totalDistance(points, unit = 'km') {
    if (!Array.isArray(points) || points.length < 2) return 0;
    
    let total = 0;
    for (let i = 0; i < points.length - 1; i++) {
      total += this.distance(points[i], points[i + 1], unit);
    }
    return total;
  },

  /**
   * 计算两点之间的方位角（从北向东）
   * @param {Object} point1 - 起点 { lat, lng }
   * @param {Object} point2 - 终点 { lat, lng }
   * @returns {number} - 方位角（度数，0-360）
   */
  bearing(point1, point2) {
    if (!this.isValid(point1.lat, point1.lng) || !this.isValid(point2.lat, point2.lng)) {
      return NaN;
    }

    const lat1 = this.toRadians(point1.lat);
    const lat2 = this.toRadians(point2.lat);
    const deltaLng = this.toRadians(point2.lng - point1.lng);

    const y = Math.sin(deltaLng) * Math.cos(lat2);
    const x = Math.cos(lat1) * Math.sin(lat2) -
              Math.sin(lat1) * Math.cos(lat2) * Math.cos(deltaLng);

    let bearing = this.toDegrees(Math.atan2(y, x));
    return (bearing + 360) % 360;
  },

  /**
   * 计算反向方位角
   * @param {Object} point1 - 起点 { lat, lng }
   * @param {Object} point2 - 终点 { lat, lng }
   * @returns {number} - 反向方位角
   */
  reverseBearing(point1, point2) {
    const bearing = this.bearing(point1, point2);
    return (bearing + 180) % 360;
  },

  /**
   * 从起点按方位角和距离计算终点
   * @param {Object} start - 起点 { lat, lng }
   * @param {number} bearing - 方位角（度数）
   * @param {number} distance - 距离
   * @param {string} [unit='km'] - 单位
   * @returns {Object} - 终点 { lat, lng }
   */
  destination(start, bearing, distance, unit = 'km') {
    if (!this.isValid(start.lat, start.lng)) {
      return { lat: NaN, lng: NaN };
    }

    const radius = this.getRadius(unit);
    const distRad = distance / radius;
    const brngRad = this.toRadians(bearing);
    const lat1 = this.toRadians(start.lat);
    const lng1 = this.toRadians(start.lng);

    const lat2 = Math.asin(
      Math.sin(lat1) * Math.cos(distRad) +
      Math.cos(lat1) * Math.sin(distRad) * Math.cos(brngRad)
    );

    const lng2 = lng1 + Math.atan2(
      Math.sin(brngRad) * Math.sin(distRad) * Math.cos(lat1),
      Math.cos(distRad) - Math.sin(lat1) * Math.sin(lat2)
    );

    return {
      lat: this.toDegrees(lat2),
      lng: this.normalizeLongitude(this.toDegrees(lng2))
    };
  },

  /**
   * 计算两点之间的中点
   * @param {Object} point1 - 第一个点 { lat, lng }
   * @param {Object} point2 - 第二个点 { lat, lng }
   * @returns {Object} - 中点 { lat, lng }
   */
  midpoint(point1, point2) {
    if (!this.isValid(point1.lat, point1.lng) || !this.isValid(point2.lat, point2.lng)) {
      return { lat: NaN, lng: NaN };
    }

    const lat1 = this.toRadians(point1.lat);
    const lat2 = this.toRadians(point2.lat);
    const lng1 = this.toRadians(point1.lng);
    const lng2 = this.toRadians(point2.lng);

    const dLng = lng2 - lng1;

    const bx = Math.cos(lat2) * Math.cos(dLng);
    const by = Math.cos(lat2) * Math.sin(dLng);

    const lat3 = Math.atan2(
      Math.sin(lat1) + Math.sin(lat2),
      Math.sqrt((Math.cos(lat1) + bx) ** 2 + by ** 2)
    );

    const lng3 = lng1 + Math.atan2(by, Math.cos(lat1) + bx);

    return {
      lat: this.toDegrees(lat3),
      lng: this.normalizeLongitude(this.toDegrees(lng3))
    };
  },

  /**
   * 计算多点路径的中心点（平均坐标）
   * @param {Array} points - 点数组 [{ lat, lng }, ...]
   * @returns {Object} - 中心点 { lat, lng }
   */
  center(points) {
    if (!Array.isArray(points) || points.length === 0) {
      return { lat: NaN, lng: NaN };
    }

    // 转换为三维坐标计算
    let x = 0, y = 0, z = 0;
    
    for (const point of points) {
      if (!this.isValid(point.lat, point.lng)) continue;
      
      const latRad = this.toRadians(point.lat);
      const lngRad = this.toRadians(point.lng);
      
      x += Math.cos(latRad) * Math.cos(lngRad);
      y += Math.cos(latRad) * Math.sin(lngRad);
      z += Math.sin(latRad);
    }

    const count = points.filter(p => this.isValid(p.lat, p.lng)).length;
    if (count === 0) return { lat: NaN, lng: NaN };

    x /= count;
    y /= count;
    z /= count;

    const lng = Math.atan2(y, x);
    const hyp = Math.sqrt(x * x + y * y);
    const lat = Math.atan2(z, hyp);

    return {
      lat: this.toDegrees(lat),
      lng: this.normalizeLongitude(this.toDegrees(lng))
    };
  },

  /**
   * 计算边界框（最小外接矩形）
   * @param {Array} points - 点数组 [{ lat, lng }, ...]
   * @returns {Object} - 边界框 { minLat, maxLat, minLng, maxLng }
   */
  boundingBox(points) {
    if (!Array.isArray(points) || points.length === 0) {
      return { minLat: NaN, maxLat: NaN, minLng: NaN, maxLng: NaN };
    }

    const validPoints = points.filter(p => this.isValid(p.lat, p.lng));
    if (validPoints.length === 0) {
      return { minLat: NaN, maxLat: NaN, minLng: NaN, maxLng: NaN };
    }

    return {
      minLat: Math.min(...validPoints.map(p => p.lat)),
      maxLat: Math.max(...validPoints.map(p => p.lat)),
      minLng: Math.min(...validPoints.map(p => p.lng)),
      maxLng: Math.max(...validPoints.map(p => p.lng))
    };
  },

  /**
   * 检查点是否在边界框内
   * @param {Object} point - 点 { lat, lng }
   * @param {Object} bbox - 边界框 { minLat, maxLat, minLng, maxLng }
   * @returns {boolean} - 是否在边界框内
   */
  isInBoundingBox(point, bbox) {
    if (!this.isValid(point.lat, point.lng)) return false;
    
    return (
      point.lat >= bbox.minLat &&
      point.lat <= bbox.maxLat &&
      point.lng >= bbox.minLng &&
      point.lng <= bbox.maxLng
    );
  },

  /**
   * 计算边界框的中心
   * @param {Object} bbox - 边界框 { minLat, maxLat, minLng, maxLng }
   * @returns {Object} - 中心点 { lat, lng }
   */
  boundingBoxCenter(bbox) {
    return {
      lat: (bbox.minLat + bbox.maxLat) / 2,
      lng: (bbox.minLng + bbox.maxLng) / 2
    };
  },

  /**
   * 从中心点和半径计算边界框
   * @param {Object} center - 中心点 { lat, lng }
   * @param {number} radius - 半径
   * @param {string} [unit='km'] - 单位
   * @returns {Object} - 边界框 { minLat, maxLat, minLng, maxLng }
   */
  boundingBoxFromRadius(center, radius, unit = 'km') {
    if (!this.isValid(center.lat, center.lng)) {
      return { minLat: NaN, maxLat: NaN, minLng: NaN, maxLng: NaN };
    }

    const radiusKm = unit === 'km' ? radius : 
                     unit === 'm' ? radius / 1000 :
                     unit === 'mi' ? radius * 1.60934 :
                     radius / 1000;

    // 计算经纬度的角度变化
    const latChange = radiusKm / this.EARTH_RADIUS_KM * (180 / Math.PI);
    const lngChange = latChange / Math.cos(this.toRadians(center.lat));

    return {
      minLat: center.lat - latChange,
      maxLat: center.lat + latChange,
      minLng: center.lng - lngChange,
      maxLng: center.lng + lngChange
    };
  },

  /**
   * 找到最近的点
   * @param {Object} target - 目标点 { lat, lng }
   * @param {Array} points - 点数组 [{ lat, lng }, ...]
   * @param {string} [unit='km'] - 单位
   * @returns {Object} - { point: 最近点, distance: 距离, index: 索引 }
   */
  findNearest(target, points, unit = 'km') {
    if (!Array.isArray(points) || points.length === 0 || !this.isValid(target.lat, target.lng)) {
      return { point: null, distance: Infinity, index: -1 };
    }

    let minDist = Infinity;
    let nearest = null;
    let nearestIndex = -1;

    for (let i = 0; i < points.length; i++) {
      const point = points[i];
      if (!this.isValid(point.lat, point.lng)) continue;

      const dist = this.distance(target, point, unit);
      if (dist < minDist) {
        minDist = dist;
        nearest = point;
        nearestIndex = i;
      }
    }

    return { point: nearest, distance: minDist, index: nearestIndex };
  },

  /**
   * 找到指定半径内的所有点
   * @param {Object} center - 中心点 { lat, lng }
   * @param {number} radius - 半径
   * @param {Array} points - 点数组 [{ lat, lng }, ...]
   * @param {string} [unit='km'] - 单位
   * @returns {Array} - 符合条件的点数组，带距离信息
   */
  findWithinRadius(center, radius, points, unit = 'km') {
    if (!Array.isArray(points) || !this.isValid(center.lat, center.lng)) {
      return [];
    }

    return points
      .filter(p => this.isValid(p.lat, p.lng))
      .map(p => ({
        point: p,
        distance: this.distance(center, p, unit)
      }))
      .filter(item => item.distance <= radius)
      .sort((a, b) => a.distance - b.distance);
  },

  /**
   * 将度分秒格式转换为十进制
   * @param {number} degrees - 度
   * @param {number} minutes - 分
   * @param {number} seconds - 秒
   * @param {string} [direction='N'] - 方向 'N'|'S'|'E'|'W'
   * @returns {number} - 十进制坐标
   */
  dmsToDecimal(degrees, minutes, seconds, direction = 'N') {
    let decimal = degrees + minutes / 60 + seconds / 3600;
    
    if (direction === 'S' || direction === 'W') {
      decimal = -decimal;
    }
    
    return decimal;
  },

  /**
   * 将十进制坐标转换为度分秒格式
   * @param {number} decimal - 十进制坐标
   * @param {string} [type='lat'] - 类型 'lat'|'lng'
   * @returns {Object} - { degrees, minutes, seconds, direction }
   */
  decimalToDms(decimal, type = 'lat') {
    const absValue = Math.abs(decimal);
    const degrees = Math.floor(absValue);
    const minutesFloat = (absValue - degrees) * 60;
    const minutes = Math.floor(minutesFloat);
    const seconds = (minutesFloat - minutes) * 60;

    let direction;
    if (type === 'lat') {
      direction = decimal >= 0 ? 'N' : 'S';
    } else {
      direction = decimal >= 0 ? 'E' : 'W';
    }

    return { degrees, minutes, seconds, direction };
  },

  /**
   * 格式化度分秒为字符串
   * @param {Object} dms - { degrees, minutes, seconds, direction }
   * @param {number} [precision=2] - 秒的小数位数
   * @returns {string} - 格式化字符串
   */
  formatDms(dms, precision = 2) {
    const seconds = dms.seconds.toFixed(precision);
    return `${dms.degrees}°${dms.minutes}'${seconds}"${dms.direction}`;
  },

  /**
   * 将十进制坐标格式化为度分秒字符串
   * @param {number} decimal - 十进制坐标
   * @param {string} [type='lat'] - 类型
   * @param {number} [precision=2] - 秒的小数位数
   * @returns {string} - 格式化字符串
   */
  formatDecimalAsDms(decimal, type = 'lat', precision = 2) {
    const dms = this.decimalToDms(decimal, type);
    return this.formatDms(dms, precision);
  },

  /**
   * 解析坐标字符串为十进制
   * 支持多种格式：40°26'46"N, 40.446, -79.98, 40:26:46N
   * @param {string} str - 坐标字符串
   * @returns {number|null} - 十进制坐标或 null
   */
  parseCoordinate(str) {
    if (typeof str !== 'string') return null;
    
    // 清理字符串
    str = str.trim().replace(/\s+/g, '');
    
    // 检查是否包含度分秒特殊字符
    const hasDmsChars = /[°′'″":NSEW]/i.test(str);
    
    // 如果是纯数字字符串（可能带负号和小数），直接解析
    if (!hasDmsChars && /^-?\d+(?:\.\d+)?$/.test(str)) {
      return parseFloat(str);
    }

    // 匹配度分秒格式（支持单引号、双引号或无引号）
    // 格式：40°26'46"N 或 40°26'46N 或 40°26'46"N
    const dmsRegex = /^(\d+)°(\d+)'(\d+(?:\.\d+)?)[″"']?([NSEW])$/i;
    const match = str.match(dmsRegex);
    if (match) {
      return this.dmsToDecimal(
        parseInt(match[1]),
        parseInt(match[2]),
        parseFloat(match[3]),
        match[4].toUpperCase()
      );
    }

    // 匹配冒号分隔格式
    const colonRegex = /^(\d+):(\d+):(\d+(?:\.\d+)?)([NSEW])$/i;
    const colonMatch = str.match(colonRegex);
    if (colonMatch) {
      return this.dmsToDecimal(
        parseInt(colonMatch[1]),
        parseInt(colonMatch[2]),
        parseFloat(colonMatch[3]),
        colonMatch[4].toUpperCase()
      );
    }

    // 匹配度分格式
    const dmRegex = /^(\d+)°(\d+(?:\.\d+)?)[′'?]?([NSEW])$/i;
    const dmMatch = str.match(dmRegex);
    if (dmMatch) {
      return this.dmsToDecimal(
        parseInt(dmMatch[1]),
        parseFloat(dmMatch[2]),
        0,
        dmMatch[3].toUpperCase()
      );
    }

    return null;
  },

  /**
   * 解析坐标对字符串
   * @param {string} str - 坐标对字符串，如 "40.446, -79.98" 或 "40°26'46"N 79°58'56"W"
   * @returns {Object|null} - { lat, lng } 或 null
   */
  parseCoordinatePair(str) {
    if (typeof str !== 'string') return null;

    // 尝试逗号分隔的十进制格式
    const decimalRegex = /^(-?\d+(?:\.\d+)?),\s*(-?\d+(?:\.\d+)?)$/;
    const decimalMatch = str.match(decimalRegex);
    if (decimalMatch) {
      return {
        lat: parseFloat(decimalMatch[1]),
        lng: parseFloat(decimalMatch[2])
      };
    }

    // 尝试度分秒格式
    const parts = str.split(/\s+/);
    if (parts.length === 2) {
      const lat = this.parseCoordinate(parts[0]);
      const lng = this.parseCoordinate(parts[1]);
      if (lat !== null && lng !== null) {
        return { lat, lng };
      }
    }

    return null;
  },

  /**
   * 格式化坐标为字符串
   * @param {Object} point - { lat, lng }
   * @param {Object} [options] - 格式选项
   * @param {string} [options.format='decimal'] - 格式 'decimal' | 'dms'
   * @param {number} [options.precision=6] - 十进制精度
   * @param {string} [options.separator=', '] - 分隔符
   * @returns {string} - 格式化字符串
   */
  format(point, options = {}) {
    if (!this.isValid(point.lat, point.lng)) return 'Invalid coordinates';

    const opts = {
      format: 'decimal',
      precision: 6,
      separator: ', ',
      ...options
    };

    if (opts.format === 'dms') {
      const latDms = this.formatDecimalAsDms(point.lat, 'lat');
      const lngDms = this.formatDecimalAsDms(point.lng, 'lng');
      return `${latDms}${opts.separator}${lngDms}`;
    }

    const lat = point.lat.toFixed(opts.precision);
    const lng = point.lng.toFixed(opts.precision);
    return `${lat}${opts.separator}${lng}`;
  },

  /**
   * 计算两个多边形是否相交
   * @param {Array} poly1 - 多边形1 [{ lat, lng }, ...]
   * @param {Array} poly2 - 多边形2 [{ lat, lng }, ...]
   * @returns {boolean} - 是否相交
   */
  polygonsIntersect(poly1, poly2) {
    if (!Array.isArray(poly1) || !Array.isArray(poly2)) return false;
    if (poly1.length < 3 || poly2.length < 3) return false;

    // 简化检查：边界框相交
    const bbox1 = this.boundingBox(poly1);
    const bbox2 = this.boundingBox(poly2);

    return !(bbox1.maxLat < bbox2.minLat ||
             bbox1.minLat > bbox2.maxLat ||
             bbox1.maxLng < bbox2.minLng ||
             bbox1.minLng > bbox2.maxLng);
  },

  /**
   * 计算多边形面积（近似）
   * @param {Array} points - 多边形顶点 [{ lat, lng }, ...]
   * @param {string} [unit='km2'] - 单位 'km2' | 'm2' | 'mi2'
   * @returns {number} - 面积
   */
  polygonArea(points, unit = 'km2') {
    if (!Array.isArray(points) || points.length < 3) return 0;

    const validPoints = points.filter(p => this.isValid(p.lat, p.lng));
    if (validPoints.length < 3) return 0;

    // 使用 Shoelace 公式的球面近似
    let area = 0;
    const n = validPoints.length;

    for (let i = 0; i < n; i++) {
      const j = (i + 1) % n;
      const lat1 = this.toRadians(validPoints[i].lat);
      const lat2 = this.toRadians(validPoints[j].lat);
      const lng1 = this.toRadians(validPoints[i].lng);
      const lng2 = this.toRadians(validPoints[j].lng);

      area += (lng2 - lng1) * (2 + Math.sin(lat1) + Math.sin(lat2));
    }

    area = Math.abs(area * this.EARTH_RADIUS_KM ** 2 / 2);

    // 单位转换
    if (unit === 'm2') return area * 1000000;
    if (unit === 'mi2') return area * 0.386102;
    return area;
  },

  /**
   * 检查点是否在多边形内
   * @param {Object} point - 点 { lat, lng }
   * @param {Array} polygon - 多边形 [{ lat, lng }, ...]
   * @returns {boolean} - 是否在多边形内
   */
  isPointInPolygon(point, polygon) {
    if (!this.isValid(point.lat, point.lng) || !Array.isArray(polygon) || polygon.length < 3) {
      return false;
    }

    // 使用射线法
    const validPolygon = polygon.filter(p => this.isValid(p.lat, p.lng));
    const n = validPolygon.length;
    let inside = false;

    for (let i = 0, j = n - 1; i < n; j = i++) {
      const xi = validPolygon[i].lng;
      const yi = validPolygon[i].lat;
      const xj = validPolygon[j].lng;
      const yj = validPolygon[j].lat;

      if (((yi > point.lat) !== (yj > point.lat)) &&
          (point.lng < (xj - xi) * (point.lat - yi) / (yj - yi) + xi)) {
        inside = !inside;
      }
    }

    return inside;
  },

  /**
   * 计算多边形周长
   * @param {Array} points - 多边形顶点 [{ lat, lng }, ...]
   * @param {string} [unit='km'] - 单位
   * @returns {number} - 周长
   */
  polygonPerimeter(points, unit = 'km') {
    if (!Array.isArray(points) || points.length < 3) return 0;

    const validPoints = points.filter(p => this.isValid(p.lat, p.lng));
    if (validPoints.length < 3) return 0;

    let perimeter = 0;
    const n = validPoints.length;

    for (let i = 0; i < n; i++) {
      const j = (i + 1) % n;
      perimeter += this.distance(validPoints[i], validPoints[j], unit);
    }

    return perimeter;
  },

  /**
   * 计算多点路径的插值点
   * @param {Array} points - 点数组 [{ lat, lng }, ...]
   * @param {number} interval - 插值间隔（距离）
   * @param {string} [unit='km'] - 单位
   * @returns {Array} - 插值后的点数组
   */
  interpolatePath(points, interval, unit = 'km') {
    if (!Array.isArray(points) || points.length < 2 || interval <= 0) {
      return [];
    }

    const result = [];
    let remaining = 0;

    for (let i = 0; i < points.length - 1; i++) {
      const start = points[i];
      const end = points[i + 1];
      
      if (!this.isValid(start.lat, start.lng) || !this.isValid(end.lat, end.lng)) {
        continue;
      }

      const segmentDist = this.distance(start, end, unit);
      const bearing = this.bearing(start, end);

      // 添加起点
      result.push(start);

      // 在段内插值
      let covered = remaining;
      while (covered + interval < segmentDist) {
        covered += interval;
        const interpPoint = this.destination(start, bearing, covered, unit);
        result.push(interpPoint);
      }

      // 计算剩余距离
      remaining = segmentDist - covered;
    }

    // 添加最后一个点
    result.push(points[points.length - 1]);

    return result;
  },

  /**
   * 计算路径的简化版本（Douglas-Peucker 算法）
   * @param {Array} points - 点数组 [{ lat, lng }, ...]
   * @param {number} tolerance - 简化容差（距离）
   * @param {string} [unit='km'] - 单位
   * @returns {Array} - 简化后的点数组
   */
  simplifyPath(points, tolerance, unit = 'km') {
    if (!Array.isArray(points) || points.length <= 2) {
      return points ? [...points] : [];
    }

    const validPoints = points.filter(p => this.isValid(p.lat, p.lng));
    if (validPoints.length <= 2) return validPoints;

    // Douglas-Peucker 算法
    const simplify = (pts, first, last) => {
      if (last <= first + 1) return [];

      let maxDist = 0;
      let maxIndex = first;

      for (let i = first + 1; i < last; i++) {
        // 计算点到线段的距离
        const dist = this.perpendicularDistance(pts[i], pts[first], pts[last], unit);
        if (dist > maxDist) {
          maxDist = dist;
          maxIndex = i;
        }
      }

      if (maxDist > tolerance) {
        const left = simplify(pts, first, maxIndex);
        const right = simplify(pts, maxIndex, last);
        return [...left, pts[maxIndex], ...right];
      }

      return [];
    };

    const result = [validPoints[0]];
    result.push(...simplify(validPoints, 0, validPoints.length - 1));
    result.push(validPoints[validPoints.length - 1]);

    return result;
  },

  /**
   * 计算点到线段的垂直距离
   * @private
   */
  perpendicularDistance(point, lineStart, lineEnd, unit = 'km') {
    // 使用球面几何近似
    const segmentLength = this.distance(lineStart, lineEnd, unit);
    if (segmentLength === 0) {
      return this.distance(point, lineStart, unit);
    }

    // 计算投影比例
    const bearing = this.bearing(lineStart, lineEnd);
    const bearingToPoint = this.bearing(lineStart, point);
    const angle = Math.abs(bearingToPoint - bearing);
    
    if (angle > 180) angle = 360 - angle;
    if (angle > 90) {
      // 点在线段外
      const distToStart = this.distance(point, lineStart, unit);
      const distToEnd = this.distance(point, lineEnd, unit);
      return Math.min(distToStart, distToEnd);
    }

    // 计算垂直距离
    const distToStart = this.distance(lineStart, point, unit);
    return distToStart * Math.sin(this.toRadians(angle));
  },

  /**
   * 生成随机坐标点
   * @param {Object} [bounds] - 边界 { minLat, maxLat, minLng, maxLng }
   * @returns {Object} - 随机点 { lat, lng }
   */
  randomPoint(bounds = null) {
    if (bounds) {
      const lat = bounds.minLat + Math.random() * (bounds.maxLat - bounds.minLat);
      const lng = bounds.minLng + Math.random() * (bounds.maxLng - bounds.minLng);
      return { lat, lng };
    }

    // 全球范围
    const lat = -90 + Math.random() * 180;
    const lng = -180 + Math.random() * 360;
    return { lat, lng };
  },

  /**
   * 生成多个随机坐标点
   * @param {number} count - 数量
   * @param {Object} [bounds] - 边界
   * @returns {Array} - 随机点数组
   */
  randomPoints(count, bounds = null) {
    return Array.from({ length: count }, () => this.randomPoint(bounds));
  },

  /**
   * 计算网格坐标点
   * @param {Object} bounds - 边界 { minLat, maxLat, minLng, maxLng }
   * @param {number} rows - 行数
   * @param {number} cols - 列数
   * @returns {Array} - 网格点数组
   */
  gridPoints(bounds, rows, cols) {
    if (!bounds || rows <= 0 || cols <= 0) return [];

    const latStep = (bounds.maxLat - bounds.minLat) / (rows - 1 || 1);
    const lngStep = (bounds.maxLng - bounds.minLng) / (cols - 1 || 1);

    const points = [];
    for (let r = 0; r < rows; r++) {
      for (let c = 0; c < cols; c++) {
        points.push({
          lat: bounds.minLat + r * latStep,
          lng: bounds.minLng + c * lngStep,
          row: r,
          col: c
        });
      }
    }

    return points;
  },

  /**
   * 计算坐标的偏移量
   * @param {Object} point - 起点 { lat, lng }
   * @param {number} offsetLat - 纬度偏移（米）
   * @param {number} offsetLng - 经度偏移（米）
   * @returns {Object} - 新坐标 { lat, lng }
   */
  offsetByMeters(point, offsetLat, offsetLng) {
    if (!this.isValid(point.lat, point.lng)) {
      return { lat: NaN, lng: NaN };
    }

    // 1米对应的纬度变化（近似）
    const metersPerDegreeLat = this.EARTH_RADIUS_M * Math.PI / 180;
    const latOffsetDegrees = offsetLat / metersPerDegreeLat;

    // 1米对应的经度变化（考虑纬度）
    const metersPerDegreeLng = metersPerDegreeLat * Math.cos(this.toRadians(point.lat));
    const lngOffsetDegrees = offsetLng / metersPerDegreeLng;

    return {
      lat: point.lat + latOffsetDegrees,
      lng: this.normalizeLongitude(point.lng + lngOffsetDegrees)
    };
  },

  /**
   * 计算两点之间的纬度差（米）
   * @param {Object} point1 - 第一个点
   * @param {Object} point2 - 第二个点
   * @returns {number} - 纬度差（米）
   */
  latDifferenceInMeters(point1, point2) {
    const latDiff = Math.abs(point2.lat - point1.lat);
    return latDiff * this.EARTH_RADIUS_M * Math.PI / 180;
  },

  /**
   * 计算两点之间的经度差（米）
   * @param {Object} point1 - 第一个点
   * @param {Object} point2 - 第二个点
   * @returns {number} - 经度差（米）
   */
  lngDifferenceInMeters(point1, point2) {
    const avgLat = (point1.lat + point2.lat) / 2;
    const lngDiff = Math.abs(point2.lng - point1.lng);
    return lngDiff * this.EARTH_RADIUS_M * Math.PI / 180 * Math.cos(this.toRadians(avgLat));
  },

  /**
   * 计算两点之间的方向（东西南北）
   * @param {Object} point1 - 起点
   * @param {Object} point2 - 终点
   * @returns {Object} - { direction: 方向名称, bearing: 方位角 }
   */
  getDirection(point1, point2) {
    const bearing = this.bearing(point1, point2);
    
    const directions = [
      { min: 0, max: 22.5, name: 'North', abbr: 'N' },
      { min: 22.5, max: 67.5, name: 'North-East', abbr: 'NE' },
      { min: 67.5, max: 112.5, name: 'East', abbr: 'E' },
      { min: 112.5, max: 157.5, name: 'South-East', abbr: 'SE' },
      { min: 157.5, max: 202.5, name: 'South', abbr: 'S' },
      { min: 202.5, max: 247.5, name: 'South-West', abbr: 'SW' },
      { min: 247.5, max: 292.5, name: 'West', abbr: 'W' },
      { min: 292.5, max: 337.5, name: 'North-West', abbr: 'NW' },
      { min: 337.5, max: 360, name: 'North', abbr: 'N' }
    ];

    for (const dir of directions) {
      if (bearing >= dir.min && bearing < dir.max) {
        return { direction: dir.name, abbreviation: dir.abbr, bearing };
      }
    }

    return { direction: 'North', abbreviation: 'N', bearing };
  },

  /**
   * 计算Vincenty距离（更精确的地球表面距离）
   * @param {Object} point1 - 起点 { lat, lng }
   * @param {Object} point2 - 终点 { lat, lng }
   * @param {string} [unit='km'] - 单位
   * @returns {number} - 距离
   */
  vincentyDistance(point1, point2, unit = 'km') {
    if (!this.isValid(point1.lat, point1.lng) || !this.isValid(point2.lat, point2.lng)) {
      return NaN;
    }

    // WGS-84 椭球参数
    const a = 6378137; // 长半轴（米）
    const b = 6356752.314245; // 短半轴（米）
    const f = 1 / 298.257223563; // 扁率

    const L = this.toRadians(point2.lng - point1.lng);
    const U1 = Math.atan((1 - f) * Math.tan(this.toRadians(point1.lat)));
    const U2 = Math.atan((1 - f) * Math.tan(this.toRadians(point2.lat)));

    let lambda = L;
    let lambdaP;
    let iterLimit = 100;
    const sinU1 = Math.sin(U1), cosU1 = Math.cos(U1);
    const sinU2 = Math.sin(U2), cosU2 = Math.cos(U2);
    
    // 在循环外声明变量
    let sinSigma = 0, cosSigma = 0, sigma = 0;
    let sinAlpha = 0, cosSqAlpha = 1, cos2SigmaM = 0;

    do {
      const sinLambda = Math.sin(lambda);
      const cosLambda = Math.cos(lambda);
      sinSigma = Math.sqrt(
        (cosU2 * sinLambda) ** 2 +
        (cosU1 * sinU2 - sinU1 * cosU2 * cosLambda) ** 2
      );
      
      if (sinSigma === 0) return 0; // 共点

      cosSigma = sinU1 * sinU2 + cosU1 * cosU2 * cosLambda;
      sigma = Math.atan2(sinSigma, cosSigma);
      sinAlpha = cosU1 * cosU2 * sinLambda / sinSigma;
      cosSqAlpha = 1 - sinAlpha ** 2;
      
      // 处理 cosSqAlpha 为 0 的情况
      if (cosSqAlpha === 0) {
        cos2SigmaM = 0;
      } else {
        cos2SigmaM = cosSigma - 2 * sinU1 * sinU2 / cosSqAlpha;
      }

      const C = f / 16 * cosSqAlpha * (4 + f * (4 - 3 * cosSqAlpha));
      lambdaP = lambda;
      lambda = L + (1 - C) * f * sinAlpha *
        (sigma + C * sinSigma * (cos2SigmaM + C * cosSigma * (-1 + 2 * cos2SigmaM ** 2)));
    } while (Math.abs(lambda - lambdaP) > 1e-12 && --iterLimit > 0);

    if (iterLimit === 0) return NaN; // 无法收敛

    const uSq = cosSqAlpha * (a ** 2 - b ** 2) / b ** 2;
    const A = 1 + uSq / 16384 * (4096 + uSq * (-768 + uSq * (320 - 175 * uSq)));
    const B = uSq / 1024 * (256 + uSq * (-128 + uSq * (74 - 47 * uSq)));
    
    const deltaSigma = B * sinSigma *
      (cos2SigmaM + B / 4 * (cosSigma * (-1 + 2 * cos2SigmaM ** 2) -
       B / 6 * cos2SigmaM * (-3 + 4 * sinSigma ** 2) * (-3 + 4 * cos2SigmaM ** 2)));

    const s = b * A * (sigma - deltaSigma);

    // 单位转换
    if (unit === 'km') return s / 1000;
    if (unit === 'm') return s;
    if (unit === 'mi') return s / 1609.344;
    if (unit === 'ft') return s / 0.3048;
    return s / 1000;
  },

  /**
   * 计算两个坐标点的相似度（基于距离）
   * @param {Object} point1 - 第一个点
   * @param {Object} point2 - 第二个点
   * @param {number} threshold - 相似阈值（距离）
   * @param {string} [unit='km'] - 单位
   * @returns {number} - 相似度（0-1）
   */
  similarity(point1, point2, threshold = 10, unit = 'km') {
    const dist = this.distance(point1, point2, unit);
    if (dist >= threshold) return 0;
    return 1 - (dist / threshold);
  },

  /**
   * 对坐标点数组进行排序（按距离）
   * @param {Object} origin - 原点
   * @param {Array} points - 点数组
   * @param {string} [unit='km'] - 单位
   * @param {string} [order='asc'] - 排序方向
   * @returns {Array} - 排序后的数组，带距离信息
   */
  sortByDistance(origin, points, unit = 'km', order = 'asc') {
    if (!Array.isArray(points) || !this.isValid(origin.lat, origin.lng)) {
      return [];
    }

    const result = points
      .filter(p => this.isValid(p.lat, p.lng))
      .map(p => ({
        point: p,
        distance: this.distance(origin, p, unit)
      }));

    const multiplier = order === 'asc' ? 1 : -1;
    return result.sort((a, b) => multiplier * (a.distance - b.distance));
  },

  /**
   * 转换坐标到不同坐标系（简化版）
   * 仅做平移偏移，不涉及完整坐标转换
   * @param {Object} point - 点 { lat, lng }
   * @param {Object} offset - 偏移 { lat, lng }
   * @returns {Object} - 新坐标
   */
  translateCoordinate(point, offset) {
    if (!this.isValid(point.lat, point.lng)) {
      return { lat: NaN, lng: NaN };
    }

    return {
      lat: this.normalizeLatitude(point.lat + offset.lat),
      lng: this.normalizeLongitude(point.lng + offset.lng)
    };
  },

  /**
   * 创建坐标矩形
   * @param {Object} center - 中心点
   * @param {number} width - 宽度（距离）
   * @param {number} height - 高度（距离）
   * @param {string} [unit='km'] - 单位
   * @returns {Array} - 矩形四个顶点
   */
  createRectangle(center, width, height, unit = 'km') {
    if (!this.isValid(center.lat, center.lng)) {
      return [];
    }

    // 计算四条边的偏移
    const halfWidth = width / 2;
    const halfHeight = height / 2;

    const nw = this.destination(center, 315, Math.sqrt(halfWidth ** 2 + halfHeight ** 2), unit);
    const ne = this.destination(center, 45, Math.sqrt(halfWidth ** 2 + halfHeight ** 2), unit);
    const se = this.destination(center, 135, Math.sqrt(halfWidth ** 2 + halfHeight ** 2), unit);
    const sw = this.destination(center, 225, Math.sqrt(halfWidth ** 2 + halfHeight ** 2), unit);

    return [nw, ne, se, sw];
  },

  /**
   * 创建圆形坐标点
   * @param {Object} center - 中心点
   * @param {number} radius - 半径
   * @param {number} segments - 分段数
   * @param {string} [unit='km'] - 单位
   * @returns {Array} - 圆形点数组
   */
  createCircle(center, radius, segments = 36, unit = 'km') {
    if (!this.isValid(center.lat, center.lng) || segments <= 0) {
      return [];
    }

    const points = [];
    const angleStep = 360 / segments;

    for (let i = 0; i < segments; i++) {
      const bearing = i * angleStep;
      const point = this.destination(center, bearing, radius, unit);
      points.push(point);
    }

    return points;
  },

  /**
   * 创建扇形坐标点
   * @param {Object} center - 中心点
   * @param {number} radius - 半径
   * @param {number} startAngle - 起始角度
   * @param {number} endAngle - 结束角度
   * @param {number} segments - 分段数
   * @param {string} [unit='km'] - 单位
   * @returns {Array} - 扇形点数组
   */
  createSector(center, radius, startAngle, endAngle, segments = 36, unit = 'km') {
    if (!this.isValid(center.lat, center.lng) || segments <= 0) {
      return [];
    }

    const points = [center];
    const angleRange = endAngle - startAngle;
    const angleStep = angleRange / segments;

    for (let i = 0; i <= segments; i++) {
      const bearing = startAngle + i * angleStep;
      const point = this.destination(center, bearing, radius, unit);
      points.push(point);
    }

    points.push(center); // 闭合扇形
    return points;
  }
};

// 导出模块
module.exports = CoordinateUtils;