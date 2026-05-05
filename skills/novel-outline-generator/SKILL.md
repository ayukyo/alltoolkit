---
name: novel-outline-generator
description: 小说大纲生成技能。支持爽文/现实主义/言情/悬疑等多题材，AI动态生成300章独特事件，输出精简章节规划表（10列核心版）+ bible.json人物圣经。**v4.0新增多源整合题材创新**，整合微博热搜、抖音热点、番茄榜单、知乎热榜等数据源，AI综合思考创新组合方向，确保市场潜力+原创性。
metadata: {"recommendedThinking": "high", "version": "4.3", "namingConvention": "古诗词名/真实姓氏", "dataSources": ["微博热搜", "抖音热点", "番茄榜单", "知乎热榜", "AI自主"], "fixHistory": ["v4.1: 强制web_search+历史去重+连续三轮逻辑", "v4.2: 文件替换规则+禁止保存到新文件名", "v4.3: 统一文件命名规范+检查报告合并+禁止版本后缀"]}
---

# 小说大纲生成技能 v4.0（多源整合创新版）

## 🎯 v4.x 改进记录

| 版本 | 改进项 |
|------|--------|
| v3.0 | AI动态生成、10列精简、内置模板、统一检测、钩子评分 |
| v3.1 | bible.json主角合并、变量池逻辑修正、题材适配评分、生成后自检流程、文件路径字段 |
| v3.2 | 自检重生逻辑、空数据异常处理、CSV格式明确、去重阈值参数化 |
| v3.3 | derive_debut异常处理、int转换安全、总章节数动态获取 |
| v4.0 | **多源整合题材创新**：微博热搜+抖音热点+番茄榜单+知乎热榜，AI综合思考组合方向 |
| v4.1 | **强制热点获取+历史去重**：强制web_search调用、禁止返回空数组、历史书名去重检查、禁止复制示例书名 |
| v4.2 | **文件替换规则**：修复后必须保存到章节规划表.csv替换原文件，禁止保存到_fixed/_final等新文件名，检查必须读取原文件 |
| v4.3 | **统一命名规范**：所有文件禁止版本后缀，检查报告合并为单一文件，禁止创建多个检查报告变体 |

---

## 🔥 多源整合题材创新系统（v4.0新增）

### 数据源配置

| 来源 | 搜索关键词 | 提取内容 | 刷新频率 |
|------|-----------|----------|----------|
| **微博热搜** | "微博热搜 今日" | 前10热搜话题 | 每日 |
| **抖音热点** | "抖音热点话题 最新" | 热门短视频趋势 | 每日 |
| **番茄小说榜** | "番茄小说排行榜 热门" | 热门题材+书名 | 每日 |
| **知乎热榜** | "知乎热榜 今日" | 深度讨论话题 | 每日 |
| **AI自主思考** | 内部推理 | 创新组合方案 | 每次生成 |

### 题材创新组合流程

```
步骤1: 并行获取4个数据源热点数据
步骤2: 分析每个来源的热门题材趋势
步骤3: 识别题材交叉点（如：外卖+玄学、非遗+赛博朋克）
步骤4: AI综合思考创新组合方向（确保原创性）
步骤5: 生成题材融合方案（市场潜力+独特性）
步骤6: 进入原有大纲生成流程
```

### 创新组合示例（仅供参考，禁止直接复制）

> ⚠️ **重要警告**：以下示例仅供理解组合逻辑，**禁止直接作为新书名**！每次生成必须创建全新的题材组合。

| 组合类型 | 组合逻辑示例 | 已使用书名（禁止重复） |
|----------|--------------|----------------------|
| **热点+玄幻** | 社会热点 + 玄学系统 | 《业力外卖员》已用❌ |
| **非遗+科技** | 传统工艺 + 未来科技 | 《漆夜》已用❌ |
| **职场+悬疑** | 职场问题 + 企业阴谋 | 待创新✓ |
| **底层+觉醒** | 打工群体 + 能力觉醒 | 待创新✓ |

**历史生成记录去重检查（每次生成前必查）：**
```
已生成书名列表（禁止重复）：
- 业力外卖员 (2026-04-30, 05-02, 05-03 已用)
- 漆夜 (2026-04-30 已用)
- 数字遗嘱 (2026-05-01 已用)
- 下班后别找我 (2026-03-08 已用)
- 准点下班我成了首富 (2026-03-09 已用)
- 寿命交易所/寿命当铺/我拿寿命换前程 (2026-03-19 已用)
- 神级人生编辑器 (2026-03-27 已用)
- 词倾天下 (2026-03-31 已用)
- 越修炼越废柴的峰主大人 (2026-03-30 已用)
- 妹妹被宠成公主，我在东莞雨中送餐 (2026-04-03 已用)
- 被讨厌的我成了人生赢家 (2026-03-26 已用)
```

### 热点获取函数（v4.0新增）

> **⚠️ 重要说明：以下函数为框架代码，实际执行时由AI通过搜索API实现数据获取，并在内部推理中完成题材交叉分析和创新决策。框架代码提供了完整的数据结构和流程指导，AI可根据实际情况灵活实现。**

