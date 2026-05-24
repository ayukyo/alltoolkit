# Haversine Formula Utilities
# Calculate distances between geographic coordinates on Earth
# Zero external dependencies - pure R base implementation

# Constants
EARTH_RADIUS_KM <- 6371.0
EARTH_RADIUS_MILES <- 3958.8
EARTH_RADIUS_METERS <- 6371000.0

#' Convert degrees to radians
#' @param degrees Numeric value in degrees
#' @return Numeric value in radians
#' @examples
#' degrees_to_radians(180)  # Returns pi
#' degrees_to_radians(90)   # Returns pi/2
degrees_to_radians <- function(degrees) {
  if (!is.numeric(degrees)) {
    stop("Input must be numeric")
  }
  return(degrees * pi / 180)
}

#' Convert radians to degrees
#' @param radians Numeric value in radians
#' @return Numeric value in degrees
#' @examples
#' radians_to_degrees(pi)    # Returns 180
#' radians_to_degrees(pi/2)   # Returns 90
radians_to_degrees <- function(radians) {
  if (!is.numeric(radians)) {
    stop("Input must be numeric")
  }
  return(radians * 180 / pi)
}

#' Calculate the haversine distance between two points on Earth
#' Uses the haversine formula to calculate the great-circle distance
#' @param lat1 Latitude of point 1 in degrees
#' @param lon1 Longitude of point 1 in degrees
#' @param lat2 Latitude of point 2 in degrees
#' @param lon2 Longitude of point 2 in degrees
#' @param unit Distance unit: "km", "miles", or "meters"
#' @return Distance between the two points
#' @examples
#' # Distance between New York and Los Angeles
#' haversine_distance(40.7128, -74.0060, 34.0522, -118.2437, "miles")
#' # Distance between London and Paris
#' haversine_distance(51.5074, -0.1278, 48.8566, 2.3522, "km")
haversine_distance <- function(lat1, lon1, lat2, lon2, unit = "km") {
  # Input validation
  if (!all(is.numeric(c(lat1, lon1, lat2, lon2)))) {
    stop("All coordinates must be numeric")
  }
  
  if (!unit %in% c("km", "miles", "meters")) {
    stop("Unit must be 'km', 'miles', or 'meters'")
  }
  
  # Convert degrees to radians
  lat1_rad <- degrees_to_radians(lat1)
  lat2_rad <- degrees_to_radians(lat2)
  lon1_rad <- degrees_to_radians(lon1)
  lon2_rad <- degrees_to_radians(lon2)
  
  # Differences
  dlat <- lat2_rad - lat1_rad
  dlon <- lon2_rad - lon1_rad
  
  # Haversine formula
  a <- sin(dlat / 2)^2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2)^2
  c <- 2 * asin(sqrt(a))
  
  # Select radius based on unit
  radius <- switch(unit,
    "km" = EARTH_RADIUS_KM,
    "miles" = EARTH_RADIUS_MILES,
    "meters" = EARTH_RADIUS_METERS
  )
  
  return(radius * c)
}

#' Calculate distance between two points (vectorized)
#' @param points Matrix or data.frame with columns: lat1, lon1, lat2, lon2
#' @param unit Distance unit: "km", "miles", or "meters"
#' @return Vector of distances
#' @examples
#' df <- data.frame(
#'   lat1 = c(40.7128, 51.5074),
#'   lon1 = c(-74.0060, -0.1278),
#'   lat2 = c(34.0522, 48.8566),
#'   lon2 = c(-118.2437, 2.3522)
#' )
#' haversine_distance_batch(df, "km")
haversine_distance_batch <- function(points, unit = "km") {
  if (!is.data.frame(points) && !is.matrix(points)) {
    stop("points must be a data.frame or matrix with lat1, lon1, lat2, lon2 columns")
  }
  
  if (is.matrix(points)) {
    points <- as.data.frame(points)
  }
  
  required_cols <- c("lat1", "lon1", "lat2", "lon2")
  if (!all(required_cols %in% names(points))) {
    stop("points must contain columns: lat1, lon1, lat2, lon2")
  }
  
  mapply(haversine_distance, 
         points$lat1, points$lon1, points$lat2, points$lon2,
         MoreArgs = list(unit = unit))
}

