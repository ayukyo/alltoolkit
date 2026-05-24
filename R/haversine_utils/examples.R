# Haversine Utilities Examples
# Run with: Rscript examples.R

source("mod.R")

cat("\n========================================\n")
cat("Haversine Utils - Usage Examples\n")
cat("========================================\n\n")

# Example 1: Basic distance calculation
cat("--- Example 1: Basic Distance Calculation ---\n")
nyc_lat <- 40.7128
nyc_lon <- -74.0060
la_lat <- 34.0522
la_lon <- -118.2437

dist_km <- haversine_distance(nyc_lat, nyc_lon, la_lat, la_lon, "km")
dist_miles <- haversine_distance(nyc_lat, nyc_lon, la_lat, la_lon, "miles")

cat(sprintf("Distance from NYC (%.4f, %.4f) to LA (%.4f, %.4f):\n", 
            nyc_lat, nyc_lon, la_lat, la_lon))
cat(sprintf("  %.2f km\n", dist_km))
cat(sprintf("  %.2f miles\n", dist_miles))

# Example 2: Multiple cities comparison
cat("\n--- Example 2: Multiple City Comparisons ---\n")
cities <- list(
  list(name = "New York", lat = 40.7128, lon = -74.0060),
  list(name = "London", lat = 51.5074, lon = -0.1278),
  list(name = "Paris", lat = 48.8566, lon = 2.3522),
  list(name = "Tokyo", lat = 35.6762, lon = 139.6503),
  list(name = "Sydney", lat = -33.8688, lon = 151.2093)
)

cat("\nDistances from New York:\n")
for (city in cities[-1]) {  # Skip NYC itself
  dist <- haversine_distance(cities[[1]]$lat, cities[[1]]$lon, 
                              city$lat, city$lon, "km")
  cat(sprintf("  to %s: %.0f km\n", city$name, dist))
}

# Example 3: Find nearest city
cat("\n--- Example 3: Find Nearest City ---\n")
candidates <- data.frame(
  lat = c(34.0522, 51.5074, 48.8566, 35.6762, -33.8688),
  lon = c(-118.2437, -0.1278, 2.3522, 139.6503, 151.2093),
  name = c("Los Angeles", "London", "Paris", "Tokyo", "Sydney")
)

my_location_lat <- 41.87
my_location_lon <- -87.62
cat(sprintf("\nMy location: Chicago (%.2f, %.2f)\n", my_location_lat, my_location_lon))

nearest <- find_nearest(my_location_lat, my_location_lon, candidates, "km")
cat(sprintf("Nearest city: %s (%.0f km away)\n", 
            candidates$name[nearest$index], nearest$distance))

# Example 4: Find cities within radius
cat("\n--- Example 4: Find Cities Within Radius ---\n")
radius_km <- 6500
within <- within_radius(my_location_lat, my_location_lon, candidates, radius_km, "km")

cat(sprintf("\nCities within %d km of Chicago:\n", radius_km))
if (nrow(within) > 0) {
  for (i in 1:nrow(within)) {
    cat(sprintf("  %s: %.0f km\n", within$name[i], within$distance[i]))
  }
} else {
  cat("  No cities found within radius\n")
}

# Example 5: Calculate bearing and direction
cat("\n--- Example 5: Bearing and Direction ---\n")
nyc_to_la_bearing <- bearing(nyc_lat, nyc_lon, la_lat, la_lon)
compass <- bearing_to_compass(nyc_to_la_bearing)
direction <- get_direction_text(nyc_to_la_bearing)

cat(sprintf("Bearing from NYC to LA: %.1f° (%s - %s)\n", 
            nyc_to_la_bearing, compass, direction))

london_to_paris_bearing <- bearing(51.5074, -0.1278, 48.8566, 2.3522)
cat(sprintf("Bearing from London to Paris: %.1f° (%s)\n", 
            london_to_paris_bearing, bearing_to_compass(london_to_paris_bearing)))

# Example 6: Midpoint between two cities
cat("\n--- Example 6: Midpoint Calculation ---\n")
mid <- midpoint(nyc_lat, nyc_lon, la_lat, la_lon)
cat(sprintf("Midpoint between NYC and LA: (%.4f, %.4f)\n", mid$lat, mid$lon))

# Find nearest city to midpoint
nearest_to_mid <- find_nearest(mid$lat, mid$lon, candidates, "km")
cat(sprintf("Nearest major city to midpoint: %s (%.0f km away)\n",
            candidates$name[nearest_to_mid$index], nearest_to_mid$distance))

# Example 7: Destination point
cat("\n--- Example 7: Destination Point ---\n")
start_lat <- 40.7128
start_lon <- -74.0060
travel_bearing <- 45  # North-East
travel_distance <- 500

dest <- destination_point(start_lat, start_lon, travel_bearing, travel_distance, "km")
cat(sprintf("Starting from NYC, traveling %.0f km at %.0f° (%s):\n", 
            travel_distance, travel_bearing, get_direction_text(travel_bearing)))
