#!/usr/bin/env python3
"""
asyncio 异步编程基础示例

模块: 04-框架与架构
知识点: 异步与任务队列 - asyncio
Python 版本: >= 3.9
最后验证: 2025-07-15

运行方式:
    python asyncio_demo.py

描述:
    演示 Python asyncio 核心功能：
    1. async/await 基本语法
    2. asyncio.gather 并发执行
    3. asyncio.create_task 任务创建
    4. asyncio.Semaphore 信号量控制并发数
    对标 Java CompletableFuture / Reactor
"""

import asyncio
import time


# ============================================================
# 1. async/await 基础
# ============================================================

async def fetch_data(name: str, delay: float) -> str:
    """模拟异步 I/O 操作（如 HTTP 请求、数据库查询）"""
    print(f"  [{name}] 开始获取数据...")
    await asyncio.sleep(delay)  # 非阻塞等待，不要用 time.sleep!
    print(f"  [{name}] 数据获取完成（耗时 {delay}s）")
    return f"{name} 的结果"


async def demo_basic():
    """基础 async/await 演示"""
    print("=" * 50)
    print("1. async/await 基础 — 顺序执行")
    print("=" * 50)

    start = time.time()
    result1 = await fetch_data("任务A", 1.0)
    result2 = await fetch_data("任务B", 1.0)
    elapsed = time.time() - start

    print(f"  结果: {result1}, {result2}")
    print(f"  顺序执行总耗时: {elapsed:.1f}s（两个 1s 任务串行 ≈ 2s）\n")


# ============================================================
# 2. asyncio.gather — 并发执行多个协程
# ============================================================

async def demo_gather():
    """gather 并发执行演示 — 对标 CompletableFuture.allOf()"""
    print("=" * 50)
    print("2. asyncio.gather — 并发执行")
    print("=" * 50)

    start = time.time()
    # gather 同时启动多个协程，等待全部完成
    results = await asyncio.gather(
        fetch_data("任务A", 1.0),
        fetch_data("任务B", 1.5),
        fetch_data("任务C", 0.5),
    )
    elapsed = time.time() - start

    print(f"  结果: {results}")
    print(f"  并发执行总耗时: {elapsed:.1f}s（取最长的 1.5s）\n")


# ============================================================
# 3. asyncio.create_task — 创建后台任务
# ============================================================

async def demo_create_task():
    """create_task 演示 — 对标 CompletableFuture.supplyAsync()"""
    print("=" * 50)
    print("3. asyncio.create_task — 后台任务")
    print("=" * 50)

    # 创建任务后立即返回，任务在后台执行
    task1 = asyncio.create_task(fetch_data("后台任务1", 1.0))
    task2 = asyncio.create_task(fetch_data("后台任务2", 0.8))

    print("  任务已创建，可以做其他事情...")
    await asyncio.sleep(0.1)
    print("  等待任务完成...")

    result1 = await task1
    result2 = await task2
    print(f"  结果: {result1}, {result2}\n")


# ============================================================
# 4. asyncio.Semaphore — 控制并发数
# ============================================================

async def limited_fetch(sem: asyncio.Semaphore, name: str, delay: float) -> str:
    """使用信号量限制并发数"""
    async with sem:  # 获取信号量，超过限制则等待
        return await fetch_data(name, delay)


async def demo_semaphore():
    """信号量控制并发数演示"""
    print("=" * 50)
    print("4. Semaphore — 控制并发数（限制为 2）")
    print("=" * 50)

    sem = asyncio.Semaphore(2)  # 最多同时执行 2 个任务

    start = time.time()
    results = await asyncio.gather(
        limited_fetch(sem, "请求1", 1.0),
        limited_fetch(sem, "请求2", 1.0),
        limited_fetch(sem, "请求3", 1.0),
        limited_fetch(sem, "请求4", 1.0),
    )
    elapsed = time.time() - start

    print(f"  结果: {results}")
    print(f"  4 个任务，并发限制 2，总耗时: {elapsed:.1f}s（≈ 2s）\n")


# ============================================================
# 5. 异常处理
# ============================================================

async def failing_task(name: str) -> str:
    """模拟可能失败的任务"""
    await asyncio.sleep(0.5)
    if name == "失败任务":
        raise ValueError(f"{name}: 模拟异常")
    return f"{name} 成功"


async def demo_error_handling():
    """异步异常处理演示"""
    print("=" * 50)
    print("5. 异步异常处理")
    print("=" * 50)

    # 方式 1: return_exceptions=True 收集异常而不抛出
    results = await asyncio.gather(
        failing_task("正常任务"),
        failing_task("失败任务"),
        return_exceptions=True,
    )
    for r in results:
        if isinstance(r, Exception):
            print(f"  捕获异常: {r}")
        else:
            print(f"  成功结果: {r}")

    # 方式 2: try/except 捕获单个任务异常
    try:
        await failing_task("失败任务")
    except ValueError as e:
        print(f"  try/except 捕获: {e}")

    print()


# ============================================================
# 主函数
# ============================================================

async def async_main():
    """运行所有演示"""
    await demo_basic()
    await demo_gather()
    await demo_create_task()
    await demo_semaphore()
    await demo_error_handling()

    print("=" * 50)
    print("总结：asyncio vs Java CompletableFuture")
    print("=" * 50)
    print("  asyncio.gather()     ↔ CompletableFuture.allOf()")
    print("  asyncio.create_task() ↔ CompletableFuture.supplyAsync()")
    print("  asyncio.Semaphore    ↔ java.util.concurrent.Semaphore")
    print("  async/await          ↔ CompletableFuture.thenApply()")


def main():
    """入口函数"""
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
