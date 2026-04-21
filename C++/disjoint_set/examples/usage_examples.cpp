/**
 * @file usage_examples.cpp
 * @brief DisjointSet 使用示例
 * @author AllToolkit
 * @date 2026-04-22
 */

#include "../mod.hpp"
#include <iostream>
#include <iomanip>

using namespace alltoolkit;

// ============================================================================
// 示例 1: 基础使用
// ============================================================================

void example1_BasicUsage() {
    std::cout << "=== Example 1: Basic Usage ===\n\n";
    
    DisjointSet<std::string> ds;
    
    // 创建集合
    std::cout << "Creating sets for A, B, C, D, E...\n";
    ds.makeSets({"A", "B", "C", "D", "E"});
    
    std::cout << "Initial state:\n";
    std::cout << "  Size: " << ds.size() << "\n";
    std::cout << "  Components: " << ds.componentCount() << "\n";
    std::cout << "  " << ds.toString() << "\n\n";
    
    // 合并操作
    std::cout << "Uniting A-B, B-C, D-E...\n";
    ds.unite("A", "B");
    ds.unite("B", "C");
    ds.unite("D", "E");
    
    std::cout << "After unions:\n";
    std::cout << "  Components: " << ds.componentCount() << "\n";
    std::cout << "  " << ds.toString() << "\n\n";
    
    // 连通性查询
    std::cout << "Connectivity queries:\n";
    std::cout << "  A and C connected: " << (ds.connected("A", "C") ? "YES" : "NO") << "\n";
    std::cout << "  A and D connected: " << (ds.connected("A", "D") ? "YES" : "NO") << "\n";
    std::cout << "  D and E connected: " << (ds.connected("D", "E") ? "YES" : "NO") << "\n\n";
    
    // 分量大小
    std::cout << "Component sizes:\n";
    std::cout << "  Component containing A: " << ds.componentSize("A") << " elements\n";
    std::cout << "  Component containing E: " << ds.componentSize("E") << " elements\n\n";
}

// ============================================================================
// 示例 2: 社交网络分析
// ============================================================================

void example2_SocialNetwork() {
    std::cout << "=== Example 2: Social Network Analysis ===\n\n";
    
    // 定义用户和友谊关系
    std::vector<std::string> users = {"Alice", "Bob", "Carol", "Dave", "Eve", "Frank"};
    std::vector<std::pair<std::string, std::string>> friendships = {
        {"Alice", "Bob"},
        {"Bob", "Carol"},
        {"Dave", "Eve"},
        {"Eve", "Frank"}
    };
    
    std::cout << "Users: Alice, Bob, Carol, Dave, Eve, Frank\n";
    std::cout << "Friendships:\n";
    for (const auto& [u1, u2] : friendships) {
        std::cout << "  " << u1 << " <-> " << u2 << "\n";
    }
    std::cout << "\n";
    
    // 构建并查集
    auto groups = findConnectedGroups(users, friendships);
    
    std::cout << "Friend circles found: " << groups.size() << "\n";
    for (size_t i = 0; i < groups.size(); i++) {
        std::cout << "  Circle " << (i + 1) << ": ";
        for (const auto& user : groups[i]) {
            std::cout << user << " ";
        }
        std::cout << "\n";
    }
    std::cout << "\n";
    
    // 分析结果：获取分量大小
    DisjointSet<std::string> ds;
    for (const auto& user : users) ds.makeSet(user);
    for (const auto& [u1, u2] : friendships) ds.unite(u1, u2);
    
    std::cout << "Analysis:\n";
    std::cout << "  Alice's circle size: " << ds.componentSize("Alice") << "\n";
    std::cout << "  Dave's circle size: " << ds.componentSize("Dave") << "\n\n";
}

// ============================================================================
// 示例 3: Kruskal 最小生成树
// ============================================================================

void example3_KruskalMST() {
    std::cout << "=== Example 3: Kruskal's Minimum Spanning Tree ===\n\n";
    
    // 定义城市（节点）和道路（带权边）
    std::vector<std::string> cities = {"Beijing", "Shanghai", "Guangzhou", "Shenzhen", "Hangzhou"};
    std::vector<WeightedEdge<std::string>> roads = {
        {"Beijing", "Shanghai", 1200.0},
        {"Beijing", "Guangzhou", 1900.0},
        {"Shanghai", "Guangzhou", 1400.0},
        {"Shanghai", "Hangzhou", 180.0},
        {"Guangzhou", "Shenzhen", 140.0},
        {"Hangzhou", "Shenzhen", 1300.0}
    };
    
    std::cout << "Cities: Beijing, Shanghai, Guangzhou, Shenzhen, Hangzhou\n";
    std::cout << "Roads (with distances in km):\n";
    for (const auto& [c1, c2, dist] : roads) {
        std::cout << "  " << c1 << " <-> " << c2 << " : " << dist << " km\n";
    }
    std::cout << "\n";
    
    // 计算 MST
    auto [mst, totalDist] = kruskalMST(cities, roads);
    
    std::cout << "Minimum Spanning Tree (optimal network):\n";
    std::cout << "  Edges:\n";
    for (const auto& [c1, c2, dist] : mst) {
        std::cout << "    " << c1 << " <-> " << c2 << " : " << dist << " km\n";
    }
    std::cout << "  Total distance: " << totalDist << " km\n\n";
}

// ============================================================================
// 示例 4: 环检测
// ============================================================================

