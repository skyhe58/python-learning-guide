# 分层架构 — Controller-Service-Repository

> **对标 Java：** Spring Boot 标准三层架构

## 分层对照

| Python 层 | Java 层 | 职责 |
|-----------|---------|------|
| **Router (API)** | `@RestController` | 接收请求、参数验证、返回响应 |
| **Service** | `@Service` | 业务逻辑、事务管理 |
| **Repository** | `@Repository` | 数据访问、SQL 查询 |
| **Schema (DTO)** | DTO / VO | 数据传输对象 |
| **Model** | `@Entity` | 数据库实体 |

## 项目目录结构（FastAPI 示例）

```
myproject/
├── main.py                        # 应用入口
├── config.py                      # 配置管理（对标 application.yml）
├── database.py                    # 数据库连接配置
│
├── api/                           # API 层（对标 Controller 层）
│   ├── __init__.py
│   ├── deps.py                    # 依赖注入（对标 Spring DI）
│   ├── v1/                        # API 版本
│   │   ├── __init__.py
│   │   ├── users.py               # 用户路由
│   │   └── orders.py              # 订单路由
│   └── router.py                  # 路由汇总
│
├── services/                      # Service 层（业务逻辑）
│   ├── __init__.py
│   ├── user_service.py
│   └── order_service.py
│
├── repositories/                  # Repository 层（数据访问）
│   ├── __init__.py
│   ├── user_repository.py
│   └── order_repository.py
│
├── models/                        # 数据库模型（对标 Entity）
│   ├── __init__.py
│   ├── user.py
│   └── order.py
│
├── schemas/                       # Pydantic 模型（对标 DTO）
│   ├── __init__.py
│   ├── user.py
│   └── order.py
│
├── core/                          # 核心工具
│   ├── __init__.py
│   ├── exceptions.py              # 自定义异常
│   └── security.py                # 认证授权
│
└── tests/                         # 测试
    ├── test_users.py
    └── test_orders.py
```

## 关键代码示例

### Router（API 层）
```python
# api/v1/users.py
from fastapi import APIRouter, Depends
from services.user_service import UserService
from schemas.user import UserCreate, UserResponse

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserResponse, status_code=201)
def create_user(data: UserCreate, service: UserService = Depends()):
    return service.create(data)

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, service: UserService = Depends()):
    return service.find_by_id(user_id)
```

### Service（业务逻辑层）
```python
# services/user_service.py
from fastapi import Depends, HTTPException
from repositories.user_repository import UserRepository
from schemas.user import UserCreate

class UserService:
    def __init__(self, repo: UserRepository = Depends()):
        self.repo = repo

    def create(self, data: UserCreate):
        if self.repo.find_by_email(data.email):
            raise HTTPException(400, "邮箱已存在")
        return self.repo.create(data)

    def find_by_id(self, user_id: int):
        user = self.repo.get(user_id)
        if not user:
            raise HTTPException(404, "用户不存在")
        return user
```

### Repository（数据访问层）
```python
# repositories/user_repository.py
from fastapi import Depends
from sqlalchemy.orm import Session
from database import get_db
from models.user import User

class UserRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def get(self, user_id: int) -> User | None:
        return self.db.query(User).filter(User.id == user_id).first()

    def find_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()

    def create(self, data) -> User:
        user = User(**data.model_dump())
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
```

## 分层原则

1. **上层依赖下层**：Router → Service → Repository
2. **同层不互相调用**：Service 之间通过事件或上层协调
3. **依赖倒置**：Service 依赖 Repository 的抽象（Protocol），不依赖具体实现
