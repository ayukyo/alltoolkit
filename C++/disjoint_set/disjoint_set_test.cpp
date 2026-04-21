/**
 * @file disjoint_set_test.cpp
 * @brief DisjointSet 单元测试
 * @author AllToolkit
 * @date 2026-04-22
 */

#include "mod.hpp"
#include <iostream>
#include <cassert>
#include <string>
#include <sstream>

using namespace alltoolkit;

// 测试辅助宏
#define TEST(name) std::cout << "Testing " << name << "..." << std::endl
#define PASS() std::cout << "  ✓ PASS" << std::endl
#define ASSERT_EQ(a, b) assert((a) == (b))
#define ASSERT_TRUE(a) assert(a)
#define ASSERT_FALSE(a) assert(!(a))

// ============================================================================
// 基础操作测试
// ============================================================================

void testBasicOperations() {
    TEST("Basic Operations");
    
    DisjointSet<int> ds;
    
    // 初始状态
    ASSERT_EQ(ds.size(), 0);
    ASSERT_EQ(ds.componentCount(), 0);
    ASSERT_FALSE(ds.contains(1));
    
    // 创建集合
    ASSERT_TRUE(ds.makeSet(1));
    ASSERT_FALSE(ds.makeSet(1));  // 已存在
    ASSERT_TRUE(ds.makeSet(2));
    ASSERT_TRUE(ds.makeSet(3));
    
    ASSERT_EQ(ds.size(), 3);
    ASSERT_EQ(ds.componentCount(), 3);
    ASSERT_TRUE(ds.contains(1));
    
    // Find 操作
    auto root1 = ds.find(1);
    ASSERT_TRUE(root1.has_value());
    ASSERT_EQ(*root1, 1);
    
    auto root4 = ds.find(4);
    ASSERT_FALSE(root4.has_value());  // 不存在
    
    PASS();
}

// ============================================================================
// Union 操作测试
// ============================================================================

void testUnionOperations() {
    TEST("Union Operations");
    
    DisjointSet<int> ds;
    ds.makeSet(1);
    ds.makeSet(2);
    ds.makeSet(3);
    ds.makeSet(4);
    
    // Union 1 和 2
    ASSERT_TRUE(ds.unite(1, 2));
    ASSERT_EQ(ds.componentCount(), 3);
    ASSERT_TRUE(ds.connected(1, 2));
    
    // 再次 union 相同元素应返回 false
    ASSERT_FALSE(ds.unite(1, 2));
    
    // Union 不存在的元素
    ASSERT_FALSE(ds.unite(1, 100));
    
    // 连续 union
    ASSERT_TRUE(ds.unite(2, 3));
    ASSERT_TRUE(ds.connected(1, 3));
    ASSERT_EQ(ds.componentCount(), 2);
    
    PASS();
}

// ============================================================================
// 连通性测试
// ============================================================================

void testConnected() {
    TEST("Connected Query");
    
    DisjointSet<std::string> ds;
    ds.makeSet("A");
    ds.makeSet("B");
    ds.makeSet("C");
    ds.makeSet("D");
    
    ASSERT_FALSE(ds.connected("A", "B"));
    
    ds.unite("A", "B");
    ASSERT_TRUE(ds.connected("A", "B"));
    ASSERT_FALSE(ds.connected("A", "C"));
    
    ds.unite("B", "C");
    ASSERT_TRUE(ds.connected("A", "C"));
    ASSERT_FALSE(ds.connected("A", "D"));
    
    // 不存在的元素
    ASSERT_FALSE(ds.connected("A", "E"));
    
    PASS();
}

// ============================================================================
// 分量大小测试
// ============================================================================

void testComponentSize() {
    TEST("Component Size");
    
    DisjointSet<int> ds;
    ds.makeSets({1, 2, 3, 4, 5, 6});
    
    ASSERT_EQ(ds.componentSize(1), 1);
    
    ds.unite(1, 2);
    ASSERT_EQ(ds.componentSize(1), 2);
    ASSERT_EQ(ds.componentSize(2), 2);
    
    ds.unite(2, 3);
    ds.unite(3, 4);
    ASSERT_EQ(ds.componentSize(1), 4);
    
    // 不存在的元素
    ASSERT_EQ(ds.componentSize(100), 0);
    
    PASS();
}

