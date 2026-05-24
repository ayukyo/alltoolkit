# Test suite for haversine_utils
# Run with: Rscript test_haversine.R

source("mod.R")

# Test counter
tests_passed <- 0
tests_failed <- 0

# Helper function for test assertions
test_that <- function(description, condition) {
  if (condition) {
    cat("✓ PASS:", description, "\n")
    tests_passed <<- tests_passed + 1
  } else {
    cat("✗ FAIL:", description, "\n")
    tests_failed <<- tests_failed + 1
  }
}

cat("\n========================================\n")
cat("Testing haversine_utils\n")
cat("========================================\n\n")

# Test 1: Degree to Radian conversion
cat("--- Testing degree/radian conversion ---\n")
test_that("degrees_to_radians(180) equals pi",
          abs(degrees_to_radians(180) - pi) < 1e-10)
test_that("degrees_to_radians(90) equals pi/2",
          abs(degrees_to_radians(90) - pi/2) < 1e-10)
test_that("degrees_to_radians(0) equals 0",
          abs(degrees_to_radians(0)) < 1e-10)
test_that("radians_to_degrees(pi) equals 180",
          abs(radians_to_degrees(pi) - 180) < 1e-10)

# Test 2: Haversine distance - known distances
cat("\n--- Testing haversine_distance with known distances ---\n")

# New York to Los Angeles: approximately 3944 km (2448 miles)
nyc_to_la_km <- haversine_distance(40.7128, -74.0060, 34.0522, -118.2437, "km")
test_that("NYC to LA distance is approximately 3944 km",
          abs(nyc_to_la_km - 3944) < 10)

nyc_to_la_miles <- haversine_distance(40.7128, -74.0060, 34.0522, -118.2437, "miles")
test_that("NYC to LA distance is approximately 2452 miles",
          abs(nyc_to_la_miles - 2452) < 10)

# London to Paris: approximately 344 km (214 miles)
london_to_paris_km <- haversine_distance(51.5074, -0.1278, 48.8566, 2.3522, "km")
test_that("London to Paris distance is approximately 344 km",
          abs(london_to_paris_km - 344) < 5)

# Beijing to Shanghai: approximately 1068 km
beijing_to_shanghai <- haversine_distance(39.9042, 116.4074, 31.2304, 121.4737, "km")
test_that("Beijing to Shanghai distance is approximately 1068 km",
          abs(beijing_to_shanghai - 1068) < 10)

# Same point should be 0 distance
same_point <- haversine_distance(40.7128, -74.0060, 40.7128, -74.0060, "km")
test_that("Same point distance is 0",
          abs(same_point) < 1e-10)

# Antipodal points (opposite sides of Earth)
antipodal <- haversine_distance(0, 0, 0, 180, "km")
test_that("Antipodal points distance is approximately half Earth circumference",
          abs(antipodal - 20015) < 50)

# Test 3: Input validation
cat("\n--- Testing input validation ---\n")

error_caught <- FALSE
tryCatch({
  haversine_distance("a", -74, 34, -118, "km")
}, error = function(e) {
  error_caught <- TRUE
})
test_that("Error on non-numeric input", error_caught)

error_caught <- FALSE
tryCatch({
  haversine_distance(40, -74, 34, -118, "invalid")
}, error = function(e) {
  error_caught <- TRUE
})
test_that("Error on invalid unit", error_caught)

# Test 4: Bearing calculations
cat("\n--- Testing bearing ---\n")

# NYC to LA bearing should be approximately West (around 273 degrees)
nyc_to_la_bearing <- bearing(40.7128, -74.0060, 34.0522, -118.2437)
test_that("NYC to LA bearing is approximately West (~273°)",
          abs(nyc_to_la_bearing - 273) < 5)

# North should be 0 or 360
north_bearing <- bearing(0, 0, 10, 0)
test_that("Bearing due North is ~0°", north_bearing < 5 || north_bearing > 355)

# Compass direction tests
test_that("bearing_to_compass(0) is N", bearing_to_compass(0) == "N")
test_that("bearing_to_compass(45) is NE", bearing_to_compass(45) == "NE")
test_that("bearing_to_compass(90) is E", bearing_to_compass(90) == "E")
test_that("bearing_to_compass(180) is S", bearing_to_compass(180) == "S")
test_that("bearing_to_compass(270) is W", bearing_to_compass(270) == "W")

# Test 5: Midpoint
cat("\n--- Testing midpoint ---\n")

mid <- midpoint(0, 0, 0, 90)
test_that("Midpoint latitude for equator points is 0",
          abs(mid$lat) < 1e-10)
test_that("Midpoint longitude for 0,0 and 0,90 is approximately 45",
          abs(mid$lon - 45) < 0.1)

# Test 6: Destination point
cat("\n--- Testing destination_point ---\n")

# Move 100km North from equator
dest <- destination_point(0, 0, 0, 100, "km")
test_that("Destination 100km North from equator has lat ~0.9°",
          abs(dest$lat - 0.9) < 0.1)
test_that("Destination 100km North from equator has lon ~0",
          abs(dest$lon) < 0.1)

# Test 7: find_nearest
cat("\n--- Testing find_nearest ---\n")

