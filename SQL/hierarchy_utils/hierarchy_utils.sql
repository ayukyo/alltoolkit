-- ============================================================
-- Hierarchy Utils - 层级数据查询工具集
-- ============================================================
-- 用于处理树形结构数据的 SQL 工具集合
-- 支持多种层级模型：邻接表、路径枚举、嵌套集、闭包表
-- 零外部依赖，纯 SQL 实现
-- ============================================================

-- ============================================================
-- 一、邻接表模型 (Adjacency List)
-- 最简单的层级模型，每条记录存储父节点ID
-- ============================================================

-- 创建邻接表示例表
-- CREATE TABLE categories_adjacency (
--     id INT PRIMARY KEY,
--     name VARCHAR(100) NOT NULL,
--     parent_id INT NULL,
--     FOREIGN KEY (parent_id) REFERENCES categories_adjacency(id)
-- );

-- 递归查询：获取所有子孙节点 (MySQL 8.0+, PostgreSQL, SQLite)
-- WITH RECURSIVE descendants AS (
--     SELECT id, name, parent_id, 0 AS depth, CAST(id AS CHAR(1000)) AS path
--     FROM categories_adjacency
--     WHERE id = ?  -- 起始节点
--     
--     UNION ALL
--     
--     SELECT c.id, c.name, c.parent_id, d.depth + 1,
--            CONCAT(d.path, '->', c.id)
--     FROM categories_adjacency c
--     INNER JOIN descendants d ON c.parent_id = d.id
--     WHERE d.depth < 10  -- 限制深度防止无限循环
-- )
-- SELECT * FROM descendants ORDER BY depth, name;

-- 递归查询：获取所有祖先节点
-- WITH RECURSIVE ancestors AS (
--     SELECT id, name, parent_id, 0 AS depth
--     FROM categories_adjacency
--     WHERE id = ?  -- 起始节点
--     
--     UNION ALL
--     
--     SELECT c.id, c.name, c.parent_id, a.depth + 1
--     FROM categories_adjacency c
--     INNER JOIN ancestors a ON a.parent_id = c.id
-- )
-- SELECT * FROM ancestors ORDER BY depth DESC;

-- ============================================================
-- 二、路径枚举模型 (Path Enumeration / Materialized Path)
-- 每条记录存储从根到当前节点的完整路径
-- ============================================================

-- 创建路径枚举示例表
-- CREATE TABLE categories_path (
--     id INT PRIMARY KEY,
--     name VARCHAR(100) NOT NULL,
--     path VARCHAR(255) NOT NULL,  -- 如: '1/4/7' 或 '/root/child/grandchild'
--     UNIQUE (path)
-- );

-- 查询某节点的所有子孙
-- SELECT * FROM categories_path
-- WHERE path LIKE CONCAT((SELECT path FROM categories_path WHERE id = ?), '/%')
--    OR id = ?;

-- 查询某节点的所有祖先
-- SELECT * FROM categories_path
-- WHERE (SELECT path FROM categories_path WHERE id = ?) LIKE CONCAT(path, '%')
-- ORDER BY LENGTH(path);

-- 获取直接子节点
-- SELECT * FROM categories_path
-- WHERE path LIKE CONCAT((SELECT path FROM categories_path WHERE id = ?), '/%')
--   AND path NOT LIKE CONCAT((SELECT path FROM categories_path WHERE id = ?), '/%/%');

-- 计算节点深度
-- SELECT id, name, path,
--        (LENGTH(path) - LENGTH(REPLACE(path, '/', ''))) AS depth
-- FROM categories_path;

-- ============================================================
-- 三、嵌套集模型 (Nested Set)
-- 使用左值右值表示节点在树中的位置
-- 查询高效但插入更新复杂
-- ============================================================

-- 创建嵌套集示例表
-- CREATE TABLE categories_nested (
--     id INT PRIMARY KEY,
--     name VARCHAR(100) NOT NULL,
--     lft INT NOT NULL,
--     rgt INT NOT NULL,
--     UNIQUE (lft),
--     UNIQUE (rgt)
-- );

-- 查询某节点的所有子孙
-- SELECT child.*
-- FROM categories_nested AS parent
-- JOIN categories_nested AS child ON child.lft BETWEEN parent.lft AND parent.rgt
-- WHERE parent.id = ?;

-- 查询某节点的所有祖先
-- SELECT parent.*
-- FROM categories_nested AS node
-- JOIN categories_nested AS parent ON node.lft BETWEEN parent.lft AND parent.rgt
-- WHERE node.id = ?
-- ORDER BY parent.lft;

