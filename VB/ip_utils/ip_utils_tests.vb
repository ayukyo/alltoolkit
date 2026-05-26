' IPUtils Tests - Comprehensive Unit Tests
' Tests for IPv4 address validation, parsing, subnet calculation, and CIDR operations

Imports System
Imports IPUtils

Module IPUtilsTests

    Sub Main()
        Console.WriteLine("=== IPUtils Tests ===")
        Console.WriteLine()

        Dim passed As Integer = 0
        Dim failed As Integer = 0

        ' IPv4Address Tests
        TestIPv4AddressParsing(passed, failed)
        TestIPv4AddressProperties(passed, failed)
        TestIPv4AddressConversion(passed, failed)
        TestIPv4AddressComparison(passed, failed)
        TestIPv4AddressArithmetic(passed, failed)

        ' SubnetMask Tests
        TestSubnetMaskCreation(passed, failed)
        TestSubnetMaskProperties(passed, failed)
        TestSubnetMaskPrefixLength(passed, failed)

        ' IPv4Network Tests
        TestIPv4NetworkCreation(passed, failed)
        TestIPv4NetworkProperties(passed, failed)
        TestIPv4NetworkContains(passed, failed)
        TestIPv4NetworkSplit(passed, failed)

        ' IPAddressParser Tests
        TestIPAddressParser(passed, failed)

        ' IPRange Tests
        TestIPRange(passed, failed)

        ' IPAddressCalculator Tests
        TestIPAddressCalculator(passed, failed)

        ' IPAddressFormatter Tests
        TestIPAddressFormatter(passed, failed)

        Console.WriteLine()
        Console.WriteLine("=== Test Results ===")
        Console.WriteLine("Passed: " & passed)
        Console.WriteLine("Failed: " & failed)
        Console.WriteLine("Total:  " & (passed + failed))
        
        If failed = 0 Then
            Console.WriteLine()
            Console.WriteLine("All tests passed!")
        End If
    End Sub

