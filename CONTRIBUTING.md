# Contributing to AllToolkit

欢迎贡献 AllToolkit！这是一个多语言通用工具库，目标是让开发者能用相同的 API 风格在不同语言中完成常见任务。

## 🚀 快速开始

### 添加新工具模块

1. **Fork 本仓库**

2. **选择语言和模块名**
   ```bash
   cd AllToolkit/{Language}/
   mkdir {module_name}
   ```

3. **创建模块文件**
   ```
   {Language}/{module_name}/
   ├── mod.{ext}              # 主模块文件
   ├── {module}_test.{ext}    # 单元测试（可选）
   └── README.md              # 模块文档（可选）
   ```

4. **创建示例代码**
   ```
   {Language}/examples/
   └── {module}_example.{ext}
   ```

5. **更新 README.md**
   - 在 "Latest Addition" 部分添加新工具说明

### 目录结构规范

```
AllToolkit/
├── {Language}/
│   ├── {module_name}/
│   │   ├── mod.{ext}
│   │   └── {module}_test.{ext}
│   ├── examples/
│   │   └── {module}_example.{ext}
│   └── README.md
└── README.md
```

## 📝 代码规范

### 通用要求

- ✅ **零依赖** - 仅使用标准库
- ✅ **完整文档** - 所有函数必须有注释
- ✅ **参数说明** - 每个参数的用途和类型
- ✅ **返回值说明** - 返回值的含义
- ✅ **使用示例** - 至少一个可运行示例
- ✅ **异常处理** - 边界情况和错误处理
- ✅ **Unicode 安全** - 正确处理多字节字符

### 注释规范

**Java/JSDoc 风格：**
```java
/**
 * 函数功能说明
 *
 * @param param1 参数说明
 * @param param2 参数说明
 * @return 返回值说明
 */
```

**Python Docstring：**
```python
def function(param1, param2):
    """
    函数功能说明
    
    Args:
        param1: 参数说明
        param2: 参数说明
    
    Returns:
        返回值说明
    """
```

**Rust Doc：**
```rust
/// 函数功能说明
///
/// # Arguments
///
/// * `param1` - 参数说明
/// * `param2` - 参数说明
///
/// # Returns
///
/// 返回值说明
pub fn function(param1: Type, param2: Type) -> Type {
```

## 🧪 测试要求

- ✅ 单元测试覆盖率 > 70%
- ✅ 包含正常场景测试
- ✅ 包含边界值测试
- ✅ 包含异常情况测试

## 📤 提交 PR

1. **创建分支**
   ```bash
   git checkout -b feat/{language}-{module_name}
   ```

2. **提交代码**
   ```bash
   git add .
   git commit -m "feat({language}): 新增 {module_name} 工具模块
   
   - 新增 {N} 个工具函数
   - 包含单元测试
   - 更新 README.md"
   ```

3. **推送到远程**
   ```bash
   git push origin feat/{language}-{module_name}
   ```

4. **创建 Pull Request**
   - 标题：`feat({language}): 新增 {module_name} 工具模块`
   - 描述：说明功能、使用场景、测试情况

## 🔍 Code Review 清单

提交前自查：

- [ ] 代码无编译错误
- [ ] 单元测试通过
- [ ] 注释完整（函数、参数、返回值）
- [ ] 示例代码可运行
- [ ] 遵循零依赖原则
- [ ] 更新了 README.md
- [ ] 无重复功能（检查现有工具）

## 💡 工具函数创意

不知道写什么？参考这些方向：

- 🔤 字符串处理（已有，可补充）
- 📁 文件操作（已有，可补充）
- 🌐 网络请求（HTTP、WebSocket）
- 🔐 加密解密（Base64、MD5、SHA、AES）
- 📊 数据格式（JSON、XML、CSV）
- 🗜️ 压缩解压（ZIP、GZIP）
- 📅 日期时间（已有，可补充）
- 🧮 数学计算（已有，可补充）
- 🎲 随机数生成
- 📱 数据验证（邮箱、手机、身份证）
- 🔄 编解码（URL、HTML、Unicode）
- 📈 数据结构（栈、队列、树、图）

## ❓ 常见问题

**Q: 可以添加第三方依赖吗？**

A: 不可以。AllToolkit 坚持零依赖原则，确保在任何环境都能直接使用。

**Q: 如果功能在其他语言已实现，还需要写吗？**

A: 需要！AllToolkit 的目标是覆盖所有主流语言，即使功能相同也要为每种语言实现。

**Q: 如何避免重复实现？**

A: 提交前先查看 README.md 和现有代码，确保功能是独特的。

**Q: 测试必须写吗？**

A: 强烈建议。单元测试能保证代码质量，也方便后续维护。

## 🙏 感谢贡献

每一位贡献者都会被记录在 README.md 的 Contributors 部分！

---

有问题？欢迎提 Issue 讨论！
