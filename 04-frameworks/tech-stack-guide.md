# Python 技术栈选型指南

> **模块：** 04-框架与架构
> **最后更新：** 2025-07-15

## 概述

本指南根据不同项目类型，推荐合适的 Python 框架组合，帮助 Java 开发者快速选择技术栈。

---

## 按项目类型推荐

### 1. REST API 服务

> 对标 Java：Spring Boot + Spring Web

| 组件 | 推荐方案 | 备选方案 | 选型依据 |
|------|----------|----------|----------|
| Web 框架 | **FastAPI** | Flask | 自动文档、类型安全、高性能 |
| ORM | **SQLAlchemy 2.0** | Tortoise ORM | 生态成熟，支持复杂查询 |
| 数据验证 | **Pydantic** | Marshmallow | FastAPI 原生集成 |
| 数据库迁移 | **Alembic** | — | SQLAlchemy 官方迁移工具 |
| 测试 | **pytest** + httpx | — | 异步测试支持好 |
| 部署 | **uvicorn** + Docker | gunicorn | ASGI 服务器，支持异步 |

```bash
pip install fastapi uvicorn sqlalchemy alembic pydantic
```

---

### 2. 全栈 Web 应用（含前端页面）

> 对标 Java：Spring Boot + Thymeleaf

| 组件 | 推荐方案 | 备选方案 | 选型依据 |
|------|----------|----------|----------|
| Web 框架 | **Django** | Flask + Jinja2 | 内置 Admin、ORM、认证 |
| ORM | **Django ORM** | — | Django 内置，无需额外配置 |
| 模板引擎 | **Django Templates** | Jinja2 | Django 内置 |
| 前端集成 | **Django + HTMX** | Django + React | 轻量级交互 |
| 管理后台 | **Django Admin** | — | 开箱即用 |
| 部署 | **gunicorn** + Nginx | — | WSGI 服务器 |

```bash
pip install django djangorestframework
```

---

### 3. 微服务架构

> 对标 Java：Spring Cloud

| 组件 | 推荐方案 | 备选方案 | 选型依据 |
|------|----------|----------|----------|
| API 服务 | **FastAPI** | Flask | 异步支持、高性能 |
| 服务间通信 | **gRPC** | HTTP REST | 高性能、强类型 |
| 消息队列 | **RabbitMQ (pika)** | Redis / Kafka | 可靠消息传递 |
| 任务队列 | **Celery** | RQ | 分布式任务处理 |
| 服务发现 | **Consul** | etcd | 成熟稳定 |
| API 网关 | **Kong / Traefik** | Nginx | 动态路由、限流 |
| 容器化 | **Docker + K8s** | — | 标准化部署 |

```bash
pip install fastapi grpcio celery pika
```

---

### 4. 数据处理 / ETL 管道

> 对标 Java：Spring Batch

| 组件 | 推荐方案 | 备选方案 | 选型依据 |
|------|----------|----------|----------|
| 数据处理 | **Pandas** | Polars | 生态丰富 |
| 任务调度 | **APScheduler** | Celery Beat | 轻量，无需 Broker |
| 工作流 | **Prefect** | Airflow | 现代 Python 原生 |
| 数据库 | **SQLAlchemy** | — | 多数据库支持 |
| 文件处理 | **openpyxl** + csv | — | Excel/CSV 处理 |

```bash
pip install pandas sqlalchemy apscheduler openpyxl
```

---

### 5. 定时任务服务

> 对标 Java：Spring @Scheduled + Quartz

| 组件 | 推荐方案 | 备选方案 | 选型依据 |
|------|----------|----------|----------|
| 单机调度 | **APScheduler** | schedule | 功能完整，支持持久化 |
| 分布式调度 | **Celery Beat** | — | 多 Worker 支持 |
| 任务持久化 | **SQLAlchemy** | Redis | 任务状态持久化 |
| 监控 | **Flower** | — | Celery 监控面板 |

```bash
pip install apscheduler celery flower
```

---

### 6. 爬虫 / 数据采集

| 组件 | 推荐方案 | 备选方案 | 选型依据 |
|------|----------|----------|----------|
| HTTP 请求 | **requests** / httpx | aiohttp | 简单易用 |
| HTML 解析 | **BeautifulSoup** | lxml | 容错性好 |
| 爬虫框架 | **Scrapy** | — | 大规模爬取 |
| 动态页面 | **Playwright** | Selenium | 现代、速度快 |
| 数据存储 | **SQLite** / MongoDB | — | 按数据量选择 |

```bash
pip install requests beautifulsoup4 scrapy playwright
```

---

### 7. AI / LLM 应用

| 组件 | 推荐方案 | 备选方案 | 选型依据 |
|------|----------|----------|----------|
| LLM 调用 | **OpenAI SDK** | LiteLLM | 官方 SDK |
| 应用框架 | **LangChain** | LlamaIndex | 生态丰富 |
| 向量数据库 | **ChromaDB** | FAISS / Milvus | 轻量易用 |
| Web 界面 | **Gradio** / Streamlit | — | 快速原型 |
| 本地模型 | **Ollama** | vLLM | 简单部署 |

```bash
pip install openai langchain chromadb gradio
```

---

## 通用基础设施

无论选择哪种技术栈，以下工具建议统一使用：

| 类别 | 推荐工具 | 说明 |
|------|----------|------|
| 包管理 | **pip + venv** 或 **Poetry** | Poetry 适合库开发 |
| 代码格式化 | **Black** + **isort** | 统一代码风格 |
| 类型检查 | **mypy** | 静态类型检查 |
| Lint | **ruff** | 速度极快的 Linter |
| 测试 | **pytest** | Python 测试标准 |
| CI/CD | **GitHub Actions** | 自动化构建部署 |
| 容器化 | **Docker** | 标准化部署 |
| 日志 | **logging** + **structlog** | 结构化日志 |

## 选型决策流程

```
需要前端页面吗？
├── 是 → Django（全栈）
└── 否 → 纯 API 服务？
    ├── 是 → 需要高性能/异步？
    │   ├── 是 → FastAPI
    │   └── 否 → Flask（简单场景）或 FastAPI
    └── 否 → 什么类型？
        ├── 数据处理 → Pandas + APScheduler
        ├── 爬虫 → Scrapy / requests + BS4
        ├── AI 应用 → LangChain + FastAPI
        └── 微服务 → FastAPI + gRPC + Celery
```
