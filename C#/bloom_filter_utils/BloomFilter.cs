using System;
using System.Collections;
using System.Security.Cryptography;
using System.Text;

namespace AllToolkit.BloomFilter
{
    /// <summary>
    /// 布隆过滤器 - 空间高效的概率型数据结构
    /// 用于快速判断一个元素是否"可能存在"或"绝对不存在"于集合中
    /// 零依赖，仅使用 .NET 标准库
    /// </summary>
    public class BloomFilter<T> : ICloneable
    {
        private readonly BitArray _bits;
        private readonly int _hashFunctions;
        private readonly int _seed;
        private int _count;

        /// <summary>
        /// 预期的元素数量
        /// </summary>
        public int ExpectedItems { get; }

        /// <summary>
        /// 位数组大小
        /// </summary>
        public int BitSize { get; }

        /// <summary>
        /// 哈希函数数量
        /// </summary>
        public int HashFunctionCount => _hashFunctions;

        /// <summary>
        /// 当前已添加元素数量
        /// </summary>
        public int Count => _count;

        /// <summary>
        /// 位数组中设置为 1 的位数
        /// </summary>
        public int BitsSet
        {
            get
            {
                int count = 0;
                for (int i = 0; i < _bits.Length; i++)
                {
                    if (_bits[i]) count++;
                }
                return count;
            }
        }

        /// <summary>
        /// 当前估计的假阳性概率
        /// </summary>
        public double EstimatedFalsePositiveProbability
        {
            get
            {
                if (_count == 0) return 0.0;
                double ratio = (double)BitsSet / BitSize;
                return Math.Pow(ratio, _hashFunctions);
            }
        }

        /// <summary>
        /// 创建布隆过滤器
        /// </summary>
        /// <param name="expectedItems">预期存储的元素数量</param>
        /// <param name="falsePositiveProbability">可接受的假阳性概率 (默认 0.01)</param>
        /// <param name="seed">哈希种子值</param>
        public BloomFilter(int expectedItems, double falsePositiveProbability = 0.01, int seed = 0)
        {
            if (expectedItems <= 0)
                throw new ArgumentException("Expected items must be positive", nameof(expectedItems));
            if (falsePositiveProbability <= 0 || falsePositiveProbability >= 1)
                throw new ArgumentException("False positive probability must be between 0 and 1", nameof(falsePositiveProbability));

            ExpectedItems = expectedItems;
            BitSize = OptimalBitSize(expectedItems, falsePositiveProbability);
            _hashFunctions = OptimalHashFunctionCount(BitSize, expectedItems);
            _bits = new BitArray(BitSize);
            _seed = seed;
            _count = 0;
        }

        /// <summary>
        /// 私有构造函数，用于克隆
        /// </summary>
        private BloomFilter(int expectedItems, int bitSize, int hashFunctions, int seed, BitArray bits, int count)
        {
            ExpectedItems = expectedItems;
            BitSize = bitSize;
            _hashFunctions = hashFunctions;
            _seed = seed;
            _bits = new BitArray(bits);
            _count = count;
        }

        /// <summary>
        /// 计算最优位数组大小
        /// </summary>
        public static int OptimalBitSize(int n, double p)
        {
            // m = -n * ln(p) / (ln(2)^2)
            return (int)Math.Ceiling(-n * Math.Log(p) / (Math.Log(2) * Math.Log(2)));
        }

        /// <summary>
        /// 计算最优哈希函数数量
        /// </summary>
        public static int OptimalHashFunctionCount(int m, int n)
        {
            // k = (m/n) * ln(2)
            return Math.Max(1, (int)Math.Round((double)m / n * Math.Log(2)));
        }

        /// <summary>
        /// 添加元素到布隆过滤器
        /// </summary>
        public void Add(T item)
        {
            if (item == null)
                throw new ArgumentNullException(nameof(item));

            byte[] bytes = GetBytes(item);
            int[] hashes = ComputeHashes(bytes);

            for (int i = 0; i < _hashFunctions; i++)
            {
                _bits[hashes[i] % BitSize] = true;
            }
            _count++;
        }

        /// <summary>
        /// 批量添加元素
        /// </summary>
        public void AddRange(IEnumerable<T> items)
        {
            if (items == null)
                throw new ArgumentNullException(nameof(items));

            foreach (var item in items)
            {
                Add(item);
            }
        }

