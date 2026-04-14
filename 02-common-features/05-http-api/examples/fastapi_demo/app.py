#!/usr/bin/env python3
"""
FastAPI 完整 REST API 示例

模块: 02-常用功能
知识点: HTTP API 开发
Python 版本: >= 3.9
最后验证: 2025-07-15

运行方式:
    uvicorn app:app --reload
    # 访问 http://127.0.0.1:8000/docs 查看 Swagger 文档

依赖安装:
    pip install fastapi uvicorn

描述:
    演示 FastAPI 的核心功能：
    1. Pydantic 模型定义与请求验证
    2. CRUD 端点（GET/POST/PUT/DELETE）
    3. 路径参数与查询参数
    4. 异常处理（HTTPException）
    5. 响应模型与状态码
"""

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field


# ============================================================
# Pydantic 模型定义
# 类似 Java 的 DTO（Data Transfer Object）+ Bean Validation
# ============================================================

class TaskCreate(BaseModel):
    """创建任务的请求模型"""
    title: str = Field(..., min_length=1, max_length=100, description="任务标题")
    description: str = Field(default="", max_length=500, description="任务描述")
    priority: int = Field(default=1, ge=1, le=5, description="优先级 1-5")


class TaskUpdate(BaseModel):
    """更新任务的请求模型"""
    title: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=500)
    priority: int | None = Field(default=None, ge=1, le=5)
    done: bool | None = None


class TaskResponse(BaseModel):
    """任务响应模型"""
    id: int
    title: str
    description: str
    priority: int
    done: bool


# ============================================================
# 应用初始化
# ============================================================

app = FastAPI(
    title="任务管理 API",
    description="FastAPI REST API 示例 — 演示 CRUD 操作",
    version="1.0.0",
)

# 内存数据存储（实际项目中应使用数据库）
tasks: list[dict] = [
    {"id": 1, "title": "学习 FastAPI", "description": "完成 REST API 示例", "priority": 3, "done": False},
    {"id": 2, "title": "学习 Flask", "description": "对比两个框架", "priority": 2, "done": False},
]
next_id = 3


# ============================================================
# 辅助函数
# ============================================================

def find_task(task_id: int) -> dict:
    """根据 ID 查找任务，未找到则抛出 404"""
    task = next((t for t in tasks if t["id"] == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail=f"任务 {task_id} 不存在")
    return task


# ============================================================
# API 端点
# ============================================================

@app.get("/")
def root():
    """根路径 — API 欢迎信息"""
    return {"message": "欢迎使用任务管理 API", "docs": "/docs"}


@app.get("/api/tasks", response_model=list[TaskResponse])
def list_tasks(
    done: bool | None = Query(default=None, description="按完成状态筛选"),
    priority: int | None = Query(default=None, ge=1, le=5, description="按优先级筛选"),
):
    """获取任务列表 — 支持查询参数筛选"""
    result = tasks
    if done is not None:
        result = [t for t in result if t["done"] == done]
    if priority is not None:
        result = [t for t in result if t["priority"] == priority]
    return result


@app.get("/api/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int):
    """获取单个任务 — 路径参数自动验证为 int"""
    return find_task(task_id)


@app.post("/api/tasks", response_model=TaskResponse, status_code=201)
def create_task(task: TaskCreate):
    """创建任务 — Pydantic 自动验证请求体"""
    global next_id
    new_task = {"id": next_id, **task.model_dump(), "done": False}
    tasks.append(new_task)
    next_id += 1
    return new_task


@app.put("/api/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task_update: TaskUpdate):
    """更新任务 — 只更新提供的字段"""
    task = find_task(task_id)
    update_data = task_update.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="未提供任何更新字段")
    task.update(update_data)
    return task


@app.delete("/api/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    """删除任务"""
    task = find_task(task_id)
    tasks.remove(task)
    return None


# ============================================================
# 全局异常处理
# ============================================================

@app.exception_handler(ValueError)
async def value_error_handler(request, exc):
    """处理值错误"""
    return {"detail": str(exc)}


# ============================================================
# 直接运行支持
# ============================================================

if __name__ == "__main__":
    import uvicorn
    print("启动 FastAPI 服务...")
    print("API 文档: http://127.0.0.1:8000/docs")
    uvicorn.run(app, host="127.0.0.1", port=8000)
