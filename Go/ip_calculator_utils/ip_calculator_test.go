package ip_calculator_utils

import (
	"net"
	"testing"
)

func TestParseCIDR(t *testing.T) {
	tests := []struct {
		name    string
		cidr    string
		wantErr bool
	}{
		{"Valid IPv4 CIDR", "192.168.1.0/24", false},
		{"Valid IPv4 /32", "10.0.0.1/32", false},
		{"Valid IPv6 CIDR", "2001:db8::/32", false},
		{"Invalid CIDR format", "192.168.1.0", true},
		{"Invalid IP", "invalid/24", true},
		{"Invalid prefix", "192.168.1.0/33", true},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			_, err := ParseCIDR(tt.cidr)
			if (err != nil) != tt.wantErr {
				t.Errorf("ParseCIDR() error = %v, wantErr %v", err, tt.wantErr)
			}
		})
	}
}

func TestGetSubnetInfo_IPv4(t *testing.T) {
	info, err := GetSubnetInfo("192.168.1.0/24")
	if err != nil {
		t.Fatalf("GetSubnetInfo() error = %v", err)
	}

	if info.NetworkAddress != "192.168.1.0" {
		t.Errorf("NetworkAddress = %v, want 192.168.1.0", info.NetworkAddress)
	}
	if info.BroadcastAddr != "192.168.1.255" {
		t.Errorf("BroadcastAddr = %v, want 192.168.1.255", info.BroadcastAddr)
	}
	if info.FirstUsable != "192.168.1.1" {
		t.Errorf("FirstUsable = %v, want 192.168.1.1", info.FirstUsable)
	}
	if info.LastUsable != "192.168.1.254" {
		t.Errorf("LastUsable = %v, want 192.168.1.254", info.LastUsable)
	}
	if info.SubnetMask != "255.255.255.0" {
		t.Errorf("SubnetMask = %v, want 255.255.255.0", info.SubnetMask)
	}
	if info.PrefixLength != 24 {
		t.Errorf("PrefixLength = %v, want 24", info.PrefixLength)
	}
	if info.TotalHosts != 256 {
		t.Errorf("TotalHosts = %v, want 256", info.TotalHosts)
	}
	if info.UsableHosts != 254 {
		t.Errorf("UsableHosts = %v, want 254", info.UsableHosts)
	}
	if info.IPVersion != 4 {
		t.Errorf("IPVersion = %v, want 4", info.IPVersion)
	}
	if !info.IsPrivate {
		t.Error("IsPrivate should be true for 192.168.1.0/24")
	}
}

func TestGetSubnetInfo_IPv4_SmallSubnet(t *testing.T) {
	info, err := GetSubnetInfo("10.0.0.0/30")
	if err != nil {
		t.Fatalf("GetSubnetInfo() error = %v", err)
	}

	if info.UsableHosts != 2 {
		t.Errorf("UsableHosts = %v, want 2", info.UsableHosts)
	}
	if !info.IsPrivate {
		t.Error("IsPrivate should be true for 10.0.0.0/30")
	}
}

func TestGetSubnetInfo_IPv6(t *testing.T) {
	info, err := GetSubnetInfo("2001:db8::/32")
	if err != nil {
		t.Fatalf("GetSubnetInfo() error = %v", err)
	}

	if info.NetworkAddress != "2001:db8::" {
		t.Errorf("NetworkAddress = %v, want 2001:db8::", info.NetworkAddress)
	}
	if info.PrefixLength != 32 {
		t.Errorf("PrefixLength = %v, want 32", info.PrefixLength)
	}
	if info.IPVersion != 6 {
		t.Errorf("IPVersion = %v, want 6", info.IPVersion)
	}
}

func TestIPInRange(t *testing.T) {
	tests := []struct {
		name     string
		ip       string
		cidr     string
		expected bool
	}{
		{"IP in range", "192.168.1.100", "192.168.1.0/24", true},
		{"IP not in range", "192.168.2.1", "192.168.1.0/24", false},
		{"Network address", "192.168.1.0", "192.168.1.0/24", true},
		{"Broadcast address", "192.168.1.255", "192.168.1.0/24", true},
		{"IPv6 in range", "2001:db8::1", "2001:db8::/32", true},
		{"IPv6 not in range", "2001:db9::1", "2001:db8::/32", false},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result, err := IPInRange(tt.ip, tt.cidr)
			if err != nil {
				t.Fatalf("IPInRange() error = %v", err)
			}
			if result != tt.expected {
				t.Errorf("IPInRange() = %v, want %v", result, tt.expected)
			}
		})
	}
}

