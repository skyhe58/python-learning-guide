# 日期时间处理

> **模块：** 02-常用功能
> **难度：** 入门
> **前置知识：** Python 基础（01-python-basics）
> **Python 版本：** >= 3.9
> **最后验证日期：** 2025-07-15

## 概念说明

Python 的 `datetime` 模块是处理日期和时间的标准库，提供了 `date`、`time`、`datetime`、`timedelta`、`timezone` 等核心类。对于 Java 开发者来说，Python 的日期时间 API 比 Java 8 之前的 `Date`/`Calendar` 简洁得多，与 Java 8 引入的 `java.time` 包（`LocalDate`/`LocalDateTime`/`Duration`）在设计理念上比较接近。

日期时间处理的三大核心场景：
1. **获取与创建** — `datetime.now()`、`datetime(2025, 7, 15)` 创建日期时间对象
2. **格式化与解析** — `strftime()` 将日期转为字符串，`strptime()` 将字符串解析为日期
3. **时间运算** — `timedelta` 进行日期加减，支持日期比较和排序

时区处理是日期时间中最容易出错的部分。Python 3.9+ 推荐使用标准库 `zoneinfo` 模块处理时区（替代第三方库 `pytz`），它提供了 IANA 时区数据库的完整支持。

### 核心类一览

| 类 | 说明 | 类比 Java |
|------|------|-----------|
| `datetime.date` | 日期（年月日） | `java.time.LocalDate` |
| `datetime.time` | 时间（时分秒） | `java.time.LocalTime` |
| `datetime.datetime` | 日期+时间 | `java.time.LocalDateTime` |
| `datetime.timedelta` | 时间差 | `java.time.Duration` / `Period` |
| `datetime.timezone` | 固定偏移时区 | `java.time.ZoneOffset` |
| `zoneinfo.ZoneInfo` | IANA 时区（3.9+） | `java.time.ZoneId` |

### 常用日期格式化代码

| 代码 | 说明 | 示例 |
|------|------|------|
| `%Y` | 四位年份 | `2025` |
| `%m` | 两位月份 | `07` |
| `%d` | 两位日期 | `15` |
| `%H` | 24 小时制小时 | `14` |
| `%M` | 分钟 | `30` |
| `%S` | 秒 | `45` |
| `%f` | 微秒 | `000000` |
| `%A` | 星期全名 | `Tuesday` |
| `%a` | 星期缩写 | `Tue` |
| `%B` | 月份全名 | `July` |
| `%z` | UTC 偏移 | `+0800` |
| `%Z` | 时区名称 | `CST` |
| `%j` | 一年中的第几天 | `196` |
| `%W` | 一年中的第几周 | `28` |

## Java 对比

| 特性 | Java (`java.time`) | Python (`datetime`) |
|------|-------------------|---------------------|
| 获取当前时间 | `LocalDateTime.now()` | `datetime.now()` |
| 创建日期 | `LocalDate.of(2025, 7, 15)` | `date(2025, 7, 15)` |
| 格式化 | `DateTimeFormatter.ofPattern("yyyy-MM-dd")` | `strftime("%Y-%m-%d")` |
| 解析 | `LocalDate.parse("2025-07-15")` | `strptime("2025-07-15", "%Y-%m-%d")` |
| 时间差 | `Duration.between(a, b)` | `b - a`（返回 `timedelta`） |
| 加减天数 | `date.plusDays(7)` | `date + timedelta(days=7)` |
| 时区 | `ZoneId.of("Asia/Shanghai")` | `ZoneInfo("Asia/Shanghai")` |

**Java 写法：**
```java
import java.time.*;
import java.time.format.DateTimeFormatter;

// 获取当前时间
LocalDateTime now = LocalDateTime.now();

// 格式化
DateTimeFormatter fmt = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");
String formatted = now.format(fmt);

// 解析
LocalDate date = LocalDate.parse("2025-07-15");

// 时间运算
LocalDate nextWeek = date.plusDays(7);
Duration duration = Duration.between(now, now.plusHours(2));
```

**Python 写法：**
```python
from datetime import datetime, date, timedelta

# 获取当前时间
now = datetime.now()

# 格式化
formatted = now.strftime("%Y-%m-%d %H:%M:%S")

# 解析
d = datetime.strptime("2025-07-15", "%Y-%m-%d")

# 时间运算（更直观的运算符重载）
next_week = d + timedelta(days=7)
duration = timedelta(hours=2)
```

