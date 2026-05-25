/**
 * CoordinateUtils - Geographic coordinate utilities
 * 
 * Provides utilities for working with geographic coordinates including:
 * - Distance calculation (Haversine formula)
 * - Bearing calculation
 * - Midpoint calculation
 * - Destination point calculation
 * - Bounding box generation
 * - Coordinate parsing and formatting
 * 
 * Zero external dependencies - pure Kotlin implementation
 */

package coordinate_utils

import kotlin.math.*

/**
 * Represents a geographic coordinate (latitude, longitude)
 */
data class Coordinate(
    val latitude: Double,
    val longitude: Double
) {
    init {
        require(latitude in -90.0..90.0) { "Latitude must be between -90 and 90 degrees" }
        require(longitude in -180.0..180.0) { "Longitude must be between -180 and 180 degrees" }
    }
    
    /**
     * Format as DMS (Degrees Minutes Seconds)
     */
    fun toDMS(): String {
        val latDir = if (latitude >= 0) "N" else "S"
        val lonDir = if (longitude >= 0) "E" else "W"
        
        val latDMS = decimalToDMS(abs(latitude))
        val lonDMS = decimalToDMS(abs(longitude))
        
        return "${latDMS}$latDir, ${lonDMS}$lonDir"
    }
    
    private fun decimalToDMS(decimal: Double): String {
        val degrees = decimal.toInt()
        val minutes = ((decimal - degrees) * 60).toInt()
        val seconds = ((decimal - degrees - minutes / 60.0) * 3600)
        return "$degrees°$minutes'${seconds.format(2)}\""
    }
    
    private fun Double.format(digits: Int) = "%.${digits}f".format(this)
    
    override fun toString(): String = "($latitude, $longitude)"
}

/**
 * Represents a bounding box defined by northeast and southwest corners
 */
data class BoundingBox(
    val northEast: Coordinate,
    val southWest: Coordinate
) {
    val north: Double get() = northEast.latitude
    val south: Double get() = southWest.latitude
    val east: Double get() = northEast.longitude
    val west: Double get() = southWest.longitude
    
    fun contains(point: Coordinate): Boolean {
        return point.latitude in south..north &&
               point.longitude in west..east
    }
    
    override fun toString(): String = "BoundingBox[SW=$southWest, NE=$northEast]"
}

/**
 * Earth radius in kilometers
 */
val EARTH_RADIUS_KM = 6371.0

/**
 * Earth radius in meters
 */
val EARTH_RADIUS_M = 6371000.0

/**
 * Earth radius in miles
 */
val EARTH_RADIUS_MI = 3958.8

/**
 * Convert degrees to radians
 */
fun Double.toRadians(): Double = this * PI / 180.0

/**
 * Convert radians to degrees
 */
fun Double.toDegrees(): Double = this * 180.0 / PI

/**
 * Calculate the distance between two coordinates using the Haversine formula
 * 
 * @param from Starting coordinate
 * @param to Ending coordinate
 * @param radius Earth radius to use (default: kilometers)
 * @return Distance in the same unit as the radius
 */
fun distance(from: Coordinate, to: Coordinate, radius: Double = EARTH_RADIUS_KM): Double {
    val lat1 = from.latitude.toRadians()
    val lat2 = to.latitude.toRadians()
    val deltaLat = (to.latitude - from.latitude).toRadians()
    val deltaLon = (to.longitude - from.longitude).toRadians()
    
    val a = sin(deltaLat / 2).pow(2) +
            cos(lat1) * cos(lat2) * sin(deltaLon / 2).pow(2)
    val c = 2 * atan2(sqrt(a), sqrt(1 - a))
    
    return radius * c
}

/**
 * Calculate the distance between two coordinates in kilometers
 */
fun distanceInKm(from: Coordinate, to: Coordinate): Double = 
    distance(from, to, EARTH_RADIUS_KM)

/**
 * Calculate the distance between two coordinates in meters
 */
fun distanceInMeters(from: Coordinate, to: Coordinate): Double = 
    distance(from, to, EARTH_RADIUS_M)

/**
 * Calculate the distance between two coordinates in miles
 */
fun distanceInMiles(from: Coordinate, to: Coordinate): Double = 
    distance(from, to, EARTH_RADIUS_MI)

