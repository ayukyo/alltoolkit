/**
 * @file mod.hpp
 * @brief C++ Disjoint Set (Union-Find) 工具库 - 零依赖、现代 C++17 实现
 * @author AllToolkit
 * @version 1.0.0
 * @date 2026-04-22
 *
 * 提供:
 * - DisjointSet 类，支持路径压缩和按秩合并优化
 * - 高效的 find、union、connected 操作
 * - 任意可哈希元素类型支持
 * - 连通分量计数和大小追踪
 * - 批量操作支持
 * - Kruskal MST 算法辅助函数
 * - 图连通性分析工具
 *
 * 时间复杂度 (均摊):
 * - Find: O(α(n)) ≈ O(1)，α 为反阿克曼函数
 * - Union: O(α(n)) ≈ O(1)
 * - Connected: O(α(n)) ≈ O(1)
 */

#ifndef ALLTOOLKIT_DISJOINT_SET_HPP
#define ALLTOOLKIT_DISJOINT_SET_HPP

#include <functional>
#include <optional>
#include <unordered_map>
#include <unordered_set>
#include <vector>
#include <set>
#include <map>
#include <tuple>
#include <algorithm>
#include <stdexcept>
#include <sstream>

namespace alltoolkit {

/**
 * @brief 并查集 (Union-Find) 数据结构
 * 
 * 支持路径压缩和按秩合并优化的并查集实现。
 * 维护一组不相交集合，提供近常数时间的查找、合并和连通性查询。
 * 
 * @tparam T 元素类型，必须可哈希
 * 
 * @example
 * ```cpp
 * DisjointSet<std::string> ds;
 * ds.makeSet("A");
 * ds.makeSet("B");
 * ds.unite("A", "B");
 * bool connected = ds.connected("A", "B"); // true
 * ```
 */
template<typename T>
class DisjointSet {
public:
    // ========================================================================
    // 构造函数和基本操作
    // ========================================================================
    
    /**
     * @brief 构造空的并查集
     */
    DisjointSet() = default;
    
    /**
     * @brief 从元素列表构造并查集
     * @param elements 初始元素列表
     */
    explicit DisjointSet(const std::vector<T>& elements) {
        for (const auto& elem : elements) {
            makeSet(elem);
        }
    }
    
    /**
     * @brief 从初始化列表构造
     * @param elements 初始元素
     */
    DisjointSet(std::initializer_list<T> elements) {
        for (const auto& elem : elements) {
            makeSet(elem);
        }
    }
    
    // ========================================================================
    // 核心操作
    // ========================================================================
    
    /**
     * @brief 创建包含单个元素的新集合
     * @param element 要添加的元素
     * @return true 如果元素被添加，false 如果元素已存在
     */
    bool makeSet(const T& element) {
        if (parent_.find(element) != parent_.end()) {
            return false;
        }
        
        parent_[element] = element;
        rank_[element] = 0;
        size_[element] = 1;
        count_++;
        return true;
    }
    
    /**
     * @brief 批量创建集合
     * @param elements 元素列表
     * @return 实际添加的元素数量
     */
    size_t makeSets(const std::vector<T>& elements) {
        size_t added = 0;
        for (const auto& elem : elements) {
            if (makeSet(elem)) {
                added++;
            }
        }
        return added;
    }
    
    /**
     * @brief 查找元素所在集合的代表元（根）
     * 
     * 使用路径压缩优化，使后续查询更快。
     * 
     * @param element 要查找的元素
     * @return 代表元，如果元素不存在则返回 std::nullopt
     */
    std::optional<T> find(const T& element) {
        auto it = parent_.find(element);
        if (it == parent_.end()) {
            return std::nullopt;
        }
        
        // 路径压缩：使每个节点直接指向根
        if (it->second != it->first) {
            parent_[element] = find(it->second).value();
        }
        return parent_[element];
    }
    
    /**
     * @brief const 版本的查找
     */
    std::optional<T> find(const T& element) const {
        auto it = parent_.find(element);
        if (it == parent_.end()) {
            return std::nullopt;
        }
        
        // 对于 const 版本，不进行路径压缩
        T current = it->second;
        while (parent_.at(current) != current) {
            current = parent_.at(current);
        }
        return current;
    }
    