```python
def fetch_hot_topics():
    """
    获取多源热点数据
    
    返回: {
        "微博热搜": ["话题1", "话题2", ...],
        "抖音热点": ["趋势1", "趋势2", ...],
        "番茄榜单": [{"书名": "xxx", "题材": "xxx"}, ...],
        "知乎热榜": ["问题1", "问题2", ...]
    }
    
    实际执行说明：
    - AI执行时使用 web_search 工具搜索各平台热点
    - 解析搜索结果提取关键话题和趋势
    - 数据结构按框架定义组织
    """
    import requests
    
    topics = {}
    
    # 微博热搜（通过搜索API获取）
    try:
        # 使用web_search或searxng获取
        # 返回热搜话题列表
        topics["微博热搜"] = fetch_weibo_hot()
    except:
        topics["微博热搜"] = []
    
    # 抖音热点
    try:
        topics["抖音热点"] = fetch_douyin_hot()
    except:
        topics["抖音热点"] = []
    
    # 番茄小说榜单
    try:
        topics["番茄榜单"] = fetch_fanqie_rank()
    except:
        topics["番茄榜单"] = []
    
    # 知乎热榜
    try:
        topics["知乎热榜"] = fetch_zhihu_hot()
    except:
        topics["知乎热榜"] = []
    
    return topics

def analyze_trend_crossings(topics):
    """
    分析题材交叉点
    
    参数: topics - 多源热点数据
    
    返回: 创新组合方向列表
    
    实际执行说明：
    - AI执行时进行内部推理分析
    - 识别热点话题与热门题材的融合可能
    - 综合考虑受众共鸣、市场趋势、原创性
    """
    crossings = []
    
    # 分析微博热搜与番茄榜单的交叉
    weibo = topics.get("微博热搜", [])
    fanqie = topics.get("番茄榜单", [])
    
    for hot_topic in weibo:
        for book in fanqie:
            # 寻找可融合的点（AI内部判断）
            if is_fusion_possible(hot_topic, book["题材"]):
                crossings.append({
                    "热点": hot_topic,
                    "热门题材": book["题材"],
                    "组合潜力": rate_combination(hot_topic, book["题材"])
                })
    
    # 按潜力评分排序
    crossings.sort(key=lambda x: x["组合潜力"], reverse=True)
    
    return crossings[:10]  # 返回前10个创新方向

def generate_innovative_genre(crossings, base_genres):
    """
    AI综合思考生成创新题材
    
    参数:
    - crossings: 题材交叉点
    - base_genres: 基础题材分类
    
    返回: 创新题材融合方案
    
    实际执行说明：
    - AI选择最佳交叉点进行深度思考
    - 结合原创性要求生成创新方向
    - 评估市场潜力和受众共鸣度
    """
    # 选择最佳交叉点
    best_crossing = crossings[0] if crossings else None
    
    if best_crossing:
        # AI思考创新组合
        innovation = {
            "热点元素": best_crossing["热点"],
            "热门题材": best_crossing["热门题材"],
            "AI创新方向": combine_with_originality(best_crossing),
            "市场潜力": assess_market_potential(best_crossing),
            "原创性评分": assess_originality(best_crossing)
        }
    else:
        # 无热点数据时，AI自主创新
        innovation = {
            "热点元素": "无",
            "热门题材": "自主选择",
            "AI创新方向": ai_self_innovate(base_genres),
            "市场潜力": "中等",
            "原创性评分": 10
        }
    
    return innovation
```

---

## 📚 题材分类与适配（自动识别）

| 题材大类 | 识别关键词 | 开篇要求 | 爽点密度 | 钩子类型 | 结局 |
|---------|-----------|---------|----------|---------|------|
| **爽文类** | 玄幻/都市/武侠/修仙 | 金手指+冲突 | 每3-5章1爽点 | 悬念式(≥7分) | HE |
| **现实主义** | 底层/虐文/都市/职场 | 真实冲突 | 虐点驱动 | 压抑式/对比式(≥7分) | BE/HE可选 |
| **言情类** | 甜宠/虐恋/都市言情 | 相遇/冲突 | 每章1糖/虐点 | 悬念式(≥7分) | HE/BE可选 |
| **悬疑类** | 推理/刑侦/悬疑 | 案件+线索 | 每10章1反转 | 悬念式(≥7分) | 真相揭晓 |

---

## 📊 章节规划表.csv 格式（v4.0 精简版）

### 字段说明（10列核心字段）

| # | 字段 | 格式 | 示例 | 数据类型 | 说明 |
|---|------|------|------|----------|------|
| 1 | 章节 | 数字 | 1 | **整数** | 章节号(1-300) |
| 2 | 时间 | 时间范围 | 第1天08:00→20:00 | 字符串 | 故事内时间 |
| 3 | 地点 | 场景名 | 外卖站点→城中村 | 字符串 | 场景转换 |
| 4 | 核心事件 | 事件描述 | 求职失败入职外卖第一天 | 字符串 | **每章独特** |
| 5 | 关键道具 | 道具名/无 | 外卖服 | 字符串 | 关键物品 |
| 6 | 伏笔操作 | 埋设/回收 | 埋设体质之谜(98章回收) | 字符串 | 伏笔标记 |
| 7 | 情绪曲线 | 起点→终点 | 希望→绝望 | 字符串 | 300种不重复 |
| 8 | 本章钩子 | 钩子内容 | 手机震动妹妹发来消息 | 字符串 | **≥7分** |
| 9 | 剧情线 | 主线/支线/敌对 | 主线+沈玥线(20-30章) | 字符串 | 多线标注 |
| 10 | 出场人物 | 人物列表 | 沈屿/苏念念/夏瑶瑶 | 字符串 | 用/分隔 |

**⚠️ CSV解析注意：**
- 章节、时间、地点等字段为字符串（CSV标准格式）
- 读取时需将"章节"字段转为整数：`int(row["章节"])`
- 出场人物用`/`分隔，解析时：`row["出场人物"].split("/")`

---

## 📁 bible.json 内置模板（v4.0 完整版）

```json
{
  "书名": "",
  "题材": "",
  "总章节": 300,
  "创建日期": "",
  "文件路径": {
    "章节规划表": "章节规划表.csv",
    "大纲": "大纲.md",
    "简介": "简介.md"
  },
  "characters": [
    {
      "姓名": "",
      "角色类型": "主角",
      "关系": "主角",
      "年龄": 0,
      "身份": "",
      "外貌": {
        "身高": "",
        "体型": "",
        "脸型": "",
        "眼睛": "",
        "发型": "",
        "穿着风格": "",
        "标志性特征": ""
      },
      "性格": "",
      "金手指": "",
      "目标": "",
      "debut_chapter": 1,
      "exit_chapter": null,
      "死亡章节": null,
      "status": {
        "当前状态": "活跃",
        "当前位置": "",
        "当前情绪": "",
        "当前服装": ""
      },
      "关系变化": {},
      "秘密": "",
      "写作注意事项": ""
    }
  ],
  "relationships": {
    "情侣关系": [],
    "暗恋关系": [],
    "敌对关系": [],
    "亲情关系": []
  },
  "plot_lines": {
    "主线": {
      "名称": "",
      "章节范围": "1-300",
      "描述": ""
    },
    "支线": [
      {
        "名称": "",
        "章节范围": "",
        "涉及人物": []
      }
    ],
    "敌对线": [
      {
        "名称": "",
        "章节范围": "",
        "反派": "",
        "强度": ""
      }
    ]
  },
  "props": {
    "关键道具": [],
    "伏笔列表": []
  },
  "variables": {
    "主角": "",
    "女主": "",
    "女配": "",
    "妹妹": "",
    "兄弟": "",
    "反派": "",
    "城市": "",
    "职业": ""
  }
}
```

