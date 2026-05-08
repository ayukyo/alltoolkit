# EXIF Metadata Utilities

Complete EXIF (Exchangeable Image File Format) metadata extraction and manipulation utilities with **zero external dependencies**.

## Features

- **EXIF Data Extraction**: Parse EXIF metadata from JPEG and TIFF images
- **GPS Location Parsing**: Extract GPS coordinates with conversion utilities
- **Camera Settings**: Retrieve camera make, model, lens, and exposure settings
- **DateTime Parsing**: Parse and convert EXIF datetime fields
- **Thumbnail Extraction**: Access embedded thumbnail data
- **EXIF Cleaning**: Remove EXIF or GPS data from images
- **Exposure Calculations**: Calculate EV and equivalent exposures

## Supported Formats

- **JPEG/JFIF**: Full EXIF support via APP1 marker
- **TIFF**: Direct TIFF EXIF parsing

## Installation

No external dependencies required. Uses Python standard library only.

```python
from exif_utils.mod import extract_exif, get_camera_info, get_gps_location
```

## Quick Start

### Extract EXIF Data

```python
from exif_utils.mod import extract_exif

# Extract all EXIF data
exif = extract_exif('photo.jpg')

print(f"Camera: {exif.make} {exif.model}")
print(f"Dimensions: {exif.width}x{exif.height}")
print(f"Taken: {exif.datetime_original}")
```

### Get Camera Settings

```python
from exif_utils.mod import get_camera_info

settings = get_camera_info('photo.jpg')
if settings:
    print(settings)  # Canon EOS R5 | RF 50mm F1.2L | 50mm | f/1.2 | 1/250s | ISO 400
```

### Get GPS Location

```python
from exif_utils.mod import get_gps_location

gps = get_gps_location('photo.jpg')
if gps:
    print(f"Latitude: {gps.latitude}")
    print(f"Longitude: {gps.longitude}")
    print(f"Google Maps: {gps.to_google_maps_url()}")
    
    # Convert to DMS format
    lat_dms, lon_dms = gps.to_dms()
    print(f"DMS: {lat_dms}, {lon_dms}")
```

### Get All Tags

```python
from exif_utils.mod import get_all_tags

tags = get_all_tags('photo.jpg')
for name, value in tags.items():
    print(f"{name}: {value}")
```

## API Reference

### High-Level Functions

#### `extract_exif(file_path: str) -> EXIFData`
Extract all EXIF data from an image file.

#### `extract_exif_from_bytes(data: bytes) -> EXIFData`
Extract EXIF data from image bytes.

#### `get_camera_info(file_path: str) -> Optional[CameraSettings]`
Get camera settings from an image file.

#### `get_gps_location(file_path: str) -> Optional[GPSLocation]`
Get GPS location from an image file.

#### `get_datetime_original(file_path: str) -> Optional[datetime]`
Get the original capture datetime.

#### `has_exif(file_path: str) -> bool`
Check if an image contains EXIF data.

#### `get_tag_value(file_path: str, tag_name: str) -> Any`
Get a specific EXIF tag value by name or hex code.

#### `get_all_tags(file_path: str) -> Dict[str, Any]`
Get all EXIF tags as a named dictionary.

### Formatting Functions

#### `format_exposure_time(seconds: float) -> str`
Format exposure time (e.g., `1/250s`, `2s`).

#### `format_aperture(f_number: float) -> str`
Format aperture (e.g., `f/2.8`).

#### `format_focal_length(mm: float) -> str`
Format focal length (e.g., `50mm`).

### Exposure Calculations

#### `calculate_ev(aperture: float, shutter_speed: float, iso: int) -> float`
Calculate exposure value (EV at ISO 100).

#### `get_equivalent_exposure(...) -> Tuple[float, float, int]`
Calculate equivalent exposure with different settings.

### Classes

#### `EXIFData`
Complete EXIF data container with fields:
- `width`, `height`: Image dimensions
- `orientation`: Orientation value (1-8)
- `make`, `model`: Camera make and model
- `datetime`, `datetime_original`: Capture times
- `camera_settings`: CameraSettings object
- `gps`: GPSLocation object
- `raw_tags`: Raw EXIF tag dictionary
- `thumbnail`: Embedded thumbnail bytes

