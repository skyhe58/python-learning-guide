# 中级面试题集

> **难度：** 中级
> **覆盖模块：** 04-框架与架构
> **适用人群：** 有 1-3 年 Python 开发经验，熟悉至少一个 Web 框架

---

## 题目 1：Django vs FastAPI vs Flask 如何选型？

> **考察知识点：** Web 框架选型
> **关联模块：** [04-frameworks/01-web-frameworks](../../04-frameworks/01-web-frameworks/)

### 题目

你的团队需要开发一个新项目，请分别说明在以下三种场景下你会选择哪个框架，并解释原因：
1. 一个需要管理后台的内容管理系统
2. 一个高并发的 REST API 微服务
3. 一个快速验证想法的 MVP 原型

### 参考答案

```python
"""
框架选型决策示例
"""

# 场景分析
scenarios = {
    "内容管理系统": {
        "推荐": "Django",
        "原因": [
            "内置 Admin 后台，开箱即用",
            "内置 ORM，数据库迁移方便",
            "内置用户认证和权限系统",
            "模板引擎支持服务端渲染",
        ],
        "对标Java": "Spring Boot + Spring Security + Thymeleaf",
    },
    "高并发 REST API": {
        "推荐": "FastAPI",
        "原因": [
            "原生 async/await 支持，性能接近 Go",
            "Pydantic 自动数据验证和序列化",
            "自动生成 OpenAPI/Swagger 文档",
            "类型提示驱动，IDE 支持好",
        ],
        "对标Java": "Spring WebFlux",
    },
    "MVP 原型": {
        "推荐": "Flask",
        "原因": [
            "核心极简，上手最快",
            "灵活度高，不强制项目结构",
            "扩展丰富，按需添加功能",
            "适合小型项目和快速迭代",
        ],
        "对标Java": "Spark / Javalin",
    },
}
```

### 解析

框架选型的核心原则是"合适比最好更重要"：
- **Django** 适合需要完整功能的全栈应用，牺牲灵活性换取开发效率
- **FastAPI** 适合纯 API 服务，特别是需要高性能和自动文档的场景
- **Flask** 适合小型项目或需要高度定制的场景

---

## 题目 2：什么是 ORM 的 N+1 查询问题？如何解决？

> **考察知识点：** ORM 性能优化
> **关联模块：** [04-frameworks/03-orm](../../04-frameworks/03-orm/)

### 题目

解释 ORM 中的 N+1 查询问题，用 SQLAlchemy 代码演示问题和解决方案。

### 参考答案

```python
"""
ORM N+1 查询问题演示与解决
"""
from sqlalchemy.orm import joinedload, selectinload

# ❌ N+1 问题代码
# 1 次查询获取所有用户 + N 次查询获取每个用户的订单
def bad_example(session):
    users = session.query(User).all()          # 1 次 SQL
    for user in users:
        print(user.orders)                      # 每次触发 1 次 SQL（共 N 次）
    # 总计: 1 + N 次 SQL 查询

# ✅ 解决方案 1: joinedload（JOIN 预加载）
def good_example_join(session):
    users = session.query(User).options(
        joinedload(User.orders)                 # LEFT JOIN 一次查询
    ).all()
    for user in users:
        print(user.orders)                      # 不触发额外 SQL
    # 总计: 1 次 SQL 查询（含 JOIN）

# ✅ 解决方案 2: selectinload（子查询预加载）
def good_example_select(session):
    users = session.query(User).options(
        selectinload(User.orders)               # SELECT ... WHERE user_id IN (...)
    ).all()
    for user in users:
        print(user.orders)
    # 总计: 2 次 SQL 查询

# 选择建议:
# joinedload  — 一对一/多对一关系，数据量小
# selectinload — 一对多关系，数据量大（避免笛卡尔积）
```

### 解析

N+1 问题是 ORM 最常见的性能陷阱，对标 Java JPA 中的 `@EntityGraph` 和 `FetchType.EAGER`。核心原因是 ORM 默认使用懒加载（Lazy Loading），访问关联对象时才触发 SQL 查询。解决方案是使用预加载策略，在查询主对象时一并加载关联数据。

---

## 题目 3：解释 Python asyncio 事件循环的工作原理

> **考察知识点：** 异步编程
> **关联模块：** [04-frameworks/02-async-task-queue](../../04-frameworks/02-async-task-queue/)