    /**
     * @brief 合并两个元素所在的集合
     * 
     * 使用按秩合并优化，保持树较浅。
     * 
     * @param element1 第一个元素
     * @param element2 第二个元素
     * @return true 如果集合被合并，false 如果已在同一集合或元素不存在
     */
    bool unite(const T& element1, const T& element2) {
        auto root1 = find(element1);
        auto root2 = find(element2);
        
        if (!root1 || !root2) {
            return false;
        }
        
        if (root1 == root2) {
            return false;  // 已在同一集合
        }
        
        // 按秩合并：将较矮的树连接到较高的树
        T r1 = *root1;
        T r2 = *root2;
        
        if (rank_[r1] < rank_[r2]) {
            std::swap(r1, r2);
        }
        
        parent_[r2] = r1;
        size_[r1] += size_[r2];
        
        if (rank_[r1] == rank_[r2]) {
            rank_[r1]++;
        }
        
        count_--;
        return true;
    }
    
    /**
     * @brief unite 的别名
     */
    bool unionSets(const T& element1, const T& element2) {
        return unite(element1, element2);
    }
    
    /**
     * @brief 检查两个元素是否在同一集合中
     * @param element1 第一个元素
     * @param element2 第二个元素
     * @return true 如果两元素存在且在同一集合
     */
    bool connected(const T& element1, const T& element2) const {
        auto root1 = find(element1);
        auto root2 = find(element2);
        return root1 && root2 && root1 == root2;
    }
    
    // ========================================================================
    // 查询操作
    // ========================================================================
    
    /**
     * @brief 获取元素数量
     */
    size_t size() const {
        return parent_.size();
    }
    
    /**
     * @brief 检查元素是否存在
     */
    bool contains(const T& element) const {
        return parent_.find(element) != parent_.end();
    }
    
    /**
     * @brief 获取连通分量数量
     */
    size_t componentCount() const {
        return count_;
    }
    
    /**
     * @brief 获取元素所在分量的大小
     * @param element 要检查的元素
     * @return 分量大小，如果元素不存在返回 0
     */
    size_t componentSize(const T& element) const {
        auto root = find(element);
        if (!root) {
            return 0;
        }
        return size_.at(*root);
    }
    
    /**
     * @brief 获取元素所在分量的所有元素
     * @param element 要查询的元素
     * @return 包含该元素的分量的所有元素集合
     */
    std::unordered_set<T> getComponent(const T& element) const {
        std::unordered_set<T> result;
        auto targetRoot = find(element);
        if (!targetRoot) {
            return result;
        }
        
        for (const auto& [elem, _] : parent_) {
            auto root = find(elem);
            if (root && root == targetRoot) {
                result.insert(elem);
            }
        }
        return result;
    }
    
    /**
     * @brief 获取所有连通分量
     * @return 连通分量列表，每个分量是一个元素集合
     */
    std::vector<std::unordered_set<T>> getComponents() const {
        std::map<T, std::unordered_set<T>> componentMap;
        
        for (const auto& [elem, _] : parent_) {
            auto root = find(elem);
            if (root) {
                componentMap[*root].insert(elem);
            }
        }
        
        std::vector<std::unordered_set<T>> result;
        for (auto& [_, comp] : componentMap) {
            result.push_back(std::move(comp));
        }
        return result;
    }
    
    /**
     * @brief 获取所有代表元（每个分量的根）
     */
    std::unordered_set<T> getRepresentatives() const {
        std::unordered_set<T> reps;
        for (const auto& [elem, _] : parent_) {
            auto root = find(elem);
            if (root) {
                reps.insert(*root);
            }
        }
        return reps;
    }
    
    /**
     * @brief 获取元素的秩
     * @param element 要检查的元素
     * @return 秩，如果元素不存在返回 -1
     */
    int getRank(const T& element) const {
        auto root = find(element);
        if (!root) {
            return -1;
        }
        auto it = rank_.find(*root);
        return it != rank_.end() ? static_cast<int>(it->second) : -1;
    }
    
    // ========================================================================
    // 批量操作
    // ========================================================================
    
    /**
     * @brief 从边列表创建并查集
     * @param edges 边列表，每条边是一对元素
     * @return 引用自身，支持链式调用
     */
    DisjointSet<T>& fromEdges(const std::vector<std::pair<T, T>>& edges) {
        for (const auto& [e1, e2] : edges) {
            makeSet(e1);
            makeSet(e2);
            unite(e1, e2);
        }
        return *this;
    }
    
    /**
     * @brief 批量添加连接
     * @param connections 连接列表
     * @return 成功合并的数量
     */
    size_t addConnections(const std::vector<std::pair<T, T>>& connections) {
        // 首先添加所有元素
        std::unordered_set<T> elements;
        for (const auto& [e1, e2] : connections) {
            elements.insert(e1);
            elements.insert(e2);
        }
        for (const auto& e : elements) {
            makeSet(e);
        }
        
        // 然后执行合并
        size_t unions = 0;
        for (const auto& [e1, e2] : connections) {
            if (unite(e1, e2)) {
                unions++;
            }
        }
        return unions;
    }
    
