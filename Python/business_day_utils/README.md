# Business Day Utils


Business Day Utils - 零依赖工作日计算工具库

提供完整的工作日计算功能，包括：
- 工作日判断（跳过周末）
- 节假日管理
- 工作日加减计算
- 计算两个日期之间的工作日数量
- 获取下一个/上一个工作日
- 批量工作日计算
- 自定义工作日定义（支持不同国家/地区）


## 功能

### 类

- **BusinessDayError**: 工作日计算错误
- **Holiday**: 节假日定义
  方法: matches
- **BusinessDayConfig**: 工作日配置
  方法: add_holiday, add_adjusted_workday, remove_holiday
- **BusinessDayCalculator**: 工作日计算器
  方法: is_weekend, is_holiday, is_adjusted_workday, is_business_day, add_business_days ... (22 个方法)

### 函数

- **create_china_holiday_calculator(year**) - 创建中国节假日计算器（需要手动设置具体日期）
- **create_us_holiday_calculator(year**) - 创建美国节假日计算器
- **is_business_day(check_date, config**) - 判断是否为工作日（便捷函数）
- **add_business_days(start_date, days, config**) - 添加工作日（便捷函数）
- **business_days_between(start_date, end_date, config**) - 计算工作日数量（便捷函数）
- **next_business_day(from_date, config**) - 获取下一个工作日（便捷函数）
- **previous_business_day(from_date, config**) - 获取上一个工作日（便捷函数）
- **matches(self, check_date**) - 检查日期是否匹配此节假日
- **add_holiday(self, name, holiday_date**, ...) - 添加节假日
- **add_adjusted_workday(self, adj_date**) - 添加调休工作日

... 共 33 个函数

## 使用示例

```python
from mod import create_china_holiday_calculator

# 使用 create_china_holiday_calculator
result = create_china_holiday_calculator()
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