#Region "IPv4Address Tests"

    Sub TestIPv4AddressParsing(ByRef passed As Integer, ByRef failed As Integer)
        Console.WriteLine("--- IPv4Address Parsing Tests ---")

        ' Test valid parsing
        Dim ip As IPv4Address = IPAddressParser.ParseIPv4("192.168.1.1")
        Assert(ip.Octet1 = 192 AndAlso ip.Octet2 = 168 AndAlso ip.Octet3 = 1 AndAlso ip.Octet4 = 1,
               "Parse 192.168.1.1", passed, failed)

        ' Test TryParse success
        Dim result As IPv4Address
        Dim success As Boolean = IPAddressParser.TryParseIPv4("10.0.0.1", result)
        Assert(success AndAlso result.Octet1 = 10, "TryParse 10.0.0.1", passed, failed)

        ' Test TryParse failure
        success = IPAddressParser.TryParseIPv4("invalid", result)
        Assert(Not success, "TryParse invalid IP", passed, failed)

        ' Test constructor
        ip = New IPv4Address(255, 255, 255, 255)
        Assert(ip.ToString() = "255.255.255.255", "Constructor with bytes", passed, failed)

        ' Test boundary values
        ip = New IPv4Address(0, 0, 0, 0)
        Assert(ip.ToString() = "0.0.0.0", "Parse 0.0.0.0", passed, failed)

        Console.WriteLine()
    End Sub

    Sub TestIPv4AddressProperties(ByRef passed As Integer, ByRef failed As Integer)
        Console.WriteLine("--- IPv4Address Properties Tests ---")

        ' Test class detection
        Dim ip As IPv4Address = IPAddressParser.ParseIPv4("10.0.0.1")
        Assert(ip.GetClass() = "A"c, "Class A detection", passed, failed)

        ip = IPAddressParser.ParseIPv4("172.16.0.1")
        Assert(ip.GetClass() = "B"c, "Class B detection", passed, failed)

        ip = IPAddressParser.ParseIPv4("192.168.1.1")
        Assert(ip.GetClass() = "C"c, "Class C detection", passed, failed)

        ip = IPAddressParser.ParseIPv4("224.0.0.1")
        Assert(ip.GetClass() = "D"c, "Class D detection", passed, failed)

        ip = IPAddressParser.ParseIPv4("240.0.0.1")
        Assert(ip.GetClass() = "E"c, "Class E detection", passed, failed)

        ' Test private detection
        ip = IPAddressParser.ParseIPv4("10.0.0.1")
        Assert(ip.IsPrivate(), "10.x.x.x is private", passed, failed)

        ip = IPAddressParser.ParseIPv4("172.16.0.1")
        Assert(ip.IsPrivate(), "172.16-31.x.x is private", passed, failed)

        ip = IPAddressParser.ParseIPv4("172.15.0.1")
        Assert(Not ip.IsPrivate(), "172.15.x.x is not private", passed, failed)

        ip = IPAddressParser.ParseIPv4("192.168.1.1")
        Assert(ip.IsPrivate(), "192.168.x.x is private", passed, failed)

        ' Test loopback
        ip = IPAddressParser.ParseIPv4("127.0.0.1")
        Assert(ip.IsLoopback(), "127.0.0.1 is loopback", passed, failed)

        ' Test link-local
        ip = IPAddressParser.ParseIPv4("169.254.1.1")
        Assert(ip.IsLinkLocal(), "169.254.x.x is link-local", passed, failed)

        ' Test multicast
        ip = IPAddressParser.ParseIPv4("224.0.0.1")
        Assert(ip.IsMulticast(), "224.x.x.x is multicast", passed, failed)

        ' Test public
        ip = IPAddressParser.ParseIPv4("8.8.8.8")
        Assert(ip.IsPublic(), "8.8.8.8 is public", passed, failed)

        ' Test reserved
        ip = IPAddressParser.ParseIPv4("0.0.0.0")
        Assert(ip.IsReserved(), "0.0.0.0 is reserved", passed, failed)

        ' Test type description
        ip = IPAddressParser.ParseIPv4("127.0.0.1")
        Assert(ip.GetTypeDescription() = "Loopback", "Type description for loopback", passed, failed)

        Console.WriteLine()
    End Sub

    Sub TestIPv4AddressConversion(ByRef passed As Integer, ByRef failed As Integer)
        Console.WriteLine("--- IPv4Address Conversion Tests ---")

        ' Test ToInt32
        Dim ip As IPv4Address = IPAddressParser.ParseIPv4("192.168.1.1")
        Dim intVal As Integer = ip.ToInt32()
        Assert(intVal > 0, "ToInt32 positive", passed, failed)

        ' Test FromInt32
        Dim ip2 As IPv4Address = IPv4Address.FromInt32(intVal)
        Assert(ip = ip2, "FromInt32 roundtrip", passed, failed)

        ' Test ToUInt32
        Dim uintVal As UInteger = ip.ToUInt32()
        Assert(uintVal > 0, "ToUInt32 positive", passed, failed)

        ' Test FromUInt32
        ip2 = IPv4Address.FromUInt32(uintVal)
        Assert(ip = ip2, "FromUInt32 roundtrip", passed, failed)

        ' Test binary string
        ip = IPAddressParser.ParseIPv4("255.255.255.0")
        Dim binary As String = ip.ToBinaryString()
        Assert(binary = "11111111.11111111.11111111.00000000", "Binary string conversion", passed, failed)

        ' Test hex string
        ip = IPAddressParser.ParseIPv4("192.168.1.1")
        Dim hex As String = ip.ToHexString()
        Assert(hex = "C0.A8.01.01", "Hex string conversion", passed, failed)

        Console.WriteLine()
    End Sub

    Sub TestIPv4AddressComparison(ByRef passed As Integer, ByRef failed As Integer)
        Console.WriteLine("--- IPv4Address Comparison Tests ---")

        Dim ip1 As IPv4Address = IPAddressParser.ParseIPv4("192.168.1.1")
        Dim ip2 As IPv4Address = IPAddressParser.ParseIPv4("192.168.1.1")
        Dim ip3 As IPv4Address = IPAddressParser.ParseIPv4("192.168.1.2")
        Dim ip4 As IPv4Address = IPAddressParser.ParseIPv4("192.168.0.1")

        ' Test equality
        Assert(ip1 = ip2, "Equality operator", passed, failed)
        Assert(ip1.Equals(ip2), "Equals method", passed, failed)
        Assert(ip1 <> ip3, "Inequality operator", passed, failed)

        ' Test comparison
        Assert(ip1 < ip3, "Less than", passed, failed)
        Assert(ip3 > ip1, "Greater than", passed, failed)
        Assert(ip1 <= ip2, "Less than or equal", passed, failed)
        Assert(ip1 >= ip2, "Greater than or equal", passed, failed)

        ' Test different values
        Assert(ip4 < ip1, "192.168.0.1 < 192.168.1.1", passed, failed)

        Console.WriteLine()
    End Sub

    Sub TestIPv4AddressArithmetic(ByRef passed As Integer, ByRef failed As Integer)
        Console.WriteLine("--- IPv4Address Arithmetic Tests ---")

        Dim ip As IPv4Address = IPAddressParser.ParseIPv4("192.168.1.1")

        ' Test addition
        Dim ip2 As IPv4Address = ip + 1
        Assert(ip2.ToString() = "192.168.1.2", "Add 1", passed, failed)

        ' Test subtraction
        ip2 = ip2 - 1
        Assert(ip2 = ip, "Subtract 1", passed, failed)

        ' Test difference
        Dim diff As Integer = ip2 - ip
        Assert(diff = 0, "Difference is 0", passed, failed)

        ' Test large addition
        ip = IPAddressParser.ParseIPv4("192.168.1.100")
        ip2 = ip + 155
        Assert(ip2.ToString() = "192.168.2.55", "Add 155 (octet rollover)", passed, failed)

        Console.WriteLine()
    End Sub