#### `CameraSettings`
Camera settings container with fields:
- `make`, `model`: Camera info
- `lens_model`: Lens name
- `focal_length`, `focal_length_35mm`: Focal lengths
- `aperture`: F-number
- `shutter_speed`: Exposure time
- `iso`: ISO sensitivity
- `exposure_program`: Program mode
- `metering_mode`: Metering type
- `flash`: Flash status
- `white_balance`: WB setting

#### `GPSLocation`
GPS location with utilities:
- `latitude`, `longitude`, `altitude`: Coordinates
- `to_dms()`: Convert to degrees/minutes/seconds
- `to_google_maps_url()`: Generate Google Maps URL
- `to_openstreetmap_url()`: Generate OSM URL

#### `EXIFCleaner`
Clean EXIF data:
- `remove_exif(data: bytes)`: Remove all EXIF
- `remove_gps(data: bytes)`: Remove GPS only

## CLI Usage

```bash
# Show EXIF summary
python mod.py --summary photo.jpg

# Show GPS coordinates
python mod.py --gps photo.jpg

# Show camera settings
python mod.py --camera photo.jpg

# Show all tags
python mod.py photo.jpg
```

## Examples

### Example 1: Batch GPS Extraction

```python
import os
from exif_utils.mod import get_gps_location, GPSLocation

photos_dir = './photos'
locations = []

for filename in os.listdir(photos_dir):
    if filename.lower().endswith('.jpg'):
        filepath = os.path.join(photos_dir, filename)
        gps = get_gps_location(filepath)
        if gps:
            locations.append({
                'file': filename,
                'lat': gps.latitude,
                'lon': gps.longitude,
                'url': gps.to_google_maps_url()
            })

# Print all locations
for loc in locations:
    print(f"{loc['file']}: {loc['url']}")
```

### Example 2: Exposure Analysis

```python
from exif_utils.mod import extract_exif, calculate_ev

exif = extract_exif('photo.jpg')

if exif.camera_settings:
    settings = exif.camera_settings
    
    # Calculate EV
    ev = calculate_ev(
        settings.aperture,
        float(settings.shutter_speed.split('s')[0].replace('/', '').replace('1', '0.004')),  # Parse shutter
        settings.iso
    )
    
    print(f"Exposure Value: EV {ev:.1f}")
```

### Example 3: Privacy Protection

```python
from exif_utils.mod import EXIFCleaner

# Read original image
with open('photo.jpg', 'rb') as f:
    data = f.read()

# Remove all EXIF for privacy
cleaned = EXIFCleaner.remove_exif(data)

# Save cleaned image
with open('photo_clean.jpg', 'wb') as f:
    f.write(cleaned)

# Or just remove GPS
no_gps = EXIFCleaner.remove_gps(data)
with open('photo_no_location.jpg', 'wb') as f:
    f.write(no_gps)
```

## Testing

Run tests:

```bash
python exif_utils_test.py
```

Run with pytest:

```bash
pytest exif_utils_test.py -v
```

## Limitations

- **EXIF Modification**: Full EXIF writing/modification requires proper TIFF segment rebuilding (not fully implemented)
- **PNG EXIF**: PNG EXIF is not standard; most PNGs don't have EXIF
- **HEIC/HEIF**: Not supported (requires specialized parsing)
- **RAW formats**: Not supported (requires format-specific parsers)

## EXIF Tag Reference

Common EXIF tags:

| Tag Code | Name | Description |
|----------|------|-------------|
| 0x010F | Make | Camera manufacturer |
| 0x0110 | Model | Camera model |
| 0x0112 | Orientation | Image orientation (1-8) |
| 0x0132 | DateTime | Last modified date |
| 0x829A | ExposureTime | Shutter speed |
| 0x829D | FNumber | Aperture |
| 0x8827 | ISOSpeedRatings | ISO value |
| 0x9003 | DateTimeOriginal | Capture date |
| 0x920A | FocalLength | Focal length (mm) |
| 0x0002 | GPSLatitude | GPS latitude |
| 0x0004 | GPSLongitude | GPS longitude |

## License

MIT License - Part of AllToolkit project.

## Author

AllToolkit Team