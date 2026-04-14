# Web 框架对比：Django / FastAPI / Flask

> **模块：** 04-框架与架构
> **难度：** 进阶
> **前置知识：** Python 基础、HTTP 协议基础
> **Python 版本：** >= 3.9
> **最后验证日期：** 2025-07-15

## 概念说明

Python Web 框架生态丰富，三大主流框架各有定位：

- **Django** — 全栈框架，"batteries included"，内置 ORM、Admin、认证系统，适合快速构建完整 Web 应用。对标 Java Spring Boot。
- **FastAPI** — 现代异步框架，基于 Starlette + Pydantic，自动生成 OpenAPI 文档，性能优异。对标 Java Spring WebFlux。
- **Flask** — 轻量级微框架，核心精简，通过扩展按需组装。对标 Java Spark / Javalin。

## Java 框架对比表

| 维度 | Django | FastAPI | Flask | Spring Boot | Spring WebFlux |
|------|--------|---------|-------|-------------|----------------|
| **功能定位** | 全栈框架 | 高性能 API 框架 | 轻量微框架 | 全栈框架 | 响应式框架 |
| **学习曲线** | 中等（概念多） | 低（类型提示驱动） | 低（核心简单） | 高（生态庞大） | 高（响应式编程） |
| **适用场景** | CMS、电商、管理后台 | REST API、微服务 | 小型应用、原型 | 企业级应用 | 高并发 API |
| **ORM** | 内置 Django ORM | 无（搭配 SQLAlchemy） | 无（搭配 SQLAlchemy） | Spring Data JPA | Spring Data R2DBC |
| **异步支持** | Django 4.1+ 部分支持 | 原生 async/await | 需要 Quart 扩展 | @Async | 原生 Mono/Flux |
| **API 文档** | 需要 DRF + drf-yasg | 自动生成 Swagger | 需要 Flask-RESTX | Springdoc | Springdoc |
| **请求验证** | Django Forms/Serializers | Pydantic（自动） | 手动或 Marshmallow | Bean Validation | Bean Validation |
| **社区活跃度** | ⭐⭐⭐⭐⭐ 非常活跃 | ⭐⭐⭐⭐⭐ 增长最快 | ⭐⭐⭐⭐ 成熟稳定 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **GitHub Stars** | 80k+ | 78k+ | 68k+ | 75k+ | — |

## Java 对比

**Java Spring Boot 写法：**
```java
@RestController
@RequestMapping("/api/users")
public class UserController {
    @GetMapping("/{id}")
    public ResponseEntity<User> getUser(@PathVariable Long id) {
        User user = userService.findById(id);
        if (user == null) {
            return ResponseEntity.notFound().build();
        }
        return ResponseEntity.ok(user);
    }

    @PostMapping
    public ResponseEntity<User> createUser(@Valid @RequestBody UserDTO dto) {
        User user = userService.create(dto);
        return ResponseEntity.status(HttpStatus.CREATED).body(user);
    }
}
```

**Python FastAPI 写法：**
```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

@app.get("/api/users/{user_id}")
def get_user(user_id: int):
    user = user_service.find_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return user

@app.post("/api/users", status_code=201)
def create_user(dto: UserDTO):
    return user_service.create(dto)
```

**Python Flask 写法：**
```python
from flask import Flask, jsonify, request, abort

app = Flask(__name__)

@app.get("/api/users/<int:user_id>")
def get_user(user_id):
    user = user_service.find_by_id(user_id)
    if not user:
        abort(404, description="用户不存在")
    return jsonify(user)

@app.post("/api/users")
def create_user():
    data = request.get_json()
    user = user_service.create(data)
    return jsonify(user), 201
```

## 实战代码

### 示例 1：FastAPI REST API

**文件：** `fastapi-demo/app.py`

完整的 FastAPI CRUD 示例，包含 Pydantic 验证、路由分组、错误处理。

**运行方式：**
```bash
pip install fastapi uvicorn
uvicorn app:app --reload
# 访问 http://127.0.0.1:8000/docs 查看 Swagger 文档
```

### 示例 2：Flask REST API

**文件：** `flask-demo/app.py`

完整的 Flask CRUD 示例，包含请求处理、错误处理、蓝图组织。

**运行方式：**
```bash
pip install flask
python app.py
# 访问 http://127.0.0.1:5000
```

### 示例 3：Django REST API 项目结构

**文件：** `django-demo/README.md`

Django REST Framework 项目结构说明和关键代码片段。

## 选型建议

| 场景 | 推荐框架 | 原因 |
|------|----------|------|
| 快速原型 / MVP | Flask | 上手最快，灵活度高 |
| REST API / 微服务 | FastAPI | 性能好，自动文档，类型安全 |
| 全栈 Web 应用 | Django | 内置功能齐全，开发效率高 |
| 高并发异步服务 | FastAPI | 原生 async，性能接近 Go |
| 管理后台 / CMS | Django | Admin 开箱即用 |

## 常见陷阱

- ⚠️ Django 的 MTV 模式（Model-Template-View）中的 View 对应 Java 的 Controller，不要混淆
- ⚠️ FastAPI 的路径参数类型声明会自动验证，不需要手动转换类型
- ⚠️ Flask 默认不支持异步，如需异步请使用 Quart 或升级到 Flask 2.0+ 配合 `async def`
- ⚠️ Django 项目结构较重，小型 API 项目建议用 FastAPI 或 Flask

> 💻 **完整可运行代码：** [fastapi-demo/app.py](fastapi-demo/app.py) | [flask-demo/app.py](flask-demo/app.py) | [django-demo/](django-demo/)

## 参考资料

- [Django 官方文档](https://docs.djangoproject.com/)
- [FastAPI 官方文档](https://fastapi.tiangolo.com/)
- [Flask 官方文档](https://flask.palletsprojects.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
