# Json Diff Utils


json_diff_utils - JSON 差异比较工具模块

提供深度 JSON 差异比较、JSON Patch (RFC 6902) 生成与应用、
JSON Merge Patch (RFC 7396) 等功能。
零外部依赖，全部使用 Python 标准库实现。

主要功能：
- 深度 JSON 差异比较（支持嵌套对象和数组）
- 路径化差异报告（如 "user.profile.name" 发生变化）
- JSON Patch (RFC 6902) 生成与应用
- JSON Merge Patch (RFC 7396) 支持
- 差异统计与可视化
- 差异过滤与搜索

作者: AllToolkit
日期: 2026-04-20


## 功能

### 类

- **DiffOperation**: JSON Patch 操作类型 (RFC 6902)
- **ChangeType**: 变更类型
- **JsonDiff**: JSON 差异项
  方法: to_dict
- **JsonPatch**: JSON Patch 操作 (RFC 6902)
  方法: to_dict
- **DiffResult**: 差异比较结果
  方法: has_changes, filter_by_type, filter_by_path, get_path, to_dict ... (6 个方法)
- **JsonDiffer**: JSON 差异比较器
  方法: diff, diff_json_strings
- **JsonPatcher**: JSON Patch 操作器 (RFC 6902)
  方法: apply_patch, generate_patch
- **JsonMergePatch**: JSON Merge Patch (RFC 7396) 实现
  方法: apply_patch, generate_patch
- **JsonDiffVisualizer**: JSON 差异可视化工具
  方法: to_colored_text, to_markdown, to_html

### 函数

- **diff(old_json, new_json, ignore_keys**, ...) - 比较两个 JSON 对象的差异（便捷函数）
- **diff_strings(old_str, new_str**) - 比较两个 JSON 字符串的差异（便捷函数）
- **generate_patch(old_json, new_json**) - 生成 JSON Patch（便捷函数）
- **apply_patch(obj, patches**) - 应用 JSON Patch（便捷函数）
- **generate_merge_patch(old_json, new_json**) - 生成 JSON Merge Patch（便捷函数）
- **apply_merge_patch(target, patch**) - 应用 JSON Merge Patch（便捷函数）
- **to_dict(self**) - 转换为字典
- **to_dict(self**) - 转换为字典
- **has_changes(self**) - 是否有变更
- **filter_by_type(self, change_type**) - 按变更类型过滤

... 共 23 个函数

## 使用示例

```python
from mod import diff

# 使用 diff
result = diff()
```

## 测试

运行测试：

```bash
python *_test.py
```

## 文件结构

```
{module_name}/
├── mod.py              # 主模块
├── *_test.py           # 测试文件
├── README.md           # 本文档
└── examples/           # 示例代码
    └── usage_examples.py
```

---

**Last updated**: 2026-04-28
