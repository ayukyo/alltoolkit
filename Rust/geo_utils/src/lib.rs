//! # Geo Utils
//!
//! A comprehensive geographic coordinate utility library.
//! Provides distance calculation, bearing, destination point, GeoHash encoding/decoding,
//! bounding box, and polygon containment checks.
//! Zero external dependencies - uses only Rust standard library.
//!
//! ## Features
//!
//! - Coordinate representation with latitude/longitude
//! - Haversine distance calculation (great-circle distance)
//! - Bearing calculation (initial and final bearing)
//! - Destination point calculation
//! - Midpoint calculation between two coordinates
//! - Bounding box generation
//! - GeoHash encoding and decoding (up to 12 characters precision)
//! - Polygon containment check (ray casting algorithm)
//! - Coordinate validation
//! - Various utility functions
//!
//! ## Example
//!
//! ```rust
//! use geo_utils::{Coordinate, GeoUtils};
//!
//! let coord1 = Coordinate::new(40.7128, -74.0060); // New York
//! let coord2 = Coordinate::new(51.5074, -0.1278);  // London
//!
//! // Calculate distance
//! let distance = GeoUtils::haversine_distance(&coord1, &coord2);
//! println!("Distance: {:.2} km", distance);
//!
//! // Calculate bearing
//! let bearing = GeoUtils::bearing(&coord1, &coord2);
//! println!("Bearing: {:.2}°", bearing);
//!
//! // Encode to GeoHash
//! let geohash = GeoUtils::encode_geohash(&coord1, 8);
//! println!("GeoHash: {}", geohash);
//! ```

use std::f64::consts::PI;

/// Earth radius in kilometers
const EARTH_RADIUS_KM: f64 = 6371.0;

/// Earth radius in meters
const EARTH_RADIUS_M: f64 = 6_371_000.0;

/// Earth radius in miles
const EARTH_RADIUS_MI: f64 = 3958.8;

/// Earth radius in nautical miles
const EARTH_RADIUS_NM: f64 = 3440.1;

/// GeoHash base32 characters
const GEOHASH_CHARS: &[u8; 32] = b"0123456789bcdefghjkmnpqrstuvwxyz";

/// Reverse lookup for GeoHash characters
fn build_geohash_reverse() -> [i8; 128] {
    let mut reverse = [-1i8; 128];
    for (i, &c) in GEOHASH_CHARS.iter().enumerate() {
        reverse[c as usize] = i as i8;
    }
    reverse
}

/// Geographic coordinate representation
#[derive(Debug, Clone, Copy, PartialEq)]
pub struct Coordinate {
    /// Latitude in degrees (-90 to 90)
    pub latitude: f64,
    /// Longitude in degrees (-180 to 180)
    pub longitude: f64,
}

impl Coordinate {
    /// Create a new coordinate
    pub fn new(latitude: f64, longitude: f64) -> Self {
        Self { latitude, longitude }
    }

    /// Create a coordinate from degrees, minutes, seconds
    pub fn from_dms(lat_deg: i32, lat_min: u32, lat_sec: f64, lat_dir: char,
                    lon_deg: i32, lon_min: u32, lon_sec: f64, lon_dir: char) -> Self {
        let lat = (lat_deg as f64) + (lat_min as f64) / 60.0 + lat_sec / 3600.0;
        let lon = (lon_deg as f64) + (lon_min as f64) / 60.0 + lon_sec / 3600.0;
        
        let latitude = if lat_dir == 'S' || lat_dir == 's' { -lat } else { lat };
        let longitude = if lon_dir == 'W' || lon_dir == 'w' { -lon } else { lon };
        
        Self { latitude, longitude }
    }

    /// Validate the coordinate
    pub fn is_valid(&self) -> bool {
        self.latitude >= -90.0 && self.latitude <= 90.0 &&
        self.longitude >= -180.0 && self.longitude <= 180.0
    }

    /// Normalize longitude to -180 to 180 range
    pub fn normalize_longitude(&self) -> Self {
        let mut lon = self.longitude % 360.0;
        if lon > 180.0 { lon -= 360.0; }
        else if lon < -180.0 { lon += 360.0; }
        Self { latitude: self.latitude, longitude: lon }
    }

    /// Convert to radians
    pub fn to_radians(&self) -> (f64, f64) {
        (self.latitude.to_radians(), self.longitude.to_radians())
    }

