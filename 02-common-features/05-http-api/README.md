# HTTP API 开发（FastAPI / Flask）

> **模块：** 02-常用功能
> **难度：** 进阶
> **前置知识：** Python 基础（01-python-basics）
> **Python 版本：** >= 3.9
> **最后验证日期：** 2025-07-15

## 概念说明

HTTP API 开发是 Web 后端的核心技能。Python 生态中最流行的两个 API 框架是 **FastAPI** 和 **Flask**：FastAPI 基于类型注解和异步支持，自动生成 API 文档，性能优异；Flask 轻量灵活，社区庞大，适合快速原型开发。

对于 Java 开发者来说，FastAPI 类似于 Spring Boot + Swagger 的组合（但更简洁），Flask 类似于 Spark Java 或 Javalin。Python 框架的共同特点是：路由定义用装饰器（而非注解+配置类）、请求参数自动解析（无需 `@RequestParam`）、JSON 序列化零配置（无需 Jackson）。

两个框架的核心概念相同：**路由（Route）** 将 URL 映射到处理函数、**请求（Request）** 封装客户端数据、**响应（Response）** 返回处理结果、**中间件（Middleware）** 处理横切关注点。

### FastAPI vs Flask 对比

| 特性 | FastAPI | Flask |
|------|---------|-------|
| 异步支持 | ✅ 原生 async/await | ❌ 需要扩展（Quart） |
| 类型验证 | ✅ Pydantic 自动验证 | ❌ 需手动验证或扩展 |
| API 文档 | ✅ 自动生成 Swagger/ReDoc | ❌ 需要 flask-restx 等扩展 |
| 性能 | 高（基于 Starlette + uvicorn） | 中等（基于 Werkzeug） |
| 学习曲线 | 中等（需了解类型注解） | 低（极简设计） |
| 社区生态 | 快速增长 | 成熟庞大 |
| 适用场景 | 高性能 API、微服务 | 快速原型、小型项目 |
| Java 对标 | Spring Boot + Swagger | Spark Java / Javalin |

### REST API 核心概念

| 概念 | 说明 | 示例 |
|------|------|------|
| GET | 获取资源 | `GET /api/users` |
| POST | 创建资源 | `POST /api/users` |
| PUT | 更新资源（全量） | `PUT /api/users/1` |
| DELETE | 删除资源 | `DELETE /api/users/1` |
| 状态码 200 | 成功 | 查询成功 |
| 状态码 201 | 已创建 | 新建资源成功 |
| 状态码 404 | 未找到 | 资源不存在 |
| 状态码 422 | 验证失败 | 请求参数不合法 |


## Java 对比

| 特性 | Java (Spring Boot) | Python (FastAPI) | Python (Flask) |
|------|-------------------|------------------|----------------|
| 路由定义 | `@GetMapping("/users")` | `@app.get("/users")` | `@app.route("/users")` |
| 请求体解析 | `@RequestBody User user` | `def create(user: User)` | `request.get_json()` |
| 参数验证 | `@Valid` + Bean Validation | Pydantic 自动验证 | 手动验证 |
| JSON 序列化 | Jackson 自动转换 | 自动转换 | `jsonify()` |
| 异常处理 | `@ExceptionHandler` | `@app.exception_handler` | `@app.errorhandler` |
| API 文档 | Springdoc / Swagger | 自动生成 | 需要扩展 |
| 启动方式 | `mvn spring-boot:run` | `uvicorn app:app` | `flask run` |

**Java 写法（Spring Boot）：**
```java
@RestController
@RequestMapping("/api/users")
public class UserController {

    @GetMapping
    public List<User> getUsers() {
        return userService.findAll();
    }

    @PostMapping
    public ResponseEntity<User> createUser(@Valid @RequestBody UserDTO dto) {
        User user = userService.create(dto);
        return ResponseEntity.status(201).body(user);
    }

    @GetMapping("/{id}")
    public User getUser(@PathVariable Long id) {
        return userService.findById(id)
            .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND));
    }
}
```