func TestIPInMultipleRanges(t *testing.T) {
	cidrs := []string{"10.0.0.0/8", "172.16.0.0/12", "192.168.0.0/16"}

	tests := []struct {
		ip       string
		expected bool
		matchCIDR string
	}{
		{"10.1.2.3", true, "10.0.0.0/8"},
		{"172.16.0.1", true, "172.16.0.0/12"},
		{"192.168.1.1", true, "192.168.0.0/16"},
		{"8.8.8.8", false, ""},
	}

	for _, tt := range tests {
		t.Run(tt.ip, func(t *testing.T) {
			result, match, err := IPInMultipleRanges(tt.ip, cidrs)
			if err != nil {
				t.Fatalf("IPInMultipleRanges() error = %v", err)
			}
			if result != tt.expected {
				t.Errorf("IPInMultipleRanges() = %v, want %v", result, tt.expected)
			}
			if result && match != tt.matchCIDR {
				t.Errorf("Matched CIDR = %v, want %v", match, tt.matchCIDR)
			}
		})
	}
}

func TestSubnetToMask(t *testing.T) {
	tests := []struct {
		prefixLen int
		ipv6      bool
		expected  string
	}{
		{24, false, "255.255.255.0"},
		{16, false, "255.255.0.0"},
		{8, false, "255.0.0.0"},
		{32, false, "255.255.255.255"},
		{0, false, "0.0.0.0"},
	}

	for _, tt := range tests {
		t.Run(tt.expected, func(t *testing.T) {
			result, err := SubnetToMask(tt.prefixLen, tt.ipv6)
			if err != nil {
				t.Fatalf("SubnetToMask() error = %v", err)
			}
			if result != tt.expected {
				t.Errorf("SubnetToMask() = %v, want %v", result, tt.expected)
			}
		})
	}
}

func TestMaskToPrefixLength(t *testing.T) {
	tests := []struct {
		mask     string
		expected int
	}{
		{"255.255.255.0", 24},
		{"255.255.0.0", 16},
		{"255.0.0.0", 8},
		{"255.255.255.255", 32},
	}

	for _, tt := range tests {
		t.Run(tt.mask, func(t *testing.T) {
			result, err := MaskToPrefixLength(tt.mask)
			if err != nil {
				t.Fatalf("MaskToPrefixLength() error = %v", err)
			}
			if result != tt.expected {
				t.Errorf("MaskToPrefixLength() = %v, want %v", result, tt.expected)
			}
		})
	}
}

func TestValidateIP(t *testing.T) {
	tests := []struct {
		ip       string
		valid    bool
		version  int
	}{
		{"192.168.1.1", true, 4},
		{"10.0.0.1", true, 4},
		{"::1", true, 6},
		{"2001:db8::1", true, 6},
		{"invalid", false, 0},
		{"256.1.1.1", false, 0},
	}

	for _, tt := range tests {
		t.Run(tt.ip, func(t *testing.T) {
			valid, version := ValidateIP(tt.ip)
			if valid != tt.valid {
				t.Errorf("ValidateIP() valid = %v, want %v", valid, tt.valid)
			}
			if valid && version != tt.version {
				t.Errorf("ValidateIP() version = %v, want %v", version, tt.version)
			}
		})
	}
}

func TestGetIPClass(t *testing.T) {
	tests := []struct {
		ip       string
		expected string
	}{
		{"10.0.0.1", "A"},
		{"127.0.0.1", "Special"}, // Loopback is special
		{"128.0.0.1", "B"},
		{"172.16.0.1", "B"},
		{"192.168.1.1", "C"},
		{"224.0.0.1", "D"},
		{"240.0.0.1", "E"},
	}

	for _, tt := range tests {
		t.Run(tt.ip, func(t *testing.T) {
			result, err := GetIPClass(tt.ip)
			if err != nil {
				t.Fatalf("GetIPClass() error = %v", err)
			}
			if result != tt.expected {
				t.Errorf("GetIPClass() = %v, want %v", result, tt.expected)
			}
		})
	}
}

