' IPUtils - Complete IP Address Validation and Calculation Library
' Zero external dependencies - Pure VB.NET implementation
' Supports IPv4 validation, parsing, subnet calculation, and CIDR notation

Imports System

Namespace IPUtils

    ''' <summary>
    ''' IP address version enumeration
    ''' </summary>
    Public Enum IPVersion
        IPv4
        IPv6
    End Enum

    ''' <summary>
    ''' Represents an IPv4 address with utility methods
    ''' </summary>
    Public Structure IPv4Address
        Implements IEquatable(Of IPv4Address)
        Implements IComparable(Of IPv4Address)

        Private ReadOnly _octets As Byte()

        Public Sub New(octets As Byte())
            If octets Is Nothing OrElse octets.Length <> 4 Then
                Throw New ArgumentException("IPv4 address must have exactly 4 octets")
            End If
            _octets = CType(octets.Clone(), Byte())
        End Sub

        Public Sub New(o1 As Byte, o2 As Byte, o3 As Byte, o4 As Byte)
            _octets = {o1, o2, o3, o4}
        End Sub

        ''' <summary>
        ''' Get octets as array
        ''' </summary>
        Public ReadOnly Property Octets As Byte()
            Get
                Return CType(_octets.Clone(), Byte())
            End Get
        End Property

        ''' <summary>
        ''' Get individual octets
        ''' </summary>
        Public ReadOnly Property Octet1 As Byte
            Get
                Return _octets(0)
            End Get
        End Property

        Public ReadOnly Property Octet2 As Byte
            Get
                Return _octets(1)
            End Get
        End Property

        Public ReadOnly Property Octet3 As Byte
            Get
                Return _octets(2)
            End Get
        End Property

        Public ReadOnly Property Octet4 As Byte
            Get
                Return _octets(3)
            End Get
        End Property

        ''' <summary>
        ''' Convert to 32-bit integer
        ''' </summary>
        Public Function ToInt32() As Integer
            Return (_octets(0) << 24) Or (_octets(1) << 16) Or (_octets(2) << 8) Or _octets(3)
        End Function

        ''' <summary>
        ''' Convert to unsigned 32-bit integer
        ''' </summary>
        Public Function ToUInt32() As UInteger
            Return CUInt((_octets(0) << 24) Or (_octets(1) << 16) Or (_octets(2) << 8) Or _octets(3))
        End Function

        ''' <summary>
        ''' Create from 32-bit integer
        ''' </summary>
        Public Shared Function FromInt32(value As Integer) As IPv4Address
            Return FromUInt32(CUInt(value))
        End Function

        ''' <summary>
        ''' Create from unsigned 32-bit integer
        ''' </summary>
        Public Shared Function FromUInt32(value As UInteger) As IPv4Address
            Return New IPv4Address(
                CByte((value >> 24) And 255),
                CByte((value >> 16) And 255),
                CByte((value >> 8) And 255),
                CByte(value And 255)
            )
        End Function

        ''' <summary>
        ''' Get IP address class (A, B, C, D, E)
        ''' </summary>
        Public Function GetClass() As Char
            Dim firstOctet = _octets(0)
            If firstOctet < 128 Then Return "A"c
            If firstOctet < 192 Then Return "B"c
            If firstOctet < 224 Then Return "C"c
            If firstOctet < 240 Then Return "D"c
            Return "E"c
        End Function

        ''' <summary>
        ''' Check if address is private (RFC 1918)
        ''' </summary>
        Public Function IsPrivate() As Boolean
            ' 10.0.0.0/8
            If _octets(0) = 10 Then Return True
            ' 172.16.0.0/12
            If _octets(0) = 172 AndAlso _octets(1) >= 16 AndAlso _octets(1) <= 31 Then Return True
            ' 192.168.0.0/16
            If _octets(0) = 192 AndAlso _octets(1) = 168 Then Return True
            Return False
        End Function

        ''' <summary>
        ''' Check if address is loopback (127.0.0.0/8)
        ''' </summary>
        Public Function IsLoopback() As Boolean
            Return _octets(0) = 127
        End Function

        ''' <summary>
        ''' Check if address is link-local (169.254.0.0/16)
        ''' </summary>
        Public Function IsLinkLocal() As Boolean
            Return _octets(0) = 169 AndAlso _octets(1) = 254
        End Function

        ''' <summary>
        ''' Check if address is multicast (224.0.0.0/4)
        ''' </summary>
        Public Function IsMulticast() As Boolean
            Return _octets(0) >= 224 AndAlso _octets(0) <= 239
        End Function

        ''' <summary>
        ''' Check if address is reserved
        ''' </summary>
        Public Function IsReserved() As Boolean
            ' 0.0.0.0/8
            If _octets(0) = 0 Then Return True
            ' 240.0.0.0/4
            If _octets(0) >= 240 Then Return True
            Return False
        End Function

        ''' <summary>
        ''' Check if address is public (routable on the internet)
        ''' </summary>
        Public Function IsPublic() As Boolean
            Return Not IsPrivate() AndAlso Not IsLoopback() AndAlso Not IsLinkLocal() AndAlso Not IsMulticast() AndAlso Not IsReserved()
        End Function

        ''' <summary>
        ''' Check if address is the default network (0.0.0.0)
        ''' </summary>
        Public Function IsDefaultNetwork() As Boolean
            Return _octets(0) = 0 AndAlso _octets(1) = 0 AndAlso _octets(2) = 0 AndAlso _octets(3) = 0
        End Function

        ''' <summary>
        ''' Check if address is broadcast (255.255.255.255)
        ''' </summary>
        Public Function IsBroadcast() As Boolean
            Return _octets(0) = 255 AndAlso _octets(1) = 255 AndAlso _octets(2) = 255 AndAlso _octets(3) = 255
        End Function

        ''' <summary>
        ''' Get address type description
        ''' </summary>
        Public Function GetTypeDescription() As String
            If IsDefaultNetwork() Then Return "Default Network"
            If IsBroadcast() Then Return "Broadcast"
            If IsLoopback() Then Return "Loopback"
            If IsLinkLocal() Then Return "Link-Local"
            If IsPrivate() Then Return "Private"
            If IsMulticast() Then Return "Multicast"
            If IsReserved() Then Return "Reserved"
            Return "Public"
        End Function

        ''' <summary>
        ''' Convert to string (dotted decimal notation)
        ''' </summary>
        Public Overrides Function ToString() As String
            Return String.Format("{0}.{1}.{2}.{3}", _octets(0), _octets(1), _octets(2), _octets(3))
        End Function

        ''' <summary>
        ''' Convert to binary string
        ''' </summary>
        Public Function ToBinaryString() As String
            Return String.Format("{0}.{1}.{2}.{3}",
                Convert.ToString(_octets(0), 2).PadLeft(8, "0"c),
                Convert.ToString(_octets(1), 2).PadLeft(8, "0"c),
                Convert.ToString(_octets(2), 2).PadLeft(8, "0"c),
                Convert.ToString(_octets(3), 2).PadLeft(8, "0"c))
        End Function

        ''' <summary>
        ''' Convert to hex string
        ''' </summary>
        Public Function ToHexString() As String
            Return String.Format("{0:X2}.{1:X2}.{2:X2}.{3:X2}", _octets(0), _octets(1), _octets(2), _octets(3))
        End Function

#Region "IEquatable Implementation"
        Public Overloads Function Equals(other As IPv4Address) As Boolean Implements IEquatable(Of IPv4Address).Equals
            Return _octets(0) = other._octets(0) AndAlso
                   _octets(1) = other._octets(1) AndAlso
                   _octets(2) = other._octets(2) AndAlso
                   _octets(3) = other._octets(3)
        End Function

        Public Overrides Function Equals(obj As Object) As Boolean
            If TypeOf obj Is IPv4Address Then
                Return Equals(DirectCast(obj, IPv4Address))
            End If
            Return False
        End Function

        Public Overrides Function GetHashCode() As Integer
            Return ToInt32()
        End Function

        Public Shared Operator =(left As IPv4Address, right As IPv4Address) As Boolean
            Return left.Equals(right)
        End Operator

        Public Shared Operator <>(left As IPv4Address, right As IPv4Address) As Boolean
            Return Not left.Equals(right)
        End Operator
#End Region

#Region "IComparable Implementation"
        Public Function CompareTo(other As IPv4Address) As Integer Implements IComparable(Of IPv4Address).CompareTo
            Return ToUInt32().CompareTo(other.ToUInt32())
        End Function

        Public Shared Operator <(left As IPv4Address, right As IPv4Address) As Boolean
            Return left.ToUInt32() < right.ToUInt32()
        End Operator

        Public Shared Operator >(left As IPv4Address, right As IPv4Address) As Boolean
            Return left.ToUInt32() > right.ToUInt32()
        End Operator

        Public Shared Operator <=(left As IPv4Address, right As IPv4Address) As Boolean
            Return left.ToUInt32() <= right.ToUInt32()
        End Operator

        Public Shared Operator >=(left As IPv4Address, right As IPv4Address) As Boolean
            Return left.ToUInt32() >= right.ToUInt32()
        End Operator
#End Region

#Region "Arithmetic Operators"
        Public Shared Operator +(address As IPv4Address, offset As Integer) As IPv4Address
            Return FromUInt32(address.ToUInt32() + CUInt(offset))
        End Operator

        Public Shared Operator -(address As IPv4Address, offset As Integer) As IPv4Address
            Return FromUInt32(address.ToUInt32() - CUInt(offset))
        End Operator

        Public Shared Operator -(left As IPv4Address, right As IPv4Address) As Integer
            Return CInt(left.ToUInt32() - right.ToUInt32())
        End Operator
#End Region
    End Structure

    ''' <summary>
    ''' Represents a subnet mask
    ''' </summary>
    Public Structure SubnetMask
        Implements IEquatable(Of SubnetMask)

        Private ReadOnly _octets As Byte()

        Public Sub New(octets As Byte())
            If octets Is Nothing OrElse octets.Length <> 4 Then
                Throw New ArgumentException("Subnet mask must have exactly 4 octets")
            End If
            If Not IsValidMask(octets) Then
                Throw New ArgumentException("Invalid subnet mask - must be contiguous 1s followed by 0s")
            End If
            _octets = CType(octets.Clone(), Byte())
        End Sub

        Private Sub New(octets As Byte(), skipValidation As Boolean)
            _octets = CType(octets.Clone(), Byte())
        End Sub

        ''' <summary>
        ''' Create from CIDR prefix length (0-32)
        ''' </summary>
        Public Shared Function FromPrefixLength(prefixLength As Integer) As SubnetMask
            If prefixLength < 0 OrElse prefixLength > 32 Then
                Throw New ArgumentOutOfRangeException("prefixLength", "Prefix length must be between 0 and 32")
            End If

            If prefixLength = 0 Then
                Return New SubnetMask({CByte(0), CByte(0), CByte(0), CByte(0)}, True)
            End If

            Dim mask As UInteger = &HFFFFFFFFUI << (32 - prefixLength)
            Return New SubnetMask({
                CByte((mask >> 24) And 255),
                CByte((mask >> 16) And 255),
                CByte((mask >> 8) And 255),
                CByte(mask And 255)
            }, True)
        End Function

        ''' <summary>
        ''' Get octets as array
        ''' </summary>
        Public ReadOnly Property Octets As Byte()
            Get
                Return CType(_octets.Clone(), Byte())
            End Get
        End Property

        ''' <summary>
        ''' Get CIDR prefix length
        ''' </summary>
        Public ReadOnly Property PrefixLength As Integer
            Get
                Dim count As Integer = 0
                Dim mask As UInteger = ToUInt32()
                While mask <> 0
                    count += 1
                    mask <<= 1
                End While
                Return count
            End Get
        End Property

        ''' <summary>
        ''' Convert to 32-bit integer
        ''' </summary>
        Public Function ToInt32() As Integer
            Return (_octets(0) << 24) Or (_octets(1) << 16) Or (_octets(2) << 8) Or _octets(3)
        End Function

        ''' <summary>
        ''' Convert to unsigned 32-bit integer
        ''' </summary>
        Public Function ToUInt32() As UInteger
            Return CUInt((_octets(0) << 24) Or (_octets(1) << 16) Or (_octets(2) << 8) Or _octets(3))
        End Function

        ''' <summary>
        ''' Get wildcard mask (inverse of subnet mask)
        ''' </summary>
        Public Function GetWildcardMask() As SubnetMask
            Return New SubnetMask({
                CByte(Not _octets(0)),
                CByte(Not _octets(1)),
                CByte(Not _octets(2)),
                CByte(Not _octets(3))
            }, True)
        End Function

        ''' <summary>
        ''' Get number of usable host addresses
        ''' </summary>
        Public Function GetHostCount() As ULong
            Dim prefix = PrefixLength
            If prefix = 32 Then Return 0
            If prefix = 31 Then Return 2
            If prefix = 0 Then Return 4294967294UL
            Return (1UL << (32 - prefix)) - 2
        End Function

        ''' <summary>
        ''' Get total number of addresses in subnet
        ''' </summary>
        Public Function GetTotalAddressCount() As ULong
            If PrefixLength = 0 Then Return 4294967296UL
            Return 1UL << (32 - PrefixLength)
        End Function

        ''' <summary>
        ''' Validate subnet mask
        ''' </summary>
        Private Shared Function IsValidMask(octets As Byte()) As Boolean
            Dim foundZero As Boolean = False
            For i As Integer = 0 To 3
                For bit As Integer = 7 To 0 Step -1
                    Dim bitValue As Boolean = (octets(i) And (1 << bit)) <> 0
                    If Not bitValue Then
                        foundZero = True
                    ElseIf foundZero Then
                        ' Found a 1 after a 0 - invalid mask
                        Return False
                    End If
                Next
            Next
            Return True
        End Function

        ''' <summary>
        ''' Convert to string (dotted decimal notation)
        ''' </summary>
        Public Overrides Function ToString() As String
            Return String.Format("{0}.{1}.{2}.{3}", _octets(0), _octets(1), _octets(2), _octets(3))
        End Function

        ''' <summary>
        ''' Convert to CIDR notation (e.g., "/24")
        ''' </summary>
        Public Function ToCIDRNotation() As String
            Return "/" & PrefixLength.ToString()
        End Function

#Region "IEquatable Implementation"
        Public Overloads Function Equals(other As SubnetMask) As Boolean Implements IEquatable(Of SubnetMask).Equals
            Return _octets(0) = other._octets(0) AndAlso
                   _octets(1) = other._octets(1) AndAlso
                   _octets(2) = other._octets(2) AndAlso
                   _octets(3) = other._octets(3)
        End Function

        Public Overrides Function Equals(obj As Object) As Boolean
            If TypeOf obj Is SubnetMask Then
                Return Equals(DirectCast(obj, SubnetMask))
            End If
            Return False
        End Function

        Public Overrides Function GetHashCode() As Integer
            Return ToInt32()
        End Function

        Public Shared Operator =(left As SubnetMask, right As SubnetMask) As Boolean
            Return left.Equals(right)
        End Operator

        Public Shared Operator <>(left As SubnetMask, right As SubnetMask) As Boolean
            Return Not left.Equals(right)
        End Operator
#End Region

        ''' <summary>
        ''' Common subnet masks
        ''' </summary>
        Public Shared ReadOnly Property ClassA As SubnetMask
            Get
                Return FromPrefixLength(8)
            End Get
        End Property

        Public Shared ReadOnly Property ClassB As SubnetMask
            Get
                Return FromPrefixLength(16)
            End Get
        End Property

        Public Shared ReadOnly Property ClassC As SubnetMask
            Get
                Return FromPrefixLength(24)
            End Get
        End Property
    End Structure

    ''' <summary>
    ''' Represents an IPv4 network/subnet
    ''' </summary>
    Public Class IPv4Network
        Private ReadOnly _networkAddress As IPv4Address
        Private ReadOnly _subnetMask As SubnetMask

        Public Sub New(networkAddress As IPv4Address, subnetMask As SubnetMask)
            ' Calculate the actual network address
            Dim networkUint As UInteger = networkAddress.ToUInt32() And subnetMask.ToUInt32()
            _networkAddress = IPv4Address.FromUInt32(networkUint)
            _subnetMask = subnetMask
        End Sub

        Public Sub New(networkAddress As IPv4Address, prefixLength As Integer)
            Me.New(networkAddress, SubnetMask.FromPrefixLength(prefixLength))
        End Sub

        ''' <summary>
        ''' Network address
        ''' </summary>
        Public ReadOnly Property NetworkAddress As IPv4Address
            Get
                Return _networkAddress
            End Get
        End Property

        ''' <summary>
        ''' Subnet mask
        ''' </summary>
        Public ReadOnly Property SubnetMask As SubnetMask
            Get
                Return _subnetMask
            End Get
        End Property

        ''' <summary>
        ''' Prefix length (CIDR notation)
        ''' </summary>
        Public ReadOnly Property PrefixLength As Integer
            Get
                Return _subnetMask.PrefixLength
            End Get
        End Property

        ''' <summary>
        ''' Broadcast address
        ''' </summary>
        Public ReadOnly Property BroadcastAddress As IPv4Address
            Get
                Dim wildcard As UInteger = Not _subnetMask.ToUInt32()
                Return IPv4Address.FromUInt32(_networkAddress.ToUInt32() Or wildcard)
            End Get
        End Property

        ''' <summary>
        ''' First usable host address
        ''' </summary>
        Public ReadOnly Property FirstUsableHost As IPv4Address
            Get
                If PrefixLength >= 31 Then Return _networkAddress
                Return _networkAddress + 1
            End Get
        End Property

        ''' <summary>
        ''' Last usable host address
        ''' </summary>
        Public ReadOnly Property LastUsableHost As IPv4Address
            Get
                If PrefixLength >= 31 Then Return BroadcastAddress
                Return BroadcastAddress - 1
            End Get
        End Property

        ''' <summary>
        ''' Number of usable host addresses
        ''' </summary>
        Public ReadOnly Property UsableHostCount As ULong
            Get
                Return _subnetMask.GetHostCount()
            End Get
        End Property

        ''' <summary>
        ''' Total number of addresses in subnet
        ''' </summary>
        Public ReadOnly Property TotalAddressCount As ULong
            Get
                Return _subnetMask.GetTotalAddressCount()
            End Get
        End Property

        ''' <summary>
        ''' Check if an IP address is within this network
        ''' </summary>
        Public Function Contains(address As IPv4Address) As Boolean
            Dim addressUint As UInteger = address.ToUInt32()
            Dim networkUint As UInteger = _networkAddress.ToUInt32()
            Dim maskUint As UInteger = _subnetMask.ToUInt32()
            Return (addressUint And maskUint) = networkUint
        End Function

        ''' <summary>
        ''' Check if this network overlaps with another network
        ''' </summary>
        Public Function Overlaps(other As IPv4Network) As Boolean
            Return Contains(other.NetworkAddress) OrElse
                   Contains(other.BroadcastAddress) OrElse
                   other.Contains(_networkAddress) OrElse
                   other.Contains(BroadcastAddress)
        End Function

        ''' <summary>
        ''' Check if this network is a subnet of another network
        ''' </summary>
        Public Function IsSubnetOf(other As IPv4Network) As Boolean
            If PrefixLength <= other.PrefixLength Then Return False
            Return other.Contains(_networkAddress) AndAlso other.Contains(BroadcastAddress)
        End Function

        ''' <summary>
        ''' Check if this network is a supernet of another network
        ''' </summary>
        Public Function IsSupernetOf(other As IPv4Network) As Boolean
            Return other.IsSubnetOf(Me)
        End Function

        ''' <summary>
        ''' Split this network into smaller subnets
        ''' </summary>
        Public Function Split(newPrefixLength As Integer) As List(Of IPv4Network)
            If newPrefixLength <= PrefixLength Then
                Throw New ArgumentException("New prefix length must be greater than current prefix length")
            End If
            If newPrefixLength > 32 Then
                Throw New ArgumentException("Prefix length cannot exceed 32")
            End If

            Dim result As New List(Of IPv4Network)()
            Dim numSubnets As Integer = 1 << (newPrefixLength - PrefixLength)
            Dim subnetSize As UInteger = 1UI << (32 - newPrefixLength)

            Dim currentAddress As UInteger = _networkAddress.ToUInt32()
            For i As Integer = 0 To numSubnets - 1
                result.Add(New IPv4Network(IPv4Address.FromUInt32(currentAddress), newPrefixLength))
                currentAddress += subnetSize
            Next

            Return result
        End Function

        ''' <summary>
        ''' Get supernet (next larger network)
        ''' </summary>
        Public Function GetSupernet() As IPv4Network
            If PrefixLength = 0 Then
                Throw New InvalidOperationException("Cannot get supernet of /0 network")
            End If
            Return New IPv4Network(_networkAddress, PrefixLength - 1)
        End Function

        ''' <summary>
        ''' Convert to CIDR notation string
        ''' </summary>
        Public Overrides Function ToString() As String
            Return String.Format("{0}/{1}", _networkAddress.ToString(), PrefixLength)
        End Function

        ''' <summary>
        ''' Get detailed information string
        ''' </summary>
        Public Function GetInfo() As String
            Dim sb As New Text.StringBuilder()
            sb.AppendLine("Network: " & ToString())
            sb.AppendLine("Network Address: " & _networkAddress.ToString())
            sb.AppendLine("Subnet Mask: " & _subnetMask.ToString())
            sb.AppendLine("Broadcast Address: " & BroadcastAddress.ToString())
            sb.AppendLine("First Host: " & FirstUsableHost.ToString())
            sb.AppendLine("Last Host: " & LastUsableHost.ToString())
            sb.AppendLine("Total Addresses: " & TotalAddressCount.ToString("N0"))
            sb.AppendLine("Usable Hosts: " & UsableHostCount.ToString("N0"))
            Return sb.ToString()
        End Function
    End Class

    ''' <summary>
    ''' IP Address Parser - Parse and validate IP addresses
    ''' </summary>
    Public Class IPAddressParser

        ''' <summary>
        ''' Parse IPv4 address from string
        ''' </summary>
        Public Shared Function ParseIPv4(ip As String) As IPv4Address
            If String.IsNullOrWhiteSpace(ip) Then
                Throw New ArgumentNullException("ip")
            End If

            Dim parts As String() = ip.Split("."c)
            If parts.Length <> 4 Then
                Throw New FormatException("Invalid IPv4 address format - must have 4 octets")
            End If

            Dim octets As Byte() = New Byte(3) {}
            For i As Integer = 0 To 3
                Dim part As String = parts(i).Trim()
                If Not Byte.TryParse(part, octets(i)) Then
                    Throw New FormatException(String.Format("Invalid octet value: {0}", part))
                End If
            Next

            Return New IPv4Address(octets)
        End Function

        ''' <summary>
        ''' Try to parse IPv4 address from string
        ''' </summary>
        Public Shared Function TryParseIPv4(ip As String, ByRef result As IPv4Address) As Boolean
            Try
                result = ParseIPv4(ip)
                Return True
            Catch
                result = Nothing
                Return False
            End Try
        End Function

        ''' <summary>
        ''' Parse subnet mask from string
        ''' </summary>
        Public Shared Function ParseSubnetMask(mask As String) As SubnetMask
            If String.IsNullOrWhiteSpace(mask) Then
                Throw New ArgumentNullException("mask")
            End If

            ' Check if it's CIDR notation (just a number)
            Dim prefixLength As Integer
            If Integer.TryParse(mask, prefixLength) Then
                Return SubnetMask.FromPrefixLength(prefixLength)
            End If

            ' Remove leading slash if present
            If mask.StartsWith("/") Then
                mask = mask.Substring(1)
                If Integer.TryParse(mask, prefixLength) Then
                    Return SubnetMask.FromPrefixLength(prefixLength)
                End If
            End If

            ' Parse as dotted decimal
            Dim parts As String() = mask.Split("."c)
            If parts.Length <> 4 Then
                Throw New FormatException("Invalid subnet mask format")
            End If

            Dim octets As Byte() = New Byte(3) {}
            For i As Integer = 0 To 3
                Dim part As String = parts(i).Trim()
                If Not Byte.TryParse(part, octets(i)) Then
                    Throw New FormatException(String.Format("Invalid octet value: {0}", part))
                End If
            Next

            Return New SubnetMask(octets)
        End Function

        ''' <summary>
        ''' Try to parse subnet mask from string
        ''' </summary>
        Public Shared Function TryParseSubnetMask(mask As String, ByRef result As SubnetMask) As Boolean
            Try
                result = ParseSubnetMask(mask)
                Return True
            Catch
                result = Nothing
                Return False
            End Try
        End Function

        ''' <summary>
        ''' Parse network in CIDR notation (e.g., "192.168.1.0/24")
        ''' </summary>
        Public Shared Function ParseCIDR(cidr As String) As IPv4Network
            If String.IsNullOrWhiteSpace(cidr) Then
                Throw New ArgumentNullException("cidr")
            End If

            Dim parts As String() = cidr.Split("/"c)
            If parts.Length <> 2 Then
                Throw New FormatException("Invalid CIDR format - expected 'IP/prefix'")
            End If

            Dim address As IPv4Address = ParseIPv4(parts(0))
            Dim prefixLength As Integer
            If Not Integer.TryParse(parts(1), prefixLength) Then
                Throw New FormatException("Invalid prefix length")
            End If

            Return New IPv4Network(address, prefixLength)
        End Function

        ''' <summary>
        ''' Try to parse network in CIDR notation
        ''' </summary>
        Public Shared Function TryParseCIDR(cidr As String, ByRef result As IPv4Network) As Boolean
            Try
                result = ParseCIDR(cidr)
                Return True
            Catch
                result = Nothing
                Return False
            End Try
        End Function

        ''' <summary>
        ''' Validate IPv4 address string
        ''' </summary>
        Public Shared Function IsValidIPv4(ip As String) As Boolean
            Dim result As IPv4Address
            Return TryParseIPv4(ip, result)
        End Function

        ''' <summary>
        ''' Validate subnet mask string
        ''' </summary>
        Public Shared Function IsValidSubnetMask(mask As String) As Boolean
            Dim result As SubnetMask
            Return TryParseSubnetMask(mask, result)
        End Function

        ''' <summary>
        ''' Validate CIDR notation string
        ''' </summary>
        Public Shared Function IsValidCIDR(cidr As String) As Boolean
            Dim result As IPv4Network
            Return TryParseCIDR(cidr, result)
        End Function
    End Class

    ''' <summary>
    ''' IP Range - Represents a range of IP addresses
    ''' </summary>
    Public Class IPRange
        Private ReadOnly _startAddress As IPv4Address
        Private ReadOnly _endAddress As IPv4Address

        Public Sub New(startAddress As IPv4Address, endAddress As IPv4Address)
            If startAddress > endAddress Then
                Throw New ArgumentException("Start address must be less than or equal to end address")
            End If
            _startAddress = startAddress
            _endAddress = endAddress
        End Sub

        Public ReadOnly Property StartAddress As IPv4Address
            Get
                Return _startAddress
            End Get
        End Property

        Public ReadOnly Property EndAddress As IPv4Address
            Get
                Return _endAddress
            End Get
        End Property

        ''' <summary>
        ''' Get count of addresses in range
        ''' </summary>
        Public ReadOnly Property Count As ULong
            Get
                Return CULng(_endAddress.ToUInt32() - _startAddress.ToUInt32()) + 1
            End Get
        End Property

        ''' <summary>
        ''' Check if an address is within this range
        ''' </summary>
        Public Function Contains(address As IPv4Address) As Boolean
            Return address >= _startAddress AndAlso address <= _endAddress
        End Function

        ''' <summary>
        ''' Check if this range overlaps with another range
        ''' </summary>
        Public Function Overlaps(other As IPRange) As Boolean
            Return _startAddress <= other._endAddress AndAlso _endAddress >= other._startAddress
        End Function

        ''' <summary>
        ''' Merge with another range (if adjacent or overlapping)
        ''' </summary>
        Public Function Merge(other As IPRange) As IPRange
            If Not Overlaps(other) AndAlso Not IsAdjacentTo(other) Then
                Throw New ArgumentException("Cannot merge non-adjacent, non-overlapping ranges")
            End If

            Dim newStart As IPv4Address = If(_startAddress < other._startAddress, _startAddress, other._startAddress)
            Dim newEnd As IPv4Address = If(_endAddress > other._endAddress, _endAddress, other._endAddress)
            Return New IPRange(newStart, newEnd)
        End Function

        ''' <summary>
        ''' Check if this range is adjacent to another range
        ''' </summary>
        Public Function IsAdjacentTo(other As IPRange) As Boolean
            Return _endAddress + 1 = other._startAddress OrElse other._endAddress + 1 = _startAddress
        End Function

        ''' <summary>
        ''' Enumerate all addresses in range
        ''' </summary>
        Public Iterator Function GetAddresses() As IEnumerable(Of IPv4Address)
            Dim current As UInteger = _startAddress.ToUInt32()
            Dim [end] As UInteger = _endAddress.ToUInt32()
            While current <= [end]
                Yield IPv4Address.FromUInt32(current)
                current += 1
            End While
        End Function

        ''' <summary>
        ''' Convert to CIDR networks
        ''' </summary>
        Public Function ToCIDRNetworks() As List(Of IPv4Network)
            Dim result As New List(Of IPv4Network)()
            Dim current As UInteger = _startAddress.ToUInt32()
            Dim [end] As UInteger = _endAddress.ToUInt32()

            While current <= [end]
                ' Find the largest block that starts at current and fits within the range
                Dim maxPrefix As Integer = 32
                While maxPrefix > 0
                    Dim blockSize As UInteger = 1UI << (32 - maxPrefix)
                    ' Check if current is aligned to this block size
                    If (current And (blockSize - 1)) <> 0 Then
                        maxPrefix -= 1
                        Continue While
                    End If
                    ' Check if block fits within remaining range
                    If current + blockSize - 1 > [end] Then
                        maxPrefix -= 1
                        Continue While
                    End If
                    Exit While
                End While

                If maxPrefix > 0 Then
                    result.Add(New IPv4Network(IPv4Address.FromUInt32(current), maxPrefix))
                    current += CUInt(1 << (32 - maxPrefix))
                Else
                    result.Add(New IPv4Network(IPv4Address.FromUInt32(current), 32))
                    current += 1
                End If
            End While

            Return result
        End Function

        Public Overrides Function ToString() As String
            Return String.Format("{0} - {1}", _startAddress.ToString(), _endAddress.ToString())
        End Function
    End Class

    ''' <summary>
    ''' IP Address Calculator - Various IP calculations
    ''' </summary>
    Public Class IPAddressCalculator

        ''' <summary>
        ''' Calculate network address from IP and subnet mask
        ''' </summary>
        Public Shared Function GetNetworkAddress(ipAddress As IPv4Address, subnetMask As SubnetMask) As IPv4Address
            Return IPv4Address.FromUInt32(ipAddress.ToUInt32() And subnetMask.ToUInt32())
        End Function

        ''' <summary>
        ''' Calculate broadcast address from IP and subnet mask
        ''' </summary>
        Public Shared Function GetBroadcastAddress(ipAddress As IPv4Address, subnetMask As SubnetMask) As IPv4Address
            Dim networkAddress As UInteger = GetNetworkAddress(ipAddress, subnetMask).ToUInt32()
            Dim wildcard As UInteger = Not subnetMask.ToUInt32()
            Return IPv4Address.FromUInt32(networkAddress Or wildcard)
        End Function

        ''' <summary>
        ''' Calculate first usable host address
        ''' </summary>
        Public Shared Function GetFirstUsableHost(networkAddress As IPv4Address, subnetMask As SubnetMask) As IPv4Address
            If subnetMask.PrefixLength >= 31 Then
                Return networkAddress
            End If
            Return networkAddress + 1
        End Function

        ''' <summary>
        ''' Calculate last usable host address
        ''' </summary>
        Public Shared Function GetLastUsableHost(networkAddress As IPv4Address, subnetMask As SubnetMask) As IPv4Address
            Dim broadcastAddress As IPv4Address = GetBroadcastAddress(networkAddress, subnetMask)
            If subnetMask.PrefixLength >= 31 Then
                Return broadcastAddress
            End If
            Return broadcastAddress - 1
        End Function

        ''' <summary>
        ''' Get next IP address
        ''' </summary>
        Public Shared Function GetNextAddress(address As IPv4Address) As IPv4Address
            Return address + 1
        End Function

        ''' <summary>
        ''' Get previous IP address
        ''' </summary>
        Public Shared Function GetPreviousAddress(address As IPv4Address) As IPv4Address
            Return address - 1
        End Function

        ''' <summary>
        ''' Calculate number of subnets that can be created
        ''' </summary>
        Public Shared Function GetSubnetCount(network As IPv4Network, newPrefixLength As Integer) As Integer
            If newPrefixLength <= network.PrefixLength Then
                Throw New ArgumentException("New prefix length must be greater than current prefix length")
            End If
            Return 1 << (newPrefixLength - network.PrefixLength)
        End Function

        ''' <summary>
        ''' Check if two networks can be summarized (supernetting)
        ''' </summary>
        Public Shared Function CanSummarize(network1 As IPv4Network, network2 As IPv4Network) As Boolean
            If network1.PrefixLength <> network2.PrefixLength Then
                Return False
            End If

            If network1.PrefixLength = 0 Then
                Return False
            End If

            Dim supernet As IPv4Network = network1.GetSupernet()
            Return supernet.Contains(network2.NetworkAddress) AndAlso supernet.Contains(network2.BroadcastAddress)
        End Function

        ''' <summary>
        ''' Summarize two networks into a supernet
        ''' </summary>
        Public Shared Function Summarize(network1 As IPv4Network, network2 As IPv4Network) As IPv4Network
            If Not CanSummarize(network1, network2) Then
                Throw New ArgumentException("Networks cannot be summarized")
            End If
            Return network1.GetSupernet()
        End Function

        ''' <summary>
        ''' Get all IP addresses between two addresses (inclusive)
        ''' </summary>
        Public Shared Function GetIPRange(startIP As IPv4Address, endIP As IPv4Address) As List(Of IPv4Address)
            Dim result As New List(Of IPv4Address)()
            Dim start As UInteger = startIP.ToUInt32()
            Dim [end] As UInteger = endIP.ToUInt32()

            If start > [end] Then
                Throw New ArgumentException("Start IP must be less than or equal to end IP")
            End If

            ' Limit to reasonable size
            If [end] - start > 100000 Then
                Throw New ArgumentException("Range too large - maximum 100,000 addresses")
            End If

            Dim current As UInteger = start
            While current <= [end]
                result.Add(IPv4Address.FromUInt32(current))
                current += 1
            End While

            Return result
        End Function
    End Class

    ''' <summary>
    ''' IP Address Formatter - Format IP addresses in various ways
    ''' </summary>
    Public Class IPAddressFormatter

        ''' <summary>
        ''' Format IPv4 address as dotted decimal
        ''' </summary>
        Public Shared Function ToDottedDecimal(address As IPv4Address) As String
            Return address.ToString()
        End Function

        ''' <summary>
        ''' Format IPv4 address as binary string
        ''' </summary>
        Public Shared Function ToBinary(address As IPv4Address) As String
            Return address.ToBinaryString()
        End Function

        ''' <summary>
        ''' Format IPv4 address as hexadecimal string
        ''' </summary>
        Public Shared Function ToHex(address As IPv4Address) As String
            Return address.ToHexString()
        End Function

        ''' <summary>
        ''' Format IPv4 address as integer
        ''' </summary>
        Public Shared Function ToInteger(address As IPv4Address) As String
            Return address.ToUInt32().ToString()
        End Function

        ''' <summary>
        ''' Format subnet mask as CIDR prefix length
        ''' </summary>
        Public Shared Function ToCIDR(mask As SubnetMask) As String
            Return "/" & mask.PrefixLength.ToString()
        End Function

        ''' <summary>
        ''' Format network info as detailed string
        ''' </summary>
        Public Shared Function FormatNetworkInfo(network As IPv4Network) As String
            Return network.GetInfo()
        End Function

        ''' <summary>
        ''' Format IP address with all representations
        ''' </summary>
        Public Shared Function FormatAll(address As IPv4Address) As String
            Dim sb As New Text.StringBuilder()
            sb.AppendLine("Decimal: " & address.ToString())
            sb.AppendLine("Binary:  " & address.ToBinaryString())
            sb.AppendLine("Hex:     " & address.ToHexString())
            sb.AppendLine("Integer: " & address.ToUInt32().ToString())
            sb.AppendLine("Class:   " & address.GetClass())
            sb.AppendLine("Type:    " & address.GetTypeDescription())
            Return sb.ToString()
        End Function
    End Class

End Namespace