**⚠️ v3.x改进：主角合并入characters数组，统一验证逻辑！**

---

## 🔧 统一去重检测工具

### Python去重检测函数

```python
def detect_duplicates(csv_data, field_name, threshold=10):
    """
    检测指定字段的重复项
    
    参数:
    - csv_data: 章节规划表数据（列表）
    - field_name: 字段名（如"核心事件"、"本章钩子"）
    - threshold: 允许的最大重复数（默认10）
    
    返回:
    - duplicates: 重复项列表
    - duplicate_count: 重复数量
    - unique_count: 唯一值数量
    - is_pass: 是否合格（重复数≤阈值）
    """
    values = []
    duplicates = []
    
    for i, row in enumerate(csv_data, 1):
        value = row.get(field_name, "")
        if value in values:
            duplicates.append({
                "章节": i,
                "重复内容": value,
                "首次出现": values.index(value) + 1
            })
        values.append(value)
    
    unique_count = len(set(values))
    duplicate_count = len(values) - unique_count
    is_pass = duplicate_count <= threshold
    
    return duplicates, duplicate_count, unique_count, is_pass

def generate_dedup_report(csv_data, threshold=10, total_chapters=None):
    """
    生成完整去重报告
    
    参数:
    - csv_data: 章节规划表数据
    - threshold: 允许的最大重复数（默认10）
    - total_chapters: 总章节数（默认从csv_data长度获取）
    
    检查字段: 核心事件、本章钩子、情绪曲线
    
    v4.0改进: 支持动态总章节数
    """
    report = {}
    
    # 动态获取总章节数
    if total_chapters is None:
        total_chapters = len(csv_data) if csv_data else 300
    
    for field in ["核心事件", "本章钩子", "情绪曲线"]:
        duplicates, dup_count, unique_count, is_pass = detect_duplicates(
            csv_data, field, threshold
        )
        report[field] = {
            "唯一值数量": unique_count,
            "总章节数": total_chapters,
            "重复数量": dup_count,
            "重复率": f"{dup_count/max(total_chapters,1)*100:.1f}%",
            "是否合格": is_pass,
            "重复详情": duplicates[:5]
        }
    
    return report

def print_dedup_report(report, total_chapters=300):
    """打印去重报告"""
    print("=" * 50)
    print("📊 章节规划表去重报告")
    print("=" * 50)
    
    all_pass = True
    for field, data in report.items():
        status = "✅" if data["是否合格"] else "❌"
        if not data["是否合格"]:
            all_pass = False
        unique_count = data.get("唯一值数量", 0)
        print(f"\n{field}:")
        print(f"  唯一值: {unique_count}/{total_chapters} ({data['重复率']})")
        print(f"  状态: {status}")
        
        if not data["是否合格"] and data.get("重复详情"):
            print(f"  重复示例:")
            for dup in data["重复详情"]:
                print(f"    - 第{dup['章节']}章与第{dup['首次出现']}章重复")
    
    print("\n" + "=" * 50)
    return all_pass
```

---

## 🎣 钩子评分系统（v4.0 题材适配版）

### 钩子评分标准（10分制）

| 类型 | 示例 | 基础评分 | 题材加权 |
|------|------|---------|----------|
| **悬念动作** | "门外传来脚步声" | 9分 | 爽文+0,悬疑+0.5,现实-0.5,言情-0.5 |
| **悬念物品** | "他打开信封脸色变了" | 9分 | 爽文+0,悬疑+0,现实+0,言情+0.5 |
| **悬念状态** | "胸口泛起淡淡金光" | 8分 | 爽文+0.5,悬疑+0,现实-1,言情-1 |
| **情感冲击** | "妹妹发消息他看了很久没回" | 8分 | 爽文-0.5,悬疑-1,现实+1,言情+0.5 |
| **对比反差** | "妹妹吃团圆饭他在雨中啃冷面包" | 8分 | 爽文-1,悬疑-1,现实+1,言情+0 |
| **伏笔暗示** | "旧手机里有条未读消息不敢点开" | 7分 | 爽文+0,悬疑+0.5,现实+0,言情-0.5 |
| **预告式** | "明天开始修炼" | 2分 ❌ | 所有题材禁止 |
| **剧透式** | "他不知道敌人已经锁定他" | 1分 ❌ | 所有题材禁止 |
| **总结式** | "这一战让他明白了很多" | 1分 ❌ | 所有题材禁止 |

### 钩子阈值要求

| 题材 | 最低评分 | 推荐类型（加权后≥7分） |
|------|----------|------------------------|
| 爽文类 | ≥7分 | 悬念动作(9)、悬念状态(8.5)、悬念物品(9) |
| 现实主义 | ≥7分 | 情感冲击(9)、对比反差(9)、悬念物品(9) |
| 言情类 | ≥7分 | 悬念物品(9.5)、情感冲击(8.5) |
| 悬疑类 | ≥7分 | 悬念动作(9.5)、悬念物品(9)、伏笔暗示(7.5) |

### 钩子质量检测函数（v4.0 题材适配版）

