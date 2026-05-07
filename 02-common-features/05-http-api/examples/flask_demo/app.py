#!/usr/bin/env python3
"""
Flask 完整 REST API 示例

模块: 02-常用功能
知识点: HTTP API 开发
Python 版本: >= 3.9
最后验证: 2025-07-15

运行方式:
    flask run
    # 或 python app.py

依赖安装:
    pip install flask

描述:
    演示 Flask 的核心功能：
    1. 路由定义与 HTTP 方法
    2. 请求参数解析（JSON/查询参数）
    3. JSON 响应与状态码
    4. 错误处理（errorhandler）
    5. CRUD 完整示例
"""

from flask import Flask, jsonify, request, abort

app = Flask(__name__)


# ============================================================
# 内存数据存储
# ============================================================

tasks: list[dict] = [
    {"id": 1, "title": "学习 Flask", "description": "完成 REST API 示例", "priority": 3, "done": False},
    {"id": 2, "title": "学习 FastAPI", "description": "对比两个框架", "priority": 2, "done": False},
]
next_id = 3


# ============================================================
# 辅助函数
# ============================================================

def find_task(task_id: int) -> dict:
    """根据 ID 查找任务"""
    task = next((t for t in tasks if t["id"] == task_id), None)
    if not task:
        abort(404, description=f"任务 {task_id} 不存在")
    return task


def validate_task_data(data: dict, required: bool = True) -> tuple[dict | None, str | None]:
    """验证任务数据（Flask 需要手动验证）"""
    if not data:
        return None, "请求体不能为空"

    if required:
        if "title" not in data or not data["title"].strip():
            return None, "title 字段不能为空"

    if "title" in data and len(data["title"]) > 100:
        return None, "title 长度不能超过 100"

    if "priority" in data:
        if not isinstance(data["priority"], int) or not (1 <= data["priority"] <= 5):
            return None, "priority 必须是 1-5 的整数"

    return data, None


# ============================================================
# API 端点
# ============================================================

@app.route("/")
def root():
    """根路径"""
    return jsonify({"message": "欢迎使用任务管理 API (Flask)", "api_base": "/api/tasks"})


@app.route("/api/tasks", methods=["GET"])
def list_tasks():
    """获取任务列表 — 支持查询参数筛选"""
    result = tasks

    # 查询参数筛选
    done_param = request.args.get("done")
    if done_param is not None:
        done = done_param.lower() == "true"
        result = [t for t in result if t["done"] == done]

    priority_param = request.args.get("priority")
    if priority_param is not None:
        try:
            priority = int(priority_param)
            result = [t for t in result if t["priority"] == priority]
        except ValueError:
            return jsonify({"error": "priority 必须是整数"}), 400

    return jsonify(result)


@app.route("/api/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id: int):
    """获取单个任务"""
    return jsonify(find_task(task_id))


@app.route("/api/tasks", methods=["POST"])
def create_task():
    """创建任务 — 手动验证请求体"""
    global next_id

    data = request.get_json(silent=True)
    validated, error = validate_task_data(data, required=True)
    if error:
        return jsonify({"error": error}), 400

    new_task = {
        "id": next_id,
        "title": validated["title"].strip(),
        "description": validated.get("description", ""),
        "priority": validated.get("priority", 1),
        "done": False,
    }
    tasks.append(new_task)
    next_id += 1

    return jsonify(new_task), 201


@app.route("/api/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id: int):
    """更新任务"""
    task = find_task(task_id)

    data = request.get_json(silent=True)
    validated, error = validate_task_data(data, required=False)
    if error:
        return jsonify({"error": error}), 400

    if "title" in validated:
        task["title"] = validated["title"].strip()
    if "description" in validated:
        task["description"] = validated["description"]
    if "priority" in validated:
        task["priority"] = validated["priority"]
    if "done" in validated:
        task["done"] = bool(validated["done"])

    return jsonify(task)


@app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id: int):
    """删除任务"""
    task = find_task(task_id)
    tasks.remove(task)
    return "", 204


# ============================================================
# 错误处理
# ============================================================

@app.errorhandler(404)
def not_found(error):
    """404 错误处理"""
    return jsonify({"error": str(error.description)}), 404


@app.errorhandler(400)
def bad_request(error):
    """400 错误处理"""
    return jsonify({"error": str(error.description)}), 400


@app.errorhandler(500)
def internal_error(error):
    """500 错误处理"""
    return jsonify({"error": "服务器内部错误"}), 500


# ============================================================
# 直接运行支持
# ============================================================

if __name__ == "__main__":
    print("启动 Flask 服务...")
    print("API 地址: http://127.0.0.1:5000/api/tasks")
    app.run(debug=True, host="127.0.0.1", port=5000)