## 实战代码

### 示例：日期时间处理完整演示

**文件：** `examples/datetime_demo.py`

演示 `datetime` 模块的核心功能：获取当前日期时间、格式化与解析（strftime/strptime）、timedelta 时间运算、timezone 时区处理、日期比较和排序、常用日期格式。

**运行方式：**
```bash
python examples/datetime_demo.py
```

**预期输出：**
```
========== 获取当前日期时间 ==========
当前日期时间: 2025-07-15 14:30:00
当前日期: 2025-07-15
当前时间: 14:30:00
时间戳: 1752566400.0

========== 格式化与解析 ==========
--- strftime 格式化 ---
ISO 格式: 2025-07-15T14:30:00
中文格式: 2025年07月15日 14:30:00
紧凑格式: 20250715
--- strptime 解析 ---
解析结果: 2025-07-15 14:30:00
解析日期: 2025-03-20 00:00:00

========== timedelta 时间运算 ==========
今天: 2025-07-15
7天后: 2025-07-22
30天前: 2025-06-15
两个日期相差: 37 天
2小时30分后: 2025-07-15 17:00:00

========== 时区处理 ==========
UTC 时间: 2025-07-15 06:30:00+00:00
北京时间: 2025-07-15 14:30:00+08:00
东京时间: 2025-07-15 15:30:00+09:00
纽约时间: 2025-07-15 02:30:00-04:00

========== 日期比较和排序 ==========
2025-01-01 < 2025-07-15 < 2025-12-31
排序结果: [datetime.date(2025, 1, 1), datetime.date(2025, 7, 15), datetime.date(2025, 12, 31)]

========== 常用日期格式 ==========
ISO 8601: 2025-07-15T14:30:00
RFC 2822: Tue, 15 Jul 2025 14:30:00
日志格式: 2025-07-15 14:30:00.000000
文件名安全: 20250715_143000
```

## 常见陷阱

### 1. strftime 和 strptime 的格式代码不同于 Java

Java 使用 `yyyy-MM-dd`，Python 使用 `%Y-%m-%d`，格式代码完全不同。

```python
# ✗ 错误：使用 Java 的格式代码
datetime.strptime("2025-07-15", "yyyy-MM-dd")  # ValueError!

# ✓ 正确：使用 Python 的格式代码
datetime.strptime("2025-07-15", "%Y-%m-%d")
```

### 2. naive datetime vs aware datetime

没有时区信息的 datetime 称为 "naive"，有时区信息的称为 "aware"。两者不能直接比较。

```python
from datetime import datetime, timezone

naive = datetime.now()           # naive：无时区
aware = datetime.now(timezone.utc)  # aware：有时区

# ✗ 错误：naive 和 aware 不能比较
# naive < aware  # TypeError!

# ✓ 正确：统一为 aware 或统一为 naive
aware2 = naive.replace(tzinfo=timezone.utc)
```

### 3. timedelta 不支持月和年

`timedelta` 只支持天、秒、微秒，不支持"加 1 个月"或"加 1 年"。

```python
from datetime import timedelta

# ✓ 支持
delta = timedelta(days=7, hours=2, minutes=30)

# ✗ 不支持
# delta = timedelta(months=1)  # TypeError!

# 需要手动处理月份加减
from datetime import date
d = date(2025, 1, 31)
# "加一个月" 需要自己处理月末问题
```

### 4. datetime.now() vs datetime.utcnow()

`datetime.utcnow()` 在 Python 3.12 中已被弃用，应使用 `datetime.now(timezone.utc)`。

```python
from datetime import datetime, timezone

# ✗ 已弃用（Python 3.12+）
# utc_now = datetime.utcnow()  # 返回 naive datetime！

# ✓ 推荐
utc_now = datetime.now(timezone.utc)  # 返回 aware datetime
```

> 💻 **完整可运行代码：** [datetime_demo.py](examples/datetime_demo.py)

## 参考资料

- [Python 官方文档 - datetime](https://docs.python.org/zh-cn/3/library/datetime.html)
- [Python 官方文档 - zoneinfo](https://docs.python.org/zh-cn/3/library/zoneinfo.html)
- [Python strftime 格式代码参考](https://strftime.org/)
- [Real Python - Python datetime](https://realpython.com/python-datetime/)