        /// <summary>
        /// 检查元素是否可能存在
        /// </summary>
        /// <returns>
        /// true: 元素可能存在（有假阳性可能）
        /// false: 元素绝对不存在
        /// </returns>
        public bool MightContain(T item)
        {
            if (item == null)
                return false;

            byte[] bytes = GetBytes(item);
            int[] hashes = ComputeHashes(bytes);

            for (int i = 0; i < _hashFunctions; i++)
            {
                if (!_bits[hashes[i] % BitSize])
                    return false;
            }
            return true;
        }

        /// <summary>
        /// Contains 的别名，与 HashSet 接口一致
        /// </summary>
        public bool Contains(T item) => MightContain(item);

        /// <summary>
        /// 清空布隆过滤器
        /// </summary>
        public void Clear()
        {
            _bits.SetAll(false);
            _count = 0;
        }

        /// <summary>
        /// 合并另一个布隆过滤器
        /// 注意：两个过滤器必须具有相同的配置
        /// </summary>
        public void UnionWith(BloomFilter<T> other)
        {
            if (other == null)
                throw new ArgumentNullException(nameof(other));
            if (other.BitSize != this.BitSize || other._hashFunctions != this._hashFunctions)
                throw new ArgumentException("Cannot union bloom filters with different configurations", nameof(other));

            for (int i = 0; i < BitSize; i++)
            {
                _bits[i] = _bits[i] || other._bits[i];
            }
            _count = -1; // Count is no longer accurate after union
        }

        /// <summary>
        /// 计算两个布隆过滤器的交集
        /// 注意：两个过滤器必须具有相同的配置
        /// </summary>
        public void IntersectWith(BloomFilter<T> other)
        {
            if (other == null)
                throw new ArgumentNullException(nameof(other));
            if (other.BitSize != this.BitSize || other._hashFunctions != this._hashFunctions)
                throw new ArgumentException("Cannot intersect bloom filters with different configurations", nameof(other));

            for (int i = 0; i < BitSize; i++)
            {
                _bits[i] = _bits[i] && other._bits[i];
            }
            _count = -1; // Count is no longer accurate after intersection
        }

        /// <summary>
        /// 克隆当前布隆过滤器
        /// </summary>
        public object Clone()
        {
            return new BloomFilter<T>(ExpectedItems, BitSize, _hashFunctions, _seed, _bits, _count);
        }

        /// <summary>
        /// 获取底层数据的字节表示
        /// </summary>
        public byte[] ToByteArray()
        {
            byte[] result = new byte[(BitSize + 7) / 8];
            _bits.CopyTo(result, 0);
            return result;
        }

        /// <summary>
        /// 从字节数组恢复布隆过滤器状态
        /// </summary>
        public static BloomFilter<T> FromByteArray(byte[] data, int expectedItems, double falsePositiveProbability, int seed = 0)
        {
            if (data == null || data.Length == 0)
                throw new ArgumentException("Data cannot be null or empty", nameof(data));

            var filter = new BloomFilter<T>(expectedItems, falsePositiveProbability, seed);
            var bits = new BitArray(data);
            
            int copyLength = Math.Min(bits.Length, filter.BitSize);
            for (int i = 0; i < copyLength; i++)
            {
                filter._bits[i] = bits[i];
            }
            
            return filter;
        }

        /// <summary>
        /// 计算序列化后的大约大小（字节）
        /// </summary>
        public int GetSerializedSize()
        {
            return (BitSize + 7) / 8;
        }

        /// <summary>
        /// 获取统计信息
        /// </summary>
        public BloomFilterStats GetStats()
        {
            return new BloomFilterStats
            {
                ExpectedItems = ExpectedItems,
                BitSize = BitSize,
                HashFunctionCount = _hashFunctions,
                ItemsAdded = _count,
                BitsSet = BitsSet,
                FillRatio = (double)BitsSet / BitSize,
                EstimatedFalsePositiveProbability = EstimatedFalsePositiveProbability
            };
        }

        #region 私有方法

        private byte[] GetBytes(T item)
        {
            if (item is string s)
            {
                return Encoding.UTF8.GetBytes(s);
            }
            else if (item is byte[] bytes)
            {
                return bytes;
            }
            else if (item is int i)
            {
                return BitConverter.GetBytes(i);
            }
            else if (item is long l)
            {
                return BitConverter.GetBytes(l);
            }
            else if (item is double d)
            {
                return BitConverter.GetBytes(d);
            }
            else if (item is float f)
            {
                return BitConverter.GetBytes(f);
            }
            else if (item is Guid g)
            {
                return g.ToByteArray();
            }
            else
            {
                // 默认使用 ToString() 并转为字节
                return Encoding.UTF8.GetBytes(item?.ToString() ?? string.Empty);
            }
        }