void example4_CycleDetection() {
    std::cout << "=== Example 4: Cycle Detection in Undirected Graph ===\n\n";
    
    // 图 1：有环（三角形）
    std::vector<int> nodes1 = {1, 2, 3, 4};
    std::vector<std::pair<int, int>> edges1 = {
        {1, 2}, {2, 3}, {3, 1}, {3, 4}
    };
    
    std::cout << "Graph 1: Triangle (1-2-3-1) plus edge to 4\n";
    std::cout << "  Has cycle: " << (hasCycleUndirected(nodes1, edges1) ? "YES" : "NO") << "\n\n";
    
    // 图 2：无环（简单路径）
    std::vector<int> nodes2 = {1, 2, 3, 4, 5};
    std::vector<std::pair<int, int>> edges2 = {
        {1, 2}, {2, 3}, {3, 4}, {4, 5}
    };
    
    std::cout << "Graph 2: Simple path 1-2-3-4-5\n";
    std::cout << "  Has cycle: " << (hasCycleUndirected(nodes2, edges2) ? "YES" : "NO") << "\n\n";
}

// ============================================================================
// 示例 5: 图像连通分量标记
// ============================================================================

void example5_ImageConnectedComponents() {
    std::cout << "=== Example 5: Image Connected Component Labeling ===\n\n";
    
    // 二值图像网格
    std::vector<std::vector<int>> grid = {
        {1, 1, 0, 0, 1},
        {1, 0, 0, 1, 1},
        {0, 0, 1, 1, 0},
        {0, 1, 1, 0, 0}
    };
    
    std::cout << "Binary image (1 = foreground, 0 = background):\n";
    for (const auto& row : grid) {
        std::cout << "  ";
        for (int cell : row) {
            std::cout << (cell ? "█" : "·") << " ";
        }
        std::cout << "\n";
    }
    std::cout << "\n";
    
    // 标记连通分量（4-连通）
    auto labels = findConnectedPixels(grid, 4);
    
    std::cout << "Connected component labels (4-connected):\n";
    for (const auto& row : labels) {
        std::cout << "  ";
        for (int label : row) {
            if (label == 0) {
                std::cout << "· ";
            } else {
                std::cout << label << " ";
            }
        }
        std::cout << "\n";
    }
    
    // 统计连通分量数量
    std::set<int> uniqueLabels;
    for (const auto& row : labels) {
        for (int label : row) {
            if (label > 0) uniqueLabels.insert(label);
        }
    }
    std::cout << "\nNumber of connected components: " << uniqueLabels.size() << "\n\n";
}

// ============================================================================
// 示例 6: 从边列表构建
// ============================================================================

void example6_FromEdges() {
    std::cout << "=== Example 6: Building from Edge List ===\n\n";
    
    // 定义边（连接关系）
    std::vector<std::pair<int, int>> edges = {
        {1, 2}, {2, 3}, {4, 5}, {5, 6}, {7, 8}
    };
    
    std::cout << "Edges:\n";
    for (const auto& [e1, e2] : edges) {
        std::cout << "  " << e1 << " <-> " << e2 << "\n";
    }
    std::cout << "\n";
    
    // 直接从边构建并查集
    DisjointSet<int> ds;
    ds.fromEdges(edges);
    
    std::cout << "Result:\n";
    std::cout << "  Total elements: " << ds.size() << "\n";
    std::cout << "  Connected components: " << ds.componentCount() << "\n";
    std::cout << "  " << ds.toString() << "\n\n";
    
    // 验证连通性
    std::cout << "Connectivity checks:\n";
    std::cout << "  1 and 3 connected: " << (ds.connected(1, 3) ? "YES" : "NO") << "\n";
    std::cout << "  4 and 6 connected: " << (ds.connected(4, 6) ? "YES" : "NO") << "\n";
    std::cout << "  1 and 7 connected: " << (ds.connected(1, 7) ? "YES" : "NO") << "\n\n";
}

// ============================================================================
// 示例 7: 性能测试（大规模）
// ============================================================================

void example7_LargeScale() {
    std::cout << "=== Example 7: Large Scale Performance ===\n\n";
    
    const int N = 100000;
    
    std::cout << "Creating " << N << " elements...\n";
    
    DisjointSet<int> ds;
    for (int i = 0; i < N; i++) {
        ds.makeSet(i);
    }
    
    std::cout << "  Initial components: " << ds.componentCount() << "\n";
    
    // 合并为 100 个分量
    std::cout << "Merging into 100 groups...\n";
    for (int g = 0; g < 100; g++) {
        for (int i = 1; i < 1000; i++) {
            ds.unite(g * 1000, g * 1000 + i);
        }
    }
    
    std::cout << "  Final components: " << ds.componentCount() << "\n";
    std::cout << "  Component size (group 0): " << ds.componentSize(0) << "\n";
    std::cout << "  Component size (group 99): " << ds.componentSize(99000) << "\n\n";
}

// ============================================================================
// Main
// ============================================================================

int main() {
    std::cout << "\n╔════════════════════════════════════════════════════════════╗\n";
    std::cout << "║          DisjointSet (Union-Find) Usage Examples           ║\n";
    std::cout << "╚════════════════════════════════════════════════════════════╝\n\n";
    
    example1_BasicUsage();
    example2_SocialNetwork();
    example3_KruskalMST();
    example4_CycleDetection();
    example5_ImageConnectedComponents();
    example6_FromEdges();
    example7_LargeScale();
    
    std::cout << "All examples completed!\n\n";
    return 0;
}