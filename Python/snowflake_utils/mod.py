"""
Snowflake ID Generator - 分布式唯一ID生成器

Snowflake ID 是 Twitter 开发的分布式唯一ID生成算法，生成64位整数ID。
特点：
- 时间有序：ID按时间递增，便于索引
- 分布式：支持多节点同时生成不冲突
- 高性能：单节点每毫秒可生成4096个ID
- 无需协调：不依赖数据库或中心化服务

ID结构（64位）:
| 1位 | 41位时间戳 | 10位机器ID | 12位序列号 |
|-----|-----------|-----------|-----------|
|  0  | 毫秒级时间 | 数据中心+工作节点 | 毫秒内序列 |

常用场景：
- 数据库主键
- 分布式系统唯一标识
- 订单号、消息ID
- 追踪ID
"""

import time
import threading
from typing import Optional, Tuple, Union
from datetime import datetime, timezone


class SnowflakeConfig:
    """Snowflake 配置类"""
    
    # 默认起始时间：2024-01-01 00:00:00 UTC
    DEFAULT_EPOCH = 1704067200000
    
    # 各部分位数
    TIMESTAMP_BITS = 41    # 时间戳位数
    DATACENTER_BITS = 5    # 数据中心ID位数
    WORKER_BITS = 5        # 工作节点ID位数
    SEQUENCE_BITS = 12      # 序列号位数
    
    # 各部分最大值
    MAX_DATACENTER_ID = (1 << DATACENTER_BITS) - 1  # 31
    MAX_WORKER_ID = (1 << WORKER_BITS) - 1           # 31
    MAX_SEQUENCE = (1 << SEQUENCE_BITS) - 1          # 4095
    
    # 位移
    WORKER_ID_SHIFT = SEQUENCE_BITS                                    # 12
    DATACENTER_ID_SHIFT = SEQUENCE_BITS + WORKER_BITS                 # 17
    TIMESTAMP_SHIFT = SEQUENCE_BITS + WORKER_BITS + DATACENTER_BITS    # 22