/**
 * Calculate the initial bearing from one point to another
 * 
 * @param from Starting coordinate
 * @param to Ending coordinate
 * @return Bearing in degrees (0-360)
 */
fun bearing(from: Coordinate, to: Coordinate): Double {
    val lat1 = from.latitude.toRadians()
    val lat2 = to.latitude.toRadians()
    val deltaLon = (to.longitude - from.longitude).toRadians()
    
    val y = sin(deltaLon) * cos(lat2)
    val x = cos(lat1) * sin(lat2) - sin(lat1) * cos(lat2) * cos(deltaLon)
    
    val bearing = atan2(y, x).toDegrees()
    
    return (bearing + 360) % 360
}

/**
 * Calculate the final bearing (reverse bearing) from one point to another
 */
fun finalBearing(from: Coordinate, to: Coordinate): Double {
    return (bearing(to, from) + 180) % 360
}

/**
 * Calculate the midpoint between two coordinates
 * 
 * @param from Starting coordinate
 * @param to Ending coordinate
 * @return Midpoint coordinate
 */
fun midpoint(from: Coordinate, to: Coordinate): Coordinate {
    val lat1 = from.latitude.toRadians()
    val lat2 = to.latitude.toRadians()
    val lon1 = from.longitude.toRadians()
    val deltaLon = (to.longitude - from.longitude).toRadians()
    
    val bx = cos(lat2) * cos(deltaLon)
    val by = cos(lat2) * sin(deltaLon)
    
    val lat3 = atan2(
        sin(lat1) + sin(lat2),
        sqrt((cos(lat1) + bx).pow(2) + by.pow(2))
    )
    val lon3 = lon1 + atan2(by, cos(lat1) + bx)
    
    return Coordinate(lat3.toDegrees(), lon3.toDegrees().normalizeLongitude())
}

/**
 * Calculate a destination point given starting point, bearing, and distance
 * 
 * @param from Starting coordinate
 * @param bearing Bearing in degrees
 * @param distance Distance in kilometers
 * @param radius Earth radius (default: kilometers)
 * @return Destination coordinate
 */
fun destination(from: Coordinate, bearing: Double, distance: Double, radius: Double = EARTH_RADIUS_KM): Coordinate {
    val lat1 = from.latitude.toRadians()
    val lon1 = from.longitude.toRadians()
    val brng = bearing.toRadians()
    val d = distance / radius
    
    val lat2 = asin(
        sin(lat1) * cos(d) + cos(lat1) * sin(d) * cos(brng)
    )
    val lon2 = lon1 + atan2(
        sin(brng) * sin(d) * cos(lat1),
        cos(d) - sin(lat1) * sin(lat2)
    )
    
    return Coordinate(lat2.toDegrees(), lon2.toDegrees().normalizeLongitude())
}

/**
 * Generate a bounding box around a center point
 * 
 * @param center Center coordinate
 * @param distance Distance in kilometers
 * @return BoundingBox enclosing the area
 */
fun boundingBox(center: Coordinate, distance: Double): BoundingBox {
    val north = destination(center, 0.0, distance)
    val south = destination(center, 180.0, distance)
    val east = destination(center, 90.0, distance)
    val west = destination(center, 270.0, distance)
    
    return BoundingBox(
        northEast = Coordinate(north.latitude, east.longitude),
        southWest = Coordinate(south.latitude, west.longitude)
    )
}

/**
 * Normalize longitude to range [-180, 180]
 */
fun Double.normalizeLongitude(): Double {
    var lon = this
    while (lon > 180) lon -= 360
    while (lon < -180) lon += 360
    return lon
}

/**
 * Normalize latitude to range [-90, 90]
 */
fun Double.normalizeLatitude(): Double {
    return this.coerceIn(-90.0, 90.0)
}

/**
 * Parse a coordinate from string in various formats
 * Supported formats:
 * - "lat, lon" or "lat,lon"
 * - "lat lon"
 * - "(lat, lon)"
 * - "lat° lon°"
 * - DMS format: "N40°26'46\" W79°58'56\""
 */