```python
def rate_hook(hook_text, genre="爽文"):
    """
    评估钩子质量（题材适配版）
    
    参数:
    - hook_text: 钩子文本
    - genre: 题材（爽文/现实主义/言情/悬疑）
    
    返回: (最终评分, 基础类型, 是否合格)
    """
    # 禁止词检测（所有题材禁止）
    forbidden_words = ["明天", "下章", "继续", "不知道", "殊不知", 
                       "已经在路上", "注定", "这一战", "终于明白", 
                       "躺在床上", "思绪万千"]
    for word in forbidden_words:
        if word in hook_text:
            return (1, "禁止类型", False)
    
    # 类型检测与基础评分
    base_score = 5
    hook_type = "普通"
    
    # 悬念动作
    suspense_action_words = ["门外", "脚步", "脸色", "突然", "巨响", "手机响", "传来"]
    for word in suspense_action_words:
        if word in hook_text:
            base_score = 9
            hook_type = "悬念动作"
            break
    
    # 悬念物品
    suspense_item_words = ["打开", "信封", "盒子", "发现", "看到", "屏幕", "消息"]
    if base_score == 5:
        for word in suspense_item_words:
            if word in hook_text:
                base_score = 9
                hook_type = "悬念物品"
                break
    
    # 情感冲击
    emotional_words = ["妹妹", "兄弟", "哭了", "手抖", "眼眶", "看了很久", 
                       "泪流", "发来消息", "没有回"]
    if base_score == 5:
        for word in emotional_words:
            if word in hook_text:
                base_score = 8
                hook_type = "情感冲击"
                break
    
    # 对比反差
    contrast_words = ["团圆饭", "雨中", "豪车", "零钱", "婚纱", "淋雨", 
                      "啃冷面包", "远远看着"]
    if base_score == 5:
        for word in contrast_words:
            if word in hook_text:
                base_score = 8
                hook_type = "对比反差"
                break
    
    # 伏笔暗示
    foreshadow_words = ["未读消息", "不敢点开", "秘密", "日记", "照片", "泛黄"]
    if base_score == 5:
        for word in foreshadow_words:
            if word in hook_text:
                base_score = 7
                hook_type = "伏笔暗示"
                break
    
    # 题材加权
    genre_weights = {
        "爽文": {"悬念动作": 0, "悬念物品": 0, "悬念状态": 0.5, 
                 "情感冲击": -0.5, "对比反差": -1, "伏笔暗示": 0},
        "现实主义": {"悬念动作": -0.5, "悬念物品": 0, "悬念状态": -1, 
                     "情感冲击": 1, "对比反差": 1, "伏笔暗示": 0},
        "言情": {"悬念动作": -0.5, "悬念物品": 0.5, "悬念状态": -1, 
                 "情感冲击": 0.5, "对比反差": 0, "伏笔暗示": -0.5},
        "悬疑": {"悬念动作": 0.5, "悬念物品": 0, "悬念状态": 0, 
                 "情感冲击": -1, "对比反差": -1, "伏笔暗示": 0.5}
    }
    
    weight = genre_weights.get(genre, {}).get(hook_type, 0)
    final_score = base_score + weight
    
    # 判断是否合格
    is_pass = final_score >= 7
    
    return (final_score, hook_type, is_pass)
```

---

## 👤 人物登场自动推导与验证

### 人物登场推导规则

```python
def derive_debut_chapters(bible):
    """
    根据剧情线自动推导人物登场章节
    
    规则:
    - 主角: 第1章（角色类型=主角）
    - 主线相关配角: 根据支线章节范围推导
    - 反派: 根据敌对线章节范围推导
    
    v4.0改进: 添加异常处理和空值检测
    """
    debut_map = {}
    
    # 异常处理：bible为空或characters不存在
    if not bible or "characters" not in bible:
        return debut_map
    
    # 从characters数组读取（包括主角）
    for char in bible.get("characters", []):
        if not char:  # 跳过空元素
            continue
        name = char.get("姓名")
        if not name:  # 跳过无姓名的角色
            continue
        
        if char.get("角色类型") == "主角":
            debut_map[name] = 1
        elif char.get("debut_chapter"):
            debut_map[name] = char.get("debut_chapter")
    
    # 异常处理：plot_lines不存在
    plot_lines = bible.get("plot_lines", {})
    if not plot_lines:
        return debut_map
    
    # 根据支线推导未明确标注的人物
    for line in plot_lines.get("支线", []):
        if not line:
            continue
        chapter_range = line.get("章节范围", "")
        if chapter_range and "-" in chapter_range:
            try:
                start_chapter = int(chapter_range.split("-")[0])
                for person in line.get("涉及人物", []):
                    if person and person not in debut_map:
                        debut_map[person] = start_chapter
            except (ValueError, IndexError):
                pass  # 忽略无效的章节范围格式
    
    # 根据敌对线推导
    for line in plot_lines.get("敌对线", []):
        if not line:
            continue
        chapter_range = line.get("章节范围", "")
        if chapter_range and "-" in chapter_range:
            try:
                start_chapter = int(chapter_range.split("-")[0])
                villain = line.get("反派")
                if villain and villain not in debut_map:
                    debut_map[villain] = start_chapter
            except (ValueError, IndexError):
                pass
    
    return debut_map

def validate_character_debut(csv_data, bible):
    """
    验证人物登场时间
    
    返回: 错误列表（提前登场的人物）
    
    v4.0改进: 添加异常处理和int转换安全
    """
    errors = []
    debut_map = derive_debut_chapters(bible)
    
    # 异常处理：csv_data为空
    if not csv_data:
        return errors
    
    # 验证每章出场人物
    for row in csv_data:
        if not row:  # 跳过空行
            continue
        
        # 安全获取章节号
        chapter_str = row.get("章节", "0")
        try:
            chapter = int(chapter_str)
        except (ValueError, TypeError):
            continue  # 跳过无效章节
        
        characters_str = row.get("出场人物", "")
        if not characters_str:
            continue
        
        characters = characters_str.split("/")
        
        for char in characters:
            char = char.strip()
            if char and char in debut_map:
                required_debut = debut_map[char]
                if chapter < required_debut:
                    errors.append({
                        "章节": chapter,
                        "人物": char,
                        "应该登场": required_debut,
                        "错误": "提前登场"
                    })
    
    return errors
```

---

## 🔄 变量自动映射池（v4.0 修正版）

### 变量池结构

```python
class VariablePool:
    """
    自动变量映射池
    
    v3.x修正: 修复逻辑判断bug，优先匹配精确角色类型
    """
    
    def __init__(self, bible):
        self.bible = bible
        self.variables = {}
        self._build_pool()
    
    def _build_pool(self):
        """自动构建变量池"""
        # 从characters数组读取（统一处理）
        for char in self.bible.get("characters", []):
            role_type = char.get("角色类型", "")
            relation = char.get("关系", "")
            name = char.get("姓名", "")
            
            if not name:
                continue
            
            # 优先匹配角色类型
            if role_type == "主角" or relation == "主角":
                self.variables["{主角}"] = name
                self.variables["{职业}"] = char.get("身份", "")
            elif role_type == "女主" or "女主" in relation:
                self.variables["{女主}"] = name
            elif role_type == "女配" or "女配" in relation:
                self.variables["{女配}"] = name
            elif role_type == "妹妹" or "妹妹" in relation:
                self.variables["{妹妹}"] = name
            elif role_type == "兄弟" or relation in ["兄弟", "好友", "闺蜜"]:
                self.variables["{兄弟}"] = name
            elif role_type == "反派" or "反派" in relation or "敌" in relation:
                self.variables["{反派}"] = name
        
        # 其他变量
        self.variables["{城市}"] = self.bible.get("城市", "东莞")
        
        # 道具相关
        props = self.bible.get("props", {})
        key_props = props.get("关键道具", [])
        if key_props:
            self.variables["{道具}"] = key_props[0]
    
    def replace(self, template):
        """
        替换模板中的变量
        
        参数: template - 含{变量}的事件模板
        返回: 替换后的具体事件
        """
        result = template
        for var, value in self.variables.items():
            if value:
                result = result.replace(var, str(value))
        
        # 处理未知变量（删除）
        import re
        result = re.sub(r'\{[^}]+\}', '', result)
        
        return result.strip()
    
    def get_all_variables(self):
        """返回所有已映射的变量"""
        return {k: v for k, v in self.variables.items() if v}
```

