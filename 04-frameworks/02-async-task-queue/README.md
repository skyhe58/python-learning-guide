# 异步与任务队列：Celery / asyncio / RQ

> **模块：** 04-框架与架构
> **难度：** 进阶
> **前置知识：** Python 基础、函数与装饰器
> **Python 版本：** >= 3.9
> **最后验证日期：** 2025-07-15

## 概念说明

Python 异步编程和任务队列是处理耗时操作的两种核心方案：

- **asyncio** — Python 原生异步框架，基于事件循环和协程，适合 I/O 密集型任务。对标 Java `CompletableFuture` / Project Reactor。
- **Celery** — 分布式任务队列，支持异步执行、定时调度、任务重试。对标 Java Spring Async + RabbitMQ。
- **RQ (Redis Queue)** — 轻量级任务队列，基于 Redis，API 简洁。适合小型项目。

## Java 对比

| 特性 | Python asyncio | Python Celery | Java CompletableFuture | Java Spring Async |
|------|---------------|---------------|----------------------|-------------------|
| **类型** | 语言内置协程 | 分布式任务队列 | 语言内置异步 | 框架级异步 |
| **并发模型** | 单线程事件循环 | 多进程/多线程 Worker | 线程池 | 线程池 |
| **适用场景** | I/O 密集型 | CPU 密集型/分布式 | I/O 密集型 | 后台任务 |
| **消息代理** | 不需要 | Redis/RabbitMQ | 不需要 | 不需要（或 MQ） |
| **任务持久化** | 不支持 | 支持 | 不支持 | 需要额外配置 |
| **定时调度** | 需要额外库 | Celery Beat 内置 | ScheduledExecutor | @Scheduled |

**Java CompletableFuture 写法：**
```java
CompletableFuture<String> future1 = CompletableFuture.supplyAsync(() -> fetchUrl("url1"));
CompletableFuture<String> future2 = CompletableFuture.supplyAsync(() -> fetchUrl("url2"));
CompletableFuture.allOf(future1, future2).join();
System.out.println(future1.get() + future2.get());
```

**Python asyncio 写法：**
```python
import asyncio

async def fetch_url(url):
    # 模拟异步 HTTP 请求
    await asyncio.sleep(1)
    return f"Response from {url}"

async def main():
    result1, result2 = await asyncio.gather(
        fetch_url("url1"),
        fetch_url("url2"),
    )
    print(result1, result2)

asyncio.run(main())
```

## 实战代码

### 示例 1：asyncio 基础

**文件：** `examples/asyncio_demo.py`

演示 async/await、gather 并发、create_task、信号量控制并发数。

**运行方式：**
```bash
python examples/asyncio_demo.py
```

### 示例 2：Celery 概念介绍

**文件：** `examples/celery_intro.py`

Celery 配置和任务定义示例（概念演示，不需要实际运行 broker）。

## 常见陷阱

- ⚠️ `asyncio.run()` 不能在已有事件循环中调用（如 Jupyter Notebook），需用 `await` 或 `nest_asyncio`
- ⚠️ asyncio 是单线程的，CPU 密集型任务会阻塞事件循环，应使用 `run_in_executor`
- ⚠️ Celery Worker 和主应用是独立进程，不能共享内存变量
- ⚠️ 不要在 async 函数中调用同步阻塞函数（如 `time.sleep`），应使用 `asyncio.sleep`

> 💻 **完整可运行代码：** [asyncio_demo.py](examples/asyncio_demo.py) | [celery_intro.py](examples/celery_intro.py)

## 参考资料

- [asyncio 官方文档](https://docs.python.org/3/library/asyncio.html)
- [Celery 官方文档](https://docs.celeryq.dev/)
- [RQ 官方文档](https://python-rq.org/)