    /// Convert latitude to degrees, minutes, seconds
    pub fn lat_to_dms(&self) -> (i32, u32, f64, char) {
        let dir = if self.latitude >= 0.0 { 'N' } else { 'S' };
        let abs_lat = self.latitude.abs();
        let deg = abs_lat.floor() as i32;
        let min = ((abs_lat - deg as f64) * 60.0).floor() as u32;
        let sec = (abs_lat - deg as f64 - min as f64 / 60.0) * 3600.0;
        (deg, min, sec, dir)
    }

    /// Convert longitude to degrees, minutes, seconds
    pub fn lon_to_dms(&self) -> (i32, u32, f64, char) {
        let dir = if self.longitude >= 0.0 { 'E' } else { 'W' };
        let abs_lon = self.longitude.abs();
        let deg = abs_lon.floor() as i32;
        let min = ((abs_lon - deg as f64) * 60.0).floor() as u32;
        let sec = (abs_lon - deg as f64 - min as f64 / 60.0) * 3600.0;
        (deg, min, sec, dir)
    }

    /// Format as DMS string
    pub fn to_dms_string(&self) -> String {
        let (lat_deg, lat_min, lat_sec, lat_dir) = self.lat_to_dms();
        let (lon_deg, lon_min, lon_sec, lon_dir) = self.lon_to_dms();
        format!("{}°{}'{:.2}\"{} {}°{}'{:.2}\"{}",
                lat_deg, lat_min, lat_sec, lat_dir,
                lon_deg, lon_min, lon_sec, lon_dir)
    }

    /// Format as decimal degrees string
    pub fn to_dd_string(&self, precision: usize) -> String {
        format!("{:.precision$}°, {:.precision$}°", self.latitude, self.longitude, precision = precision)
    }

    /// Calculate distance to another coordinate (in km)
    pub fn distance_to(&self, other: &Coordinate) -> f64 {
        GeoUtils::haversine_distance(self, other)
    }

    /// Calculate bearing to another coordinate
    pub fn bearing_to(&self, other: &Coordinate) -> f64 {
        GeoUtils::bearing(self, other)
    }

    /// Get destination point from bearing and distance
    pub fn destination(&self, bearing: f64, distance_km: f64) -> Coordinate {
        GeoUtils::destination(self, bearing, distance_km)
    }

    /// Encode to GeoHash
    pub fn to_geohash(&self, precision: usize) -> String {
        GeoUtils::encode_geohash(self, precision)
    }

    /// Create from GeoHash
    pub fn from_geohash(geohash: &str) -> Option<Self> {
        GeoUtils::decode_geohash(geohash)
    }

    /// Check if within a polygon
    pub fn is_within_polygon(&self, polygon: &[Coordinate]) -> bool {
        GeoUtils::point_in_polygon(self, polygon)
    }
}

impl Default for Coordinate {
    fn default() -> Self { Self::new(0.0, 0.0) }
}

impl std::fmt::Display for Coordinate {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "({:.6}, {:.6})", self.latitude, self.longitude)
    }
}

/// Bounding box representation
#[derive(Debug, Clone, Copy)]
pub struct BoundingBox {
    pub min_lat: f64,
    pub max_lat: f64,
    pub min_lon: f64,
    pub max_lon: f64,
}

impl BoundingBox {
    /// Create a new bounding box
    pub fn new(min_lat: f64, max_lat: f64, min_lon: f64, max_lon: f64) -> Self {
        Self { min_lat, max_lat, min_lon, max_lon }
    }

    /// Create from two corners
    pub fn from_corners(c1: &Coordinate, c2: &Coordinate) -> Self {
        Self {
            min_lat: c1.latitude.min(c2.latitude),
            max_lat: c1.latitude.max(c2.latitude),
            min_lon: c1.longitude.min(c2.longitude),
            max_lon: c1.longitude.max(c2.longitude),
        }
    }

    /// Create from center point and radius
    pub fn from_center_radius(center: &Coordinate, radius_km: f64) -> Self {
        GeoUtils::bounding_box(center, radius_km)
    }

    /// Get the center of the bounding box
    pub fn center(&self) -> Coordinate {
        Coordinate::new((self.min_lat + self.max_lat) / 2.0, (self.min_lon + self.max_lon) / 2.0)
    }

    /// Get the width in degrees
    pub fn width(&self) -> f64 { self.max_lon - self.min_lon }

    /// Get the height in degrees
    pub fn height(&self) -> f64 { self.max_lat - self.min_lat }