#End Region

#Region "SubnetMask Tests"

    Sub TestSubnetMaskCreation(ByRef passed As Integer, ByRef failed As Integer)
        Console.WriteLine("--- SubnetMask Creation Tests ---")

        ' Test FromPrefixLength
        Dim mask As SubnetMask = SubnetMask.FromPrefixLength(24)
        Assert(mask.ToString() = "255.255.255.0", "/24 mask", passed, failed)

        mask = SubnetMask.FromPrefixLength(16)
        Assert(mask.ToString() = "255.255.0.0", "/16 mask", passed, failed)

        mask = SubnetMask.FromPrefixLength(8)
        Assert(mask.ToString() = "255.0.0.0", "/8 mask", passed, failed)

        mask = SubnetMask.FromPrefixLength(32)
        Assert(mask.ToString() = "255.255.255.255", "/32 mask", passed, failed)

        mask = SubnetMask.FromPrefixLength(0)
        Assert(mask.ToString() = "0.0.0.0", "/0 mask", passed, failed)

        ' Test parsing
        mask = IPAddressParser.ParseSubnetMask("255.255.255.0")
        Assert(mask.ToString() = "255.255.255.0", "Parse dotted decimal mask", passed, failed)

        mask = IPAddressParser.ParseSubnetMask("24")
        Assert(mask.ToString() = "255.255.255.0", "Parse prefix length", passed, failed)

        mask = IPAddressParser.ParseSubnetMask("/24")
        Assert(mask.ToString() = "255.255.255.0", "Parse CIDR prefix", passed, failed)

        Console.WriteLine()
    End Sub

    Sub TestSubnetMaskProperties(ByRef passed As Integer, ByRef failed As Integer)
        Console.WriteLine("--- SubnetMask Properties Tests ---")

        ' Test PrefixLength
        Dim mask As SubnetMask = SubnetMask.FromPrefixLength(24)
        Assert(mask.PrefixLength = 24, "PrefixLength property", passed, failed)

        ' Test host count
        Assert(mask.GetHostCount() = 254, "/24 host count", passed, failed)

        mask = SubnetMask.FromPrefixLength(16)
        Assert(mask.GetHostCount() = 65534, "/16 host count", passed, failed)

        mask = SubnetMask.FromPrefixLength(32)
        Assert(mask.GetHostCount() = 0, "/32 host count", passed, failed)

        mask = SubnetMask.FromPrefixLength(31)
        Assert(mask.GetHostCount() = 2, "/31 host count (point-to-point)", passed, failed)

        ' Test total address count
        mask = SubnetMask.FromPrefixLength(24)
        Assert(mask.GetTotalAddressCount() = 256, "/24 total addresses", passed, failed)

        ' Test wildcard mask
        mask = SubnetMask.FromPrefixLength(24)
        Dim wildcard As SubnetMask = mask.GetWildcardMask()
        Assert(wildcard.ToString() = "0.0.0.255", "Wildcard mask for /24", passed, failed)

        Console.WriteLine()
    End Sub

    Sub TestSubnetMaskPrefixLength(ByRef passed As Integer, ByRef failed As Integer)
        Console.WriteLine("--- SubnetMask Prefix Length Tests ---")

        ' Test various prefix lengths
        Dim masks As String() = {
            "0.0.0.0",
            "128.0.0.0",
            "192.0.0.0",
            "224.0.0.0",
            "240.0.0.0",
            "248.0.0.0",
            "252.0.0.0",
            "254.0.0.0",
            "255.0.0.0",
            "255.128.0.0",
            "255.192.0.0",
            "255.224.0.0",
            "255.240.0.0",
            "255.248.0.0",
            "255.252.0.0",
            "255.254.0.0",
            "255.255.0.0",
            "255.255.128.0",
            "255.255.192.0",
            "255.255.224.0",
            "255.255.240.0",
            "255.255.248.0",
            "255.255.252.0",
            "255.255.254.0",
            "255.255.255.0",
            "255.255.255.128",
            "255.255.255.192",
            "255.255.255.224",
            "255.255.255.240",
            "255.255.255.248",
            "255.255.255.252",
            "255.255.255.254",
            "255.255.255.255"
        }

        For i As Integer = 0 To masks.Length - 1
            Dim mask As SubnetMask = IPAddressParser.ParseSubnetMask(masks(i))
            Assert(mask.PrefixLength = i, String.Format("Prefix {0} = {1}", i, masks(i)), passed, failed)
        Next

        Console.WriteLine()
    End Sub

