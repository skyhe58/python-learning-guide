#!/usr/bin/env python3
"""
APScheduler 定时任务示例

模块: 04-框架与架构
知识点: 定时任务 - APScheduler
Python 版本: >= 3.9
最后验证: 2025-07-15

运行方式:
    python apscheduler_demo.py

依赖安装:
    pip install apscheduler

描述:
    演示 APScheduler 三种触发器：
    1. interval — 固定间隔触发（对标 Java @Scheduled(fixedRate)）
    2. cron — Cron 表达式触发（对标 Java @Scheduled(cron)）
    3. date — 一次性触发（对标 Java ScheduledExecutorService.schedule）
    4. 动态任务管理（添加/暂停/恢复/删除）
"""

import sys
import time
from datetime import datetime, timedelta


def check_dependency():
    """检查 APScheduler 是否已安装"""
    try:
        import apscheduler  # noqa: F401
        return True
    except ImportError:
        print("=" * 55)
        print("APScheduler 未安装！")
        print("请运行: pip install apscheduler")
        print("=" * 55)
        return False


# ============================================================
# 任务函数
# ============================================================

def interval_task():
    """间隔任务 — 每隔固定时间执行"""
    print(f"  [interval] 心跳检测: {datetime.now().strftime('%H:%M:%S')}")


def cron_task():
    """Cron 任务 — 按 Cron 表达式执行"""
    print(f"  [cron] 定时报告: {datetime.now().strftime('%H:%M:%S')}")


def date_task(message: str):
    """一次性任务 — 在指定时间执行一次"""
    print(f"  [date] 一次性任务: {message} @ {datetime.now().strftime('%H:%M:%S')}")


def parameterized_task(task_name: str, priority: int):
    """带参数的任务"""
    print(f"  [参数任务] {task_name} (优先级={priority}) @ {datetime.now().strftime('%H:%M:%S')}")


# ============================================================
# 演示函数
# ============================================================

def demo_with_apscheduler():
    """使用 APScheduler 的完整演示"""
    from apscheduler.schedulers.background import BackgroundScheduler
    from apscheduler.triggers.interval import IntervalTrigger
    from apscheduler.triggers.cron import CronTrigger
    from apscheduler.triggers.date import DateTrigger

    print("=" * 55)
    print("APScheduler 定时任务演示")
    print("=" * 55)

    # 使用 BackgroundScheduler（不阻塞主线程）
    scheduler = BackgroundScheduler()

    # --- 1. Interval 触发器 ---
    print("\n1. 添加 interval 任务（每 2 秒执行）")
    scheduler.add_job(
        interval_task,
        trigger=IntervalTrigger(seconds=2),
        id="heartbeat",
        name="心跳检测",
    )

    # --- 2. Cron 触发器 ---
    print("2. 添加 cron 任务（每分钟的第 0 和 30 秒执行）")
    scheduler.add_job(
        cron_task,
        trigger=CronTrigger(second="0,30"),
        id="report",
        name="定时报告",
    )

    # --- 3. Date 触发器（一次性） ---
    run_time = datetime.now() + timedelta(seconds=3)
    print(f"3. 添加 date 任务（{run_time.strftime('%H:%M:%S')} 执行一次）")
    scheduler.add_job(
        date_task,
        trigger=DateTrigger(run_date=run_time),
        args=["数据库备份完成"],
        id="backup",
        name="一次性备份",
    )

    # --- 4. 带参数的任务 ---
    print("4. 添加带参数的任务（每 3 秒）")
    scheduler.add_job(
        parameterized_task,
        trigger="interval",
        seconds=3,
        args=["数据同步", 1],
        id="sync",
        name="数据同步",
    )

    # 启动调度器
    scheduler.start()
    print(f"\n调度器已启动，当前任务数: {len(scheduler.get_jobs())}")
    print("运行 8 秒后停止...\n")

    # 运行一段时间
    time.sleep(4)

    # --- 5. 动态管理任务 ---
    print("\n--- 动态任务管理 ---")

    # 暂停任务
    scheduler.pause_job("heartbeat")
    print("  暂停: heartbeat 任务")

    time.sleep(3)

    # 恢复任务
    scheduler.resume_job("heartbeat")
    print("  恢复: heartbeat 任务")

    time.sleep(2)

    # 列出所有任务
    print("\n--- 当前任务列表 ---")
    for job in scheduler.get_jobs():
        print(f"  {job.id}: {job.name} (下次执行: {job.next_run_time})")

    # 停止调度器
    scheduler.shutdown()
    print("\n调度器已停止")


def demo_without_apscheduler():
    """不依赖 APScheduler 的简化演示（使用标准库）"""
    import threading

    print("=" * 55)
    print("定时任务演示（使用 Python 标准库模拟）")
    print("提示: 安装 APScheduler 可获得完整功能")
    print("  pip install apscheduler")
    print("=" * 55)

    stop_event = threading.Event()

    def simple_interval(func, interval, name):
        """简单的间隔执行器"""
        while not stop_event.is_set():
            func()
            stop_event.wait(interval)

    # 启动间隔任务
    t1 = threading.Thread(
        target=simple_interval,
        args=(interval_task, 2, "heartbeat"),
        daemon=True,
    )
    t1.start()

    print("\n简单定时任务运行 6 秒...\n")
    time.sleep(6)
    stop_event.set()

    print("\n--- APScheduler 触发器类型说明 ---")
    print("  interval: 固定间隔执行（如每 5 秒、每 1 小时）")
    print("  cron:     Cron 表达式（如每天 9:00、每周一）")
    print("  date:     一次性执行（如 2025-12-31 23:59:59）")

    print("\n--- Cron 表达式示例 ---")
    cron_examples = [
        ("每天 9:00", "hour=9, minute=0"),
        ("工作日 9:00", "hour=9, minute=0, day_of_week='mon-fri'"),
        ("每小时整点", "minute=0"),
        ("每月 1 号 0:00", "day=1, hour=0, minute=0"),
        ("每 5 分钟", "minute='*/5'"),
    ]
    for desc, expr in cron_examples:
        print(f"  {desc:20s} -> CronTrigger({expr})")


# ============================================================
# 主函数
# ============================================================

def main():
    """运行 APScheduler 演示"""
    if check_dependency():
        demo_with_apscheduler()
    else:
        demo_without_apscheduler()

    print("\n" + "=" * 55)
    print("APScheduler vs Java 对照:")
    print("  IntervalTrigger  ↔ @Scheduled(fixedRate=5000)")
    print("  CronTrigger      ↔ @Scheduled(cron='0 0 9 * * ?')")
    print("  DateTrigger      ↔ ScheduledExecutorService.schedule()")
    print("  pause_job()      ↔ Quartz scheduler.pauseJob()")
    print("  resume_job()     ↔ Quartz scheduler.resumeJob()")
    print("=" * 55)


if __name__ == "__main__":
    main()
