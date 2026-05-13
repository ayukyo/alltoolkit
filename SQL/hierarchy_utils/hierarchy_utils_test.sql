-- ============================================================
-- Hierarchy Utils 测试文件
-- ============================================================
-- 测试四种层级模型的实现
-- 使用 SQLite 语法（兼容 MySQL 8.0+, PostgreSQL）
-- ============================================================

-- ============================================================
-- 测试一：邻接表模型测试
-- ============================================================

-- 创建测试表
CREATE TABLE IF NOT EXISTS categories_adj (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    parent_id INTEGER,
    FOREIGN KEY (parent_id) REFERENCES categories_adj(id)
);

-- 插入测试数据
-- 树形结构:
-- 1: Root
--   2: Child A
--     4: Grandchild A1
--     5: Grandchild A2
--   3: Child B
--     6: Grandchild B1

INSERT INTO categories_adj (id, name, parent_id) VALUES
    (1, 'Root', NULL),
    (2, 'Child A', 1),
    (3, 'Child B', 1),
    (4, 'Grandchild A1', 2),
    (5, 'Grandchild A2', 2),
    (6, 'Grandchild B1', 3);

-- 测试1.1: 查询所有子节点（非递归方式）
SELECT 'Test 1.1: Direct children of Root' AS test_name;
SELECT id, name FROM categories_adj WHERE parent_id = 1;
-- 期望结果: 2 (Child A), 3 (Child B)

-- 测试1.2: 检查叶子节点
SELECT 'Test 1.2: Check leaf nodes' AS test_name;
SELECT c.id, c.name,
       CASE WHEN NOT EXISTS (SELECT 1 FROM categories_adj WHERE parent_id = c.id)
            THEN 'Yes' ELSE 'No' END AS is_leaf
FROM categories_adj c
ORDER BY c.id;
-- 期望结果: 4,5,6 是叶子节点

-- 测试1.3: 递归查询所有子孙节点
SELECT 'Test 1.3: All descendants of Root (recursive)' AS test_name;
WITH RECURSIVE descendants AS (
    SELECT id, name, parent_id, 0 AS depth
    FROM categories_adj
    WHERE id = 1
    
    UNION ALL
    
    SELECT c.id, c.name, c.parent_id, d.depth + 1
    FROM categories_adj c
    INNER JOIN descendants d ON c.parent_id = d.id
    WHERE d.depth < 10
)
SELECT id, name, depth FROM descendants ORDER BY depth, id;
-- 期望结果: 1(depth=0), 2,3(depth=1), 4,5,6(depth=2)

-- 测试1.4: 递归查询所有祖先
SELECT 'Test 1.4: All ancestors of Grandchild A1' AS test_name;
WITH RECURSIVE ancestors AS (
    SELECT id, name, parent_id, 0 AS depth
    FROM categories_adj
    WHERE id = 4
    
    UNION ALL
    
    SELECT c.id, c.name, c.parent_id, a.depth + 1
    FROM categories_adj c
    INNER JOIN ancestors a ON a.parent_id = c.id
)
SELECT id, name, depth FROM ancestors ORDER BY depth;
-- 期望结果: 4(depth=0), 2(depth=1), 1(depth=2)

-- 清理
DROP TABLE categories_adj;

-- ============================================================
-- 测试二：路径枚举模型测试
-- ============================================================

-- 创建测试表
CREATE TABLE IF NOT EXISTS categories_path (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    path TEXT NOT NULL UNIQUE
);

-- 插入测试数据
INSERT INTO categories_path (id, name, path) VALUES
    (1, 'Root', '1'),
    (2, 'Child A', '1/2'),
    (3, 'Child B', '1/3'),
    (4, 'Grandchild A1', '1/2/4'),
    (5, 'Grandchild A2', '1/2/5'),
    (6, 'Grandchild B1', '1/3/6');

-- 测试2.1: 查询所有子孙节点
SELECT 'Test 2.1: All descendants of Root' AS test_name;
SELECT * FROM categories_path
WHERE path LIKE '1/%' OR id = 1;
-- 期望结果: 所有6条记录

-- 测试2.2: 查询直接子节点
SELECT 'Test 2.2: Direct children of Child A' AS test_name;
SELECT * FROM categories_path
WHERE path LIKE '1/2/%'
  AND path NOT LIKE '1/2/%/%';