// ============================================================================
// 批量操作测试
// ============================================================================

void testBatchOperations() {
    TEST("Batch Operations");
    
    DisjointSet<int> ds;
    
    // makeSets
    size_t added = ds.makeSets({1, 2, 3, 4, 5});
    ASSERT_EQ(added, 5);
    ASSERT_EQ(ds.size(), 5);
    
    // uniteAll
    size_t unions = ds.uniteAll({1, 2, 3});
    ASSERT_EQ(unions, 2);
    ASSERT_TRUE(ds.connected(1, 3));
    
    // fromEdges
    DisjointSet<std::string> ds2;
    ds2.fromEdges({{"A", "B"}, {"B", "C"}, {"D", "E"}});
    ASSERT_EQ(ds2.size(), 5);
    ASSERT_EQ(ds2.componentCount(), 2);
    ASSERT_TRUE(ds2.connected("A", "C"));
    ASSERT_FALSE(ds2.connected("A", "D"));
    
    PASS();
}

// ============================================================================
// 获取分量测试
// ============================================================================

void testGetComponents() {
    TEST("Get Components");
    
    DisjointSet<int> ds;
    ds.makeSets({1, 2, 3, 4, 5, 6});
    
    ds.unite(1, 2);
    ds.unite(2, 3);
    ds.unite(4, 5);
    
    auto components = ds.getComponents();
    ASSERT_EQ(components.size(), 3);
    
    // 检查特定分量
    auto comp1 = ds.getComponent(1);
    ASSERT_EQ(comp1.size(), 3);
    ASSERT_TRUE(comp1.count(1) > 0);
    ASSERT_TRUE(comp1.count(2) > 0);
    ASSERT_TRUE(comp1.count(3) > 0);
    
    auto reps = ds.getRepresentatives();
    ASSERT_EQ(reps.size(), 3);
    
    PASS();
}

// ============================================================================
// 字符串表示测试
// ============================================================================

void testToString() {
    TEST("ToString");
    
    DisjointSet<int> ds;
    ds.makeSets({1, 2, 3});
    ds.unite(1, 2);
    
    std::string str = ds.toString();
    // 应包含 DisjointSet 和元素
    ASSERT_TRUE(str.find("DisjointSet") != std::string::npos);
    
    PASS();
}

// ============================================================================
// Kruskal MST 测试
// ============================================================================

void testKruskalMST() {
    TEST("Kruskal MST");
    
    std::vector<std::string> nodes = {"A", "B", "C", "D"};
    std::vector<WeightedEdge<std::string>> edges = {
        {"A", "B", 1.0},
        {"B", "C", 2.0},
        {"C", "D", 3.0},
        {"A", "D", 4.0},
        {"B", "D", 5.0}
    };
    
    auto [mst, weight] = kruskalMST(nodes, edges);
    
    ASSERT_EQ(mst.size(), 3);  // MST 应有 n-1 条边
    ASSERT_EQ(weight, 6.0);    // 1 + 2 + 3
    
    PASS();
}

// ============================================================================
// 环检测测试
// ============================================================================

void testCycleDetection() {
    TEST("Cycle Detection");
    
    std::vector<int> nodes = {1, 2, 3};
    
    // 有环（三角形）
    std::vector<std::pair<int, int>> edges1 = {{1, 2}, {2, 3}, {3, 1}};
    ASSERT_TRUE(hasCycleUndirected(nodes, edges1));
    
    // 无环（直线）
    std::vector<std::pair<int, int>> edges2 = {{1, 2}, {2, 3}};
    ASSERT_FALSE(hasCycleUndirected(nodes, edges2));
    
    PASS();
}

// ============================================================================
// 连通分量计数测试
// ============================================================================

