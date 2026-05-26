# IPUtils - IP Address Utilities for VB.NET

Complete IPv4 address validation, parsing, subnet calculation, and CIDR operations library with zero external dependencies.

## Features

### IPv4Address
- Parse and validate IPv4 addresses
- Address type detection (private, public, loopback, multicast, etc.)
- IP class detection (A, B, C, D, E)
- Conversion to/from integer, binary, hexadecimal formats
- Comparison and arithmetic operations

### SubnetMask
- Create from prefix length (CIDR notation)
- Parse from dotted decimal or prefix length
- Host count calculation
- Wildcard mask generation

### IPv4Network
- Network address calculation
- Broadcast address calculation
- Usable host range (first/last usable hosts)
- Subnet containment checks
- Network splitting and supernetting
- CIDR notation support

### IPRange
- IP range operations
- Range overlap detection
- Range merging
- Conversion to optimal CIDR networks

### IPAddressParser
- Parse IPv4 addresses from strings
- Parse subnet masks (dotted decimal or CIDR)
- Parse CIDR notation (e.g., "192.168.1.0/24")
- Validation methods

### IPAddressCalculator
- Network and broadcast address calculation
- First/last usable host calculation
- Subnet count calculation
- Network summarization

### IPAddressFormatter
- Format IP addresses in various representations
- Decimal, binary, hexadecimal, integer formats
- Network info formatting

## Usage Examples

### Parsing IPv4 Addresses

```vbnet
Imports IPUtils

' Parse from string
Dim ip As IPv4Address = IPAddressParser.ParseIPv4("192.168.1.1")
Console.WriteLine(ip.ToString())  ' Output: 192.168.1.1

' Safe parsing with TryParse
Dim result As IPv4Address
If IPAddressParser.TryParseIPv4("10.0.0.1", result) Then
    Console.WriteLine("Parsed: " & result.ToString())
End If

' Validate IP address
If IPAddressParser.IsValidIPv4("192.168.1.1") Then
    Console.WriteLine("Valid IP")
End If

' Create from bytes
ip = New IPv4Address(10, 20, 30, 40)
```

### Checking IP Address Properties

```vbnet
Dim ip As IPv4Address = IPAddressParser.ParseIPv4("192.168.1.1")

' Check address type
Console.WriteLine(ip.IsPrivate())      ' True
Console.WriteLine(ip.IsPublic())       ' False
Console.WriteLine(ip.IsLoopback())     ' False
Console.WriteLine(ip.IsMulticast())    ' False

' Get IP class
Console.WriteLine(ip.GetClass())       ' C

' Get type description
Console.WriteLine(ip.GetTypeDescription())  ' Private
```

### Working with Subnet Masks

```vbnet
' Create from prefix length
Dim mask As SubnetMask = SubnetMask.FromPrefixLength(24)
Console.WriteLine(mask.ToString())     ' 255.255.255.0

' Get host count
Console.WriteLine(mask.GetHostCount()) ' 254

' Get wildcard mask
Dim wildcard As SubnetMask = mask.GetWildcardMask()
Console.WriteLine(wildcard.ToString()) ' 0.0.0.255

' Parse subnet mask
mask = IPAddressParser.ParseSubnetMask("255.255.255.128")
mask = IPAddressParser.ParseSubnetMask("/25")
mask = IPAddressParser.ParseSubnetMask("25")
```

### IPv4 Network Operations

```vbnet
' Create network from CIDR notation
Dim network As IPv4Network = IPAddressParser.ParseCIDR("192.168.1.0/24")

' Get network properties
Console.WriteLine(network.NetworkAddress)      ' 192.168.1.0
Console.WriteLine(network.BroadcastAddress)    ' 192.168.1.255
Console.WriteLine(network.FirstUsableHost)     ' 192.168.1.1
Console.WriteLine(network.LastUsableHost)      ' 192.168.1.254
Console.WriteLine(network.UsableHostCount)     ' 254

' Check if address is in network
Dim ip As IPv4Address = IPAddressParser.ParseIPv4("192.168.1.50")
If network.Contains(ip) Then
    Console.WriteLine("IP is in network")
End If

' Split network into smaller subnets
Dim subnets As List(Of IPv4Network) = network.Split(26)
' Creates 4 /26 subnets
```

### IP Address Conversion

```vbnet
Dim ip As IPv4Address = IPAddressParser.ParseIPv4("192.168.1.1")

' To integer
Console.WriteLine(ip.ToInt32())        ' -1062731519
Console.WriteLine(ip.ToUInt32())       ' 3232235777

' From integer
Dim ip2 As IPv4Address = IPv4Address.FromUInt32(3232235777)

' Binary representation
Console.WriteLine(ip.ToBinaryString()) ' 11000000.10101000.00000001.00000001

' Hexadecimal representation
Console.WriteLine(ip.ToHexString())    ' C0.A8.01.01
```