-- 获取直接子节点
-- SELECT child.*
-- FROM categories_nested AS parent
-- JOIN categories_nested AS child ON child.lft BETWEEN parent.lft AND parent.rgt
-- WHERE parent.id = ?
--   AND NOT EXISTS (
--       SELECT 1 FROM categories_nested AS mid
--       WHERE mid.lft BETWEEN parent.lft AND parent.rgt
--         AND child.lft BETWEEN mid.lft AND mid.rgt
--         AND mid.id != parent.id
--         AND mid.id != child.id
--   );

-- 计算子树大小
-- SELECT id, name, (rgt - lft + 1) / 2 AS subtree_size
-- FROM categories_nested;

-- 计算节点深度
-- SELECT node.id, node.name, COUNT(parent.id) AS depth
-- FROM categories_nested AS node
-- JOIN categories_nested AS parent ON node.lft BETWEEN parent.lft AND parent.rgt
-- GROUP BY node.id, node.name;

-- 插入新节点（需要更新所有受影响的左右值）
-- START TRANSACTION;
-- UPDATE categories_nested SET rgt = rgt + 2 WHERE rgt >= ?;
-- UPDATE categories_nested SET lft = lft + 2 WHERE lft >= ?;
-- INSERT INTO categories_nested (name, lft, rgt) VALUES (?, ?, ? + 1);
-- COMMIT;

-- ============================================================
-- 四、闭包表模型 (Closure Table)
-- 使用单独的关系表存储所有祖先-后代关系
-- 最灵活但存储空间较大
-- ============================================================

-- 创建闭包表示例表
-- CREATE TABLE categories (
--     id INT PRIMARY KEY,
--     name VARCHAR(100) NOT NULL
-- );

-- CREATE TABLE category_closure (
--     ancestor_id INT NOT NULL,
--     descendant_id INT NOT NULL,
--     depth INT NOT NULL DEFAULT 0,
--     PRIMARY KEY (ancestor_id, descendant_id),
--     FOREIGN KEY (ancestor_id) REFERENCES categories(id),
--     FOREIGN KEY (descendant_id) REFERENCES categories(id)
-- );

-- 查询某节点的所有子孙
-- SELECT c.*, cc.depth
-- FROM categories c
-- JOIN category_closure cc ON c.id = cc.descendant_id
-- WHERE cc.ancestor_id = ?
-- ORDER BY cc.depth;

-- 查询某节点的所有祖先
-- SELECT c.*, cc.depth
-- FROM categories c
-- JOIN category_closure cc ON c.id = cc.ancestor_id
-- WHERE cc.descendant_id = ?
-- ORDER BY cc.depth DESC;

-- 获取直接子节点
-- SELECT c.*
-- FROM categories c
-- JOIN category_closure cc ON c.id = cc.descendant_id
-- WHERE cc.ancestor_id = ? AND cc.depth = 1;

-- 获取根节点
-- SELECT c.*
-- FROM categories c
-- WHERE c.id NOT IN (SELECT descendant_id FROM category_closure WHERE depth = 1);

-- 插入新节点（需要添加所有闭包关系）
-- INSERT INTO categories (id, name) VALUES (?, ?);
-- INSERT INTO category_closure (ancestor_id, descendant_id, depth)
-- SELECT ancestor_id, ?, depth + 1 FROM category_closure WHERE descendant_id = ?
-- UNION ALL SELECT ?, ?, 0;  -- 自引用

-- 删除节点及其所有子孙
-- DELETE FROM categories WHERE id IN (
--     SELECT descendant_id FROM category_closure WHERE ancestor_id = ?
-- );

-- ============================================================
-- 五、常用层级操作函数
-- ============================================================

-- 通用：检查是否为叶子节点（邻接表）
-- SELECT c.*, 
--        NOT EXISTS (SELECT 1 FROM categories_adjacency WHERE parent_id = c.id) AS is_leaf
-- FROM categories_adjacency c;

-- 通用：获取节点层级路径（邻接表递归）
-- WITH RECURSIVE node_path AS (
--     SELECT id, name, parent_id, CAST(name AS CHAR(1000)) AS full_path
--     FROM categories_adjacency
--     WHERE id = ?
--     
--     UNION ALL
--     
--     SELECT c.id, c.name, c.parent_id, CONCAT(c.name, ' > ', np.full_path)
--     FROM categories_adjacency c
--     INNER JOIN node_path np ON np.parent_id = c.id
-- )
-- SELECT full_path FROM node_path WHERE parent_id IS NULL;

