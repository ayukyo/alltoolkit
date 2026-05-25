/**
 * CoordinateUtils - Usage Examples
 * 
 * This file demonstrates various use cases for the CoordinateUtils library.
 * 
 * Run with: kotlinc -script Examples.kt
 */

package coordinate_utils

fun main() {
    println("=" .repeat(60))
    println("CoordinateUtils - Geographic Coordinate Utilities for Kotlin")
    println("=".repeat(60))
    println()
    
    // Example 1: Calculate distance between cities
    example1_DistanceCalculation()
    
    // Example 2: Bearing and navigation
    example2_BearingAndNavigation()
    
    // Example 3: Midpoint and destination
    example3_MidpointAndDestination()
    
    // Example 4: Bounding box for proximity search
    example4_BoundingBox()
    
    // Example 5: Coordinate parsing and formatting
    example5_CoordinateParsing()
    
    // Example 6: Polygon operations
    example6_PolygonOperations()
    
    // Example 7: Find closest location
    example7_FindClosest()
    
    // Example 8: Path interpolation
    example8_PathInterpolation()
    
    // Example 9: UTM coordinate system
    example9_UTMConversion()
    
    println("\n" + "=".repeat(60))
    println("All examples completed!")
    println("=".repeat(60))
}

fun example1_DistanceCalculation() {
    println("\n📍 Example 1: Distance Calculation")
    println("-".repeat(40))
    
    val newYork = Coordinate(40.7128, -74.0060)
    val london = Coordinate(51.5074, -0.1278)
    val tokyo = Coordinate(35.6762, 139.6503)
    val sydney = Coordinate(-33.8688, 151.2093)
    
    println("New York: $newYork")
    println("London: $london")
    println("Tokyo: $tokyo")
    println("Sydney: $sydney")
    println()
    
    // Calculate distances in different units
    val nyToLondon = distanceInKm(newYork, london)
    val nyToTokyo = distanceInKm(newYork, tokyo)
    val nyToSydney = distanceInKm(newYork, sydney)
    
    println("Distance New York → London: ${"%.1f".format(nyToLondon)} km " +
            "(${"%.1f".format(distanceInMiles(newYork, london))} mi)")
    println("Distance New York → Tokyo: ${"%.1f".format(nyToTokyo)} km")
    println("Distance New York → Sydney: ${"%.1f".format(nyToSydney)} km")
}

fun example2_BearingAndNavigation() {
    println("\n🧭 Example 2: Bearing and Navigation")
    println("-".repeat(40))
    
    val sanFrancisco = Coordinate(37.7749, -122.4194)
    val seattle = Coordinate(47.6062, -122.3321)
    
    val bearing = bearing(sanFrancisco, seattle)
    val finalBearing = finalBearing(sanFrancisco, seattle)
    
    println("From San Francisco to Seattle:")
    println("  Initial bearing: ${"%.1f".format(bearing)}°")
    println("  Final bearing: ${"%.1f".format(finalBearing)}°")
    println()
    
    // Direction names
    fun bearingToDirection(bearing: Double): String {
        val directions = listOf("N", "NE", "E", "SE", "S", "SW", "W", "NW", "N")
        val index = ((bearing + 22.5) / 45).toInt()
        return directions[index]
    }
    
    println("Direction: ${bearingToDirection(bearing)}")
}

fun example3_MidpointAndDestination() {
    println("\n🗺️ Example 3: Midpoint and Destination")
    println("-".repeat(40))
    
    val boston = Coordinate(42.3601, -71.0589)
    val miami = Coordinate(25.7617, -80.1918)
    
    // Find midpoint
    val midPoint = midpoint(boston, miami)
    println("Boston: $boston")
    println("Miami: $miami")
    println("Midpoint: $midPoint")
    println()
    
    // Travel 500km northeast from Boston
    val bearing = 45.0
    val distance = 500.0
    val destination = destination(boston, bearing, distance)
    
    println("Travel ${distance}km at ${bearing}° from Boston:")
    println("  Destination: $destination")
    println("  In DMS: ${destination.toDMS()}")
}

fun example4_BoundingBox() {
    println("\n📦 Example 4: Bounding Box for Proximity Search")
    println("-".repeat(40))
    
    val storeLocation = Coordinate(40.7580, -73.9855) // Times Square
    val searchRadius = 5.0 // 5 km
    
    val bbox = boundingBox(storeLocation, searchRadius)
    
    println("Store location: $storeLocation")
    println("Search radius: $searchRadius km")
    println("Bounding box:")
    println("  North: ${"%.4f".format(bbox.north)}")
    println("  South: ${"%.4f".format(bbox.south)}")
    println("  East: ${"%.4f".format(bbox.east)}")
    println("  West: ${"%.4f".format(bbox.west)}")
    println()
    
    // Check if a customer is within range
    val customer = Coordinate(40.7614, -73.9776)
    println("Customer at $customer")
    println("  In bounding box: ${bbox.contains(customer)}")
    println("  Actual distance: ${"%.2f".format(distanceInKm(storeLocation, customer))} km")
}