**Python 写法（FastAPI）：**
```python
from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/api/users")
def get_users():
    return users

@app.post("/api/users", status_code=201)
def create_user(user: UserCreate):
    new_user = {"id": len(users) + 1, **user.model_dump()}
    users.append(new_user)
    return new_user

@app.get("/api/users/{user_id}")
def get_user(user_id: int):
    user = next((u for u in users if u["id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return user
```

## 实战代码

### 示例 1：FastAPI 完整 REST API

**文件：** `examples/fastapi_demo/app.py`

演示 FastAPI 的核心功能：路由定义、Pydantic 请求验证、CRUD 端点、异常处理、查询参数。

**安装依赖：**
```bash
pip install fastapi uvicorn
```

**运行方式：**
```bash
cd examples/fastapi_demo
uvicorn app:app --reload
# 访问 http://127.0.0.1:8000/docs 查看自动生成的 API 文档
```

### 示例 2：Flask 完整 REST API

**文件：** `examples/flask_demo/app.py`

演示 Flask 的核心功能：路由定义、请求处理、JSON 响应、错误处理。

**安装依赖：**
```bash
pip install flask
```

**运行方式：**
```bash
cd examples/flask_demo
flask run
# 或 python app.py
```

## 常见陷阱

### 1. FastAPI 的 async 与 sync 混用

FastAPI 支持同步和异步函数，但混用时需注意：同步函数会在线程池中运行，不会阻塞事件循环。

```python
# ✓ 异步函数：适合 IO 密集型操作
@app.get("/async")
async def async_endpoint():
    data = await fetch_data()
    return data

# ✓ 同步函数：FastAPI 自动放入线程池
@app.get("/sync")
def sync_endpoint():
    data = fetch_data_sync()
    return data

# ✗ 错误：在 async 函数中调用阻塞操作
@app.get("/bad")
async def bad_endpoint():
    import time
    time.sleep(5)  # 会阻塞整个事件循环！
    return {"msg": "done"}
```

### 2. Flask 忘记返回 JSON

Flask 不会自动将 dict 转为 JSON 响应（旧版本），需要使用 `jsonify()`。

```python
from flask import jsonify

# ✗ 旧版 Flask 中不推荐直接返回 dict
@app.route("/api/data")
def get_data():
    return {"key": "value"}  # Flask 2.2+ 支持，旧版不行

# ✓ 推荐：使用 jsonify 确保兼容性
@app.route("/api/data")
def get_data():
    return jsonify({"key": "value"})
```

### 3. 请求体验证不充分

Flask 没有内置的请求体验证，需要手动检查。

```python
# ✗ Flask 中不验证请求体
@app.route("/api/users", methods=["POST"])
def create_user():
    data = request.get_json()
    # data 可能为 None，或缺少必要字段！

# ✓ 手动验证
@app.route("/api/users", methods=["POST"])
def create_user():
    data = request.get_json()
    if not data or "name" not in data:
        return jsonify({"error": "缺少 name 字段"}), 400
```

### 4. 忘记设置正确的 HTTP 状态码

```python
# ✗ 创建资源但返回 200
@app.post("/api/users")
def create_user(user: UserCreate):
    return new_user  # 默认 200，应该是 201

# ✓ FastAPI：指定状态码
@app.post("/api/users", status_code=201)
def create_user(user: UserCreate):
    return new_user

# ✓ Flask：返回元组指定状态码
@app.route("/api/users", methods=["POST"])
def create_user():
    return jsonify(new_user), 201
```

> 💻 **完整可运行代码：** [fastapi_demo/app.py](examples/fastapi_demo/app.py) | [flask_demo/app.py](examples/flask_demo/app.py)

## 参考资料

- [FastAPI 官方文档](https://fastapi.tiangolo.com/zh/)
- [Flask 官方文档](https://flask.palletsprojects.com/zh/)
- [Pydantic 官方文档](https://docs.pydantic.dev/)
- [Real Python - FastAPI Tutorial](https://realpython.com/fastapi-python-web-apis/)
- [Real Python - Flask Tutorial](https://realpython.com/flask-project/)