class SnowflakeGenerator:
    """
    Snowflake ID 生成器
    
    线程安全的分布式唯一ID生成器。
    
    示例:
        >>> generator = SnowflakeGenerator(datacenter_id=1, worker_id=1)
        >>> snowflake_id = generator.generate()
        >>> print(snowflake_id)
        1234567890123456789
    """
    
    def __init__(
        self,
        datacenter_id: int = 0,
        worker_id: int = 0,
        epoch: Optional[int] = None,
        sequence: int = 0
    ):
        """
        初始化 Snowflake 生成器
        
        参数:
            datacenter_id: 数据中心ID (0-31)
            worker_id: 工作节点ID (0-31)
            epoch: 自定义起始时间戳（毫秒），默认2024-01-01
            sequence: 初始序列号
            
        Raises:
            ValueError: 当ID超出范围时
        """
        if datacenter_id < 0 or datacenter_id > SnowflakeConfig.MAX_DATACENTER_ID:
            raise ValueError(
                f"数据中心ID必须在 0-{SnowflakeConfig.MAX_DATACENTER_ID} 之间，"
                f"当前: {datacenter_id}"
            )
        
        if worker_id < 0 or worker_id > SnowflakeConfig.MAX_WORKER_ID:
            raise ValueError(
                f"工作节点ID必须在 0-{SnowflakeConfig.MAX_WORKER_ID} 之间，"
                f"当前: {worker_id}"
            )
        
        self._datacenter_id = datacenter_id
        self._worker_id = worker_id
        self._epoch = epoch if epoch is not None else SnowflakeConfig.DEFAULT_EPOCH
        self._sequence = sequence
        self._last_timestamp = -1
        
        self._lock = threading.Lock()
    
    @property
    def datacenter_id(self) -> int:
        """获取数据中心ID"""
        return self._datacenter_id
    
    @property
    def worker_id(self) -> int:
        """获取工作节点ID"""
        return self._worker_id
    
    @property
    def epoch(self) -> int:
        """获取起始时间戳"""
        return self._epoch
    
    @property
    def epoch_datetime(self) -> datetime:
        """获取起始时间的datetime对象"""
        return datetime.fromtimestamp(self._epoch / 1000.0, tz=timezone.utc)
    
    def _current_timestamp(self) -> int:
        """获取当前时间戳（毫秒）"""
        return int(time.time() * 1000)
    
    def _wait_next_millis(self, last_timestamp: int) -> int:
        """等待到下一毫秒"""
        timestamp = self._current_timestamp()
        while timestamp <= last_timestamp:
            time.sleep(0.0001)  # 睡眠0.1毫秒
            timestamp = self._current_timestamp()
        return timestamp
    
    def generate(self) -> int:
        """
        生成下一个 Snowflake ID
        
        返回:
            int: 64位唯一ID
            
        Raises:
            RuntimeError: 系统时钟回拨时
        """
        with self._lock:
            timestamp = self._current_timestamp()
            
            # 时钟回拨检测
            if timestamp < self._last_timestamp:
                raise RuntimeError(
                    f"时钟回拨检测！当前时间戳 {timestamp} 小于上次时间戳 "
                    f"{self._last_timestamp}，差值: "
                    f"{self._last_timestamp - timestamp} 毫秒"
                )
            
            # 同一毫秒内
            if timestamp == self._last_timestamp:
                self._sequence = (self._sequence + 1) & SnowflakeConfig.MAX_SEQUENCE
                # 序列号溢出，等待下一毫秒
                if self._sequence == 0:
                    timestamp = self._wait_next_millis(self._last_timestamp)
            else:
                # 新毫秒，序列号重置
                self._sequence = 0
            
            self._last_timestamp = timestamp
            
            # 组装ID
            snowflake_id = (
                ((timestamp - self._epoch) << SnowflakeConfig.TIMESTAMP_SHIFT) |
                (self._datacenter_id << SnowflakeConfig.DATACENTER_ID_SHIFT) |
                (self._worker_id << SnowflakeConfig.WORKER_ID_SHIFT) |
                self._sequence
            )
            
            return snowflake_id
    
    def generate_batch(self, count: int) -> list:
        """
        批量生成 Snowflake ID
        
        参数:
            count: 生成数量
            
        返回:
            list: ID列表
        """
        return [self.generate() for _ in range(count)]
    
    def decompose(self, snowflake_id: int) -> dict:
        """
        解析 Snowflake ID 的组成部分
        
        参数:
            snowflake_id: Snowflake ID
            
        返回:
            dict: 包含各组成部分的字典
        """
        timestamp = (snowflake_id >> SnowflakeConfig.TIMESTAMP_SHIFT) + self._epoch
        datacenter_id = (snowflake_id >> SnowflakeConfig.DATACENTER_ID_SHIFT) & SnowflakeConfig.MAX_DATACENTER_ID
        worker_id = (snowflake_id >> SnowflakeConfig.WORKER_ID_SHIFT) & SnowflakeConfig.MAX_WORKER_ID
        sequence = snowflake_id & SnowflakeConfig.MAX_SEQUENCE
        
        return {
            'id': snowflake_id,
            'timestamp': timestamp,
            'datetime': datetime.fromtimestamp(timestamp / 1000.0, tz=timezone.utc),
            'datacenter_id': datacenter_id,
            'worker_id': worker_id,
            'sequence': sequence,
            'epoch': self._epoch
        }
    
    def extract_timestamp(self, snowflake_id: int) -> int:
        """从Snowflake ID提取时间戳（毫秒）"""
        return (snowflake_id >> SnowflakeConfig.TIMESTAMP_SHIFT) + self._epoch
    
    def extract_datetime(self, snowflake_id: int) -> datetime:
        """从Snowflake ID提取datetime对象"""
        timestamp = self.extract_timestamp(snowflake_id)
        return datetime.fromtimestamp(timestamp / 1000.0, tz=timezone.utc)
    
    def extract_datacenter_id(self, snowflake_id: int) -> int:
        """从Snowflake ID提取数据中心ID"""
        return (snowflake_id >> SnowflakeConfig.DATACENTER_ID_SHIFT) & SnowflakeConfig.MAX_DATACENTER_ID
    
    def extract_worker_id(self, snowflake_id: int) -> int:
        """从Snowflake ID提取工作节点ID"""
        return (snowflake_id >> SnowflakeConfig.WORKER_ID_SHIFT) & SnowflakeConfig.MAX_WORKER_ID
    
    def extract_sequence(self, snowflake_id: int) -> int:
        """从Snowflake ID提取序列号"""
        return snowflake_id & SnowflakeConfig.MAX_SEQUENCE
    
    def compare_ids(self, id1: int, id2: int) -> int:
        """
        比较两个Snowflake ID的时间顺序
        
        参数:
            id1, id2: Snowflake ID
            
        返回:
            int: -1 (id1 < id2), 0 (相等), 1 (id1 > id2)
        """
        if id1 < id2:
            return -1
        elif id1 > id2:
            return 1
        return 0
    
    def ids_in_range(
        self,
        start_time: Union[datetime, int],
        end_time: Union[datetime, int]
    ) -> Tuple[int, int]:
        """
        计算指定时间范围内的Snowflake ID边界
        
        参数:
            start_time: 开始时间（datetime或毫秒时间戳）
            end_time: 结束时间（datetime或毫秒时间戳）
            
        返回:
            Tuple[int, int]: (起始ID, 结束ID)
        """
        if isinstance(start_time, datetime):
            start_ms = int(start_time.timestamp() * 1000)
        else:
            start_ms = start_time
        
        if isinstance(end_time, datetime):
            end_ms = int(end_time.timestamp() * 1000)
        else:
            end_ms = end_time
        
        start_id = (start_ms - self._epoch) << SnowflakeConfig.TIMESTAMP_SHIFT
        end_id = ((end_ms - self._epoch) << SnowflakeConfig.TIMESTAMP_SHIFT) | \
                 SnowflakeConfig.MAX_SEQUENCE
        
        return (start_id, end_id)
    
    def __repr__(self) -> str:
        return (
            f"SnowflakeGenerator("
            f"datacenter_id={self._datacenter_id}, "
            f"worker_id={self._worker_id}, "
            f"epoch={self._epoch})"
        )