fun parseCoordinate(input: String): Coordinate {
    val cleaned = input.trim()
        .replace("°", " ")
        .replace("'", " ")
        .replace("\"", " ")
        .replace(",", " ")
        .replace("(", "")
        .replace(")", "")
        .trim()
    
    // Check for DMS format with N/S/E/W
    val dmsPattern = Regex(
        """([NS])?\s*(\d+)\s+(\d+)\s+(\d+\.?\d*)\s*([NS])?\s*([EW])?\s*(\d+)\s+(\d+)\s+(\d+\.?\d*)\s*([EW])?""",
        RegexOption.IGNORE_CASE
    )
    
    dmsPattern.find(cleaned)?.let { match ->
        val latDir = (match.groupValues[1].ifEmpty { match.groupValues[5] }).uppercase()
        val latDeg = match.groupValues[2].toDouble()
        val latMin = match.groupValues[3].toDouble()
        val latSec = match.groupValues[4].toDouble()
        
        val lonDir = (match.groupValues[6].ifEmpty { match.groupValues[10] }).uppercase()
        val lonDeg = match.groupValues[7].toDouble()
        val lonMin = match.groupValues[8].toDouble()
        val lonSec = match.groupValues[9].toDouble()
        
        var lat = dmsToDecimal(latDeg, latMin, latSec)
        var lon = dmsToDecimal(lonDeg, lonMin, lonSec)
        
        if (latDir == "S") lat = -lat
        if (lonDir == "W") lon = -lon
        
        return Coordinate(lat, lon)
    }
    
    // Simple decimal format
    val parts = cleaned.split(Regex("\\s+")).filter { it.isNotBlank() }
    if (parts.size >= 2) {
        val lat = parts[0].toDoubleOrNull() 
            ?: throw IllegalArgumentException("Invalid latitude: ${parts[0]}")
        val lon = parts[1].toDoubleOrNull()
            ?: throw IllegalArgumentException("Invalid longitude: ${parts[1]}")
        return Coordinate(lat, lon)
    }
    
    throw IllegalArgumentException("Cannot parse coordinate: $input")
}

/**
 * Convert DMS (Degrees Minutes Seconds) to decimal degrees
 */
fun dmsToDecimal(degrees: Double, minutes: Double, seconds: Double): Double {
    return degrees + minutes / 60 + seconds / 3600
}

/**
 * Convert decimal degrees to DMS components
 */
fun decimalToDms(decimal: Double): Triple<Int, Int, Double> {
    val absDecimal = abs(decimal)
    val degrees = absDecimal.toInt()
    val minutes = ((absDecimal - degrees) * 60).toInt()
    val seconds = (absDecimal - degrees - minutes / 60.0) * 3600
    return Triple(degrees, minutes, seconds)
}

/**
 * Check if a point is within a polygon using ray casting algorithm
 * 
 * @param point Point to check
 * @param polygon List of vertices forming the polygon (closed or open)
 * @return true if point is inside the polygon
 */
fun isInsidePolygon(point: Coordinate, polygon: List<Coordinate>): Boolean {
    if (polygon.size < 3) return false
    
    var inside = false
    var j = polygon.lastIndex
    
    for (i in polygon.indices) {
        val pi = polygon[i]
        val pj = polygon[j]
        
        if ((pi.latitude > point.latitude) != (pj.latitude > point.latitude) &&
            point.longitude < (pj.longitude - pi.longitude) * (point.latitude - pi.latitude) / 
            (pj.latitude - pi.latitude) + pi.longitude) {
            inside = !inside
        }
        j = i
    }
    
    return inside
}

/**
 * Calculate the area of a polygon on Earth's surface (in square kilometers)
 * Uses the Shoelace formula with spherical correction
 * 
 * @param polygon List of vertices forming a closed polygon
 * @return Area in square kilometers
 */
fun polygonArea(polygon: List<Coordinate>): Double {
    if (polygon.size < 3) return 0.0
    
    var area = 0.0
    var j = polygon.lastIndex
    
    for (i in polygon.indices) {
        val pi = polygon[i]
        val pj = polygon[j]
        
        area += (pj.longitude.toRadians() - pi.longitude.toRadians()) *
                (2 + sin(pi.latitude.toRadians()) + sin(pj.latitude.toRadians()))
        j = i
    }
    
    area = abs(area * EARTH_RADIUS_KM.pow(2) / 2)
    return area
}