void testCountConnectedComponents() {
    TEST("Count Connected Components");
    
    std::vector<int> nodes = {1, 2, 3, 4, 5};
    std::vector<std::pair<int, int>> edges = {{1, 2}, {2, 3}, {4, 5}};
    
    size_t count = countConnectedComponents(nodes, edges);
    ASSERT_EQ(count, 2);
    
    // 连通图
    std::vector<std::pair<int, int>> edges2 = {{1, 2}, {2, 3}, {3, 4}, {4, 5}};
    ASSERT_TRUE(isConnectedGraph(nodes, edges2));
    
    // 不连通图
    ASSERT_FALSE(isConnectedGraph(nodes, edges));
    
    PASS();
}

// ============================================================================
// 图像连通分量测试
// ============================================================================

void testImageConnectedComponents() {
    TEST("Image Connected Components");
    
    std::vector<std::vector<int>> grid = {
        {1, 1, 0, 0, 1},
        {1, 0, 0, 1, 1},
        {0, 0, 1, 1, 0},
        {0, 1, 1, 0, 0}
    };
    
    auto labels = findConnectedPixels(grid, 4);
    
    // 检查返回的标签网格大小正确
    ASSERT_EQ(labels.size(), 4);
    ASSERT_EQ(labels[0].size(), 5);
    
    // 检查前景像素被标记
    ASSERT_TRUE(labels[0][0] > 0);
    ASSERT_TRUE(labels[0][1] > 0);
    ASSERT_TRUE(labels[1][0] > 0);
    
    // 检查背景像素为 0
    ASSERT_EQ(labels[0][2], 0);
    ASSERT_EQ(labels[1][1], 0);
    
    PASS();
}

// ============================================================================
// 复制和重置测试
// ============================================================================

void testCopyAndReset() {
    TEST("Copy and Reset");
    
    DisjointSet<int> ds;
    ds.makeSets({1, 2, 3, 4});
    ds.unite(1, 2);
    ds.unite(3, 4);
    
    // 复制
    auto copy = ds.copy();
    ASSERT_EQ(copy.size(), 4);
    ASSERT_EQ(copy.componentCount(), 2);
    ASSERT_TRUE(copy.connected(1, 2));
    
    // 修改原集合不影响复制
    ds.unite(2, 3);
    ASSERT_FALSE(copy.connected(1, 3));  // 复制中仍不连通
    
    // 重置
    ds.reset();
    ASSERT_EQ(ds.size(), 0);
    ASSERT_EQ(ds.componentCount(), 0);
    
    PASS();
}

// ============================================================================
// 大规模测试
// ============================================================================

void testLargeScale() {
    TEST("Large Scale (10000 elements)");
    
    DisjointSet<int> ds;
    
    // 创建 10000 个元素
    for (int i = 0; i < 10000; i++) {
        ds.makeSet(i);
    }
    
    ASSERT_EQ(ds.size(), 10000);
    ASSERT_EQ(ds.componentCount(), 10000);
    
    // 合并为 100 个分量（每个分量 100 个元素）
    for (int i = 0; i < 100; i++) {
        for (int j = 1; j < 100; j++) {
            ds.unite(i * 100, i * 100 + j);
        }
    }
    
    ASSERT_EQ(ds.componentCount(), 100);
    ASSERT_EQ(ds.componentSize(0), 100);
    ASSERT_EQ(ds.componentSize(5000), 100);
    
    PASS();
}

// ============================================================================
// Main
// ============================================================================

int main() {
    std::cout << "\n=== DisjointSet Unit Tests ===\n\n";
    
    testBasicOperations();
    testUnionOperations();
    testConnected();
    testComponentSize();
    testBatchOperations();
    testGetComponents();
    testToString();
    testKruskalMST();
    testCycleDetection();
    testCountConnectedComponents();
    testImageConnectedComponents();
    testCopyAndReset();
    testLargeScale();
    
    std::cout << "\n=== All Tests Passed! ===\n\n";
    return 0;
}