#' Find the nearest point from a list of candidates
#' @param ref_lat Reference point latitude
#' @param ref_lon Reference point longitude
#' @param candidates Matrix or data.frame with lat and lon columns
#' @param unit Distance unit: "km", "miles", or "meters"
#' @return List with index, distance, and coordinates of nearest point
#' @examples
#' candidates <- data.frame(
#'   lat = c(34.05, 40.71, 41.87),
#'   lon = c(-118.24, -74.00, -87.62)
#' )
#' find_nearest(41.87, -87.62, candidates, "km")
find_nearest <- function(ref_lat, ref_lon, candidates, unit = "km") {
  if (!is.data.frame(candidates) && !is.matrix(candidates)) {
    stop("candidates must be a data.frame or matrix with lat and lon columns")
  }
  
  if (is.matrix(candidates)) {
    candidates <- as.data.frame(candidates)
  }
  
  if (!all(c("lat", "lon") %in% names(candidates))) {
    stop("candidates must contain 'lat' and 'lon' columns")
  }
  
  distances <- mapply(haversine_distance,
                     ref_lat, ref_lon,
                     candidates$lat, candidates$lon,
                     MoreArgs = list(unit = unit))
  
  nearest_idx <- which.min(distances)
  
  return(list(
    index = nearest_idx,
    distance = distances[nearest_idx],
    lat = candidates$lat[nearest_idx],
    lon = candidates$lon[nearest_idx]
  ))
}

#' Find all points within a given radius
#' @param ref_lat Reference point latitude
#' @param ref_lon Reference point longitude
#' @param candidates Matrix or data.frame with lat and lon columns
#' @param radius Radius to search within
#' @param unit Distance unit: "km", "miles", or "meters"
#' @return data.frame with indices, distances, and coordinates of points within radius
#' @examples
#' candidates <- data.frame(
#'   lat = c(34.05, 40.71, 41.87),
#'   lon = c(-118.24, -74.00, -87.62),
#'   name = c("LA", "NYC", "Chicago")
#' )
#' within_radius(41.87, -87.62, candidates, 1500, "km")
within_radius <- function(ref_lat, ref_lon, candidates, radius, unit = "km") {
  if (!is.data.frame(candidates) && !is.matrix(candidates)) {
    stop("candidates must be a data.frame or matrix with lat and lon columns")
  }
  
  if (is.matrix(candidates)) {
    candidates <- as.data.frame(candidates)
  }
  
  if (!all(c("lat", "lon") %in% names(candidates))) {
    stop("candidates must contain 'lat' and 'lon' columns")
  }
  
  distances <- mapply(haversine_distance,
                     ref_lat, ref_lon,
                     candidates$lat, candidates$lon,
                     MoreArgs = list(unit = unit))
  
  within_idx <- which(distances <= radius)
  
  if (length(within_idx) == 0) {
    return(data.frame(
      index = integer(0),
      distance = numeric(0),
      lat = numeric(0),
      lon = numeric(0)
    ))
  }
  
  result <- data.frame(
    index = within_idx,
    distance = distances[within_idx],
    lat = candidates$lat[within_idx],
    lon = candidates$lon[within_idx]
  )
  
  # Add any additional columns from candidates
  extra_cols <- setdiff(names(candidates), c("lat", "lon"))
  if (length(extra_cols) > 0) {
    result <- cbind(result, candidates[within_idx, extra_cols, drop = FALSE])
  }
  
  return(result)
}

