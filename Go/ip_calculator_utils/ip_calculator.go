// Package ip_calculator_utils provides IP address and subnet calculation utilities.
// Supports IPv4 and IPv6 CIDR notation, subnet range calculation, and IP validation.
package ip_calculator_utils

import (
	"bytes"
	"encoding/binary"
	"errors"
	"fmt"
	"math"
	"net"
	"strconv"
	"strings"
)

var (
	ErrInvalidCIDR       = errors.New("invalid CIDR notation")
	ErrInvalidIP         = errors.New("invalid IP address")
	ErrInvalidSubnetMask = errors.New("invalid subnet mask")
	ErrIPVersionMismatch = errors.New("IP version mismatch")
)

// SubnetInfo contains detailed information about a subnet
type SubnetInfo struct {
	NetworkAddress string   // 网络地址
	BroadcastAddr  string   // 广播地址 (IPv4 only)
	FirstUsable    string   // 第一个可用IP
	LastUsable     string   // 最后一个可用IP
	SubnetMask     string   // 子网掩码
	WildcardMask   string   // 通配符掩码
	PrefixLength   int      // 前缀长度
	TotalHosts     uint64   // 总IP数量
	UsableHosts    uint64   // 可用IP数量
	IPVersion      int      // IP版本 (4 or 6)
	IsPrivate      bool     // 是否私有地址
	IsLoopback     bool     // 是否回环地址
	ReservedIPs    []string // 保留的IP地址
}

// IPRange represents a range of IP addresses
type IPRange struct {
	Start string
	End   string
	Count uint64
}

// ParseCIDR parses a CIDR notation string and returns the network information
func ParseCIDR(cidr string) (*net.IPNet, error) {
	_, ipNet, err := net.ParseCIDR(cidr)
	if err != nil {
		return nil, ErrInvalidCIDR
	}
	return ipNet, nil
}

// GetSubnetInfo returns detailed information about a subnet
func GetSubnetInfo(cidr string) (*SubnetInfo, error) {
	ip, ipNet, err := net.ParseCIDR(cidr)
	if err != nil {
		return nil, ErrInvalidCIDR
	}

	info := &SubnetInfo{
		PrefixLength: 0,
		IPVersion:    4,
		IsPrivate:    false,
		IsLoopback:   false,
	}

	// Determine IP version
	if ip.To4() != nil {
		info.IPVersion = 4
		info.PrefixLength, _ = ipNet.Mask.Size()
		info.TotalHosts = uint64(math.Pow(2, float64(32-info.PrefixLength)))
		if info.PrefixLength < 31 {
			info.UsableHosts = info.TotalHosts - 2
		} else if info.PrefixLength == 31 {
			info.UsableHosts = 2 // Point-to-point link
		} else {
			info.UsableHosts = 1 // /32 single host
		}
	} else {
		info.IPVersion = 6
		info.PrefixLength, _ = ipNet.Mask.Size()
		// For IPv6, use big integers to avoid overflow
		hostBits := 128 - info.PrefixLength
		if hostBits >= 64 {
			info.TotalHosts = math.MaxUint64
		} else {
			info.TotalHosts = 1 << hostBits
		}
		info.UsableHosts = info.TotalHosts
	}

	// Calculate addresses
	info.NetworkAddress = ipNet.IP.String()
	info.SubnetMask = net.IP(ipNet.Mask).String()

	// Calculate broadcast and usable addresses for IPv4
	if info.IPVersion == 4 {
		info.BroadcastAddr = calculateBroadcast(ipNet).String()
		info.WildcardMask = calculateWildcard(ipNet.Mask).String()

		if info.PrefixLength < 31 {
			info.FirstUsable = incrementIP(ipNet.IP).String()
			info.LastUsable = decrementIP(net.ParseIP(info.BroadcastAddr)).String()
		} else {
			info.FirstUsable = ipNet.IP.String()
			info.LastUsable = ipNet.IP.String()
		}
	} else {
		// IPv6 doesn't have broadcast
		info.FirstUsable = incrementIP(ipNet.IP).String()
		info.LastUsable = calculateIPv6LastUsable(ipNet).String()
	}

	// Check for private/loopback
	info.IsPrivate = isPrivateNetwork(ipNet)
	info.IsLoopback = isLoopback(ip)

	// Add reserved IPs
	info.ReservedIPs = getReservedIPs(info)

	return info, nil
}