    /**
     * @brief 合并多个元素到同一集合
     * @param elements 要合并的元素
     * @return 成功合并的数量
     */
    size_t uniteAll(const std::vector<T>& elements) {
        if (elements.size() < 2) {
            return 0;
        }
        
        size_t unions = 0;
        const T& first = elements[0];
        for (size_t i = 1; i < elements.size(); i++) {
            if (unite(first, elements[i])) {
                unions++;
            }
        }
        return unions;
    }
    
    /**
     * @brief 重置为空状态
     */
    void reset() {
        parent_.clear();
        rank_.clear();
        size_.clear();
        count_ = 0;
    }
    
    /**
     * @brief 清空（reset 的别名）
     */
    void clear() {
        reset();
    }
    
    // ========================================================================
    // 工具方法
    // ========================================================================
    
    /**
     * @brief 创建副本
     */
    DisjointSet<T> copy() const {
        DisjointSet<T> newDs;
        newDs.parent_ = parent_;
        newDs.rank_ = rank_;
        newDs.size_ = size_;
        newDs.count_ = count_;
        return newDs;
    }
    
    /**
     * @brief 转换为字符串表示
     */
    std::string toString() const {
        auto components = getComponents();
        std::ostringstream oss;
        oss << "DisjointSet(";
        for (size_t i = 0; i < components.size(); i++) {
            if (i > 0) oss << ", ";
            oss << "{";
            size_t j = 0;
            for (const auto& elem : components[i]) {
                if (j > 0) oss << ", ";
                oss << elem;
                j++;
            }
            oss << "}";
        }
        oss << ")";
        return oss.str();
    }
    
    /**
     * @brief 获取所有元素
     */
    std::unordered_set<T> elements() const {
        std::unordered_set<T> result;
        for (const auto& [elem, _] : parent_) {
            result.insert(elem);
        }
        return result;
    }
    
