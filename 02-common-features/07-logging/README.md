# 日志管理（logging）

> **模块：** 02-常用功能
> **难度：** 入门
> **前置知识：** Python 基础（01-python-basics）
> **Python 版本：** >= 3.9
> **最后验证日期：** 2025-07-15

## 概念说明

日志管理是生产环境中不可或缺的技能。Python 标准库的 `logging` 模块提供了灵活而强大的日志系统，支持多级别日志、多输出目标、自定义格式和日志轮转。对于 Java 开发者来说，Python 的 `logging` 模块类似于 SLF4J + Logback 的组合，但配置更简单——不需要 XML 配置文件，几行代码即可完成。

`logging` 模块的核心组件包括：**Logger（记录器）** 负责产生日志、**Handler（处理器）** 负责输出日志到目标（控制台、文件等）、**Formatter（格式器）** 负责定义日志格式、**Filter（过滤器）** 负责过滤日志。这四个组件的协作方式与 Java 的 Logback 几乎一致。

日志级别从低到高：`DEBUG` < `INFO` < `WARNING` < `ERROR` < `CRITICAL`。默认级别是 `WARNING`，即只有 WARNING 及以上级别的日志才会输出——这是新手最常遇到的"日志不显示"问题。

### 日志级别说明

| 级别 | 数值 | 用途 | 示例 |
|------|------|------|------|
| `DEBUG` | 10 | 调试信息，开发时使用 | 变量值、函数调用跟踪 |
| `INFO` | 20 | 一般信息，确认程序正常运行 | 服务启动、请求处理 |
| `WARNING` | 30 | 警告信息，潜在问题 | 配置缺失、性能下降 |
| `ERROR` | 40 | 错误信息，功能受影响 | 请求失败、数据库连接断开 |
| `CRITICAL` | 50 | 严重错误，程序可能崩溃 | 系统资源耗尽、核心服务不可用 |

### 核心组件

| 组件 | 说明 | Java 对应 |
|------|------|-----------|
| Logger | 日志记录器，按名称层级组织 | `LoggerFactory.getLogger()` |
| Handler | 日志输出目标（控制台/文件/网络） | Appender（ConsoleAppender 等） |
| Formatter | 日志格式定义 | Layout / Pattern |
| Filter | 日志过滤规则 | Filter |


## Java 对比

| 特性 | Java (SLF4J + Logback) | Python (logging) |
|------|------------------------|------------------|
| 获取 Logger | `LoggerFactory.getLogger(MyClass.class)` | `logging.getLogger(__name__)` |
| 日志级别 | TRACE/DEBUG/INFO/WARN/ERROR | DEBUG/INFO/WARNING/ERROR/CRITICAL |
| 配置方式 | `logback.xml` | `basicConfig()` 或 `dictConfig()` |
| 格式化 | `%d{HH:mm:ss} %-5level %msg%n` | `%(asctime)s %(levelname)s %(message)s` |
| 文件输出 | `FileAppender` | `FileHandler` |
| 日志轮转 | `RollingFileAppender` | `RotatingFileHandler` |
| 参数化日志 | `log.info("User: {}", name)` | `log.info("User: %s", name)` |

**Java 写法（SLF4J + Logback）：**
```java
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class MyService {
    // 需要 logback.xml 配置文件
    private static final Logger log = LoggerFactory.getLogger(MyService.class);

    public void process(String name) {
        log.info("Processing user: {}", name);
        try {
            // ... 业务逻辑 ...
        } catch (Exception e) {
            log.error("Failed to process: {}", name, e);
        }
    }
}
```

**Python 写法：**
```python
import logging

# 无需配置文件，几行代码搞定
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

def process(name: str):
    logger.info("Processing user: %s", name)
    try:
        # ... 业务逻辑 ...
        pass
    except Exception as e:
        logger.error("Failed to process: %s", name, exc_info=True)
```

## 实战代码

### 示例：logging 完整演示

**文件：** `examples/logging_demo.py`

演示 logging 模块的核心功能：基本配置、日志级别、文件日志、自定义格式、多 Handler、日志轮转。

**运行方式：**
```bash
python examples/logging_demo.py
```

**预期输出：**
```
========== 基本日志配置 ==========
2025-07-15 10:00:00 DEBUG 这是 DEBUG 级别日志
2025-07-15 10:00:00 INFO 这是 INFO 级别日志
2025-07-15 10:00:00 WARNING 这是 WARNING 级别日志
2025-07-15 10:00:00 ERROR 这是 ERROR 级别日志
2025-07-15 10:00:00 CRITICAL 这是 CRITICAL 级别日志

========== 参数化日志 ==========
处理用户: 张三, 年龄: 25

========== 异常日志 ==========
发生错误: division by zero
（包含完整堆栈跟踪）

========== 多 Handler 配置 ==========
控制台和文件同时输出日志

========== 日志轮转 ==========
日志文件超过指定大小后自动轮转
```

## 常见陷阱

### 1. 默认级别是 WARNING

新手最常遇到的问题：`logging.info()` 没有输出！因为默认级别是 WARNING。

```python
import logging

# ✗ 不会输出！默认级别是 WARNING
logging.info("这条日志不会显示")

# ✓ 设置级别为 DEBUG 或 INFO
logging.basicConfig(level=logging.DEBUG)
logging.info("现在可以显示了")
```

### 2. basicConfig 只能调用一次

`basicConfig()` 只在第一次调用时生效，后续调用会被忽略。

```python
import logging

# 第一次调用生效
logging.basicConfig(level=logging.DEBUG)

# ✗ 第二次调用无效！级别不会变成 WARNING
logging.basicConfig(level=logging.WARNING)

# ✓ 如果需要重新配置，使用 force=True（Python 3.8+）
logging.basicConfig(level=logging.WARNING, force=True)
```

### 3. 字符串格式化的性能问题

日志消息应使用 `%s` 占位符而非 f-string，避免不必要的字符串格式化。

```python
import logging
logger = logging.getLogger(__name__)

# ✗ 不推荐：即使日志级别不够，f-string 也会执行格式化
logger.debug(f"处理数据: {expensive_function()}")

# ✓ 推荐：使用 % 占位符，只在需要输出时才格式化
logger.debug("处理数据: %s", expensive_function())
```

### 4. 根 Logger 与模块 Logger 混用

```python
import logging

# ✗ 直接使用 logging.info() 是根 Logger
logging.info("根 Logger")

# ✓ 推荐：使用模块级 Logger，便于控制和过滤
logger = logging.getLogger(__name__)
logger.info("模块 Logger")
```

> 💻 **完整可运行代码：** [logging_demo.py](examples/logging_demo.py)

## 参考资料

- [Python 官方文档 - logging](https://docs.python.org/zh-cn/3/library/logging.html)
- [Python 官方文档 - logging HOWTO](https://docs.python.org/zh-cn/3/howto/logging.html)
- [Python 官方文档 - logging.handlers](https://docs.python.org/zh-cn/3/library/logging.handlers.html)
- [Real Python - Logging in Python](https://realpython.com/python-logging/)
