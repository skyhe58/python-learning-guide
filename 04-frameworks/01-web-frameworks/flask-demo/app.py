#!/usr/bin/env python3
"""
Flask REST API 完整示例

模块: 04-框架与架构
知识点: Web 框架 - Flask
Python 版本: >= 3.9
最后验证: 2025-07-15

运行方式:
    python app.py
    # 访问 http://127.0.0.1:5000

依赖安装:
    pip install flask

描述:
    演示 Flask 核心功能：
    1. 路由定义与 HTTP 方法
    2. 请求参数解析（JSON、查询参数、路径参数）
    3. 错误处理（abort、自定义错误页面）
    4. 蓝图（Blueprint）模块化组织
    对标 Java Spark / Javalin 轻量级框架
"""

from datetime import datetime
from flask import Flask, jsonify, request, abort


# ============================================================
# 应用初始化
# ============================================================

app = Flask(__name__)

# 内存数据存储
todos: list[dict] = [
    {
        "id": 1, "title": "学习 Flask", "done": False,
        "created_at": "2025-01-01T00:00:00",
    },
    {
        "id": 2, "title": "学习 Django", "done": False,
        "created_at": "2025-01-02T00:00:00",
    },
]
next_id = 3


# ============================================================
# 辅助函数
# ============================================================

def find_todo(todo_id: int) -> dict:
    """根据 ID 查找待办事项"""
    todo = next((t for t in todos if t["id"] == todo_id), None)
    if not todo:
        abort(404, description=f"待办事项 {todo_id} 不存在")
    return todo


def validate_todo_data(data: dict, required: bool = True) -> dict:
    """验证请求数据（Flask 需要手动验证，不像 FastAPI 有 Pydantic）"""
    if not data:
        abort(400, description="请求体不能为空")

    if required and "title" not in data:
        abort(400, description="缺少必填字段: title")

    title = data.get("title")
    if title is not None:
        if not isinstance(title, str) or len(title.strip()) == 0:
            abort(400, description="title 不能为空字符串")
        if len(title) > 200:
            abort(400, description="title 长度不能超过 200")

    return data


# ============================================================
# API 路由
# ============================================================

@app.get("/")
def index():
    """API 根路径"""
    return jsonify({"message": "待办事项 API (Flask)", "version": "1.0.0"})


@app.get("/api/todos")
def list_todos():
    """获取待办列表 — 支持查询参数筛选"""
    done_filter = request.args.get("done")
    result = todos

    if done_filter is not None:
        done_value = done_filter.lower() == "true"
        result = [t for t in result if t["done"] == done_value]

    return jsonify(result)


@app.get("/api/todos/<int:todo_id>")
def get_todo(todo_id: int):
    """获取单个待办事项"""
    return jsonify(find_todo(todo_id))


@app.post("/api/todos")
def create_todo():
    """创建待办事项"""
    global next_id
    data = request.get_json(silent=True)
    validate_todo_data(data, required=True)

    new_todo = {
        "id": next_id,
        "title": data["title"].strip(),
        "done": data.get("done", False),
        "created_at": datetime.now().isoformat(),
    }
    todos.append(new_todo)
    next_id += 1
    return jsonify(new_todo), 201


@app.put("/api/todos/<int:todo_id>")
def update_todo(todo_id: int):
    """更新待办事项"""
    todo = find_todo(todo_id)
    data = request.get_json(silent=True)
    validate_todo_data(data, required=False)

    if "title" in data:
        todo["title"] = data["title"].strip()
    if "done" in data:
        todo["done"] = bool(data["done"])

    return jsonify(todo)


@app.delete("/api/todos/<int:todo_id>")
def delete_todo(todo_id: int):
    """删除待办事项"""
    todo = find_todo(todo_id)
    todos.remove(todo)
    return "", 204


# ============================================================
# 错误处理
# ============================================================

@app.errorhandler(400)
def bad_request(error):
    """400 错误处理"""
    return jsonify({"error": "Bad Request", "message": error.description}), 400


@app.errorhandler(404)
def not_found(error):
    """404 错误处理"""
    return jsonify({"error": "Not Found", "message": error.description}), 404


@app.errorhandler(500)
def internal_error(error):
    """500 错误处理"""
    return jsonify({"error": "Internal Server Error", "message": "服务器内部错误"}), 500


# ============================================================
# 直接运行
# ============================================================

def main():
    """启动 Flask 开发服务器"""
    print("启动 Flask 服务...")
    print("访问: http://127.0.0.1:5000")
    app.run(host="127.0.0.1", port=5000, debug=True)


if __name__ == "__main__":
    main()