    // 迭代器支持
    auto begin() const { return parent_.begin(); }
    auto end() const { return parent_.end(); }
    
private:
    std::unordered_map<T, T> parent_;      // 父节点映射
    std::unordered_map<T, size_t> rank_;    // 秩（树高度估计）
    std::unordered_map<T, size_t> size_;    // 分量大小
    size_t count_ = 0;                       // 连通分量计数
};

// ============================================================================
// 图/网络工具函数
// ============================================================================

/**
 * @brief 计算无向图的连通分量数量
 * @param nodes 节点列表
 * @param edges 边列表
 * @return 连通分量数量
 */
template<typename T>
size_t countConnectedComponents(const std::vector<T>& nodes, 
                                const std::vector<std::pair<T, T>>& edges) {
    DisjointSet<T> ds(nodes);
    for (const auto& [n1, n2] : edges) {
        ds.makeSet(n1);
        ds.makeSet(n2);
        ds.unite(n1, n2);
    }
    return ds.componentCount();
}

/**
 * @brief 查找所有连通分量
 * @param elements 元素列表
 * @param connections 连接列表
 * @return 连通分量列表
 */
template<typename T>
std::vector<std::unordered_set<T>> findConnectedGroups(
    const std::vector<T>& elements,
    const std::vector<std::pair<T, T>>& connections) {
    
    DisjointSet<T> ds;
    for (const auto& elem : elements) {
        ds.makeSet(elem);
    }
    for (const auto& [e1, e2] : connections) {
        ds.unite(e1, e2);
    }
    return ds.getComponents();
}

/**
 * @brief 检查图是否连通（只有一个分量）
 * @param nodes 节点列表
 * @param edges 边列表
 * @return true 如果图连通
 */
template<typename T>
bool isConnectedGraph(const std::vector<T>& nodes,
                     const std::vector<std::pair<T, T>>& edges) {
    if (nodes.empty()) {
        return true;
    }
    return countConnectedComponents(nodes, edges) == 1;
}

/**
 * @brief 使用并查集检测无向图中是否有环
 * @param nodes 节点列表
 * @param edges 边列表
 * @return true 如果存在环
 */
template<typename T>
bool hasCycleUndirected(const std::vector<T>& nodes,
                        const std::vector<std::pair<T, T>>& edges) {
    DisjointSet<T> ds;
    for (const auto& node : nodes) {
        ds.makeSet(node);
    }
    
    for (const auto& [n1, n2] : edges) {
        if (ds.connected(n1, n2)) {
            return true;  // 添加这条边会形成环
        }
        ds.unite(n1, n2);
    }
    
    return false;
}

// ============================================================================
// Kruskal MST 辅助
// ============================================================================

/**
 * @brief 带权边类型: (node1, node2, weight)
 */
template<typename T, typename W = double>
using WeightedEdge = std::tuple<T, T, W>;

/**
 * @brief 使用 Kruskal 算法求最小生成树
 * @param nodes 节点列表
 * @param edges 带权边列表
 * @return pair<MST边列表, 总权重>，如果不连通返回空
 */
template<typename T, typename W = double>
std::pair<std::vector<WeightedEdge<T, W>>, W> kruskalMST(
    const std::vector<T>& nodes,
    const std::vector<WeightedEdge<T, W>>& edges) {
    
    DisjointSet<T> ds;
    for (const auto& node : nodes) {
        ds.makeSet(node);
    }
    
    // 按权重排序边
    auto sortedEdges = edges;
    std::sort(sortedEdges.begin(), sortedEdges.end(),
              [](const auto& a, const auto& b) {
                  return std::get<2>(a) < std::get<2>(b);
              });
    
    std::vector<WeightedEdge<T, W>> mst;
    W totalWeight = W{};
    
    for (const auto& [n1, n2, weight] : sortedEdges) {
        if (!ds.connected(n1, n2)) {
            ds.unite(n1, n2);
            mst.emplace_back(n1, n2, weight);
            totalWeight += weight;
            
            if (mst.size() == nodes.size() - 1) {
                break;
            }
        }
    }
    
    // 检查是否形成有效的 MST
    if (mst.size() != nodes.size() - 1) {
        return {{}, W{}};
    }
    
    return {mst, totalWeight};
}

// ============================================================================
// 图像处理工具（连通分量标记）
// ============================================================================

/**
 * @brief 在二值图像中标记连通分量
 * @param grid 二维网格，1 表示前景，0 表示背景
 * @param connectivity 4 表示 4-连通，8 表示 8-连通（包括对角线）
 * @return 标记后的网格，每个连通分量有唯一标签
 */
inline std::vector<std::vector<int>> findConnectedPixels(
    const std::vector<std::vector<int>>& grid,
    int connectivity = 4) {
    
    if (grid.empty() || grid[0].empty()) {
        return {};
    }
    
    size_t rows = grid.size();
    size_t cols = grid[0].size();
    DisjointSet<int> ds;
    
    // 第一遍：分配临时标签并记录等价关系
    std::vector<std::vector<int>> labels(rows, std::vector<int>(cols, 0));
    int currentLabel = 0;
    
    for (size_t r = 0; r < rows; r++) {
        for (size_t c = 0; c < cols; c++) {
            if (grid[r][c] == 0) {
                continue;
            }
            
            std::vector<int> neighbors;
            
            // 检查上方邻居
            if (r > 0 && labels[r-1][c] > 0) {
                neighbors.push_back(labels[r-1][c]);
            }
            // 检查左侧邻居
            if (c > 0 && labels[r][c-1] > 0) {
                neighbors.push_back(labels[r][c-1]);
            }
            
            // 8-连通额外检查对角线
            if (connectivity == 8) {
                if (r > 0 && c > 0 && labels[r-1][c-1] > 0) {
                    neighbors.push_back(labels[r-1][c-1]);
                }
                if (r > 0 && c < cols-1 && labels[r-1][c+1] > 0) {
                    neighbors.push_back(labels[r-1][c+1]);
                }
            }
            
            if (neighbors.empty()) {
                currentLabel++;
                labels[r][c] = currentLabel;
                ds.makeSet(currentLabel);
            } else {
                int minLabel = *std::min_element(neighbors.begin(), neighbors.end());
                labels[r][c] = minLabel;
                for (int lbl : neighbors) {
                    ds.unite(minLabel, lbl);
                }
            }
        }
    }
    
    // 第二遍：分配最终标签
    std::unordered_map<int, int> labelMap;
    int finalLabel = 0;
    
    for (size_t r = 0; r < rows; r++) {
        for (size_t c = 0; c < cols; c++) {
            if (labels[r][c] > 0) {
                auto root = ds.find(labels[r][c]);
                if (root) {
                    if (labelMap.find(*root) == labelMap.end()) {
                        finalLabel++;
                        labelMap[*root] = finalLabel;
                    }
                    labels[r][c] = labelMap[*root];
                }
            }
        }
    }
    
    return labels;
}

} // namespace alltoolkit

#endif // ALLTOOLKIT_DISJOINT_SET_HPP