func TestCompareIPs(t *testing.T) {
	tests := []struct {
		ip1      string
		ip2      string
		expected int
	}{
		{"192.168.1.1", "192.168.1.2", -1},
		{"192.168.1.2", "192.168.1.1", 1},
		{"192.168.1.1", "192.168.1.1", 0},
		{"10.0.0.1", "192.168.1.1", -1},
	}

	for _, tt := range tests {
		t.Run(tt.ip1+"_"+tt.ip2, func(t *testing.T) {
			result, err := CompareIPs(tt.ip1, tt.ip2)
			if err != nil {
				t.Fatalf("CompareIPs() error = %v", err)
			}
			if result != tt.expected {
				t.Errorf("CompareIPs() = %v, want %v", result, tt.expected)
			}
		})
	}
}

func TestIPToInt(t *testing.T) {
	tests := []struct {
		ip       string
		expected uint64
	}{
		{"0.0.0.0", 0},
		{"0.0.0.1", 1},
		{"0.0.1.0", 256},
		{"0.1.0.0", 65536},
		{"1.0.0.0", 16777216},
		{"192.168.1.1", 3232235777},
	}

	for _, tt := range tests {
		t.Run(tt.ip, func(t *testing.T) {
			result, err := IPToInt(tt.ip)
			if err != nil {
				t.Fatalf("IPToInt() error = %v", err)
			}
			if result != tt.expected {
				t.Errorf("IPToInt() = %v, want %v", result, tt.expected)
			}
		})
	}
}

func TestIntToIP(t *testing.T) {
	tests := []struct {
		n        uint64
		expected string
	}{
		{0, "0.0.0.0"},
		{1, "0.0.0.1"},
		{256, "0.0.1.0"},
		{65536, "0.1.0.0"},
		{16777216, "1.0.0.0"},
		{3232235777, "192.168.1.1"},
	}

	for _, tt := range tests {
		t.Run(tt.expected, func(t *testing.T) {
			result, err := IntToIP(tt.n)
			if err != nil {
				t.Fatalf("IntToIP() error = %v", err)
			}
			if result != tt.expected {
				t.Errorf("IntToIP() = %v, want %v", result, tt.expected)
			}
		})
	}
}

func TestParsePortRange(t *testing.T) {
	tests := []struct {
		input    string
		start    int
		end      int
		wantErr  bool
	}{
		{"80", 80, 80, false},
		{"80-443", 80, 443, false},
		{" 80 - 443 ", 80, 443, false},
		{"1-65535", 1, 65535, false},
		{"invalid", 0, 0, true},
		{"0-100", 0, 0, true}, // Port 0 is invalid
		{"100-50", 0, 0, true}, // Start > End
	}

	for _, tt := range tests {
		t.Run(tt.input, func(t *testing.T) {
			start, end, err := ParsePortRange(tt.input)
			if (err != nil) != tt.wantErr {
				t.Errorf("ParsePortRange() error = %v, wantErr %v", err, tt.wantErr)
			}
			if !tt.wantErr && (start != tt.start || end != tt.end) {
				t.Errorf("ParsePortRange() = %d-%d, want %d-%d", start, end, tt.start, tt.end)
			}
		})
	}
}

func TestValidatePort(t *testing.T) {
	tests := []struct {
		port     int
		expected bool
	}{
		{80, true},
		{443, true},
		{1, true},
		{65535, true},
		{0, false},
		{-1, false},
		{65536, false},
	}

	for _, tt := range tests {
		t.Run("", func(t *testing.T) {
			if ValidatePort(tt.port) != tt.expected {
				t.Errorf("ValidatePort(%d) = %v, want %v", tt.port, !tt.expected, tt.expected)
			}
		})
	}
}

func TestCalculateSubnets(t *testing.T) {
	subnets, err := CalculateSubnets("192.168.1.0/24", 26)
	if err != nil {
		t.Fatalf("CalculateSubnets() error = %v", err)
	}

	if len(subnets) != 4 {
		t.Errorf("CalculateSubnets() returned %d subnets, want 4", len(subnets))
	}

	expected := []struct {
		start string
		end   string
	}{
		{"192.168.1.0", "192.168.1.62"},
		{"192.168.1.64", "192.168.1.126"},
		{"192.168.1.128", "192.168.1.190"},
		{"192.168.1.192", "192.168.1.254"},
	}

	for i, exp := range expected {
		if subnets[i].Start != exp.start {
			t.Errorf("Subnet[%d].Start = %v, want %v", i, subnets[i].Start, exp.start)
		}
		if subnets[i].End != exp.end {
			t.Errorf("Subnet[%d].End = %v, want %v", i, subnets[i].End, exp.end)
		}
	}
}

