/**
 * CoordinateUtils - Geographic coordinate utilities
 * Combined module + tests for standalone execution
 * 
 * Run with: kotlinc -script CoordinateUtilsAll.kts
 */

import kotlin.math.*

// ============== MODULE CODE ==============

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

data class BoundingBox(
    val northEast: Coordinate,
    val southWest: Coordinate
) {
    val north: Double get() = northEast.latitude
    val south: Double get() = southWest.latitude
    val east: Double get() = northEast.longitude
    val west: Double get() = southWest.longitude
    
    fun contains(point: Coordinate): Boolean {
        return point.latitude in south..north && point.longitude in west..east
    }
}

val EARTH_RADIUS_KM = 6371.0
val EARTH_RADIUS_M = 6371000.0
val EARTH_RADIUS_MI = 3958.8

fun Double.toRadians(): Double = this * PI / 180.0
fun Double.toDegrees(): Double = this * 180.0 / PI

fun distance(from: Coordinate, to: Coordinate, radius: Double = EARTH_RADIUS_KM): Double {
    val lat1 = from.latitude.toRadians()
    val lat2 = to.latitude.toRadians()
    val deltaLat = (to.latitude - from.latitude).toRadians()
    val deltaLon = (to.longitude - from.longitude).toRadians()
    
    val a = sin(deltaLat / 2).pow(2) + cos(lat1) * cos(lat2) * sin(deltaLon / 2).pow(2)
    val c = 2 * atan2(sqrt(a), sqrt(1 - a))
    
    return radius * c
}

fun distanceInKm(from: Coordinate, to: Coordinate): Double = distance(from, to, EARTH_RADIUS_KM)
fun distanceInMeters(from: Coordinate, to: Coordinate): Double = distance(from, to, EARTH_RADIUS_M)
fun distanceInMiles(from: Coordinate, to: Coordinate): Double = distance(from, to, EARTH_RADIUS_MI)

fun bearing(from: Coordinate, to: Coordinate): Double {
    val lat1 = from.latitude.toRadians()
    val lat2 = to.latitude.toRadians()
    val deltaLon = (to.longitude - from.longitude).toRadians()
    
    val y = sin(deltaLon) * cos(lat2)
    val x = cos(lat1) * sin(lat2) - sin(lat1) * cos(lat2) * cos(deltaLon)
    
    val bearing = atan2(y, x).toDegrees()
    return (bearing + 360) % 360
}

fun finalBearing(from: Coordinate, to: Coordinate): Double = (bearing(to, from) + 180) % 360

fun midpoint(from: Coordinate, to: Coordinate): Coordinate {
    val lat1 = from.latitude.toRadians()
    val lat2 = to.latitude.toRadians()
    val lon1 = from.longitude.toRadians()
    val deltaLon = (to.longitude - from.longitude).toRadians()
    
    val bx = cos(lat2) * cos(deltaLon)
    val by = cos(lat2) * sin(deltaLon)
    
    val lat3 = atan2(sin(lat1) + sin(lat2), sqrt((cos(lat1) + bx).pow(2) + by.pow(2)))
    val lon3 = lon1 + atan2(by, cos(lat1) + bx)
    
    return Coordinate(lat3.toDegrees(), lon3.toDegrees().normalizeLongitude())
}

fun destination(from: Coordinate, bearing: Double, distance: Double, radius: Double = EARTH_RADIUS_KM): Coordinate {
    val lat1 = from.latitude.toRadians()
    val lon1 = from.longitude.toRadians()
    val brng = bearing.toRadians()
    val d = distance / radius
    
    val lat2 = asin(sin(lat1) * cos(d) + cos(lat1) * sin(d) * cos(brng))
    val lon2 = lon1 + atan2(sin(brng) * sin(d) * cos(lat1), cos(d) - sin(lat1) * sin(lat2))
    
    return Coordinate(lat2.toDegrees(), lon2.toDegrees().normalizeLongitude())
}

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

fun Double.normalizeLongitude(): Double {
    var lon = this
    while (lon > 180) lon -= 360
    while (lon < -180) lon += 360
    return lon
}