    /// Check if a coordinate is within the bounding box
    pub fn contains(&self, coord: &Coordinate) -> bool {
        coord.latitude >= self.min_lat && coord.latitude <= self.max_lat &&
        coord.longitude >= self.min_lon && coord.longitude <= self.max_lon
    }

    /// Get the corners of the bounding box
    pub fn corners(&self) -> [Coordinate; 4] {
        [
            Coordinate::new(self.min_lat, self.min_lon), // SW
            Coordinate::new(self.min_lat, self.max_lon), // SE
            Coordinate::new(self.max_lat, self.max_lon), // NE
            Coordinate::new(self.max_lat, self.min_lon), // NW
        ]
    }

    /// Expand the bounding box by a factor
    pub fn expand(&self, factor: f64) -> Self {
        let lat_diff = (self.max_lat - self.min_lat) * factor / 2.0;
        let lon_diff = (self.max_lon - self.min_lon) * factor / 2.0;
        Self {
            min_lat: self.min_lat - lat_diff,
            max_lat: self.max_lat + lat_diff,
            min_lon: self.min_lon - lon_diff,
            max_lon: self.max_lon + lon_diff,
        }
    }

    /// Merge with another bounding box
    pub fn merge(&self, other: &BoundingBox) -> Self {
        Self {
            min_lat: self.min_lat.min(other.min_lat),
            max_lat: self.max_lat.max(other.max_lat),
            min_lon: self.min_lon.min(other.min_lon),
            max_lon: self.max_lon.max(other.max_lon),
        }
    }
}

impl std::fmt::Display for BoundingBox {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "[{:.6},{:.6}] to [{:.6},{:.6}]",
               self.min_lat, self.min_lon, self.max_lat, self.max_lon)
    }
}

/// Unit of distance measurement
#[derive(Debug, Clone, Copy, PartialEq)]
pub enum DistanceUnit {
    Kilometers,
    Meters,
    Miles,
    NauticalMiles,
}

impl DistanceUnit {
    /// Get the earth radius for this unit
    pub fn earth_radius(&self) -> f64 {
        match self {
            DistanceUnit::Kilometers => EARTH_RADIUS_KM,
            DistanceUnit::Meters => EARTH_RADIUS_M,
            DistanceUnit::Miles => EARTH_RADIUS_MI,
            DistanceUnit::NauticalMiles => EARTH_RADIUS_NM,
        }
    }

    /// Convert from kilometers to this unit
    pub fn from_km(&self, km: f64) -> f64 {
        match self {
            DistanceUnit::Kilometers => km,
            DistanceUnit::Meters => km * 1000.0,
            DistanceUnit::Miles => km * 0.621371,
            DistanceUnit::NauticalMiles => km * 0.539957,
        }
    }

    /// Convert to kilometers from this unit
    pub fn to_km(&self, value: f64) -> f64 {
        match self {
            DistanceUnit::Kilometers => value,
            DistanceUnit::Meters => value / 1000.0,
            DistanceUnit::Miles => value / 0.621371,
            DistanceUnit::NauticalMiles => value / 0.539957,
        }
    }
}

/// Main geographic utilities
pub struct GeoUtils;

impl GeoUtils {
    /// Calculate the great-circle distance between two points using Haversine formula
    pub fn haversine_distance(from: &Coordinate, to: &Coordinate) -> f64 {
        let (lat1, lon1) = from.to_radians();
        let (lat2, lon2) = to.to_radians();

        let dlat = lat2 - lat1;
        let dlon = lon2 - lon1;

        let a = (dlat / 2.0).sin().powi(2) + lat1.cos() * lat2.cos() * (dlon / 2.0).sin().powi(2);
        let c = 2.0 * a.sqrt().atan2((1.0 - a).sqrt());

        EARTH_RADIUS_KM * c
    }

    /// Calculate distance in specified unit
    pub fn distance(from: &Coordinate, to: &Coordinate, unit: DistanceUnit) -> f64 {
        unit.from_km(Self::haversine_distance(from, to))
    }

    /// Calculate the initial bearing from one point to another
    pub fn bearing(from: &Coordinate, to: &Coordinate) -> f64 {
        let (lat1, lon1) = from.to_radians();
        let (lat2, lon2) = to.to_radians();

        let dlon = lon2 - lon1;
        let y = dlon.sin() * lat2.cos();
        let x = lat1.cos() * lat2.sin() - lat1.sin() * lat2.cos() * dlon.cos();

        let bearing = y.atan2(x).to_degrees();
        (bearing + 360.0) % 360.0
    }

