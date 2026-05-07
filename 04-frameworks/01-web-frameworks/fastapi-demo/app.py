#!/usr/bin/env python3
"""
FastAPI REST API 完整示例

模块: 04-框架与架构
知识点: Web 框架 - FastAPI
Python 版本: >= 3.9
最后验证: 2025-07-15

运行方式:
    uvicorn app:app --reload
    # 或直接运行: python app.py
    # 访问 http://127.0.0.1:8000/docs 查看 Swagger 文档

依赖安装:
    pip install fastapi uvicorn pydantic

描述:
    演示 FastAPI 核心功能：
    1. Pydantic 模型验证（对标 Java Bean Validation）
    2. CRUD 路由（GET/POST/PUT/DELETE）
    3. 查询参数与路径参数
    4. 全局异常处理
    5. 自动生成 OpenAPI 文档
"""

from datetime import datetime
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field


# ============================================================
# Pydantic 数据模型（对标 Java DTO + Bean Validation）
# ============================================================

class BookCreate(BaseModel):
    """创建图书请求模型"""
    title: str = Field(..., min_length=1, max_length=200, description="书名")
    author: str = Field(..., min_length=1, max_length=100, description="作者")
    price: float = Field(..., gt=0, description="价格（必须大于 0）")
    category: str = Field(default="未分类", max_length=50, description="分类")


class BookUpdate(BaseModel):
    """更新图书请求模型（所有字段可选）"""
    title: str | None = Field(default=None, min_length=1, max_length=200)
    author: str | None = Field(default=None, min_length=1, max_length=100)
    price: float | None = Field(default=None, gt=0)
    category: str | None = Field(default=None, max_length=50)


class BookResponse(BaseModel):
    """图书响应模型"""
    id: int
    title: str
    author: str
    price: float
    category: str
    created_at: str


# ============================================================
# 应用初始化
# ============================================================

app = FastAPI(
    title="图书管理 API",
    description="FastAPI REST API 示例 — 演示完整 CRUD 和数据验证",
    version="1.0.0",
)

# 内存数据存储（生产环境应使用数据库）
books: list[dict] = [
    {
        "id": 1, "title": "Python 编程", "author": "张三",
        "price": 59.9, "category": "编程",
        "created_at": "2025-01-01T00:00:00",
    },
    {
        "id": 2, "title": "深入理解 JVM", "author": "李四",
        "price": 79.0, "category": "Java",
        "created_at": "2025-01-02T00:00:00",
    },
]
next_id = 3


# ============================================================
# 辅助函数
# ============================================================

def find_book(book_id: int) -> dict:
    """根据 ID 查找图书，未找到抛出 404"""
    book = next((b for b in books if b["id"] == book_id), None)
    if not book:
        raise HTTPException(status_code=404, detail=f"图书 {book_id} 不存在")
    return book


# ============================================================
# API 路由
# ============================================================

@app.get("/")
def root():
    """API 根路径"""
    return {"message": "图书管理 API", "docs": "/docs"}


@app.get("/api/books", response_model=list[BookResponse])
def list_books(
    category: str | None = Query(default=None, description="按分类筛选"),
    min_price: float | None = Query(default=None, ge=0, description="最低价格"),
    max_price: float | None = Query(default=None, ge=0, description="最高价格"),
):
    """获取图书列表 — 支持分类和价格区间筛选"""
    result = books
    if category:
        result = [b for b in result if b["category"] == category]
    if min_price is not None:
        result = [b for b in result if b["price"] >= min_price]
    if max_price is not None:
        result = [b for b in result if b["price"] <= max_price]
    return result


@app.get("/api/books/{book_id}", response_model=BookResponse)
def get_book(book_id: int):
    """获取单本图书"""
    return find_book(book_id)


@app.post("/api/books", response_model=BookResponse, status_code=201)
def create_book(book: BookCreate):
    """创建图书 — Pydantic 自动验证请求体"""
    global next_id
    new_book = {
        "id": next_id,
        **book.model_dump(),
        "created_at": datetime.now().isoformat(),
    }
    books.append(new_book)
    next_id += 1
    return new_book


@app.put("/api/books/{book_id}", response_model=BookResponse)
def update_book(book_id: int, book_update: BookUpdate):
    """更新图书 — 只更新提供的字段（PATCH 语义）"""
    book = find_book(book_id)
    update_data = book_update.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="未提供任何更新字段")
    book.update(update_data)
    return book


@app.delete("/api/books/{book_id}", status_code=204)
def delete_book(book_id: int):
    """删除图书"""
    book = find_book(book_id)
    books.remove(book)
    return None


# ============================================================
# 全局异常处理
# ============================================================

@app.exception_handler(ValueError)
async def value_error_handler(request, exc):
    """捕获值错误，返回 400"""
    return JSONResponse(status_code=400, content={"detail": str(exc)})


# ============================================================
# 直接运行
# ============================================================

def main():
    """启动 FastAPI 开发服务器"""
    try:
        import uvicorn
    except ImportError:
        print("请先安装 uvicorn: pip install uvicorn")
        return
    print("启动 FastAPI 服务...")
    print("API 文档: http://127.0.0.1:8000/docs")
    print("ReDoc 文档: http://127.0.0.1:8000/redoc")
    uvicorn.run(app, host="127.0.0.1", port=8000)


if __name__ == "__main__":
    main()