#End Region

#Region "IPv4Network Tests"

    Sub TestIPv4NetworkCreation(ByRef passed As Integer, ByRef failed As Integer)
        Console.WriteLine("--- IPv4Network Creation Tests ---")

        ' Test creation with prefix length
        Dim network As IPv4Network = New IPv4Network(
            IPAddressParser.ParseIPv4("192.168.1.0"), 24)
        Assert(network.ToString() = "192.168.1.0/24", "Create with prefix length", passed, failed)

        ' Test creation with subnet mask
        network = New IPv4Network(
            IPAddressParser.ParseIPv4("192.168.1.100"),
            SubnetMask.FromPrefixLength(24))
        Assert(network.NetworkAddress.ToString() = "192.168.1.0", "Network address from any IP", passed, failed)

        ' Test CIDR parsing
        Dim success As Boolean = IPAddressParser.TryParseCIDR("10.0.0.0/8", network)
        Assert(success AndAlso network.ToString() = "10.0.0.0/8", "Parse CIDR notation", passed, failed)

        Console.WriteLine()
    End Sub

    Sub TestIPv4NetworkProperties(ByRef passed As Integer, ByRef failed As Integer)
        Console.WriteLine("--- IPv4Network Properties Tests ---")

        Dim network As IPv4Network = New IPv4Network(
            IPAddressParser.ParseIPv4("192.168.1.0"), 24)

        ' Test network address
        Assert(network.NetworkAddress.ToString() = "192.168.1.0", "Network address", passed, failed)

        ' Test broadcast address
        Assert(network.BroadcastAddress.ToString() = "192.168.1.255", "Broadcast address", passed, failed)

        ' Test first usable host
        Assert(network.FirstUsableHost.ToString() = "192.168.1.1", "First usable host", passed, failed)

        ' Test last usable host
        Assert(network.LastUsableHost.ToString() = "192.168.1.254", "Last usable host", passed, failed)

        ' Test usable host count
        Assert(network.UsableHostCount = 254, "Usable host count", passed, failed)

        ' Test total address count
        Assert(network.TotalAddressCount = 256, "Total address count", passed, failed)

        ' Test /31 network (point-to-point)
        network = New IPv4Network(IPAddressParser.ParseIPv4("192.168.1.0"), 31)
        Assert(network.FirstUsableHost.ToString() = "192.168.1.0", "/31 first host", passed, failed)
        Assert(network.LastUsableHost.ToString() = "192.168.1.1", "/31 last host", passed, failed)

        ' Test /32 network (single host)
        network = New IPv4Network(IPAddressParser.ParseIPv4("192.168.1.1"), 32)
        Assert(network.UsableHostCount = 0, "/32 host count", passed, failed)

        Console.WriteLine()
    End Sub

    Sub TestIPv4NetworkContains(ByRef passed As Integer, ByRef failed As Integer)
        Console.WriteLine("--- IPv4Network Contains Tests ---")

        Dim network As IPv4Network = New IPv4Network(
            IPAddressParser.ParseIPv4("192.168.1.0"), 24)

        ' Test addresses within network
        Assert(network.Contains(IPAddressParser.ParseIPv4("192.168.1.0")), "Contains network address", passed, failed)
        Assert(network.Contains(IPAddressParser.ParseIPv4("192.168.1.1")), "Contains first host", passed, failed)
        Assert(network.Contains(IPAddressParser.ParseIPv4("192.168.1.255")), "Contains broadcast", passed, failed)
        Assert(network.Contains(IPAddressParser.ParseIPv4("192.168.1.128")), "Contains middle address", passed, failed)

        ' Test addresses outside network
        Assert(Not network.Contains(IPAddressParser.ParseIPv4("192.168.0.1")), "Not contains outside address", passed, failed)
        Assert(Not network.Contains(IPAddressParser.ParseIPv4("192.168.2.1")), "Not contains outside address 2", passed, failed)
        Assert(Not network.Contains(IPAddressParser.ParseIPv4("10.0.0.1")), "Not contains completely different network", passed, failed)

        Console.WriteLine()
    End Sub

    Sub TestIPv4NetworkSplit(ByRef passed As Integer, ByRef failed As Integer)
        Console.WriteLine("--- IPv4Network Split Tests ---")

        Dim network As IPv4Network = New IPv4Network(
            IPAddressParser.ParseIPv4("192.168.0.0"), 16)

        ' Test splitting /16 into /24
        Dim subnets As List(Of IPv4Network) = network.Split(24)
        Assert(subnets.Count = 256, "Split /16 into 256 /24 networks", passed, failed)

        ' Test splitting /24 into /26
        network = New IPv4Network(IPAddressParser.ParseIPv4("192.168.1.0"), 24)
        subnets = network.Split(26)
        Assert(subnets.Count = 4, "Split /24 into 4 /26 networks", passed, failed)
        Assert(subnets(0).ToString() = "192.168.1.0/26", "First subnet", passed, failed)
        Assert(subnets(1).ToString() = "192.168.1.64/26", "Second subnet", passed, failed)
        Assert(subnets(2).ToString() = "192.168.1.128/26", "Third subnet", passed, failed)
        Assert(subnets(3).ToString() = "192.168.1.192/26", "Fourth subnet", passed, failed)

        ' Test supernet
        Dim supernet As IPv4Network = subnets(0).GetSupernet()
        Assert(supernet.ToString() = "192.168.1.0/25", "Get supernet", passed, failed)

        Console.WriteLine()
    End Sub

