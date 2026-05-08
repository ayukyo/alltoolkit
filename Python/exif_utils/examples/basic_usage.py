#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit EXIF Utilities - Basic Usage Example

This example demonstrates common EXIF extraction tasks.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    extract_exif,
    get_camera_info,
    get_gps_location,
    get_datetime_original,
    has_exif,
    get_all_tags,
    format_exposure_time,
    format_aperture,
    EXIFCleaner,
)


def demo_basic_extraction(filepath: str):
    """Demonstrate basic EXIF extraction."""
    print("=== Basic EXIF Extraction ===\n")
    
    # Check if file has EXIF
    if not has_exif(filepath):
        print("This image has no EXIF data.")
        return
    
    # Extract all EXIF data
    exif = extract_exif(filepath)
    
    print(f"Image Dimensions: {exif.width} x {exif.height}")
    print(f"Orientation: {exif.orientation}")
    
    if exif.make and exif.model:
        print(f"Camera: {exif.make} {exif.model}")
    
    if exif.datetime_original:
        print(f"Taken: {exif.datetime_original}")
    elif exif.datetime:
        print(f"Modified: {exif.datetime}")
    
    if exif.software:
        print(f"Software: {exif.software}")
    
    print()


def demo_camera_settings(filepath: str):
    """Demonstrate camera settings extraction."""
    print("=== Camera Settings ===\n")
    
    settings = get_camera_info(filepath)
    
    if settings is None:
        print("No camera settings found.")
        return
    
    print(f"Camera: {settings.make or 'Unknown'} {settings.model or 'Unknown'}")
    
    if settings.lens_model:
        print(f"Lens: {settings.lens_model}")
    
    if settings.focal_length:
        fl = f"{format_focal_length(settings.focal_length)}"
        if settings.focal_length_35mm:
            fl += f" (35mm equivalent: {settings.focal_length_35mm}mm)"
        print(f"Focal Length: {fl}")
    
    if settings.aperture:
        print(f"Aperture: {format_aperture(settings.aperture)}")
    
    if settings.shutter_speed:
        print(f"Shutter Speed: {settings.shutter_speed}")
    
    if settings.iso:
        print(f"ISO: {settings.iso}")
    
    if settings.exposure_program:
        print(f"Exposure Program: {settings.exposure_program}")
    
    if settings.metering_mode:
        print(f"Metering Mode: {settings.metering_mode}")
    
    if settings.flash:
        print(f"Flash: {settings.flash}")
    
    if settings.white_balance:
        print(f"White Balance: {settings.white_balance}")
    
    print()


def demo_gps_location(filepath: str):
    """Demonstrate GPS location extraction."""
    print("=== GPS Location ===\n")
    
    gps = get_gps_location(filepath)
    
    if gps is None:
        print("No GPS data found in this image.")
        return
    
    print(f"Latitude: {gps.latitude:.6f}")
    print(f"Longitude: {gps.longitude:.6f}")
    
    if gps.altitude:
        print(f"Altitude: {gps.altitude:.2f} meters")
    
    # Convert to DMS format
    lat_dms, lon_dms = gps.to_dms()
    print(f"\nDMS Format:")
    print(f"  Latitude: {lat_dms}")
    print(f"  Longitude: {lon_dms}")
    
    # Generate map URLs
    print(f"\nMap URLs:")
    print(f"  Google Maps: {gps.to_google_maps_url()}")
    print(f"  OpenStreetMap: {gps.to_openstreetmap_url()}")
    
    print()


