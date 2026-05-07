#!/usr/bin/env python3
"""
消息队列模式模拟（使用 Python 标准库）

模块: 04-框架与架构
知识点: 消息队列集成
Python 版本: >= 3.9
最后验证: 2025-07-15

运行方式:
    python redis_queue_demo.py

描述:
    使用 Python 标准库（queue + threading）模拟消息队列的核心模式：
    1. 基础生产者/消费者模式
    2. 发布/订阅模式（Pub/Sub）
    3. 带优先级的消息队列
    4. 带确认机制的可靠消息传递
    不依赖 Redis 或 RabbitMQ 等外部服务
"""

import queue
import threading
import time
import json
from dataclasses import dataclass, field
from typing import Any


# ============================================================
# 1. 基础生产者/消费者模式
# ============================================================

def demo_basic_queue():
    """基础消息队列 — 对标 RabbitMQ 简单队列"""
    print("=" * 55)
    print("1. 基础生产者/消费者模式")
    print("=" * 55)

    msg_queue: queue.Queue[str] = queue.Queue(maxsize=10)
    results: list[str] = []

    def producer(name: str, messages: list[str]):
        """生产者：发送消息到队列"""
        for msg in messages:
            msg_queue.put(msg)
            print(f"  [生产者-{name}] 发送: {msg}")
            time.sleep(0.1)

    def consumer(name: str, count: int):
        """消费者：从队列接收消息"""
        for _ in range(count):
            msg = msg_queue.get(timeout=5)
            results.append(msg)
            print(f"  [消费者-{name}] 收到: {msg}")
            msg_queue.task_done()

    messages = ["订单-001", "订单-002", "订单-003", "订单-004"]

    # 启动生产者和消费者线程
    t_producer = threading.Thread(target=producer, args=("P1", messages))
    t_consumer = threading.Thread(target=consumer, args=("C1", len(messages)))

    t_consumer.start()
    t_producer.start()

    t_producer.join()
    t_consumer.join()

    print(f"  处理完成，共 {len(results)} 条消息\n")


# ============================================================
# 2. 发布/订阅模式（Pub/Sub）
# ============================================================

class PubSubBroker:
    """简单的发布/订阅代理 — 对标 Redis Pub/Sub"""

    def __init__(self):
        self._subscribers: dict[str, list[queue.Queue]] = {}
        self._lock = threading.Lock()

    def subscribe(self, topic: str) -> queue.Queue:
        """订阅主题"""
        q: queue.Queue = queue.Queue()
        with self._lock:
            if topic not in self._subscribers:
                self._subscribers[topic] = []
            self._subscribers[topic].append(q)
        return q

    def publish(self, topic: str, message: Any):
        """发布消息到主题"""
        with self._lock:
            subscribers = self._subscribers.get(topic, [])
        for q in subscribers:
            q.put(message)


def demo_pubsub():
    """发布/订阅模式演示"""
    print("=" * 55)
    print("2. 发布/订阅模式（Pub/Sub）")
    print("=" * 55)

    broker = PubSubBroker()
    received: dict[str, list] = {"订阅者A": [], "订阅者B": []}

    # 两个订阅者订阅同一主题
    queue_a = broker.subscribe("news")
    queue_b = broker.subscribe("news")

    def subscriber(name: str, q: queue.Queue, count: int):
        for _ in range(count):
            msg = q.get(timeout=5)
            received[name].append(msg)
            print(f"  [{name}] 收到: {msg}")

    t_a = threading.Thread(target=subscriber, args=("订阅者A", queue_a, 3))
    t_b = threading.Thread(target=subscriber, args=("订阅者B", queue_b, 3))
    t_a.start()
    t_b.start()

    # 发布消息（所有订阅者都会收到）
    for msg in ["突发新闻", "体育快讯", "天气预报"]:
        broker.publish("news", msg)
        print(f"  [发布者] 发布: {msg}")
        time.sleep(0.1)

    t_a.join()
    t_b.join()

    print(f"  订阅者A 收到 {len(received['订阅者A'])} 条")
    print(f"  订阅者B 收到 {len(received['订阅者B'])} 条\n")


# ============================================================
# 3. 优先级队列
# ============================================================

@dataclass(order=True)
class PriorityMessage:
    """带优先级的消息（数字越小优先级越高）"""
    priority: int
    data: str = field(compare=False)


