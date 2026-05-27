// Example usage of ip_calculator_utils package
package main

import (
	"fmt"

	ipcalc "github.com/ayukyo/alltoolkit/Go/ip_calculator_utils"
)

func main() {
	fmt.Println("=== IP 子网计算器示例 ===")
	fmt.Println()

	// 示例1: 解析CIDR并获取详细信息
	fmt.Println("【示例1】解析 CIDR 获取子网信息")
	fmt.Println("----------------------------------------")
	example1()

	// 示例2: 检查IP是否在子网内
	fmt.Println()
	fmt.Println("【示例2】检查 IP 是否在子网内")
	fmt.Println("----------------------------------------")
	example2()

	// 示例3: 子网掩码转换
	fmt.Println()
	fmt.Println("【示例3】子网掩码与前缀长度转换")
	fmt.Println("----------------------------------------")
	example3()

	// 示例4: 计算子网划分
	fmt.Println()
	fmt.Println("【示例4】子网划分计算")
	fmt.Println("----------------------------------------")
	example4()

	// 示例5: IP地址比较和转换
	fmt.Println()
	fmt.Println("【示例5】IP地址比较与数值转换")
	fmt.Println("----------------------------------------")
	example5()

	// 示例6: IPv6支持
	fmt.Println()
	fmt.Println("【示例6】IPv6 支持")
	fmt.Println("----------------------------------------")
	example6()

	// 示例7: 端口范围解析
	fmt.Println()
	fmt.Println("【示例7】端口范围解析")
	fmt.Println("----------------------------------------")
	example7()

	// 示例8: IP分类
	fmt.Println()
	fmt.Println("【示例8】IP地址分类")
	fmt.Println("----------------------------------------")
	example8()
}

func example1() {
	cidrs := []string{
		"192.168.1.0/24",
		"10.0.0.0/8",
		"172.16.0.0/12",
		"192.168.100.0/30",
	}

	for _, cidr := range cidrs {
		info, err := ipcalc.GetSubnetInfo(cidr)
		if err != nil {
			fmt.Printf("错误: %v\n", err)
			continue
		}

		fmt.Printf("CIDR: %s\n", cidr)
		fmt.Printf("  网络地址: %s\n", info.NetworkAddress)
		fmt.Printf("  子网掩码: %s\n", info.SubnetMask)
		fmt.Printf("  通配符掩码: %s\n", info.WildcardMask)
		fmt.Printf("  前缀长度: %d\n", info.PrefixLength)
		fmt.Printf("  总IP数量: %d\n", info.TotalHosts)
		fmt.Printf("  可用IP数量: %d\n", info.UsableHosts)
		if info.IPVersion == 4 {
			fmt.Printf("  广播地址: %s\n", info.BroadcastAddr)
			fmt.Printf("  第一个可用: %s\n", info.FirstUsable)
			fmt.Printf("  最后一个可用: %s\n", info.LastUsable)
		}
		fmt.Printf("  私有地址: %v\n", info.IsPrivate)
		fmt.Printf("  回环地址: %v\n", info.IsLoopback)
		fmt.Println()
	}
}

func example2() {
	testCases := []struct {
		ip   string
		cidr string
	}{
		{"192.168.1.100", "192.168.1.0/24"},
		{"192.168.2.1", "192.168.1.0/24"},
		{"10.10.10.10", "10.0.0.0/8"},
		{"172.17.0.1", "172.16.0.0/12"},
	}

	for _, tc := range testCases {
		inRange, err := ipcalc.IPInRange(tc.ip, tc.cidr)
		if err != nil {
			fmt.Printf("错误: %v\n", err)
			continue
		}

		status := "不在范围内"
		if inRange {
			status = "在范围内 ✓"
		}
		fmt.Printf("%s %s -> %s\n", tc.ip, status, tc.cidr)
	}

	fmt.Println()
	fmt.Println("检查 IP 是否在多个子网中:")
	cidrs := []string{"10.0.0.0/8", "172.16.0.0/12", "192.168.0.0/16"}
	ips := []string{"10.1.2.3", "172.16.0.1", "8.8.8.8", "192.168.1.1"}

	for _, ip := range ips {
		inRange, match, _ := ipcalc.IPInMultipleRanges(ip, cidrs)
		if inRange {
			fmt.Printf("%s -> 在私有地址范围内 (%s)\n", ip, match)
		} else {
			fmt.Printf("%s -> 不在私有地址范围内 (公网IP)\n", ip)
		}
	}
}

func example3() {
	// 前缀长度转子网掩码
	prefixes := []int{8, 16, 24, 25, 30, 32}
	fmt.Println("前缀长度 -> 子网掩码:")
	for _, p := range prefixes {
		mask, _ := ipcalc.SubnetToMask(p, false)
		fmt.Printf("  /%d -> %s\n", p, mask)
	}

	fmt.Println()

	// 子网掩码转前缀长度
	masks := []string{"255.0.0.0", "255.255.0.0", "255.255.255.0", "255.255.255.128", "255.255.255.252"}
	fmt.Println("子网掩码 -> 前缀长度:")
	for _, m := range masks {
		prefix, _ := ipcalc.MaskToPrefixLength(m)
		fmt.Printf("  %s -> /%d\n", m, prefix)
	}
}