### 题目

解释 asyncio 事件循环的工作原理，说明 `async/await` 与多线程的区别，以及为什么 asyncio 适合 I/O 密集型任务。

### 参考答案

```python
"""
asyncio 事件循环原理演示
"""
import asyncio
import time

# asyncio 是单线程协作式并发
# 事件循环在一个线程中调度多个协程
# 当协程遇到 await（I/O 等待）时，主动让出控制权

async def io_task(name, delay):
    print(f"[{name}] 开始 I/O 操作")
    await asyncio.sleep(delay)  # 让出控制权，事件循环调度其他协程
    print(f"[{name}] I/O 完成")
    return name

async def main():
    start = time.time()
    # gather 并发执行，总耗时 = max(各任务耗时)
    results = await asyncio.gather(
        io_task("A", 2),
        io_task("B", 1),
        io_task("C", 1.5),
    )
    print(f"总耗时: {time.time() - start:.1f}s")  # ≈ 2s，不是 4.5s
    print(f"结果: {results}")

# 事件循环工作流程:
# 1. 启动协程 A、B、C
# 2. A 遇到 await sleep(2)，挂起，切换到 B
# 3. B 遇到 await sleep(1)，挂起，切换到 C
# 4. C 遇到 await sleep(1.5)，挂起
# 5. 1s 后 B 的 sleep 完成，恢复 B
# 6. 1.5s 后 C 完成，2s 后 A 完成

# asyncio vs 多线程:
# asyncio: 单线程，协作式，无锁，适合 I/O 密集型
# 多线程: 多线程，抢占式，需要锁，受 GIL 限制
```

### 解析

asyncio 的核心是**协作式多任务**：协程在 `await` 处主动让出控制权，事件循环负责调度。与 Java 的 `CompletableFuture` 类似，但 Python 的 `async/await` 语法更简洁。关键区别是 Python 有 GIL（全局解释器锁），多线程无法真正并行执行 CPU 密集型任务，而 asyncio 在 I/O 等待时切换协程，充分利用等待时间。

---

## 题目 4：Celery 任务失败后如何实现自动重试？

> **考察知识点：** 任务队列、容错设计
> **关联模块：** [04-frameworks/02-async-task-queue](../../04-frameworks/02-async-task-queue/)

### 题目

使用 Celery 实现一个带自动重试和指数退避的任务，并说明如何保证任务的幂等性。

### 参考答案

```python
"""
Celery 任务重试与幂等性设计
"""
from celery import Celery

app = Celery("demo", broker="redis://localhost:6379/0")

# 方式 1: 装饰器配置自动重试
@app.task(
    bind=True,
    max_retries=3,
    default_retry_delay=60,
    autoretry_for=(ConnectionError, TimeoutError),  # 自动重试的异常类型
    retry_backoff=True,       # 启用指数退避
    retry_backoff_max=600,    # 最大退避时间 10 分钟
    retry_jitter=True,        # 添加随机抖动，避免雪崩
)
def send_notification(self, user_id, message):
    """发送通知 — 带自动重试"""
    # 幂等性设计: 使用唯一标识检查是否已处理
    cache_key = f"notification:{self.request.id}"
    if cache.get(cache_key):
        return {"status": "already_sent"}

    try:
        result = notification_service.send(user_id, message)
        cache.set(cache_key, True, timeout=3600)  # 标记已处理
        return result
    except ConnectionError:
        raise  # autoretry_for 会自动捕获并重试

# 方式 2: 手动控制重试
@app.task(bind=True, max_retries=5)
def process_payment(self, order_id, amount):
    """处理支付 — 手动重试控制"""
    try:
        result = payment_gateway.charge(order_id, amount)
        return result
    except PaymentError as exc:
        # 指数退避: 2^retry * 60 秒
        countdown = 60 * (2 ** self.request.retries)
        raise self.retry(exc=exc, countdown=countdown)

# 幂等性保证要点:
# 1. 使用任务 ID (self.request.id) 作为去重键
# 2. 在处理前检查是否已处理过
# 3. 数据库操作使用唯一约束防止重复插入
# 4. 支付等关键操作使用幂等键（idempotency key）
```

### 解析

Celery 重试机制对标 Java 的 `@Retryable`（Spring Retry）。关键设计点：
1. **指数退避**：避免短时间内大量重试压垮下游服务
2. **随机抖动**：防止多个任务同时重试造成"惊群效应"
3. **幂等性**：确保任务重复执行不会产生副作用，这是分布式系统的基本要求

