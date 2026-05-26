' IPUtils Examples - Usage Examples for IP Address Utilities
' Demonstrates IPv4 address validation, parsing, subnet calculation, and CIDR operations

Imports System
Imports IPUtils

Module IPUtilsExamples

    Sub Main()
        Console.WriteLine("=== IPUtils Examples ===")
        Console.WriteLine()

        ' Example 1: IPv4 Address Parsing and Validation
        IPv4ParsingExample()

        ' Example 2: IPv4 Address Properties
        IPv4PropertiesExample()

        ' Example 3: IPv4 Address Conversion
        IPv4ConversionExample()

        ' Example 4: Subnet Mask Operations
        SubnetMaskExample()

        ' Example 5: IPv4 Network Operations
        IPv4NetworkExample()

        ' Example 6: CIDR Notation Parsing
        CIDRNotationExample()

        ' Example 7: IP Range Operations
        IPRangeExample()

        ' Example 8: Network Splitting and Supernetting
        NetworkSplittingExample()

        ' Example 9: IP Address Calculator
        IPAddressCalculatorExample()

        ' Example 10: IP Address Formatter
        IPAddressFormatterExample()

        ' Example 11: Common Network Scenarios
        CommonScenariosExample()

        Console.WriteLine()
        Console.WriteLine("Press any key to exit...")
        Console.ReadKey()
    End Sub

#Region "Example 1: IPv4 Address Parsing and Validation"

    Sub IPv4ParsingExample()
        Console.WriteLine("--- Example 1: IPv4 Address Parsing and Validation ---")
        Console.WriteLine()

        ' Parse IPv4 address from string
        Dim ip As IPv4Address = IPAddressParser.ParseIPv4("192.168.1.1")
        Console.WriteLine("Parsed IP: " & ip.ToString())
        Console.WriteLine("Octets: " & ip.Octet1 & "." & ip.Octet2 & "." & ip.Octet3 & "." & ip.Octet4)
        Console.WriteLine()

        ' TryParse for safe parsing
        Dim result As IPv4Address
        If IPAddressParser.TryParseIPv4("10.0.0.1", result) Then
            Console.WriteLine("Successfully parsed: " & result.ToString())
        Else
            Console.WriteLine("Failed to parse IP address")
        End If
        Console.WriteLine()

        ' Validate IP address string
        Dim testIPs As String() = {"192.168.1.1", "256.1.1.1", "invalid", "0.0.0.0"}
        For Each testIP As String In testIPs
            Dim isValid As Boolean = IPAddressParser.IsValidIPv4(testIP)
            Console.WriteLine(String.Format("'{0}' is {1}", testIP, If(isValid, "valid", "invalid")))
        Next
        Console.WriteLine()

        ' Create IPv4 address from bytes
        ip = New IPv4Address(10, 20, 30, 40)
        Console.WriteLine("Created from bytes: " & ip.ToString())
        Console.WriteLine()
    End Sub

#End Region

#Region "Example 2: IPv4 Address Properties"

    Sub IPv4PropertiesExample()
        Console.WriteLine("--- Example 2: IPv4 Address Properties ---")
        Console.WriteLine()

        ' Check different IP address types
        Dim testAddresses As String() = {
            "10.0.0.1",           ' Private (Class A)
            "172.16.0.1",         ' Private (Class B)
            "192.168.1.1",        ' Private (Class C)
            "127.0.0.1",          ' Loopback
            "169.254.1.1",        ' Link-local
            "224.0.0.1",          ' Multicast (Class D)
            "240.0.0.1",          ' Reserved (Class E)
            "8.8.8.8",            ' Public
            "0.0.0.0",            ' Default network
            "255.255.255.255"     ' Broadcast
        }

        For Each addr As String In testAddresses
            Dim ip As IPv4Address = IPAddressParser.ParseIPv4(addr)
            Console.WriteLine(String.Format("{0}: Class={1}, Type={2}, Private={3}, Public={4}",
                addr,
                ip.GetClass(),
                ip.GetTypeDescription(),
                ip.IsPrivate(),
                ip.IsPublic()))
        Next
        Console.WriteLine()
    End Sub

#End Region

