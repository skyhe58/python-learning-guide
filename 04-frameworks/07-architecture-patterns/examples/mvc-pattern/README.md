# MVC 模式 — Django MTV 项目结构

> **对标 Java：** Spring MVC

## Django MTV vs Java Spring MVC

| Django MTV | Java Spring MVC | 职责 |
|-----------|----------------|------|
| **Model** | `@Entity` | 数据模型和业务逻辑 |
| **Template** | JSP / Thymeleaf (View) | 页面渲染 |
| **View** | `@Controller` | 请求处理和响应 |

> 注意：Django 的 View 对应 Java 的 Controller，Django 的 Template 对应 Java 的 View。

## 项目目录结构

```
myproject/
├── manage.py                      # 项目管理入口
├── myproject/                     # 项目配置
│   ├── __init__.py
│   ├── settings.py                # 全局配置（对标 application.yml）
│   ├── urls.py                    # 根路由
│   └── wsgi.py
│
├── users/                         # 用户模块（Django App）
│   ├── __init__.py
│   ├── models.py                  # Model — 数据模型
│   │   └── class User(models.Model)
│   ├── views.py                   # View — 请求处理（对标 Controller）
│   │   └── class UserListView(ListView)
│   ├── templates/                 # Template — 页面模板（对标 View）
│   │   └── users/
│   │       ├── user_list.html
│   │       └── user_detail.html
│   ├── urls.py                    # 模块路由
│   ├── forms.py                   # 表单验证（对标 @Valid DTO）
│   ├── admin.py                   # Admin 后台
│   ├── tests.py                   # 单元测试
│   └── migrations/                # 数据库迁移
│
├── orders/                        # 订单模块
│   ├── models.py
│   ├── views.py
│   ├── templates/
│   └── ...
│
├── templates/                     # 全局模板
│   └── base.html                  # 基础模板（布局）
│
└── static/                        # 静态文件（CSS/JS/图片）
```

## 关键代码示例

### Model（数据模型）
```python
# users/models.py
from django.db import models

class User(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
```

### View（请求处理 — 对标 Controller）
```python
# users/views.py
from django.views.generic import ListView, DetailView
from .models import User

class UserListView(ListView):
    model = User
    template_name = "users/user_list.html"
    context_object_name = "users"
    paginate_by = 20
```

### Template（页面渲染 — 对标 View）
```html
<!-- users/templates/users/user_list.html -->
{% extends "base.html" %}
{% block content %}
<h1>用户列表</h1>
{% for user in users %}
  <p>{{ user.name }} - {{ user.email }}</p>
{% endfor %}
{% endblock %}
```

### URL 路由
```python
# users/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.UserListView.as_view(), name="user-list"),
]
```
