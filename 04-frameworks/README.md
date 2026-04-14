# 框架与架构

> **阶段：** 第三阶段
> **前置条件：** [01-Python 基础](../01-python-basics/)，建议完成第二阶段后学习

## 模块简介

本模块系统性地介绍 Python 生态中常用的框架和架构模式，对标 Java 中的 Spring Boot、Spring Cloud、MyBatis 等。帮助 Java 开发者在 Python 项目中选择合适的技术栈，快速上手主流框架。

## 知识点列表

| 序号 | 知识点 | 描述 | 难度 |
|------|--------|------|------|
| 01 | [Web 框架](./01-web-frameworks/) | Django/FastAPI/Flask 对比，对标 Spring Boot | 进阶 |
| 02 | [异步与任务队列](./02-async-task-queue/) | Celery/asyncio/RQ，对标 Spring Async | 进阶 |
| 03 | [ORM 框架](./03-orm/) | SQLAlchemy/Django ORM，对标 MyBatis/Hibernate | 进阶 |
| 04 | [消息队列集成](./04-message-queue/) | RabbitMQ/Redis/Kafka 与 Python 集成 | 进阶 |
| 05 | [微服务架构](./05-microservice/) | gRPC/Nameko/FastAPI 微服务模式 | 高级 |
| 06 | [定时任务](./06-scheduler/) | APScheduler/Celery Beat，对标 Quartz | 进阶 |
| 07 | [项目架构模式](./07-architecture-patterns/) | MVC/分层架构/DDD，对标 Spring MVC | 高级 |

## 推荐学习顺序

1. **Web 框架** — 最核心的框架知识，三大框架对比
2. **ORM 框架** — Web 开发离不开数据库操作
3. **异步与任务队列** — 处理耗时任务的关键技术
4. **定时任务** — 常见的后台任务调度需求
5. **消息队列集成** — 分布式系统的基础组件
6. **微服务架构** — 大型项目的架构选择
7. **项目架构模式** — 代码组织的最佳实践

## 模块依赖安装

```bash
pip install -r requirements.txt
```
