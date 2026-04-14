# ORM 框架：SQLAlchemy / Django ORM / Tortoise ORM

> **模块：** 04-框架与架构
> **难度：** 进阶
> **前置知识：** Python 基础、数据库基础（SQL）
> **Python 版本：** >= 3.9
> **最后验证日期：** 2025-07-15

## 概念说明

ORM（Object-Relational Mapping）将数据库表映射为 Python 对象，避免手写 SQL。Python 生态三大 ORM：

- **SQLAlchemy** — Python 最强大的 ORM，支持 Core（SQL 表达式）和 ORM 两种模式。对标 Java MyBatis + Hibernate。
- **Django ORM** — Django 内置 ORM，与 Django 深度集成，API 简洁。对标 Java Spring Data JPA。
- **Tortoise ORM** — 异步 ORM，专为 asyncio 设计，适合 FastAPI。对标 Java R2DBC。

## Java 对比

| 特性 | SQLAlchemy | Django ORM | Tortoise ORM | MyBatis | Hibernate/JPA |
|------|-----------|------------|-------------|---------|---------------|
| **模式** | Active Record + Data Mapper | Active Record | Active Record | Data Mapper | Active Record |
| **SQL 控制** | 高（Core 层可写原生 SQL） | 中（支持 raw SQL） | 中 | 高（手写 SQL） | 低（自动生成） |
| **异步支持** | SQLAlchemy 2.0+ | Django 4.1+ 部分 | 原生异步 | 无 | 无 |
| **迁移工具** | Alembic | 内置 migrations | Aerich | Flyway | Hibernate DDL |
| **学习曲线** | 中高 | 低 | 低 | 中 | 中 |
| **独立使用** | ✅ 可独立使用 | ❌ 依赖 Django | ✅ 可独立使用 | ✅ | ✅ |

**Java JPA 写法：**
```java
@Entity
@Table(name = "users")
public class User {
    @Id @GeneratedValue
    private Long id;

    @Column(nullable = false, length = 50)
    private String name;

    @Column(unique = true)
    private String email;
}

// 查询
List<User> users = userRepository.findByNameContaining("张");
```

**Python SQLAlchemy 写法：**
```python
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True)

# 查询
users = session.query(User).filter(User.name.contains("张")).all()
```

## 实战代码

### 示例 1：SQLAlchemy 完整 CRUD

**文件：** `examples/sqlalchemy_demo.py`

使用 SQLite 内存数据库演示模型定义、CRUD 操作、关联查询。

**运行方式：**
```bash
pip install sqlalchemy
python examples/sqlalchemy_demo.py
```

## N+1 查询问题

ORM 最常见的性能陷阱。当遍历父对象并访问子对象时，会产生 N+1 次查询：

```python
# ❌ N+1 问题：1 次查询用户 + N 次查询订单
users = session.query(User).all()
for user in users:
    print(user.orders)  # 每次访问触发一次 SQL 查询

# ✅ 使用 joinedload 预加载（对标 JPA @EntityGraph）
from sqlalchemy.orm import joinedload
users = session.query(User).options(joinedload(User.orders)).all()
```

## 常见陷阱

- ⚠️ 忘记 `session.commit()` 导致数据未持久化（类似 Java 忘记 `@Transactional`）
- ⚠️ N+1 查询问题：遍历关联对象时产生大量 SQL，需使用 `joinedload` / `selectinload`
- ⚠️ SQLAlchemy 2.0 语法与 1.x 差异较大，注意版本
- ⚠️ Django ORM 的 `QuerySet` 是惰性求值的，只有在迭代时才执行 SQL

> 💻 **完整可运行代码：** [sqlalchemy_demo.py](examples/sqlalchemy_demo.py)

## 参考资料

- [SQLAlchemy 官方文档](https://docs.sqlalchemy.org/)
- [Django ORM 文档](https://docs.djangoproject.com/en/4.2/topics/db/)
- [Tortoise ORM 文档](https://tortoise.github.io/)