#End Region

#Region "IPAddressParser Tests"

    Sub TestIPAddressParser(ByRef passed As Integer, ByRef failed As Integer)
        Console.WriteLine("--- IPAddressParser Tests ---")

        ' Test IsValidIPv4
        Assert(IPAddressParser.IsValidIPv4("192.168.1.1"), "Valid IPv4", passed, failed)
        Assert(IPAddressParser.IsValidIPv4("0.0.0.0"), "Valid IPv4 (zeros)", passed, failed)
        Assert(IPAddressParser.IsValidIPv4("255.255.255.255"), "Valid IPv4 (max)", passed, failed)
        Assert(Not IPAddressParser.IsValidIPv4("256.1.1.1"), "Invalid IPv4 (out of range)", passed, failed)
        Assert(Not IPAddressParser.IsValidIPv4("1.1.1"), "Invalid IPv4 (3 octets)", passed, failed)
        Assert(Not IPAddressParser.IsValidIPv4("1.1.1.1.1"), "Invalid IPv4 (5 octets)", passed, failed)
        Assert(Not IPAddressParser.IsValidIPv4("abc.def.ghi.jkl"), "Invalid IPv4 (letters)", passed, failed)

        ' Test IsValidSubnetMask
        Assert(IPAddressParser.IsValidSubnetMask("255.255.255.0"), "Valid subnet mask", passed, failed)
        Assert(IPAddressParser.IsValidSubnetMask("24"), "Valid prefix length", passed, failed)
        Assert(IPAddressParser.IsValidSubnetMask("/24"), "Valid CIDR prefix", passed, failed)
        Assert(Not IPAddressParser.IsValidSubnetMask("255.0.255.0"), "Invalid subnet mask (non-contiguous)", passed, failed)

        ' Test IsValidCIDR
        Assert(IPAddressParser.IsValidCIDR("192.168.1.0/24"), "Valid CIDR", passed, failed)
        Assert(IPAddressParser.IsValidCIDR("10.0.0.0/8"), "Valid CIDR /8", passed, failed)
        Assert(Not IPAddressParser.IsValidCIDR("192.168.1.0"), "Invalid CIDR (no prefix)", passed, failed)
        Assert(Not IPAddressParser.IsValidCIDR("192.168.1.0/33"), "Invalid CIDR (prefix > 32)", passed, failed)

        Console.WriteLine()
    End Sub