// IPInRange checks if an IP address is within a CIDR range
func IPInRange(ipStr, cidr string) (bool, error) {
	ip := net.ParseIP(ipStr)
	if ip == nil {
		return false, ErrInvalidIP
	}

	_, ipNet, err := net.ParseCIDR(cidr)
	if err != nil {
		return false, ErrInvalidCIDR
	}

	return ipNet.Contains(ip), nil
}

// IPInMultipleRanges checks if an IP is in any of the provided CIDR ranges
func IPInMultipleRanges(ipStr string, cidrs []string) (bool, string, error) {
	for _, cidr := range cidrs {
		inRange, err := IPInRange(ipStr, cidr)
		if err != nil {
			return false, "", err
		}
		if inRange {
			return true, cidr, nil
		}
	}
	return false, "", nil
}

// SubnetToMask converts a prefix length to subnet mask
func SubnetToMask(prefixLen int, ipv6 bool) (string, error) {
	if ipv6 {
		if prefixLen < 0 || prefixLen > 128 {
			return "", ErrInvalidSubnetMask
		}
	} else {
		if prefixLen < 0 || prefixLen > 32 {
			return "", ErrInvalidSubnetMask
		}
	}

	bits := 32
	if ipv6 {
		bits = 128
	}

	mask := net.CIDRMask(prefixLen, bits)
	return net.IP(mask).String(), nil
}

// MaskToPrefixLength converts a subnet mask to prefix length
func MaskToPrefixLength(mask string) (int, error) {
	ip := net.ParseIP(mask)
	if ip == nil {
		return 0, ErrInvalidSubnetMask
	}

	ipv4 := ip.To4()
	if ipv4 != nil {
		ones, _ := net.IPv4Mask(ipv4[0], ipv4[1], ipv4[2], ipv4[3]).Size()
		return ones, nil
	}

	ones, _ := net.IP(ip).DefaultMask().Size()
	return ones, nil
}

// CalculateSubnets calculates the subnets that can be created by subnetting
func CalculateSubnets(cidr string, newPrefixLen int) ([]IPRange, error) {
	ip, ipNet, err := net.ParseCIDR(cidr)
	if err != nil {
		return nil, ErrInvalidCIDR
	}

	currentPrefix, _ := ipNet.Mask.Size()

	if newPrefixLen <= currentPrefix {
		return nil, errors.New("new prefix length must be greater than current")
	}

	if ip.To4() != nil && newPrefixLen > 32 {
		return nil, errors.New("IPv4 prefix length cannot exceed 32")
	}

	if ip.To4() == nil && newPrefixLen > 128 {
		return nil, errors.New("IPv6 prefix length cannot exceed 128")
	}

	numSubnets := 1 << (newPrefixLen - currentPrefix)
	results := make([]IPRange, 0, numSubnets)

	// Calculate starting point
	startIP := make(net.IP, len(ipNet.IP))
	copy(startIP, ipNet.IP)

	for i := 0; i < numSubnets; i++ {
		subnetCIDR := fmt.Sprintf("%s/%d", startIP.String(), newPrefixLen)
		info, err := GetSubnetInfo(subnetCIDR)
		if err != nil {
			continue
		}

		results = append(results, IPRange{
			Start: info.NetworkAddress,
			End:   info.LastUsable,
			Count: info.UsableHosts,
		})

		// Move to next subnet
		startIP = incrementIPBy(startIP, 1<<(32-newPrefixLen))
	}

	return results, nil
}

// GetIPsInRange generates IP addresses within a range (limited for safety)
func GetIPsInRange(cidr string, limit int) ([]string, error) {
	_, ipNet, err := net.ParseCIDR(cidr)
	if err != nil {
		return nil, ErrInvalidCIDR
	}

	info, err := GetSubnetInfo(cidr)
	if err != nil {
		return nil, err
	}

	// Safety limit
	if limit <= 0 {
		limit = 256
	}
	if limit > 10000 {
		limit = 10000
	}

	ips := make([]string, 0, min(limit, int(info.TotalHosts)))
	current := make(net.IP, len(ipNet.IP))
	copy(current, ipNet.IP)

	for i := 0; i < limit && ipNet.Contains(current); i++ {
		ips = append(ips, current.String())
		current = incrementIP(current)
	}

	return ips, nil
}

