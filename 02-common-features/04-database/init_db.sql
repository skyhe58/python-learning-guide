-- ============================================================
-- 数据库初始化脚本
-- 适用于: SQLite / MySQL / PostgreSQL
-- 描述: 创建示例表结构并插入测试数据
-- ============================================================

-- 用户表
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,  -- MySQL 使用 AUTO_INCREMENT
    name TEXT NOT NULL,
    age INTEGER NOT NULL CHECK (age > 0 AND age < 150),
    email TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 订单表
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    product TEXT NOT NULL,
    amount REAL NOT NULL CHECK (amount > 0),
    status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'paid', 'shipped', 'completed', 'cancelled')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- ============================================================
-- 插入示例数据
-- ============================================================

-- 用户数据
INSERT INTO users (name, age, email) VALUES ('张三', 28, 'zhangsan@example.com');
INSERT INTO users (name, age, email) VALUES ('李四', 35, 'lisi@example.com');
INSERT INTO users (name, age, email) VALUES ('王五', 22, 'wangwu@example.com');
INSERT INTO users (name, age, email) VALUES ('赵六', 29, 'zhaoliu@example.com');
INSERT INTO users (name, age, email) VALUES ('孙七', 31, 'sunqi@example.com');

-- 订单数据
INSERT INTO orders (user_id, product, amount, status) VALUES (1, 'Python 编程书', 59.90, 'completed');
INSERT INTO orders (user_id, product, amount, status) VALUES (1, '机械键盘', 299.00, 'shipped');
INSERT INTO orders (user_id, product, amount, status) VALUES (2, '显示器', 1599.00, 'paid');
INSERT INTO orders (user_id, product, amount, status) VALUES (3, '鼠标', 89.00, 'pending');
INSERT INTO orders (user_id, product, amount, status) VALUES (4, '耳机', 199.00, 'completed');

-- ============================================================
-- 常用查询示例（供参考）
-- ============================================================

-- 查询所有用户
-- SELECT * FROM users ORDER BY id;

-- 查询用户及其订单数
-- SELECT u.name, COUNT(o.id) as order_count
-- FROM users u LEFT JOIN orders o ON u.id = o.user_id
-- GROUP BY u.id, u.name;

-- 查询每个用户的总消费金额
-- SELECT u.name, COALESCE(SUM(o.amount), 0) as total_spent
-- FROM users u LEFT JOIN orders o ON u.id = o.user_id
-- GROUP BY u.id, u.name
-- ORDER BY total_spent DESC;

-- 查询已完成订单的用户
-- SELECT DISTINCT u.name, u.email
-- FROM users u JOIN orders o ON u.id = o.user_id
-- WHERE o.status = 'completed';