    /// Calculate the final bearing from one point to another
    pub fn final_bearing(from: &Coordinate, to: &Coordinate) -> f64 {
        (Self::bearing(to, from) + 180.0) % 360.0
    }

    /// Calculate the midpoint between two coordinates
    pub fn midpoint(from: &Coordinate, to: &Coordinate) -> Coordinate {
        let (lat1, lon1) = from.to_radians();
        let (lat2, lon2) = to.to_radians();

        let dlon = lon2 - lon1;
        let bx = lat2.cos() * dlon.cos();
        let by = lat2.cos() * dlon.sin();

        let lat3 = (lat1.sin() + lat2.sin()).atan2(((lat1.cos() + bx).powi(2) + by.powi(2)).sqrt());
        let lon3 = lon1 + by.atan2(lat1.cos() + bx);

        Coordinate::new(lat3.to_degrees(), lon3.to_degrees())
    }

    /// Calculate destination point given start point, bearing, and distance
    pub fn destination(from: &Coordinate, bearing: f64, distance_km: f64) -> Coordinate {
        let (lat1, lon1) = from.to_radians();
        let brng = bearing.to_radians();
        let d = distance_km / EARTH_RADIUS_KM;

        let lat2 = (lat1.sin() * d.cos() + lat1.cos() * d.sin() * brng.cos()).asin();
        let lon2 = lon1 + (brng.sin() * d.sin() * lat1.cos()).atan2(d.cos() - lat1.sin() * lat2.sin());

        let lon = lon2.to_degrees();
        let mut lon = lon % 360.0;
        if lon > 180.0 { lon -= 360.0; }
        else if lon < -180.0 { lon += 360.0; }

        Coordinate::new(lat2.to_degrees(), lon)
    }

    /// Generate a bounding box around a center point
    pub fn bounding_box(center: &Coordinate, radius_km: f64) -> BoundingBox {
        let angular_distance = radius_km / EARTH_RADIUS_KM;
        let lat = center.latitude.to_radians();
        let lat_offset = angular_distance;
        let lon_offset = angular_distance / lat.cos().abs().max(1e-10);

        BoundingBox {
            min_lat: (center.latitude - lat_offset.to_degrees()).max(-90.0),
            max_lat: (center.latitude + lat_offset.to_degrees()).min(90.0),
            min_lon: center.longitude - lon_offset.to_degrees(),
            max_lon: center.longitude + lon_offset.to_degrees(),
        }
    }

    /// Encode a coordinate to GeoHash
    pub fn encode_geohash(coord: &Coordinate, precision: usize) -> String {
        let precision = precision.min(12).max(1);
        let mut hash = String::with_capacity(precision);
        
        let mut lat_range = (-90.0, 90.0);
        let mut lon_range = (-180.0, 180.0);
        
        let mut bit = 0;
        let mut ch = 0u8;
        
        while hash.len() < precision {
            if bit % 2 == 0 {
                let mid = (lon_range.0 + lon_range.1) / 2.0;
                if coord.longitude >= mid {
                    ch |= 1 << (4 - (bit % 5));
                    lon_range.0 = mid;
                } else {
                    lon_range.1 = mid;
                }
            } else {
                let mid = (lat_range.0 + lat_range.1) / 2.0;
                if coord.latitude >= mid {
                    ch |= 1 << (4 - (bit % 5));
                    lat_range.0 = mid;
                } else {
                    lat_range.1 = mid;
                }
            }
            
            bit += 1;
            
            if bit % 5 == 0 {
                hash.push(GEOHASH_CHARS[ch as usize] as char);
                ch = 0;
            }
        }
        
        hash
    }

    /// Decode a GeoHash to a coordinate (center of the cell)
    pub fn decode_geohash(geohash: &str) -> Option<Coordinate> {
        if geohash.is_empty() { return None; }

        let reverse = build_geohash_reverse();
        let mut lat_range = (-90.0, 90.0);
        let mut lon_range = (-180.0, 180.0);
        let mut bit = 0;

        for c in geohash.to_lowercase().chars() {
            let idx = reverse[c as usize];
            if idx < 0 { return None; }

            let mut mask = 16u8;
            while mask > 0 {
                if bit % 2 == 0 {
                    let mid = (lon_range.0 + lon_range.1) / 2.0;
                    if (idx as u8) & mask != 0 { lon_range.0 = mid; }
                    else { lon_range.1 = mid; }
                } else {
                    let mid = (lat_range.0 + lat_range.1) / 2.0;
                    if (idx as u8) & mask != 0 { lat_range.0 = mid; }
                    else { lat_range.1 = mid; }
                }
                mask >>= 1;
                bit += 1;
            }
        }

        Some(Coordinate::new(
            (lat_range.0 + lat_range.1) / 2.0,
            (lon_range.0 + lon_range.1) / 2.0,
        ))
    }