        private int[] ComputeHashes(byte[] data)
        {
            int[] hashes = new int[_hashFunctions];

            // 使用 HMAC-SHA256 生成多个哈希值
            using (var hmac = new HMACSHA256(BitConverter.GetBytes(_seed)))
            {
                byte[] hash1 = hmac.ComputeHash(data);

                // 使用双重哈希技术生成多个哈希值
                // h(i) = hash1 + i * hash2
                int h1 = BitConverter.ToInt32(hash1, 0);
                int h2 = BitConverter.ToInt32(hash1, 4);

                for (int i = 0; i < _hashFunctions; i++)
                {
                    hashes[i] = Math.Abs(h1 + i * h2);
                }
            }

            return hashes;
        }

        #endregion
    }

    /// <summary>
    /// 布隆过滤器统计信息
    /// </summary>
    public class BloomFilterStats
    {
        public int ExpectedItems { get; set; }
        public int BitSize { get; set; }
        public int HashFunctionCount { get; set; }
        public int ItemsAdded { get; set; }
        public int BitsSet { get; set; }
        public double FillRatio { get; set; }
        public double EstimatedFalsePositiveProbability { get; set; }

        public override string ToString()
        {
            return $"BloomFilter[Bits={BitSize}, Hashes={HashFunctionCount}, Items={ItemsAdded}, " +
                   $"Fill={FillRatio:P2}, Est.FalsePositive={EstimatedFalsePositiveProbability:P4}]";
        }
    }

    /// <summary>
    /// 可缩放布隆过滤器 - 自动调整大小以维持假阳性概率
    /// </summary>
    public class ScalableBloomFilter<T>
    {
        private readonly List<BloomFilter<T>> _filters;
        private readonly double _initialFalsePositiveProbability;
        private readonly double _growthFactor;
        private readonly int _seed;
        private int _currentScale;
        private long _totalCount;

        /// <summary>
        /// 创建可缩放布隆过滤器
        /// </summary>
        /// <param name="initialExpectedItems">初始预期元素数量</param>
        /// <param name="falsePositiveProbability">可接受的假阳性概率</param>
        /// <param name="growthFactor">增长因子</param>
        /// <param name="seed">哈希种子</param>
        public ScalableBloomFilter(int initialExpectedItems = 1000, 
            double falsePositiveProbability = 0.01, 
            double growthFactor = 2.0, 
            int seed = 0)
        {
            if (initialExpectedItems <= 0)
                throw new ArgumentException("Initial expected items must be positive", nameof(initialExpectedItems));

            _initialFalsePositiveProbability = falsePositiveProbability;
            _growthFactor = growthFactor;
            _seed = seed;
            _filters = new List<BloomFilter<T>>();
            _currentScale = 0;
            _totalCount = 0;

            AddNewFilter(initialExpectedItems);
        }

        /// <summary>
        /// 当前已添加的元素总数
        /// </summary>
        public long Count => _totalCount;

        /// <summary>
        /// 当前过滤器层数
        /// </summary>
        public int FilterCount => _filters.Count;

        /// <summary>
        /// 添加新元素
        /// </summary>
        public void Add(T item)
        {
            // 检查当前过滤器是否已接近容量
            var currentFilter = _filters[_currentScale];
            
            if (currentFilter.Count >= currentFilter.ExpectedItems)
            {
                // 需要添加新的过滤器
                _currentScale++;
                int newExpectedItems = (int)(currentFilter.ExpectedItems * _growthFactor);
                AddNewFilter(newExpectedItems);
            }

            _filters[_currentScale].Add(item);
            _totalCount++;
        }

        /// <summary>
        /// 批量添加元素
        /// </summary>
        public void AddRange(IEnumerable<T> items)
        {
            foreach (var item in items)
            {
                Add(item);
            }
        }

        /// <summary>
        /// 检查元素是否可能存在
        /// </summary>
        public bool MightContain(T item)
        {
            foreach (var filter in _filters)
            {
                if (filter.MightContain(item))
                    return true;
            }
            return false;
        }

        /// <summary>
        /// Contains 的别名
        /// </summary>
        public bool Contains(T item) => MightContain(item);

        /// <summary>
        /// 获取所有过滤器的统计信息
        /// </summary>
        public List<BloomFilterStats> GetAllStats()
        {
            return _filters.Select(f => f.GetStats()).ToList();
        }

        private void AddNewFilter(int expectedItems)
        {
            // 每层的假阳性概率更严格
            double fp = _initialFalsePositiveProbability / Math.Pow(2, _filters.Count + 1);
            _filters.Add(new BloomFilter<T>(expectedItems, fp, _seed + _filters.Count));
        }
    }

