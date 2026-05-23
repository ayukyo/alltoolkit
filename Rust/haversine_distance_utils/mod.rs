//! 哈弗辛距离工具库 - 零外部依赖
//!
//! 提供完整的地理距离计算功能，基于哈弗辛公式
//! 支持多种单位、边界框计算、方位角计算等功能



/// 地球半径常量（单位：公里）
pub const EARTH_RADIUS_KM: f64 = 6371.0;

/// 地球半径常量（单位：英里）
pub const EARTH_RADIUS_MI: f64 = 3958.8;

/// 地球半径常量（单位：海里）
pub const EARTH_RADIUS_NM: f64 = 3440.1;

/// 距离单位枚举
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum DistanceUnit {
    /// 公里
    Kilometers,
    /// 米
    Meters,
    /// 英里
    Miles,
    /// 海里
    NauticalMiles,
    /// 英尺
    Feet,
    /// 码
    Yards,
}

impl DistanceUnit {
    /// 获取对应的地球半径
    pub fn earth_radius(&self) -> f64 {
        match self {
            DistanceUnit::Kilometers => EARTH_RADIUS_KM,
            DistanceUnit::Meters => EARTH_RADIUS_KM * 1000.0,
            DistanceUnit::Miles => EARTH_RADIUS_MI,
            DistanceUnit::NauticalMiles => EARTH_RADIUS_NM,
            DistanceUnit::Feet => EARTH_RADIUS_MI * 5280.0,
            DistanceUnit::Yards => EARTH_RADIUS_MI * 1760.0,
        }
    }

    /// 单位名称
    pub fn name(&self) -> &'static str {
        match self {
            DistanceUnit::Kilometers => "km",
            DistanceUnit::Meters => "m",
            DistanceUnit::Miles => "mi",
            DistanceUnit::NauticalMiles => "nmi",
            DistanceUnit::Feet => "ft",
            DistanceUnit::Yards => "yd",
        }
    }
}

/// 地理坐标点
#[derive(Debug, Clone, Copy, PartialEq)]
pub struct GeoPoint {
    /// 纬度（-90 到 90）
    pub latitude: f64,
    /// 经度（-180 到 180）
    pub longitude: f64,
}

impl GeoPoint {
    /// 创建新的地理坐标点
    pub fn new(latitude: f64, longitude: f64) -> Self {
        GeoPoint { latitude, longitude }
    }

    /// 从度分秒格式创建坐标点
    pub fn from_dms(lat_deg: i32, lat_min: i32, lat_sec: f64, lat_dir: char,
                    lon_deg: i32, lon_min: i32, lon_sec: f64, lon_dir: char) -> Self {
        let lat = (lat_deg as f64 + lat_min as f64 / 60.0 + lat_sec / 3600.0)
            * if lat_dir == 'S' || lat_dir == 's' { -1.0 } else { 1.0 };
        let lon = (lon_deg as f64 + lon_min as f64 / 60.0 + lon_sec / 3600.0)
            * if lon_dir == 'W' || lon_dir == 'w' { -1.0 } else { 1.0 };
        GeoPoint { latitude: lat, longitude: lon }
    }

    /// 验证坐标是否有效
    pub fn is_valid(&self) -> bool {
        self.latitude >= -90.0 && self.latitude <= 90.0 &&
        self.longitude >= -180.0 && self.longitude <= 180.0
    }

    /// 转换为弧度
    pub fn to_radians(&self) -> (f64, f64) {
        (self.latitude.to_radians(), self.longitude.to_radians())
    }

    /// 计算与另一点的距离（默认公里）
    pub fn distance_to(&self, other: &GeoPoint) -> f64 {
        self.distance_to_with_unit(other, DistanceUnit::Kilometers)
    }

    /// 计算与另一点的距离（指定单位）
    pub fn distance_to_with_unit(&self, other: &GeoPoint, unit: DistanceUnit) -> f64 {
        haversine_distance(
            self.latitude, self.longitude,
            other.latitude, other.longitude,
            unit,
        )
    }

    /// 计算到另一点的方位角（度）
    pub fn bearing_to(&self, other: &GeoPoint) -> f64 {
        calculate_bearing(
            self.latitude, self.longitude,
            other.latitude, other.longitude,
        )
    }