    /// Get the bounding box of a GeoHash cell
    pub fn geohash_bounds(geohash: &str) -> Option<BoundingBox> {
        if geohash.is_empty() { return None; }

        let reverse = build_geohash_reverse();
        let mut lat_range = (-90.0, 90.0);
        let mut lon_range = (-180.0, 180.0);
        let mut bit = 0;

        for c in geohash.to_lowercase().chars() {
            let idx = reverse[c as usize];
            if idx < 0 { return None; }

            let mut mask = 16u8;
            while mask > 0 {
                if bit % 2 == 0 {
                    let mid = (lon_range.0 + lon_range.1) / 2.0;
                    if (idx as u8) & mask != 0 { lon_range.0 = mid; }
                    else { lon_range.1 = mid; }
                } else {
                    let mid = (lat_range.0 + lat_range.1) / 2.0;
                    if (idx as u8) & mask != 0 { lat_range.0 = mid; }
                    else { lat_range.1 = mid; }
                }
                mask >>= 1;
                bit += 1;
            }
        }

        Some(BoundingBox::new(lat_range.0, lat_range.1, lon_range.0, lon_range.1))
    }

    /// Get neighboring GeoHash cells
    pub fn geohash_neighbors(geohash: &str) -> Option<[String; 8]> {
        let bounds = Self::geohash_bounds(geohash)?;
        let center = bounds.center();
        let precision = geohash.len();
        let lat_diff = bounds.height();
        let lon_diff = bounds.width();
        
        let neighbors = [
            Coordinate::new(center.latitude + lat_diff, center.longitude),
            Coordinate::new(center.latitude + lat_diff, center.longitude + lon_diff),
            Coordinate::new(center.latitude, center.longitude + lon_diff),
            Coordinate::new(center.latitude - lat_diff, center.longitude + lon_diff),
            Coordinate::new(center.latitude - lat_diff, center.longitude),
            Coordinate::new(center.latitude - lat_diff, center.longitude - lon_diff),
            Coordinate::new(center.latitude, center.longitude - lon_diff),
            Coordinate::new(center.latitude + lat_diff, center.longitude - lon_diff),
        ];

        let result: Vec<String> = neighbors.iter()
            .filter(|n| n.is_valid())
            .map(|n| Self::encode_geohash(n, precision))
            .collect();

        if result.len() == 8 {
            Some(result.try_into().unwrap())
        } else {
            None
        }
    }

    /// Check if a point is inside a polygon (ray casting algorithm)
    pub fn point_in_polygon(point: &Coordinate, polygon: &[Coordinate]) -> bool {
        if polygon.len() < 3 { return false; }

        let mut inside = false;
        let mut j = polygon.len() - 1;

        for i in 0..polygon.len() {
            let pi = &polygon[i];
            let pj = &polygon[j];

            if ((pi.latitude > point.latitude) != (pj.latitude > point.latitude)) &&
               (point.longitude < (pj.longitude - pi.longitude) * (point.latitude - pi.latitude) /
                (pj.latitude - pi.latitude) + pi.longitude) {
                inside = !inside;
            }
            j = i;
        }

        inside
    }

    /// Calculate the area of a polygon in square kilometers
    pub fn polygon_area(polygon: &[Coordinate]) -> f64 {
        if polygon.len() < 3 { return 0.0; }

        let mut area = 0.0;
        let n = polygon.len();

        for i in 0..n {
            let j = (i + 1) % n;
            let lat_i = polygon[i].latitude.to_radians();
            let lat_j = polygon[j].latitude.to_radians();
            let lon_i = polygon[i].longitude.to_radians();
            let lon_j = polygon[j].longitude.to_radians();

            area += (lon_j - lon_i) * (2.0 + lat_i.sin() + lat_j.sin());
        }

        area.abs() * EARTH_RADIUS_KM.powi(2) / 2.0
    }

