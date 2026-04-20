using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading;

namespace AllToolkit.TrieUtils
{
    /// <summary>
    /// Trie (前缀树) 工具类 - 高效的前缀匹配数据结构
    /// 零依赖，仅使用 .NET 标准库
    /// 
    /// 适用场景：
    /// - 自动补全
    /// - 拼写检查
    /// - 字典查找
    /// - IP 路由表
    /// - 单词游戏
    /// </summary>
    public class TrieNode
    {
        /// <summary>
        /// 子节点字典，键为字符，值为子节点
        /// </summary>
        public Dictionary<char, TrieNode> Children { get; } = new Dictionary<char, TrieNode>();

        /// <summary>
        /// 标记是否为单词结尾
        /// </summary>
        public bool IsEnd { get; set; }

        /// <summary>
        /// 存储的值（可选）
        /// </summary>
        public object Value { get; set; }

        /// <summary>
        /// 单词频率/计数
        /// </summary>
        public int Count { get; set; }
    }

    /// <summary>
    /// 单词频率记录
    /// </summary>
    public class WordFrequency
    {
        public string Word { get; set; }
        public int Count { get; set; }
    }

    /// <summary>
    /// Trie 前缀树实现
    /// 支持插入、搜索、删除、前缀匹配、模式匹配等功能
    /// 线程安全
    /// </summary>
    public class Trie : IDisposable
    {
        private readonly TrieNode _root;
        private int _size;
        private readonly ReaderWriterLockSlim _lock = new ReaderWriterLockSlim();
        private bool _disposed = false;

        /// <summary>
        /// 创建新的 Trie 实例
        /// </summary>
        public Trie()
        {
            _root = new TrieNode();
            _size = 0;
        }

        /// <summary>
        /// Trie 中单词的数量
        /// </summary>
        public int Size
        {
            get
            {
                _lock.EnterReadLock();
                try
                {
                    return _size;
                }
                finally
                {
                    _lock.ExitReadLock();
                }
            }
        }

        /// <summary>
        /// Trie 是否为空
        /// </summary>
        public bool IsEmpty
        {
            get
            {
                _lock.EnterReadLock();
                try
                {
                    return _size == 0;
                }
                finally
                {
                    _lock.ExitReadLock();
                }
            }
        }

        #region 插入操作

        /// <summary>
        /// 插入单词（不带值）
        /// </summary>
        /// <param name="word">要插入的单词</param>
        /// <returns>如果是新单词返回 true，已存在返回 false</returns>
        public bool Insert(string word)
        {
            return Insert(word, null);
        }

        /// <summary>
        /// 插入单词（带值）
        /// </summary>
        /// <param name="word">要插入的单词</param>
        /// <param name="value">关联的值</param>
        /// <returns>如果是新单词返回 true，已存在返回 false</returns>
        public bool Insert(string word, object value)
        {
            if (string.IsNullOrEmpty(word))
                return false;

            _lock.EnterWriteLock();
            try
            {
                var node = _root;
                foreach (var ch in word)
                {
                    if (!node.Children.ContainsKey(ch))
                    {
                        node.Children[ch] = new TrieNode();
                    }
                    node = node.Children[ch];
                }

                var isNew = !node.IsEnd;
                if (isNew)
                {
                    _size++;
                }
                node.IsEnd = true;
                node.Value = value;
                node.Count++;
                return isNew;
            }
            finally
            {
                _lock.ExitWriteLock();
            }
        }

        /// <summary>
        /// 批量插入单词
        /// </summary>
        /// <param name="words">单词列表</param>
        /// <returns>成功插入的新单词数量</returns>
        public int BatchInsert(IEnumerable<string> words)
        {
            int count = 0;
            foreach (var word in words)
            {
                if (Insert(word))
                    count++;
            }
            return count;
        }

        /// <summary>
        /// 批量插入带值的单词
        /// </summary>
        /// <param name="pairs">单词-值字典</param>
        /// <returns>成功插入的新单词数量</returns>
        public int BatchInsertWithValues(IDictionary<string, object> pairs)
        {
            int count = 0;
            foreach (var pair in pairs)
            {
                if (Insert(pair.Key, pair.Value))
                    count++;
            }
            return count;
        }

        #endregion

        #region 搜索操作

        /// <summary>
        /// 搜索单词是否存在
        /// </summary>
        /// <param name="word">要搜索的单词</param>
        /// <returns>存在返回 true</returns>
        public bool Search(string word)
        {
            _lock.EnterReadLock();
            try
            {
                var node = FindNode(word);
                return node != null && node.IsEnd;
            }
            finally
            {
                _lock.ExitReadLock();
            }
        }