-- 通用：层级排序（邻接表）
-- WITH RECURSIVE sorted_tree AS (
--     SELECT id, name, parent_id, 0 AS depth,
--            CAST(name AS CHAR(1000)) AS sort_path
--     FROM categories_adjacency
--     WHERE parent_id IS NULL
--     
--     UNION ALL
--     
--     SELECT c.id, c.name, c.parent_id, st.depth + 1,
--            CONCAT(st.sort_path, ' > ', c.name)
--     FROM categories_adjacency c
--     INNER JOIN sorted_tree st ON c.parent_id = st.id
-- )
-- SELECT * FROM sorted_tree ORDER BY sort_path;

-- ============================================================
-- 六、树形数据迁移工具
-- ============================================================

-- 邻接表 -> 闭包表
-- INSERT INTO category_closure (ancestor_id, descendant_id, depth)
-- WITH RECURSIVE closure AS (
--     SELECT id AS ancestor_id, id AS descendant_id, 0 AS depth
--     FROM categories_adjacency
--     
--     UNION ALL
--     
--     SELECT c.ancestor_id, n.id, c.depth + 1
--     FROM closure c
--     JOIN categories_adjacency n ON n.parent_id = c.descendant_id
-- )
-- SELECT * FROM closure;

-- 邻接表 -> 路径枚举
-- UPDATE categories_path cp
-- SET path = (
--     WITH RECURSIVE path_builder AS (
--         SELECT id, CAST(id AS CHAR(1000)) AS path
--         FROM categories_adjacency
--         WHERE parent_id IS NULL
--         
--         UNION ALL
--         
--         SELECT ca.id, CONCAT(pb.path, '/', ca.id)
--         FROM categories_adjacency ca
--         JOIN path_builder pb ON ca.parent_id = pb.id
--     )
--     SELECT path FROM path_builder WHERE id = cp.id
-- );

-- ============================================================
-- 七、性能优化建议
-- ============================================================

-- 为邻接表创建索引
-- CREATE INDEX idx_parent_id ON categories_adjacency(parent_id);

-- 为路径枚举创建索引
-- CREATE INDEX idx_path ON categories_path(path);

-- 为嵌套集创建索引
-- CREATE INDEX idx_lft ON categories_nested(lft);
-- CREATE INDEX idx_rgt ON categories_nested(rgt);
-- CREATE INDEX idx_lft_rgt ON categories_nested(lft, rgt);

-- 为闭包表创建索引
-- CREATE INDEX idx_ancestor ON category_closure(ancestor_id);
-- CREATE INDEX idx_descendant ON category_closure(descendant_id);
-- CREATE INDEX idx_depth ON category_closure(depth);

-- ============================================================
-- 八、实际应用场景示例
-- ============================================================

-- 场景1：组织架构图
-- 查询某员工的所有下属
-- WITH RECURSIVE subordinates AS (
--     SELECT id, name, manager_id, 0 AS level
--     FROM employees
--     WHERE id = ?
--     
--     UNION ALL
--     
--     SELECT e.id, e.name, e.manager_id, s.level + 1
--     FROM employees e
--     INNER JOIN subordinates s ON e.manager_id = s.id
-- )
-- SELECT * FROM subordinates;

-- 场景2：评论回复树
-- 查询某评论的所有回复
-- WITH RECURSIVE replies AS (
--     SELECT id, content, parent_comment_id, created_at, 0 AS depth
--     FROM comments
--     WHERE id = ?
--     
--     UNION ALL
--     
--     SELECT c.id, c.content, c.parent_comment_id, c.created_at, r.depth + 1
--     FROM comments c
--     INNER JOIN replies r ON c.parent_comment_id = r.id
-- )
-- SELECT * FROM replies ORDER BY created_at;

-- 场景3：菜单权限检查
-- 检查用户是否有权限访问某菜单（包含父菜单权限）
-- SELECT m.*
-- FROM menus m
-- WHERE m.id IN (
--     SELECT menu_id FROM user_menu_permissions WHERE user_id = ?
-- )
-- OR EXISTS (
--     SELECT 1 FROM menus parent
--     WHERE parent.id = m.parent_id
--     AND parent.id IN (SELECT menu_id FROM user_menu_permissions WHERE user_id = ?)
-- );