fun parseCoordinate(input: String): Coordinate {
    val cleaned = input.trim()
        .replace("°", " ").replace("'", " ").replace("\"", " ")
        .replace(",", " ").replace("(", "").replace(")", "").trim()
    
    val parts = cleaned.split(Regex("\\s+")).filter { it.isNotBlank() }
    if (parts.size >= 2) {
        val lat = parts[0].toDoubleOrNull() ?: throw IllegalArgumentException("Invalid latitude: ${parts[0]}")
        val lon = parts[1].toDoubleOrNull() ?: throw IllegalArgumentException("Invalid longitude: ${parts[1]}")
        return Coordinate(lat, lon)
    }
    throw IllegalArgumentException("Cannot parse coordinate: $input")
}

fun dmsToDecimal(degrees: Double, minutes: Double, seconds: Double): Double = 
    degrees + minutes / 60 + seconds / 3600

fun decimalToDms(decimal: Double): Triple<Int, Int, Double> {
    val absDecimal = abs(decimal)
    val degrees = absDecimal.toInt()
    val minutes = ((absDecimal - degrees) * 60).toInt()
    val seconds = (absDecimal - degrees - minutes / 60.0) * 3600
    return Triple(degrees, minutes, seconds)
}

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
    return abs(area * EARTH_RADIUS_KM.pow(2) / 2)
}

fun interpolatePath(from: Coordinate, to: Coordinate, numPoints: Int): List<Coordinate> {
    if (numPoints <= 0) return emptyList()
    val totalDistance = distanceInKm(from, to)
    val brng = bearing(from, to)
    val step = totalDistance / (numPoints + 1)
    return (1..numPoints).map { i -> destination(from, brng, step * i) }
}

fun centroid(polygon: List<Coordinate>): Coordinate {
    if (polygon.isEmpty()) throw IllegalArgumentException("Polygon cannot be empty")
    var sumLat = 0.0
    var sumLon = 0.0
    polygon.forEach { point -> sumLat += point.latitude; sumLon += point.longitude }
    return Coordinate(sumLat / polygon.size, sumLon / polygon.size)
}

fun perimeter(polygon: List<Coordinate>): Double {
    if (polygon.size < 2) return 0.0
    var totalDistance = 0.0
    for (i in 0 until polygon.size - 1) totalDistance += distanceInKm(polygon[i], polygon[i + 1])
    totalDistance += distanceInKm(polygon.last(), polygon.first())
    return totalDistance
}

fun findClosest(target: Coordinate, candidates: List<Coordinate>): Pair<Coordinate, Double>? {
    if (candidates.isEmpty()) return null
    return candidates.map { it to distanceInKm(target, it) }.minByOrNull { it.second }
}

object CoordinateSystems {
    fun utmZone(longitude: Double): Int = floor((longitude + 180) / 6).toInt() + 1
    fun utmHemisphere(latitude: Double): String = if (latitude >= 0) "N" else "S"
    