        /// <summary>
        /// 搜索单词并返回关联的值
        /// </summary>
        /// <param name="word">要搜索的单词</param>
        /// <param name="value">输出的值</param>
        /// <returns>找到返回 true</returns>
        public bool SearchWithValue(string word, out object value)
        {
            value = null;
            _lock.EnterReadLock();
            try
            {
                var node = FindNode(word);
                if (node != null && node.IsEnd)
                {
                    value = node.Value;
                    return true;
                }
                return false;
            }
            finally
            {
                _lock.ExitReadLock();
            }
        }

        /// <summary>
        /// 搜索单词并返回关联的值（泛型版本）
        /// </summary>
        /// <typeparam name="T">值类型</typeparam>
        /// <param name="word">要搜索的单词</param>
        /// <param name="value">输出的值</param>
        /// <returns>找到返回 true</returns>
        public bool SearchWithValue<T>(string word, out T value)
        {
            value = default;
            _lock.EnterReadLock();
            try
            {
                var node = FindNode(word);
                if (node != null && node.IsEnd && node.Value is T typedValue)
                {
                    value = typedValue;
                    return true;
                }
                return false;
            }
            finally
            {
                _lock.ExitReadLock();
            }
        }

        /// <summary>
        /// 获取单词的频率/计数
        /// </summary>
        /// <param name="word">单词</param>
        /// <returns>频率计数</returns>
        public int GetCount(string word)
        {
            _lock.EnterReadLock();
            try
            {
                var node = FindNode(word);
                return node != null && node.IsEnd ? node.Count : 0;
            }
            finally
            {
                _lock.ExitReadLock();
            }
        }

        /// <summary>
        /// 检查是否存在以指定前缀开头的单词
        /// </summary>
        /// <param name="prefix">前缀</param>
        /// <returns>存在返回 true</returns>
        public bool StartsWith(string prefix)
        {
            _lock.EnterReadLock();
            try
            {
                return FindNode(prefix) != null;
            }
            finally
            {
                _lock.ExitReadLock();
            }
        }

        #endregion

        #region 删除操作

        /// <summary>
        /// 删除单词
        /// </summary>
        /// <param name="word">要删除的单词</param>
        /// <returns>成功删除返回 true</returns>
        public bool Delete(string word)
        {
            if (string.IsNullOrEmpty(word))
                return false;

            _lock.EnterWriteLock();
            try
            {
                var path = new List<TrieNode> { _root };
                var chars = new List<char>();

                var node = _root;
                foreach (var ch in word)
                {
                    if (!node.Children.ContainsKey(ch))
                        return false;
                    chars.Add(ch);
                    node = node.Children[ch];
                    path.Add(node);
                }

                if (!node.IsEnd)
                    return false;

                node.IsEnd = false;
                node.Value = null;
                node.Count = 0;
                _size--;

                // 清理无用节点
                for (int i = path.Count - 1; i > 0; i--)
                {
                    var currentNode = path[i];
                    if (currentNode.IsEnd || currentNode.Children.Count > 0)
                        break;
                    var parentNode = path[i - 1];
                    parentNode.Children.Remove(chars[i - 1]);
                }

                return true;
            }
            finally
            {
                _lock.ExitWriteLock();
            }
        }

        /// <summary>
        /// 清空 Trie
        /// </summary>
        public void Clear()
        {
            _lock.EnterWriteLock();
            try
            {
                _root.Children.Clear();
                _size = 0;
            }
            finally
            {
                _lock.ExitWriteLock();
            }
        }

        #endregion

        #region 前缀搜索

        /// <summary>
        /// 获取所有以指定前缀开头的单词
        /// </summary>
        /// <param name="prefix">前缀</param>
        /// <returns>单词列表</returns>
        public List<string> WordsWithPrefix(string prefix)
        {
            _lock.EnterReadLock();
            try
            {
                var results = new List<string>();
                var startNode = FindNode(prefix);
                if (startNode == null)
                    return results;

                CollectWords(startNode, prefix, results);
                return results;
            }
            finally
            {
                _lock.ExitReadLock();
            }
        }

        /// <summary>
        /// 获取指定数量的前缀匹配单词
        /// </summary>
        /// <param name="prefix">前缀</param>
        /// <param name="limit">最大数量</param>
        /// <returns>单词列表</returns>
        public List<string> WordsWithPrefixLimit(string prefix, int limit)
        {
            _lock.EnterReadLock();
            try
            {
                var results = new List<string>();
                var startNode = FindNode(prefix);
                if (startNode == null)
                    return results;

                CollectWordsLimit(startNode, prefix, results, limit);
                return results;
            }
            finally
            {
                _lock.ExitReadLock();
            }
        }