    /// 计算到另一点的初始方位角名称
    pub fn bearing_name(&self, other: &GeoPoint) -> &'static str {
        bearing_to_name(self.bearing_to(other))
    }

    /// 计算从某点以指定方位角和距离到达的终点
    pub fn destination(&self, bearing: f64, distance: f64, unit: DistanceUnit) -> GeoPoint {
        calculate_destination(self.latitude, self.longitude, bearing, distance, unit)
    }

    /// 计算中点
    pub fn midpoint(&self, other: &GeoPoint) -> GeoPoint {
        calculate_midpoint(
            self.latitude, self.longitude,
            other.latitude, other.longitude,
        )
    }

    /// 判断点是否在指定半径内
    pub fn is_within_radius(&self, center: &GeoPoint, radius: f64, unit: DistanceUnit) -> bool {
        self.distance_to_with_unit(center, unit) <= radius
    }
}

/// 使用哈弗辛公式计算两点间的球面距离
///
/// # 参数
/// - `lat1`: 第一点纬度（度）
/// - `lon1`: 第一点经度（度）
/// - `lat2`: 第二点纬度（度）
/// - `lon2`: 第二点经度（度）
/// - `unit`: 距离单位
///
/// # 返回
/// 两点间的球面距离
pub fn haversine_distance(lat1: f64, lon1: f64, lat2: f64, lon2: f64, unit: DistanceUnit) -> f64 {
    let lat1_rad = lat1.to_radians();
    let lat2_rad = lat2.to_radians();
    let delta_lat = (lat2 - lat1).to_radians();
    let delta_lon = (lon2 - lon1).to_radians();

    let a = (delta_lat / 2.0).sin().powi(2) +
            lat1_rad.cos() * lat2_rad.cos() * (delta_lon / 2.0).sin().powi(2);
    let c = 2.0 * a.sqrt().atan2((1.0 - a).sqrt());

    unit.earth_radius() * c
}

/// 计算两点间的方位角（初始方位角）
///
/// # 返回
/// 方位角（度，0-360，正北为0，顺时针）
pub fn calculate_bearing(lat1: f64, lon1: f64, lat2: f64, lon2: f64) -> f64 {
    let lat1_rad = lat1.to_radians();
    let lat2_rad = lat2.to_radians();
    let delta_lon = (lon2 - lon1).to_radians();

    let y = delta_lon.sin() * lat2_rad.cos();
    let x = lat1_rad.cos() * lat2_rad.sin() -
            lat1_rad.sin() * lat2_rad.cos() * delta_lon.cos();

    let bearing = y.atan2(x).to_degrees();
    (bearing + 360.0) % 360.0
}

/// 将方位角转换为方向名称
pub fn bearing_to_name(bearing: f64) -> &'static str {
    let directions = [
        "N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
        "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW",
    ];
    let index = ((bearing + 11.25) / 22.5).floor() as usize % 16;
    directions[index]
}

/// 计算从起点以指定方位角行进一定距离后的终点
///
/// # 参数
/// - `lat`: 起点纬度（度）
/// - `lon`: 起点经度（度）
/// - `bearing`: 方位角（度）
/// - `distance`: 距离
/// - `unit`: 距离单位
///
/// # 返回
/// 终点坐标
pub fn calculate_destination(lat: f64, lon: f64, bearing: f64, distance: f64, unit: DistanceUnit) -> GeoPoint {
    let lat_rad = lat.to_radians();
    let lon_rad = lon.to_radians();
    let bearing_rad = bearing.to_radians();
    let angular_distance = distance / unit.earth_radius();

    let dest_lat = (lat_rad.sin() * angular_distance.cos() +
                   lat_rad.cos() * angular_distance.sin() * bearing_rad.cos()).asin();
    let dest_lon = lon_rad + (bearing_rad.sin() * angular_distance.sin() * lat_rad.cos()).atan2(
        angular_distance.cos() - lat_rad.sin() * dest_lat.sin()
    );

    GeoPoint {
        latitude: dest_lat.to_degrees(),
        longitude: dest_lon.to_degrees(),
    }
}