fun example5_CoordinateParsing() {
    println("\n📝 Example 5: Coordinate Parsing and Formatting")
    println("-".repeat(40))
    
    // Parse various formats
    val formats = listOf(
        "40.7128, -74.0060",
        "40.7128 -74.0060",
        "(40.7128, -74.0060)",
        "40.7128° -74.0060°"
    )
    
    println("Parsing different formats:")
    formats.forEach { format ->
        val coord = parseCoordinate(format)
        println("  \"$format\" → $coord")
    }
    println()
    
    // Format as DMS
    val coord = Coordinate(40.7128, -74.0060)
    println("Coordinate: $coord")
    println("  DMS format: ${coord.toDMS()}")
    
    // DMS conversion
    val (deg, min, sec) = decimalToDms(40.7128)
    println("  DMS components: $deg° $min' ${"%.2f".format(sec)}\"")
}

fun example6_PolygonOperations() {
    println("\n🔷 Example 6: Polygon Operations")
    println("-".repeat(40))
    
    // Define a triangular area
    val triangle = listOf(
        Coordinate(40.0, -75.0),
        Coordinate(41.0, -75.0),
        Coordinate(40.5, -74.0)
    )
    
    val area = polygonArea(triangle)
    val center = centroid(triangle)
    val perim = perimeter(triangle)
    
    println("Triangle vertices: ${triangle.size}")
    triangle.forEachIndexed { i, v ->
        println("  $i: $v")
    }
    println()
    println("Area: ${"%.2f".format(area)} km²")
    println("Perimeter: ${"%.2f".format(perim)} km")
    println("Centroid: $center")
    println()
    
    // Point in polygon test
    val testPoints = listOf(
        Coordinate(40.5, -74.8),
        Coordinate(45.0, -75.0)
    )
    
    println("Point in polygon test:")
    testPoints.forEach { point ->
        val inside = isInsidePolygon(point, triangle)
        println("  $point: ${if (inside) "INSIDE" else "OUTSIDE"}")
    }
}

fun example7_FindClosest() {
    println("\n🎯 Example 7: Find Closest Location")
    println("-".repeat(40))
    
    val myLocation = Coordinate(37.7749, -122.4194) // San Francisco
    
    val coffeeShops = listOf(
        "Blue Bottle" to Coordinate(37.7820, -122.4060),
        "Sightglass" to Coordinate(37.7775, -122.4100),
        "Ritual" to Coordinate(37.7590, -122.4210),
        "Four Barrel" to Coordinate(37.7660, -122.4250)
    )
    
    println("My location: $myLocation")
    println("\nCoffee shops:")
    coffeeShops.forEach { (name, loc) ->
        val dist = distanceInKm(myLocation, loc)
        println("  $name: ${"%.2f".format(dist)} km away")
    }
    println()
    
    val (closest, distance) = findClosest(myLocation, coffeeShops.map { it.second })!!
    val closestIndex = coffeeShops.map { it.second }.indexOf(closest)
    println("Closest: ${coffeeShops[closestIndex].first} (${"%.2f".format(distance)} km)")
}

fun example8_PathInterpolation() {
    println("\n✈️ Example 8: Path Interpolation")
    println("-".repeat(40))
    
    val losAngeles = Coordinate(34.0522, -118.2437)
    val newYork = Coordinate(40.7128, -74.0060)
    
    val numWaypoints = 5
    val waypoints = interpolatePath(losAngeles, newYork, numWaypoints)
    
    println("Flight path from Los Angeles to New York:")
    println("  Departure: $losAngeles")
    
    waypoints.forEachIndexed { i, wp ->
        println("  Waypoint ${i + 1}: ${"%.4f".format(wp.latitude)}, ${"%.4f".format(wp.longitude)}")
    }
    
    println("  Arrival: $newYork")
    println()
    
    val totalDistance = distanceInKm(losAngeles, newYork)
    println("Total distance: ${"%.1f".format(totalDistance)} km")
}

fun example9_UTMConversion() {
    println("\n🌐 Example 9: UTM Coordinate System")
    println("-".repeat(40))
    
    val locations = listOf(
        "New York" to Coordinate(40.7128, -74.0060),
        "London" to Coordinate(51.5074, -0.1278),
        "Tokyo" to Coordinate(35.6762, 139.6503),
        "Sydney" to Coordinate(-33.8688, 151.2093)
    )
    
    println("UTM conversions:")
    locations.forEach { (name, coord) ->
        val (zone, easting, northing) = CoordinateSystems.wgs84ToUtm(coord)
        val hemisphere = CoordinateSystems.utmHemisphere(coord.latitude)
        
        println("\n$name ($coord):")
        println("  UTM Zone: $zone$hemisphere")
        println("  Easting: ${"%.2f".format(easting)} m")
        println("  Northing: ${"%.2f".format(northing)} m")
    }
}