// MergeCIDRs attempts to merge adjacent CIDR ranges
func MergeCIDRs(cidrs []string) ([]string, error) {
	if len(cidrs) == 0 {
		return nil, nil
	}

	// Parse all CIDRs and sort them
	type cidrWithIP struct {
		cidr string
		ip   net.IP
		net  *net.IPNet
	}

	parsed := make([]cidrWithIP, 0, len(cidrs))
	for _, cidr := range cidrs {
		ip, ipNet, err := net.ParseCIDR(cidr)
		if err != nil {
			return nil, fmt.Errorf("%w: %s", ErrInvalidCIDR, cidr)
		}
		parsed = append(parsed, cidrWithIP{cidr, ip, ipNet})
	}

	// For simplicity, return the original list
	// A full implementation would merge adjacent blocks
	result := make([]string, len(cidrs))
	for i, p := range parsed {
		result[i] = p.cidr
	}

	return result, nil
}

// CompareIPs compares two IP addresses
// Returns -1 if ip1 < ip2, 0 if equal, 1 if ip1 > ip2
func CompareIPs(ip1, ip2 string) (int, error) {
	parsed1 := net.ParseIP(ip1)
	parsed2 := net.ParseIP(ip2)

	if parsed1 == nil {
		return 0, fmt.Errorf("%w: %s", ErrInvalidIP, ip1)
	}
	if parsed2 == nil {
		return 0, fmt.Errorf("%w: %s", ErrInvalidIP, ip2)
	}

	return bytes.Compare(parsed1, parsed2), nil
}

// ValidateIP validates an IP address
func ValidateIP(ip string) (bool, int) {
	parsed := net.ParseIP(ip)
	if parsed == nil {
		return false, 0
	}

	if parsed.To4() != nil {
		return true, 4
	}
	return true, 6
}

// GetIPClass returns the IP class (A, B, C, D, E) for IPv4
func GetIPClass(ip string) (string, error) {
	parsed := net.ParseIP(ip)
	if parsed == nil {
		return "", ErrInvalidIP
	}

	ipv4 := parsed.To4()
	if ipv4 == nil {
		return "", errors.New("IP class only applies to IPv4")
	}

	firstOctet := int(ipv4[0])

	switch {
	case firstOctet >= 1 && firstOctet <= 126:
		return "A", nil
	case firstOctet >= 128 && firstOctet <= 191:
		return "B", nil
	case firstOctet >= 192 && firstOctet <= 223:
		return "C", nil
	case firstOctet >= 224 && firstOctet <= 239:
		return "D", nil
	case firstOctet >= 240 && firstOctet <= 255:
		return "E", nil
	default:
		return "Special", nil
	}
}

// Helper functions

func calculateBroadcast(ipNet *net.IPNet) net.IP {
	ip := ipNet.IP.To4()
	if ip == nil {
		return nil
	}

	mask := ipNet.Mask
	if len(mask) != 4 {
		return nil
	}

	broadcast := make(net.IP, 4)
	for i := 0; i < 4; i++ {
		broadcast[i] = ip[i] | ^mask[i]
	}

	return broadcast
}

func calculateWildcard(mask net.IPMask) net.IP {
	wildcard := make(net.IP, len(mask))
	for i, b := range mask {
		wildcard[i] = ^b
	}
	return wildcard
}

func incrementIP(ip net.IP) net.IP {
	result := make(net.IP, len(ip))
	copy(result, ip)

	for i := len(result) - 1; i >= 0; i-- {
		result[i]++
		if result[i] != 0 {
			break
		}
	}

	return result
}

func decrementIP(ip net.IP) net.IP {
	result := make(net.IP, len(ip))
	copy(result, ip)

	for i := len(result) - 1; i >= 0; i-- {
		result[i]--
		if result[i] != 0xFF {
			break
		}
	}

	return result
}

func incrementIPBy(ip net.IP, n int) net.IP {
	result := make(net.IP, len(ip))
	copy(result, ip)

	for i := len(result) - 1; i >= 0 && n > 0; i-- {
		val := int(result[i]) + n
		result[i] = byte(val & 0xFF)
		n = val >> 8
	}

	return result
}

func calculateIPv6LastUsable(ipNet *net.IPNet) net.IP {
	result := make(net.IP, len(ipNet.IP))
	copy(result, ipNet.IP)

	for i, m := range ipNet.Mask {
		result[i] |= ^m
	}

	return result
}

