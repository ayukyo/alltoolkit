/**
 * Tests for CoordinateUtils - Self-contained version
 * 
 * Run with: kotlinc -script CoordinateUtilsTest.kt
 */

// Simple assertion functions (no external dependencies)
fun assertEquals(expected: Any?, actual: Any?, message: String = "") {
    if (expected != actual) {
        throw AssertionError("$message\nExpected: $expected\nActual: $actual")
    }
}

fun assertEquals(expected: Double, actual: Double, delta: Double, message: String = "") {
    if (kotlin.math.abs(expected - actual) > delta) {
        throw AssertionError("$message\nExpected: $expected ± $delta\nActual: $actual")
    }
}

fun assertTrue(condition: Boolean, message: String = "") {
    if (!condition) {
        throw AssertionError(message.ifEmpty { "Condition was false" })
    }
}

fun assertFalse(condition: Boolean, message: String = "") {
    if (condition) {
        throw AssertionError(message.ifEmpty { "Condition was true" })
    }
}

fun assertFailsWith(message: String = "", block: () -> Unit) {
    try {
        block()
        throw AssertionError(message.ifEmpty { "Expected exception but none was thrown" })
    } catch (e: Exception) {
        // Expected
    }
}

// Load the main module
// Note: In production, you would import the CoordinateUtils module directly