---

## 🚀 生成流程（v4.1 多源整合版）

### 第一阶段：大纲生成（6:00）

| 步骤 | 内容 | 输出 |
|------|------|------|
| **1** | **历史书名去重检查** | 确认新书名不重复 |
| **2** | **多源热点获取（强制web_search）** | 4个来源热点数据（禁止空数组） |
| **3** | **题材交叉分析** | 创新组合方向列表 |
| **4** | **AI创新决策** | 题材融合方案（原创性≥9分） |
| **5** | 题材确认 | genre变量 |
| **6** | 生成核心设定 | 书名+核心梗+主角人设 |
| **7** | 扩展人物 | characters数组（≥18角色） |
| **8** | 多线设计 | plot_lines结构 |
| **9** | AI动态生成事件 | 300章独特事件 |
| **10** | 生成bible.json | 使用v4.0模板 |
| **11** | 生成章节规划表.csv | 10列精简版 |
| **12** | **生成阶段自检（快速）** | 调用regenerate_if_failed(max_attempts=3) |
| **13** | 生成其他文件 | 大纲.md、简介.md |
| **14** | 输出报告 | 热点来源+去重+评分+登场验证报告 |

### 第二阶段：查漏补缺（8:00-20:00）

> ⚠️ **核心逻辑：连续三轮通过才停止！**

| 时间 | 任务 | 检查内容 | 逻辑 |
|------|------|----------|------|
| **08:00** | 第一轮查漏补缺 | 去重+钩子评分+人物登场+逻辑连贯 | 发现问题立即修复 |
| **10:00** | 第二轮查漏补缺 | 同上 | 发现问题立即修复 |
| **12:00** | 第三轮查漏补缺 | 同上 | 发现问题立即修复 |
| **14:00** | 第四轮查漏补缺 | 同上+伏笔闭环 | 发现问题立即修复 |
| **16:00** | 第五轮查漏补缺 | 同上 | 发现问题立即修复 |
| **18:00** | 第六轮查漏补缺 | 同上 | 发现问题立即修复 |
| **20:00** | 最终检查 | 全面检查+稳定性验证 | **必须连续3轮通过才结束** |

**查漏补缺核心逻辑（v4.1新增）**：
```
使用 continuous_check_until_stable() 函数：
- 无限轮次检查（最多10轮）
- 发现问题立即调用 fix_failed_items() 修复
- 修复后重新验证
- 必须连续3轮全部通过才停止
- 任何一轮不合格，重置计数继续检查

⚠️ 文件操作规则（必须遵守）：
1. 读取：必须从 `章节规划表.csv` 读取（禁止读取 _fixed/_final 等变体）
2. 保存：修复后必须保存到 `章节规划表.csv`（替换原文件）
3. 备份：保存前可选备份到 `章节规划表_backup.csv`
4. 禁止：禁止保存到新文件名（如 _fixed、_final、_v2 等）
5. 验证：保存后立即重新读取验证修复成功
```

### 查漏补缺文件操作示例（v4.1新增）

**正确的文件操作流程**：
```python
# 1. 读取原文件
csv_path = "novel-ideas/命痕整形师_2026-05-05/章节规划表.csv"
csv_data = read_csv(csv_path)

# 2. 检查并修复
fixed_data = fix_failed_items(csv_data, bible, genre, report)

# 3. 保存到原文件（替换）
write_csv(csv_path, fixed_data)  # 直接替换原文件

# 4. 重新读取验证
csv_data_verify = read_csv(csv_path)
verify_fix_success(csv_data_verify)
```

### v4.0 热点获取提示词（强制执行）

> ⚠️ **关键要求**：必须使用 `web_search` 工具获取真实热点数据，禁止返回空数组！

生成大纲前，AI**必须先执行以下步骤**：

**步骤0：检查历史生成记录（强制去重）**
```
读取 novel-ideas/ 目录下所有已生成的 bible.json 文件
提取已使用的书名列表
确认新书名不能与任何已用书名重复（包括题材组合相似）
```

**步骤1：使用 web_search 工具获取热点数据**
```
必须调用 web_search 工具（不是搜索函数框架）：
- web_search(query="微博热搜 今日", count=10)
- web_search(query="抖音热点话题 最新", count=10)
- web_search(query="番茄小说排行榜 都市爽文", count=10)
- web_search(query="知乎热榜 今日", count=10)

解析搜索结果，提取真实话题和趋势
如果某个来源获取失败，使用 AI 内部知识补充，但必须返回非空数据
```

**步骤2：题材交叉分析**
```
分析热点话题与热门题材的融合可能
优先选择：
- 与已生成书名差异大的组合
- 市场潜力高但尚未被使用的方向
- 原创性强（评分≥9分）
```

**步骤3：生成创新书名**
```
AI综合思考创新组合方向
书名必须：
- 与已生成书名完全不同（禁止重复）
- 题材组合新颖（避免相似组合如"业力外卖员"的变体）
- 市场潜力评估合理
```

### 热点获取失败时的自主创新流程

如果热点数据确实无法获取，执行自主创新：

```
1. 检查已生成书名列表（强制）
2. 排除已用题材组合：
   - 外卖+玄学（已用）
   - 非遗+科技（已用）
   - 寿命交易（已用）
   - 下班/职场喜剧（已用）
3. 从未用方向选择：
   - 医疗/教育/金融 + 玄学/科技/悬疑
   - 家庭/亲情 + 超能力/命运
   - 体育/游戏 + 系统/穿越
4. 生成全新书名和题材组合
```

