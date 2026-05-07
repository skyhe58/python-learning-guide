#!/usr/bin/env python3
"""
Celery 分布式任务队列概念介绍

模块: 04-框架与架构
知识点: 异步与任务队列 - Celery
Python 版本: >= 3.9
最后验证: 2025-07-15

运行方式:
    python celery_intro.py
    # 注意：本示例为概念演示，展示 Celery 配置和用法
    # 实际运行 Celery 需要安装 Redis 或 RabbitMQ 作为消息代理

依赖安装:
    pip install celery redis

描述:
    演示 Celery 核心概念：
    1. Celery 应用配置
    2. 任务定义与装饰器
    3. 任务调用方式（delay/apply_async）
    4. 任务重试与错误处理
    5. 任务链与工作流
    对标 Java Spring @Async + RabbitMQ
"""


# ============================================================
# 1. Celery 架构说明
# ============================================================

CELERY_ARCHITECTURE = """
Celery 架构（对标 Java Spring Async + MQ）:

┌──────────┐    ┌──────────────┐    ┌──────────┐
│  Producer │───>│ Message Broker│───>│  Worker  │
│  (生产者) │    │  (消息代理)   │    │ (消费者) │
│  Web App  │    │ Redis/RabbitMQ│    │ Celery   │
└──────────┘    └──────────────┘    └──────────┘
                                         │
                                    ┌────┴────┐
                                    │ Backend  │
                                    │(结果存储)│
                                    │ Redis/DB │
                                    └─────────┘

Java 对比:
  Producer  ↔ @Service 中调用 @Async 方法
  Broker    ↔ RabbitMQ / ActiveMQ
  Worker    ↔ @Async 线程池
  Backend   ↔ Future<T> 结果
"""


# ============================================================
# 2. Celery 应用配置示例
# ============================================================

CELERY_CONFIG_EXAMPLE = '''
# celery_app.py — Celery 应用配置
from celery import Celery

# 创建 Celery 实例（对标 Spring @EnableAsync 配置）
app = Celery(
    "myproject",
    broker="redis://localhost:6379/0",      # 消息代理地址
    backend="redis://localhost:6379/1",     # 结果存储地址
)

# 配置选项
app.conf.update(
    task_serializer="json",                 # 任务序列化格式
    result_serializer="json",               # 结果序列化格式
    accept_content=["json"],                # 接受的内容类型
    timezone="Asia/Shanghai",               # 时区
    enable_utc=True,                        # 使用 UTC
    task_track_started=True,                # 跟踪任务开始状态
    task_acks_late=True,                    # 任务完成后才确认（防丢失）
    worker_prefetch_multiplier=1,           # 预取数量
    task_default_retry_delay=60,            # 默认重试延迟（秒）
    task_max_retries=3,                     # 默认最大重试次数
)
'''


# ============================================================
# 3. 任务定义示例
# ============================================================

TASK_DEFINITION_EXAMPLE = '''
# tasks.py — 任务定义
from celery_app import app
import time

# --- 基础任务 ---
@app.task
def add(x, y):
    """简单加法任务（对标 Java @Async 方法）"""
    return x + y

# --- 带重试的任务 ---
@app.task(bind=True, max_retries=3, default_retry_delay=10)
def send_email(self, to, subject, body):
    """
    发送邮件任务 — 带自动重试
    bind=True 使任务可以访问 self（任务实例）
    对标 Java Spring Retry @Retryable
    """
    try:
        # 模拟发送邮件
        result = email_service.send(to, subject, body)
        return {"status": "sent", "to": to}
    except ConnectionError as exc:
        # 触发重试，指数退避
        raise self.retry(exc=exc, countdown=2 ** self.request.retries)

# --- 带超时的任务 ---
@app.task(time_limit=300, soft_time_limit=240)
def process_large_file(file_path):
    """
    处理大文件 — 带超时限制
    time_limit: 硬超时（强制终止）
    soft_time_limit: 软超时（抛出 SoftTimeLimitExceeded）
    """
    # 处理逻辑...
    pass
'''


# ============================================================
# 4. 任务调用方式
# ============================================================

TASK_CALLING_EXAMPLE = '''
# 调用任务的几种方式

# 方式 1: delay() — 最简单的异步调用
result = add.delay(4, 6)
# 对标 Java: CompletableFuture<Integer> future = asyncService.add(4, 6);

# 方式 2: apply_async() — 更多控制选项
result = add.apply_async(
    args=[4, 6],
    countdown=10,           # 10 秒后执行
    expires=3600,           # 1 小时后过期
    queue="high_priority",  # 指定队列
)

# 方式 3: 获取结果
print(result.id)            # 任务 ID
print(result.status)        # 任务状态: PENDING/STARTED/SUCCESS/FAILURE
print(result.get(timeout=10))  # 等待结果（最多 10 秒）
# 对标 Java: future.get(10, TimeUnit.SECONDS)

# 方式 4: 任务链（Chain）— 串行执行
from celery import chain
workflow = chain(
    fetch_data.s("url"),        # 第一步：获取数据
    process_data.s(),           # 第二步：处理数据（接收上一步结果）
    save_result.s("output.json"),  # 第三步：保存结果
)
workflow.apply_async()

# 方式 5: 任务组（Group）— 并行执行
from celery import group
job = group([
    process_item.s(item) for item in items
])
result = job.apply_async()
# 对标 Java: CompletableFuture.allOf(futures)
'''


# ============================================================
# 5. 启动命令
# ============================================================

CELERY_COMMANDS = """
Celery 常用命令:

# 启动 Worker（对标启动 Spring Boot 应用的异步线程池）
celery -A celery_app worker --loglevel=info

# 启动 Worker（指定并发数）
celery -A celery_app worker --concurrency=4

# 启动定时任务调度器（Celery Beat）
celery -A celery_app beat --loglevel=info

# 查看活跃任务
celery -A celery_app inspect active

# 监控面板（Flower）
pip install flower
celery -A celery_app flower
# 访问 http://localhost:5555
"""


# ============================================================
# 主函数 — 打印概念说明
# ============================================================

def main():
    """展示 Celery 核心概念"""
    print("=" * 60)
    print("Celery 分布式任务队列 — 概念介绍")
    print("=" * 60)

    print("\n📐 架构说明:")
    print(CELERY_ARCHITECTURE)

    print("\n⚙️ 配置示例:")
    print(CELERY_CONFIG_EXAMPLE)

    print("\n📝 任务定义:")
    print(TASK_DEFINITION_EXAMPLE)

    print("\n🚀 任务调用:")
    print(TASK_CALLING_EXAMPLE)

    print("\n💻 启动命令:")
    print(CELERY_COMMANDS)

    print("=" * 60)
    print("提示：实际运行 Celery 需要先安装并启动 Redis 或 RabbitMQ")
    print("  安装 Redis: brew install redis (Mac) / apt install redis (Linux)")
    print("  启动 Redis: redis-server")
    print("=" * 60)


if __name__ == "__main__":
    main()