#' Calculate the bounding box for a given center point and radius
#' Useful for database queries to limit search area
#' @param lat Center latitude
#' @param lon Center longitude
#' @param radius Radius around the center
#' @param unit Distance unit: "km", "miles", or "meters"
#' @return List with min_lat, max_lat, min_lon, max_lon
#' @examples
#' bbox <- bounding_box(40.7128, -74.0060, 50, "km")
#' # Can be used in SQL: WHERE lat BETWEEN bbox$min_lat AND bbox$max_lat
bounding_box <- function(lat, lon, radius, unit = "km") {
  # Convert radius to km for calculation
  radius_km <- switch(unit,
    "km" = radius,
    "miles" = radius * 1.60934,
    "meters" = radius / 1000
  )
  
  # Approximate degrees per km (varies with latitude)
  lat_degree_km <- 111.32  # approximately constant
  lon_degree_km <- 111.32 * cos(degrees_to_radians(lat))
  
  # Calculate deltas
  lat_delta <- radius_km / lat_degree_km
  lon_delta <- radius_km / lon_degree_km
  
  return(list(
    min_lat = lat - lat_delta,
    max_lat = lat + lat_delta,
    min_lon = lon - lon_delta,
    max_lon = lon + lon_delta
  ))
}

#' Calculate the midpoint between two coordinates
#' @param lat1 Latitude of point 1
#' @param lon1 Longitude of point 1
#' @param lat2 Latitude of point 2
#' @param lon2 Longitude of point 2
#' @return List with lat and lon of the midpoint
#' @examples
#' midpoint(40.7128, -74.0060, 34.0522, -118.2437)
midpoint <- function(lat1, lon1, lat2, lon2) {
  if (!all(is.numeric(c(lat1, lon1, lat2, lon2)))) {
    stop("All coordinates must be numeric")
  }
  
  # Convert to radians
  lat1_rad <- degrees_to_radians(lat1)
  lat2_rad <- degrees_to_radians(lat2)
  lon1_rad <- degrees_to_radians(lon1)
  lon2_rad <- degrees_to_radians(lon2)
  
  dlon <- lon2_rad - lon1_rad
  
  # Calculate midpoint
  bx <- cos(lat2_rad) * cos(dlon)
  by <- cos(lat2_rad) * sin(dlon)
  
  lat_mid <- atan2(sin(lat1_rad) + sin(lat2_rad),
                   sqrt((cos(lat1_rad) + bx)^2 + by^2))
  lon_mid <- lon1_rad + atan2(by, cos(lat1_rad) + bx)
  
  return(list(
    lat = radians_to_degrees(lat_mid),
    lon = radians_to_degrees(lon_mid)
  ))
}

#' Calculate the initial bearing from point 1 to point 2
#' @param lat1 Latitude of point 1
#' @param lon1 Longitude of point 1
#' @param lat2 Latitude of point 2
#' @param lon2 Longitude of point 2
#' @return Bearing in degrees (0-360, where 0 is North)
#' @examples
#' bearing(40.7128, -74.0060, 34.0522, -118.2437)
bearing <- function(lat1, lon1, lat2, lon2) {
  if (!all(is.numeric(c(lat1, lon1, lat2, lon2)))) {
    stop("All coordinates must be numeric")
  }
  
  lat1_rad <- degrees_to_radians(lat1)
  lat2_rad <- degrees_to_radians(lat2)
  dlon <- degrees_to_radians(lon2 - lon1)
  
  x <- sin(dlon) * cos(lat2_rad)
  y <- cos(lat1_rad) * sin(lat2_rad) - 
      sin(lat1_rad) * cos(lat2_rad) * cos(dlon)
  
  bearing_rad <- atan2(x, y)
  bearing_deg <- radians_to_degrees(bearing_rad)
  
  # Normalize to 0-360
  return((bearing_deg + 360) %% 360)
}

#' Convert bearing to compass direction
#' @param bearing Bearing in degrees (0-360)
#' @return Compass direction string (N, NE, E, SE, S, SW, W, NW)
#' @examples
#' bearing_to_compass(45)   # "NE"
#' bearing_to_compass(180) # "S"
bearing_to_compass <- function(bearing) {
  if (!is.numeric(bearing) || bearing < 0 || bearing > 360) {
    stop("Bearing must be numeric between 0 and 360")
  }
  
  directions <- c("N", "NE", "E", "SE", "S", "SW", "W", "NW")
  index <- round(bearing / 45) %% 8 + 1
  return(directions[index])
}