### 热点数据JSON格式

```json
{
  "hot_data": {
    "微博热搜": ["热搜话题1", "热搜话题2", "热搜话题3"],
    "抖音热点": ["热点趋势1", "热点趋势2", "热点趋势3"],
    "番茄榜单": [{"书名": "热门书名1", "题材": "都市"}, {"书名": "热门书名2", "题材": "玄幻"}],
    "知乎热榜": ["知乎问题1", "知乎问题2", "知乎问题3"],
    "获取时间": "2026-04-30 18:00"
  },
  "genre_innovation": {
    "热点元素": "外卖骑手",
    "热门题材": "都市玄学",
    "AI创新方向": "外卖员觉醒业力视觉，看见善恶数字",
    "组合来源": "微博热搜#3 + 番茄榜单都市类#1",
    "市场潜力": "高（外卖群体共鸣+玄学爽点）",
    "原创性评分": 9.5
  }
}
```

### 生成后自检流程（v4.0 完整版）

```python
def post_generation_check(csv_data, bible, genre):
    """
    生成后自检流程
    
    返回: (是否全部通过, 详细报告)
    """
    report = {
        "去重检测": None,
        "钩子评分": None,
        "人物登场": None
    }
    all_pass = True
    
    # 异常处理：空数据
    if not csv_data:
        return False, {"错误": "CSV数据为空"}
    
    # 1. 去重检测
    dedup_report = generate_dedup_report(csv_data)
    report["去重检测"] = dedup_report
    if not all(r["是否合格"] for r in dedup_report.values()):
        all_pass = False
    
    # 2. 钩子评分检测
    hook_scores = []
    for row in csv_data:
        hook = row.get("本章钩子", "")
        if hook:  # 只检测非空钩子
            score, type_, is_pass = rate_hook(hook, genre)
            hook_scores.append({
                "章节": row.get("章节"),
                "评分": score,
                "类型": type_,
                "是否合格": is_pass
            })
    
    # 异常处理：无钩子数据
    if hook_scores:
        failed_hooks = [h for h in hook_scores if not h["是否合格"]]
        report["钩子评分"] = {
            "平均评分": sum(h["评分"] for h in hook_scores) / len(hook_scores),
            "最低评分": min(h["评分"] for h in hook_scores),
            "不合格数量": len(failed_hooks),
            "是否合格": len(failed_hooks) <= 10
        }
        if len(failed_hooks) > 10:
            all_pass = False
    else:
        report["钩子评分"] = {
            "平均评分": 0,
            "最低评分": 0,
            "不合格数量": 300,
            "是否合格": False
        }
        all_pass = False
    
    # 3. 人物登场验证
    debut_errors = validate_character_debut(csv_data, bible)
    report["人物登场"] = {
        "错误数量": len(debut_errors),
        "是否合格": len(debut_errors) == 0,
        "错误详情": debut_errors[:5]
    }
    if debut_errors:
        all_pass = False
    
    return all_pass, report

def regenerate_if_failed(csv_data, bible, genre, max_attempts=3):
    """
    自检不合格时自动重新生成（最多重试N次）
    
    注意：这是生成阶段的重试逻辑，用于生成时快速修复
    
    参数:
    - max_attempts: 最大重试次数（默认3次）
    
    返回: (最终CSV数据, 是否成功, 报告)
    """
    for attempt in range(1, max_attempts + 1):
        print(f"第{attempt}次自检...")
        
        all_pass, report = post_generation_check(csv_data, bible, genre)
        
        if all_pass:
            print("✅ 自检通过！")
            return csv_data, True, report
        
        print(f"❌ 第{attempt}次自检不合格，重新生成...")
        
        if attempt < max_attempts:
            # 根据报告针对性修复
            csv_data = fix_failed_items(csv_data, bible, genre, report)
    
    print(f"⚠️ {max_attempts}次重试后仍不合格，请人工检查")
    return csv_data, False, report

def continuous_check_until_stable(csv_data, bible, genre, required_passes=3, max_iterations=10):
    """
    连续N轮通过才停止（查漏补缺阶段的核心逻辑）
    
    这是v4.1新增的查漏补缺流程：
    - 无限轮次检查（最多max_iterations次）
    - 发现问题立即修复
    - 必须连续N轮全部通过才结束
    - 如果中间有任何一轮不合格，重置计数
    
    参数:
    - required_passes: 需要连续通过的轮数（默认3轮）
    - max_iterations: 最大迭代次数（防止无限循环，默认10次）
    
    返回: (最终CSV数据, 总轮数, 连续通过轮数, 报告列表)
    """
    consecutive_passes = 0
    iteration = 0
    all_reports = []
    
    while iteration < max_iterations:
        iteration += 1
        print(f"\n{'='*50}")
        print(f"📊 第 {iteration} 轮检查")
        print(f"当前连续通过轮数: {consecutive_passes}/{required_passes}")
        print(f"{'='*50}")
        
        # 执行完整检查
        all_pass, report = post_generation_check(csv_data, bible, genre)
        all_reports.append({
            "轮数": iteration,
            "是否通过": all_pass,
            "报告": report
        })
        
        if all_pass:
            consecutive_passes += 1
            print(f"✅ 第{iteration}轮检查全部通过！")
            print(f"   连续通过轮数: {consecutive_passes}/{required_passes}")
            
            # 检查是否达到要求
            if consecutive_passes >= required_passes:
                print(f"\n🎉 连续{required_passes}轮全部通过！大纲质量稳定！")
                return csv_data, iteration, consecutive_passes, all_reports
        else:
            # 本轮不合格，重置计数并修复
            consecutive_passes = 0
            print(f"❌ 第{iteration}轮检查发现问题，立即修复...")
            
            # 根据报告针对性修复
            csv_data = fix_failed_items(csv_data, bible, genre, report)
            print(f"   已修复问题，继续下一轮检查...")
    
    # 达到最大迭代次数
    print(f"\n⚠️ 达到最大迭代次数({max_iterations}次)")
    print(f"   最终连续通过轮数: {consecutive_passes}/{required_passes}")
    if consecutive_passes >= required_passes:
        print(f"   ✅ 大纲质量达标")
    else:
        print(f"   ❌ 大纲质量不稳定，需要人工检查")
    
    return csv_data, iteration, consecutive_passes, all_reports

def fix_failed_items(csv_data, bible, genre, report):
    """
    根据自检报告针对性修复失败项
    
    ⚠️ 重要：修复后必须保存并替换原文件！
    
    修复策略:
    - 去重失败: 重新生成重复章节的事件
    - 钩子不合格: 重新生成不合格钩子
    - 人物登场错误: 移除提前登场的人物
    
    文件保存规则（必须遵守）：
    1. 修复后的数据必须保存到 `章节规划表.csv`（原文件）
    2. 保存前可备份到 `章节规划表_backup.csv`
    3. 禁止保存到 `_fixed`、`_final` 等新文件名
    4. 检查时必须读取 `章节规划表.csv`
    """
    fixed_csv = csv_data.copy()
    
    # 修复重复事件
    for field, data in report.get("去重检测", {}).items():
        if not data.get("是否合格"):
            for dup in data.get("重复详情", []):
                chapter_idx = dup["章节"] - 1
                if chapter_idx < len(fixed_csv):
                    # 重新生成该章事件
                    old_event = fixed_csv[chapter_idx].get(field, "")
                    new_event = generate_unique_item(field, genre, old_event, bible)
                    fixed_csv[chapter_idx][field] = new_event
    
    # 修复不合格钩子
    hook_data = report.get("钩子评分", {})
    if not hook_data.get("是否合格"):
        for i, row in enumerate(fixed_csv):
            hook = row.get("本章钩子", "")
            if hook:
                score, _, is_pass = rate_hook(hook, genre)
                if not is_pass:
                    # 重新生成钩子
                    new_hook = generate_unique_hook(genre, bible)
                    fixed_csv[i]["本章钩子"] = new_hook
    
    # 修复人物登场错误
    debut_data = report.get("人物登场", {})
    if debut_data.get("错误详情"):
        debut_map = derive_debut_chapters(bible)
        for error in debut_data.get("错误详情", []):
            chapter_idx = error["章节"] - 1
            if chapter_idx < len(fixed_csv):
                # 移除提前登场的人物
                characters = fixed_csv[chapter_idx].get("出场人物", "").split("/")
                wrong_char = error["人物"]
                new_characters = [c for c in characters if c.strip() != wrong_char]
                fixed_csv[chapter_idx]["出场人物"] = "/".join(new_characters)
    
    return fixed_csv

def generate_unique_item(field_type, genre, existing_value, bible):
    """
    生成独特的事件/钩子/情绪
    
    参数:
    - field_type: 字段类型（核心事件/本章钩子/情绪曲线）
    - genre: 题材
    - existing_value: 需要替换的旧值
    - bible: 人物圣经
    
    返回: 新生成的独特值
    """
    # 核心事件生成
    if field_type == "核心事件":
        return f"[新生成事件] {genre}风格独特事件"
    
    # 钩子生成
    elif field_type == "本章钩子":
        hook_templates = {
            "爽文": ["门外传来脚步声", "他打开信封脸色变了"],
            "现实主义": ["妹妹发消息他看了很久没回", "雨中啃冷面包"],
            "言情": ["手机震动是他发来的消息", "她笑了笑说出了一个名字"],
            "悬疑": ["地上有一滩血还没干", "三天只剩三天了"]
        }
        templates = hook_templates.get(genre, hook_templates["爽文"])
        return templates[0] if templates[0] != existing_value else templates[-1]
    
    # 情绪曲线生成
    elif field_type == "情绪曲线":
        emotions = ["希望→绝望", "温暖→心碎", "压抑→麻木", "紧张→释然"]
        for e in emotions:
            if e != existing_value:
                return e
        return "平静→期待"
    
    return existing_value

def generate_unique_hook(genre, bible):
    """生成独特钩子"""
    return generate_unique_item("本章钩子", genre, "", bible)

def print_check_report(report):
    """打印自检报告"""
    print("\n" + "=" * 60)
    print("📊 v4.0 生成后自检报告")
    print("=" * 60)
    
    # 去重检测
    print("\n【去重检测】")
    for field, data in report["去重检测"].items():
        status = "✅" if data["是否合格"] else "❌"
        print(f"  {field}: {data['唯一值数量']}/300 唯一 {status}")
    
    # 钩子评分
    print("\n【钩子评分】")
    hook_data = report["钩子评分"]
    status = "✅" if hook_data["是否合格"] else "❌"
    print(f"  平均评分: {hook_data['平均评分']:.1f}分")
    print(f"  最低评分: {hook_data['最低评分']:.1f}分")
    print(f"  不合格数量: {hook_data['不合格数量']}个 {status}")
    
    # 人物登场
    print("\n【人物登场】")
    debut_data = report["人物登场"]
    status = "✅" if debut_data["是否合格"] else "❌"
    print(f"  错误数量: {debut_data['错误数量']}个 {status}")
    
    print("\n" + "=" * 60)
    
    all_pass = all([
        all(r["是否合格"] for r in report["去重检测"].values()),
        report["钩子评分"]["是否合格"],
        report["人物登场"]["是否合格"]
    ])
    
    if all_pass:
        print("✅ 全部自检通过！")
    else:
        print("❌ 存在不合格项，需要重新生成！")
    
    return all_pass
```