-- 期望结果: 4, 5

-- 测试2.3: 查询所有祖先
SELECT 'Test 2.3: All ancestors of Grandchild A1' AS test_name;
SELECT * FROM categories_path
WHERE '1/2/4' LIKE path || '%'
ORDER BY LENGTH(path);
-- 期望结果: 1, 2, 4

-- 测试2.4: 计算深度
SELECT 'Test 2.4: Calculate depth' AS test_name;
SELECT id, name, path,
       (LENGTH(path) - LENGTH(REPLACE(path, '/', ''))) AS depth
FROM categories_path
ORDER BY id;
-- 期望结果: 1(depth=0), 2,3(depth=1), 4,5,6(depth=2)

-- 清理
DROP TABLE categories_path;

-- ============================================================
-- 测试三：嵌套集模型测试
-- ============================================================

-- 创建测试表
CREATE TABLE IF NOT EXISTS categories_nested (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    lft INTEGER NOT NULL UNIQUE,
    rgt INTEGER NOT NULL UNIQUE
);

-- 插入测试数据
-- 树形结构:
-- Root (lft=1, rgt=12)
--   Child A (lft=2, rgt=7)
--     Grandchild A1 (lft=3, rgt=4)
--     Grandchild A2 (lft=5, rgt=6)
--   Child B (lft=8, rgt=11)
--     Grandchild B1 (lft=9, rgt=10)

INSERT INTO categories_nested (id, name, lft, rgt) VALUES
    (1, 'Root', 1, 12),
    (2, 'Child A', 2, 7),
    (3, 'Child B', 8, 11),
    (4, 'Grandchild A1', 3, 4),
    (5, 'Grandchild A2', 5, 6),
    (6, 'Grandchild B1', 9, 10);

-- 测试3.1: 查询所有子孙节点
SELECT 'Test 3.1: All descendants of Root' AS test_name;
SELECT child.id, child.name
FROM categories_nested AS parent
JOIN categories_nested AS child ON child.lft BETWEEN parent.lft AND parent.rgt
WHERE parent.id = 1
ORDER BY child.lft;
-- 期望结果: 所有6条记录

-- 测试3.2: 查询所有祖先
SELECT 'Test 3.2: All ancestors of Grandchild A1' AS test_name;
SELECT parent.id, parent.name
FROM categories_nested AS node
JOIN categories_nested AS parent ON node.lft BETWEEN parent.lft AND parent.rgt
WHERE node.id = 4
ORDER BY parent.lft;
-- 期望结果: 1, 2, 4

-- 测试3.3: 获取直接子节点
SELECT 'Test 3.3: Direct children of Root' AS test_name;
SELECT child.id, child.name
FROM categories_nested AS parent
JOIN categories_nested AS child ON child.lft > parent.lft AND child.rgt < parent.rgt
WHERE parent.id = 1
  AND NOT EXISTS (
      SELECT 1 FROM categories_nested AS mid
      WHERE mid.lft > parent.lft AND mid.rgt < parent.rgt
        AND child.lft > mid.lft AND child.rgt < mid.rgt
  )
ORDER BY child.lft;
-- 期望结果: 2, 3

-- 测试3.4: 计算子树大小
SELECT 'Test 3.4: Subtree size' AS test_name;
SELECT id, name, (rgt - lft + 1) / 2 AS subtree_size
FROM categories_nested
ORDER BY id;
-- 期望结果: 1(6), 2(3), 3(2), 4(1), 5(1), 6(1)

-- 测试3.5: 计算节点深度
SELECT 'Test 3.5: Calculate depth' AS test_name;
SELECT node.id, node.name, COUNT(parent.id) - 1 AS depth
FROM categories_nested AS node
JOIN categories_nested AS parent ON node.lft BETWEEN parent.lft AND parent.rgt
GROUP BY node.id, node.name
ORDER BY node.id;
-- 期望结果: 1(depth=0), 2,3(depth=1), 4,5,6(depth=2)

-- 测试3.6: 检查叶子节点
SELECT 'Test 3.6: Check leaf nodes' AS test_name;
SELECT id, name,
       CASE WHEN rgt = lft + 1 THEN 'Yes' ELSE 'No' END AS is_leaf
FROM categories_nested
ORDER BY id;
-- 期望结果: 4,5,6 是叶子节点

-- 清理
DROP TABLE categories_nested;

