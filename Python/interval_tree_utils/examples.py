"""
区间树工具使用示例
==================

本示例演示 IntervalTree 的各种使用场景。
"""

from interval_tree import IntervalTree, Interval


def example_basic_usage():
    """基本使用示例"""
    print("=" * 50)
    print("基本使用示例")
    print("=" * 50)
    
    # 创建区间树
    tree = IntervalTree()
    
    # 插入区间
    tree.insert(Interval(1, 10, value="区间A"))
    tree.insert(Interval(5, 15, value="区间B"))
    tree.insert(Interval(20, 30, value="区间C"))
    
    print(f"树中区间数量: {len(tree)}")
    print(f"树的高度: {tree.height()}")
    print()
    
    # 点查询
    print("点查询:")
    point = 7
    results = tree.query_point(point)
    print(f"  包含点 {point} 的区间: {[f'{r.value}' for r in results]}")
    
    point = 25
    results = tree.query_point(point)
    print(f"  包含点 {point} 的区间: {[f'{r.value}' for r in results]}")
    print()


def example_meeting_scheduler():
    """会议调度示例"""
    print("=" * 50)
    print("会议调度示例")
    print("=" * 50)
    
    # 创建会议时间表
    meetings = IntervalTree()
    
    meetings.insert(Interval(9, 10, value="团队晨会"))
    meetings.insert(Interval(10, 12, value="产品评审"))
    meetings.insert(Interval(14, 16, value="技术分享"))
    meetings.insert(Interval(15, 17, value="客户会议"))
    meetings.insert(Interval(16, 18, value="周报"))
    
    # 检查时间冲突
    print("时间冲突检查:")
    new_meeting = Interval(11, 14)
    conflicts = meetings.query_overlaps(new_meeting)
    print(f"  新会议时间 {new_meeting} 冲突: {[c.value for c in conflicts]}")
    
    new_meeting = Interval(12, 14)
    conflicts = meetings.query_overlaps(new_meeting)
    print(f"  新会议时间 {new_meeting} 冲突: {[c.value for c in conflicts]}")
    
    # 查找特定时间段在哪个会议中
    print("\n查找会议:")
    time = 15.5
    results = meetings.query_point(time)
    print(f"  时间 {time} 在会议: {[r.value for r in results]}")
    print()


def example_resource_allocation():
    """资源分配示例"""
    print("=" * 50)
    print("服务器资源分配示例")
    print("=" * 50)
    
    # 创建服务器资源分配表
    allocations = IntervalTree()
    
    allocations.insert(Interval(0, 100, value="服务器A: 用户服务"))
    allocations.insert(Interval(50, 200, value="服务器B: 数据库"))
    allocations.insert(Interval(150, 250, value="服务器C: 缓存"))
    allocations.insert(Interval(200, 300, value="服务器D: 文件存储"))
    
    # 查找特定资源使用者
    resource_id = 75
    users = allocations.query_point(resource_id)
    print(f"资源 {resource_id} 被使用: {[u.value for u in users]}")
    
    # 查找资源空闲段
    print("\n空闲资源段 (0-400):")
    gaps = allocations.find_all_gaps(0, 400)
    for gap in gaps:
        print(f"  空闲段: {gap}")
    print()


def example_genomic_analysis():
    """基因组分析示例"""
    print("=" * 50)
    print("基因组区域分析示例")
    print("=" * 50)
    
    # 创建基因区域数据库
    genes = IntervalTree()
    
    genes.insert(Interval(1000, 2000, value="GeneA"))
    genes.insert(Interval(1500, 2500, value="GeneB"))
    genes.insert(Interval(3000, 4000, value="GeneC"))
    genes.insert(Interval(3500, 4500, value="GeneD"))
    
    # 查找特定位置的基因
    position = 1700
    overlapping = genes.query_point(position)
    print(f"位置 {position} 的基因: {[g.value for g in overlapping]}")
    
    # 查找区域重叠
    region = Interval(1200, 1600)
    overlapping = genes.query_overlaps(region)
    print(f"区域 {region} 重叠的基因: {[g.value for g in overlapping]}")
    
    # 查找完全包含某区域的基因
    contained = genes.query_contains(Interval(1600, 1800))
    print(f"包含区域 [1600, 1800] 的基因: {[g.value for g in contained]}")
    print()