class DiscordSnowflake(SnowflakeGenerator):
    """
    Discord Snowflake ID 生成器
    
    Discord的Snowflake使用2015-01-01 00:00:00 UTC作为起始时间。
    Discord ID是公开的，通常以字符串形式使用。
    
    示例:
        >>> gen = DiscordSnowflake(worker_id=1)
        >>> discord_id = gen.generate()
        >>> str(discord_id)  # Discord使用字符串形式
        '1234567890123456789'
    """
    
    DISCORD_EPOCH = 1420070400000  # 2015-01-01 00:00:00 UTC
    
    def __init__(self, worker_id: int = 0, sequence: int = 0):
        """
        初始化 Discord Snowflake 生成器
        
        参数:
            worker_id: 工作节点ID (0-31)
            sequence: 初始序列号
        """
        # Discord不使用datacenter_id，将其设为0
        # worker_id左移，使用完整的10位作为worker_id
        super().__init__(
            datacenter_id=0,
            worker_id=worker_id,
            epoch=self.DISCORD_EPOCH,
            sequence=sequence
        )
    
    def generate_str(self) -> str:
        """生成字符串形式的Discord ID"""
        return str(self.generate())
    
    @classmethod
    def get_creation_time(cls, snowflake_id: Union[int, str]) -> datetime:
        """
        从Discord ID获取创建时间
        
        参数:
            snowflake_id: Discord Snowflake ID（整数或字符串）
            
        返回:
            datetime: 创建时间
        """
        if isinstance(snowflake_id, str):
            snowflake_id = int(snowflake_id)
        
        timestamp = (snowflake_id >> 22) + cls.DISCORD_EPOCH
        return datetime.fromtimestamp(timestamp / 1000.0, tz=timezone.utc)


class TwitterSnowflake(SnowflakeGenerator):
    """
    Twitter Snowflake ID 生成器
    
    Twitter原始Snowflake使用2010-11-04 01:42:54 UTC作为起始时间。
    
    示例:
        >>> gen = TwitterSnowflake(datacenter_id=1, worker_id=1)
        >>> tweet_id = gen.generate()
    """
    
    TWITTER_EPOCH = 1288834974657  # 2010-11-04 01:42:54 UTC

    def __init__(self, datacenter_id: int = 0, worker_id: int = 0, sequence: int = 0):
        """
        初始化 Twitter Snowflake 生成器
        
        参数:
            datacenter_id: 数据中心ID (0-31)
            worker_id: 工作节点ID (0-31)
            sequence: 初始序列号
        """
        super().__init__(
            datacenter_id=datacenter_id,
            worker_id=worker_id,
            epoch=self.TWITTER_EPOCH,
            sequence=sequence
        )
    
    @classmethod
    def get_creation_time(cls, snowflake_id: int) -> datetime:
        """
        从Twitter Snowflake ID获取创建时间
        
        参数:
            snowflake_id: Twitter Snowflake ID
            
        返回:
            datetime: 创建时间
        """
        timestamp = (snowflake_id >> 22) + cls.TWITTER_EPOCH
        return datetime.fromtimestamp(timestamp / 1000.0, tz=timezone.utc)


# 便捷函数
_default_generator: Optional[SnowflakeGenerator] = None


def get_default_generator() -> SnowflakeGenerator:
    """获取默认的全局生成器"""
    global _default_generator
    if _default_generator is None:
        _default_generator = SnowflakeGenerator()
    return _default_generator


