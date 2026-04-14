#!/usr/bin/env python3
"""
SQLAlchemy ORM 完整示例

模块: 04-框架与架构
知识点: ORM 框架 - SQLAlchemy
Python 版本: >= 3.9
最后验证: 2025-07-15

运行方式:
    python sqlalchemy_demo.py

依赖安装:
    pip install sqlalchemy

描述:
    使用 SQLite 内存数据库演示 SQLAlchemy 2.0 核心功能：
    1. 模型定义（Mapped 类型注解风格）
    2. 一对多关联关系
    3. CRUD 操作
    4. 查询构建（过滤、排序、聚合）
    5. 事务管理
    对标 Java Hibernate / JPA
"""

from datetime import datetime
from sqlalchemy import (
    String, Float, ForeignKey, func, create_engine, select,
)
from sqlalchemy.orm import (
    DeclarativeBase, Mapped, mapped_column, relationship,
    Session, sessionmaker,
)


# ============================================================
# 1. 模型定义（对标 Java @Entity）
# ============================================================

class Base(DeclarativeBase):
    """所有模型的基类（对标 Java 的 BaseEntity）"""
    pass


class Author(Base):
    """作者模型"""
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True)

    # 一对多关系（对标 Java @OneToMany）
    books: Mapped[list["Book"]] = relationship(back_populates="author")

    def __repr__(self) -> str:
        return f"Author(id={self.id}, name='{self.name}')"


class Book(Base):
    """图书模型"""
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    price: Mapped[float] = mapped_column(Float, default=0.0)
    published_at: Mapped[str] = mapped_column(
        String(20), default=lambda: datetime.now().strftime("%Y-%m-%d")
    )

    # 外键（对标 Java @ManyToOne）
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"))
    author: Mapped["Author"] = relationship(back_populates="books")

    def __repr__(self) -> str:
        return f"Book(id={self.id}, title='{self.title}', price={self.price})"


# ============================================================
# 2. 数据库初始化
# ============================================================

def init_database():
    """创建内存数据库和表"""
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)


# ============================================================
# 3. CRUD 操作
# ============================================================

def demo_create(session: Session):
    """创建数据（对标 JPA save()）"""
    print("=" * 50)
    print("CREATE — 插入数据")
    print("=" * 50)

    author1 = Author(name="张三", email="zhangsan@example.com")
    author2 = Author(name="李四", email="lisi@example.com")

    session.add_all([author1, author2])
    session.flush()  # 刷新获取 ID（不提交事务）

    books = [
        Book(title="Python 入门", price=49.9, author_id=author1.id),
        Book(title="Python 进阶", price=69.9, author_id=author1.id),
        Book(title="Flask 实战", price=59.0, author_id=author1.id),
        Book(title="Java 编程思想", price=89.0, author_id=author2.id),
        Book(title="Spring Boot 实战", price=79.0, author_id=author2.id),
    ]
    session.add_all(books)
    session.commit()

    print(f"  创建了 {len([author1, author2])} 位作者和 {len(books)} 本书\n")


def demo_read(session: Session):
    """查询数据"""
    print("=" * 50)
    print("READ — 查询数据")
    print("=" * 50)

    # 查询所有作者（对标 JPA findAll()）
    authors = session.execute(select(Author)).scalars().all()
    print(f"  所有作者: {authors}")

    # 条件查询（对标 JPA findByXxx()）
    stmt = select(Book).where(Book.price > 60).order_by(Book.price.desc())
    expensive_books = session.execute(stmt).scalars().all()
    print(f"  价格 > 60 的书: {expensive_books}")

    # 模糊查询（对标 JPA @Query LIKE）
    stmt = select(Book).where(Book.title.contains("Python"))
    python_books = session.execute(stmt).scalars().all()
    print(f"  标题含 'Python': {python_books}")

    # 关联查询 — 通过作者查书
    author = session.execute(
        select(Author).where(Author.name == "张三")
    ).scalar_one()
    print(f"  张三的书: {author.books}")

    # 聚合查询（对标 JPA @Query + GROUP BY）
    stmt = (
        select(Author.name, func.count(Book.id), func.avg(Book.price))
        .join(Book)
        .group_by(Author.name)
    )
    stats = session.execute(stmt).all()
    for name, count, avg_price in stats:
        print(f"  {name}: {count} 本书, 均价 {avg_price:.1f}")

    print()


def demo_update(session: Session):
    """更新数据（对标 JPA save() 更新）"""
    print("=" * 50)
    print("UPDATE — 更新数据")
    print("=" * 50)

    book = session.execute(
        select(Book).where(Book.title == "Python 入门")
    ).scalar_one()

    print(f"  更新前: {book}")
    book.price = 55.0
    book.title = "Python 入门（第2版）"
    session.commit()
    print(f"  更新后: {book}\n")


def demo_delete(session: Session):
    """删除数据（对标 JPA deleteById()）"""
    print("=" * 50)
    print("DELETE — 删除数据")
    print("=" * 50)

    book = session.execute(
        select(Book).where(Book.title.contains("Java"))
    ).scalar_one()

    print(f"  删除: {book}")
    session.delete(book)
    session.commit()

    remaining = session.execute(select(func.count(Book.id))).scalar()
    print(f"  剩余图书数: {remaining}\n")


# ============================================================
# 4. 事务管理
# ============================================================

def demo_transaction(session_factory):
    """事务管理演示（对标 Java @Transactional）"""
    print("=" * 50)
    print("TRANSACTION — 事务管理")
    print("=" * 50)

    # 方式 1: 使用 session 上下文管理器（推荐）
    with session_factory() as session:
        try:
            author = Author(name="王五", email="wangwu@example.com")
            session.add(author)
            session.flush()

            book = Book(title="测试书籍", price=39.9, author_id=author.id)
            session.add(book)

            session.commit()
            print("  事务提交成功")
        except Exception as e:
            session.rollback()
            print(f"  事务回滚: {e}")

    # 方式 2: begin() 自动管理（类似 Java try-with-resources）
    with session_factory.begin() as session:
        count = session.execute(select(func.count(Author.id))).scalar()
        print(f"  当前作者总数: {count}\n")


# ============================================================
# 主函数
# ============================================================

def main():
    """运行所有 SQLAlchemy 演示"""
    print("SQLAlchemy ORM 演示（使用 SQLite 内存数据库）\n")

    session_factory = init_database()

    with session_factory() as session:
        demo_create(session)
        demo_read(session)
        demo_update(session)
        demo_delete(session)

    demo_transaction(session_factory)

    print("=" * 50)
    print("SQLAlchemy vs Java JPA 对照:")
    print("  session.add()     ↔ repository.save()")
    print("  session.query()   ↔ repository.findAll()")
    print("  session.commit()  ↔ @Transactional 自动提交")
    print("  session.rollback()↔ @Transactional 自动回滚")
    print("  relationship()    ↔ @OneToMany / @ManyToOne")
    print("=" * 50)


if __name__ == "__main__":
    main()