fun runTests() {
    println("=" .repeat(60))
    println("CoordinateUtils Tests")
    println("=".repeat(60))
    
    var passed = 0
    var failed = 0
    val results = mutableListOf<Pair<String, Boolean>>()
    
    // Test coordinates
    val newYork = Coordinate(40.7128, -74.0060)
    val london = Coordinate(51.5074, -0.1278)
    val tokyo = Coordinate(35.6762, 139.6503)
    val sydney = Coordinate(-33.8688, 151.2093)
    val beijing = Coordinate(39.9042, 116.4074)
    val paris = Coordinate(48.8566, 2.3522)
    
    // Test functions
    fun test(name: String, block: () -> Unit) {
        try {
            block()
            results.add(name to true)
            passed++
            println("  ✓ $name")
        } catch (e: Exception) {
            results.add(name to false)
            failed++
            println("  ✗ $name: ${e.message}")
        }
    }
    
    println("\n--- Coordinate Creation & Validation ---")
    
    test("Coordinate creation") {
        val coord = Coordinate(45.0, -90.0)
        assertEquals(45.0, coord.latitude)
        assertEquals(-90.0, coord.longitude)
    }
    
    test("Coordinate validation - valid range") {
        Coordinate(90.0, 180.0)
        Coordinate(-90.0, -180.0)
        Coordinate(0.0, 0.0)
    }
    
    test("Coordinate validation - invalid latitude high") {
        assertFailsWith { Coordinate(91.0, 0.0) }
    }
    
    test("Coordinate validation - invalid latitude low") {
        assertFailsWith { Coordinate(-91.0, 0.0) }
    }
    
    test("Coordinate validation - invalid longitude high") {
        assertFailsWith { Coordinate(0.0, 181.0) }
    }
    
    test("Coordinate validation - invalid longitude low") {
        assertFailsWith { Coordinate(0.0, -181.0) }
    }
    
    println("\n--- Distance Calculations ---")
    
    test("Distance New York to London (~5570 km)") {
        val dist = distanceInKm(newYork, london)
        assertTrue(dist in 5550.0..5590.0, "Distance should be ~5570 km, got $dist")
    }
    
    test("Distance New York to Tokyo (~10870 km)") {
        val dist = distanceInKm(newYork, tokyo)
        assertTrue(dist in 10850.0..10890.0, "Distance should be ~10870 km, got $dist")
    }
    
    test("Distance in different units") {
        val distKm = distanceInKm(newYork, london)
        val distM = distanceInMeters(newYork, london)
        val distMi = distanceInMiles(newYork, london)
        
        assertEquals(distKm * 1000, distM, 1.0)
        assertEquals(distKm * 0.621371, distMi, 10.0)
    }
    
    test("Distance Paris to London (~344 km)") {
        val dist = distanceInKm(paris, london)
        assertTrue(dist in 340.0..350.0, "Distance should be ~344 km, got $dist")
    }
    
    test("Distance Beijing to Tokyo (~2100 km)") {
        val dist = distanceInKm(beijing, tokyo)
        assertTrue(dist in 2090.0..2110.0, "Distance should be ~2100 km, got $dist")
    }
    
    test("Same point distance is zero") {
        val dist = distanceInKm(newYork, newYork)
        assertEquals(0.0, dist, 0.001)
    }
    
    test("Antipodal points distance") {
        val point1 = Coordinate(0.0, 0.0)
        val point2 = Coordinate(0.0, 180.0)
        val dist = distanceInKm(point1, point2)
        assertTrue(dist > 19000.0, "Antipodal distance should be > 19000 km, got $dist")
    }
    
    println("\n--- Bearing Calculations ---")
    
    test("Bearing New York to London (~52°)") {
        val bearing = bearing(newYork, london)
        assertTrue(bearing in 50.0..55.0, "Bearing should be ~52°, got $bearing")
    }
    
    test("Bearing New York to Sydney (~230°)") {
        val brng = bearing(newYork, sydney)
        assertTrue(brng in 200.0..260.0, "Bearing should be ~230°, got $brng")
    }
    
    test("Final bearing") {
        val initialBearing = bearing(newYork, london)
        val finalBearing = finalBearing(newYork, london)
        val expectedFinal = (initialBearing + 180) % 360
        assertTrue(kotlin.math.abs(finalBearing - expectedFinal) < 5.0)
    }
    
    println("\n--- Midpoint & Destination ---")
    
    test("Midpoint calculation") {
        val mid = midpoint(newYork, london)
        assertTrue(mid.latitude in 46.0..48.0, "Midpoint latitude should be ~47°, got ${mid.latitude}")
        assertTrue(mid.longitude in -38.0..-36.0, "Midpoint longitude should be ~-37°, got ${mid.longitude}")
    }
    
    test("Destination 100km northeast") {
        val dest = destination(newYork, 45.0, 100.0)
        assertTrue(dest.latitude > newYork.latitude)
        assertTrue(dest.longitude > newYork.longitude)
        val actualDistance = distanceInKm(newYork, dest)
        assertEquals(100.0, actualDistance, 1.0)
    }
    
    test("Destination round trip") {
        val bearing = 123.0
        val distance = 500.0
        val dest = destination(newYork, bearing, distance)
        val returnBearing = (bearing + 180) % 360
        val backHome = destination(dest, returnBearing, distance)
        
        assertEquals(newYork.latitude, backHome.latitude, 0.001)
        assertEquals(newYork.longitude, backHome.longitude, 0.001)
    }
    
    println("\n--- Bounding Box ---")
    
    test("Bounding box creation") {
        val bbox = boundingBox(newYork, 10.0)
        assertTrue(bbox.north > newYork.latitude)
        assertTrue(bbox.south < newYork.latitude)
        assertTrue(bbox.east > newYork.longitude)
        assertTrue(bbox.west < newYork.longitude)
        assertTrue(bbox.contains(newYork))
    }
    
    test("Bounding box size at equator") {
        val bbox = boundingBox(Coordinate(0.0, 0.0), 100.0)
        val latDiff = bbox.north - bbox.south
        val lonDiff = bbox.east - bbox.west
        
        assertTrue(latDiff in 1.7..2.0, "Latitude span should be ~1.8°, got $latDiff")
        assertTrue(lonDiff in 1.7..2.0, "Longitude span should be ~1.8°, got $lonDiff")
    }
    
    println("\n--- Coordinate Parsing ---")
    
    test("Parse decimal format") {
        val coord = parseCoordinate("40.7128, -74.0060")
        assertEquals(40.7128, coord.latitude, 0.0001)
        assertEquals(-74.006, coord.longitude, 0.0001)
    }
    
    test("Parse space separated") {
        val coord = parseCoordinate("40.7128 -74.0060")
        assertEquals(40.7128, coord.latitude, 0.0001)
    }
    
    test("Parse with parentheses") {
        val coord = parseCoordinate("(40.7128, -74.0060)")
        assertEquals(40.7128, coord.latitude, 0.0001)
    }
    
    test("Parse with degree symbol") {
        val coord = parseCoordinate("40.7128° -74.0060°")
        assertEquals(40.7128, coord.latitude, 0.0001)
    }
    
    println("\n--- DMS Conversion ---")
    
    test("DMS to decimal") {
        val decimal = dmsToDecimal(40.0, 26.0, 46.8)
        assertEquals(40.446333, decimal, 0.0001)
    }
    
    test("Decimal to DMS round trip") {
        val decimal = dmsToDecimal(40.0, 26.0, 46.8)
        val (deg, min, sec) = decimalToDms(decimal)
        assertEquals(40, deg)
        assertEquals(26, min)
        assertEquals(46.8, sec, 1.0)
    }
    
    test("Coordinate to DMS format") {
        val coord = Coordinate(40.7128, -74.0060)
        val dms = coord.toDMS()
        
        assertTrue(dms.contains("N"))
        assertTrue(dms.contains("W"))
        assertTrue(dms.contains("40°"))
        assertTrue(dms.contains("74°"))
    }
    
    println("\n--- Polygon Operations ---")
    
    test("Point inside polygon") {
        val triangle = listOf(
            Coordinate(1.0, 0.0),
            Coordinate(0.0, 1.0),
            Coordinate(-1.0, 0.0)
        )
        
        assertTrue(isInsidePolygon(Coordinate(0.0, 0.5), triangle))
        assertTrue(isInsidePolygon(Coordinate(0.0, 0.1), triangle))
    }
    
    test("Point outside polygon") {
        val triangle = listOf(
            Coordinate(1.0, 0.0),
            Coordinate(0.0, 1.0),
            Coordinate(-1.0, 0.0)
        )
        
        assertFalse(isInsidePolygon(Coordinate(2.0, 0.0), triangle))
        assertFalse(isInsidePolygon(Coordinate(0.0, 2.0), triangle))
    }
    
    test("Polygon area") {
        val square = listOf(
            Coordinate(0.0, 0.0),
            Coordinate(1.0, 0.0),
            Coordinate(1.0, 1.0),
            Coordinate(0.0, 1.0)
        )
        
        val area = polygonArea(square)
        assertTrue(area in 12000.0..13000.0, "Area should be ~12300 km², got $area")
    }
    
    test("Polygon centroid") {
        val polygon = listOf(
            Coordinate(0.0, 0.0),
            Coordinate(10.0, 0.0),
            Coordinate(10.0, 10.0),
            Coordinate(0.0, 10.0)
        )
        
        val center = centroid(polygon)
        assertEquals(5.0, center.latitude, 0.0001)
        assertEquals(5.0, center.longitude, 0.0001)
    }
    
    test("Polygon perimeter") {
        val square = listOf(
            Coordinate(0.0, 0.0),
            Coordinate(0.0, 1.0),
            Coordinate(1.0, 1.0),
            Coordinate(1.0, 0.0)
        )
        
        val perim = perimeter(square)
        assertTrue(perim in 440.0..450.0, "Perimeter should be ~444 km, got $perim")
    }
    
    println("\n--- Path Interpolation ---")
    
    test("Interpolate path") {
        val points = interpolatePath(newYork, london, 3)
        assertEquals(3, points.size)
        
        val distances = points.map { distanceInKm(it, london) }
        for (i in 0 until distances.size - 1) {
            assertTrue(distances[i] > distances[i + 1])
        }
    }
    
    println("\n--- Find Closest ---")
    
    test("Find closest location") {
        val candidates = listOf(london, tokyo, sydney, paris)
        val (closest, dist) = findClosest(newYork, candidates)!!
        
        assertEquals(london, closest)
        assertTrue(dist < distanceInKm(newYork, tokyo))
        assertTrue(dist < distanceInKm(newYork, sydney))
        assertTrue(dist < distanceInKm(newYork, paris))
    }
    
    test("Find closest empty list") {
        val result = findClosest(newYork, emptyList())
        assertEquals(null, result)
    }
    
    println("\n--- Longitude Normalization ---")
    
    test("Normalize longitude") {
        assertEquals(0.0, 0.0.normalizeLongitude())
        assertEquals(180.0, 180.0.normalizeLongitude())
        assertEquals(-180.0, (-180.0).normalizeLongitude())
        assertEquals(-170.0, 190.0.normalizeLongitude())
        assertEquals(170.0, (-190.0).normalizeLongitude())
    }
    
    println("\n--- UTM Conversion ---")
    
    test("UTM zone calculation") {
        assertEquals(1, CoordinateSystems.utmZone(-180.0))
        assertEquals(1, CoordinateSystems.utmZone(-179.0))
        assertEquals(30, CoordinateSystems.utmZone(-0.1))
        assertEquals(31, CoordinateSystems.utmZone(0.0))
        assertEquals(31, CoordinateSystems.utmZone(0.1))
        assertEquals(60, CoordinateSystems.utmZone(179.0))
        assertEquals(60, CoordinateSystems.utmZone(180.0))
    }
    
    test("UTM hemisphere") {
        assertEquals("N", CoordinateSystems.utmHemisphere(45.0))
        assertEquals("N", CoordinateSystems.utmHemisphere(0.0))
        assertEquals("S", CoordinateSystems.utmHemisphere(-1.0))
        assertEquals("S", CoordinateSystems.utmHemisphere(-45.0))
    }
    
    test("WGS84 to UTM conversion") {
        val (zone, easting, northing) = CoordinateSystems.wgs84ToUtm(Coordinate(40.0, -75.0))
        assertEquals(18, zone)
        assertTrue(easting in 400000.0..600000.0)
        assertTrue(northing > 4000000.0)
    }
    
    // Summary
    println("\n" + "=".repeat(60))
    println("Results: $passed passed, $failed failed")
    println("=".repeat(60))
    
    if (failed > 0) {
        println("\n❌ SOME TESTS FAILED")
        kotlin.system.exitProcess(1)
    } else {
        println("\n✅ ALL TESTS PASSED")
    }
}

runTests()