        /// <summary>
        /// 自动补全
        /// </summary>
        /// <param name="prefix">前缀</param>
        /// <param name="limit">最大建议数量</param>
        /// <returns>补全建议列表</returns>
        public List<string> AutoComplete(string prefix, int limit = 10)
        {
            if (limit <= 0)
                limit = 10;
            return WordsWithPrefixLimit(prefix, limit);
        }

        /// <summary>
        /// 获取所有单词
        /// </summary>
        /// <returns>所有单词列表</returns>
        public List<string> AllWords()
        {
            _lock.EnterReadLock();
            try
            {
                var results = new List<string>();
                CollectWords(_root, "", results);
                return results;
            }
            finally
            {
                _lock.ExitReadLock();
            }
        }

        /// <summary>
        /// 按频率排序获取所有单词
        /// </summary>
        /// <returns>单词频率列表（降序）</returns>
        public List<WordFrequency> GetWordsByFrequency()
        {
            _lock.EnterReadLock();
            try
            {
                var wf = new List<WordFrequency>();
                CollectWordsWithFrequency(_root, "", wf);
                return wf.OrderByDescending(w => w.Count).ToList();
            }
            finally
            {
                _lock.ExitReadLock();
            }
        }

        #endregion

        #region 高级功能

        /// <summary>
        /// 获取最长公共前缀
        /// </summary>
        /// <returns>最长公共前缀</returns>
        public string LongestCommonPrefix()
        {
            _lock.EnterReadLock();
            try
            {
                if (_size == 0)
                    return "";

                var prefix = new List<char>();
                var node = _root;

                while (node.Children.Count == 1 && !node.IsEnd)
                {
                    var kvp = node.Children.First();
                    prefix.Add(kvp.Key);
                    node = kvp.Value;
                }

                return new string(prefix.ToArray());
            }
            finally
            {
                _lock.ExitReadLock();
            }
        }

        /// <summary>
        /// 获取单词的最短唯一前缀
        /// </summary>
        /// <param name="word">单词</param>
        /// <returns>最短唯一前缀</returns>
        public string MinPrefix(string word)
        {
            _lock.EnterReadLock();
            try
            {
                var node = _root;
                for (int i = 0; i < word.Length; i++)
                {
                    var ch = word[i];
                    if (node.Children.Count > 1 || node.IsEnd)
                        return word.Substring(0, i + 1);
                    if (!node.Children.ContainsKey(ch))
                        return word;
                    node = node.Children[ch];
                }
                return word;
            }
            finally
            {
                _lock.ExitReadLock();
            }
        }

        /// <summary>
        /// 检查 Trie 中是否有单词是指定字符串的前缀
        /// </summary>
        /// <param name="s">字符串</param>
        /// <returns>存在返回 true</returns>
        public bool ContainsAnyPrefixOf(string s)
        {
            if (string.IsNullOrEmpty(s))
                return false;

            _lock.EnterReadLock();
            try
            {
                var node = _root;
                foreach (var ch in s)
                {
                    if (node.IsEnd)
                        return true;
                    if (!node.Children.ContainsKey(ch))
                        return false;
                    node = node.Children[ch];
                }
                return node.IsEnd;
            }
            finally
            {
                _lock.ExitReadLock();
            }
        }

        /// <summary>
        /// 获取 Trie 中是指定字符串前缀的最长单词
        /// </summary>
        /// <param name="s">字符串</param>
        /// <returns>最长前缀单词</returns>
        public string LongestPrefixOf(string s)
        {
            if (string.IsNullOrEmpty(s))
                return "";

            _lock.EnterReadLock();
            try
            {
                string longest = "";
                var node = _root;

                for (int i = 0; i < s.Length; i++)
                {
                    var ch = s[i];
                    if (!node.Children.ContainsKey(ch))
                        break;
                    node = node.Children[ch];
                    if (node.IsEnd)
                        longest = s.Substring(0, i + 1);
                }

                return longest;
            }
            finally
            {
                _lock.ExitReadLock();
            }
        }

        /// <summary>
        /// 模式匹配（支持通配符）
        /// ? 匹配任意单个字符
        /// * 匹配零个或多个字符
        /// </summary>
        /// <param name="pattern">模式</param>
        /// <returns>匹配的单词列表</returns>
        public List<string> PatternMatch(string pattern)
        {
            _lock.EnterReadLock();
            try
            {
                var results = new List<string>();
                MatchPattern(_root, "", pattern, results);
                return results;
            }
            finally
            {
                _lock.ExitReadLock();
            }
        }