#Region "Example 3: IPv4 Address Conversion"

    Sub IPv4ConversionExample()
        Console.WriteLine("--- Example 3: IPv4 Address Conversion ---")
        Console.WriteLine()

        Dim ip As IPv4Address = IPAddressParser.ParseIPv4("192.168.1.1")
        Console.WriteLine("Original IP: " & ip.ToString())
        Console.WriteLine()

        ' Integer conversion
        Console.WriteLine("As Integer: " & ip.ToInt32())
        Console.WriteLine("As Unsigned: " & ip.ToUInt32())
        Console.WriteLine()

        ' Binary representation
        Console.WriteLine("Binary: " & ip.ToBinaryString())
        Console.WriteLine()

        ' Hexadecimal representation
        Console.WriteLine("Hexadecimal: " & ip.ToHexString())
        Console.WriteLine()

        ' Roundtrip conversion
        Dim intVal As Integer = ip.ToInt32()
        Dim ip2 As IPv4Address = IPv4Address.FromInt32(intVal)
        Console.WriteLine("Roundtrip from int: " & ip2.ToString())

        Dim uintVal As UInteger = ip.ToUInt32()
        ip2 = IPv4Address.FromUInt32(uintVal)
        Console.WriteLine("Roundtrip from uint: " & ip2.ToString())
        Console.WriteLine()
    End Sub

#End Region

#Region "Example 4: Subnet Mask Operations"

    Sub SubnetMaskExample()
        Console.WriteLine("--- Example 4: Subnet Mask Operations ---")
        Console.WriteLine()

        ' Create subnet mask from prefix length
        Dim mask As SubnetMask = SubnetMask.FromPrefixLength(24)
        Console.WriteLine("/24 mask: " & mask.ToString())
        Console.WriteLine()

        ' Common subnet masks
        Console.WriteLine("Common Subnet Masks:")
        Console.WriteLine("/8 (Class A):  " & SubnetMask.FromPrefixLength(8).ToString())
        Console.WriteLine("/16 (Class B): " & SubnetMask.FromPrefixLength(16).ToString())
        Console.WriteLine("/24 (Class C): " & SubnetMask.FromPrefixLength(24).ToString())
        Console.WriteLine("/32 (Single host): " & SubnetMask.FromPrefixLength(32).ToString())
        Console.WriteLine()

        ' Host count for different prefix lengths
        Console.WriteLine("Host Counts:")
        For prefix As Integer = 8 To 30 Step 2
            mask = SubnetMask.FromPrefixLength(prefix)
            Console.WriteLine(String.Format("/{0}: {1} usable hosts, {2} total addresses",
                prefix, mask.GetHostCount(), mask.GetTotalAddressCount()))
        Next
        Console.WriteLine()

        ' Wildcard mask
        mask = SubnetMask.FromPrefixLength(24)
        Dim wildcard As SubnetMask = mask.GetWildcardMask()
        Console.WriteLine("Wildcard for /24: " & wildcard.ToString())
        Console.WriteLine()

        ' Parse subnet mask
        mask = IPAddressParser.ParseSubnetMask("255.255.255.128")
        Console.WriteLine("Parsed mask: " & mask.ToString() & " (/" & mask.PrefixLength & ")")
        Console.WriteLine()
    End Sub

#End Region

#Region "Example 5: IPv4 Network Operations"

    Sub IPv4NetworkExample()
        Console.WriteLine("--- Example 5: IPv4 Network Operations ---")
        Console.WriteLine()

        ' Create network
        Dim network As New IPv4Network(IPAddressParser.ParseIPv4("192.168.1.0"), 24)
        Console.WriteLine("Network: " & network.ToString())
        Console.WriteLine(network.GetInfo())
        Console.WriteLine()

        ' Create network from non-network address
        network = New IPv4Network(IPAddressParser.ParseIPv4("192.168.1.100"), 24)
        Console.WriteLine("Network from 192.168.1.100/24:")
        Console.WriteLine("Network Address: " & network.NetworkAddress.ToString())
        Console.WriteLine()

        ' Check if address is in network
        Dim testIP As IPv4Address = IPAddressParser.ParseIPv4("192.168.1.50")
        Console.WriteLine(String.Format("{0} is in {1}: {2}",
            testIP.ToString(), network.ToString(), network.Contains(testIP)))

        testIP = IPAddressParser.ParseIPv4("192.168.2.50")
        Console.WriteLine(String.Format("{0} is in {1}: {2}",
            testIP.ToString(), network.ToString(), network.Contains(testIP)))
        Console.WriteLine()

        ' Compare networks
        Dim network2 As New IPv4Network(IPAddressParser.ParseIPv4("192.168.1.0"), 26)
        Console.WriteLine(String.Format("{0} is subnet of {1}: {2}",
            network2.ToString(), network.ToString(), network2.IsSubnetOf(network)))
        Console.WriteLine()
    End Sub