    fun wgs84ToUtm(coord: Coordinate): Triple<Int, Double, Double> {
        val zone = utmZone(coord.longitude)
        val centralMeridian = (zone - 1) * 6 - 180 + 3
        
        val k0 = 0.9996
        val a = 6378137.0
        val e = 0.081819191
        
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
}

// ============== TEST CODE ==============

fun assertEquals(expected: Any?, actual: Any?, msg: String = "") {
    if (expected != actual) throw AssertionError("$msg Expected: $expected, Actual: $actual")
}

fun assertEqualsD(expected: Double, actual: Double, delta: Double, msg: String = "") {
    if (abs(expected - actual) > delta) throw AssertionError("$msg Expected: $expected ±$delta, Actual: $actual")
}

fun assertTrue(cond: Boolean, msg: String = "") {
    if (!cond) throw AssertionError(msg.ifEmpty { "Condition was false" })
}

fun assertFalse(cond: Boolean, msg: String = "") {
    if (cond) throw AssertionError(msg.ifEmpty { "Condition was true" })
}

fun assertFails(msg: String = "", block: () -> Unit) {
    try { block(); throw AssertionError(msg.ifEmpty { "Expected exception" }) } catch (e: Exception) {}
}

fun runTests() {
    println("=" .repeat(60))
    println("CoordinateUtils Tests")
    println("=".repeat(60))
    
    var passed = 0
    var failed = 0
    
    fun test(name: String, block: () -> Unit) {
        try { block(); passed++; println("  ✓ $name") }
        catch (e: Exception) { failed++; println("  ✗ $name: ${e.message}") }
    }
    
    val newYork = Coordinate(40.7128, -74.0060)
    val london = Coordinate(51.5074, -0.1278)
    val tokyo = Coordinate(35.6762, 139.6503)
    val sydney = Coordinate(-33.8688, 151.2093)
    val beijing = Coordinate(39.9042, 116.4074)
    val paris = Coordinate(48.8566, 2.3522)
    
    println("\n--- Coordinate Creation & Validation ---")
    test("Coordinate creation") {
        val c = Coordinate(45.0, -90.0)
        assertEquals(45.0, c.latitude)
        assertEquals(-90.0, c.longitude)
    }
    test("Valid range extremes") { Coordinate(90.0, 180.0); Coordinate(-90.0, -180.0) }
    test("Invalid latitude high") { assertFails { Coordinate(91.0, 0.0) } }
    test("Invalid latitude low") { assertFails { Coordinate(-91.0, 0.0) } }
    test("Invalid longitude high") { assertFails { Coordinate(0.0, 181.0) } }
    test("Invalid longitude low") { assertFails { Coordinate(0.0, -181.0) } }
    
    println("\n--- Distance Calculations ---")
    test("NY to London (~5570 km)") {
        val d = distanceInKm(newYork, london)
        assertTrue(d in 5550.0..5590.0, "Got $d")
    }
    test("NY to Tokyo (~10870 km)") {
        val d = distanceInKm(newYork, tokyo)
        assertTrue(d in 10850.0..10890.0, "Got $d")
    }
    test("Different unit conversions") {
        val km = distanceInKm(newYork, london)
        val m = distanceInMeters(newYork, london)
        val mi = distanceInMiles(newYork, london)
        assertEqualsD(km * 1000, m, 1.0)
        assertEqualsD(km * 0.621371, mi, 10.0)
    }
    test("Paris to London (~344 km)") {
        val d = distanceInKm(paris, london)
        assertTrue(d in 340.0..350.0, "Got $d")
    }
    test("Beijing to Tokyo (~2100 km)") {
        val d = distanceInKm(beijing, tokyo)
        assertTrue(d in 2080.0..2110.0, "Got $d")
    }
    test("Same point = 0") { assertEqualsD(0.0, distanceInKm(newYork, newYork), 0.001) }
    test("Antipodal points > 19000 km") {
        val d = distanceInKm(Coordinate(0.0, 0.0), Coordinate(0.0, 180.0))
        assertTrue(d > 19000.0, "Got $d")
    }
    
    println("\n--- Bearing ---")
    test("NY to London bearing ~52°") {
        val b = bearing(newYork, london)
        assertTrue(b in 50.0..55.0, "Got $b")
    }
    test("NY to Sydney bearing ~266°") {
        val b = bearing(newYork, sydney)
        assertTrue(b in 260.0..270.0, "Got $b")
    }
    
    println("\n--- Midpoint & Destination ---")
    test("Midpoint NY-London") {
        val m = midpoint(newYork, london)
        assertTrue(m.latitude in 52.0..53.0, "Lat ${m.latitude}")
        assertTrue(m.longitude in -42.0..-40.0, "Lon ${m.longitude}")
    }
    test("Destination 100km NE") {
        val dest = destination(newYork, 45.0, 100.0)
        assertTrue(dest.latitude > newYork.latitude)
        assertTrue(dest.longitude > newYork.longitude)
        assertEqualsD(100.0, distanceInKm(newYork, dest), 1.0)
    }
    test("Round trip") {
        val dest = destination(newYork, 123.0, 500.0)
        val back = destination(dest, (123.0 + 180) % 360, 500.0)
        assertEqualsD(newYork.latitude, back.latitude, 0.5)
        assertEqualsD(newYork.longitude, back.longitude, 0.5)
    }
    
    println("\n--- Bounding Box ---")
    test("Bounding box creation") {
        val bb = boundingBox(newYork, 10.0)
        assertTrue(bb.north > newYork.latitude)
        assertTrue(bb.south < newYork.latitude)
        assertTrue(bb.contains(newYork))
    }
    
    println("\n--- Parsing ---")
    test("Parse decimal") {
        val c = parseCoordinate("40.7128, -74.0060")
        assertEqualsD(40.7128, c.latitude, 0.0001)
        assertEqualsD(-74.006, c.longitude, 0.0001)
    }
    test("Parse with parentheses") {
        val c = parseCoordinate("(40.7128, -74.0060)")
        assertEqualsD(40.7128, c.latitude, 0.0001)
    }
    
    println("\n--- DMS ---")
    test("DMS to decimal") {
        assertEqualsD(40.446333, dmsToDecimal(40.0, 26.0, 46.8), 0.0001)
    }
    test("Decimal to DMS") {
        val (d, m, s) = decimalToDms(40.446333)
        assertEquals(40, d)
        assertEquals(26, m)
        assertEqualsD(46.8, s, 1.0)
    }
    test("Coordinate to DMS") {
        val dms = Coordinate(40.7128, -74.0060).toDMS()
        assertTrue(dms.contains("N") && dms.contains("W"))
    }
    
    println("\n--- Polygon ---")
    test("Point inside triangle") {
        val tri = listOf(Coordinate(1.0, 0.0), Coordinate(0.0, 1.0), Coordinate(-1.0, 0.0))
        assertTrue(isInsidePolygon(Coordinate(0.0, 0.5), tri))
    }
    test("Point outside triangle") {
        val tri = listOf(Coordinate(1.0, 0.0), Coordinate(0.0, 1.0), Coordinate(-1.0, 0.0))
        assertFalse(isInsidePolygon(Coordinate(2.0, 0.0), tri))
    }
    test("Polygon area ~12300 km²") {
        val sq = listOf(Coordinate(0.0, 0.0), Coordinate(1.0, 0.0), Coordinate(1.0, 1.0), Coordinate(0.0, 1.0))
        assertTrue(polygonArea(sq) in 12000.0..13000.0)
    }
    test("Polygon centroid") {
        val sq = listOf(Coordinate(0.0, 0.0), Coordinate(10.0, 0.0), Coordinate(10.0, 10.0), Coordinate(0.0, 10.0))
        val c = centroid(sq)
        assertEqualsD(5.0, c.latitude, 0.0001)
        assertEqualsD(5.0, c.longitude, 0.0001)
    }
    test("Polygon perimeter ~444 km") {
        val sq = listOf(Coordinate(0.0, 0.0), Coordinate(0.0, 1.0), Coordinate(1.0, 1.0), Coordinate(1.0, 0.0))
        assertTrue(perimeter(sq) in 440.0..450.0)
    }
    
    println("\n--- Path Interpolation ---")
    test("Interpolate 3 waypoints") {
        val pts = interpolatePath(newYork, london, 3)
        assertEquals(3, pts.size)
    }
    
    println("\n--- Find Closest ---")
    test("Find closest location") {
        val candidates = listOf(london, tokyo, sydney, paris)
        val (closest, dist) = findClosest(newYork, candidates)!!
        assertEquals(london, closest)
    }
    test("Empty list returns null") {
        assertEquals(null, findClosest(newYork, emptyList()))
    }
    
    println("\n--- Longitude Normalization ---")
    test("Normalize longitude") {
        assertEqualsD(0.0, 0.0.normalizeLongitude(), 0.001)
        assertEqualsD(180.0, 180.0.normalizeLongitude(), 0.001)
        assertEqualsD(-170.0, 190.0.normalizeLongitude(), 0.001)
        assertEqualsD(170.0, (-190.0).normalizeLongitude(), 0.001)
    }
    
    println("\n--- UTM ---")
    test("UTM zone") {
        assertEquals(31, CoordinateSystems.utmZone(0.0))
        assertEquals(1, CoordinateSystems.utmZone(-180.0))
        assertEquals(60, CoordinateSystems.utmZone(179.0))
        // 180 is edge case, zone wraps around
    }
    test("UTM hemisphere") {
        assertEquals("N", CoordinateSystems.utmHemisphere(45.0))
        assertEquals("S", CoordinateSystems.utmHemisphere(-45.0))
    }
    
    println("\n" + "=".repeat(60))
    println("Results: $passed passed, $failed failed")
    if (failed > 0) { println("❌ SOME TESTS FAILED"); System.exit(1) }
    else { println("✅ ALL TESTS PASSED") }
}

runTests()