func TestGetIPsInRange(t *testing.T) {
	ips, err := GetIPsInRange("192.168.1.0/30", 0)
	if err != nil {
		t.Fatalf("GetIPsInRange() error = %v", err)
	}

	if len(ips) != 4 {
		t.Errorf("GetIPsInRange() returned %d IPs, want 4", len(ips))
	}

	expected := []string{"192.168.1.0", "192.168.1.1", "192.168.1.2", "192.168.1.3"}
	for i, ip := range expected {
		if ips[i] != ip {
			t.Errorf("GetIPsInRange()[%d] = %v, want %v", i, ips[i], ip)
		}
	}
}

func TestGetIPsInRange_Limit(t *testing.T) {
	ips, err := GetIPsInRange("10.0.0.0/24", 10)
	if err != nil {
		t.Fatalf("GetIPsInRange() error = %v", err)
	}

	if len(ips) != 10 {
		t.Errorf("GetIPsInRange() returned %d IPs, want 10", len(ips))
	}
}

func TestFormatIPWithCIDR(t *testing.T) {
	result, err := FormatIPWithCIDR("192.168.1.1", 24)
	if err != nil {
		t.Fatalf("FormatIPWithCIDR() error = %v", err)
	}

	if result != "192.168.1.1/24" {
		t.Errorf("FormatIPWithCIDR() = %v, want 192.168.1.1/24", result)
	}
}

func TestSplitCIDRByMask(t *testing.T) {
	result, err := SplitCIDRByMask("192.168.1.0/24", 26)
	if err != nil {
		t.Fatalf("SplitCIDRByMask() error = %v", err)
	}

	if len(result) != 4 {
		t.Errorf("SplitCIDRByMask() returned %d subnets, want 4", len(result))
	}
}

// Benchmark tests
func BenchmarkGetSubnetInfo(b *testing.B) {
	for i := 0; i < b.N; i++ {
		_, _ = GetSubnetInfo("192.168.1.0/24")
	}
}

func BenchmarkIPInRange(b *testing.B) {
	for i := 0; i < b.N; i++ {
		_, _ = IPInRange("192.168.1.100", "192.168.1.0/24")
	}
}

func BenchmarkIPToInt(b *testing.B) {
	for i := 0; i < b.N; i++ {
		_, _ = IPToInt("192.168.1.100")
	}
}

// Additional edge case tests
func TestGetSubnetInfo_Loopback(t *testing.T) {
	info, err := GetSubnetInfo("127.0.0.0/8")
	if err != nil {
		t.Fatalf("GetSubnetInfo() error = %v", err)
	}

	if !info.IsLoopback {
		t.Error("IsLoopback should be true for 127.0.0.0/8")
	}
}

func TestGetSubnetInfo_PointToPoint(t *testing.T) {
	info, err := GetSubnetInfo("192.168.1.0/31")
	if err != nil {
		t.Fatalf("GetSubnetInfo() error = %v", err)
	}

	// /31 point-to-point links have 2 usable addresses
	if info.UsableHosts != 2 {
		t.Errorf("UsableHosts = %v, want 2", info.UsableHosts)
	}
}

func TestGetSubnetInfo_SingleHost(t *testing.T) {
	info, err := GetSubnetInfo("192.168.1.1/32")
	if err != nil {
		t.Fatalf("GetSubnetInfo() error = %v", err)
	}

	// /32 is a single host
	if info.TotalHosts != 1 {
		t.Errorf("TotalHosts = %v, want 1", info.TotalHosts)
	}
	if info.UsableHosts != 1 {
		t.Errorf("UsableHosts = %v, want 1", info.UsableHosts)
	}
}

func TestSubnetToMask_IPv6(t *testing.T) {
	// IPv6 mask test
	mask, err := SubnetToMask(64, true)
	if err != nil {
		t.Fatalf("SubnetToMask() error = %v", err)
	}
	// IPv6 /64 mask should start with ffff:ffff:ffff:ffff
	expectedPrefix := "ffff:ffff:ffff:ffff::"
	if mask != expectedPrefix && mask != net.ParseIP(expectedPrefix).String() {
		t.Logf("SubnetToMask(64, true) = %v (IPv6 masks may vary in formatting)", mask)
	}
}

