# Hierarchy Utils - SQL 层级数据查询工具集

一个用于处理树形结构数据的 SQL 工具集合，支持四种主流层级模型，零外部依赖。

## 支持的层级模型

### 1. 邻接表模型 (Adjacency List)
- **原理**: 每条记录存储父节点ID
- **优点**: 简单直观，插入/删除/移动操作简单
- **缺点**: 查询所有子孙/祖先需要递归（MySQL 8.0+, PostgreSQL, SQLite支持）
- **适合**: 层级不深、读写平衡的场景

### 2. 路径枚举模型 (Path Enumeration)
- **原理**: 每条记录存储从根到当前节点的完整路径
- **优点**: 查询子孙节点非常快，无需递归
- **缺点**: 插入/移动节点需要更新多条记录
- **适合**: 层级有限、需要显示完整路径的场景

### 3. 嵌套集模型 (Nested Set)
- **原理**: 使用左值右值表示节点在树中的位置
- **优点**: 查询速度极快，无需递归
- **缺点**: 插入/删除/移动操作复杂，需要更新大量记录
- **适合**: 读多写少、层级深的场景

### 4. 闭包表模型 (Closure Table)
- **原理**: 使用单独的关系表存储所有祖先-后代关系
- **优点**: 查询最灵活，支持复杂层级查询
- **缺点**: 存储空间较大，维护关系表有额外开销
- **适合**: 查询复杂、需要灵活操作的场景

## 文件结构

```
SQL/hierarchy_utils/
├── hierarchy_utils.sql      # 主工具文件（包含所有模型的SQL模板）
├── hierarchy_utils_test.sql # 测试文件（SQLite语法，兼容MySQL 8.0+、PostgreSQL）
├── usage_examples.sql        # 使用示例（5个实际场景）
└── README.md               # 说明文档
```

## 核心功能

### 通用层级操作
- 查询所有子孙节点
- 查询所有祖先节点
- 获取直接子节点
- 获取根节点
- 检查叶子节点
- 计算节点深度
- 获取节点路径（面包屑导航）
- 层级排序

### 数据迁移工具
- 邻接表 → 闭包表
- 邻接表 → 路径枚举

## 使用示例

### 邻接表 - 查询所有子孙
```sql
WITH RECURSIVE descendants AS (
    SELECT id, name, parent_id, 0 AS depth
    FROM categories
    WHERE id = ?  -- 起始节点
    
    UNION ALL
    
    SELECT c.id, c.name, c.parent_id, d.depth + 1
    FROM categories c
    INNER JOIN descendants d ON c.parent_id = d.id
    WHERE d.depth < 10
)
SELECT * FROM descendants ORDER BY depth;
```

### 嵌套集 - 查询子树
```sql
SELECT child.*
FROM categories AS parent
JOIN categories AS child ON child.lft BETWEEN parent.lft AND parent.rgt
WHERE parent.id = ?;
```

### 闭包表 - 权限检查
```sql
SELECT * FROM menus
WHERE id IN (
    SELECT descendant_id FROM menu_closure
    WHERE ancestor_id IN (SELECT menu_id FROM user_roles WHERE user_id = ?)
);
```

## 实际应用场景

1. **商品分类系统** - 多级分类导航、面包屑
2. **组织架构系统** - 部门层级、审批流程
3. **评论回复系统** - 嵌套评论、引用回复
4. **权限菜单系统** - 菜单树、权限继承
5. **多语言分类系统** - 多语言支持的分类树

## 性能优化

```sql
-- 邻接表索引
CREATE INDEX idx_parent_id ON categories(parent_id);

-- 路径枚举索引
CREATE INDEX idx_path ON categories_path(path);

-- 嵌套集索引
CREATE INDEX idx_lft_rgt ON categories(lft, rgt);

-- 闭包表索引
CREATE INDEX idx_closure_ancestor ON closure(ancestor_id);
CREATE INDEX idx_closure_descendant ON closure(descendant_id);
```

## 模型选择指南

| 特性 | 邻接表 | 路径枚举 | 嵌套集 | 闭包表 |
|------|--------|----------|--------|--------|
| 查询子节点 | 简单 | 简单 | 简单 | 简单 |
| 查询子孙 | 递归 | 简单 | 简单 | 简单 |
| 查询祖先 | 递归 | 简单 | 简单 | 简单 |
| 插入节点 | 简单 | 中等 | 复杂 | 中等 |
| 删除节点 | 简单 | 中等 | 复杂 | 简单 |
| 移动子树 | 简单 | 复杂 | 复杂 | 中等 |
| 存储空间 | 小 | 小 | 小 | 大 |
| 推荐场景 | 读写平衡 | 路径展示 | 读多写少 | 复杂查询 |

## 数据库兼容性

- ✅ SQLite 3.8.3+（支持 WITH RECURSIVE）
- ✅ MySQL 8.0+（支持 WITH RECURSIVE）
- ✅ PostgreSQL 8.4+（原生支持）
- ✅ SQL Server 2008+（原生支持）
- ✅ Oracle 11g R2+（原生支持）

## 测试

```bash
# SQLite 测试
sqlite3 :memory: < hierarchy_utils_test.sql

# MySQL 测试
mysql -u root -p test < hierarchy_utils_test.sql

# PostgreSQL 测试
psql -d test -f hierarchy_utils_test.sql
```

## 日期

- 创建日期: 2026-05-14
- 版本: 1.0.0