/// 计算两点的中点
pub fn calculate_midpoint(lat1: f64, lon1: f64, lat2: f64, lon2: f64) -> GeoPoint {
    let lat1_rad = lat1.to_radians();
    let lat2_rad = lat2.to_radians();
    let lon1_rad = lon1.to_radians();
    let delta_lon = (lon2 - lon1).to_radians();

    let bx = lat2_rad.cos() * delta_lon.cos();
    let by = lat2_rad.cos() * delta_lon.sin();

    let mid_lat = (lat1_rad.sin() + lat2_rad.sin()).atan2(
        (lat1_rad.cos() + bx).hypot(by)
    );
    let mid_lon = lon1_rad + by.atan2(lat1_rad.cos() + bx);

    GeoPoint {
        latitude: mid_lat.to_degrees(),
        longitude: mid_lon.to_degrees(),
    }
}

/// 边界框
#[derive(Debug, Clone, Copy, PartialEq)]
pub struct BoundingBox {
    pub min_lat: f64,
    pub max_lat: f64,
    pub min_lon: f64,
    pub max_lon: f64,
}

impl BoundingBox {
    /// 创建新的边界框
    pub fn new(min_lat: f64, max_lat: f64, min_lon: f64, max_lon: f64) -> Self {
        BoundingBox { min_lat, max_lat, min_lon, max_lon }
    }

    /// 从中心点和半径创建边界框
    pub fn from_center_radius(center: &GeoPoint, radius: f64, unit: DistanceUnit) -> Self {
        let radius_km = match unit {
            DistanceUnit::Kilometers => radius,
            DistanceUnit::Meters => radius / 1000.0,
            DistanceUnit::Miles => radius * 1.60934,
            DistanceUnit::NauticalMiles => radius * 1.852,
            DistanceUnit::Feet => radius * 0.0003048,
            DistanceUnit::Yards => radius * 0.0009144,
        };

        // 计算纬度偏移（大约每度 111 公里）
        let lat_offset = radius_km / 111.0;

        // 计算经度偏移（取决于纬度）
        let lon_offset = radius_km / (111.0 * center.latitude.to_radians().cos());

        BoundingBox {
            min_lat: center.latitude - lat_offset,
            max_lat: center.latitude + lat_offset,
            min_lon: center.longitude - lon_offset,
            max_lon: center.longitude + lon_offset,
        }
    }

    /// 检查点是否在边界框内
    pub fn contains(&self, point: &GeoPoint) -> bool {
        point.latitude >= self.min_lat &&
        point.latitude <= self.max_lat &&
        point.longitude >= self.min_lon &&
        point.longitude <= self.max_lon
    }

    /// 获取边界框的四个角点
    pub fn corners(&self) -> [GeoPoint; 4] {
        [
            GeoPoint::new(self.min_lat, self.min_lon), // 西南
            GeoPoint::new(self.min_lat, self.max_lon), // 东南
            GeoPoint::new(self.max_lat, self.max_lon), // 东北
            GeoPoint::new(self.max_lat, self.min_lon), // 西北
        ]
    }

    /// 计算边界框的中心点
    pub fn center(&self) -> GeoPoint {
        GeoPoint::new(
            (self.min_lat + self.max_lat) / 2.0,
            (self.min_lon + self.max_lon) / 2.0,
        )
    }

    /// 计算边界框对角线距离
    pub fn diagonal_distance(&self, unit: DistanceUnit) -> f64 {
        haversine_distance(
            self.min_lat, self.min_lon,
            self.max_lat, self.max_lon,
            unit,
        )
    }
}

/// 地理距离计算器
pub struct GeoCalculator {
    unit: DistanceUnit,
}

impl GeoCalculator {
    /// 创建新的计算器
    pub fn new(unit: DistanceUnit) -> Self {
        GeoCalculator { unit }
    }

    /// 创建使用公制的计算器
    pub fn metric() -> Self {
        GeoCalculator { unit: DistanceUnit::Kilometers }
    }

    /// 创建使用英制的计算器
    pub fn imperial() -> Self {
        GeoCalculator { unit: DistanceUnit::Miles }
    }

    /// 计算两点间距离
    pub fn distance(&self, p1: &GeoPoint, p2: &GeoPoint) -> f64 {
        p1.distance_to_with_unit(p2, self.unit)
    }

    /// 计算多点路径总长度
    pub fn path_length(&self, points: &[GeoPoint]) -> f64 {
        if points.len() < 2 {
            return 0.0;
        }
        points.windows(2)
            .map(|w| w[0].distance_to_with_unit(&w[1], self.unit))
            .sum()
    }