    /// <summary>
    /// 计数布隆过滤器 - 支持删除操作
    /// </summary>
    public class CountingBloomFilter<T>
    {
        private readonly int[] _counters;
        private readonly int _hashFunctions;
        private readonly int _maxCounter;
        private readonly int _seed;
        private int _count;

        public int ExpectedItems { get; }
        public int BitSize { get; }
        public int HashFunctionCount => _hashFunctions;
        public int Count => _count;

        /// <summary>
        /// 创建计数布隆过滤器
        /// </summary>
        /// <param name="expectedItems">预期元素数量</param>
        /// <param name="falsePositiveProbability">假阳性概率</param>
        /// <param name="bitsPerCounter">每个计数器的位数 (默认4位，最大值15)</param>
        /// <param name="seed">哈希种子</param>
        public CountingBloomFilter(int expectedItems, double falsePositiveProbability = 0.01, 
            int bitsPerCounter = 4, int seed = 0)
        {
            if (expectedItems <= 0)
                throw new ArgumentException("Expected items must be positive", nameof(expectedItems));

            ExpectedItems = expectedItems;
            BitSize = BloomFilter<T>.OptimalBitSize(expectedItems, falsePositiveProbability);
            _hashFunctions = BloomFilter<T>.OptimalHashFunctionCount(BitSize, expectedItems);
            _counters = new int[BitSize];
            _maxCounter = (1 << bitsPerCounter) - 1;
            _seed = seed;
            _count = 0;
        }

        /// <summary>
        /// 添加元素
        /// </summary>
        public bool Add(T item)
        {
            if (item == null)
                throw new ArgumentNullException(nameof(item));

            byte[] bytes = GetBytes(item);
            int[] hashes = ComputeHashes(bytes);

            bool overflow = false;
            for (int i = 0; i < _hashFunctions; i++)
            {
                int index = hashes[i] % BitSize;
                if (_counters[index] < _maxCounter)
                {
                    _counters[index]++;
                }
                else
                {
                    overflow = true;
                }
            }
            _count++;
            return !overflow;
        }

        /// <summary>
        /// 移除元素
        /// </summary>
        public bool Remove(T item)
        {
            if (item == null)
                return false;

            if (!MightContain(item))
                return false;

            byte[] bytes = GetBytes(item);
            int[] hashes = ComputeHashes(bytes);

            for (int i = 0; i < _hashFunctions; i++)
            {
                int index = hashes[i] % BitSize;
                if (_counters[index] > 0)
                {
                    _counters[index]--;
                }
            }
            _count--;
            return true;
        }

        /// <summary>
        /// 检查元素是否可能存在
        /// </summary>
        public bool MightContain(T item)
        {
            if (item == null)
                return false;

            byte[] bytes = GetBytes(item);
            int[] hashes = ComputeHashes(bytes);

            for (int i = 0; i < _hashFunctions; i++)
            {
                if (_counters[hashes[i] % BitSize] == 0)
                    return false;
            }
            return true;
        }

        public bool Contains(T item) => MightContain(item);

        /// <summary>
        /// 清空过滤器
        /// </summary>
        public void Clear()
        {
            Array.Clear(_counters, 0, _counters.Length);
            _count = 0;
        }

        /// <summary>
        /// 获取估计的假阳性概率
        /// </summary>
        public double EstimatedFalsePositiveProbability
        {
            get
            {
                if (_count == 0) return 0.0;
                
                int nonZeroCount = _counters.Count(c => c > 0);
                double ratio = (double)nonZeroCount / BitSize;
                return Math.Pow(ratio, _hashFunctions);
            }
        }

        private byte[] GetBytes(T item)
        {
            if (item is string s) return System.Text.Encoding.UTF8.GetBytes(s);
            if (item is byte[] bytes) return bytes;
            if (item is int i) return BitConverter.GetBytes(i);
            if (item is long l) return BitConverter.GetBytes(l);
            return System.Text.Encoding.UTF8.GetBytes(item?.ToString() ?? string.Empty);
        }

        private int[] ComputeHashes(byte[] data)
        {
            int[] hashes = new int[_hashFunctions];
            using (var hmac = new HMACSHA256(BitConverter.GetBytes(_seed)))
            {
                byte[] hash = hmac.ComputeHash(data);
                int h1 = BitConverter.ToInt32(hash, 0);
                int h2 = BitConverter.ToInt32(hash, 4);

                for (int i = 0; i < _hashFunctions; i++)
                {
                    hashes[i] = Math.Abs(h1 + i * h2);
                }
            }
            return hashes;
        }
    }
}