#' Destination point given start, bearing, and distance
#' @param lat Starting latitude
#' @param lon Starting longitude
#' @param bearing Bearing in degrees
#' @param distance Distance to travel
#' @param unit Distance unit: "km", "miles", or "meters"
#' @return List with lat and lon of destination
#' @examples
#' dest <- destination_point(40.7128, -74.0060, 45, 100, "km")
destination_point <- function(lat, lon, bearing, distance, unit = "km") {
  if (!all(is.numeric(c(lat, lon, bearing, distance)))) {
    stop("All inputs must be numeric")
  }
  
  # Convert distance to km
  distance_km <- switch(unit,
    "km" = distance,
    "miles" = distance * 1.60934,
    "meters" = distance / 1000
  )
  
  # Angular distance
  d <- distance_km / EARTH_RADIUS_KM
  
  lat_rad <- degrees_to_radians(lat)
  lon_rad <- degrees_to_radians(lon)
  brng_rad <- degrees_to_radians(bearing)
  
  # Calculate destination
  lat_dest <- asin(sin(lat_rad) * cos(d) + 
                   cos(lat_rad) * sin(d) * cos(brng_rad))
  
  lon_dest <- lon_rad + atan2(sin(brng_rad) * sin(d) * cos(lat_rad),
                              cos(d) - sin(lat_rad) * sin(lat_dest))
  
  return(list(
    lat = radians_to_degrees(lat_dest),
    lon = radians_to_degrees(lon_dest)
  ))
}

#' Calculate total distance of a path
#' @param path Matrix or data.frame with lat and lon columns in order
#' @param unit Distance unit: "km", "miles", or "meters"
#' @return Total distance along the path
#' @examples
#' path <- data.frame(
#'   lat = c(40.71, 41.87, 34.05),
#'   lon = c(-74.00, -87.62, -118.24)
#' )
#' path_distance(path, "km")
path_distance <- function(path, unit = "km") {
  if (!is.data.frame(path) && !is.matrix(path)) {
    stop("path must be a data.frame or matrix with lat and lon columns")
  }
  
  if (is.matrix(path)) {
    path <- as.data.frame(path)
  }
  
  if (!all(c("lat", "lon") %in% names(path))) {
    stop("path must contain 'lat' and 'lon' columns")
  }
  
  if (nrow(path) < 2) {
    return(0)
  }
  
  total <- 0
  for (i in 1:(nrow(path) - 1)) {
    total <- total + haversine_distance(
      path$lat[i], path$lon[i],
      path$lat[i + 1], path$lon[i + 1],
      unit
    )
  }
  
  return(total)
}

#' Validate latitude value
#' @param lat Latitude value to validate
#' @return TRUE if valid, FALSE otherwise
#' @examples
#' is_valid_latitude(45)    # TRUE
#' is_valid_latitude(91)    # FALSE
is_valid_latitude <- function(lat) {
  return(is.numeric(lat) && lat >= -90 && lat <= 90)
}

#' Validate longitude value
#' @param lon Longitude value to validate
#' @return TRUE if valid, FALSE otherwise
#' @examples
#' is_valid_longitude(180)   # TRUE
#' is_valid_longitude(181)   # FALSE
is_valid_longitude <- function(lon) {
  return(is.numeric(lon) && lon >= -180 && lon <= 180)
}

#' Normalize longitude to -180 to 180 range
#' @param lon Longitude value
#' @return Normalized longitude
#' @examples
#' normalize_longitude(270)  # Returns -90
normalize_longitude <- function(lon) {
  if (!is.numeric(lon)) {
    stop("Input must be numeric")
  }
  return(((lon + 180) %% 360) - 180)
}

#' Get cardinal direction text from bearing
#' @param bearing Bearing in degrees
#' @return Full cardinal direction text
#' @examples
#' get_direction_text(45)   # "North East"
get_direction_text <- function(bearing) {
  compass <- bearing_to_compass(bearing)
  
  direction_map <- list(
    "N" = "North",
    "NE" = "North East",
    "E" = "East",
    "SE" = "South East",
    "S" = "South",
    "SW" = "South West",
    "W" = "West",
    "NW" = "North West"
  )
  
  return(direction_map[[compass]])
}