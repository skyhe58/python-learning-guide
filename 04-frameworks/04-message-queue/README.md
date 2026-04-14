# 消息队列集成：RabbitMQ / Redis / Kafka

> **模块：** 04-框架与架构
> **难度：** 进阶
> **前置知识：** Python 基础、异步编程基础
> **Python 版本：** >= 3.9
> **最后验证日期：** 2025-07-15

## 概念说明

消息队列是分布式系统的核心组件，用于解耦服务、异步处理、流量削峰。Python 生态中常用的消息队列集成方案：

- **RabbitMQ (pika)** — AMQP 协议消息代理，支持复杂路由。对标 Java Spring AMQP。
- **Redis** — 除了缓存，还可作为轻量级消息代理（Pub/Sub、Stream）。对标 Java Jedis/Lettuce。
- **Kafka (kafka-python)** — 高吞吐量分布式流处理平台。对标 Java Spring Kafka。

## Java 对比

| 特性 | RabbitMQ (pika) | Redis (redis-py) | Kafka (kafka-python) | Spring AMQP | Spring Kafka |
|------|----------------|------------------|---------------------|-------------|-------------|
| **协议** | AMQP | Redis 协议 | Kafka 协议 | AMQP | Kafka 协议 |
| **消息持久化** | ✅ 支持 | 有限（Stream 支持） | ✅ 支持 | ✅ | ✅ |
| **消息确认** | ✅ ACK/NACK | ❌ Pub/Sub 无确认 | ✅ Offset 提交 | ✅ | ✅ |
| **适用场景** | 任务队列、RPC | 缓存+简单消息 | 日志收集、流处理 | 企业级消息 | 大数据流 |
| **吞吐量** | 万级/秒 | 十万级/秒 | 百万级/秒 | 万级/秒 | 百万级/秒 |

**Java Spring AMQP 写法：**
```java
// 生产者
@Service
public class MessageProducer {
    @Autowired
    private RabbitTemplate rabbitTemplate;

    public void send(String message) {
        rabbitTemplate.convertAndSend("myQueue", message);
    }
}

// 消费者
@Component
public class MessageConsumer {
    @RabbitListener(queues = "myQueue")
    public void receive(String message) {
        System.out.println("收到: " + message);
    }
}
```

**Python pika 写法：**
```python
import pika

# 生产者
connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()
channel.queue_declare(queue="myQueue")
channel.basic_publish(exchange="", routing_key="myQueue", body="Hello")

# 消费者
def callback(ch, method, properties, body):
    print(f"收到: {body.decode()}")

channel.basic_consume(queue="myQueue", on_message_callback=callback, auto_ack=True)
channel.start_consuming()
```

## 实战代码

### 示例 1：Python 标准库模拟消息队列

**文件：** `examples/redis_queue_demo.py`

使用 Python 标准库（queue + threading）模拟生产者/消费者模式，不依赖外部服务。

**运行方式：**
```bash
python examples/redis_queue_demo.py
```

## 选型建议

| 场景 | 推荐方案 | 原因 |
|------|----------|------|
| 任务队列 | RabbitMQ + Celery | 成熟稳定，消息确认机制完善 |
| 简单消息通知 | Redis Pub/Sub | 轻量，无需额外部署 |
| 日志收集/流处理 | Kafka | 高吞吐量，支持消息回溯 |
| 小型项目 | Redis Queue (RQ) | 简单易用，依赖少 |

## 常见陷阱

- ⚠️ RabbitMQ 连接是非线程安全的，多线程环境需要连接池
- ⚠️ Redis Pub/Sub 消息不持久化，消费者离线时消息会丢失
- ⚠️ Kafka 消费者需要正确管理 offset，否则可能重复消费或丢失消息
- ⚠️ 消息序列化要统一格式（JSON），避免生产者和消费者格式不一致

> 💻 **完整可运行代码：** [redis_queue_demo.py](examples/redis_queue_demo.py)

## 参考资料

- [RabbitMQ Python 教程](https://www.rabbitmq.com/tutorials)
- [pika 官方文档](https://pika.readthedocs.io/)
- [kafka-python 文档](https://kafka-python.readthedocs.io/)
- [Redis Pub/Sub 文档](https://redis.io/docs/interact/pubsub/)