        /// <summary>
        /// 将 Trie 转换为字典
        /// </summary>
        /// <returns>单词-值字典</returns>
        public Dictionary<string, object> ToMap()
        {
            _lock.EnterReadLock();
            try
            {
                var result = new Dictionary<string, object>();
                CollectWordsToMap(_root, "", result);
                return result;
            }
            finally
            {
                _lock.ExitReadLock();
            }
        }

        /// <summary>
        /// 将 Trie 转换为字典（泛型版本）
        /// </summary>
        /// <typeparam name="T">值类型</typeparam>
        /// <returns>单词-值字典</returns>
        public Dictionary<string, T> ToMap<T>()
        {
            _lock.EnterReadLock();
            try
            {
                var result = new Dictionary<string, T>();
                CollectWordsToMap(_root, "", result);
                return result;
            }
            finally
            {
                _lock.ExitReadLock();
            }
        }

        #endregion

        #region 辅助方法

        private TrieNode FindNode(string prefix)
        {
            var node = _root;
            foreach (var ch in prefix)
            {
                if (!node.Children.ContainsKey(ch))
                    return null;
                node = node.Children[ch];
            }
            return node;
        }

        private void CollectWords(TrieNode node, string prefix, List<string> results)
        {
            if (node.IsEnd)
                results.Add(prefix);
            foreach (var kvp in node.Children.OrderBy(k => k.Key))
            {
                CollectWords(kvp.Value, prefix + kvp.Key, results);
            }
        }

        private void CollectWordsLimit(TrieNode node, string prefix, List<string> results, int limit)
        {
            if (results.Count >= limit)
                return;
            if (node.IsEnd)
                results.Add(prefix);
            foreach (var kvp in node.Children.OrderBy(k => k.Key))
            {
                if (results.Count >= limit)
                    return;
                CollectWordsLimit(kvp.Value, prefix + kvp.Key, results, limit);
            }
        }

        private void CollectWordsWithFrequency(TrieNode node, string prefix, List<WordFrequency> wf)
        {
            if (node.IsEnd)
                wf.Add(new WordFrequency { Word = prefix, Count = node.Count });
            foreach (var kvp in node.Children)
            {
                CollectWordsWithFrequency(kvp.Value, prefix + kvp.Key, wf);
            }
        }

        private void CollectWordsToMap(TrieNode node, string prefix, Dictionary<string, object> result)
        {
            if (node.IsEnd)
                result[prefix] = node.Value;
            foreach (var kvp in node.Children)
            {
                CollectWordsToMap(kvp.Value, prefix + kvp.Key, result);
            }
        }

        private void CollectWordsToMap<T>(TrieNode node, string prefix, Dictionary<string, T> result)
        {
            if (node.IsEnd && node.Value is T typedValue)
                result[prefix] = typedValue;
            foreach (var kvp in node.Children)
            {
                CollectWordsToMap(kvp.Value, prefix + kvp.Key, result);
            }
        }

        private void MatchPattern(TrieNode node, string current, string pattern, List<string> results)
        {
            if (pattern.Length == 0)
            {
                if (node.IsEnd)
                    results.Add(current);
                return;
            }

            var ch = pattern[0];
            var remaining = pattern.Substring(1);

            switch (ch)
            {
                case '?':
                    // 匹配任意单个字符
                    foreach (var kvp in node.Children)
                    {
                        MatchPattern(kvp.Value, current + kvp.Key, remaining, results);
                    }
                    break;
                case '*':
                    // 匹配零个字符
                    MatchPattern(node, current, remaining, results);
                    // 匹配一个或多个字符
                    foreach (var kvp in node.Children)
                    {
                        MatchPattern(kvp.Value, current + kvp.Key, pattern, results);
                    }
                    break;
                default:
                    if (node.Children.ContainsKey(ch))
                    {
                        MatchPattern(node.Children[ch], current + ch, remaining, results);
                    }
                    break;
            }
        }

        #endregion

        #region IDisposable

        public void Dispose()
        {
            Dispose(true);
            GC.SuppressFinalize(this);
        }

        protected virtual void Dispose(bool disposing)
        {
            if (!_disposed)
            {
                if (disposing)
                {
                    _lock?.Dispose();
                }
                _disposed = true;
            }
        }

        ~Trie()
        {
            Dispose(false);
        }

        #endregion
    }

    /// <summary>
    /// 泛型 Trie 实现
    /// </summary>
    /// <typeparam name="T">值类型</typeparam>
    public class Trie<T> : IDisposable
    {
        private readonly TrieNode<T> _root;
        private int _size;
        private readonly ReaderWriterLockSlim _lock = new ReaderWriterLockSlim();
        private bool _disposed = false;