/**
 * Interpolate points along a great circle path
 * 
 * @param from Starting coordinate
 * @param to Ending coordinate
 * @param numPoints Number of points to generate (excluding endpoints)
 * @return List of interpolated coordinates
 */
fun interpolatePath(from: Coordinate, to: Coordinate, numPoints: Int): List<Coordinate> {
    if (numPoints <= 0) return emptyList()
    
    val totalDistance = distanceInKm(from, to)
    val brng = bearing(from, to)
    val step = totalDistance / (numPoints + 1)
    
    return (1..numPoints).map { i ->
        destination(from, brng, step * i)
    }
}

/**
 * Calculate the centroid (geometric center) of a polygon
 * 
 * @param polygon List of vertices
 * @return Centroid coordinate
 */
fun centroid(polygon: List<Coordinate>): Coordinate {
    if (polygon.isEmpty()) throw IllegalArgumentException("Polygon cannot be empty")
    
    var sumLat = 0.0
    var sumLon = 0.0
    
    polygon.forEach { point ->
        sumLat += point.latitude
        sumLon += point.longitude
    }
    
    return Coordinate(
        sumLat / polygon.size,
        sumLon / polygon.size
    )
}

/**
 * Calculate the perimeter of a polygon (in kilometers)
 * 
 * @param polygon List of vertices
 * @return Perimeter in kilometers
 */
fun perimeter(polygon: List<Coordinate>): Double {
    if (polygon.size < 2) return 0.0
    
    var totalDistance = 0.0
    for (i in 0 until polygon.size - 1) {
        totalDistance += distanceInKm(polygon[i], polygon[i + 1])
    }
    // Close the polygon
    totalDistance += distanceInKm(polygon.last(), polygon.first())
    
    return totalDistance
}

/**
 * Find the closest point among a list of candidates
 * 
 * @param target Target coordinate
 * @param candidates List of candidate coordinates
 * @return Pair of (closest coordinate, distance in km)
 */
fun findClosest(target: Coordinate, candidates: List<Coordinate>): Pair<Coordinate, Double>? {
    if (candidates.isEmpty()) return null
    
    return candidates
        .map { it to distanceInKm(target, it) }
        .minByOrNull { it.second }
}

/**
 * Convert between coordinate reference systems (simple WGS84 approximation)
 * Note: This is a simplified conversion; for precise transformations, use a proper geodesy library
 */
object CoordinateSystems {
    /**
     * Convert WGS84 latitude/longitude to UTM
     * Simplified approximation - for precise conversion use proj4j or similar
     */
    fun wgs84ToUtm(coord: Coordinate): Triple<Int, Double, Double> {
        val zone = floor((coord.longitude + 180) / 6).toInt() + 1
        val centralMeridian = (zone - 1) * 6 - 180 + 3
        
        val k0 = 0.9996
        val a = 6378137.0 // WGS84 semi-major axis
        val e = 0.081819191 // eccentricity
        
        val lat = coord.latitude * PI / 180.0
        val lon = coord.longitude * PI / 180.0
        val lon0 = centralMeridian * PI / 180.0
        
        val N = a / sqrt(1 - e.pow(2) * sin(lat).pow(2))
        val T = tan(lat).pow(2)
        val C = e.pow(2) * cos(lat).pow(2) / (1 - e.pow(2))
        val A = (lon - lon0) * cos(lat)
        
        val M = a * ((1 - e.pow(2) / 4 - 3 * e.pow(4) / 64) * lat
                - (3 * e.pow(2) / 8 + 3 * e.pow(4) / 32) * sin(2 * lat)
                + (15 * e.pow(4) / 256) * sin(4 * lat))
        
        val easting = k0 * N * (A + (1 - T + C) * A.pow(3) / 6) + 500000
        val northing = k0 * (M + N * tan(lat) * (A.pow(2) / 2 + (5 - T + 9 * C + 4 * C.pow(2)) * A.pow(4) / 24))
        
        return Triple(zone, easting, if (coord.latitude < 0) northing + 10000000 else northing)
    }
    
    /**
     * Determine UTM zone for a longitude
     */
    fun utmZone(longitude: Double): Int = floor((longitude + 180) / 6).toInt() + 1
    
    /**
     * Determine UTM hemisphere
     */
    fun utmHemisphere(latitude: Double): String = if (latitude >= 0) "N" else "S"
}