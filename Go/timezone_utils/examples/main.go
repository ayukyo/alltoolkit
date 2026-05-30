// Examples for timezone_utils package
package main

import (
	"fmt"
	"time"
	"github.com/ayukyo/alltoolkit/go/timezone_utils"
)

func main() {
	fmt.Println("=== Timezone Utils Examples ===\n")

	// 1. Get timezone information
	fmt.Println("1. Get Timezone Info:")
	info, err := timezone_utils.GetTimezoneInfo("America/New_York")
	if err != nil {
		fmt.Printf("Error: %v\n", err)
		return
	}
	fmt.Printf("   Name: %s\n", info.Name)
	fmt.Printf("   Offset: %s\n", info.OffsetString)
	fmt.Printf("   Location: %s\n", info.Location)
	fmt.Printf("   DST Active: %v\n\n", info.Isdst)

	// 2. Convert time between timezones
	fmt.Println("2. Convert Time (NYC -> Tokyo):")
	nyTime := time.Date(2026, 5, 31, 12, 0, 0, 0, time.FixedZone("EST", -5*3600))
	tokyoTime, err := timezone_utils.Convert(nyTime, "America/New_York", "Asia/Tokyo")
	if err != nil {
		fmt.Printf("Error: %v\n", err)
		return
	}
	fmt.Printf("   NYC: %s\n", nyTime.Format("2006-01-02 15:04:05"))
	fmt.Printf("   Tokyo: %s\n\n", tokyoTime.Format("2006-01-02 15:04:05"))

	// 3. Get current time in a timezone
	fmt.Println("3. Current Time in Shanghai:")
	now, err := timezone_utils.Now("Asia/Shanghai")
	if err != nil {
		fmt.Printf("Error: %v\n", err)
		return
	}
	fmt.Printf("   %s\n\n", now.Format("2006-01-02 15:04:05"))

	// 4. Get UTC offset between timezones
	fmt.Println("4. UTC Offset (NYC vs Tokyo):")
	offsetStr, err := timezone_utils.GetOffsetString("America/New_York", "Asia/Tokyo")
	if err != nil {
		fmt.Printf("Error: %v\n", err)
		return
	}
	fmt.Printf("   Tokyo is %s ahead of NYC\n\n", offsetStr)

	// 5. Convert string time between timezones
	fmt.Println("5. Convert String Time:")
	result, err := timezone_utils.ConvertString("2026-05-31 22:30:00", "2006-01-02 15:04:05", "Asia/Shanghai", "America/New_York")
	if err != nil {
		fmt.Printf("Error: %v\n", err)
		return
	}
	fmt.Printf("   Shanghai 22:30 -> NYC %s\n\n", result)

	// 6. Find timezone by city
	fmt.Println("6. Find Timezone by City:")
	zones, err := timezone_utils.FindTimezoneByCity("london")
	if err != nil {
		fmt.Printf("Error: %v\n", err)
		return
	}
	fmt.Printf("   Found: %v\n\n", zones)

	// 7. Check if DST is active
	fmt.Println("7. DST Check:")
	isDST, err := timezone_utils.IsDST("America/New_York")
	if err != nil {
		fmt.Printf("Error: %v\n", err)
		return
	}
	fmt.Printf("   New York DST: %v\n\n", isDST)

	// 8. Get all timezones by continent
	fmt.Println("8. Timezones by Continent:")
	byContinent := timezone_utils.GetTimezonesByContinent()
	for continent, zones := range byContinent {
		fmt.Printf("   %s: %d zones\n", continent, len(zones))
	}
}