def example_calendar():
    """日历事件示例"""
    print("=" * 50)
    print("日历事件管理示例")
    print("=" * 50)
    
    # 创建日历事件（时间单位：小时，从今天0点开始）
    calendar = IntervalTree()
    
    calendar.insert(Interval(9, 10, value="晨会"))
    calendar.insert(Interval(12, 13, value="午餐"))
    calendar.insert(Interval(14, 16, value="项目讨论"))
    calendar.insert(Interval(16, 17, value="代码审查"))
    calendar.insert(Interval(17, 18, value="团队活动"))
    
    # 检查新事件是否冲突
    print("新事件冲突检查:")
    new_events = [
        Interval(9.5, 10.5, value="临时会议"),
        Interval(11, 12, value="客户电话"),
        Interval(18, 19, value="下班锻炼"),
    ]
    
    for event in new_events:
        conflicts = calendar.query_overlaps(event)
        if conflicts:
            print(f"  {event.value} ({event.start}:00-{event.end}:00) 冲突: {[c.value for c in conflicts]}")
        else:
            print(f"  {event.value} ({event.start}:00-{event.end}:00) 无冲突 ✓")
    print()


def example_ip_address_allocation():
    """IP地址分配示例"""
    print("=" * 50)
    print("IP地址段分配示例")
    print("=" * 50)
    
    # 创建IP地址段分配
    ip_pool = IntervalTree()
    
    ip_pool.insert(Interval(0, 255, value="部门A: 192.168.1.0/24"))
    ip_pool.insert(Interval(256, 511, value="部门B: 192.168.2.0/24"))
    ip_pool.insert(Interval(512, 767, value="部门C: 192.168.3.0/24"))
    ip_pool.insert(Interval(768, 1023, value="保留: 192.168.4.0/24"))
    
    # 查找IP归属
    def ip_to_int(ip_str):
        parts = [int(p) for p in ip_str.split('.')]
        return parts[2] * 256 + parts[3]
    
    test_ips = ["192.168.1.100", "192.168.2.50", "192.168.3.200"]
    for ip in test_ips:
        ip_int = ip_to_int(ip)
        result = ip_pool.query_point(ip_int)
        if result:
            print(f"  {ip} → {result[0].value}")
    
    # 查找未分配的地址段
    print("\n未分配地址段 (192.168.5.0 - 192.168.10.255):")
    gaps = ip_pool.find_all_gaps(1024, 2815)
    for gap in gaps:
        start_ip = f"192.168.{gap.start // 256}.{gap.start % 256}"
        end_ip = f"192.168.{gap.end // 256}.{gap.end % 256}"
        print(f"  {start_ip} - {end_ip}")
    print()


def example_interval_operations():
    """区间操作示例"""
    print("=" * 50)
    print("区间操作示例")
    print("=" * 50)
    
    a = Interval(1, 10)
    b = Interval(5, 15)
    
    print(f"区间 A: {a}")
    print(f"区间 B: {b}")
    print()
    
    # 重叠检测
    print(f"A 与 B 重叠: {a.overlaps(b)}")
    
    # 交集
    intersection = a.intersection(b)
    print(f"A 与 B 的交集: {intersection}")
    
    # 并集
    union = a.union(b)
    print(f"A 与 B 的并集: {union}")
    
    # 包含检测
    print(f"A 包含 B: {a.contains(b)}")
    
    inner = Interval(3, 7)
    print(f"A 包含 {inner}: {a.contains(inner)}")
    
    # 点包含
    print(f"点 5 在 A 中: {a.contains_point(5)}")
    print(f"点 15 在 A 中: {a.contains_point(15)}")
    print()


def example_from_tuples():
    """从元组创建示例"""
    print("=" * 50)
    print("从元组创建区间树")
    print("=" * 50)
    
    # 从元组列表创建
    data = [
        (1, 5, "A"),
        (3, 8, "B"),
        (10, 15, "C"),
    ]
    
    tree = IntervalTree.from_tuples(data)
    print(f"创建了包含 {len(tree)} 个区间的树")
    
    # 查询
    results = tree.query_point(4)
    print(f"点 4 的查询结果: {[r.value for r in results]}")
    print()


def example_statistics():
    """统计信息示例"""
    print("=" * 50)
    print("区间树统计信息")
    print("=" * 50)
    
    tree = IntervalTree()
    
    # 添加一些区间
    for i in range(10):
        tree.insert(Interval(i * 10, i * 10 + 8, value=f"区间{i}"))
    
    stats = tree.get_statistics()
    print(f"区间数量: {stats['size']}")
    print(f"树高度: {stats['height']}")
    print(f"节点数量: {stats['node_count']}")
    print(f"是否为空: {stats['is_empty']}")
    print()


if __name__ == '__main__':
    example_basic_usage()
    example_meeting_scheduler()
    example_resource_allocation()
    example_genomic_analysis()
    example_calendar()
    example_ip_address_allocation()
    example_interval_operations()
    example_from_tuples()
    example_statistics()
    
    print("=" * 50)
    print("所有示例运行完成！")
    print("=" * 50)