#End Region

#Region "Example 6: CIDR Notation Parsing"

    Sub CIDRNotationExample()
        Console.WriteLine("--- Example 6: CIDR Notation Parsing ---")
        Console.WriteLine()

        ' Parse CIDR notation
        Dim cidrStrings As String() = {
            "10.0.0.0/8",
            "172.16.0.0/12",
            "192.168.0.0/16",
            "192.168.1.0/24",
            "192.168.1.128/25"
        }

        For Each cidr As String In cidrStrings
            Dim network As IPv4Network = IPAddressParser.ParseCIDR(cidr)
            Console.WriteLine("CIDR: " & cidr)
            Console.WriteLine("  Network: " & network.NetworkAddress.ToString())
            Console.WriteLine("  Broadcast: " & network.BroadcastAddress.ToString())
            Console.WriteLine("  First Host: " & network.FirstUsableHost.ToString())
            Console.WriteLine("  Last Host: " & network.LastUsableHost.ToString())
            Console.WriteLine("  Usable Hosts: " & network.UsableHostCount.ToString("N0"))
            Console.WriteLine()
        Next

        ' Validate CIDR
        Dim testCIDRs As String() = {"192.168.1.0/24", "192.168.1.0", "192.168.1.0/33"}
        For Each testCIDR As String In testCIDRs
            Dim isValid As Boolean = IPAddressParser.IsValidCIDR(testCIDR)
            Console.WriteLine(String.Format("'{0}' is {1}", testCIDR, If(isValid, "valid CIDR", "invalid CIDR")))
        Next
        Console.WriteLine()
    End Sub

#End Region

#Region "Example 7: IP Range Operations"

    Sub IPRangeExample()
        Console.WriteLine("--- Example 7: IP Range Operations ---")
        Console.WriteLine()

        ' Create IP range
        Dim startIP As IPv4Address = IPAddressParser.ParseIPv4("192.168.1.1")
        Dim endIP As IPv4Address = IPAddressParser.ParseIPv4("192.168.1.100")
        Dim range As New IPRange(startIP, endIP)

        Console.WriteLine("IP Range: " & range.ToString())
        Console.WriteLine("Count: " & range.Count.ToString() & " addresses")
        Console.WriteLine()

        ' Check if address is in range
        Dim testIP As IPv4Address = IPAddressParser.ParseIPv4("192.168.1.50")
        Console.WriteLine(String.Format("{0} in range: {1}", testIP.ToString(), range.Contains(testIP)))

        testIP = IPAddressParser.ParseIPv4("192.168.1.200")
        Console.WriteLine(String.Format("{0} in range: {1}", testIP.ToString(), range.Contains(testIP)))
        Console.WriteLine()

        ' Convert range to CIDR networks
        Console.WriteLine("Range as CIDR networks:")
        Dim networks As List(Of IPv4Network) = range.ToCIDRNetworks()
        For Each net As IPv4Network In networks
            Console.WriteLine("  " & net.ToString())
        Next
        Console.WriteLine()

        ' Merge adjacent ranges
        Dim range2 As New IPRange(
            IPAddressParser.ParseIPv4("192.168.1.101"),
            IPAddressParser.ParseIPv4("192.168.1.200"))
        Console.WriteLine("Range 1: " & range.ToString())
        Console.WriteLine("Range 2: " & range2.ToString())
        Console.WriteLine("Adjacent: " & range.IsAdjacentTo(range2))

        Dim merged As IPRange = range.Merge(range2)
        Console.WriteLine("Merged: " & merged.ToString())
        Console.WriteLine()
    End Sub

#End Region