def demo_priority_queue():
    """优先级消息队列演示"""
    print("=" * 55)
    print("3. 优先级消息队列")
    print("=" * 55)

    pq: queue.PriorityQueue[PriorityMessage] = queue.PriorityQueue()

    # 发送不同优先级的消息
    messages = [
        PriorityMessage(priority=3, data="普通日志"),
        PriorityMessage(priority=1, data="紧急告警"),
        PriorityMessage(priority=2, data="警告信息"),
        PriorityMessage(priority=1, data="系统崩溃"),
        PriorityMessage(priority=3, data="调试信息"),
    ]

    for msg in messages:
        pq.put(msg)
        print(f"  入队: [优先级={msg.priority}] {msg.data}")

    print("  --- 按优先级出队 ---")
    while not pq.empty():
        msg = pq.get()
        print(f"  出队: [优先级={msg.priority}] {msg.data}")

    print()


# ============================================================
# 4. 带确认机制的可靠消息传递
# ============================================================

class ReliableQueue:
    """带消息确认的可靠队列 — 对标 RabbitMQ ACK 机制"""

    def __init__(self):
        self._queue: queue.Queue = queue.Queue()
        self._unacked: dict[str, dict] = {}
        self._lock = threading.Lock()
        self._msg_id = 0

    def send(self, data: Any) -> str:
        """发送消息，返回消息 ID"""
        with self._lock:
            self._msg_id += 1
            msg_id = f"msg-{self._msg_id:04d}"
        message = {"id": msg_id, "data": data, "timestamp": time.time()}
        self._queue.put(message)
        return msg_id

    def receive(self, timeout: float = 5.0) -> dict | None:
        """接收消息（消息进入未确认状态）"""
        try:
            message = self._queue.get(timeout=timeout)
            with self._lock:
                self._unacked[message["id"]] = message
            return message
        except queue.Empty:
            return None

    def ack(self, msg_id: str):
        """确认消息已处理"""
        with self._lock:
            self._unacked.pop(msg_id, None)

    def nack(self, msg_id: str):
        """拒绝消息，重新入队"""
        with self._lock:
            message = self._unacked.pop(msg_id, None)
        if message:
            self._queue.put(message)

    @property
    def unacked_count(self) -> int:
        return len(self._unacked)


def demo_reliable_queue():
    """可靠消息传递演示"""
    print("=" * 55)
    print("4. 带确认机制的可靠消息传递（ACK/NACK）")
    print("=" * 55)

    rq = ReliableQueue()

    # 发送消息
    for data in ["处理订单", "发送邮件", "生成报表"]:
        msg_id = rq.send(data)
        print(f"  发送: {msg_id} -> {data}")

    # 消费消息
    msg1 = rq.receive()
    if msg1:
        print(f"  收到: {msg1['id']} -> {msg1['data']}")
        rq.ack(msg1["id"])  # 确认处理成功
        print(f"  ACK: {msg1['id']}（处理成功）")

    msg2 = rq.receive()
    if msg2:
        print(f"  收到: {msg2['id']} -> {msg2['data']}")
        rq.nack(msg2["id"])  # 处理失败，重新入队
        print(f"  NACK: {msg2['id']}（重新入队）")

    # 重新消费被 NACK 的消息
    msg2_retry = rq.receive()
    if msg2_retry:
        print(f"  重试: {msg2_retry['id']} -> {msg2_retry['data']}")
        rq.ack(msg2_retry["id"])
        print(f"  ACK: {msg2_retry['id']}（重试成功）")

    print(f"  未确认消息数: {rq.unacked_count}\n")


# ============================================================
# 主函数
# ============================================================

def main():
    """运行所有消息队列模式演示"""
    print("消息队列模式演示（使用 Python 标准库模拟）\n")

    demo_basic_queue()
    demo_pubsub()
    demo_priority_queue()
    demo_reliable_queue()

    print("=" * 55)
    print("模式对照:")
    print("  基础队列      ↔ RabbitMQ Simple Queue")
    print("  发布/订阅     ↔ Redis Pub/Sub")
    print("  优先级队列    ↔ RabbitMQ Priority Queue")
    print("  ACK/NACK 机制 ↔ RabbitMQ Manual Acknowledgment")
    print("=" * 55)


if __name__ == "__main__":
    main()