#End Region

#Region "IPRange Tests"

    Sub TestIPRange(ByRef passed As Integer, ByRef failed As Integer)
        Console.WriteLine("--- IPRange Tests ---")

        Dim startIP As IPv4Address = IPAddressParser.ParseIPv4("192.168.1.1")
        Dim endIP As IPv4Address = IPAddressParser.ParseIPv4("192.168.1.10")

        Dim range As New IPRange(startIP, endIP)

        ' Test properties
        Assert(range.StartAddress = startIP, "Start address", passed, failed)
        Assert(range.EndAddress = endIP, "End address", passed, failed)
        Assert(range.Count = 10, "Count = 10", passed, failed)

        ' Test contains
        Assert(range.Contains(IPAddressParser.ParseIPv4("192.168.1.5")), "Contains middle", passed, failed)
        Assert(range.Contains(IPAddressParser.ParseIPv4("192.168.1.1")), "Contains start", passed, failed)
        Assert(range.Contains(IPAddressParser.ParseIPv4("192.168.1.10")), "Contains end", passed, failed)
        Assert(Not range.Contains(IPAddressParser.ParseIPv4("192.168.1.0")), "Not contains before start", passed, failed)
        Assert(Not range.Contains(IPAddressParser.ParseIPv4("192.168.1.11")), "Not contains after end", passed, failed)

        ' Test overlaps
        Dim range2 As New IPRange(
            IPAddressParser.ParseIPv4("192.168.1.5"),
            IPAddressParser.ParseIPv4("192.168.1.15"))
        Assert(range.Overlaps(range2), "Overlapping ranges", passed, failed)

        Dim range3 As New IPRange(
            IPAddressParser.ParseIPv4("192.168.2.1"),
            IPAddressParser.ParseIPv4("192.168.2.10"))
        Assert(Not range.Overlaps(range3), "Non-overlapping ranges", passed, failed)

        ' Test adjacent
        Dim range4 As New IPRange(
            IPAddressParser.ParseIPv4("192.168.1.11"),
            IPAddressParser.ParseIPv4("192.168.1.20"))
        Assert(range.IsAdjacentTo(range4), "Adjacent ranges", passed, failed)

        ' Test merge
        Dim merged As IPRange = range.Merge(range4)
        Assert(merged.StartAddress.ToString() = "192.168.1.1", "Merged start", passed, failed)
        Assert(merged.EndAddress.ToString() = "192.168.1.20", "Merged end", passed, failed)

        ' Test ToCIDRNetworks
        Dim networks As List(Of IPv4Network) = range.ToCIDRNetworks()
        Assert(networks.Count > 0, "ToCIDRNetworks returns networks", passed, failed)

        Console.WriteLine()
    End Sub

#End Region