---

## 题目 5：设计一个 RESTful API，需要注意哪些规范？

> **考察知识点：** REST API 设计
> **关联模块：** [04-frameworks/01-web-frameworks](../../04-frameworks/01-web-frameworks/)

### 题目

设计一个图书管理系统的 REST API，列出端点设计、HTTP 方法选择、状态码使用和错误处理规范。

### 参考答案

```python
"""
RESTful API 设计规范示例（FastAPI）
"""
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

app = FastAPI()

# 1. URL 设计: 使用名词复数，层级关系用嵌套
# GET    /api/v1/books          获取图书列表
# POST   /api/v1/books          创建图书
# GET    /api/v1/books/{id}     获取单本图书
# PUT    /api/v1/books/{id}     更新图书（全量）
# PATCH  /api/v1/books/{id}     更新图书（部分）
# DELETE /api/v1/books/{id}     删除图书
# GET    /api/v1/books/{id}/reviews  获取图书评论（嵌套资源）

# 2. 请求/响应模型
class BookCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    author: str = Field(..., min_length=1)
    isbn: str = Field(..., pattern=r"^\d{13}$")
    price: float = Field(..., gt=0)

# 3. 分页查询
@app.get("/api/v1/books")
def list_books(
    page: int = Query(default=1, ge=1),
    size: int = Query(default=20, ge=1, le=100),
    sort: str = Query(default="-created_at"),
):
    """
    返回格式:
    {
        "items": [...],
        "total": 100,
        "page": 1,
        "size": 20,
        "pages": 5
    }
    """
    pass

# 4. 状态码规范
# 200 OK          — 成功获取/更新
# 201 Created     — 成功创建
# 204 No Content  — 成功删除
# 400 Bad Request — 请求参数错误
# 401 Unauthorized — 未认证
# 403 Forbidden   — 无权限
# 404 Not Found   — 资源不存在
# 409 Conflict    — 资源冲突（如重复创建）
# 422 Unprocessable — 验证失败
# 500 Internal    — 服务器错误

# 5. 统一错误响应格式
class ErrorResponse(BaseModel):
    code: str        # 业务错误码
    message: str     # 用户友好的错误信息
    details: dict | None = None  # 详细错误信息
```

### 解析

REST API 设计的核心原则：资源导向（URL 是名词）、HTTP 方法表达操作、状态码表达结果、统一错误格式。这些规范与 Java Spring Boot 的 REST API 设计完全一致。额外注意 API 版本控制（URL 前缀 `/api/v1/`）和分页规范。

---

## 题目 6：数据库事务在 Python 中如何管理？

> **考察知识点：** 数据库事务
> **关联模块：** [04-frameworks/03-orm](../../04-frameworks/03-orm/)

### 题目

用 SQLAlchemy 演示事务管理，包括自动提交、手动回滚和嵌套事务。

### 参考答案

```python
"""
SQLAlchemy 事务管理（对标 Java @Transactional）
"""
from sqlalchemy.orm import Session

# 方式 1: 上下文管理器自动管理（推荐）
# 对标 Java: @Transactional
with session_factory() as session:
    try:
        user = User(name="张三", email="zhangsan@example.com")
        session.add(user)
        order = Order(user_id=user.id, amount=99.9)
        session.add(order)
        session.commit()      # 成功则提交
    except Exception:
        session.rollback()    # 失败则回滚
        raise

# 方式 2: begin() 自动提交/回滚
# 对标 Java: try-with-resources + @Transactional
with session_factory.begin() as session:
    # begin() 块结束时自动 commit
    # 异常时自动 rollback
    session.add(User(name="李四"))

# 方式 3: Savepoint（嵌套事务）
# 对标 Java: @Transactional(propagation = NESTED)
with session_factory() as session:
    session.add(User(name="外层用户"))

    savepoint = session.begin_nested()  # 创建保存点
    try:
        session.add(User(name="内层用户"))
        # 如果内层失败，只回滚到保存点
        savepoint.commit()
    except Exception:
        savepoint.rollback()  # 只回滚内层操作

    session.commit()  # 外层用户仍然会被保存

# FastAPI 中的事务管理（依赖注入模式）
def get_db():
    db = session_factory()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
```