def generate_id() -> int:
    """
    使用默认生成器生成Snowflake ID
    
    返回:
        int: Snowflake ID
    """
    return get_default_generator().generate()


def generate_batch(count: int) -> list:
    """
    使用默认生成器批量生成Snowflake ID
    
    参数:
        count: 生成数量
        
    返回:
        list: ID列表
    """
    return get_default_generator().generate_batch(count)


def decompose_id(snowflake_id: int, epoch: Optional[int] = None) -> dict:
    """
    解析Snowflake ID
    
    参数:
        snowflake_id: Snowflake ID
        epoch: 起始时间戳（毫秒），默认使用DEFAULT_EPOCH
        
    返回:
        dict: 包含各组成部分的字典
    """
    if epoch is None:
        epoch = SnowflakeConfig.DEFAULT_EPOCH
    
    timestamp = (snowflake_id >> SnowflakeConfig.TIMESTAMP_SHIFT) + epoch
    datacenter_id = (snowflake_id >> SnowflakeConfig.DATACENTER_ID_SHIFT) & SnowflakeConfig.MAX_DATACENTER_ID
    worker_id = (snowflake_id >> SnowflakeConfig.WORKER_ID_SHIFT) & SnowflakeConfig.MAX_WORKER_ID
    sequence = snowflake_id & SnowflakeConfig.MAX_SEQUENCE
    
    return {
        'id': snowflake_id,
        'timestamp': timestamp,
        'datetime': datetime.fromtimestamp(timestamp / 1000.0, tz=timezone.utc),
        'datacenter_id': datacenter_id,
        'worker_id': worker_id,
        'sequence': sequence,
        'epoch': epoch
    }


def extract_timestamp(snowflake_id: int, epoch: Optional[int] = None) -> int:
    """
    从Snowflake ID提取时间戳
    
    参数:
        snowflake_id: Snowflake ID
        epoch: 起始时间戳（毫秒）
        
    返回:
        int: 时间戳（毫秒）
    """
    if epoch is None:
        epoch = SnowflakeConfig.DEFAULT_EPOCH
    return (snowflake_id >> SnowflakeConfig.TIMESTAMP_SHIFT) + epoch


def extract_datetime(snowflake_id: int, epoch: Optional[int] = None) -> datetime:
    """
    从Snowflake ID提取datetime对象
    
    参数:
        snowflake_id: Snowflake ID
        epoch: 起始时间戳（毫秒）
        
    返回:
        datetime: datetime对象
    """
    timestamp = extract_timestamp(snowflake_id, epoch)
    return datetime.fromtimestamp(timestamp / 1000.0, tz=timezone.utc)


def create_generator(datacenter_id: int = 0, worker_id: int = 0, epoch: Optional[int] = None) -> SnowflakeGenerator:
    """
    创建Snowflake生成器
    
    参数:
        datacenter_id: 数据中心ID (0-31)
        worker_id: 工作节点ID (0-31)
        epoch: 自定义起始时间戳（毫秒）
        
    返回:
        SnowflakeGenerator: 生成器实例
    """
    return SnowflakeGenerator(
        datacenter_id=datacenter_id,
        worker_id=worker_id,
        epoch=epoch
    )


if __name__ == "__main__":
    # 简单演示
    print("=== Snowflake ID 生成器演示 ===\n")
    
    # 创建生成器
    gen = SnowflakeGenerator(datacenter_id=1, worker_id=1)
    print(f"生成器: {gen}\n")
    
    # 生成ID
    print("生成5个ID:")
    for i in range(5):
        sid = gen.generate()
        info = gen.decompose(sid)
        print(f"  {i+1}. ID: {sid}")
        print(f"     时间: {info['datetime']}")
        print(f"     数据中心: {info['datacenter_id']}, 节点: {info['worker_id']}, 序列: {info['sequence']}")
    
    print("\n=== 使用便捷函数 ===")
    sid = generate_id()
    print(f"生成的ID: {sid}")
    print(f"解析结果: {decompose_id(sid)}")
    
    print("\n=== Discord Snowflake ===")
    discord_gen = DiscordSnowflake(worker_id=1)
    discord_id = discord_gen.generate()
    print(f"Discord ID: {discord_id}")
    print(f"创建时间: {DiscordSnowflake.get_creation_time(discord_id)}")
    
    print("\n=== Twitter Snowflake ===")
    twitter_gen = TwitterSnowflake(datacenter_id=1, worker_id=1)
    twitter_id = twitter_gen.generate()
    print(f"Twitter ID: {twitter_id}")
    print(f"创建时间: {TwitterSnowflake.get_creation_time(twitter_id)}")