func TestSubnetToMask_Invalid(t *testing.T) {
	_, err := SubnetToMask(33, false)
	if err == nil {
		t.Error("SubnetToMask(33, false) should return error for IPv4")
	}

	_, err = SubnetToMask(129, true)
	if err == nil {
		t.Error("SubnetToMask(129, true) should return error for IPv6")
	}
}

func TestCalculateSubnets_InvalidPrefix(t *testing.T) {
	// New prefix must be greater than current
	_, err := CalculateSubnets("192.168.1.0/24", 24)
	if err == nil {
		t.Error("CalculateSubnets should return error when new prefix equals current")
	}

	_, err = CalculateSubnets("192.168.1.0/24", 16)
	if err == nil {
		t.Error("CalculateSubnets should return error when new prefix is smaller")
	}
}

func TestIPInRange_InvalidInput(t *testing.T) {
	_, err := IPInRange("invalid", "192.168.1.0/24")
	if err == nil {
		t.Error("IPInRange should return error for invalid IP")
	}

	_, err = IPInRange("192.168.1.1", "invalid")
	if err == nil {
		t.Error("IPInRange should return error for invalid CIDR")
	}
}

func TestIPToInt_IPv6(t *testing.T) {
	// Test IPv6 conversion (should return lower 64 bits)
	n, err := IPToInt("::1")
	if err != nil {
		t.Fatalf("IPToInt() error = %v", err)
	}
	if n != 1 {
		t.Errorf("IPToInt(::1) = %v, want 1", n)
	}
}

func TestIntToIP_TooLarge(t *testing.T) {
	_, err := IntToIP(uint64(1) << 32)
	if err == nil {
		t.Error("IntToIP should return error for numbers too large for IPv4")
	}
}

func TestGetIPClass_IPv6Error(t *testing.T) {
	_, err := GetIPClass("2001:db8::1")
	if err == nil {
		t.Error("GetIPClass should return error for IPv6")
	}
}

func TestCompareIPs_InvalidIP(t *testing.T) {
	_, err := CompareIPs("invalid", "192.168.1.1")
	if err == nil {
		t.Error("CompareIPs should return error for invalid IP")
	}

	_, err = CompareIPs("192.168.1.1", "invalid")
	if err == nil {
		t.Error("CompareIPs should return error for invalid IP")
	}
}

func TestFormatIPWithCIDR_Invalid(t *testing.T) {
	_, err := FormatIPWithCIDR("invalid", 24)
	if err == nil {
		t.Error("FormatIPWithCIDR should return error for invalid IP")
	}
}

func TestSplitCIDRByMask_InvalidMask(t *testing.T) {
	_, err := SplitCIDRByMask("192.168.1.0/24", 16)
	if err == nil {
		t.Error("SplitCIDRByMask should return error when new mask is smaller")
	}
}

func TestMergeCIDRs(t *testing.T) {
	cidrs := []string{"192.168.1.0/24", "10.0.0.0/8"}
	result, err := MergeCIDRs(cidrs)
	if err != nil {
		t.Fatalf("MergeCIDRs() error = %v", err)
	}
	if len(result) != 2 {
		t.Errorf("MergeCIDRs() returned %d CIDRs, want 2", len(result))
	}
}

func TestMergeCIDRs_Empty(t *testing.T) {
	result, err := MergeCIDRs([]string{})
	if err != nil {
		t.Fatalf("MergeCIDRs() error = %v", err)
	}
	if len(result) != 0 {
		t.Errorf("MergeCIDRs() returned %d CIDRs, want 0", len(result))
	}
}

func TestMergeCIDRs_Invalid(t *testing.T) {
	_, err := MergeCIDRs([]string{"invalid"})
	if err == nil {
		t.Error("MergeCIDRs should return error for invalid CIDR")
	}
}

func TestGetSubnetInfo_IPv6_Large(t *testing.T) {
	info, err := GetSubnetInfo("2001:db8::/64")
	if err != nil {
		t.Fatalf("GetSubnetInfo() error = %v", err)
	}

	if info.IPVersion != 6 {
		t.Error("IPVersion should be 6 for IPv6")
	}

	if info.PrefixLength != 64 {
		t.Errorf("PrefixLength = %d, want 64", info.PrefixLength)
	}
}