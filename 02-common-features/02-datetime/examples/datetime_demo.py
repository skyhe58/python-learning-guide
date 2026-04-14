#!/usr/bin/env python3
"""
Python 日期时间处理完整演示

模块: 02-常用功能
知识点: 日期时间处理
Python 版本: >= 3.9
最后验证: 2025-07-15

运行方式:
    python datetime_demo.py

描述:
    演示 datetime 模块的核心功能：
    1. 获取当前日期时间
    2. 格式化与解析（strftime/strptime）
    3. timedelta 时间运算
    4. timezone 时区处理
    5. 日期比较和排序
    6. 常用日期格式
"""

from datetime import datetime, date, time, timedelta, timezone
from zoneinfo import ZoneInfo


# ============================================================
# 1. 获取当前日期时间
# ============================================================

def demo_current_datetime():
    """获取当前日期时间的各种方式"""
    print("=" * 10, "获取当前日期时间", "=" * 10)

    # 类似 Java: LocalDateTime.now()
    now = datetime.now()
    print(f"当前日期时间: {now.strftime('%Y-%m-%d %H:%M:%S')}")

    # 类似 Java: LocalDate.now()
    today = date.today()
    print(f"当前日期: {today}")

    # 获取时间部分
    current_time = now.time()
    print(f"当前时间: {current_time.strftime('%H:%M:%S')}")

    # 时间戳（Unix timestamp）
    # 类似 Java: Instant.now().getEpochSecond()
    timestamp = now.timestamp()
    print(f"时间戳: {timestamp}")

    print()


# ============================================================
# 2. 格式化与解析
# ============================================================

def demo_format_parse():
    """strftime 格式化和 strptime 解析"""
    print("=" * 10, "格式化与解析", "=" * 10)

    now = datetime(2025, 7, 15, 14, 30, 0)

    # --- strftime：datetime -> 字符串 ---
    # 类似 Java: DateTimeFormatter.ofPattern("yyyy-MM-dd").format(date)
    # 注意：Python 用 %Y-%m-%d，Java 用 yyyy-MM-dd
    print("--- strftime 格式化 ---")

    iso_format = now.strftime("%Y-%m-%dT%H:%M:%S")
    print(f"ISO 格式: {iso_format}")

    cn_format = now.strftime("%Y年%m月%d日 %H:%M:%S")
    print(f"中文格式: {cn_format}")

    compact = now.strftime("%Y%m%d")
    print(f"紧凑格式: {compact}")

    # --- strptime：字符串 -> datetime ---
    # 类似 Java: LocalDateTime.parse("2025-07-15T14:30:00")
    print("--- strptime 解析 ---")

    dt1 = datetime.strptime("2025-07-15 14:30:00", "%Y-%m-%d %H:%M:%S")
    print(f"解析结果: {dt1}")

    dt2 = datetime.strptime("2025/03/20", "%Y/%m/%d")
    print(f"解析日期: {dt2}")

    print()


# ============================================================
# 3. timedelta 时间运算
# ============================================================

def demo_timedelta():
    """timedelta 进行日期加减运算"""
    print("=" * 10, "timedelta 时间运算", "=" * 10)

    today = date(2025, 7, 15)
    now = datetime(2025, 7, 15, 14, 30, 0)

    # 日期加减
    # 类似 Java: date.plusDays(7) / date.minusDays(30)
    # Python 使用运算符重载，更直观
    next_week = today + timedelta(days=7)
    last_month = today - timedelta(days=30)
    print(f"今天: {today}")
    print(f"7天后: {next_week}")
    print(f"30天前: {last_month}")

    # 两个日期相减得到 timedelta
    # 类似 Java: ChronoUnit.DAYS.between(date1, date2)
    diff = next_week - last_month
    print(f"两个日期相差: {diff.days} 天")

    # 时间加减
    later = now + timedelta(hours=2, minutes=30)
    print(f"2小时30分后: {later.strftime('%Y-%m-%d %H:%M:%S')}")

    print()


# ============================================================
# 4. 时区处理
# ============================================================

def demo_timezone():
    """timezone 和 zoneinfo 时区处理"""
    print("=" * 10, "时区处理", "=" * 10)

    # 创建 UTC 时间（aware datetime）
    # 类似 Java: ZonedDateTime.now(ZoneId.of("UTC"))
    utc_now = datetime(2025, 7, 15, 6, 30, 0, tzinfo=timezone.utc)
    print(f"UTC 时间: {utc_now}")

    # 使用 zoneinfo（Python 3.9+）转换时区
    # 类似 Java: ZonedDateTime.withZoneSameInstant(ZoneId.of("Asia/Shanghai"))
    beijing_tz = ZoneInfo("Asia/Shanghai")
    beijing_time = utc_now.astimezone(beijing_tz)
    print(f"北京时间: {beijing_time}")

    tokyo_tz = ZoneInfo("Asia/Tokyo")
    tokyo_time = utc_now.astimezone(tokyo_tz)
    print(f"东京时间: {tokyo_time}")

    ny_tz = ZoneInfo("America/New_York")
    ny_time = utc_now.astimezone(ny_tz)
    print(f"纽约时间: {ny_time}")

    print()


# ============================================================
# 5. 日期比较和排序
# ============================================================

def demo_comparison():
    """日期比较和排序"""
    print("=" * 10, "日期比较和排序", "=" * 10)

    d1 = date(2025, 1, 1)
    d2 = date(2025, 7, 15)
    d3 = date(2025, 12, 31)

    # 日期可以直接比较
    # 类似 Java: date1.isBefore(date2)
    # Python 直接用 < > == 运算符
    print(f"{d1} < {d2} < {d3}")

    # 排序
    dates = [d3, d1, d2]
    sorted_dates = sorted(dates)
    print(f"排序结果: {sorted_dates}")

    print()


# ============================================================
# 6. 常用日期格式
# ============================================================

def demo_common_formats():
    """常用日期格式示例"""
    print("=" * 10, "常用日期格式", "=" * 10)

    dt = datetime(2025, 7, 15, 14, 30, 0)

    # ISO 8601 格式
    print(f"ISO 8601: {dt.isoformat()}")

    # RFC 2822 格式（邮件常用）
    rfc2822 = dt.strftime("%a, %d %b %Y %H:%M:%S")
    print(f"RFC 2822: {rfc2822}")

    # 日志格式
    log_fmt = dt.strftime("%Y-%m-%d %H:%M:%S.%f")
    print(f"日志格式: {log_fmt}")

    # 文件名安全格式（无特殊字符）
    filename_fmt = dt.strftime("%Y%m%d_%H%M%S")
    print(f"文件名安全: {filename_fmt}")

    print()


# ============================================================
# 主函数
# ============================================================

def main():
    """主函数：依次演示所有日期时间知识点"""
    demo_current_datetime()
    demo_format_parse()
    demo_timedelta()
    demo_timezone()
    demo_comparison()
    demo_common_formats()


if __name__ == "__main__":
    main()
