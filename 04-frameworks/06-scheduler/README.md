# 定时任务：APScheduler / Celery Beat

> **模块：** 04-框架与架构
> **难度：** 进阶
> **前置知识：** Python 基础、函数与装饰器
> **Python 版本：** >= 3.9
> **最后验证日期：** 2025-07-15

## 概念说明

定时任务是后端开发的常见需求，Python 生态中两大方案：

- **APScheduler** — 轻量级定时任务库，支持 interval/cron/date 三种触发器，可独立使用。对标 Java Quartz。
- **Celery Beat** — Celery 的定时调度组件，适合分布式环境。对标 Java Spring @Scheduled + 分布式调度。

## Java 对比

| 特性 | APScheduler | Celery Beat | Java Quartz | Spring @Scheduled |
|------|------------|-------------|-------------|-------------------|
| **类型** | 进程内调度 | 分布式调度 | 进程内调度 | 进程内调度 |
| **Cron 支持** | ✅ | ✅ | ✅ | ✅ |
| **持久化** | 支持（SQLAlchemy） | Redis/DB | 支持（JDBC） | 不支持 |
| **集群支持** | 有限 | ✅ 原生支持 | ✅ | 需要 ShedLock |
| **动态管理** | ✅ 运行时增删任务 | ✅ | ✅ | ❌ 编译时确定 |
| **依赖** | 无（独立库） | 需要 Celery + Broker | 无 | Spring 框架 |

**Java Spring @Scheduled 写法：**
```java
@Component
public class ScheduledTasks {
    @Scheduled(fixedRate = 5000)
    public void reportEvery5Seconds() {
        System.out.println("每 5 秒执行一次: " + new Date());
    }

    @Scheduled(cron = "0 0 9 * * MON-FRI")
    public void workdayMorningTask() {
        System.out.println("工作日早上 9 点执行");
    }
}
```

**Python APScheduler 写法：**
```python
from apscheduler.schedulers.blocking import BlockingScheduler

scheduler = BlockingScheduler()

@scheduler.scheduled_job("interval", seconds=5)
def report_every_5_seconds():
    print(f"每 5 秒执行一次: {datetime.now()}")

@scheduler.scheduled_job("cron", hour=9, day_of_week="mon-fri")
def workday_morning_task():
    print("工作日早上 9 点执行")

scheduler.start()
```

## 实战代码

### 示例 1：APScheduler 三种触发器

**文件：** `examples/apscheduler_demo.py`

演示 interval（间隔）、cron（定时）、date（一次性）三种触发器。

**运行方式：**
```bash
pip install apscheduler
python examples/apscheduler_demo.py
```

## APScheduler 触发器速查

| 触发器 | 说明 | 示例 |
|--------|------|------|
| `interval` | 固定间隔执行 | `seconds=30`, `minutes=5`, `hours=1` |
| `cron` | Cron 表达式 | `hour=9, minute=30, day_of_week='mon-fri'` |
| `date` | 一次性执行 | `run_date='2025-12-31 23:59:59'` |

## 常见陷阱

- ⚠️ APScheduler 默认使用内存存储，进程重启后任务丢失，生产环境应配置持久化
- ⚠️ `BlockingScheduler` 会阻塞主线程，Web 应用中应使用 `BackgroundScheduler`
- ⚠️ Celery Beat 在多实例部署时可能重复执行，需要使用 `django-celery-beat` 或 Redis 锁
- ⚠️ Cron 表达式中月份和星期的起始值与 Java Quartz 不同，注意对照

> 💻 **完整可运行代码：** [apscheduler_demo.py](examples/apscheduler_demo.py)

## 参考资料

- [APScheduler 官方文档](https://apscheduler.readthedocs.io/)
- [Celery Beat 文档](https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html)
