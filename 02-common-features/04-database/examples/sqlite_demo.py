#!/usr/bin/env python3
"""
SQLite 数据库操作完整演示

模块: 02-常用功能
知识点: 数据库操作
Python 版本: >= 3.9
最后验证: 2025-07-15

运行方式:
    python sqlite_demo.py

描述:
    演示 SQLite 数据库的完整操作流程：
    1. 连接数据库（使用内存数据库 :memory:）
    2. 建表
    3. CRUD 操作（增删改查）
    4. 参数化查询（防 SQL 注入）
    5. 事务处理（commit/rollback）
    6. 错误处理
    7. Row Factory（字典式访问）
"""

import sqlite3


# ============================================================
# 1. 建表与插入
# ============================================================

def demo_create_and_insert(conn: sqlite3.Connection):
    """建表并插入数据"""
    print("=" * 10, "建表与插入", "=" * 10)

    cursor = conn.cursor()

    # 建表（IF NOT EXISTS 避免重复创建）
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            email TEXT UNIQUE
        )
    """)

    # 插入单条数据 — 使用参数化查询（? 占位符）
    # 类似 Java JDBC 的 PreparedStatement
    cursor.execute(
        "INSERT INTO users (name, age, email) VALUES (?, ?, ?)",
        ("张三", 28, "zhangsan@example.com")
    )

    # 批量插入
    users = [
        ("李四", 35, "lisi@example.com"),
        ("王五", 22, "wangwu@example.com"),
    ]
    cursor.executemany(
        "INSERT INTO users (name, age, email) VALUES (?, ?, ?)",
        users
    )

    conn.commit()
    print(f"插入成功，最后插入的 ID: {cursor.lastrowid}")

    # 查询所有数据
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    print("所有用户:")
    for row in rows:
        print(f"  {row}")

    print()


# ============================================================
# 2. 参数化查询
# ============================================================

def demo_parameterized_query(conn: sqlite3.Connection):
    """参数化查询 — 防止 SQL 注入的关键"""
    print("=" * 10, "参数化查询", "=" * 10)

    cursor = conn.cursor()

    # 条件查询：查找年龄大于指定值的用户
    min_age = 25
    cursor.execute("SELECT name, age FROM users WHERE age > ?", (min_age,))
    print(f"年龄大于 {min_age} 的用户:")
    for name, age in cursor.fetchall():
        print(f"  {name} ({age}岁)")

    # 精确查询：按邮箱查找
    cursor.execute(
        "SELECT name, age FROM users WHERE email = ?",
        ("lisi@example.com",)
    )
    result = cursor.fetchone()
    print(f"按邮箱查找: {result}")

    print()


# ============================================================
# 3. 更新与删除
# ============================================================

def demo_update_delete(conn: sqlite3.Connection):
    """更新和删除操作"""
    print("=" * 10, "更新与删除", "=" * 10)

    cursor = conn.cursor()

    # 更新：修改张三的年龄和邮箱
    cursor.execute(
        "UPDATE users SET age = ?, email = ? WHERE name = ?",
        (30, "zhangsan_new@example.com", "张三")
    )
    conn.commit()

    cursor.execute("SELECT name, age, email FROM users WHERE name = ?", ("张三",))
    print(f"更新后: {cursor.fetchone()}")

    # 删除：删除王五
    cursor.execute("DELETE FROM users WHERE name = ?", ("王五",))
    conn.commit()

    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]
    print(f"删除后剩余用户数: {count}")

    print()


# ============================================================
# 4. 批量插入
# ============================================================

def demo_batch_insert(conn: sqlite3.Connection):
    """批量插入数据"""
    print("=" * 10, "批量插入", "=" * 10)

    cursor = conn.cursor()

    new_users = [
        ("赵六", 29, "zhaoliu@example.com"),
        ("孙七", 31, "sunqi@example.com"),
        ("王五", 22, "wangwu@example.com"),
    ]

    cursor.executemany(
        "INSERT INTO users (name, age, email) VALUES (?, ?, ?)",
        new_users
    )
    conn.commit()

    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]
    print(f"批量插入后总用户数: {count}")

    print()


# ============================================================
# 5. 事务处理
# ============================================================

def demo_transaction(conn: sqlite3.Connection):
    """事务处理：commit 和 rollback"""
    print("=" * 10, "事务处理", "=" * 10)

    cursor = conn.cursor()

    # 获取当前用户数
    cursor.execute("SELECT COUNT(*) FROM users")
    before_count = cursor.fetchone()[0]

    try:
        # 开始一组操作
        cursor.execute(
            "INSERT INTO users (name, age, email) VALUES (?, ?, ?)",
            ("临时用户", 20, "temp@example.com")
        )
        # 模拟错误：插入重复邮箱
        cursor.execute(
            "INSERT INTO users (name, age, email) VALUES (?, ?, ?)",
            ("另一个用户", 25, "temp@example.com")  # 邮箱重复！
        )
        conn.commit()
    except sqlite3.IntegrityError:
        # 发生错误，回滚整个事务
        conn.rollback()

    cursor.execute("SELECT COUNT(*) FROM users")
    after_count = cursor.fetchone()[0]
    print(f"事务回滚成功，用户数未变: {after_count}")

    print()


# ============================================================
# 6. 聚合查询
# ============================================================

def demo_aggregate(conn: sqlite3.Connection):
    """聚合查询：COUNT/AVG/MAX/MIN"""
    print("=" * 10, "聚合查询", "=" * 10)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*) as total,
               ROUND(AVG(age), 2) as avg_age,
               MAX(age) as max_age,
               MIN(age) as min_age
        FROM users
    """)
    total, avg_age, max_age, min_age = cursor.fetchone()
    print(f"用户统计: 总数={total}, 平均年龄={avg_age}, "
          f"最大年龄={max_age}, 最小年龄={min_age}")

    print()


# ============================================================
# 7. Row Factory — 字典式访问
# ============================================================

def demo_row_factory(conn: sqlite3.Connection):
    """使用 Row Factory 实现字典式访问"""
    print("=" * 10, "Row Factory", "=" * 10)

    # 设置 row_factory 为 sqlite3.Row，支持按列名访问
    # 类似 Java ResultSet 的 getString("column_name")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT name, email FROM users WHERE age > ?", (25,))
    print("使用 Row 对象访问:")
    for row in cursor.fetchall():
        print(f"  name={row['name']}, email={row['email']}")

    # 恢复默认
    conn.row_factory = None

    print()


# ============================================================
# 主函数
# ============================================================

def main():
    """主函数：使用内存数据库演示所有操作"""
    # 使用 :memory: 内存数据库，无需文件，程序结束后自动销毁
    with sqlite3.connect(":memory:") as conn:
        demo_create_and_insert(conn)
        demo_parameterized_query(conn)
        demo_update_delete(conn)
        demo_batch_insert(conn)
        demo_transaction(conn)
        demo_aggregate(conn)
        demo_row_factory(conn)


if __name__ == "__main__":
    main()