### 解析

Python 的事务管理比 Java 更显式——没有 `@Transactional` 注解的魔法，需要手动管理 `commit()` 和 `rollback()`。推荐使用上下文管理器（`with` 语句）确保事务正确关闭。在 FastAPI 中，通常通过依赖注入（`Depends`）管理数据库会话的生命周期。

---

## 题目 7：微服务之间如何通信？对比 HTTP 和 gRPC。

> **考察知识点：** 微服务通信
> **关联模块：** [04-frameworks/05-microservice](../../04-frameworks/05-microservice/)

### 题目

对比微服务间 HTTP REST 和 gRPC 两种通信方式的优缺点，说明各自适用场景。

### 参考答案

```python
"""
微服务通信方式对比
"""

comparison = {
    "HTTP REST": {
        "协议": "HTTP/1.1 或 HTTP/2",
        "数据格式": "JSON（文本）",
        "优点": [
            "通用性强，任何语言/工具都支持",
            "可读性好，便于调试",
            "浏览器可直接调用",
            "生态丰富（Swagger、Postman）",
        ],
        "缺点": [
            "JSON 序列化/反序列化开销大",
            "没有强类型约束，接口变更容易出错",
            "不支持双向流",
        ],
        "适用场景": "对外 API、前后端通信、简单微服务",
        "Python框架": "FastAPI / Flask + requests/httpx",
    },
    "gRPC": {
        "协议": "HTTP/2",
        "数据格式": "Protocol Buffers（二进制）",
        "优点": [
            "性能高（二进制序列化，比 JSON 快 5-10 倍）",
            "强类型（.proto 文件定义接口）",
            "支持双向流（Streaming）",
            "自动生成客户端代码",
        ],
        "缺点": [
            "可读性差（二进制格式）",
            "浏览器不能直接调用",
            "需要学习 Protobuf",
            "调试不如 REST 方便",
        ],
        "适用场景": "内部微服务通信、高性能场景、多语言系统",
        "Python框架": "grpcio + grpcio-tools",
    },
}

# 选型建议:
# 对外 API → HTTP REST（通用性）
# 内部服务间 → gRPC（性能）
# 实时数据流 → gRPC Streaming
# 简单场景 → HTTP REST（降低复杂度）
```

### 解析

微服务通信选型的核心考量是**性能 vs 通用性**。gRPC 在内部服务间通信中性能优势明显（对标 Java gRPC），但 HTTP REST 的通用性和可调试性更好。实际项目中常见的做法是：对外暴露 REST API，内部服务间使用 gRPC。

---

## 题目 8：Python 中常用的设计模式有哪些？

> **考察知识点：** 设计模式
> **关联模块：** [04-frameworks/07-architecture-patterns](../../04-frameworks/07-architecture-patterns/)

### 题目

列举 Python 中常用的 3 种设计模式，并用代码演示。

### 参考答案

```python
"""
Python 常用设计模式
"""

# 1. 单例模式（Singleton）— 对标 Java Spring Bean 默认作用域
class DatabaseConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.connected = False
        return cls._instance

    def connect(self):
        self.connected = True
        return self

# Python 更常用模块级单例（模块天然是单例）
# db.py
# connection = DatabaseConnection()  # 模块导入时创建，全局唯一

# 2. 工厂模式（Factory）— 对标 Java Factory Pattern
class Serializer:
    @staticmethod
    def create(format_type: str):
        serializers = {
            "json": JsonSerializer,
            "xml": XmlSerializer,
            "yaml": YamlSerializer,
        }
        cls = serializers.get(format_type)
        if not cls:
            raise ValueError(f"不支持的格式: {format_type}")
        return cls()

# 3. 装饰器模式（Decorator）— Python 原生支持
import functools
import time

def retry(max_retries=3, delay=1):
    """重试装饰器 — 对标 Java @Retryable"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise
                    time.sleep(delay * (attempt + 1))
        return wrapper
    return decorator

@retry(max_retries=3, delay=2)
def call_api(url):
    """带重试的 API 调用"""
    pass
```

### 解析

Python 的设计模式实现通常比 Java 更简洁：
- **单例**：Python 用模块级变量即可，不需要 Java 的 `synchronized` 或双重检查锁
- **工厂**：Python 用字典映射替代 Java 的 `switch-case` 或抽象工厂
- **装饰器**：Python 原生语法支持，比 Java 的代理模式简洁得多