#Region "Example 8: Network Splitting and Supernetting"

    Sub NetworkSplittingExample()
        Console.WriteLine("--- Example 8: Network Splitting and Supernetting ---")
        Console.WriteLine()

        ' Split /24 into /26 subnets
        Dim network As New IPv4Network(IPAddressParser.ParseIPv4("192.168.1.0"), 24)
        Console.WriteLine("Original network: " & network.ToString())
        Console.WriteLine()

        Dim subnets As List(Of IPv4Network) = network.Split(26)
        Console.WriteLine("Split into /26 subnets:")
        For Each subnet As IPv4Network In subnets
            Console.WriteLine("  " & subnet.ToString() & " (hosts: " & subnet.UsableHostCount & ")")
        Next
        Console.WriteLine()

        ' Split /16 into /24 subnets
        network = New IPv4Network(IPAddressParser.ParseIPv4("10.0.0.0"), 16)
        Console.WriteLine("Split 10.0.0.0/16 into /24 subnets (first 10):")
        subnets = network.Split(24)
        For i As Integer = 0 To 9
            Console.WriteLine("  " & subnets(i).ToString())
        Next
        Console.WriteLine("  ... (total: " & subnets.Count & " subnets)")
        Console.WriteLine()

        ' Get supernet
        Dim smallNetwork As New IPv4Network(IPAddressParser.ParseIPv4("192.168.1.128"), 25)
        Console.WriteLine("Network: " & smallNetwork.ToString())
        Console.WriteLine("Supernet: " & smallNetwork.GetSupernet().ToString())
        Console.WriteLine()

        ' Check if networks can be summarized
        Dim net1 As New IPv4Network(IPAddressParser.ParseIPv4("192.168.1.0"), 25)
        Dim net2 As New IPv4Network(IPAddressParser.ParseIPv4("192.168.1.128"), 25)
        Console.WriteLine("Can summarize " & net1.ToString() & " and " & net2.ToString() & ": " &
            IPAddressCalculator.CanSummarize(net1, net2))
        If IPAddressCalculator.CanSummarize(net1, net2) Then
            Console.WriteLine("Summarized network: " & IPAddressCalculator.Summarize(net1, net2).ToString())
        End If
        Console.WriteLine()
    End Sub

#End Region

#Region "Example 9: IP Address Calculator"

    Sub IPAddressCalculatorExample()
        Console.WriteLine("--- Example 9: IP Address Calculator ---")
        Console.WriteLine()

        ' Calculate network info from IP and mask
        Dim ip As IPv4Address = IPAddressParser.ParseIPv4("192.168.1.100")
        Dim mask As SubnetMask = SubnetMask.FromPrefixLength(24)

        Console.WriteLine("IP Address: " & ip.ToString())
        Console.WriteLine("Subnet Mask: " & mask.ToString() & " (/24)")
        Console.WriteLine()

        Dim networkAddr As IPv4Address = IPAddressCalculator.GetNetworkAddress(ip, mask)
        Console.WriteLine("Network Address: " & networkAddr.ToString())

        Dim broadcastAddr As IPv4Address = IPAddressCalculator.GetBroadcastAddress(ip, mask)
        Console.WriteLine("Broadcast Address: " & broadcastAddr.ToString())

        Dim firstHost As IPv4Address = IPAddressCalculator.GetFirstUsableHost(networkAddr, mask)
        Console.WriteLine("First Usable Host: " & firstHost.ToString())

        Dim lastHost As IPv4Address = IPAddressCalculator.GetLastUsableHost(networkAddr, mask)
        Console.WriteLine("Last Usable Host: " & lastHost.ToString())
        Console.WriteLine()

        ' Next and previous addresses
        Console.WriteLine("Next address after " & ip.ToString() & ": " &
            IPAddressCalculator.GetNextAddress(ip).ToString())
        Console.WriteLine("Previous address before " & ip.ToString() & ": " &
            IPAddressCalculator.GetPreviousAddress(ip).ToString())
        Console.WriteLine()

        ' Subnet count
        Dim baseNetwork As New IPv4Network(IPAddressParser.ParseIPv4("10.0.0.0"), 8)
        Dim subnetCount As Integer = IPAddressCalculator.GetSubnetCount(baseNetwork, 16)
        Console.WriteLine(String.Format("Number of /16 subnets in {0}: {1}",
            baseNetwork.ToString(), subnetCount))
        Console.WriteLine()
    End Sub

#End Region