-- ============================================================
-- 测试四：闭包表模型测试
-- ============================================================

-- 创建测试表
CREATE TABLE IF NOT EXISTS categories_closure (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS category_closure (
    ancestor_id INTEGER NOT NULL,
    descendant_id INTEGER NOT NULL,
    depth INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (ancestor_id, descendant_id),
    FOREIGN KEY (ancestor_id) REFERENCES categories_closure(id),
    FOREIGN KEY (descendant_id) REFERENCES categories_closure(id)
);

-- 插入测试数据
-- 节点数据
INSERT INTO categories_closure (id, name) VALUES
    (1, 'Root'),
    (2, 'Child A'),
    (3, 'Child B'),
    (4, 'Grandchild A1'),
    (5, 'Grandchild A2'),
    (6, 'Grandchild B1');

-- 闭包关系数据 (ancestor_id, descendant_id, depth)
INSERT INTO category_closure (ancestor_id, descendant_id, depth) VALUES
    (1, 1, 0),  -- Root 自引用
    (2, 2, 0),  -- Child A 自引用
    (3, 3, 0),  -- Child B 自引用
    (4, 4, 0),  -- Grandchild A1 自引用
    (5, 5, 0),  -- Grandchild A2 自引用
    (6, 6, 0),  -- Grandchild B1 自引用
    (1, 2, 1),  -- Root -> Child A
    (1, 3, 1),  -- Root -> Child B
    (2, 4, 1),  -- Child A -> Grandchild A1
    (2, 5, 1),  -- Child A -> Grandchild A2
    (3, 6, 1),  -- Child B -> Grandchild B1
    (1, 4, 2),  -- Root -> Grandchild A1
    (1, 5, 2),  -- Root -> Grandchild A2
    (1, 6, 2);  -- Root -> Grandchild B1

-- 测试4.1: 查询所有子孙节点
SELECT 'Test 4.1: All descendants of Root' AS test_name;
SELECT c.id, c.name, cc.depth
FROM categories_closure c
JOIN category_closure cc ON c.id = cc.descendant_id
WHERE cc.ancestor_id = 1
ORDER BY cc.depth, c.id;
-- 期望结果: 所有6条记录，depth从0到2

-- 测试4.2: 查询所有祖先
SELECT 'Test 4.2: All ancestors of Grandchild A1' AS test_name;
SELECT c.id, c.name, cc.depth
FROM categories_closure c
JOIN category_closure cc ON c.id = cc.ancestor_id
WHERE cc.descendant_id = 4
ORDER BY cc.depth DESC;
-- 期望结果: 4(depth=0), 2(depth=1), 1(depth=2)

-- 测试4.3: 获取直接子节点
SELECT 'Test 4.3: Direct children of Root' AS test_name;
SELECT c.id, c.name
FROM categories_closure c
JOIN category_closure cc ON c.id = cc.descendant_id
WHERE cc.ancestor_id = 1 AND cc.depth = 1
ORDER BY c.id;
-- 期望结果: 2, 3

-- 测试4.4: 获取根节点
SELECT 'Test 4.4: Get root nodes' AS test_name;
SELECT c.*
FROM categories_closure c
WHERE c.id NOT IN (SELECT descendant_id FROM category_closure WHERE depth = 1);
-- 期望结果: 1 (Root)

-- 测试4.5: 检查叶子节点
SELECT 'Test 4.5: Check leaf nodes' AS test_name;
SELECT c.id, c.name,
       CASE WHEN NOT EXISTS (SELECT 1 FROM category_closure WHERE ancestor_id = c.id AND depth = 1)
            THEN 'Yes' ELSE 'No' END AS is_leaf
FROM categories_closure c
ORDER BY c.id;
-- 期望结果: 4,5,6 是叶子节点

-- 清理
DROP TABLE category_closure;
DROP TABLE categories_closure;

-- ============================================================
-- 测试总结
-- ============================================================
SELECT '========================================' AS summary;
SELECT 'All tests completed!' AS summary;
SELECT 'Four hierarchy models tested:' AS summary;
SELECT '1. Adjacency List - Simple, recursive queries needed' AS summary;
SELECT '2. Path Enumeration - Fast subtree queries' AS summary;
SELECT '3. Nested Set - Fast reads, slow writes' AS summary;
SELECT '4. Closure Table - Most flexible, larger storage' AS summary;