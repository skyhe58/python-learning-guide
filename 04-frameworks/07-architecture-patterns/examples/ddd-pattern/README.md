# DDD（领域驱动设计）— Python 实践

> **对标 Java：** Spring + DDD 六边形架构

## DDD 核心概念

| DDD 概念 | Python 实现 | Java 实现 | 说明 |
|----------|------------|-----------|------|
| **Entity（实体）** | dataclass / Pydantic | `@Entity` | 有唯一标识的领域对象 |
| **Value Object（值对象）** | frozen dataclass | 不可变类 | 无标识，按值比较 |
| **Aggregate（聚合）** | 类 + 内部方法 | 类 + 内部方法 | 一组相关对象的集合 |
| **Repository（仓储）** | Protocol + 实现类 | Interface + 实现类 | 聚合的持久化接口 |
| **Domain Service（领域服务）** | 普通类 | `@Service` | 跨聚合的业务逻辑 |
| **Application Service（应用服务）** | 普通类 | `@Service` | 用例编排 |

## 项目目录结构

```
myproject/
├── main.py                            # 应用入口
├── config.py                          # 配置
│
├── domain/                            # 领域层（核心，不依赖任何外部框架）
│   ├── __init__.py
│   ├── models/                        # 领域模型
│   │   ├── __init__.py
│   │   ├── order.py                   # Order 聚合根
│   │   ├── order_item.py             # OrderItem 实体
│   │   └── money.py                   # Money 值对象
│   ├── repositories/                  # 仓储接口（Protocol）
│   │   ├── __init__.py
│   │   └── order_repository.py        # OrderRepository Protocol
│   ├── services/                      # 领域服务
│   │   ├── __init__.py
│   │   └── pricing_service.py         # 定价服务
│   ├── events/                        # 领域事件
│   │   ├── __init__.py
│   │   └── order_events.py            # OrderCreated, OrderPaid 等
│   └── exceptions.py                  # 领域异常
│
├── application/                       # 应用层（用例编排）
│   ├── __init__.py
│   ├── commands/                      # 命令（写操作）
│   │   └── create_order.py
│   ├── queries/                       # 查询（读操作）
│   │   └── get_order.py
│   └── services/                      # 应用服务
│       └── order_app_service.py
│
├── infrastructure/                    # 基础设施层（技术实现）
│   ├── __init__.py
│   ├── persistence/                   # 持久化实现
│   │   ├── __init__.py
│   │   ├── sqlalchemy_order_repo.py   # OrderRepository 的 SQLAlchemy 实现
│   │   └── orm_models.py             # ORM 映射
│   ├── messaging/                     # 消息队列实现
│   │   └── event_publisher.py
│   └── external/                      # 外部服务集成
│       └── payment_gateway.py
│
└── api/                               # 接口层（HTTP/gRPC）
    ├── __init__.py
    ├── rest/
    │   └── order_controller.py
    └── schemas/
        └── order_schemas.py
```

## 关键代码示例

### 领域模型（Entity + Value Object）
```python
# domain/models/money.py — 值对象
from dataclasses import dataclass

@dataclass(frozen=True)  # frozen=True 使其不可变
class Money:
    amount: float
    currency: str = "CNY"

    def add(self, other: "Money") -> "Money":
        assert self.currency == other.currency
        return Money(self.amount + other.amount, self.currency)

# domain/models/order.py — 聚合根
from dataclasses import dataclass, field
from .money import Money

@dataclass
class Order:
    id: str
    customer_id: str
    items: list = field(default_factory=list)
    status: str = "PENDING"

    def add_item(self, product_id: str, quantity: int, price: Money):
        """业务逻辑封装在聚合内部"""
        if self.status != "PENDING":
            raise ValueError("只有待处理订单可以添加商品")
        self.items.append({"product_id": product_id, "quantity": quantity, "price": price})

    @property
    def total(self) -> Money:
        return Money(sum(item["price"].amount * item["quantity"] for item in self.items))
```

### 仓储接口（Protocol）
```python
# domain/repositories/order_repository.py
from typing import Protocol
from domain.models.order import Order

class OrderRepository(Protocol):
    """仓储接口 — 对标 Java Repository Interface"""
    def save(self, order: Order) -> None: ...
    def find_by_id(self, order_id: str) -> Order | None: ...
    def find_by_customer(self, customer_id: str) -> list[Order]: ...
```

### 应用服务
```python
# application/services/order_app_service.py
class OrderAppService:
    """应用服务 — 编排用例，不包含业务逻辑"""
    def __init__(self, order_repo: OrderRepository):
        self.order_repo = order_repo

    def create_order(self, customer_id: str, items: list) -> Order:
        order = Order(id=generate_id(), customer_id=customer_id)
        for item in items:
            order.add_item(**item)  # 业务逻辑在领域模型中
        self.order_repo.save(order)
        return order
```

## DDD 分层依赖规则

```
api → application → domain ← infrastructure
                      ↑
              （domain 不依赖任何外层）
```

- **domain 层**：纯 Python，不依赖 FastAPI、SQLAlchemy 等框架
- **application 层**：依赖 domain，编排业务用例
- **infrastructure 层**：实现 domain 定义的接口（Repository 等）
- **api 层**：HTTP 入口，调用 application 层
