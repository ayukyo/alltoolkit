-- ============================================================
-- Hierarchy Utils 使用示例
-- ============================================================
-- 展示四种层级模型在实际场景中的应用
-- 使用 SQLite 语法（兼容 MySQL 8.0+, PostgreSQL）
-- ============================================================

-- ============================================================
-- 场景一：电商商品分类系统（邻接表模型）
-- ============================================================
-- 特点：简单直观，适合层级不深、读少写多的场景

CREATE TABLE IF NOT EXISTS product_categories (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    parent_id INTEGER,
    sort_order INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (parent_id) REFERENCES product_categories(id)
);

-- 示例数据：电子产品分类
INSERT INTO product_categories (id, name, parent_id, sort_order) VALUES
    (1, '电子产品', NULL, 1),
    (2, '手机通讯', 1, 1),
    (3, '电脑办公', 1, 2),
    (4, '智能设备', 1, 3),
    (5, '智能手机', 2, 1),
    (6, '功能手机', 2, 2),
    (7, '笔记本电脑', 3, 1),
    (8, '台式电脑', 3, 2),
    (9, '智能手表', 4, 1),
    (10, '智能耳机', 4, 2);

-- 示例1.1: 获取导航菜单（多级分类）
-- 只获取前两级分类
WITH RECURSIVE menu_tree AS (
    SELECT id, name, parent_id, 0 AS depth,
           CAST(name AS TEXT) AS path
    FROM product_categories
    WHERE parent_id IS NULL
    
    UNION ALL
    
    SELECT c.id, c.name, c.parent_id, mt.depth + 1,
           mt.path || ' > ' || c.name
    FROM product_categories c
    INNER JOIN menu_tree mt ON c.parent_id = mt.id
    WHERE mt.depth < 1  -- 只获取两级
)
SELECT * FROM menu_tree ORDER BY path;

-- 示例1.2: 获取某分类的所有上级分类路径（面包屑导航）
WITH RECURSIVE breadcrumbs AS (
    SELECT id, name, parent_id, CAST(name AS TEXT) AS full_path
    FROM product_categories
    WHERE id = 7  -- 笔记本电脑
    
    UNION ALL
    
    SELECT p.id, p.name, p.parent_id, p.name || ' > ' || b.full_path
    FROM product_categories p
    INNER JOIN breadcrumbs b ON b.parent_id = p.id
)
SELECT full_path FROM breadcrumbs WHERE parent_id IS NULL;
-- 结果: 电子产品 > 电脑办公 > 笔记本电脑

-- 示例1.3: 获取某分类及其所有子分类的ID列表（用于商品筛选）
WITH RECURSIVE category_tree AS (
    SELECT id FROM product_categories WHERE id = 2  -- 手机通讯
    UNION ALL
    SELECT c.id FROM product_categories c
    INNER JOIN category_tree ct ON c.parent_id = ct.id
)
SELECT GROUP_CONCAT(id) AS category_ids FROM category_tree;
-- 结果: 2,5,6

-- ============================================================
-- 场景二：组织架构系统（嵌套集模型）
-- ============================================================
-- 特点：读取速度快，适合层级深、读多写少的场景