### IP Range Operations

```vbnet
' Create IP range
Dim range As New IPRange(
    IPAddressParser.ParseIPv4("192.168.1.1"),
    IPAddressParser.ParseIPv4("192.168.1.100")
)

Console.WriteLine(range.Count)  ' 100 addresses

' Check if address is in range
If range.Contains(IPAddressParser.ParseIPv4("192.168.1.50")) Then
    Console.WriteLine("Address in range")
End If

' Convert to optimal CIDR networks
Dim networks As List(Of IPv4Network) = range.ToCIDRNetworks()
For Each net As IPv4Network In networks
    Console.WriteLine(net.ToString())
Next
```

### Address Arithmetic

```vbnet
Dim ip As IPv4Address = IPAddressParser.ParseIPv4("192.168.1.1")

' Add offset
Dim nextIp As IPv4Address = ip + 1  ' 192.168.1.2

' Subtract offset
Dim prevIp As IPv4Address = ip - 1  ' 192.168.1.0

' Compare addresses
If ip1 < ip2 Then
    Console.WriteLine("ip1 comes before ip2")
End If
```

## Common Use Cases

### Determine Network Requirements

```vbnet
' Calculate subnet size for 500 hosts
Dim requiredHosts As Integer = 500
Dim prefix As Integer = 32
While (1 << (32 - prefix)) - 2 < requiredHosts
    prefix -= 1
End While
' Result: /23 subnet (510 usable hosts)
```

### Split Office Network for Departments

```vbnet
Dim officeNet As New IPv4Network(
    IPAddressParser.ParseIPv4("192.168.0.0"), 24
)
Dim deptSubnets As List(Of IPv4Network) = officeNet.Split(26)
' Creates 4 /26 subnets, each with 62 usable hosts
```

### Check Network Overlaps

```vbnet
Dim net1 As New IPv4Network(IPAddressParser.ParseIPv4("192.168.1.0"), 24)
Dim net2 As New IPv4Network(IPAddressParser.ParseIPv4("192.168.1.128"), 25)

If net1.Overlaps(net2) Then
    Console.WriteLine("Networks overlap!")
End If
```

## API Reference

### IPv4Address Structure

| Property/Method | Description |
|-----------------|-------------|
| `Octet1` - `Octet4` | Individual octets (0-255) |
| `Octets` | Byte array of all octets |
| `ToInt32()` / `ToUInt32()` | Convert to integer |
| `FromInt32()` / `FromUInt32()` | Create from integer |
| `GetClass()` | Returns IP class (A/B/C/D/E) |
| `IsPrivate()` | RFC 1918 private address |
| `IsLoopback()` | 127.x.x.x |
| `IsLinkLocal()` | 169.254.x.x |
| `IsMulticast()` | 224-239.x.x.x |
| `IsPublic()` | Internet-routable |
| `ToBinaryString()` | Binary representation |
| `ToHexString()` | Hexadecimal representation |

### SubnetMask Structure

| Property/Method | Description |
|-----------------|-------------|
| `FromPrefixLength(n)` | Create from CIDR prefix |
| `PrefixLength` | Get CIDR prefix length |
| `GetHostCount()` | Usable host addresses |
| `GetTotalAddressCount()` | Total addresses |
| `GetWildcardMask()` | Inverse mask |

### IPv4Network Class

| Property/Method | Description |
|-----------------|-------------|
| `NetworkAddress` | Network address |
| `BroadcastAddress` | Broadcast address |
| `FirstUsableHost` | First usable host |
| `LastUsableHost` | Last usable host |
| `UsableHostCount` | Number of usable hosts |
| `Contains(ip)` | Check if IP in network |
| `Overlaps(network)` | Check network overlap |
| `Split(prefix)` | Split into smaller subnets |
| `GetSupernet()` | Get next larger network |

## File Structure

```
VB/ip_utils/
├── ip_utils.vb          # Main library
├── ip_utils_tests.vb    # Unit tests
├── examples.vb          # Usage examples
└── README.md            # Documentation
```

## Running Tests

Compile and run the test file:

```bash
vbc ip_utils.vb ip_utils_tests.vb
ip_utils_tests.exe
```

## Running Examples

```bash
vbc ip_utils.vb examples.vb
examples.exe
```

## Dependencies

- Zero external dependencies
- Pure VB.NET implementation
- Requires .NET Framework 4.5+ or .NET Core 3.0+

## License

MIT License - Free for personal and commercial use.