#Region "Example 10: IP Address Formatter"

    Sub IPAddressFormatterExample()
        Console.WriteLine("--- Example 10: IP Address Formatter ---")
        Console.WriteLine()

        Dim ip As IPv4Address = IPAddressParser.ParseIPv4("192.168.1.1")

        ' Various format outputs
        Console.WriteLine("IP Address: " & ip.ToString())
        Console.WriteLine()
        Console.WriteLine("Different formats:")
        Console.WriteLine("  Dotted Decimal: " & IPAddressFormatter.ToDottedDecimal(ip))
        Console.WriteLine("  Binary:         " & IPAddressFormatter.ToBinary(ip))
        Console.WriteLine("  Hexadecimal:    " & IPAddressFormatter.ToHex(ip))
        Console.WriteLine("  Integer:        " & IPAddressFormatter.ToInteger(ip))
        Console.WriteLine()

        ' Complete format info
        Console.WriteLine("Complete format info:")
        Console.WriteLine(IPAddressFormatter.FormatAll(ip))
        Console.WriteLine()

        ' Network info formatting
        Dim network As New IPv4Network(ip, SubnetMask.FromPrefixLength(24))
        Console.WriteLine("Network info:")
        Console.WriteLine(IPAddressFormatter.FormatNetworkInfo(network))
    End Sub

#End Region

#Region "Example 11: Common Network Scenarios"

    Sub CommonScenariosExample()
        Console.WriteLine("--- Example 11: Common Network Scenarios ---")
        Console.WriteLine()

        ' Scenario 1: Determine if IP is in private range
        Console.WriteLine("Scenario 1: Is IP private?")
        Dim testIPs As String() = {"192.168.1.1", "8.8.8.8", "10.10.10.10", "172.20.0.1"}
        For Each testIP As String In testIPs
            Dim ip As IPv4Address = IPAddressParser.ParseIPv4(testIP)
            Console.WriteLine(String.Format("  {0}: Private={1}, Public={2}",
                testIP, ip.IsPrivate(), ip.IsPublic()))
        Next
        Console.WriteLine()

        ' Scenario 2: Calculate subnet for office network
        Console.WriteLine("Scenario 2: Office network planning")
        Console.WriteLine("Need 500 hosts - what subnet size?")
        Dim requiredHosts As Integer = 500
        Dim prefix As Integer = 32
        While (1 << (32 - prefix)) - 2 < requiredHosts
            prefix -= 1
        End While
        Dim mask As SubnetMask = SubnetMask.FromPrefixLength(prefix)
        Console.WriteLine(String.Format("  Use /{0} subnet: {1} hosts available",
            prefix, mask.GetHostCount()))
        Console.WriteLine()

        ' Scenario 3: Split network for departments
        Console.WriteLine("Scenario 3: Split 192.168.0.0/24 for 4 departments")
        Dim officeNet As New IPv4Network(IPAddressParser.ParseIPv4("192.168.0.0"), 24)
        Dim deptSubnets As List(Of IPv4Network) = officeNet.Split(26)
        For i As Integer = 0 To deptSubnets.Count - 1
            Console.WriteLine(String.Format("  Department {0}: {1} ({2} hosts)",
                i + 1, deptSubnets(i).ToString(), deptSubnets(i).UsableHostCount))
        Next
        Console.WriteLine()

        ' Scenario 4: Find overlapping networks
        Console.WriteLine("Scenario 4: Check network overlap")
        Dim net1 As New IPv4Network(IPAddressParser.ParseIPv4("192.168.1.0"), 24)
        Dim net2 As New IPv4Network(IPAddressParser.ParseIPv4("192.168.1.128"), 25)
        Dim net3 As New IPv4Network(IPAddressParser.ParseIPv4("192.168.2.0"), 24)

        Console.WriteLine(String.Format("  {0} overlaps {1}: {2}",
            net1.ToString(), net2.ToString(), net1.Overlaps(net2)))
        Console.WriteLine(String.Format("  {0} overlaps {1}: {2}",
            net1.ToString(), net3.ToString(), net1.Overlaps(net3)))
        Console.WriteLine()

        ' Scenario 5: Convert IP range to efficient CIDR blocks
        Console.WriteLine("Scenario 5: Optimize IP allocation")
        Dim rangeStart As IPv4Address = IPAddressParser.ParseIPv4("192.168.1.1")
        Dim rangeEnd As IPv4Address = IPAddressParser.ParseIPv4("192.168.1.63")
        Dim allocRange As New IPRange(rangeStart, rangeEnd)
        Console.WriteLine(String.Format("  Range {0} to {1} ({2} IPs)",
            rangeStart.ToString(), rangeEnd.ToString(), allocRange.Count))
        Console.WriteLine("  Efficient CIDR allocation:")
        For Each net As IPv4Network In allocRange.ToCIDRNetworks()
            Console.WriteLine("    " & net.ToString())
        Next
        Console.WriteLine()
    End Sub

#End Region

End Module