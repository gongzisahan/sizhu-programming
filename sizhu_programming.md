
# 四柱编程
## 当老天是 Python 程序员

> 如果命运是一套预先封装好的程序，那么八字就是它的底层源代码。在这里，没有虚无缥缈的神明，只有严谨的字典映射、精准的循环控制与底层接口调用。翻开本书，带上你的 IDE，让我们一起对宇宙的操作系统进行逆向工程。

---

**覆盖版本**：邵伟华《四柱预测学》· 沈孝瞻《子平真诠》· 子平凡思博客理论  
**依赖环境**：Python 3.10+  |  任意 IDE  
**许可证**：天命所授，概不退换

---

## 目录

- [第0章　元认知：在写代码之前](#第0章元认知在写代码之前)
- **第一部分　基础数据层**
  - [第1章　阴阳五行：命理系统的基本类型](#第1章阴阳五行命理系统的基本类型)
  - [第2章　天干地支：命理系统的基本单元](#第2章天干地支命理系统的基本单元)
  - [第3章　六十甲子：天干地支的组合空间](#第3章六十甲子天干地支的组合空间)
- **第二部分　排盘引擎**
  - [第4章　四柱的计算：从出生时间到命盘](#第4章四柱的计算从出生时间到命盘)
  - [第5章　大运与流年：时间轴的扩展](#第5章大运与流年时间轴的扩展)
- **第三部分　分析模块**
  - [第6章　十神系统：关系的语义层](#第6章十神系统关系的语义层)
  - [第7章　格局分析：强弱与结构判断](#第7章格局分析强弱与结构判断)
  - [第8章　合冲刑害：干支的动态交互](#第8章合冲刑害干支的动态交互)
  - [第9章　用神与忌神：三层架构](#第9章用神与忌神三层架构)
  - [第10章　神煞：附加标签系统](#第10章神煞附加标签系统)
  - [第11章　综合断命：推理模型的构建](#第11章综合断命推理模型的构建)
  - [第12章　实断框架：从代码到推命](#第12章实断框架从代码到推命)
- **附录**
  - [附录A　完整数据表](#附录a完整数据表)
  - [附录B　合冲刑害速查表](#附录b合冲刑害速查表)
  - [附录C　推荐工具与开源资源](#附录c推荐工具与开源资源)
  - [附录D　子平凡思贡献摘要](#附录d子平凡思贡献摘要)

---

## 第0章　元认知：在写代码之前

在正式建模之前，有必要先确立一个认识论上的前提。命理博客作者子平凡思在其新浪博客系列文章中多次强调：

> "五行是反推式的安立，说白了也是一个模型，假如当初安立的不是五行是六行，现在也一样使用。"

这句话对工程师来说非常重要。它意味着：我们建的不是一个"发现真理"的系统，而是一个**忠实实现某个历史约定模型**的系统。这个模型经过千年实践筛选，相对自洽，但本质上仍是人类对时间节律的一种符号化约定。

```python
# 程序员视角的元认知注释
"""
四柱系统是一个符号推理引擎 (Symbolic Reasoning Engine)。
其底层是：约定的枚举类型 + 固定规则的关系图 + 查表逻辑。

系统的"准确性"依赖于：
  1. 规则实现的正确性   → 程序员的责任（本书覆盖范围）
  2. 规则体系本身的自洽性 → 命理学的研究域
  3. 具体断命的解读能力  → 人的责任，程序无法替代

本书只覆盖第1点。
"""
```

与子平真诠的格局体系相比，邵伟华的扶抑体系更偏向"量化强弱"，而子平凡思的贡献在于清晰地划分了两个层次——格局决定"质"（成与败），其余因素决定"量"（高与低）。这个框架将贯穿全书。

```
软件架构类比：

格局     → 主程序（决定功能边界和上限）
大运     → 运行时环境（决定能否正常运行）
神煞     → 配置参数（调节输出量级）
纳音     → 皮肤主题（影响风格，不改变核心逻辑）
扶抑强弱  → 性能基准测试（辅助参考，不直接决定架构）
```

---

# 第一部分　基础数据层

## 第1章　阴阳五行：命理系统的基本类型

### 1.1 阴阳的二元定义

在四柱命理中，阴阳是最基础的属性标签，可以视作一个布尔类型的枚举。每一个天干和地支都带有固定的阴阳属性，且阴阳会影响十神的推导方式。

```python
from enum import Enum

class YinYang(Enum):
    YANG = "阳"
    YIN  = "阴"
```

规律很简单：天干地支按顺序排列时，奇数位（第1、3、5…）为阳，偶数位（第2、4、6…）为阴。

### 1.2 五行的枚举类型与属性表

五行（Wood, Fire, Earth, Metal, Water）是命理系统的核心数据类型，贯穿整个分析链路。

```python
class WuXing(Enum):
    WOOD  = "木"
    FIRE  = "火"
    EARTH = "土"
    METAL = "金"
    WATER = "水"
```

五行不仅是一个标签，还携带若干属性。以下是常用的属性映射表：

| 五行 | 方位 | 季节 | 颜色 | 数字 | 脏腑 |
|------|------|------|------|------|------|
| 木   | 东   | 春   | 青   | 3、8 | 肝、胆 |
| 火   | 南   | 夏   | 红   | 2、7 | 心、小肠 |
| 土   | 中   | 长夏 | 黄   | 5、10 | 脾、胃 |
| 金   | 西   | 秋   | 白   | 4、9 | 肺、大肠 |
| 水   | 北   | 冬   | 黑   | 1、6 | 肾、膀胱 |

### 1.3 五行生克的有向图关系

五行之间的生克关系是一张固定的有向图，是整个分析引擎的基础运算。

**相生**（顺序传递，前者生后者）：木 → 火 → 土 → 金 → 水 → 木

**相克**（间隔克制）：木 → 土、土 → 水、水 → 火、火 → 金、金 → 木

```python
# 五行相生关系：key 生 value
GENERATES: dict[WuXing, WuXing] = {
    WuXing.WOOD:  WuXing.FIRE,
    WuXing.FIRE:  WuXing.EARTH,
    WuXing.EARTH: WuXing.METAL,
    WuXing.METAL: WuXing.WATER,
    WuXing.WATER: WuXing.WOOD,
}

# 五行相克关系：key 克 value
CONTROLS: dict[WuXing, WuXing] = {
    WuXing.WOOD:  WuXing.EARTH,
    WuXing.EARTH: WuXing.WATER,
    WuXing.WATER: WuXing.FIRE,
    WuXing.FIRE:  WuXing.METAL,
    WuXing.METAL: WuXing.WOOD,
}

def generates(a: WuXing, b: WuXing) -> bool:
    """a 是否生 b"""
    return GENERATES[a] == b

def controls(a: WuXing, b: WuXing) -> bool:
    """a 是否克 b"""
    return CONTROLS[a] == b

def is_generated_by(a: WuXing, b: WuXing) -> bool:
    """a 是否被 b 生（b 生 a）"""
    return GENERATES[b] == a

def is_controlled_by(a: WuXing, b: WuXing) -> bool:
    """a 是否被 b 克（b 克 a）"""
    return CONTROLS[b] == a
```

---

## 第2章　天干地支：命理系统的基本单元

### 2.1 十天干的数据定义

天干（Heavenly Stems）是一个长度为 10 的有序序列。每个天干有固定的索引（0–9）、阴阳、五行三个核心属性。

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class TianGan:
    name:    str
    yinyang: YinYang
    wuxing:  WuXing
    index:   int

TIANGAN: list[TianGan] = [
    TianGan("甲", YinYang.YANG, WuXing.WOOD,  0),
    TianGan("乙", YinYang.YIN,  WuXing.WOOD,  1),
    TianGan("丙", YinYang.YANG, WuXing.FIRE,  2),
    TianGan("丁", YinYang.YIN,  WuXing.FIRE,  3),
    TianGan("戊", YinYang.YANG, WuXing.EARTH, 4),
    TianGan("己", YinYang.YIN,  WuXing.EARTH, 5),
    TianGan("庚", YinYang.YANG, WuXing.METAL, 6),
    TianGan("辛", YinYang.YIN,  WuXing.METAL, 7),
    TianGan("壬", YinYang.YANG, WuXing.WATER, 8),
    TianGan("癸", YinYang.YIN,  WuXing.WATER, 9),
]

TIANGAN_MAP: dict[str, TianGan] = {t.name: t for t in TIANGAN}
```

规律：每两个天干共享一个五行，阳干（YANG）在前，阴干（YIN）在后。

### 2.2 十二地支的数据定义

地支（Earthly Branches）是一个长度为 12 的有序序列，对应十二个月份和生肖。

```python
@dataclass(frozen=True)
class DiZhi:
    name:    str
    yinyang: YinYang
    wuxing:  WuXing
    month:   int    # 命理月份（0=丑月/农历正月前, 1=寅月, ... 11=子月）
    shengxiao: str
    index:   int

DIZHI: list[DiZhi] = [
    DiZhi("子", YinYang.YANG, WuXing.WATER, 11, "鼠",  0),
    DiZhi("丑", YinYang.YIN,  WuXing.EARTH,  0, "牛",  1),
    DiZhi("寅", YinYang.YANG, WuXing.WOOD,   1, "虎",  2),
    DiZhi("卯", YinYang.YIN,  WuXing.WOOD,   2, "兔",  3),
    DiZhi("辰", YinYang.YANG, WuXing.EARTH,  3, "龙",  4),
    DiZhi("巳", YinYang.YIN,  WuXing.FIRE,   4, "蛇",  5),
    DiZhi("午", YinYang.YANG, WuXing.FIRE,   5, "马",  6),
    DiZhi("未", YinYang.YIN,  WuXing.EARTH,  6, "羊",  7),
    DiZhi("申", YinYang.YANG, WuXing.METAL,  7, "猴",  8),
    DiZhi("酉", YinYang.YIN,  WuXing.METAL,  8, "鸡",  9),
    DiZhi("戌", YinYang.YANG, WuXing.EARTH,  9, "狗", 10),
    DiZhi("亥", YinYang.YIN,  WuXing.WATER, 10, "猪", 11),
]

DIZHI_MAP: dict[str, DiZhi] = {d.name: d for d in DIZHI}
```

### 2.3 地支藏干：一对多的映射关系

地支藏干是地支数据结构中最复杂的部分。每个地支内部"藏"有 1–3 个天干，分别称为**主气、中气、余气**。

这是一个典型的一对多关系，可以用字典映射实现：

```python
# 格式：地支名 -> [(天干名, 力量权重), ...]
# 主气权重最高（约 60%），中气次之（约 30%），余气最低（约 10%）
CANG_GAN: dict[str, list[tuple[str, float]]] = {
    "子": [("癸", 1.0)],
    "丑": [("己", 0.6), ("癸", 0.3), ("辛", 0.1)],
    "寅": [("甲", 0.6), ("丙", 0.3), ("戊", 0.1)],
    "卯": [("乙", 1.0)],
    "辰": [("戊", 0.6), ("乙", 0.3), ("癸", 0.1)],
    "巳": [("丙", 0.6), ("庚", 0.3), ("戊", 0.1)],
    "午": [("丁", 0.6), ("己", 0.4)],
    "未": [("己", 0.6), ("丁", 0.3), ("乙", 0.1)],
    "申": [("庚", 0.6), ("壬", 0.3), ("戊", 0.1)],
    "酉": [("辛", 1.0)],
    "戌": [("戊", 0.6), ("辛", 0.3), ("丁", 0.1)],
    "亥": [("壬", 0.6), ("甲", 0.4)],
}
```

> **权重说明**：上面的权重是示意性参考比例，不同门派在具体权重上有所出入。邵伟华体系对主气赋予更高权重；子平真诠则更重视月令主气的透干情况。子平凡思强调：月令藏干是否透出天干，比权重数字本身更重要——透干者力量显，不透者力量潜藏。

---

## 第3章　六十甲子：天干地支的组合空间

### 3.1 合法组合的生成规则

天干 10 个，地支 12 个，理论上有 120 种组合，但命理历法中只有 60 种合法组合（称为六十甲子）。

**规律**：只有阴阳相同（同为阳干配阳支，同为阴干配阴支）的组合才合法。这导致组合数从 120 缩减到 60。

```python
def generate_jiazi_cycle() -> list[tuple[str, str]]:
    """生成六十甲子序列"""
    cycle: list[tuple[str, str]] = []
    tg_idx, dz_idx = 0, 0
    for _ in range(60):
        cycle.append((TIANGAN[tg_idx].name, DIZHI[dz_idx].name))
        tg_idx = (tg_idx + 1) % 10
        dz_idx = (dz_idx + 1) % 12
    return cycle

# 结果起始：甲子、乙丑、丙寅、丁卯...
# 实质上是求 lcm(10, 12) = 60
```

### 3.2 纳音五行

每对干支在六十甲子中有对应的纳音五行，是命理系统的辅助属性层。子平凡思明确指出：纳音可作"象法"参考，但不应凌驾于六神格局体系之上。

```python
# 纳音五行（按六十甲子序号，每两个一组）
NAYIN: list[tuple[list[str], str, WuXing]] = [
    (["甲子", "乙丑"], "海中金", WuXing.METAL),
    (["丙寅", "丁卯"], "炉中火", WuXing.FIRE),
    (["戊辰", "己巳"], "大林木", WuXing.WOOD),
    (["庚午", "辛未"], "路旁土", WuXing.EARTH),
    (["壬申", "癸酉"], "剑锋金", WuXing.METAL),
    (["甲戌", "乙亥"], "山头火", WuXing.FIRE),
    (["丙子", "丁丑"], "涧下水", WuXing.WATER),
    (["戊寅", "己卯"], "城头土", WuXing.EARTH),
    (["庚辰", "辛巳"], "白蜡金", WuXing.METAL),
    (["壬午", "癸未"], "杨柳木", WuXing.WOOD),
    (["甲申", "乙酉"], "泉中水", WuXing.WATER),
    (["丙戌", "丁亥"], "屋上土", WuXing.EARTH),
    (["戊子", "己丑"], "霹雳火", WuXing.FIRE),
    (["庚寅", "辛卯"], "松柏木", WuXing.WOOD),
    (["壬辰", "癸巳"], "长流水", WuXing.WATER),
    (["甲午", "乙未"], "沙中金", WuXing.METAL),
    (["丙申", "丁酉"], "山下火", WuXing.FIRE),
    (["戊戌", "己亥"], "平地木", WuXing.WOOD),
    (["庚子", "辛丑"], "壁上土", WuXing.EARTH),
    (["壬寅", "癸卯"], "金箔金", WuXing.METAL),
    (["甲辰", "乙巳"], "覆灯火", WuXing.FIRE),
    (["丙午", "丁未"], "天河水", WuXing.WATER),
    (["戊申", "己酉"], "大驿土", WuXing.EARTH),
    (["庚戌", "辛亥"], "钗钏金", WuXing.METAL),
    (["壬子", "癸丑"], "桑柘木", WuXing.WOOD),
    (["甲寅", "乙卯"], "大溪水", WuXing.WATER),
    (["丙辰", "丁巳"], "沙中土", WuXing.EARTH),
    (["戊午", "己未"], "天上火", WuXing.FIRE),
    (["庚申", "辛酉"], "石榴木", WuXing.WOOD),
    (["壬戌", "癸亥"], "大海水", WuXing.WATER),
]
```

---

# 第二部分　排盘引擎

## 第4章　四柱的计算：从出生时间到命盘

### 4.1 四柱的整体结构

四柱是四个"柱"的合称：**年柱、月柱、日柱、时柱**，每柱由一个天干和一个地支组成，合计 8 个字（故又称"八字"）。

```
年柱: [年干][年支]
月柱: [月干][月支]
日柱: [日干][日支]
时柱: [时干][时支]
```

每个柱的计算逻辑不同，难度递增：年柱最简单，日柱最复杂。

```python
@dataclass
class BaZi:
    year:  tuple[str, str]   # (年干, 年支)
    month: tuple[str, str]   # (月干, 月支)
    day:   tuple[str, str]   # (日干, 日支)
    hour:  tuple[str, str]   # (时干, 时支)

    @property
    def ri_zhu_gan(self) -> str:
        """日主（日柱天干），全书分析的核心参照点"""
        return self.day[0]

    def all_gan(self) -> list[tuple[str, str, bool]]:
        """返回所有天干：(天干名, 所属柱, 是否为月柱)"""
        return [
            (self.year[0],  "年干", False),
            (self.month[0], "月干", True),
            (self.day[0],   "日干", False),
            (self.hour[0],  "时干", False),
        ]

    def all_zhi(self) -> list[tuple[str, str]]:
        """返回所有地支"""
        return [
            (self.year[1],  "年支"),
            (self.month[1], "月支"),
            (self.day[1],   "日支"),
            (self.hour[1],  "时支"),
        ]
```

### 4.2 节气换月：命理历法的关键

> ⚠️ **这是最容易出错的地方**：命理月份的分界不是农历初一，而是节气中的"节"（非"气"）。

命理以每月的"节"作为换月节点：

| 命理月 | 地支 | 对应节气（节） |
|--------|------|----------------|
| 正月   | 寅   | 立春（约2月4日） |
| 二月   | 卯   | 惊蛰（约3月6日） |
| 三月   | 辰   | 清明（约4月5日） |
| 四月   | 巳   | 立夏（约5月6日） |
| 五月   | 午   | 芒种（约6月6日） |
| 六月   | 未   | 小暑（约7月7日） |
| 七月   | 申   | 立秋（约8月7日） |
| 八月   | 酉   | 白露（约9月8日） |
| 九月   | 戌   | 寒露（约10月8日）|
| 十月   | 亥   | 立冬（约11月7日）|
| 十一月 | 子   | 大雪（约12月7日）|
| 十二月 | 丑   | 小寒（约1月6日） |

节气的精确时刻每年不同，**必须查表或通过天文算法获取，不能用固定日期代替**。

### 4.3 月干的推算：五虎遁年

知道月支后，月干由**年干**决定，规律称为"五虎遁年起月法"：

```python
# 月支顺序（从寅月=正月开始）
MONTH_ZHI_ORDER = ["寅","卯","辰","巳","午","未","申","酉","戌","亥","子","丑"]

# 五虎遁年表：年干索引 % 5 -> 各月天干列表（从寅月起）
MONTH_STEM_TABLE: dict[int, list[str]] = {
    0: ["丙","丁","戊","己","庚","辛","壬","癸","甲","乙","丙","丁"],  # 甲/己年
    1: ["戊","己","庚","辛","壬","癸","甲","乙","丙","丁","戊","己"],  # 乙/庚年
    2: ["庚","辛","壬","癸","甲","乙","丙","丁","戊","己","庚","辛"],  # 丙/辛年
    3: ["壬","癸","甲","乙","丙","丁","戊","己","庚","辛","壬","癸"],  # 丁/壬年
    4: ["甲","乙","丙","丁","戊","己","庚","辛","壬","癸","甲","乙"],  # 戊/癸年
}

def get_month_gan(year_gan: str, month_zhi: str) -> str:
    """根据年干和月支推算月干"""
    year_gan_idx = TIANGAN_MAP[year_gan].index
    month_zhi_idx = MONTH_ZHI_ORDER.index(month_zhi)
    return MONTH_STEM_TABLE[year_gan_idx % 5][month_zhi_idx]
```

### 4.4 时干的推算：五鼠遁日

时支由出生时刻决定（以两小时为一个时辰），时干由**日干**决定：

```python
# 时支与对应的北京时间范围
HOUR_BRANCH: list[tuple[str, int, int]] = [
    ("子", 23, 1),   # 23:00–01:00
    ("丑",  1, 3),
    ("寅",  3, 5),
    ("卯",  5, 7),
    ("辰",  7, 9),
    ("巳",  9, 11),
    ("午", 11, 13),
    ("未", 13, 15),
    ("申", 15, 17),
    ("酉", 17, 19),
    ("戌", 19, 21),
    ("亥", 21, 23),
]

def get_hour_zhi(hour: int) -> str:
    """将24小时制转换为时支"""
    for zhi, start, end in HOUR_BRANCH:
        if start <= hour < end:
            return zhi
        if zhi == "子" and (hour >= 23 or hour < 1):
            return "子"
    return "子"

# 五鼠遁日表：日干索引 % 5 -> 各时天干（从子时起）
HOUR_STEM_TABLE: dict[int, list[str]] = {
    0: ["甲","乙","丙","丁","戊","己","庚","辛","壬","癸","甲","乙"],  # 甲/己日
    1: ["丙","丁","戊","己","庚","辛","壬","癸","甲","乙","丙","丁"],  # 乙/庚日
    2: ["戊","己","庚","辛","壬","癸","甲","乙","丙","丁","戊","己"],  # 丙/辛日
    3: ["庚","辛","壬","癸","甲","乙","丙","丁","戊","己","庚","辛"],  # 丁/壬日
    4: ["壬","癸","甲","乙","丙","丁","戊","己","庚","辛","壬","癸"],  # 戊/癸日
}

def get_hour_gan(day_gan: str, hour_zhi: str) -> str:
    """根据日干和时支推算时干"""
    day_gan_idx = TIANGAN_MAP[day_gan].index
    hour_zhi_idx = DIZHI_MAP[hour_zhi].index
    return HOUR_STEM_TABLE[day_gan_idx % 5][hour_zhi_idx]
```

### 4.5 现代工具与库的使用

日柱的推算（确定某一公历日期对应的干支）依赖万年历数据，手动实现复杂且容易出错。现代开发中推荐直接使用成熟库：

```python
# Python 推荐库：lunar-python
# pip install lunar-python

from lunar_python import Lunar, Solar

def get_bazi(year: int, month: int, day: int, hour: int) -> BaZi:
    """从公历时间获取四柱八字"""
    solar = Solar.fromYmdHms(year, month, day, hour, 0, 0)
    lunar = solar.getLunar()
    ec   = lunar.getEightChar()

    # lunar-python 返回的是完整干支字符串（2个字）
    return BaZi(
        year  = (ec.getYear()[0],  ec.getYear()[1]),
        month = (ec.getMonth()[0], ec.getMonth()[1]),
        day   = (ec.getDay()[0],   ec.getDay()[1]),
        hour  = (ec.getTime()[0],  ec.getTime()[1]),
    )

# 示例
bazi = get_bazi(1990, 5, 15, 8)
print(f"日主：{bazi.ri_zhu_gan}")
```

> **工程建议**：排盘本身是成熟问题，建议将精力放在后续的分析逻辑上，而非重复造轮子。

---

## 第5章　大运与流年：时间轴的扩展

### 5.1 大运的起运计算

大运是对一个人人生阶段的粗粒度划分，每一步大运管辖约 10 年。起运年龄（几岁开始行大运）的计算涉及出生日期与最近节气的距离。

**计算原则：**
- 阳年生男、阴年生女：**顺推**（往后数节气）
- 阳年生女、阴年生男：**逆推**（往前数节气）

```python
def calc_dayun_start_age(
    birth_date,
    gender: str,
    year_yinyang: YinYang
) -> float:
    """
    计算起运年龄（简化版）
    返回：起运的实岁（可能是小数）
    """
    forward = (
        (year_yinyang == YinYang.YANG and gender == "男") or
        (year_yinyang == YinYang.YIN  and gender == "女")
    )

    if forward:
        days_to_jieqi = find_next_jieqi_days(birth_date)
    else:
        days_to_jieqi = find_prev_jieqi_days(birth_date)

    # 命理传统换算：3天折合1年
    return days_to_jieqi / 3.0
```

### 5.2 大运干支的推算

大运从月柱开始，顺推或逆推六十甲子序列，每步为一个干支：

```python
def get_dayun_sequence(
    month_pillar: tuple[str, str],
    forward: bool,
    count: int = 8
) -> list[tuple[str, str]]:
    """
    推算大运序列
    month_pillar: 月柱干支元组
    forward: True=顺推, False=逆推
    count: 推算步数
    """
    cycle = generate_jiazi_cycle()
    # 找月柱在六十甲子中的位置
    try:
        start_idx = cycle.index(month_pillar)
    except ValueError:
        raise ValueError(f"月柱 {month_pillar} 不在六十甲子中")

    result: list[tuple[str, str]] = []
    idx = start_idx
    for _ in range(count):
        idx = (idx + 1) % 60 if forward else (idx - 1) % 60
        result.append(cycle[idx])
    return result
```

### 5.3 大运的干支分治与统看

命理界对大运"干支各管五年"还是"十年统看"争论已久。子平凡思的立场与子平真诠一脉相承——以格局为核心统看，但工程实现时可以引入折中权重：

```python
def calc_dayun_influence(
    bazi: BaZi,
    dayun_gan: str,
    dayun_zhi: str,
    year_in_dayun: int  # 1-10，第几年
) -> float:
    """
    大运影响力计算（三七互涉法）
    前5年天干占7成，地支占3成；后5年反转
    """
    gan_score = calc_yongshen_fit(bazi, dayun_gan)
    zhi_score = calc_yongshen_fit(bazi, dayun_zhi)

    if year_in_dayun <= 5:
        # 前半段：天干为主
        return gan_score * 0.7 + zhi_score * 0.3
    else:
        # 后半段：地支为主
        return gan_score * 0.3 + zhi_score * 0.7
```

### 5.4 流年

流年是当前日历年的干支，每年固定，从甲子年开始按六十甲子循环：

```python
def get_year_ganzhi(year: int) -> tuple[str, str]:
    """公历年份 → 干支年"""
    # 以1984年甲子年为基准
    offset = (year - 1984) % 60
    cycle = generate_jiazi_cycle()
    return cycle[offset]

# 示例
print(get_year_ganzhi(2024))  # ('甲', '辰') → 甲辰年
```

---

# 第三部分　分析模块

## 第6章　十神系统：关系的语义层

### 6.1 日主的确立

日柱的天干称为**日主**（也叫日元），是整个命盘分析的核心参照物。所有其他天干（地支通过藏干透出）都以日主为基准，计算其与日主的五行生克关系，进而得到十神。

```python
def get_rizhu_gan(bazi: BaZi) -> str:
    return bazi.ri_zhu_gan
```

### 6.2 十神的推导算法

十神的推导基于两个维度：**五行关系**（生我、克我、我生、我克、同我）× **阴阳关系**（同性/异性），共产生 10 种组合。

| 关系      | 同性（阴阳相同） | 异性（阴阳不同） |
|-----------|-----------------|-----------------|
| 同五行    | 比肩            | 劫财            |
| 我生（食伤）| 食神          | 伤官            |
| 我克（财） | 偏财           | 正财            |
| 克我（官杀）| 七杀          | 正官            |
| 生我（印） | 偏印           | 正印            |

```python
def get_shishen(rizhu_gan: str, target_gan: str) -> str:
    """
    计算 target_gan 相对于 rizhu_gan 的十神
    """
    rz = TIANGAN_MAP[rizhu_gan]
    tg = TIANGAN_MAP[target_gan]
    same_yin = (rz.yinyang == tg.yinyang)

    if rz.wuxing == tg.wuxing:
        return "比肩" if same_yin else "劫财"
    elif generates(rz.wuxing, tg.wuxing):   # 我生
        return "食神" if same_yin else "伤官"
    elif controls(rz.wuxing, tg.wuxing):    # 我克
        return "偏财" if same_yin else "正财"
    elif controls(tg.wuxing, rz.wuxing):    # 克我
        return "七杀" if same_yin else "正官"
    elif generates(tg.wuxing, rz.wuxing):   # 生我
        return "偏印" if same_yin else "正印"
    else:
        raise ValueError(f"无法推导十神：{rizhu_gan} vs {target_gan}")
```

### 6.3 十神的命理语义

十神是命理断事的核心语言，每个神代表一类人事关系或能量模式：

| 十神 | 符号含义 | 关联六亲（男命） | 关联六亲（女命） | 关联事物 |
|------|----------|------------------|------------------|----------|
| 比肩 | 同类平等 | 兄弟 | 姐妹 | 竞争、朋友 |
| 劫财 | 同类夺财 | 兄弟 | 姐妹 | 竞争、损耗 |
| 食神 | 我生同性 | — | — | 才艺、福气、食禄 |
| 伤官 | 我生异性 | — | — | 才华、叛逆、克官 |
| 偏财 | 我克同性 | 父亲、情人 | 父亲 | 横财、应酬 |
| 正财 | 我克异性 | 妻子 | 父亲 | 正当收入、勤劳 |
| 七杀 | 克我同性 | — | 情夫 | 压力、权威、凶险 |
| 正官 | 克我异性 | — | 丈夫 | 名誉、法规、管束 |
| 偏印 | 生我同性 | 继母 | — | 偏学、直觉 |
| 正印 | 生我异性 | 母亲 | 母亲 | 文书、学历、贵人 |

### 6.4 子平凡思：六神情义优先于五行生克

子平凡思在博客中强调：

> "六亲生克显然比五行生克更能体现六神的内涵。"

这意味着在代码实现中，不能只做五行层面的矩阵运算，还需要引入"情义"维度：

```python
from dataclasses import dataclass

@dataclass
class ShiShenRelation:
    """
    十神关系不只是五行生克，还有情义属性
    （子平凡思视角的扩展模型）
    """
    shishen:   str    # 十神名称
    wuxing_rel: str   # 五行关系：生/克/同

    # 情义属性（子平凡思强调的第二层）
    qing_yi: str      # "有情" | "无情"
    # 有情：用神与日主/格局配合自然，无冲突
    # 无情：虽有生克关系，但位置、力量使其配合失调

    # 位置属性
    position: str     # "透干" | "藏支" | "得根"
    is_yue_ling: bool # 是否为月令（月令力量最重）

def calc_relation_weight(rel: ShiShenRelation) -> float:
    """
    同一五行关系，因情义和位置不同，权重大不相同
    """
    base_weights = {"生": 0.8, "克": 0.8, "同": 1.0}
    base = base_weights.get(rel.wuxing_rel, 0.5)

    # 有情者权重加乘（子平凡思：有情的生克才是真正有力的）
    if rel.qing_yi == "有情":
        base *= 1.5
    elif rel.qing_yi == "无情":
        base *= 0.5   # 无情的生克，实际效力大打折扣

    # 月令加权（子平真诠：月令为提纲，力量最重）
    if rel.is_yue_ling:
        base *= 2.0

    # 透干者力量更显（透干为苗，地支为根）
    if rel.position == "透干":
        base *= 1.3
    elif rel.position == "藏支":
        base *= 0.7

    return base
```

---

## 第7章　格局分析：强弱与结构判断

### 7.0 大局观：格局是主程序，其余是插件

子平凡思最核心的主张：**格局决定命局的层次上限，大运决定这个上限能否实现，其余因素（神煞、纳音、干支细节）是调节量级的修正项，不是决定成败的主程序。**

> "人的命造，区区八个字，却表达着这个命局最主要的一种或几种事象、规律，把握了这个大局，则可以层层展开分析，丝丝入扣。根在苗先，实在花后，脱离了八字原局去谈论大运、流年，是很难取得良好的预测效果的。"

```python
class BaziAnalyzer:
    """
    完整的四柱分析器（子平凡思格局优先架构）
    """
    def analyze(self, bazi: BaZi) -> dict:
        # ── 第一层：格局（主程序）──
        geju_result = self._evaluate_geju(bazi)

        # ── 第二层：格局成败（质）──
        chengbai = self._check_chengbai(geju_result, bazi)

        # ── 第三层：强弱修正（在格局成立后参考）──
        strength = self._calc_rizhu_strength(bazi)

        # ── 第四层：神煞（量级调节，非主导）──
        shensha_mod = self._calc_shensha_modifier(bazi)

        # ── 整合：大局观 ──
        base_level = self._calc_base_level(chengbai, strength)
        final_level = base_level + shensha_mod

        return {
            "格局":   geju_result["name"],
            "成败":   chengbai["is_cheng"],
            "成败原因": chengbai["reason"],
            "格局层次": round(min(10.0, max(0.0, final_level)), 2),
            "日主强弱": strength,
        }

    # ❌ 反面教材：不要让神煞直接决定格局成败
    # def wrong_analyze(self, bazi):
    #     if "天乙贵人" in shensha: return "贵格"  # 错误！
```

### 7.1 日主强弱的量化模型

日主强弱是辅助判断工具，在子平凡思的框架里，它是格局内的参数而非独立决策层。

```python
# 十神对日主的影响分值（基础值）
SHISHEN_STRENGTH_SCORE: dict[str, float] = {
    # 生扶类（正值）
    "比肩": +1.0, "劫财": +1.0,
    "正印": +0.8, "偏印": +0.8,
    # 克耗类（负值）
    "正财": -0.6, "偏财": -0.6,
    "正官": -0.6, "七杀": -0.8,
    "食神": -0.5, "伤官": -0.7,
}

def calc_rizhu_strength(bazi: BaZi) -> float:
    """
    日主强弱计算
    遍历8个字的藏干，累加各天干对日主的影响分数
    月令藏干分数加倍（月令力量最重）
    返回：正值=偏旺，负值=偏弱，接近0=中和
    """
    total = 0.0
    rizhu = bazi.ri_zhu_gan

    for pillar_name, pillar in [
        ("年", bazi.year), ("月", bazi.month),
        ("日", bazi.day),  ("时", bazi.hour)
    ]:
        is_month = (pillar_name == "月")
        # 天干直接计算
        gan = pillar[0]
        if gan != rizhu:
            ss = get_shishen(rizhu, gan)
            score = SHISHEN_STRENGTH_SCORE.get(ss, 0)
            total += score * (2.0 if is_month else 1.0)

        # 地支通过藏干计算
        zhi = pillar[1]
        for cang_gan, weight in CANG_GAN[zhi]:
            ss = get_shishen(rizhu, cang_gan)
            score = SHISHEN_STRENGTH_SCORE.get(ss, 0) * weight
            total += score * (2.0 if is_month else 1.0)

    return total
```

### 7.2 普通格局：月令取格（子平真诠体系）

《子平真诠》的格局体系以**月令为核心**。格局由月支的藏干透出哪个天干来决定：

```python
def get_geju_name(bazi: BaZi) -> str:
    """
    月令取格（子平真诠体系）
    优先取透出天干，无透出则取主气
    """
    month_zhi = bazi.month[1]
    rizhu_gan = bazi.ri_zhu_gan
    cang = CANG_GAN[month_zhi]

    # 获取年、日、时天干（排除日主自身，排除月干以避免循环）
    other_gans = {bazi.year[0], bazi.day[0], bazi.hour[0]}

    # 优先取透出的藏干（力量最显）
    for gan_name, weight in sorted(cang, key=lambda x: -x[1]):
        if gan_name in other_gans:
            ss = get_shishen(rizhu_gan, gan_name)
            # 建禄、月刃特殊处理
            if ss in ("比肩",):
                return "建禄格"
            if ss in ("劫财",):
                return "月刃格"
            return ss + "格"

    # 无透出则取主气
    main_gan = cang[0][0]
    ss = get_shishen(rizhu_gan, main_gan)
    if ss == "比肩": return "建禄格"
    if ss == "劫财": return "月刃格"
    return ss + "格"
```

### 7.3 格局成败：质的判断（子平凡思视角）

```python
# 各格局的成败规则（简化版）
GEJU_CHENGBAI_RULES: dict[str, dict] = {
    "正官格": {
        "喜": ["正印", "偏财"],    # 印护官，财生官
        "忌": ["伤官", "七杀"],    # 伤官见官，七杀混杂
        "成格描述": "官逢财印，清纯无混",
        "破格描述": "伤官透出，或七杀混杂",
    },
    "七杀格": {
        "喜": ["食神", "正印"],    # 食神制杀，印化杀
        "忌": ["正财", "伤官"],    # 财生杀，引杀攻身
        "成格描述": "食制或印化，杀有驾驭",
        "破格描述": "财星引杀，或两者皆无制",
    },
    "正财格": {
        "喜": ["食神", "正官"],    # 食生财，财生官
        "忌": ["七杀", "比劫"],    # 杀破财，比劫夺财
        "成格描述": "财旺有食生，官护财",
        "破格描述": "比劫重重，或七杀破局",
    },
    "偏财格": {
        "喜": ["食神", "正官"],
        "忌": ["七杀", "比劫"],
        "成格描述": "偏财得食生，无比劫夺",
        "破格描述": "比劫群起夺财",
    },
    "食神格": {
        "喜": ["偏财"],            # 食神生财
        "忌": ["偏印"],            # 枭神夺食
        "成格描述": "食神生财，无枭夺",
        "破格描述": "偏印出现夺食",
    },
    "伤官格": {
        "喜": ["正财", "正印"],    # 伤官生财，伤官佩印
        "忌": ["正官"],            # 伤官见官，大忌
        "成格描述": "伤官生财或佩印",
        "破格描述": "见正官，伤官见官",
    },
    "正印格": {
        "喜": ["正官", "七杀"],    # 官印双全，杀印相生
        "忌": ["正财", "伤官"],    # 财坏印（需细分），食伤泄气
        "成格描述": "官印双全，或杀印相生",
        "破格描述": "财重印轻，贪财坏印",
    },
    "偏印格": {
        "喜": ["七杀", "正官"],
        "忌": ["食神"],            # 枭神夺食
        "成格描述": "偏印逢官杀有化",
        "破格描述": "食神被夺，格局无力",
    },
    "建禄格": {
        "喜": ["正官", "正财"],
        "忌": ["七杀无制"],
        "成格描述": "透官逢财印，或透财逢食伤",
        "破格描述": "无财官，透煞印",
    },
    "月刃格": {
        "喜": ["正官", "七杀"],    # 官杀制刃
        "忌": ["无官无杀"],
        "成格描述": "官或杀制刃，有制伏",
        "破格描述": "无官无杀，刃气无制",
    },
}

def check_geju_chengbai(geju_name: str, bazi: BaZi) -> tuple[bool, str]:
    """
    判断格局成败（子平凡思：这是"质"的判断，最优先）
    返回：(是否成格, 原因说明)
    """
    if geju_name not in GEJU_CHENGBAI_RULES:
        return True, "格局规则未录入，默认成立"

    rules = GEJU_CHENGBAI_RULES[geju_name]
    rizhu = bazi.ri_zhu_gan

    # 获取命盘中所有透出的十神
    visible_shishen = set()
    for gan_name, _, _ in bazi.all_gan():
        if gan_name != rizhu:
            visible_shishen.add(get_shishen(rizhu, gan_name))

    # 检查是否有忌神破格
    ji_found = [j for j in rules["忌"] if j in visible_shishen]
    xi_found = [x for x in rules["喜"] if x in visible_shishen]

    if ji_found and not xi_found:
        return False, f"破格：{ji_found} 出现且无喜神制化 → {rules['破格描述']}"
    if ji_found and xi_found:
        # 有喜有忌，看力量对比（简化处理）
        return True, f"成败参半：喜神{xi_found}制化忌神{ji_found} → 格局有瑕"
    if xi_found:
        return True, f"成格：{xi_found} 配合 → {rules['成格描述']}"
    return True, "格局基本成立，喜忌均不显"
```

### 7.4 特殊格局：专旺与从格

```python
STRONG_THRESHOLD = 3.0
WEAK_THRESHOLD   = -3.0

# 专旺格（日主五行一统天下）
ZHUAN_WANG_MAP: dict[WuXing, str] = {
    WuXing.WOOD:  "曲直格",
    WuXing.FIRE:  "炎上格",
    WuXing.EARTH: "稼穑格",
    WuXing.METAL: "从革格",
    WuXing.WATER: "润下格",
}

def check_special_geju(bazi: BaZi) -> str | None:
    """检查特殊格局（专旺/从格），无则返回 None"""
    strength = calc_rizhu_strength(bazi)

    if strength > STRONG_THRESHOLD:
        dominant_wx = get_dominant_wuxing(bazi)
        if dominant_wx:
            return ZHUAN_WANG_MAP.get(dominant_wx)

    if strength < WEAK_THRESHOLD:
        follow_wx = get_dominant_other_wuxing(bazi)
        if follow_wx:
            return f"从{follow_wx.value}格"

    return None  # 普通格局
```

---

## 第8章　合冲刑害：干支的动态交互

四柱命盘中的干支并非孤立存在，而是会相互作用。这些作用规则是命理分析中逻辑最复杂的部分。

### 8.1 天干五合

```python
# 天干五合：{frozenset({干A, 干B}): 化合五行}
TIANGAN_HE: dict[frozenset, WuXing] = {
    frozenset({"甲", "己"}): WuXing.EARTH,
    frozenset({"乙", "庚"}): WuXing.METAL,
    frozenset({"丙", "辛"}): WuXing.WATER,
    frozenset({"丁", "壬"}): WuXing.WOOD,
    frozenset({"戊", "癸"}): WuXing.FIRE,
}

def check_tiangan_he(gan_a: str, gan_b: str) -> WuXing | None:
    """检查两天干是否相合，返回化合五行或 None"""
    key = frozenset({gan_a, gan_b})
    return TIANGAN_HE.get(key)
```

### 8.2 地支六合、三合、半合

```python
# 地支六合
DIZHI_LIUHE: dict[frozenset, WuXing] = {
    frozenset({"子", "丑"}): WuXing.EARTH,
    frozenset({"寅", "亥"}): WuXing.WOOD,
    frozenset({"卯", "戌"}): WuXing.FIRE,
    frozenset({"辰", "酉"}): WuXing.METAL,
    frozenset({"巳", "申"}): WuXing.WATER,
    frozenset({"午", "未"}): WuXing.FIRE,  # 部分派别论土
}

# 地支三合局
SANHE: dict[frozenset, WuXing] = {
    frozenset({"申", "子", "辰"}): WuXing.WATER,
    frozenset({"寅", "午", "戌"}): WuXing.FIRE,
    frozenset({"巳", "酉", "丑"}): WuXing.METAL,
    frozenset({"亥", "卯", "未"}): WuXing.WOOD,
}

# 地支半合（三合中取其二）
BANHE: dict[frozenset, WuXing] = {
    frozenset({"申", "子"}): WuXing.WATER,
    frozenset({"子", "辰"}): WuXing.WATER,
    frozenset({"寅", "午"}): WuXing.FIRE,
    frozenset({"午", "戌"}): WuXing.FIRE,
    frozenset({"巳", "酉"}): WuXing.METAL,
    frozenset({"酉", "丑"}): WuXing.METAL,
    frozenset({"亥", "卯"}): WuXing.WOOD,
    frozenset({"卯", "未"}): WuXing.WOOD,
}

def check_sanhe(branches: list[str]) -> WuXing | None:
    """检查地支列表中是否存在三合局"""
    branch_set = set(branches)
    for key, elem in SANHE.items():
        if key.issubset(branch_set):
            return elem
    return None
```

### 8.3 地支六冲、三刑、六害

```python
# 地支六冲（相距6位）
DIZHI_LIUCHONG: list[frozenset] = [
    frozenset({"子", "午"}),
    frozenset({"丑", "未"}),
    frozenset({"寅", "申"}),
    frozenset({"卯", "酉"}),
    frozenset({"辰", "戌"}),
    frozenset({"巳", "亥"}),
]

# 三刑
SAN_XING_GROUP1 = frozenset({"寅", "巳", "申"})   # 持势之刑
SAN_XING_GROUP2 = frozenset({"丑", "戌", "未"})   # 无恩之刑
XING_PAIRS = [frozenset({"子", "卯"})]              # 无礼之刑
ZI_XING = {"辰", "午", "酉", "亥"}                  # 自刑

# 地支六害
LIUHAI: list[frozenset] = [
    frozenset({"子", "未"}),
    frozenset({"丑", "午"}),
    frozenset({"寅", "巳"}),
    frozenset({"卯", "辰"}),
    frozenset({"申", "亥"}),
    frozenset({"酉", "戌"}),
]

def check_liuchong(zhi_a: str, zhi_b: str) -> bool:
    return frozenset({zhi_a, zhi_b}) in DIZHI_LIUCHONG

def check_sanxing(branches: list[str]) -> str | None:
    branch_set = set(branches)
    if SAN_XING_GROUP1.issubset(branch_set): return "持势三刑"
    if SAN_XING_GROUP2.issubset(branch_set): return "无恩三刑"
    for pair in XING_PAIRS:
        if pair.issubset(branch_set): return "无礼相刑"
    # 自刑
    for z in branches:
        if branches.count(z) >= 2 and z in ZI_XING:
            return f"{z}自刑"
    return None
```

### 8.4 合冲的优先级与实现

```python
"""
优先级规则（综合邵伟华与子平凡思视角）：

1. 三合/三会 > 六合 > 半合
2. 合能解冲（贪合忘冲）：
   - 若两支已合化，原有冲力减弱
   - 合局与冲局并存且合化成功，以合局为主
3. 冲能解合：第三支冲入其中一支，合力减弱
4. 格局层面：合冲对格局的影响取决于被合冲的是用神还是忌神
   - 冲用神：格局受损（破格风险）
   - 冲忌神：格局受益（解救效果）
   - 合用神：视情况，可能是"绊住用神"（不利）
"""

def calc_hechong_impact(bazi: BaZi, geju_name: str) -> dict:
    """
    计算命盘中的合冲刑害对格局的综合影响
    """
    zhis = [bazi.year[1], bazi.month[1], bazi.day[1], bazi.hour[1]]
    rizhu = bazi.ri_zhu_gan

    results = {
        "六合": [],
        "三合": [],
        "六冲": [],
        "三刑": None,
        "六害": [],
        "格局影响": [],
    }

    # 检查六合
    for i in range(len(zhis)):
        for j in range(i + 1, len(zhis)):
            key = frozenset({zhis[i], zhis[j]})
            if key in DIZHI_LIUHE:
                results["六合"].append((zhis[i], zhis[j], DIZHI_LIUHE[key]))

    # 检查三合
    sanhe_wx = check_sanhe(zhis)
    if sanhe_wx:
        results["三合"].append(sanhe_wx)

    # 检查六冲
    for i in range(len(zhis)):
        for j in range(i + 1, len(zhis)):
            if check_liuchong(zhis[i], zhis[j]):
                results["六冲"].append((zhis[i], zhis[j]))

    # 检查三刑
    results["三刑"] = check_sanxing(zhis)

    return results
```

---

## 第9章　用神与忌神：三层架构

### 9.0 架构总览

结合子平凡思、子平真诠与邵伟华，用神体系重构为三层架构：

```
第一层（主导层）：格局用神
    └── 由月令取格决定，主导命局成败
    └── 依据：子平真诠体系
    └── 优先级：最高

第二层（修正层）：扶抑用神
    └── 在格局基础上，兼顾日主强弱
    └── 依据：邵伟华《四柱预测学》
    └── 优先级：次之（格局用神矛盾时以格局为准）

第三层（调节层）：调候用神
    └── 考虑生月寒暖，微调格局层次
    └── 依据：《穷通宝鉴》
    └── 优先级：辅助参考
```

### 9.1 格局用神（第一层）

```python
GEJU_YONGSHEN_RULE: dict[str, dict] = {
    "正官格": {
        "用神方向": ["正印", "偏财"],
        "忌神方向": ["伤官", "七杀"],
        "说明": "印护官星，财星生官；忌伤官破官、七杀混杂",
    },
    "七杀格": {
        "用神方向": ["食神", "正印"],
        "忌神方向": ["正财", "偏财"],
        "说明": "食神制杀最纯，印绶化杀次之；忌财星生杀攻身",
    },
    "正印格": {
        "用神方向": ["正官", "七杀"],
        "忌神方向": ["正财"],  # 需细分（见9.2印格逢财专论）
        "说明": "官印双全，杀印相生；财破印需分三情形处理",
    },
    "偏印格": {
        "用神方向": ["七杀", "正官"],
        "忌神方向": ["食神"],
        "说明": "偏印逢官杀有制化；食神被夺则格破",
    },
    "食神格": {
        "用神方向": ["偏财"],
        "忌神方向": ["偏印"],
        "说明": "食神生财最妙；枭神夺食则凶",
    },
    "伤官格": {
        "用神方向": ["正财", "正印"],
        "忌神方向": ["正官"],
        "说明": "伤官生财或佩印；见正官主是非",
    },
    "正财格": {
        "用神方向": ["食神", "正官"],
        "忌神方向": ["七杀", "比劫"],
        "说明": "食生财，财生官；比劫夺财则破",
    },
    "偏财格": {
        "用神方向": ["食神", "正官"],
        "忌神方向": ["七杀", "比劫"],
        "说明": "同正财格，但偏财更忌比劫",
    },
    "建禄格": {
        "用神方向": ["正官", "正财"],
        "忌神方向": [],
        "说明": "透官逢财印，或透财逢食伤皆可",
    },
    "月刃格": {
        "用神方向": ["正官", "七杀"],
        "忌神方向": [],
        "说明": "官杀制刃最佳；无官杀则格低",
    },
}
```

### 9.2 印格逢财专论（子平凡思修正）

这是子平凡思对传统说法的重要修正，原有的"印重身强透财以抑太过"被认为误导了很多学习者：

```python
def analyze_yinju_with_cai(bazi: BaZi) -> str:
    """
    印格遇财的分析（子平凡思修正版）

    ❌ 旧错误模型：印旺身强 → 透财 → 格局有成（"以抑太过"）
    ✅ 正确模型：印格遇财有三种情形，需分别判断

    子平凡思原话：
    "印重身强，透财以抑太过之说，误导了很多人，若是正印格与日主
    无情，岂可说弃便弃？更有违人伦。那些正印重又见正财而事业有成
    的人们，人生多是辛苦异常的。"
    """
    rizhu = bazi.ri_zhu_gan
    zheng_yin_strength = _calc_shishen_strength(bazi, "正印")
    cai_strength       = _calc_shishen_strength(bazi, "正财") + \
                         _calc_shishen_strength(bazi, "偏财")
    has_jiecai         = _has_shishen(bazi, "劫财") or _has_shishen(bazi, "比肩")
    yin_wuqing         = _check_yin_wuqing(bazi)  # 印与日主是否无情

    # ── 情形1：贪财坏印 ──
    # 财重印轻，且无比劫来救印
    if cai_strength > zheng_yin_strength * 1.5 and not has_jiecai:
        return (
            "贪财坏印：格局破败。\n"
            "财重压印，印绶无力护身，日主根基动摇。"
        )

    # ── 情形2：弃印就财 ──
    # 印与日主真正无情（位置、力量均配合失调），财旺可成
    if yin_wuqing and cai_strength > zheng_yin_strength:
        return (
            "弃印就财：格局有成，但人生多辛苦。\n"
            "印与日主配合无情，财星得用，事业以财论。\n"
            "注意：此情形需确认印真的'无情'，不可轻易套用。"
        )

    # ── 情形3：正印逢正财，印旺身强依然有成 ──
    # 子平凡思的核心修正：不能简单套用"财破印"
    if zheng_yin_strength > 0 and not yin_wuqing:
        return (
            "正印逢财：格局基本成立，人生多劳苦。\n"
            "正印如母，正财如父，母遇父未必被破坏。\n"
            "此类命局事业有成者多，但人生多艰辛、多压力，\n"
            "不可以'财破印'论格局破败。"
        )

    return "需综合其他因素进一步判断"
```

### 9.3 扶抑用神（第二层，邵伟华体系）

```python
def get_yongshen_fuyi(bazi: BaZi) -> dict:
    """
    扶抑法求用神（邵伟华体系）
    在格局用神的框架内作补充参考
    """
    strength = calc_rizhu_strength(bazi)
    rz = TIANGAN_MAP[bazi.ri_zhu_gan]
    rz_wx = rz.wuxing

    if strength < -0.5:   # 日主偏弱
        yongshen_wx = [
            GENERATES[CONTROLS[rz_wx]],  # 生我的五行（印）
            rz_wx,                        # 同类（比劫）
        ]
        jishen_wx = [
            GENERATES[rz_wx],             # 我生的五行（食伤）
            CONTROLS[rz_wx],              # 克我的五行（官杀）
        ]
        label = "日主偏弱，喜印比"
    elif strength > 0.5:  # 日主偏旺
        yongshen_wx = [
            CONTROLS[rz_wx],              # 克我（官杀）
            GENERATES[rz_wx],             # 我生（食伤泄秀）
        ]
        jishen_wx = [
            GENERATES[CONTROLS[rz_wx]],  # 生我（印）
            rz_wx,                        # 同类（比劫）
        ]
        label = "日主偏旺，喜官食"
    else:
        yongshen_wx = []
        jishen_wx   = []
        label = "日主中和，以格局用神为准"

    return {
        "强弱判断": label,
        "扶抑用神": [wx.value for wx in yongshen_wx],
        "扶抑忌神": [wx.value for wx in jishen_wx],
        "强弱数值": round(strength, 2),
    }
```

### 9.4 调候用神（第三层）

```python
# 调候用神表（节选，完整表约120条）
# 格式：(日主天干, 出生月支) -> 优先用神列表
TIAOHUO_TABLE: dict[tuple[str, str], list[str]] = {
    ("甲", "子"): ["丁", "庚", "丙"],  # 冬木，用丁火温暖，庚金修剪
    ("甲", "丑"): ["丁", "庚", "丙"],
    ("甲", "午"): ["癸", "丁", "庚"],  # 夏木，先用癸水润泽
    ("甲", "未"): ["癸", "丁", "庚"],
    ("丙", "子"): ["壬", "戊"],        # 冬火，用壬水引通
    ("丙", "亥"): ["壬", "戊"],
    ("庚", "午"): ["壬", "丁", "甲"],  # 夏金，喜水冷却
    ("庚", "巳"): ["壬", "丁", "戊"],
    ("壬", "午"): ["庚", "辛", "癸"],  # 夏水，喜金生
    # ... 完整表请参考《穷通宝鉴》
}

def get_yongshen_tiaohuo(rizhu_gan: str, month_zhi: str) -> list[str]:
    key = (rizhu_gan, month_zhi)
    return TIAOHUO_TABLE.get(key, [])
```

### 9.5 综合用神（三层整合）

```python
def get_yongshen_comprehensive(bazi: BaZi) -> dict:
    """综合用神（三层架构）"""
    geju_name = get_geju_name(bazi)
    geju_yongshen = GEJU_YONGSHEN_RULE.get(geju_name, {})

    fuyi = get_yongshen_fuyi(bazi)
    tiaohuo = get_yongshen_tiaohuo(bazi.ri_zhu_gan, bazi.month[1])

    # 三层有矛盾时，格局用神优先（子平凡思原则）
    return {
        "格局用神（第一层）": geju_yongshen.get("用神方向", []),
        "格局忌神（第一层）": geju_yongshen.get("忌神方向", []),
        "扶抑用神（第二层）": fuyi["扶抑用神"],
        "调候建议（第三层）": tiaohuo,
        "优先原则": "格局用神 > 扶抑用神 > 调候建议",
        "日主强弱": fuyi["强弱判断"],
    }
```

---

## 第10章　神煞：附加标签系统

神煞是命理系统中的"附加 tag"，本质是基于特定规则查表得到的标签。

**子平凡思对神煞的定位**：
- 格局主导"成与败"（质），神煞主导"轻与重"（量）
- "格局既成，即使满盘孤辰入煞，何损其贵？格局既破，即使满盘天德贵人，何以为功？"
- 但在六亲、寿夭等具体事象上，神煞往往具有关键作用

### 10.1 神煞的查表算法

```python
# 天乙贵人（由日主天干查对应地支）
TIANYI_GUIREN: dict[str, list[str]] = {
    "甲": ["丑", "未"], "戊": ["丑", "未"],
    "乙": ["子", "申"], "己": ["子", "申"],
    "丙": ["亥", "酉"], "庚": ["亥", "酉"],
    "丁": ["亥", "酉"], "辛": ["寅", "午"],
    "壬": ["卯", "巳"], "癸": ["卯", "巳"],
}

# 文昌贵人（由日主天干查）
WENCHANG_GUIREN: dict[str, str] = {
    "甲": "巳", "乙": "午", "丙": "申", "丁": "酉",
    "戊": "申", "己": "酉", "庚": "亥", "辛": "子",
    "壬": "寅", "癸": "卯",
}

# 驿马星（由年支或日支所在三合局查）
YIMA: dict[str, str] = {
    "申": "寅", "子": "寅", "辰": "寅",  # 申子辰→寅
    "寅": "申", "午": "申", "戌": "申",  # 寅午戌→申
    "亥": "巳", "卯": "巳", "未": "巳",  # 亥卯未→巳
    "巳": "亥", "酉": "亥", "丑": "亥",  # 巳酉丑→亥
}

def check_all_shensha(bazi: BaZi) -> dict[str, list[str]]:
    """检查命盘中所有主要神煞"""
    rizhu = bazi.ri_zhu_gan
    all_zhis = [bazi.year[1], bazi.month[1], bazi.day[1], bazi.hour[1]]
    pillar_names = ["年支", "月支", "日支", "时支"]
    result: dict[str, list[str]] = {}

    # 天乙贵人
    tianyi_targets = TIANYI_GUIREN.get(rizhu, [])
    hits = [pillar_names[i] for i, z in enumerate(all_zhis) if z in tianyi_targets]
    if hits: result["天乙贵人"] = hits

    # 文昌贵人
    wc_target = WENCHANG_GUIREN.get(rizhu)
    if wc_target:
        hits = [pillar_names[i] for i, z in enumerate(all_zhis) if z == wc_target]
        if hits: result["文昌贵人"] = hits

    # 驿马
    yima_targets = {YIMA.get(z) for z in all_zhis if YIMA.get(z)}
    hits = [pillar_names[i] for i, z in enumerate(all_zhis) if z in yima_targets]
    if hits: result["驿马"] = hits

    return result
```

### 10.2 常用神煞速查

| 神煞 | 查法依据 | 性质 | 简要含义 |
|------|----------|------|----------|
| 天乙贵人 | 日主天干 | 吉 | 逢凶化吉，得贵人扶助 |
| 文昌贵人 | 日主天干 | 吉 | 聪慧好学，利文职 |
| 驿马星   | 年/日支三合局 | 动 | 奔波移动，变动频繁 |
| 桃花     | 年/日支 | 情 | 异性缘、人缘好 |
| 将星     | 年支 | 吉 | 领导力，事业运强 |
| 羊刃     | 日主天干 | 凶 | 性烈，逢冲激发凶险 |
| 魁罡     | 日柱整体 | 强 | 刚烈果断，成败分明 |
| 孤辰寡宿 | 年支 | 孤 | 感情路坎坷，婚姻迟 |
| 华盖     | 年/日支 | 艺 | 孤高、才艺、宗教缘 |

---

## 第11章　综合断命：推理模型的构建

### 11.1 子平凡思体系的分析流程

```python
"""
子平凡思格局优先分析流程

核心原则：
1. 原局是命运的硬件规格（上限）
2. 格局决定质（成与败）
3. 大运决定格局实现程度
4. 其余因素调节量级

"一个乞丐，他的大运好到了天上，也依然是乞丐，
不会脱离八字原局给他注定的范畴。"
                    —— 子平凡思
"""

ANALYSIS_FLOW_FANSI = """
输入：出生年月日时 + 性别
  │
  ▼
① 排出四柱（推荐使用 lunar-python）
  │
  ▼
② 月令取格（确定格局名称）
  ← 这是大局，最优先
  │
  ▼
③ 判断格局成败（质的判断）
  ← 有喜神辅助？有忌神破坏？
  ← 破格的"破"仍会应验于事象
  │
  ▼
④ 确定格局用神（第一层）
  ← 由格局规则表查询
  │
  ▼
⑤ 参考扶抑用神（第二层）
  ← 与格局用神有矛盾时，格局优先
  │
  ▼
⑥ 检查合冲刑害
  ← 对格局用神的影响（冲用神=破格风险）
  │
  ▼
⑦ 附加神煞（量级调节，非主导）
  │
  ▼
⑧ 大运分析：用神运/忌神运
  ← 大运不改变原局上限，只决定实现程度
  │
  ▼
⑨ 流年叠加
  │
  ▼
输出：格局层次 + 各时期运势实现程度
"""
```

### 11.2 邵伟华体系的分析流程

```python
ANALYSIS_FLOW_SHAO = """
输入：出生年月日时 + 性别
  │
  ▼
① 排出四柱 + 大运
  │
  ▼
② 找出日主，判断强弱
  │
  ▼
③ 确定用神、忌神（扶抑为主，调候为辅）
  │
  ▼
④ 分析十神分布：六亲、事业、感情基础格局
  │
  ▼
⑤ 检查合冲刑害对各柱的影响
  │
  ▼
⑥ 附加神煞
  │
  ▼
⑦ 逐步大运分析：每步大运的用忌神力量变化
  │
  ▼
⑧ 流年叠加：当年干支对命盘的冲激
  │
  ▼
输出：各时间段的吉凶趋势 + 六亲事业健康概述
"""
```

### 11.3 两套体系的对比

| 维度 | 邵伟华体系 | 子平真诠/子平凡思体系 |
|------|-----------|----------------------|
| 核心抓手 | 日主强弱 | 格局成败 |
| 用神来源 | 五行扶抑 | 月令格局 |
| 强弱地位 | 第一位 | 格局内的参数 |
| 神煞使用 | 较重视 | 辅助量级，不决定成败 |
| 适合人群 | 入门学习 | 深化研究 |
| 理论依据 | 《四柱预测学》 | 《子平真诠》《子平凡思博客》 |

### 11.4 六亲、事业、健康推断框架

```python
"""
六亲推断框架（以男命为例）：

父亲：偏财（为父之星）
  → 偏财旺且无损：父亲健在且有力
  → 偏财被克/合去：父缘薄，早丧或疏远

妻子：正财
  → 正财旺且坐日支：婚姻稳固
  → 正财被劫财夺：婚姻受损，多竞争者
  → 注意：日支为妻宫，宫位与星位需结合看

子女：食神/伤官（食伤为子女星）
  → 食神健旺：子女聪明，缘分好
  → 食神被枭神（偏印）夺：不利子女

母亲：正印
  → 正印有根且透干：母亲健康、有影响力
  → 正印被财破：母缘薄

兄弟：比肩/劫财
  → 多比劫：兄弟多，但也主竞争、破财

──────────────────────────────

事业推断框架：
  正官格 / 七杀格成立：适合体制内、管理岗位
  食神格 / 伤官格成立：适合自由职业、技术创意
  财格成立：适合商业、理财
  印格成立：适合学术、教育、文职

官杀混杂且无制：事业多变，压力大
伤官见官：官非是非，仕途阻碍

──────────────────────────────

健康推断框架（五行对应脏腑）：
  木弱（甲乙受克/休囚）：肝胆、筋骨、视力
  火弱（丙丁受克/休囚）：心脏、血压、视力
  土弱（戊己受克/休囚）：脾胃、消化系统
  金弱（庚辛受克/休囚）：肺、皮肤、大肠、呼吸
  水弱（壬癸受克/休囚）：肾脏、泌尿、骨骼

大运流年逢剋洩日主元气，且命局原本薄弱的五行再度受损 →
此时段为健康警示期，宜主动保健
"""
```

---

## 第12章　实断框架：从代码到推命

### 12.1 大运上限原则

子平凡思有一句话值得反复思考：

> "一个乞丐，他的大运好到了天上，也依然是乞丐，不会脱离八字原局给他'注定'的范畴。"

这对应一个重要工程约束：**原局是系统的硬件规格，大运是运行时环境，运行时环境不能提升硬件规格上限。**

```python
@dataclass
class GeJuResult:
    name:   str     # 格局名称
    is_cheng: bool  # 质：格局是否成立（二元）
    level:  float   # 量：格局层次（0.0–10.0）
    reason: str     # 成败原因

def predict_dayun_period(
    bazi: BaZi,
    geju_result: GeJuResult,
    dayun_gan: str,
    dayun_zhi: str,
    start_age: int
) -> dict:
    """
    大运预测：大运不能超越原局的上限
    """
    base_ceiling = geju_result.level   # 原局层次上限

    # 大运天干对用神的影响
    dayun_fit_gan = calc_yongshen_fit_score(bazi, dayun_gan)
    dayun_fit_zhi = calc_yongshen_fit_score(bazi, dayun_zhi)

    # 干支各有侧重（前五年干重，后五年支重）
    dayun_fit_avg = dayun_fit_gan * 0.5 + dayun_fit_zhi * 0.5

    # 大运好时趋近上限，大运差时跌落下限
    if dayun_fit_avg > 0:    # 用神运
        period_level = base_ceiling * (0.6 + 0.4 * min(dayun_fit_avg, 1.0))
    elif dayun_fit_avg < 0:  # 忌神运
        period_level = base_ceiling * max(0.1, 1.0 + 0.5 * dayun_fit_avg)
    else:
        period_level = base_ceiling * 0.6

    return {
        "大运":   f"{dayun_gan}{dayun_zhi}",
        "起运年龄": start_age,
        "原局上限": round(base_ceiling, 2),
        "本运层次": round(period_level, 2),
        "大运性质": "用神运" if dayun_fit_avg > 0 else "忌神运" if dayun_fit_avg < 0 else "平运",
        "注意": "大运层次不会超过原局上限",
    }
```

### 12.2 完整分析器示例

```python
class BaZiFullAnalyzer:
    """
    四柱完整分析器
    整合子平凡思格局优先 + 邵伟华扶抑 + 子平真诠格局用神
    """

    def analyze(self, bazi: BaZi, gender: str = "男") -> dict:
        result = {}

        # ── 第一层：格局（最优先）──
        geju_name = get_geju_name(bazi)
        is_cheng, chengbai_reason = check_geju_chengbai(geju_name, bazi)
        geju_level = self._calc_geju_level(bazi, geju_name, is_cheng)

        result["格局"] = {
            "名称": geju_name,
            "是否成格": is_cheng,
            "成败原因": chengbai_reason,
            "格局层次": round(geju_level, 2),
        }

        # ── 第二层：日主强弱（辅助参考）──
        strength = calc_rizhu_strength(bazi)
        result["日主强弱"] = {
            "数值": round(strength, 2),
            "判断": "偏旺" if strength > 0.5 else "偏弱" if strength < -0.5 else "中和",
        }

        # ── 第三层：用神体系 ──
        result["用神"] = get_yongshen_comprehensive(bazi)

        # ── 合冲刑害 ──
        result["合冲刑害"] = calc_hechong_impact(bazi, geju_name)

        # ── 神煞（量级修正）──
        result["神煞"] = check_all_shensha(bazi)
        result["神煞说明"] = "神煞影响格局层次（量），不决定格局成败（质）"

        # ── 综合层次 ──
        shensha_mod = len(result["神煞"]) * 0.1  # 简化：每个吉神+0.1
        result["综合层次"] = round(
            min(10.0, max(0.0, geju_level + shensha_mod)), 2
        )

        return result

    def _calc_geju_level(
        self, bazi: BaZi, geju_name: str, is_cheng: bool
    ) -> float:
        if not is_cheng:
            return 1.0  # 破格基础分

        base = 5.0
        # 用神是否透干得根（有力）
        yongshen_list = GEJU_YONGSHEN_RULE.get(geju_name, {}).get("用神方向", [])
        for ss in yongshen_list:
            if self._shishen_is_strong(bazi, ss):
                base += 1.0
        # 忌神是否透干（破格风险）
        jishen_list = GEJU_YONGSHEN_RULE.get(geju_name, {}).get("忌神方向", [])
        for ss in jishen_list:
            if self._shishen_is_visible(bazi, ss):
                base -= 1.5
        return base

    def _shishen_is_strong(self, bazi: BaZi, ss_name: str) -> bool:
        """某十神是否透干且有根"""
        rizhu = bazi.ri_zhu_gan
        for gan, _, _ in bazi.all_gan():
            if gan != rizhu and get_shishen(rizhu, gan) == ss_name:
                return True
        return False

    def _shishen_is_visible(self, bazi: BaZi, ss_name: str) -> bool:
        """某十神是否透出天干"""
        return self._shishen_is_strong(bazi, ss_name)


# 使用示例
if __name__ == "__main__":
    # 示例：1990年5月15日 8时 男命
    # （实际使用时用 lunar-python 获取真实八字）
    bazi = BaZi(
        year  = ("庚", "午"),
        month = ("辛", "巳"),
        day   = ("甲", "子"),
        hour  = ("丙", "辰"),
    )

    analyzer = BaZiFullAnalyzer()
    result = analyzer.analyze(bazi, gender="男")

    print("=" * 50)
    print(f"日主：{bazi.ri_zhu_gan}")
    print(f"格局：{result['格局']['名称']}")
    print(f"成格：{result['格局']['是否成格']}")
    print(f"原因：{result['格局']['成败原因']}")
    print(f"格局层次：{result['格局']['格局层次']} / 10")
    print(f"日主强弱：{result['日主强弱']['判断']} ({result['日主强弱']['数值']})")
    print(f"综合层次：{result['综合层次']} / 10")
    print(f"神煞：{list(result['神煞'].keys())}")
```

---

# 附录

## 附录A　完整数据表

### 天干完整属性表

| 序号 | 天干 | 阴阳 | 五行 | 对应数字 |
|------|------|------|------|----------|
| 0 | 甲 | 阳 | 木 | 3 |
| 1 | 乙 | 阴 | 木 | 8 |
| 2 | 丙 | 阳 | 火 | 7 |
| 3 | 丁 | 阴 | 火 | 2 |
| 4 | 戊 | 阳 | 土 | 5 |
| 5 | 己 | 阴 | 土 | 10 |
| 6 | 庚 | 阳 | 金 | 9 |
| 7 | 辛 | 阴 | 金 | 4 |
| 8 | 壬 | 阳 | 水 | 1 |
| 9 | 癸 | 阴 | 水 | 6 |

### 地支藏干完整速查表

| 地支 | 主气 | 中气 | 余气 |
|------|------|------|------|
| 子   | 癸   | —   | —   |
| 丑   | 己   | 癸   | 辛   |
| 寅   | 甲   | 丙   | 戊   |
| 卯   | 乙   | —   | —   |
| 辰   | 戊   | 乙   | 癸   |
| 巳   | 丙   | 庚   | 戊   |
| 午   | 丁   | 己   | —   |
| 未   | 己   | 丁   | 乙   |
| 申   | 庚   | 壬   | 戊   |
| 酉   | 辛   | —   | —   |
| 戌   | 戊   | 辛   | 丁   |
| 亥   | 壬   | 甲   | —   |

---

## 附录B　合冲刑害速查表

**地支六合**

| 组合 | 化合五行 |
|------|---------|
| 子丑 | 土 |
| 寅亥 | 木 |
| 卯戌 | 火 |
| 辰酉 | 金 |
| 巳申 | 水 |
| 午未 | 火（或土） |

**地支六冲**

子午 · 丑未 · 寅申 · 卯酉 · 辰戌 · 巳亥

**地支三合**

| 三合局 | 五行 | 旺支（仲支）|
|--------|------|-----------|
| 申子辰 | 水   | 子         |
| 寅午戌 | 火   | 午         |
| 巳酉丑 | 金   | 酉         |
| 亥卯未 | 木   | 卯         |

**地支三刑**

| 类型 | 组合 |
|------|------|
| 持势之刑 | 寅巳申 |
| 无恩之刑 | 丑戌未 |
| 无礼之刑 | 子卯 |
| 自刑   | 辰辰 / 午午 / 酉酉 / 亥亥 |

**地支六害**

子未 · 丑午 · 寅巳 · 卯辰 · 申亥 · 酉戌

---

## 附录C　推荐工具与开源资源

### 排盘工具（直接使用，无需自行实现）

| 工具 | 语言 | 说明 |
|------|------|------|
| `lunar-python` | Python | 功能全面，含节气、大运、神煞；`pip install lunar-python` |
| `lunar-javascript` | JavaScript | 前端友好，接口清晰 |
| `sxtwl` | Python/C++ | 高精度天文历，节气精确到分钟 |

### 关键文献

| 文献 | 说明 |
|------|------|
| 邵伟华《四柱预测学》 | 入门首选，体系完整，案例丰富 |
| 沈孝瞻《子平真诠》（徐乐吾评注版） | 格局用神的权威原典 |
| 子平凡思新浪博客 | 现代格局派重要注疏，含《子平真诠的是与非》系列 |
| 袁树珊《命谱》 | 大量实际命例，适合对照验证 |
| 《穷通宝鉴》（徐乐吾《造化元钥》） | 调候用神参考文献 |
| 任铁樵《滴天髓》 | 旺衰派经典，与格局派互补 |

---

## 附录D　子平凡思贡献摘要

子平凡思是新浪博客命理作者（博客ID：blog_59c85de1），以"正官""七杀"对话体著称，代表作包括《子平真诠的是与非》系列、《三命别裁》系列、《看命口诀解读》等。其核心理论贡献如下：

| 原有说法 | 子平凡思修正 | 工程启示 |
|----------|-------------|---------|
| 印旺身强透财以抑太过 | 正印逢财分三情形，不可简单套用 | 避免将五行生克直接映射为格局成败 |
| 神煞决定贵贱 | 神煞影响"量"，格局决定"质" | 神煞是配置参数，不是主程序分支 |
| 五行生克主导断命 | 六亲生克（情义）比五行更有内涵 | 增加"有情/无情"维度，不只是矩阵运算 |
| 大运好则运势好 | 原局是天花板，大运决定实现率 | 大运是运行时参数，不改变系统规格 |
| 格局破则弃之 | 破格的"破"仍会应验于事象 | 成败判断 ≠ 事象不会发生 |
| 月令无用取外格 | 月令格局与外格可并存 | 多格局并行处理，主次分明 |
| 五行是客观真理 | 五行是反推式的安立，是一个模型 | 工程师的元认知：我们在实现约定，不是发现真理 |

**子平凡思名言（适合贴在显示器旁）：**

> "五行是反推式的安立，说白了也是一个模型，假如当初安立的不是五行是六行，现在也一样使用。"

> "一个乞丐，他的大运好到了天上，也依然是乞丐，不会脱离八字原局给他'注定'的范畴。"

> "人的命造，区区八个字，却表达着这个命局最主要的一种或几种事象、规律，把握了这个大局，则可以层层展开分析，丝丝入扣。"

> "六亲生克显然比五行生克更能体现六神的内涵。"

---

## 写在最后

四柱命理是一套经过千年演化的符号推理系统，其内部规则有大量门派分歧和历史沉积。本书以编程教科书的方式整理其数据结构与算法逻辑，目的是帮助读者建立清晰的系统性认知，而不是提供一套"正确答案"。

子平凡思对这套系统保持了清醒的元认知——他知道五行是模型，知道模型可以换，知道有些规则是"约定俗成的适者生存"而非"天然正确的宇宙真理"。这种态度，和一个好的工程师面对遗留系统时的态度，惊人地相似：尊重历史约定，理解它的内在逻辑，在边界内精确运作，而不是把它当作神谕。

真正的命理推断需要大量实践和对经典文献的深入研读，算法只是起点。

---

*本书基于子平真诠格局体系、邵伟华扶抑体系、子平凡思博客理论整合编写。*  
*代码仅供学习参考，不构成命理断言。*