    /// 找到离给定点最近的点
    pub fn nearest(&self, origin: &GeoPoint, points: &[GeoPoint]) -> Option<(usize, f64)> {
        points.iter()
            .enumerate()
            .map(|(i, p)| (i, origin.distance_to_with_unit(p, self.unit)))
            .min_by(|a, b| a.1.partial_cmp(&b.1).unwrap())
    }

    /// 找到离给定点最远的点
    pub fn farthest(&self, origin: &GeoPoint, points: &[GeoPoint]) -> Option<(usize, f64)> {
        points.iter()
            .enumerate()
            .map(|(i, p)| (i, origin.distance_to_with_unit(p, self.unit)))
            .max_by(|a, b| a.1.partial_cmp(&b.1).unwrap())
    }

    /// 计算一组点的质心
    pub fn centroid(&self, points: &[GeoPoint]) -> Option<GeoPoint> {
        if points.is_empty() {
            return None;
        }

        let (x, y, z) = points.iter()
            .map(|p| {
                let lat_rad = p.latitude.to_radians();
                let lon_rad = p.longitude.to_radians();
                (lat_rad.cos() * lon_rad.cos(),
                 lat_rad.cos() * lon_rad.sin(),
                 lat_rad.sin())
            })
            .fold((0.0, 0.0, 0.0), |acc, (x, y, z)| (acc.0 + x, acc.1 + y, acc.2 + z));

        let n = points.len() as f64;
        let x_avg = x / n;
        let y_avg = y / n;
        let z_avg = z / n;

        let lon = y_avg.atan2(x_avg).to_degrees();
        let lat = z_avg.atan2((x_avg * x_avg + y_avg * y_avg).sqrt()).to_degrees();

        Some(GeoPoint::new(lat, lon))
    }

    /// 过滤半径内的点
    pub fn within_radius<'a>(&self, center: &GeoPoint, radius: f64, points: &'a [GeoPoint]) -> Vec<&'a GeoPoint> {
        points.iter()
            .filter(|p| p.distance_to_with_unit(center, self.unit) <= radius)
            .collect()
    }
}

/// 距离格式化器
pub struct DistanceFormatter;

impl DistanceFormatter {
    /// 格式化距离为可读字符串
    pub fn format(distance: f64, unit: DistanceUnit) -> String {
        format!("{:.2} {}", distance, unit.name())
    }

    /// 格式化距离，自动选择合适单位
    pub fn format_auto(distance_km: f64) -> String {
        if distance_km < 1.0 {
            format!("{:.0} m", distance_km * 1000.0)
        } else if distance_km < 10.0 {
            format!("{:.2} km", distance_km)
        } else if distance_km < 100.0 {
            format!("{:.1} km", distance_km)
        } else {
            format!("{:.0} km", distance_km)
        }
    }

    /// 将距离从一种单位转换为另一种
    pub fn convert(value: f64, from: DistanceUnit, to: DistanceUnit) -> f64 {
        let km = match from {
            DistanceUnit::Kilometers => value,
            DistanceUnit::Meters => value / 1000.0,
            DistanceUnit::Miles => value * 1.60934,
            DistanceUnit::NauticalMiles => value * 1.852,
            DistanceUnit::Feet => value * 0.0003048,
            DistanceUnit::Yards => value * 0.0009144,
        };

        match to {
            DistanceUnit::Kilometers => km,
            DistanceUnit::Meters => km * 1000.0,
            DistanceUnit::Miles => km / 1.60934,
            DistanceUnit::NauticalMiles => km / 1.852,
            DistanceUnit::Feet => km / 0.0003048,
            DistanceUnit::Yards => km / 0.0009144,
        }
    }
}

/// 预定义的著名城市坐标
pub mod cities {
    use super::GeoPoint;

    /// 北京
    pub const BEIJING: GeoPoint = GeoPoint { latitude: 39.9042, longitude: 116.4074 };
    /// 上海
    pub const SHANGHAI: GeoPoint = GeoPoint { latitude: 31.2304, longitude: 121.4737 };
    /// 纽约
    pub const NEW_YORK: GeoPoint = GeoPoint { latitude: 40.7128, longitude: -74.0060 };
    /// 伦敦
    pub const LONDON: GeoPoint = GeoPoint { latitude: 51.5074, longitude: -0.1278 };
    /// 东京
    pub const TOKYO: GeoPoint = GeoPoint { latitude: 35.6762, longitude: 139.6503 };
    /// 巴黎
    pub const PARIS: GeoPoint = GeoPoint { latitude: 48.8566, longitude: 2.3522 };
    /// 悉尼
    pub const SYDNEY: GeoPoint = GeoPoint { latitude: -33.8688, longitude: 151.2093 };
    /// 新加坡
    pub const SINGAPORE: GeoPoint = GeoPoint { latitude: 1.3521, longitude: 103.8198 };
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_haversine_distance_same_point() {
        let distance = haversine_distance(40.0, -74.0, 40.0, -74.0, DistanceUnit::Kilometers);
        assert_eq!(distance, 0.0);
    }

