# 常用功能 速查卡片

## 核心概念

| 知识点 | 核心模块/库 | 一句话说明 | 难度 |
|--------|------------|-----------|------|
| 正则表达式 | `re` | 文本模式匹配与替换 | 入门 |
| 日期时间 | `datetime` | 日期时间创建、格式化、运算 | 入门 |
| 数据格式 | `json` / `yaml` / `xml` | 数据序列化与反序列化 | 入门 |
| 数据库 | `sqlite3` | SQL 数据库连接、CRUD、事务 | 进阶 |
| HTTP API | `fastapi` / `flask` | REST API 路由、请求处理、响应 | 进阶 |
| 单元测试 | `pytest` | 断言、fixture、参数化、mock | 入门 |
| 日志管理 | `logging` | 日志级别、Handler、Formatter | 入门 |

## 常用语法

### 正则表达式（re）

```python
import re

# 搜索第一个匹配
m = re.search(r"\d+", "价格:100元")       # m.group() -> '100'

# 查找所有匹配
re.findall(r"\d+", "100元和200元")         # ['100', '200']

# 替换
re.sub(r"\d+", "***", "手机号13800001111") # '手机号***'

# 分割
re.split(r"[,;\s]+", "a, b;c d")          # ['a', 'b', 'c', 'd']

# 预编译（多次使用时推荐）
pattern = re.compile(r"[\w.]+@[\w.]+")
pattern.findall(text)

# 分组捕获
m = re.search(r"(\d{4})-(\d{2})-(\d{2})", "2025-07-15")
m.group(1)  # '2025'

# 命名分组
m = re.search(r"(?P<year>\d{4})-(?P<month>\d{2})", "2025-07")
m.group("year")  # '2025'
```

### 日期时间（datetime）

```python
from datetime import datetime, timedelta, timezone

# 当前时间
now = datetime.now()
utc_now = datetime.now(timezone.utc)

# 创建指定时间
dt = datetime(2025, 7, 15, 10, 30, 0)

# 格式化与解析
s = dt.strftime("%Y-%m-%d %H:%M:%S")      # '2025-07-15 10:30:00'
dt = datetime.strptime(s, "%Y-%m-%d %H:%M:%S")

# 时间运算
tomorrow = now + timedelta(days=1)
diff = datetime(2025, 12, 31) - now        # timedelta 对象
diff.days                                   # 天数差

# 时区处理
tz_cn = timezone(timedelta(hours=8))
cn_time = datetime.now(tz_cn)

# 时间戳互转
ts = dt.timestamp()                         # datetime -> 时间戳
dt = datetime.fromtimestamp(ts)             # 时间戳 -> datetime
```

### 数据格式（JSON / YAML / XML）

```python
import json

# JSON 序列化/反序列化
json_str = json.dumps({"name": "张三"}, ensure_ascii=False)
data = json.loads(json_str)

# JSON 文件读写
with open("data.json", "w") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
with open("data.json") as f:
    data = json.load(f)

# YAML（需要 pip install pyyaml）
import yaml
data = yaml.safe_load(yaml_str)            # 解析（始终用 safe_load！）
yaml_str = yaml.dump(data, allow_unicode=True)

# XML
import xml.etree.ElementTree as ET
root = ET.fromstring(xml_str)              # 解析
elem = root.find(".//item")               # XPath 查找
ET.tostring(root, encoding="unicode")      # 生成
```

### 数据库（sqlite3）

```python
import sqlite3

# 连接（:memory: 为内存数据库）
with sqlite3.connect("test.db") as conn:
    cursor = conn.cursor()

    # 建表
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER
        )
    """)

    # 插入（参数化查询，防 SQL 注入）
    cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", ("张三", 25))

    # 批量插入
    cursor.executemany("INSERT INTO users (name, age) VALUES (?, ?)",
                       [("李四", 30), ("王五", 22)])

    # 查询
    cursor.execute("SELECT * FROM users WHERE age > ?", (20,))
    rows = cursor.fetchall()

    # Row Factory（字典式访问）
    conn.row_factory = sqlite3.Row
    cursor.execute("SELECT * FROM users")
    for row in cursor.fetchall():
        print(row["name"])

    conn.commit()
```

### HTTP API（FastAPI / Flask）

```python
# === FastAPI ===
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float

@app.get("/items/{item_id}")
def get_item(item_id: int):
    if item_id not in db:
        raise HTTPException(404, "未找到")
    return db[item_id]

@app.post("/items", status_code=201)
def create_item(item: Item):          # Pydantic 自动验证
    return {"id": 1, **item.model_dump()}

# 运行: uvicorn app:app --reload

# === Flask ===
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/items/<int:item_id>")
def get_item(item_id):
    return jsonify(db.get(item_id))

@app.route("/items", methods=["POST"])
def create_item():
    data = request.get_json()
    return jsonify(data), 201

# 运行: flask run
```

