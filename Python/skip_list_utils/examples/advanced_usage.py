"""
Skip List 高级用法示例

演示跳表的高级应用场景：
- 数据库索引模拟
- 排行榜系统
- 时间窗口统计
- 区间合并
- LRU 缓存替代
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import SkipList, SkipListSet, ConcurrentSkipList
import time


def database_index_simulation():
    """模拟数据库索引"""
    print("=" * 60)
    print("数据库索引模拟")
    print("=" * 60)
    
    # 模拟用户表
    users = {
        1: {"name": "Alice", "age": 30, "city": "Beijing"},
        2: {"name": "Bob", "age": 25, "city": "Shanghai"},
        3: {"name": "Charlie", "age": 35, "city": "Guangzhou"},
        4: {"name": "Diana", "age": 28, "city": "Beijing"},
        5: {"name": "Eve", "age": 32, "city": "Shanghai"},
    }
    
    # 创建年龄索引
    age_index = SkipList[int]()
    for user_id, user in users.items():
        age_index.insert(user["age"], user_id)
    
    # 创建城市索引（多值索引）
    city_index = SkipList[str](allow_duplicates=False)
    city_to_users = {}  # 辅助存储城市到用户列表的映射
    
    for user_id, user in users.items():
        city = user["city"]
        if city not in city_to_users:
            city_to_users[city] = []
        city_to_users[city].append(user_id)
    
    print("按年龄排序的用户 ID:")
    for age, user_id in age_index:
        print(f"  年龄 {age}: 用户 {user_id} ({users[user_id]['name']})")
    
    # 范围查询：25-30 岁的用户
    print("\n25-30 岁的用户:")
    for age, user_id in age_index.range(25, 30):
        print(f"  {users[user_id]['name']}: {age}岁")
    
    # 最年轻和最年长
    youngest = age_index.first()
    oldest = age_index.last()
    print(f"\n最年轻: {users[youngest[1]]['name']} ({youngest[0]}岁)")
    print(f"最年长: {users[oldest[1]]['name']} ({oldest[0]}岁)")


def leaderboard_system():
    """排行榜系统"""
    print("\n" + "=" * 60)
    print("排行榜系统")
    print("=" * 60)
    
    # 使用负分数作为 key 来实现降序排名
    # 分数越高，负值越小，排在前面
    leaderboard = SkipList[int]()
    player_names = {}
    
    def add_player(player_id: str, name: str, score: int):
        leaderboard.insert(-score, player_id)  # 负分数
        player_names[player_id] = name
    
    def get_rank(player_id: str, score: int) -> int:
        """获取排名（1 开始）"""
        rank = 0
        for s, pid in leaderboard:
            rank += 1
            if pid == player_id:
                return rank
        return -1
    
    def get_top_n(n: int):
        """获取前 N 名"""
        result = []
        for i, (neg_score, player_id) in enumerate(leaderboard):
            if i >= n:
                break
            result.append((i + 1, player_names[player_id], -neg_score))
        return result
    
    # 添加玩家
    add_player("p1", "Alice", 1500)
    add_player("p2", "Bob", 2000)
    add_player("p3", "Charlie", 1800)
    add_player("p4", "Diana", 2500)
    add_player("p5", "Eve", 1200)
    
    print("排行榜:")
    for rank, name, score in get_top_n(5):
        print(f"  #{rank} {name}: {score}分")


def time_window_statistics():
    """时间窗口统计"""
    print("\n" + "=" * 60)
    print("时间窗口统计")
    print("=" * 60)
    
    # 使用时间戳作为 key
    events = SkipList[float]()
    
    # 添加事件（时间戳 -> 事件数据）
    now = time.time()
    events.insert(now - 300, {"type": "click", "user": "A"})  # 5分钟前
    events.insert(now - 120, {"type": "purchase", "user": "B"})  # 2分钟前
    events.insert(now - 60, {"type": "click", "user": "C"})  # 1分钟前
    events.insert(now - 30, {"type": "click", "user": "A"})  # 30秒前
    events.insert(now - 10, {"type": "purchase", "user": "D"})  # 10秒前
    
    # 统计最近 1 分钟的事件
    one_min_ago = now - 60
    recent_events = list(events.range(start_key=one_min_ago))
    print(f"最近 1 分钟的事件数: {len(recent_events)}")
    
    # 统计最近 5 分钟的购买事件
    five_min_ago = now - 300
    purchases = sum(
        1 for _, data in events.range(start_key=five_min_ago)
        if data["type"] == "purchase"
    )
    print(f"最近 5 分钟的购买数: {purchases}")
    
    # 计算事件频率
    total_events = events.size
    total_time = 300  # 5分钟
    print(f"事件频率: {total_events / total_time * 60:.2f} 事件/分钟")


def interval_operations():
    """区间操作"""
    print("\n" + "=" * 60)
    print("区间操作示例")
    print("=" * 60)
    
    # 管理区间 [start, end)
    intervals = SkipList[int]()
    
    def add_interval(start: int, end: int, label: str):
        """添加区间"""
        intervals.insert(start, {"end": end, "label": label})
    
    def find_overlapping(point: int):
        """找到包含指定点的所有区间"""
        result = []
        # 遍历所有起点小于等于 point 的区间
        for start, data in intervals.range(end_key=point):
            if data["end"] > point:
                result.append((start, data["end"], data["label"]))
        return result
    
    def merge_intervals():
        """合并重叠区间"""
        if intervals.is_empty:
            return []
        
        merged = []
        current_start, current_data = intervals.first()
        current_end = current_data["end"]
        current_label = current_data["label"]
        
        for start, data in intervals:
            if start <= current_end:  # 重叠
                current_end = max(current_end, data["end"])
            else:
                merged.append((current_start, current_end, current_label))
                current_start = start
                current_end = data["end"]
                current_label = data["label"]
        
        merged.append((current_start, current_end, current_label))
        return merged
    
    # 添加区间
    add_interval(1, 5, "A")
    add_interval(3, 8, "B")
    add_interval(10, 15, "C")
    add_interval(12, 18, "D")
    add_interval(20, 25, "E")
    
    print("原始区间:")
    for start, data in intervals:
        print(f"  [{start}, {data['end']}) - {data['label']}")
    
    # 查找重叠
    print("\n包含点 4 的区间:")
    for start, end, label in find_overlapping(4):
        print(f"  [{start}, {end}) - {label}")
    
    print("\n包含点 13 的区间:")
    for start, end, label in find_overlapping(13):
        print(f"  [{start}, {end}) - {label}")
    
    # 合并区间
    print("\n合并后的区间:")
    for start, end, label in merge_intervals():
        print(f"  [{start}, {end})")


def lru_cache_alternative():
    """使用跳表实现 LRU 缓存的替代方案"""
    print("\n" + "=" * 60)
    print("基于跳表的有序缓存")
    print("=" * 60)
    
    class OrderedCache:
        """按访问时间排序的缓存"""
        
        def __init__(self, capacity: int = 100):
            self.capacity = capacity
            self.by_key = {}  # key -> (timestamp, value)
            self.by_time = SkipList[float]()  # timestamp -> key
            self.counter = 0  # 用于处理相同时间戳
        
        def get(self, key: str) -> tuple:
            """获取缓存项并更新访问时间"""
            if key not in self.by_key:
                return None, False
            
            old_time, value = self.by_key[key]
            self.by_time.delete(old_time)
            
            new_time = time.time() + self.counter * 1e-9
            self.counter += 1
            self.by_time.insert(new_time, key)
            self.by_key[key] = (new_time, value)
            
            return value, True
        
        def put(self, key: str, value):
            """添加缓存项"""
            if key in self.by_key:
                old_time, _ = self.by_key[key]
                self.by_time.delete(old_time)
            
            new_time = time.time() + self.counter * 1e-9
            self.counter += 1
            self.by_time.insert(new_time, key)
            self.by_key[key] = (new_time, value)
            
            # 淘汰最久未访问的项
            while len(self.by_key) > self.capacity:
                oldest_time, oldest_key = self.by_time.first()
                self.by_time.delete(oldest_time)
                del self.by_key[oldest_key]
        
        def get_lru(self):
            """获取最久未访问的项"""
            if self.by_time.is_empty:
                return None
            time_key, key = self.by_time.first()
            return key, self.by_key[key][1]
        
        def get_mru(self):
            """获取最近访问的项"""
            if self.by_time.is_empty:
                return None
            time_key, key = self.by_time.last()
            return key, self.by_key[key][1]
    
    cache = OrderedCache(capacity=3)
    
    cache.put("a", "Alice")
    cache.put("b", "Bob")
    cache.put("c", "Charlie")
    
    print("添加 a, b, c 后:")
    print(f"  LRU: {cache.get_lru()}")
    print(f"  MRU: {cache.get_mru()}")
    
    # 访问 'a'，使其变为 MRU
    cache.get("a")
    print("\n访问 'a' 后:")
    print(f"  LRU: {cache.get_lru()}")
    print(f"  MRU: {cache.get_mru()}")
    
    # 添加新项，淘汰 LRU
    cache.put("d", "Diana")
    print("\n添加 'd' 后（淘汰 LRU）:")
    print(f"  LRU: {cache.get_lru()}")
    print(f"  'b' 是否存在: {'b' in cache.by_key}")


def sorted_set_operations():
    """有序集合操作（类似 Redis Sorted Set）"""
    print("\n" + "=" * 60)
    print("有序集合操作（类似 Redis Sorted Set）")
    print("=" * 60)
    
    class SortedSet:
        """类似 Redis Sorted Set 的实现"""
        
        def __init__(self):
            self.by_score = SkipList[float]()
            self.members = {}  # member -> score
        
        def add(self, member: str, score: float) -> bool:
            """添加成员，返回是否为新成员"""
            if member in self.members:
                old_score = self.members[member]
                self.by_score.delete(old_score)
            
            # 使用复合 key 处理相同分数
            key = (score, member)
            self.by_score.insert(score, member)
            self.members[member] = score
            
            return member not in self.members
        
        def remove(self, member: str) -> bool:
            """移除成员"""
            if member not in self.members:
                return False
            
            score = self.members[member]
            self.by_score.delete(score)
            del self.members[member]
            return True
        
        def score(self, member: str) -> float:
            """获取成员分数"""
            return self.members.get(member)
        
        def rank(self, member: str) -> int:
            """获取成员排名（0 开始，分数从低到高）"""
            if member not in self.members:
                return None
            
            target_score = self.members[member]
            rank = 0
            for s, m in self.by_score:
                if m == member:
                    return rank
                rank += 1
            return None
        
        def range_by_score(self, min_score: float, max_score: float):
            """按分数范围获取成员"""
            return list(self.by_score.range(min_score, max_score))
        
        def top_n(self, n: int, descending: bool = True):
            """获取前 N 名"""
            items = list(self.by_score)
            if descending:
                items = items[::-1]
            return items[:n]
    
    ss = SortedSet()
    
    ss.add("player1", 100)
    ss.add("player2", 200)
    ss.add("player3", 150)
    ss.add("player4", 300)
    ss.add("player5", 250)
    
    print("所有成员（按分数排序）:")
    for score, member in ss.by_score:
        print(f"  {member}: {score}分")
    
    print("\n前 3 名:")
    for score, member in ss.top_n(3):
        print(f"  {member}: {score}分")
    
    print(f"\nplayer3 的排名: {ss.rank('player3')}")
    print(f"player3 的分数: {ss.score('player3')}")
    
    print("\n分数在 150-250 范围内的成员:")
    for score, member in ss.range_by_score(150, 250):
        print(f"  {member}: {score}分")


if __name__ == "__main__":
    database_index_simulation()
    leaderboard_system()
    time_window_statistics()
    interval_operations()
    lru_cache_alternative()
    sorted_set_operations()
    
    print("\n" + "=" * 60)
    print("所有高级示例运行完成！")
    print("=" * 60)