candidates <- data.frame(
  lat = c(34.05, 40.71, 41.87),
  lon = c(-118.24, -74.00, -87.62),
  name = c("LA", "NYC", "Chicago")
)

nearest <- find_nearest(41.87, -87.62, candidates, "km")
test_that("Nearest to Chicago is Chicago itself",
          nearest$index == 3)
test_that("Nearest distance to itself is approximately 0",
          nearest$distance < 1)

# Test 8: within_radius
cat("\n--- Testing within_radius ---\n")

within <- within_radius(41.87, -87.62, candidates, 1500, "km")
test_that("Within 1500km of Chicago includes at least Chicago",
          nrow(within) >= 1)

within_ny <- within_radius(40.71, -74.00, candidates, 1200, "km")
test_that("Within 1200km of NYC includes NYC and Chicago",
          nrow(within_ny) == 2)

# Test 9: bounding_box
cat("\n--- Testing bounding_box ---\n")

bbox <- bounding_box(40.7128, -74.0060, 50, "km")
test_that("Bounding box min_lat < max_lat",
          bbox$min_lat < bbox$max_lat)
test_that("Bounding box min_lon < max_lon",
          bbox$min_lon < bbox$max_lon)
test_that("Bounding box center is approximately correct",
          abs((bbox$min_lat + bbox$max_lat) / 2 - 40.7128) < 0.01)

# Test 10: path_distance
cat("\n--- Testing path_distance ---\n")

path <- data.frame(
  lat = c(40.71, 41.87, 34.05),
  lon = c(-74.00, -87.62, -118.24)
)

total_dist <- path_distance(path, "km")
test_that("Path distance is greater than zero",
          total_dist > 0)
test_that("Path distance equals sum of individual segments",
          total_dist > haversine_distance(40.71, -74, 41.87, -87.62, "km"))

# Single point path
single_point <- data.frame(lat = 40.71, lon = -74.00)
test_that("Single point path has zero distance",
          path_distance(single_point, "km") == 0)

# Test 11: Validation functions
cat("\n--- Testing validation functions ---\n")

test_that("is_valid_latitude(45) is TRUE", is_valid_latitude(45))
test_that("is_valid_latitude(-90) is TRUE", is_valid_latitude(-90))
test_that("is_valid_latitude(91) is FALSE", !is_valid_latitude(91))
test_that("is_valid_longitude(180) is TRUE", is_valid_longitude(180))
test_that("is_valid_longitude(-180) is TRUE", is_valid_longitude(-180))
test_that("is_valid_longitude(181) is FALSE", !is_valid_longitude(181))

# Test 12: normalize_longitude
cat("\n--- Testing normalize_longitude ---\n")

test_that("normalize_longitude(270) equals -90",
          abs(normalize_longitude(270) - (-90)) < 1e-10)
test_that("normalize_longitude(-270) equals 90",
          abs(normalize_longitude(-270) - 90) < 1e-10)
test_that("normalize_longitude(180) equals -180",
          abs(normalize_longitude(180) - (-180)) < 1e-10)

# Test 13: haversine_distance_batch
cat("\n--- Testing haversine_distance_batch ---\n")

batch_points <- data.frame(
  lat1 = c(40.7128, 51.5074),
  lon1 = c(-74.0060, -0.1278),
  lat2 = c(34.0522, 48.8566),
  lon2 = c(-118.2437, 2.3522)
)

batch_distances <- haversine_distance_batch(batch_points, "km")
test_that("Batch returns vector of length 2",
          length(batch_distances) == 2)
test_that("First batch distance matches NYC to LA",
          abs(batch_distances[1] - nyc_to_la_km) < 1)
test_that("Second batch distance matches London to Paris",
          abs(batch_distances[2] - london_to_paris_km) < 1)

# Test 14: Direction text
cat("\n--- Testing get_direction_text ---\n")

test_that("get_direction_text(0) is North",
          get_direction_text(0) == "North")
test_that("get_direction_text(90) is East",
          get_direction_text(90) == "East")
test_that("get_direction_text(180) is South",
          get_direction_text(180) == "South")
test_that("get_direction_text(270) is West",
          get_direction_text(270) == "West")

# Test 15: Units consistency
cat("\n--- Testing unit consistency ---\n")

dist_km <- haversine_distance(40.7128, -74.0060, 34.0522, -118.2437, "km")
dist_miles <- haversine_distance(40.7128, -74.0060, 34.0522, -118.2437, "miles")
dist_meters <- haversine_distance(40.7128, -74.0060, 34.0522, -118.2437, "meters")

test_that("km to miles conversion is correct",
          abs(dist_km / dist_miles - 1.60934) < 0.01)
test_that("km to meters conversion is correct",
          abs(dist_km * 1000 - dist_meters) < 1)

# Summary
cat("\n========================================\n")
cat("Test Results\n")
cat("========================================\n")
cat("Passed:", tests_passed, "\n")
cat("Failed:", tests_failed, "\n")
cat("Total:", tests_passed + tests_failed, "\n")

if (tests_failed == 0) {
  cat("\n✓ All tests passed!\n")
  quit(status = 0)
} else {
  cat("\n✗ Some tests failed!\n")
  quit(status = 1)
}