### 单元测试（pytest）

```python
import pytest
from unittest.mock import patch, MagicMock

# 基本断言
def test_add():
    assert 1 + 1 == 2

# 参数化
@pytest.mark.parametrize("input,expected", [
    ("hello", 5), ("", 0), ("你好", 2),
])
def test_length(input, expected):
    assert len(input) == expected

# 异常测试
def test_error():
    with pytest.raises(ZeroDivisionError):
        1 / 0

# Fixture
@pytest.fixture
def sample_data():
    return [1, 2, 3]

def test_sum(sample_data):
    assert sum(sample_data) == 6

# Mock
def test_api():
    with patch("requests.get") as mock_get:
        mock_get.return_value.json.return_value = {"id": 1}
        # ... 测试代码 ...

# 运行: pytest test_file.py -v
```

### 日志管理（logging）

```python
import logging

# 快速配置
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)-8s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# 模块级 Logger（推荐）
logger = logging.getLogger(__name__)

# 日志级别
logger.debug("调试信息")
logger.info("一般信息")
logger.warning("警告")
logger.error("错误")
logger.critical("严重错误")

# 参数化日志（推荐，惰性格式化）
logger.info("用户: %s, 年龄: %d", name, age)

# 异常日志（附带堆栈）
try:
    risky_operation()
except Exception:
    logger.exception("操作失败")

# 文件日志 + 轮转
from logging.handlers import RotatingFileHandler
handler = RotatingFileHandler("app.log", maxBytes=10*1024*1024, backupCount=5)
logger.addHandler(handler)
```


## 常见陷阱

- ⚠️ **正则：忘记原始字符串** — 写正则用 `r"\d+"` 而非 `"\d+"`，避免转义问题
- ⚠️ **正则：混淆 match 和 search** — `match` 只匹配开头，`search` 搜索全文
- ⚠️ **日期：naive vs aware** — `datetime.now()` 不带时区（naive），跨时区场景用 `datetime.now(timezone.utc)`
- ⚠️ **JSON：中文被转义** — `json.dumps()` 加 `ensure_ascii=False` 保留中文
- ⚠️ **JSON：不支持 datetime** — 需要自定义 `JSONEncoder` 或先转为字符串
- ⚠️ **YAML：安全风险** — 始终用 `yaml.safe_load()` 而非 `yaml.load()`
- ⚠️ **数据库：SQL 注入** — 永远用参数化查询 `cursor.execute(sql, (param,))`，不要拼接字符串
- ⚠️ **数据库：忘记 commit** — INSERT/UPDATE/DELETE 后必须 `conn.commit()`
- ⚠️ **数据库：单元素元组** — 参数化查询单参数用 `(value,)` 不是 `(value)`
- ⚠️ **FastAPI：async 中用阻塞操作** — `async def` 中不要用 `time.sleep()`，用 `asyncio.sleep()`
- ⚠️ **Flask：忘记返回 JSON** — 用 `jsonify()` 包装返回值
- ⚠️ **pytest：命名不规范** — 文件和函数必须以 `test_` 开头才能被发现
- ⚠️ **pytest：fixture 作用域** — 默认每个测试函数重新创建，开销大时用 `scope="module"`
- ⚠️ **logging：默认级别是 WARNING** — `logging.info()` 默认不输出，需设置 `level=logging.DEBUG`
- ⚠️ **logging：basicConfig 只生效一次** — 重新配置需加 `force=True`
- ⚠️ **logging：f-string 性能** — 用 `logger.info("msg: %s", val)` 而非 `logger.info(f"msg: {val}")`

## 面试高频考点

- **正则表达式**：贪婪 vs 非贪婪匹配的区别？`findall` 遇到分组时返回什么？
- **日期时间**：naive datetime 和 aware datetime 的区别？如何处理时区转换？
- **JSON**：`json.dumps()` 遇到不可序列化类型怎么办？如何自定义序列化？
- **数据库**：什么是参数化查询？为什么不能用字符串拼接 SQL？什么是事务的 ACID 特性？
- **HTTP API**：FastAPI 和 Flask 的主要区别？RESTful API 设计原则？HTTP 状态码含义？
- **pytest**：fixture 的作用域有哪些？参数化测试怎么写？如何 mock 外部依赖？
- **logging**：日志级别有哪些？Handler 和 Formatter 的关系？如何实现日志轮转？
- **综合**：Python 的 `with` 语句在数据库连接和文件操作中的作用？上下文管理器原理？