---

## 题目 9：如何优化 Python Web 应用的性能？

> **考察知识点：** 性能优化
> **关联模块：** [04-frameworks/01-web-frameworks](../../04-frameworks/01-web-frameworks/)

### 题目

列举 Python Web 应用常见的性能瓶颈和优化方案。

### 参考答案

```python
"""
Python Web 应用性能优化策略
"""

optimization_strategies = {
    "1. 数据库优化": {
        "问题": "N+1 查询、慢查询、连接池不足",
        "方案": [
            "使用 joinedload/selectinload 预加载关联数据",
            "添加数据库索引（Index）",
            "使用连接池（SQLAlchemy pool_size 配置）",
            "读写分离（主从复制）",
        ],
    },
    "2. 缓存策略": {
        "问题": "重复计算、频繁数据库查询",
        "方案": [
            "Redis 缓存热点数据",
            "functools.lru_cache 缓存函数结果",
            "HTTP 缓存头（ETag、Cache-Control）",
        ],
        "代码": """
from functools import lru_cache

@lru_cache(maxsize=128)
def get_config(key: str) -> str:
    return db.query(Config).filter_by(key=key).first().value
""",
    },
    "3. 异步处理": {
        "问题": "同步阻塞导致吞吐量低",
        "方案": [
            "使用 FastAPI + async/await 处理 I/O",
            "耗时任务交给 Celery 异步执行",
            "使用 asyncio.gather 并发请求",
        ],
    },
    "4. 部署优化": {
        "问题": "单进程无法利用多核 CPU",
        "方案": [
            "gunicorn/uvicorn 多 Worker 进程",
            "Nginx 反向代理 + 负载均衡",
            "Docker + K8s 水平扩展",
        ],
    },
}

# 性能分析工具
profiling_tools = {
    "cProfile": "Python 内置性能分析器",
    "py-spy": "采样式性能分析（不影响运行速度）",
    "line_profiler": "逐行性能分析",
    "django-debug-toolbar": "Django 请求分析",
    "slowapi": "FastAPI 限流中间件",
}
```

### 解析

Python Web 性能优化的核心思路与 Java 类似：减少数据库查询、善用缓存、异步处理耗时操作、水平扩展。Python 特有的注意点是 GIL 限制了多线程的 CPU 并行能力，因此多进程（gunicorn workers）比多线程更有效。

---

## 题目 10：Python Web 应用如何部署到生产环境？

> **考察知识点：** 部署方案
> **关联模块：** [04-frameworks/01-web-frameworks](../../04-frameworks/01-web-frameworks/)

### 题目

描述一个 FastAPI 应用从开发到生产部署的完整流程。

### 参考答案

```python
"""
FastAPI 生产部署方案
"""

# 1. Dockerfile
dockerfile = """
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
"""

# 2. docker-compose.yml（开发环境）
docker_compose = """
version: '3.8'
services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/mydb
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis
  db:
    image: postgres:15
    environment:
      POSTGRES_PASSWORD: pass
  redis:
    image: redis:7-alpine
  celery:
    build: .
    command: celery -A tasks worker --loglevel=info
    depends_on:
      - redis
"""

# 3. Nginx 反向代理配置
nginx_config = """
upstream fastapi {
    server 127.0.0.1:8000;
    server 127.0.0.1:8001;  # 多实例负载均衡
}

server {
    listen 80;
    server_name api.example.com;

    location / {
        proxy_pass http://fastapi;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
"""

# 4. 部署检查清单
checklist = [
    "环境变量管理（不要硬编码密钥）",
    "日志配置（结构化日志 + 集中收集）",
    "健康检查端点（/health）",
    "数据库迁移（Alembic migrate）",
    "HTTPS 证书（Let's Encrypt）",
    "监控告警（Prometheus + Grafana）",
    "CI/CD 流水线（GitHub Actions）",
    "备份策略（数据库定期备份）",
]
```

### 解析

Python Web 应用的生产部署流程与 Java 类似：容器化（Docker）→ 反向代理（Nginx）→ 进程管理（uvicorn workers）→ 监控告警。关键区别是 Python 使用 WSGI/ASGI 服务器（gunicorn/uvicorn）替代 Java 的 Tomcat/Netty，使用 Alembic 替代 Flyway 做数据库迁移。