    #[test]
    fn test_haversine_distance_beijing_shanghai() {
        let distance = haversine_distance(
            cities::BEIJING.latitude, cities::BEIJING.longitude,
            cities::SHANGHAI.latitude, cities::SHANGHAI.longitude,
            DistanceUnit::Kilometers,
        );
        // 北京到上海约 1068 公里
        assert!(distance > 1060.0 && distance < 1080.0);
    }

    #[test]
    fn test_haversine_distance_new_york_london() {
        let distance = haversine_distance(
            cities::NEW_YORK.latitude, cities::NEW_YORK.longitude,
            cities::LONDON.latitude, cities::LONDON.longitude,
            DistanceUnit::Kilometers,
        );
        // 纽约到伦敦约 5570 公里
        assert!(distance > 5500.0 && distance < 5600.0);
    }

    #[test]
    fn test_distance_unit_conversion() {
        let km = haversine_distance(0.0, 0.0, 0.0, 1.0, DistanceUnit::Kilometers);
        let miles = haversine_distance(0.0, 0.0, 0.0, 1.0, DistanceUnit::Miles);
        let nm = haversine_distance(0.0, 0.0, 0.0, 1.0, DistanceUnit::NauticalMiles);

        assert!(miles < km); // 英里数应该小于公里数
        assert!(nm < km); // 海里数应该小于公里数
    }

    #[test]
    fn test_geo_point_creation() {
        let point = GeoPoint::new(40.7128, -74.0060);
        assert_eq!(point.latitude, 40.7128);
        assert_eq!(point.longitude, -74.0060);
        assert!(point.is_valid());
    }

    #[test]
    fn test_geo_point_invalid() {
        let invalid = GeoPoint::new(100.0, 200.0);
        assert!(!invalid.is_valid());
    }

    #[test]
    fn test_bearing() {
        // 从北极到赤道应该是正南（180度）
        let bearing = calculate_bearing(90.0, 0.0, 0.0, 0.0);
        assert!((bearing - 180.0).abs() < 1.0);

        // 从赤道到北极应该是正北（0度）
        let bearing = calculate_bearing(0.0, 0.0, 90.0, 0.0);
        assert!(bearing < 1.0 || bearing > 359.0);
    }

    #[test]
    fn test_bearing_name() {
        assert_eq!(bearing_to_name(0.0), "N");
        assert_eq!(bearing_to_name(45.0), "NE");
        assert_eq!(bearing_to_name(90.0), "E");
        assert_eq!(bearing_to_name(135.0), "SE");
        assert_eq!(bearing_to_name(180.0), "S");
        assert_eq!(bearing_to_name(225.0), "SW");
        assert_eq!(bearing_to_name(270.0), "W");
        assert_eq!(bearing_to_name(315.0), "NW");
    }

    #[test]
    fn test_midpoint() {
        let mid = calculate_midpoint(0.0, 0.0, 0.0, 2.0);
        assert!((mid.longitude - 1.0).abs() < 0.001);
    }

    #[test]
    fn test_destination() {
        // 从赤道向正北行进约 111 公里，应该到达约 1 度纬度
        let dest = calculate_destination(0.0, 0.0, 0.0, 111.0, DistanceUnit::Kilometers);
        assert!((dest.latitude - 1.0).abs() < 0.1);
        assert!(dest.longitude.abs() < 0.1);
    }

    #[test]
    fn test_bounding_box() {
        let center = GeoPoint::new(40.0, -74.0);
        let bbox = BoundingBox::from_center_radius(&center, 10.0, DistanceUnit::Kilometers);

        // 边界框应该包含中心点
        assert!(bbox.contains(&center));

        // 远离中心的点不应该在边界框内
        let far_point = GeoPoint::new(50.0, -74.0);
        assert!(!bbox.contains(&far_point));
    }