def demo_all_tags(filepath: str):
    """Demonstrate extracting all EXIF tags."""
    print("=== All EXIF Tags ===\n")
    
    tags = get_all_tags(filepath)
    
    if not tags:
        print("No EXIF tags found.")
        return
    
    # Group tags by category
    camera_tags = ['Make', 'Model', 'LensModel', 'LensMake', 'LensSpecification']
    exposure_tags = ['ExposureTime', 'FNumber', 'ISOSpeedRatings', 'ApertureValue', 
                     'ShutterSpeedValue', 'ExposureProgram', 'MeteringMode']
    gps_tags = ['GPSLatitude', 'GPSLongitude', 'GPSAltitude', 'GPSLatitudeRef',
                'GPSLongitudeRef', 'GPSAltitudeRef']
    
    print("Camera Tags:")
    for tag in camera_tags:
        if tag in tags:
            print(f"  {tag}: {tags[tag]}")
    
    print("\nExposure Tags:")
    for tag in exposure_tags:
        if tag in tags:
            print(f"  {tag}: {tags[tag]}")
    
    print("\nGPS Tags:")
    for tag in gps_tags:
        if tag in tags:
            print(f"  {tag}: {tags[tag]}")
    
    # Print remaining tags
    remaining = {k: v for k, v in tags.items() 
                 if k not in camera_tags + exposure_tags + gps_tags}
    
    if remaining:
        print("\nOther Tags:")
        for name, value in sorted(remaining.items())[:10]:
            if isinstance(value, bytes):
                value = f"<{len(value)} bytes>"
            print(f"  {name}: {value}")
    
    print(f"\nTotal tags: {len(tags)}")
    print()


def demo_privacy_protection(filepath: str):
    """Demonstrate removing EXIF for privacy."""
    print("=== Privacy Protection ===\n")
    
    # Read original file
    with open(filepath, 'rb') as f:
        original_data = f.read()
    
    original_size = len(original_data)
    
    # Remove all EXIF
    cleaned = EXIFCleaner.remove_exif(original_data)
    cleaned_size = len(cleaned)
    
    print(f"Original size: {original_size} bytes")
    print(f"Cleaned size: {cleaned_size} bytes")
    print(f"Size reduction: {original_size - cleaned_size} bytes")
    
    # Check if cleaned file still has EXIF
    from mod import extract_exif_from_bytes
    
    try:
        cleaned_exif = extract_exif_from_bytes(cleaned)
        if len(cleaned_exif.raw_tags) == 0:
            print("✓ Successfully removed all EXIF data")
        else:
            print(f"⚠ Some tags remaining: {len(cleaned_exif.raw_tags)}")
    except Exception:
        print("✓ No EXIF data in cleaned image")
    
    # Optionally save cleaned file
    # output_path = filepath.replace('.jpg', '_cleaned.jpg')
    # with open(output_path, 'wb') as f:
    #     f.write(cleaned)
    # print(f"Saved cleaned image: {output_path}")
    
    print()


def demo_datetime_extraction(filepath: str):
    """Demonstrate datetime extraction."""
    print("=== DateTime Extraction ===\n")
    
    dt = get_datetime_original(filepath)
    
    if dt is None:
        print("No datetime information found.")
        return
    
    print(f"Capture time: {dt}")
    print(f"ISO format: {dt.isoformat()}")
    print(f"Formatted: {dt.strftime('%B %d, %Y at %I:%M %p')}")
    print()


def main():
    """Main entry point."""
    print("AllToolkit EXIF Utilities - Usage Examples")
    print("=" * 50)
    print()
    
    # Check if a file path was provided
    if len(sys.argv) < 2:
        print("Usage: python basic_usage.py <image_file>")
        print()
        print("This script demonstrates EXIF extraction from image files.")
        print("Provide a JPEG or TIFF image file to extract its EXIF data.")
        return
    
    filepath = sys.argv[1]
    
    if not os.path.exists(filepath):
        print(f"Error: File not found: {filepath}")
        return
    
    print(f"Analyzing: {filepath}")
    print()
    
    # Run demonstrations
    demo_basic_extraction(filepath)
    demo_camera_settings(filepath)
    demo_gps_location(filepath)
    demo_datetime_extraction(filepath)
    demo_all_tags(filepath)
    demo_privacy_protection(filepath)


if __name__ == '__main__':
    main()