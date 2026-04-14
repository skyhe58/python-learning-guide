# Django REST API 项目示例

> **框架：** Django 4.2+ / Django REST Framework
> **对标 Java：** Spring Boot + Spring Data JPA
> **Python 版本：** >= 3.9

## 项目结构

```
myproject/
├── manage.py                  # 项目管理入口（类似 Java 的 mvn/gradle 命令）
├── myproject/
│   ├── __init__.py
│   ├── settings.py            # 全局配置（类似 application.yml）
│   ├── urls.py                # 根路由（类似 Spring 的 @RequestMapping）
│   ├── wsgi.py                # WSGI 部署入口
│   └── asgi.py                # ASGI 异步部署入口
├── tasks/                     # 应用模块（类似 Java 的一个 Module）
│   ├── __init__.py
│   ├── models.py              # 数据模型（类似 JPA @Entity）
│   ├── serializers.py         # 序列化器（类似 Java DTO + Validator）
│   ├── views.py               # 视图/控制器（类似 @RestController）
│   ├── urls.py                # 应用路由
│   ├── admin.py               # Admin 后台配置
│   ├── tests.py               # 单元测试
│   └── migrations/            # 数据库迁移（类似 Flyway/Liquibase）
│       └── 0001_initial.py
└── requirements.txt
```

## 关键代码片段

### 1. 数据模型（models.py）

```python
# 类似 Java 的 @Entity + JPA 注解
from django.db import models

class Task(models.Model):
    """任务模型 — 对标 Java @Entity"""
    title = models.CharField(max_length=100, verbose_name="标题")
    description = models.TextField(blank=True, default="", verbose_name="描述")
    priority = models.IntegerField(default=1, verbose_name="优先级")
    done = models.BooleanField(default=False, verbose_name="是否完成")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "任务"

    def __str__(self):
        return self.title
```

### 2. 序列化器（serializers.py）

```python
# 类似 Java 的 DTO + Bean Validation
from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    """任务序列化器 — 自动根据 Model 生成字段验证"""
    class Meta:
        model = Task
        fields = ["id", "title", "description", "priority", "done",
                  "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]
```

### 3. 视图（views.py）

```python
# 类似 Java 的 @RestController
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Task
from .serializers import TaskSerializer

class TaskViewSet(viewsets.ModelViewSet):
    """
    任务 CRUD ViewSet — 一个类搞定所有 CRUD 端点
    对标 Java Spring Data REST 的自动生成 CRUD
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    # GET /api/tasks/        → list()    自动提供
    # POST /api/tasks/       → create()  自动提供
    # GET /api/tasks/{id}/   → retrieve() 自动提供
    # PUT /api/tasks/{id}/   → update()  自动提供
    # DELETE /api/tasks/{id}/ → destroy() 自动提供
```

### 4. 路由配置（urls.py）

```python
# 类似 Java 的 @RequestMapping 路由注册
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from tasks.views import TaskViewSet

router = DefaultRouter()
router.register(r"tasks", TaskViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
]
```

## 快速启动命令

```bash
# 创建项目
pip install django djangorestframework
django-admin startproject myproject
cd myproject

# 创建应用
python manage.py startapp tasks

# 数据库迁移（类似 Flyway migrate）
python manage.py makemigrations
python manage.py migrate

# 创建管理员
python manage.py createsuperuser

# 启动开发服务器
python manage.py runserver
# 访问 http://127.0.0.1:8000/api/
# 访问 http://127.0.0.1:8000/admin/ 进入管理后台
```

## Django vs Spring Boot 对比

| Django | Spring Boot | 说明 |
|--------|-------------|------|
| `models.py` | `@Entity` 类 | 数据模型定义 |
| `serializers.py` | DTO + `@Valid` | 请求验证和序列化 |
| `views.py` | `@RestController` | 业务逻辑处理 |
| `urls.py` | `@RequestMapping` | 路由配置 |
| `settings.py` | `application.yml` | 全局配置 |
| `migrations/` | Flyway/Liquibase | 数据库版本管理 |
| `admin.py` | 无（需自建） | 管理后台（Django 独有优势） |
| `manage.py` | `mvn spring-boot:run` | 项目管理命令 |