    /// Calculate the perimeter of a polygon in kilometers
    pub fn polygon_perimeter(polygon: &[Coordinate]) -> f64 {
        if polygon.len() < 2 { return 0.0; }

        let mut perimeter = 0.0;
        for i in 0..polygon.len() {
            let j = (i + 1) % polygon.len();
            perimeter += Self::haversine_distance(&polygon[i], &polygon[j]);
        }
        perimeter
    }

    /// Calculate the centroid of a polygon
    pub fn polygon_centroid(polygon: &[Coordinate]) -> Option<Coordinate> {
        if polygon.is_empty() { return None; }

        let sum_lat: f64 = polygon.iter().map(|c| c.latitude).sum();
        let sum_lon: f64 = polygon.iter().map(|c| c.longitude).sum();
        let n = polygon.len() as f64;

        Some(Coordinate::new(sum_lat / n, sum_lon / n))
    }

    /// Interpolate points along a great circle path
    pub fn interpolate(from: &Coordinate, to: &Coordinate, num_points: usize) -> Vec<Coordinate> {
        if num_points == 0 { return vec![]; }

        let (lat1, lon1) = from.to_radians();
        let (lat2, lon2) = to.to_radians();
        let d = Self::haversine_distance(from, to) / EARTH_RADIUS_KM;

        if d.abs() < 1e-10 { return vec![*from; num_points]; }

        let mut points = Vec::with_capacity(num_points);
        
        for i in 0..num_points {
            let f = (i + 1) as f64 / (num_points + 1) as f64;
            let a = ((1.0 - f) * d).sin() / d.sin();
            let b = (f * d).sin() / d.sin();

            let x = a * lat1.cos() * lon1.cos() + b * lat2.cos() * lon2.cos();
            let y = a * lat1.cos() * lon1.sin() + b * lat2.cos() * lon2.sin();
            let z = a * lat1.sin() + b * lat2.sin();

            let lat = z.atan2((x * x + y * y).sqrt()).to_degrees();
            let mut lon = y.atan2(x).to_degrees();
            lon = lon % 360.0;
            if lon > 180.0 { lon -= 360.0; }
            else if lon < -180.0 { lon += 360.0; }

            points.push(Coordinate::new(lat, lon));
        }

        points
    }

    /// Calculate the total distance along a path
    pub fn path_distance(path: &[Coordinate]) -> f64 {
        if path.len() < 2 { return 0.0; }
        path.windows(2).map(|w| Self::haversine_distance(&w[0], &w[1])).sum()
    }

    /// Check if two bounding boxes intersect
    pub fn bounding_boxes_intersect(a: &BoundingBox, b: &BoundingBox) -> bool {
        a.min_lat <= b.max_lat && a.max_lat >= b.min_lat &&
        a.min_lon <= b.max_lon && a.max_lon >= b.min_lon
    }

    /// Calculate rhumb line bearing
    pub fn rhumb_bearing(from: &Coordinate, to: &Coordinate) -> f64 {
        let (lat1, lon1) = from.to_radians();
        let (lat2, lon2) = to.to_radians();

        let dlon = lon2 - lon1;
        let dphi = (lat2.tan() / lat1.tan()).ln();
        
        let bearing = dlon.atan2(dphi).to_degrees();
        (bearing + 360.0) % 360.0
    }

    /// Calculate rhumb line distance
    pub fn rhumb_distance(from: &Coordinate, to: &Coordinate) -> f64 {
        let (lat1, lon1) = from.to_radians();
        let (lat2, lon2) = to.to_radians();

        let dphi = (lat2.tan() / lat1.tan()).ln();
        let mut dlon = (lon2 - lon1).abs();

        if dlon > PI { dlon = 2.0 * PI - dlon; }

        let q = if dphi.abs() < 1e-10 { lat1.cos() }
                else { (lat2 - lat1) / dphi };

        let delta = (dphi.powi(2) + (q * dlon).powi(2)).sqrt();
        delta * EARTH_RADIUS_KM
    }

    /// Get cardinal direction from bearing
    pub fn bearing_to_cardinal(bearing: f64) -> &'static str {
        let directions = [
            "N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
            "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW",
        ];
        let index = ((bearing + 11.25) / 22.5).floor() as usize % 16;
        directions[index]
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn approx_eq(a: f64, b: f64, eps: f64) -> bool { (a - b).abs() < eps }