---

## 🤖 AI动态事件生成规则

### 事件生成参数

```python
def generate_event(chapter, genre, setting, previous_events):
    """
    AI动态生成单章事件
    
    参数:
    - chapter: 章节号(1-300)
    - genre: 题材
    - setting: 核心设定
    - previous_events: 已生成事件集合
    
    返回: 独特的事件描述
    """
    # 章节位置类型
    if chapter <= 10:
        event_phase = "开篇引入"
    elif chapter <= 50:
        event_phase = "发展积累"
    elif chapter <= 100:
        event_phase = "冲突升级"
    elif chapter <= 200:
        event_phase = "高潮转折"
    elif chapter <= 280:
        event_phase = "收尾铺垫"
    else:
        event_phase = "结局收束"
    
    # 题材风格
    style_map = {
        "爽文": {"冲突强度": "高", "爽点密度": "高"},
        "现实主义": {"冲突强度": "中", "虐点密度": "高"},
        "言情": {"冲突强度": "低", "糖虐密度": "高"},
        "悬疑": {"冲突强度": "中", "线索密度": "高"}
    }
    
    # AI生成（确保独特）
    event = ai_generate_unique_event(
        chapter=chapter,
        phase=event_phase,
        style=style_map.get(genre, {}),
        setting=setting,
        exclude=previous_events
    )
    
    return event
```

