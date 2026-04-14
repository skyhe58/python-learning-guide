# 框架与架构 速查卡片

## 核心概念

| 概念 | 说明 | 对标 Java |
|------|------|-----------|
| Django | 全栈 Web 框架，内置 ORM/Admin/认证 | Spring Boot |
| FastAPI | 异步高性能 API 框架，自动生成文档 | Spring WebFlux |
| Flask | 轻量级微框架，按需扩展 | Spark / Javalin |
| SQLAlchemy | Python 最强大的 ORM | Hibernate / MyBatis |
| Celery | 分布式任务队列 | Spring Async + RabbitMQ |
| asyncio | Python 原生异步编程 | CompletableFuture |
| APScheduler | 定时任务调度 | Quartz / @Scheduled |
| gRPC | 高性能 RPC 框架 | Java gRPC |

## Web 框架速查

### FastAPI

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float

@app.get("/items/{item_id}")
def get_item(item_id: int):
    return {"id": item_id}

@app.post("/items", status_code=201)
def create_item(item: Item):
    return item

# 运行: uvicorn app:app --reload
```

### Flask

```python
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.get("/items/<int:item_id>")
def get_item(item_id):
    return jsonify({"id": item_id})

@app.post("/items")
def create_item():
    data = request.get_json()
    return jsonify(data), 201

# 运行: python app.py 或 flask run
```

### Django REST

```python
# views.py
from rest_framework import viewsets
from .models import Item
from .serializers import ItemSerializer

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
```

## ORM 速查

### SQLAlchemy 2.0

```python
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))

# CRUD
session.add(User(name="张三"))       # Create
session.query(User).all()            # Read
user.name = "李四"; session.commit()  # Update
session.delete(user)                  # Delete

# 避免 N+1: 使用 joinedload
from sqlalchemy.orm import joinedload
session.query(User).options(joinedload(User.orders)).all()
```

## 异步编程速查

### asyncio

```python
import asyncio

async def fetch(url):
    await asyncio.sleep(1)
    return f"Result from {url}"

# 并发执行
results = await asyncio.gather(fetch("a"), fetch("b"))

# 控制并发数
sem = asyncio.Semaphore(5)
async with sem:
    await fetch("url")

# 入口
asyncio.run(main())
```

### Celery

```python
# 定义任务
@app.task(bind=True, max_retries=3)
def send_email(self, to, body):
    try:
        do_send(to, body)
    except Exception as exc:
        raise self.retry(exc=exc, countdown=60)

# 调用任务
result = send_email.delay("user@example.com", "Hello")
result.get(timeout=10)  # 等待结果
```

## 定时任务速查

### APScheduler

```python
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()

# 间隔触发
scheduler.add_job(func, "interval", seconds=30)

# Cron 触发
scheduler.add_job(func, "cron", hour=9, minute=0, day_of_week="mon-fri")

# 一次性触发
scheduler.add_job(func, "date", run_date="2025-12-31 23:59:59")

scheduler.start()
```

## 常见陷阱

- ⚠️ Django View = Java Controller，不要混淆
- ⚠️ asyncio 中不要用 `time.sleep()`，用 `asyncio.sleep()`
- ⚠️ SQLAlchemy 忘记 `session.commit()` 数据不会持久化
- ⚠️ Celery Worker 和主应用是独立进程，不共享内存
- ⚠️ FastAPI 路径参数自动类型转换，不需要手动 `int()`
- ⚠️ ORM N+1 问题：遍历关联对象时用 `joinedload` 预加载
- ⚠️ APScheduler `BlockingScheduler` 会阻塞主线程，Web 应用用 `BackgroundScheduler`

## 面试高频考点

- Django vs FastAPI vs Flask 选型依据
- asyncio 事件循环原理和 GIL 的关系
- Celery 任务重试机制和幂等性设计
- ORM N+1 查询问题及解决方案
- 微服务中的断路器模式
- REST API 设计最佳实践
- 分层架构 vs DDD 的适用场景