        public Trie()
        {
            _root = new TrieNode<T>();
            _size = 0;
        }

        public int Size
        {
            get
            {
                _lock.EnterReadLock();
                try { return _size; }
                finally { _lock.ExitReadLock(); }
            }
        }

        public bool IsEmpty => Size == 0;

        public bool Insert(string word, T value = default)
        {
            if (string.IsNullOrEmpty(word))
                return false;

            _lock.EnterWriteLock();
            try
            {
                var node = _root;
                foreach (var ch in word)
                {
                    if (!node.Children.ContainsKey(ch))
                        node.Children[ch] = new TrieNode<T>();
                    node = node.Children[ch];
                }

                var isNew = !node.IsEnd;
                if (isNew) _size++;
                node.IsEnd = true;
                node.Value = value;
                return isNew;
            }
            finally { _lock.ExitWriteLock(); }
        }

        public bool Search(string word, out T value)
        {
            value = default;
            _lock.EnterReadLock();
            try
            {
                var node = FindNode(word);
                if (node != null && node.IsEnd)
                {
                    value = node.Value;
                    return true;
                }
                return false;
            }
            finally { _lock.ExitReadLock(); }
        }

        public bool Search(string word)
        {
            _lock.EnterReadLock();
            try
            {
                var node = FindNode(word);
                return node != null && node.IsEnd;
            }
            finally { _lock.ExitReadLock(); }
        }

        public bool StartsWith(string prefix)
        {
            _lock.EnterReadLock();
            try { return FindNode(prefix) != null; }
            finally { _lock.ExitReadLock(); }
        }

        public bool Delete(string word)
        {
            if (string.IsNullOrEmpty(word)) return false;

            _lock.EnterWriteLock();
            try
            {
                var path = new List<TrieNode<T>> { _root };
                var chars = new List<char>();
                var node = _root;

                foreach (var ch in word)
                {
                    if (!node.Children.ContainsKey(ch)) return false;
                    chars.Add(ch);
                    node = node.Children[ch];
                    path.Add(node);
                }

                if (!node.IsEnd) return false;

                node.IsEnd = false;
                node.Value = default;
                _size--;

                for (int i = path.Count - 1; i > 0; i--)
                {
                    var current = path[i];
                    if (current.IsEnd || current.Children.Count > 0) break;
                    path[i - 1].Children.Remove(chars[i - 1]);
                }

                return true;
            }
            finally { _lock.ExitWriteLock(); }
        }

        public List<string> WordsWithPrefix(string prefix)
        {
            _lock.EnterReadLock();
            try
            {
                var results = new List<string>();
                var startNode = FindNode(prefix);
                if (startNode == null) return results;
                CollectWords(startNode, prefix, results);
                return results;
            }
            finally { _lock.ExitReadLock(); }
        }

        public List<string> AutoComplete(string prefix, int limit = 10)
        {
            var all = WordsWithPrefix(prefix);
            return all.Take(limit).ToList();
        }

        public List<string> AllWords()
        {
            _lock.EnterReadLock();
            try
            {
                var results = new List<string>();
                CollectWords(_root, "", results);
                return results;
            }
            finally { _lock.ExitReadLock(); }
        }

        public void Clear()
        {
            _lock.EnterWriteLock();
            try { _root.Children.Clear(); _size = 0; }
            finally { _lock.ExitWriteLock(); }
        }

        private TrieNode<T> FindNode(string prefix)
        {
            var node = _root;
            foreach (var ch in prefix)
            {
                if (!node.Children.ContainsKey(ch)) return null;
                node = node.Children[ch];
            }
            return node;
        }

        private void CollectWords(TrieNode<T> node, string prefix, List<string> results)
        {
            if (node.IsEnd) results.Add(prefix);
            foreach (var kvp in node.Children.OrderBy(k => k.Key))
                CollectWords(kvp.Value, prefix + kvp.Key, results);
        }

        public void Dispose()
        {
            Dispose(true);
            GC.SuppressFinalize(this);
        }

        protected virtual void Dispose(bool disposing)
        {
            if (!_disposed)
            {
                if (disposing) _lock?.Dispose();
                _disposed = true;
            }
        }

        ~Trie() { Dispose(false); }
    }

    /// <summary>
    /// 泛型 Trie 节点
    /// </summary>
    public class TrieNode<T>
    {
        public Dictionary<char, TrieNode<T>> Children { get; } = new Dictionary<char, TrieNode<T>>();
        public bool IsEnd { get; set; }
        public T Value { get; set; }
    }
}