---

## ✅ 质量检查清单（v4.1）

### 第一阶段：大纲生成（6:00）

```
□ 历史书名去重：检查已生成书名，禁止重复
□ 热点数据获取（强制）：web_search获取真实数据，禁止空数组
□ 题材交叉分析：识别热点+热门题材融合点
□ AI创新决策：综合思考创新组合方向（禁止复制示例）
□ 市场潜力评估：热度+共鸣点+受众分析
□ 原创性评分：确保≥9分（避免跟风）
□ 题材识别：自动识别关键词
□ bible.json：主角合并入characters数组
□ 人物登场：derive_debut_chapters() + validate_character_debut()
□ 核心事件：detect_duplicates(threshold=10) ≤10个重复
□ 本章钩子：rate_hook(genre) ≥7分题材加权
□ 情绪曲线：去重检测 ≤10个重复
□ 变量映射：VariablePool._build_pool() 优先匹配角色类型
□ 生成后自检：regenerate_if_failed(max_attempts=3) 快速通过
□ CSV格式：明确数据类型，章节转int处理
□ 异常处理：空值检测、int转换安全
□ 总章节数：动态获取，支持不同长度
□ 输出文件：bible.json + CSV + 大纲.md + 简介.md
□ 文件路径：bible.json包含file_path字段
```

### 第二阶段：查漏补缺（8:00-20:00）

```
□ 第一轮检查（8:00）：去重+钩子评分+人物登场+逻辑连贯
□ 发现问题修复：调用fix_failed_items()立即修复
□ 修复后验证：确认修复成功
□ 第二轮检查（10:00）：同上
□ 第三轮检查（12:00）：同上
□ 第四轮检查（14:00）：同上+伏笔闭环验证
□ 第五轮检查（16:00）：同上
□ 第六轮检查（18:00）：同上
□ 最终检查（20:00）：使用continuous_check_until_stable(required_passes=3)
□ 稳定性验证：必须连续3轮全部通过
□ 最大迭代：10轮上限防止无限循环
□ 最终报告：输出总轮数+连续通过轮数+详细报告
```

---

## 🔗 与 novel-writer 技能接口规范

### 输出目录结构

```
novel-ideas/书名_YYYY-MM-DD/
├── bible.json           # v4.0模板（含主角、文件路径、热点来源）
├── 章节规划表.csv       # 10列精简版
├── 大纲.md
├── 简介.md
└── 检查报告.md          # 统一的检查报告（可选）
```

### ⚠️ 文件命名规范（v4.2强制要求）

**核心原则：禁止添加版本后缀！每次修复替换原文件！**

| 文件类型 | 允许的文件名 | 禁止的文件名 |
|----------|--------------|--------------|
| 章节规划表 | `章节规划表.csv` | `_fixed`, `_final`, `_v2`, `_backup`（仅备份时允许） |
| 检查报告 | `检查报告.md` 或 `检查报告.json` | `_final`, `_complete`, `_完整版`, 带时间戳 |
| bible.json | `bible.json` | 任何后缀或前缀 |
| 大纲.md | `大纲.md` | 任何后缀或前缀 |
| 简介.md | `简介.md` | 任何后缀或前缀 |

**检查报告命名规则**：
```
正确：检查报告.md, 检查报告.json
禁止：check_report.json, afternoon_check_report.json, final_check_report_xxx.json
禁止：检查修复报告.md, 下午大纲查漏补缺报告.md, 每日大纲检查报告.md
禁止：_完整版, _final, _validated, _complete 等任何后缀
```

**修复报告合并规则**：
```
所有修复记录合并到单一检查报告文件
不要创建单独的 fix_report.json, fix_hooks_log.json, foreshadow_fix_report.json
所有修复信息作为检查报告的一部分
```

**正确的文件操作流程**：
```python
# 读取原文件
bible = read_json("bible.json")
csv = read_csv("章节规划表.csv")

# 修复
fixed_csv = fix_failed_items(csv, bible, genre, report)

# 替换原文件（禁止创建新文件名）
write_csv("章节规划表.csv", fixed_csv)  # 直接替换

# 检查报告（合并所有信息）
write_file("检查报告.md", merged_report)  # 单一报告文件
```

### novel-writer 输入规范

| 文件 | 字段 | 说明 |
|------|------|------|
| bible.json | characters[].debut_chapter | 人物登场章节（含主角） |
| bible.json | characters[].角色类型 | 区分主角/女主/女配等 |
| bible.json | file_path.章节规划表 | CSV文件名 |
| bible.json | plot_lines | 多线剧情范围 |
| bible.json | variables | 变量映射池 |
| 章节规划表.csv | 核心事件 | 每章独特事件 |
| 章节规划表.csv | 本章钩子 | ≥7分钩子 |

---

## 📖 示例输出报告

```
【大纲生成完成 - v4.0】

书名：《[书名]》
题材：[题材组合]
总章节：300章

============================================================
🔥 多源热点数据来源（v4.0新增）
============================================================
微博热搜：[热搜话题1, 热搜话题2, ...]
抖音热点：[趋势1, 趋势2, ...]
番茄榜单：[热门书名, 热门题材, ...]
知乎热榜：[问题1, 问题2, ...]

题材创新组合：[热点元素] + [热门题材] = [AI创新方向]
组合来源：[数据源A#排名] + [数据源B#排名]
市场潜力：[高/中/低]
原创性评分：[评分]

============================================================
📊 v4.0 生成后自检报告
============================================================

【去重检测】
  核心事件: 295/300 唯一 ✅
  本章钩子: 298/300 唯一 ✅
  情绪曲线: 300/300 唯一 ✅

【钩子评分】
  平均评分: 8.5分
  最低评分: 7.0分
  不合格数量: 0个 ✅

【人物登场】
  错误数量: 0个 ✅

============================================================
✅ 全部自检通过！

📁 输出文件：
  - novel-ideas/[书名]_YYYY-MM-DD/
    ├── bible.json (v4.0模板)
    ├── 章节规划表.csv (10列)
    ├── 大纲.md
    └── 简介.md
```

---

**v4.0 改进：多源整合题材创新（微博热搜+抖音热点+番茄榜单+知乎热榜），AI综合思考创新组合方向，确保市场潜力+原创性！**