    #[test]
    fn test_coordinate_creation() {
        let coord = Coordinate::new(40.7128, -74.0060);
        assert!(approx_eq(coord.latitude, 40.7128, 0.001));
        assert!(approx_eq(coord.longitude, -74.006, 0.001));
    }

    #[test]
    fn test_coordinate_validation() {
        assert!(Coordinate::new(0.0, 0.0).is_valid());
        assert!(Coordinate::new(90.0, 180.0).is_valid());
        assert!(!Coordinate::new(91.0, 0.0).is_valid());
    }

    #[test]
    fn test_haversine_distance() {
        let ny = Coordinate::new(40.7128, -74.0060);
        let london = Coordinate::new(51.5074, -0.1278);
        let distance = GeoUtils::haversine_distance(&ny, &london);
        assert!(approx_eq(distance, 5570.0, 10.0));
    }

    #[test]
    fn test_bearing() {
        let ny = Coordinate::new(40.7128, -74.0060);
        let london = Coordinate::new(51.5074, -0.1278);
        let bearing = GeoUtils::bearing(&ny, &london);
        assert!(approx_eq(bearing, 52.0, 5.0));
    }

    #[test]
    fn test_midpoint() {
        let ny = Coordinate::new(40.7128, -74.0060);
        let london = Coordinate::new(51.5074, -0.1278);
        let mid = GeoUtils::midpoint(&ny, &london);
        assert!(mid.latitude > 40.0 && mid.latitude < 55.0);
        assert!(mid.longitude > -50.0 && mid.longitude < -10.0);
    }

    #[test]
    fn test_destination() {
        let ny = Coordinate::new(40.7128, -74.0060);
        let dest = GeoUtils::destination(&ny, 52.0, 1000.0);
        assert!(dest.latitude > ny.latitude);
    }

    #[test]
    fn test_geohash_encode() {
        let ny = Coordinate::new(40.7128, -74.0060);
        let hash = GeoUtils::encode_geohash(&ny, 8);
        assert!(hash.starts_with("dr5"));
    }

    #[test]
    fn test_geohash_roundtrip() {
        let coord = Coordinate::new(37.7749, -122.4194);
        let hash = GeoUtils::encode_geohash(&coord, 10);
        let decoded = GeoUtils::decode_geohash(&hash).unwrap();
        assert!(approx_eq(decoded.latitude, coord.latitude, 0.0001));
        assert!(approx_eq(decoded.longitude, coord.longitude, 0.0001));
    }

    #[test]
    fn test_point_in_polygon() {
        let polygon = vec![
            Coordinate::new(0.0, 0.0),
            Coordinate::new(0.0, 10.0),
            Coordinate::new(10.0, 10.0),
            Coordinate::new(10.0, 0.0),
        ];
        assert!(GeoUtils::point_in_polygon(&Coordinate::new(5.0, 5.0), &polygon));
        assert!(!GeoUtils::point_in_polygon(&Coordinate::new(15.0, 5.0), &polygon));
    }

    #[test]
    fn test_bearing_to_cardinal() {
        assert_eq!(GeoUtils::bearing_to_cardinal(0.0), "N");
        assert_eq!(GeoUtils::bearing_to_cardinal(90.0), "E");
        assert_eq!(GeoUtils::bearing_to_cardinal(180.0), "S");
        assert_eq!(GeoUtils::bearing_to_cardinal(270.0), "W");
    }

    #[test]
    fn test_bounding_box() {
        let center = Coordinate::new(40.0, -100.0);
        let bbox = GeoUtils::bounding_box(&center, 100.0);
        assert!(bbox.contains(&center));
    }

    #[test]
    fn test_polygon_area() {
        let polygon = vec![
            Coordinate::new(0.0, 0.0),
            Coordinate::new(0.0, 1.0),
            Coordinate::new(1.0, 1.0),
            Coordinate::new(1.0, 0.0),
        ];
        let area = GeoUtils::polygon_area(&polygon);
        assert!(area > 10000.0 && area < 15000.0);
    }

    #[test]
    fn test_distance_units() {
        let ny = Coordinate::new(40.7128, -74.0060);
        let london = Coordinate::new(51.5074, -0.1278);
        let km = GeoUtils::distance(&ny, &london, DistanceUnit::Kilometers);
        let mi = GeoUtils::distance(&ny, &london, DistanceUnit::Miles);
        assert!(approx_eq(mi, km * 0.621371, 5.0));
    }
}