    #[test]
    fn test_geo_calculator_distance() {
        let calc = GeoCalculator::metric();
        let d = calc.distance(&cities::BEIJING, &cities::SHANGHAI);
        assert!(d > 1060.0 && d < 1080.0);
    }

    #[test]
    fn test_geo_calculator_path_length() {
        let calc = GeoCalculator::metric();
        let points = vec![
            GeoPoint::new(0.0, 0.0),
            GeoPoint::new(0.0, 1.0),
            GeoPoint::new(1.0, 1.0),
        ];
        let length = calc.path_length(&points);
        assert!(length > 0.0);
    }

    #[test]
    fn test_geo_calculator_nearest() {
        let calc = GeoCalculator::metric();
        let origin = GeoPoint::new(0.0, 0.0);
        let points = vec![
            GeoPoint::new(10.0, 10.0),
            GeoPoint::new(1.0, 1.0),
            GeoPoint::new(5.0, 5.0),
        ];
        let result = calc.nearest(&origin, &points);
        assert_eq!(result.map(|(i, _)| i), Some(1));
    }

    #[test]
    fn test_geo_calculator_centroid() {
        let calc = GeoCalculator::metric();
        let points = vec![
            GeoPoint::new(0.0, 0.0),
            GeoPoint::new(0.0, 2.0),
        ];
        let centroid = calc.centroid(&points).unwrap();
        assert!((centroid.longitude - 1.0).abs() < 0.01);
    }

    #[test]
    fn test_distance_formatter() {
        let formatted = DistanceFormatter::format(100.5, DistanceUnit::Kilometers);
        assert_eq!(formatted, "100.50 km");

        let auto = DistanceFormatter::format_auto(0.5);
        assert!(auto.contains("m"));

        let auto_km = DistanceFormatter::format_auto(50.0);
        assert!(auto_km.contains("km"));
    }

    #[test]
    fn test_distance_conversion() {
        let miles = DistanceFormatter::convert(1.0, DistanceUnit::Kilometers, DistanceUnit::Miles);
        assert!((miles - 0.621371).abs() < 0.01);

        let meters = DistanceFormatter::convert(1.0, DistanceUnit::Kilometers, DistanceUnit::Meters);
        assert_eq!(meters, 1000.0);
    }

    #[test]
    fn test_cities() {
        // 测试预定义城市坐标有效性
        assert!(cities::BEIJING.is_valid());
        assert!(cities::NEW_YORK.is_valid());
        assert!(cities::SYDNEY.is_valid()); // 南半球
    }

    #[test]
    fn test_geo_point_distance_to() {
        let beijing = GeoPoint::new(cities::BEIJING.latitude, cities::BEIJING.longitude);
        let shanghai = GeoPoint::new(cities::SHANGHAI.latitude, cities::SHANGHAI.longitude);

        let distance = beijing.distance_to(&shanghai);
        assert!(distance > 1060.0 && distance < 1080.0);
    }

    #[test]
    fn test_geo_point_within_radius() {
        let center = GeoPoint::new(0.0, 0.0);
        let inside = GeoPoint::new(0.0, 0.01);
        let outside = GeoPoint::new(10.0, 10.0);

        assert!(inside.is_within_radius(&center, 10.0, DistanceUnit::Kilometers));
        assert!(!outside.is_within_radius(&center, 10.0, DistanceUnit::Kilometers));
    }

    #[test]
    fn test_bounding_box_corners() {
        let bbox = BoundingBox::new(0.0, 10.0, 0.0, 20.0);
        let corners = bbox.corners();

        assert_eq!(corners[0].latitude, 0.0);  // 西南
        assert_eq!(corners[0].longitude, 0.0);
        assert_eq!(corners[2].latitude, 10.0); // 东北
        assert_eq!(corners[2].longitude, 20.0);
    }

    #[test]
    fn test_geo_calculator_within_radius() {
        let calc = GeoCalculator::metric();
        let center = GeoPoint::new(0.0, 0.0);
        let points = vec![
            GeoPoint::new(0.0, 0.01),   // 约 1.1 km
            GeoPoint::new(0.0, 0.1),    // 约 11 km
            GeoPoint::new(0.0, 0.2),    // 约 22 km
        ];

        let within = calc.within_radius(&center, 15.0, &points);
        assert_eq!(within.len(), 2);
    }
}