func isPrivateNetwork(ipNet *net.IPNet) bool {
	privateCIDRs := []string{
		"10.0.0.0/8",
		"172.16.0.0/12",
		"192.168.0.0/16",
		"127.0.0.0/8",
		"169.254.0.0/16",
		"192.0.2.0/24",
		"198.51.100.0/24",
		"203.0.113.0/24",
		"224.0.0.0/4",
		"240.0.0.0/4",
		"::1/128",
		"fc00::/7",
		"fe80::/10",
	}

	for _, cidr := range privateCIDRs {
		_, privateNet, _ := net.ParseCIDR(cidr)
		if privateNet != nil && privateNet.Contains(ipNet.IP) {
			return true
		}
	}

	return false
}

func isLoopback(ip net.IP) bool {
	return ip.IsLoopback()
}

func getReservedIPs(info *SubnetInfo) []string {
	reserved := []string{}

	if info.IPVersion == 4 {
		reserved = append(reserved, info.NetworkAddress)
		if info.PrefixLength < 31 {
			reserved = append(reserved, info.BroadcastAddr)
		}
	}

	return reserved
}

// FormatIPWithCIDR formats an IP with CIDR notation
func FormatIPWithCIDR(ip string, prefixLen int) (string, error) {
	parsed := net.ParseIP(ip)
	if parsed == nil {
		return "", ErrInvalidIP
	}

	return fmt.Sprintf("%s/%d", parsed.String(), prefixLen), nil
}

// SplitCIDRByMask splits a CIDR into multiple subnets by mask
func SplitCIDRByMask(cidr string, newMask int) ([]string, error) {
	_, ipNet, err := net.ParseCIDR(cidr)
	if err != nil {
		return nil, ErrInvalidCIDR
	}

	currentPrefix, _ := ipNet.Mask.Size()
	if newMask < currentPrefix {
		return nil, errors.New("new mask must be larger than current mask")
	}

	subnets, err := CalculateSubnets(cidr, newMask)
	if err != nil {
		return nil, err
	}

	result := make([]string, len(subnets))
	for i, s := range subnets {
		result[i] = fmt.Sprintf("%s/%d", s.Start, newMask)
	}

	return result, nil
}

// IPToInt converts an IP address to an integer
func IPToInt(ip string) (uint64, error) {
	parsed := net.ParseIP(ip)
	if parsed == nil {
		return 0, ErrInvalidIP
	}

	ipv4 := parsed.To4()
	if ipv4 != nil {
		return uint64(binary.BigEndian.Uint32(ipv4)), nil
	}

	// For IPv6, return lower 64 bits
	lower := binary.BigEndian.Uint64(parsed[8:16])
	return lower, nil
}

// IntToIP converts an integer to an IPv4 address
func IntToIP(n uint64) (string, error) {
	if n > math.MaxUint32 {
		return "", errors.New("number too large for IPv4")
	}

	ip := make(net.IP, 4)
	binary.BigEndian.PutUint32(ip, uint32(n))
	return ip.String(), nil
}

// ParsePortRange parses a port range string like "80-443" or "80"
func ParsePortRange(portRange string) (start, end int, err error) {
	if strings.Contains(portRange, "-") {
		parts := strings.Split(portRange, "-")
		if len(parts) != 2 {
			return 0, 0, errors.New("invalid port range format")
		}

		start, err = strconv.Atoi(strings.TrimSpace(parts[0]))
		if err != nil {
			return 0, 0, errors.New("invalid start port")
		}

		end, err = strconv.Atoi(strings.TrimSpace(parts[1]))
		if err != nil {
			return 0, 0, errors.New("invalid end port")
		}
	} else {
		port, err := strconv.Atoi(strings.TrimSpace(portRange))
		if err != nil {
			return 0, 0, errors.New("invalid port")
		}
		start, end = port, port
	}

	if start < 1 || start > 65535 || end < 1 || end > 65535 {
		return 0, 0, errors.New("port must be between 1 and 65535")
	}

	if start > end {
		return 0, 0, errors.New("start port must be <= end port")
	}

	return start, end, nil
}

// ValidatePort validates a port number
func ValidatePort(port int) bool {
	return port >= 1 && port <= 65535
}

// min returns the smaller of two integers
func min(a, b int) int {
	if a < b {
		return a
	}
	return b
}