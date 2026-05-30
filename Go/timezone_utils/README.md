# Timezone Utils

时区转换和查询工具，零外部依赖，仅使用 Go 标准库。

## 功能特性

- ✅ 时区信息查询（名称、偏移量、DST状态）
- ✅ 时区间时间转换
- ✅ 时区列表（按洲分组、城市搜索）
- ✅ UTC 偏移量计算
- ✅ DST 夏令时检测
- ✅ 字符串时间格式转换
- ✅ 零外部依赖

## 安装

```bash
go get github.com/ayukyo/alltoolkit/go/timezone_utils
```

## 快速开始

```go
package main

import (
	"fmt"
	"time"
	"github.com/ayukyo/alltoolkit/go/timezone_utils"
)

func main() {
	// 获取时区信息
	info, _ := timezone_utils.GetTimezoneInfo("America/New_York")
	fmt.Printf("Offset: %s\n", info.OffsetString)  // "-04:00" (DST期间)

	// 时区转换
	nyTime := time.Date(2026, 5, 31, 12, 0, 0, 0, time.UTC)
	tokyoTime, _ := timezone_utils.Convert(nyTime, "America/New_York", "Asia/Tokyo")
	fmt.Println(tokyoTime.Format("15:04:05"))  // "01:00:00"

	// 获取当前时间
	now, _ := timezone_utils.Now("Asia/Shanghai")
	fmt.Println(now.Format("2006-01-02 15:04:05"))

	// UTC 偏移量
	offset, _ := timezone_utils.GetOffsetString("America/New_York", "Asia/Tokyo")
	fmt.Println(offset)  // "UTC+14"

	// 城市搜索
	zones, _ := timezone_utils.FindTimezoneByCity("tokyo")
	fmt.Println(zones)  // [Asia/Tokyo]
}
```

## API 参考

### 时区查询

| 函数 | 说明 |
|------|------|
| `GetTimezone(name)` | 获取时区对象 |
| `GetTimezoneInfo(name)` | 获取详细时区信息 |
| `IsValidTimezone(zone)` | 验证时区是否有效 |

### 时间转换

| 函数 | 说明 |
|------|------|
| `Convert(t, fromZone, toZone)` | 时间转换 |
| `ConvertString(str, format, fromZone, toZone)` | 字符串时间转换 |
| `ToUTC(t, fromZone)` | 转换为 UTC |
| `FromUTC(t, toZone)` | 从 UTC 转换 |

### 当前时间

| 函数 | 说明 |
|------|------|
| `Now(zone)` | 获取指定时区的当前时间 |
| `Today(zone)` | 获取指定时区的今天日期 |

### 偏移量

| 函数 | 说明 |
|------|------|
| `GetOffset(zone1, zone2)` | 获取两时区间的偏移量 |
| `GetOffsetString(zone1, zone2)` | 人类可读的偏移量字符串 |
| `GetUTCOffset(zone)` | 获取 UTC 偏移量 |

### DST

| 函数 | 说明 |
|------|------|
| `IsDST(zone)` | 检查夏令时是否生效 |
| `NextDSTChange(zone)` | 下次 DST 变化时间 |

### 列表

| 函数 | 说明 |
|------|------|
| `CommonTimezones()` | 常见时区列表 |
| `GetTimezonesByContinent()` | 按洲分组的时区 |
| `FindTimezoneByCity(city)` | 按城市搜索时区 |

## 支持的时区格式

- 标准 IANA 时区名: `America/New_York`, `Asia/Shanghai`, `Europe/London`
- UTC 别名: `UTC`

## 许可证

MIT