func example4() {
	cidr := "192.168.1.0/24"
	newPrefix := 26

	fmt.Printf("将 %s 划分为 /%d 子网:\n", cidr, newPrefix)
	fmt.Println()

	subnets, err := ipcalc.CalculateSubnets(cidr, newPrefix)
	if err != nil {
		fmt.Printf("错误: %v\n", err)
		return
	}

	for i, subnet := range subnets {
		fmt.Printf("子网 %d: %s - %s (%d 个可用IP)\n", i+1, subnet.Start, subnet.End, subnet.Count)
	}

	fmt.Println()
	fmt.Println("使用 SplitCIDRByMask 获取 CIDR 表示:")
	cidrs, _ := ipcalc.SplitCIDRByMask(cidr, newPrefix)
	for i, c := range cidrs {
		fmt.Printf("  子网 %d: %s\n", i+1, c)
	}
}

func example5() {
	// IP地址比较
	fmt.Println("IP地址比较:")
	comparisons := [][2]string{
		{"192.168.1.1", "192.168.1.2"},
		{"10.0.0.1", "192.168.1.1"},
		{"172.16.0.1", "172.16.0.1"},
	}

	for _, pair := range comparisons {
		result, _ := ipcalc.CompareIPs(pair[0], pair[1])
		var symbol string
		switch result {
		case -1:
			symbol = "<"
		case 0:
			symbol = "=="
		case 1:
			symbol = ">"
		}
		fmt.Printf("  %s %s %s\n", pair[0], symbol, pair[1])
	}

	fmt.Println()

	// IP地址与整数转换
	fmt.Println("IP地址与整数转换:")
	ips := []string{"0.0.0.1", "0.0.1.0", "1.0.0.0", "192.168.1.1"}
	for _, ip := range ips {
		n, _ := ipcalc.IPToInt(ip)
		fmt.Printf("  %s -> %d\n", ip, n)

		// 转换回去验证
		back, _ := ipcalc.IntToIP(n)
		fmt.Printf("  %d -> %s\n", n, back)
	}
}

func example6() {
	ipv6CIDRs := []string{
		"2001:db8::/32",
		"fe80::/10",
		"::1/128",
		"fd00::/8",
	}

	for _, cidr := range ipv6CIDRs {
		info, err := ipcalc.GetSubnetInfo(cidr)
		if err != nil {
			fmt.Printf("错误: %v\n", err)
			continue
		}

		fmt.Printf("CIDR: %s\n", cidr)
		fmt.Printf("  网络地址: %s\n", info.NetworkAddress)
		fmt.Printf("  前缀长度: %d\n", info.PrefixLength)
		fmt.Printf("  IP版本: IPv%d\n", info.IPVersion)
		if info.TotalHosts > 1000000 {
			fmt.Printf("  IP数量: 极大 (2^%d)\n", 128-info.PrefixLength)
		} else {
			fmt.Printf("  IP数量: %d\n", info.TotalHosts)
		}
		fmt.Printf("  私有地址: %v\n", info.IsPrivate)
		fmt.Println()
	}

	// IPv6 IP范围检查
	fmt.Println("IPv6 范围检查:")
	testCases := []struct {
		ip   string
		cidr string
	}{
		{"2001:db8::1", "2001:db8::/32"},
		{"2001:db9::1", "2001:db8::/32"},
		{"::1", "::1/128"},
	}

	for _, tc := range testCases {
		inRange, _ := ipcalc.IPInRange(tc.ip, tc.cidr)
		status := "不在范围内"
		if inRange {
			status = "在范围内 ✓"
		}
		fmt.Printf("%s %s -> %s\n", tc.ip, status, tc.cidr)
	}
}

func example7() {
	ports := []string{"80", "443", "80-443", "1024-65535"}

	for _, p := range ports {
		start, end, err := ipcalc.ParsePortRange(p)
		if err != nil {
			fmt.Printf("%s -> 错误: %v\n", p, err)
			continue
		}

		if start == end {
			fmt.Printf("%s -> 单端口: %d\n", p, start)
		} else {
			fmt.Printf("%s -> 范围: %d-%d (共 %d 个端口)\n", p, start, end, end-start+1)
		}
	}

	fmt.Println()
	fmt.Println("端口验证:")
	testPorts := []int{0, 1, 80, 443, 65535, 65536}
	for _, port := range testPorts {
		if ipcalc.ValidatePort(port) {
			fmt.Printf("  端口 %d -> 有效\n", port)
		} else {
			fmt.Printf("  端口 %d -> 无效\n", port)
		}
	}
}

func example8() {
	ips := []string{
		"10.0.0.1",
		"127.0.0.1",
		"128.0.0.1",
		"172.16.0.1",
		"192.168.1.1",
		"224.0.0.1",
		"240.0.0.1",
	}

	fmt.Println("IPv4 地址分类:")
	for _, ip := range ips {
		class, err := ipcalc.GetIPClass(ip)
		if err != nil {
			fmt.Printf("%s -> 错误: %v\n", ip, err)
			continue
		}

		valid, version := ipcalc.ValidateIP(ip)
		fmt.Printf("%s -> Class %s (IPv%d, 有效: %v)\n", ip, class, version, valid)
	}

	fmt.Println()
	fmt.Println("IP地址详细信息:")
	for _, ip := range ips[:4] {
		valid, version := ipcalc.ValidateIP(ip)
		if valid {
			cidr, _ := ipcalc.FormatIPWithCIDR(ip, 32)
			fmt.Printf("  %s -> %s (IPv%d)\n", ip, cidr, version)
		}
	}
}