#Region "IPAddressCalculator Tests"

    Sub TestIPAddressCalculator(ByRef passed As Integer, ByRef failed As Integer)
        Console.WriteLine("--- IPAddressCalculator Tests ---")

        Dim ip As IPv4Address = IPAddressParser.ParseIPv4("192.168.1.100")
        Dim mask As SubnetMask = SubnetMask.FromPrefixLength(24)

        ' Test network address calculation
        Dim networkAddr As IPv4Address = IPAddressCalculator.GetNetworkAddress(ip, mask)
        Assert(networkAddr.ToString() = "192.168.1.0", "Calculate network address", passed, failed)

        ' Test broadcast address calculation
        Dim broadcastAddr As IPv4Address = IPAddressCalculator.GetBroadcastAddress(ip, mask)
        Assert(broadcastAddr.ToString() = "192.168.1.255", "Calculate broadcast address", passed, failed)

        ' Test first usable host
        Dim firstHost As IPv4Address = IPAddressCalculator.GetFirstUsableHost(networkAddr, mask)
        Assert(firstHost.ToString() = "192.168.1.1", "Calculate first usable host", passed, failed)

        ' Test last usable host
        Dim lastHost As IPv4Address = IPAddressCalculator.GetLastUsableHost(networkAddr, mask)
        Assert(lastHost.ToString() = "192.168.1.254", "Calculate last usable host", passed, failed)

        ' Test next/previous address
        Dim nextAddr As IPv4Address = IPAddressCalculator.GetNextAddress(ip)
        Assert(nextAddr.ToString() = "192.168.1.101", "Get next address", passed, failed)

        Dim prevAddr As IPv4Address = IPAddressCalculator.GetPreviousAddress(ip)
        Assert(prevAddr.ToString() = "192.168.1.99", "Get previous address", passed, failed)

        ' Test subnet count
        Dim network As New IPv4Network(IPAddressParser.ParseIPv4("192.168.0.0"), 16)
        Dim count As Integer = IPAddressCalculator.GetSubnetCount(network, 24)
        Assert(count = 256, "Subnet count /16 to /24", passed, failed)

        Console.WriteLine()
    End Sub

#End Region

#Region "IPAddressFormatter Tests"

    Sub TestIPAddressFormatter(ByRef passed As Integer, ByRef failed As Integer)
        Console.WriteLine("--- IPAddressFormatter Tests ---")

        Dim ip As IPv4Address = IPAddressParser.ParseIPv4("192.168.1.1")
        Dim mask As SubnetMask = SubnetMask.FromPrefixLength(24)

        ' Test various formats
        Assert(IPAddressFormatter.ToDottedDecimal(ip) = "192.168.1.1", "Dotted decimal format", passed, failed)
        Assert(IPAddressFormatter.ToBinary(ip).Contains("11000000"), "Binary format contains 192", passed, failed)
        Assert(IPAddressFormatter.ToHex(ip) = "C0.A8.01.01", "Hex format", passed, failed)
        Assert(IPAddressFormatter.ToInteger(ip) = "3232235777", "Integer format", passed, failed)
        Assert(IPAddressFormatter.ToCIDR(mask) = "/24", "CIDR format", passed, failed)

        ' Test FormatAll
        Dim allFormats As String = IPAddressFormatter.FormatAll(ip)
        Assert(allFormats.Contains("Decimal:"), "FormatAll contains Decimal", passed, failed)
        Assert(allFormats.Contains("Binary:"), "FormatAll contains Binary", passed, failed)
        Assert(allFormats.Contains("Hex:"), "FormatAll contains Hex", passed, failed)

        ' Test FormatNetworkInfo
        Dim network As New IPv4Network(ip, mask)
        Dim info As String = IPAddressFormatter.FormatNetworkInfo(network)
        Assert(info.Contains("Network:"), "FormatNetworkInfo contains Network", passed, failed)
        Assert(info.Contains("Broadcast"), "FormatNetworkInfo contains Broadcast", passed, failed)

        Console.WriteLine()
    End Sub

#End Region

    Sub Assert(condition As Boolean, testName As String, ByRef passed As Integer, ByRef failed As Integer)
        If condition Then
            Console.WriteLine("  [PASS] " & testName)
            passed += 1
        Else
            Console.WriteLine("  [FAIL] " & testName)
            failed += 1
        End If
    End Sub

End Module