cat(sprintf("  Destination: (%.4f, %.4f)\n", dest$lat, dest$lon))

# Verify by calculating distance back
verify_dist <- haversine_distance(dest$lat, dest$lon, start_lat, start_lon, "km")
cat(sprintf("  Verified distance: %.0f km\n", verify_dist))

# Example 8: Bounding box for search
cat("\n--- Example 8: Bounding Box for Database Query ---\n")
search_radius <- 100
bbox <- bounding_box(nyc_lat, nyc_lon, search_radius, "km")

cat(sprintf("Bounding box for %d km radius around NYC:\n", search_radius))
cat(sprintf("  Latitude:  %.4f to %.4f\n", bbox$min_lat, bbox$max_lat))
cat(sprintf("  Longitude: %.4f to %.4f\n", bbox$min_lon, bbox$max_lon))

cat("\n  SQL WHERE clause:\n")
cat(sprintf("    WHERE lat BETWEEN %.4f AND %.4f\n", bbox$min_lat, bbox$max_lat))
cat(sprintf("      AND lon BETWEEN %.4f AND %.4f\n", bbox$min_lon, bbox$max_lon))

# Example 9: Path distance calculation
cat("\n--- Example 9: Multi-City Trip Distance ---\n")
trip_path <- data.frame(
  lat = c(40.7128, 41.8781, 41.8781, 34.0522, 34.0522),
  lon = c(-74.0060, -87.6298, -87.6298, -118.2437, -118.2437),
  city = c("New York", "Chicago", "Chicago", "Los Angeles", "Los Angeles")
)

total_trip <- path_distance(trip_path, "km")
cat("Trip itinerary: New York → Chicago → Los Angeles\n")
cat(sprintf("Total distance: %.0f km (%.0f miles)\n", 
            total_trip, total_trip * 0.621371))

# Example 10: Batch distance calculation
cat("\n--- Example 10: Batch Distance Calculation ---\n")
locations <- data.frame(
  lat1 = c(40.7128, 51.5074, 35.6762),
  lon1 = c(-74.0060, -0.1278, 139.6503),
  lat2 = c(34.0522, 48.8566, -33.8688),
  lon2 = c(-118.2437, 2.3522, 151.2093),
  pair = c("NYC→LA", "London→Paris", "Tokyo→Sydney")
)

distances <- haversine_distance_batch(locations, "km")
cat("Batch distance calculations:\n")
for (i in 1:nrow(locations)) {
  cat(sprintf("  %s: %.0f km\n", locations$pair[i], distances[i]))
}

# Example 11: Coordinate validation
cat("\n--- Example 11: Coordinate Validation ---\n")
coordinates <- list(
  valid_lat = c(45, -90, 0, 89.9999),
  invalid_lat = c(91, -91, 100),
  valid_lon = c(180, -180, 0, 179.9999),
  invalid_lon = c(181, -181, 200)
)

cat("Valid latitudes: 45, -90, 0, 89.9999 →", 
    all(sapply(coordinates$valid_lat, is_valid_latitude)), "\n")
cat("Invalid latitudes: 91, -91, 100 →", 
    all(!sapply(coordinates$invalid_lat, is_valid_latitude)), "\n")
cat("Valid longitudes: 180, -180, 0, 179.9999 →", 
    all(sapply(coordinates$valid_lon, is_valid_longitude)), "\n")
cat("Invalid longitudes: 181, -181, 200 →", 
    all(!sapply(coordinates$invalid_lon, is_valid_longitude)), "\n")

# Example 12: Real-world scenario - Store locator
cat("\n--- Example 12: Real-World Scenario - Store Locator ---\n")
stores <- data.frame(
  lat = c(40.7580, 40.7614, 40.7484, 40.7829),
  lon = c(-73.9855, -73.9776, -73.9857, -73.9654),
  name = c("Times Square Store", "MoMA Store", "Empire State Store", "Met Store"),
  hours = c("9AM-10PM", "10AM-8PM", "8AM-11PM", "10AM-5PM")
)

user_lat <- 40.7505
user_lon <- -73.9934  # Near Times Square

cat(sprintf("User location: (%.4f, %.4f)\n", user_lat, user_lon))

# Find nearest store
nearest_store <- find_nearest(user_lat, user_lon, stores, "km")
cat(sprintf("\nNearest store: %s (%.1f km away)\n", 
            stores$name[nearest_store$index], nearest_store$distance))
cat(sprintf("Hours: %s\n", stores$hours[nearest_store$index]))

# Find stores within 5 km
nearby_stores <- within_radius(user_lat, user_lon, stores, 5, "km")
cat(sprintf("\nStores within 5 km:\n"))
if (nrow(nearby_stores) > 0) {
  for (i in 1:nrow(nearby_stores)) {
    cat(sprintf("  %s: %.1f km (%s)\n", 
                nearby_stores$name[i], nearby_stores$distance[i], nearby_stores$hours[i]))
  }
}

cat("\n========================================\n")
cat("Examples completed!\n")
cat("========================================\n")