CREATE TABLE IF NOT EXISTS departments (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    lft INTEGER NOT NULL,
    rgt INTEGER NOT NULL,
    manager_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 示例数据：公司组织架构
-- 使用嵌套集表示：
-- 公司 (1, 14)
--   技术部 (2, 7)
--     前端组 (3, 4)
--     后端组 (5, 6)
--   市场部 (8, 11)
--     销售组 (9, 10)
--   财务部 (12, 13)

INSERT INTO departments (id, name, lft, rgt) VALUES
    (1, '公司总部', 1, 14),
    (2, '技术部', 2, 7),
    (3, '前端组', 3, 4),
    (4, '后端组', 5, 6),
    (5, '市场部', 8, 11),
    (6, '销售组', 9, 10),
    (7, '财务部', 12, 13);

-- 示例2.1: 获取某部门的所有下级部门（用于权限检查）
SELECT d.id, d.name, (d.rgt - d.lft + 1) / 2 AS subtree_size
FROM departments d
WHERE d.lft BETWEEN (SELECT lft FROM departments WHERE id = 2) 
                AND (SELECT rgt FROM departments WHERE id = 2)
ORDER BY d.lft;
-- 结果: 技术部, 前端组, 后端组

-- 示例2.2: 获取某部门的所有上级部门（用于审批流程）
SELECT parent.id, parent.name
FROM departments AS node
JOIN departments AS parent ON node.lft BETWEEN parent.lft AND parent.rgt
WHERE node.id = 3  -- 前端组
ORDER BY parent.lft;
-- 结果: 公司总部, 技术部, 前端组

-- 示例2.3: 获取组织架构树（带深度）
SELECT node.id, node.name,
       COUNT(parent.id) - 1 AS depth,
       PRINTF('%*s%s', (COUNT(parent.id) - 1) * 2, '', node.name) AS tree_view
FROM departments AS node
JOIN departments AS parent ON node.lft BETWEEN parent.lft AND parent.rgt
GROUP BY node.id
ORDER BY node.lft;
-- 结果: 树形结构视图

-- 示例2.4: 统计各部门的直属下级数量
SELECT parent.id, parent.name,
       (COUNT(child.id) - 1) AS direct_children_count
FROM departments AS parent
LEFT JOIN departments AS child ON child.lft BETWEEN parent.lft AND parent.rgt
WHERE child.lft = parent.lft + 1 
   OR (child.lft > parent.lft + 1 AND NOT EXISTS (
       SELECT 1 FROM departments mid 
       WHERE mid.lft > parent.lft AND mid.rgt < parent.rgt
       AND child.lft > mid.lft AND child.rgt < mid.rgt
   ))
GROUP BY parent.id
ORDER BY parent.lft;

-- ============================================================
-- 场景三：评论回复系统（路径枚举模型）
-- ============================================================
-- 特点：查询路径简单，适合层级有限、需要显示完整路径的场景

CREATE TABLE IF NOT EXISTS comments (
    id INTEGER PRIMARY KEY,
    post_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    content TEXT NOT NULL,
    path TEXT NOT NULL,  -- 格式: 1/2/5 表示ID为5的评论，父路径是1/2
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (path)
);

-- 示例数据：帖子评论
INSERT INTO comments (id, post_id, user_id, content, path) VALUES
    (1, 100, 1, '这篇文章写得很好！', '1'),
    (2, 100, 2, '同意楼上！', '1/2'),
    (3, 100, 3, '我也觉得不错', '1/3'),
    (4, 100, 1, '谢谢支持', '1/2/4'),
    (5, 100, 4, '有不同意见...', '5'),
    (6, 100, 2, '愿闻其详', '5/6');

-- 示例3.1: 获取评论及其所有回复（树形显示）
SELECT id, user_id, content, path,
       (LENGTH(path) - LENGTH(REPLACE(path, '/', ''))) AS depth,
       SUBSTR('      ', 1, (LENGTH(path) - LENGTH(REPLACE(path, '/', ''))) * 2) || content AS tree_display
FROM comments
WHERE post_id = 100
ORDER BY path;
-- 结果: 按路径排序的树形评论

-- 示例3.2: 获取某条评论的所有上级评论（引用回复）
SELECT * FROM comments
WHERE (SELECT path FROM comments WHERE id = 4) LIKE path || '%'
ORDER BY LENGTH(path);
-- 结果: 1 -> 2 -> 4 的评论链

-- 示例3.3: 添加新评论（需要计算路径）
-- 假设要回复评论ID=4，新评论ID=7
-- INSERT INTO comments (id, post_id, user_id, content, path)
-- SELECT 7, 100, 5, '新增回复', 
--        (SELECT path FROM comments WHERE id = 4) || '/7';

-- 示例3.4: 统计每条评论的回复数量
SELECT parent.id, parent.content,
       (SELECT COUNT(*) FROM comments child 
        WHERE child.path LIKE parent.path || '/%') AS reply_count
FROM comments parent
ORDER BY parent.id;

-- ============================================================
-- 场景四：权限菜单系统（闭包表模型）
-- ============================================================
-- 特点：查询灵活，适合复杂的层级权限控制

CREATE TABLE IF NOT EXISTS menus (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    url TEXT,
    icon TEXT,
    sort_order INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS menu_closure (
    ancestor_id INTEGER NOT NULL,
    descendant_id INTEGER NOT NULL,
    depth INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (ancestor_id, descendant_id),
    FOREIGN KEY (ancestor_id) REFERENCES menus(id),
    FOREIGN KEY (descendant_id) REFERENCES menus(id)
);

CREATE TABLE IF NOT EXISTS role_menu (
    role_id INTEGER NOT NULL,
    menu_id INTEGER NOT NULL,
    PRIMARY KEY (role_id, menu_id)
);

-- 示例数据：后台管理菜单
INSERT INTO menus (id, name, url, icon, sort_order) VALUES
    (1, '系统管理', NULL, 'setting', 1),
    (2, '用户管理', '/system/user', 'user', 1),
    (3, '角色管理', '/system/role', 'role', 2),
    (4, '菜单管理', '/system/menu', 'menu', 3),
    (5, '日志管理', '/system/log', 'log', 4),
    (6, '操作日志', '/system/log/operation', NULL, 1),
    (7, '登录日志', '/system/log/login', NULL, 2);

-- 菜单闭包关系
INSERT INTO menu_closure (ancestor_id, descendant_id, depth) VALUES
    (1, 1, 0), (2, 2, 0), (3, 3, 0), (4, 4, 0), (5, 5, 0), (6, 6, 0), (7, 7, 0),
    (1, 2, 1), (1, 3, 1), (1, 4, 1), (1, 5, 1),
    (5, 6, 1), (5, 7, 1),
    (1, 6, 2), (1, 7, 2);

-- 角色权限数据
INSERT INTO role_menu (role_id, menu_id) VALUES
    (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7),  -- 管理员：所有菜单
    (2, 1), (2, 2), (2, 5), (2, 6);  -- 普通用户：部分菜单

-- 示例4.1: 获取用户可访问的所有菜单（包含上级菜单）
WITH user_menus AS (
    SELECT DISTINCT m.id, m.name, m.url, m.icon, m.sort_order
    FROM menus m
    WHERE m.id IN (SELECT menu_id FROM role_menu WHERE role_id = 2)  -- 用户角色ID
       OR m.id IN (
           SELECT ancestor_id FROM menu_closure
           WHERE descendant_id IN (SELECT menu_id FROM role_menu WHERE role_id = 2)
       )
)
SELECT um.id, um.name, um.url, um.icon,
       COALESCE(mc.depth, 0) AS depth
FROM user_menus um
LEFT JOIN menu_closure mc ON mc.descendant_id = um.id AND mc.ancestor_id = um.id
                           OR mc.ancestor_id != mc.descendant_id
GROUP BY um.id
ORDER BY um.sort_order;
-- 结果: 用户可访问的菜单树

-- 示例4.2: 检查用户是否有某个菜单的权限（包含父菜单权限）
SELECT CASE WHEN EXISTS (
    SELECT 1 FROM role_menu rm
    JOIN menu_closure mc ON rm.menu_id = mc.ancestor_id
    WHERE rm.role_id = 2 AND mc.descendant_id = 6  -- 检查操作日志权限
) THEN '有权限' ELSE '无权限' END AS has_permission;
-- 结果: 有权限（因为角色2有菜单5的权限，而菜单6是菜单5的子菜单）

-- 示例4.3: 获取菜单树结构（带深度）
SELECT m.id, m.name, m.url,
       mc.depth,
       PRINTF('%*s%s', mc.depth * 2, '', m.name) AS tree_view
FROM menus m
JOIN menu_closure mc ON m.id = mc.descendant_id AND mc.ancestor_id = 1
ORDER BY m.sort_order, mc.depth;
-- 结果: 树形菜单结构

-- 示例4.4: 批量删除菜单及其所有子菜单
-- 删除"日志管理"及其子菜单
-- DELETE FROM menus WHERE id IN (
--     SELECT descendant_id FROM menu_closure WHERE ancestor_id = 5
-- );
-- DELETE FROM menu_closure WHERE descendant_id IN (SELECT id FROM menus WHERE ...);

-- ============================================================
-- 场景五：多语言分类系统（混合模型）
-- ============================================================
-- 使用邻接表 + 闭包表的混合方案，兼顾性能和灵活性

CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY,
    parent_id INTEGER,
    name TEXT NOT NULL,
    slug TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS category_translations (
    category_id INTEGER NOT NULL,
    language_code TEXT NOT NULL,
    name TEXT NOT NULL,
    PRIMARY KEY (category_id, language_code)
);

CREATE TABLE IF NOT EXISTS category_paths (
    ancestor_id INTEGER NOT NULL,
    descendant_id INTEGER NOT NULL,
    depth INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (ancestor_id, descendant_id)
);

-- 示例数据
INSERT INTO categories (id, parent_id, name, slug) VALUES
    (1, NULL, 'Electronics', 'electronics'),
    (2, 1, 'Phones', 'phones'),
    (3, 1, 'Computers', 'computers');

INSERT INTO category_translations (category_id, language_code, name) VALUES
    (1, 'zh', '电子产品'),
    (1, 'ja', '電子機器'),
    (2, 'zh', '手机'),
    (2, 'ja', '携帯電話'),
    (3, 'zh', '电脑'),
    (3, 'ja', 'コンピュータ');

INSERT INTO category_paths (ancestor_id, descendant_id, depth) VALUES
    (1, 1, 0), (2, 2, 0), (3, 3, 0),
    (1, 2, 1), (1, 3, 1);

-- 示例5.1: 获取某语言下的分类树
SELECT c.id, COALESCE(ct.name, c.name) AS name, c.slug, cp.depth
FROM categories c
LEFT JOIN category_translations ct ON c.id = ct.category_id AND ct.language_code = 'zh'
JOIN category_paths cp ON c.id = cp.descendant_id AND cp.ancestor_id = 1
ORDER BY cp.depth, c.id;
-- 结果: 中文分类树

-- ============================================================
-- 性能优化建议
-- ============================================================

-- 1. 为邻接表创建索引
-- CREATE INDEX idx_parent_id ON categories(parent_id);

-- 2. 为路径枚举创建前缀索引
-- CREATE INDEX idx_path ON categories_path(path);

-- 3. 为嵌套集创建索引
-- CREATE INDEX idx_lft_rgt ON departments(lft, rgt);

-- 4. 为闭包表创建索引
-- CREATE INDEX idx_closure_ancestor ON menu_closure(ancestor_id);
-- CREATE INDEX idx_closure_descendant ON menu_closure(descendant_id);
-- CREATE INDEX idx_closure_depth ON menu_closure(depth);

-- 5. 使用物化视图（如果支持）
-- CREATE MATERIALIZED VIEW category_tree AS
-- WITH RECURSIVE tree AS (...)
-- SELECT * FROM tree;

-- ============================================================
-- 模型选择指南
-- ============================================================
/*
+----------------+----------------+----------------+----------------+
|     特性        |    邻接表      |    嵌套集      |    闭包表      |
+----------------+----------------+----------------+----------------+
| 查询子节点      |      简单      |      简单      |      简单      |
| 查询子孙        |  需要递归      |      简单      |      简单      |
| 查询祖先        |  需要递归      |      简单      |      简单      |
| 插入节点        |      简单      |      复杂      |      中等      |
| 删除节点        |      简单      |      复杂      |      简单      |
| 移动子树        |      简单      |      复杂      |      中等      |
| 存储空间        |      小        |      小        |      大        |
| 适合场景        | 读写平衡       |   读多写少      |   查询复杂     |
+----------------+----------------+----------------+----------------+
*/