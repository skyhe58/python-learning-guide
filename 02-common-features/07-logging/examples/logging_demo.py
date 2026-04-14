#!/usr/bin/env python3
"""
Python logging 模块完整演示

模块: 02-常用功能
知识点: 日志管理
Python 版本: >= 3.9
最后验证: 2025-07-15

运行方式:
    python logging_demo.py

描述:
    演示 logging 模块的核心功能：
    1. 基本日志配置（basicConfig）
    2. 日志级别（DEBUG/INFO/WARNING/ERROR/CRITICAL）
    3. 参数化日志消息
    4. 异常日志（exc_info）
    5. 自定义格式（Formatter）
    6. 多 Handler（控制台 + 文件）
    7. 日志轮转（RotatingFileHandler）
    8. 自定义 Filter
"""

import logging
import logging.handlers
import os
import tempfile


# ============================================================
# 1. 基本日志配置
# ============================================================

def demo_basic_config():
    """基本日志配置 — 最简单的入门方式"""
    print("=" * 10, "基本日志配置", "=" * 10)

    # basicConfig 配置根 Logger
    # force=True 允许重新配置（Python 3.8+）
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)-8s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        force=True,
    )

    # 五个日志级别，从低到高
    logging.debug("这是 DEBUG 级别日志")
    logging.info("这是 INFO 级别日志")
    logging.warning("这是 WARNING 级别日志")
    logging.error("这是 ERROR 级别日志")
    logging.critical("这是 CRITICAL 级别日志")

    print()


# ============================================================
# 2. 模块级 Logger（推荐方式）
# ============================================================

def demo_module_logger():
    """使用模块级 Logger — 生产环境推荐"""
    print("=" * 10, "模块级 Logger", "=" * 10)

    # 使用 __name__ 创建模块级 Logger
    # 类似 Java: LoggerFactory.getLogger(MyClass.class)
    logger = logging.getLogger("my_module")
    logger.setLevel(logging.DEBUG)

    # 如果没有 handler，添加一个控制台 handler
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(
            "%(name)s - %(levelname)s - %(message)s"
        ))
        logger.addHandler(handler)

    logger.info("这是模块级 Logger 的日志")
    logger.debug("模块名: %s", logger.name)

    # 清理 handler，避免影响后续演示
    logger.handlers.clear()

    print()


# ============================================================
# 3. 参数化日志
# ============================================================

def demo_parameterized_logging():
    """参数化日志 — 避免不必要的字符串格式化"""
    print("=" * 10, "参数化日志", "=" * 10)

    logger = logging.getLogger("param_demo")
    logger.setLevel(logging.DEBUG)
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("%(levelname)s - %(message)s"))
        logger.addHandler(handler)

    name = "张三"
    age = 25

    # ✓ 推荐：使用 % 占位符（惰性格式化）
    logger.info("处理用户: %s, 年龄: %d", name, age)

    # 也支持字典格式
    logger.info("用户信息: %(name)s (%(age)d岁)", {"name": name, "age": age})

    logger.handlers.clear()
    print()


# ============================================================
# 4. 异常日志
# ============================================================

def demo_exception_logging():
    """异常日志 — 记录完整的堆栈跟踪"""
    print("=" * 10, "异常日志", "=" * 10)

    logger = logging.getLogger("exception_demo")
    logger.setLevel(logging.DEBUG)
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(
            "%(levelname)s - %(message)s"
        ))
        logger.addHandler(handler)

    try:
        result = 1 / 0
    except ZeroDivisionError:
        # exc_info=True 会附加完整的堆栈跟踪
        logger.error("计算出错", exc_info=True)

    # 或者使用 logger.exception()（等价于 error + exc_info=True）
    try:
        int("abc")
    except ValueError:
        logger.exception("类型转换失败")

    logger.handlers.clear()
    print()


# ============================================================
# 5. 自定义 Formatter
# ============================================================

def demo_custom_formatter():
    """自定义日志格式"""
    print("=" * 10, "自定义格式", "=" * 10)

    logger = logging.getLogger("format_demo")
    logger.setLevel(logging.DEBUG)

    # 详细格式：包含时间、级别、模块、行号
    detailed_formatter = logging.Formatter(
        fmt="[%(asctime)s] %(levelname)-8s %(name)s:%(lineno)d - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    handler = logging.StreamHandler()
    handler.setFormatter(detailed_formatter)
    logger.addHandler(handler)

    logger.info("使用详细格式的日志")
    logger.warning("包含模块名和行号")

    logger.handlers.clear()
    print()


# ============================================================
# 6. 多 Handler（控制台 + 文件）
# ============================================================

def demo_multi_handler():
    """多 Handler — 同时输出到控制台和文件"""
    print("=" * 10, "多 Handler 配置", "=" * 10)

    logger = logging.getLogger("multi_handler")
    logger.setLevel(logging.DEBUG)

    # Handler 1：控制台（只输出 INFO 及以上）
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter(
        "%(levelname)s - %(message)s"
    ))

    # Handler 2：文件（输出所有级别）
    log_dir = tempfile.mkdtemp()
    log_file = os.path.join(log_dir, "app.log")
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(
        "[%(asctime)s] %(levelname)-8s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    ))

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    # DEBUG 只写入文件，不显示在控制台
    logger.debug("这条只在文件中")
    logger.info("这条在控制台和文件中都有")
    logger.error("错误日志，两处都有")

    # 读取文件内容验证
    file_handler.close()
    with open(log_file, encoding="utf-8") as f:
        print(f"\n文件日志内容 ({log_file}):")
        print(f.read())

    logger.handlers.clear()

    # 清理临时文件
    os.remove(log_file)
    os.rmdir(log_dir)

    print()


# ============================================================
# 7. 日志轮转
# ============================================================

def demo_rotating_log():
    """日志轮转 — 文件超过指定大小后自动切换"""
    print("=" * 10, "日志轮转", "=" * 10)

    logger = logging.getLogger("rotating_demo")
    logger.setLevel(logging.DEBUG)

    log_dir = tempfile.mkdtemp()
    log_file = os.path.join(log_dir, "rotating.log")

    # RotatingFileHandler：按文件大小轮转
    # maxBytes=1024 表示每个文件最大 1KB
    # backupCount=3 表示最多保留 3 个备份文件
    rotating_handler = logging.handlers.RotatingFileHandler(
        log_file,
        maxBytes=1024,
        backupCount=3,
        encoding="utf-8",
    )
    rotating_handler.setFormatter(logging.Formatter(
        "%(asctime)s %(levelname)s %(message)s"
    ))
    logger.addHandler(rotating_handler)

    # 写入足够多的日志触发轮转
    for i in range(50):
        logger.info("日志消息 #%d: 这是一条测试日志，用于演示日志轮转功能", i)

    rotating_handler.close()

    # 查看生成的日志文件
    log_files = [f for f in os.listdir(log_dir) if f.startswith("rotating")]
    print(f"生成的日志文件: {sorted(log_files)}")
    print(f"说明: rotating.log 是当前文件，.1/.2/.3 是历史备份")

    logger.handlers.clear()

    # 清理临时文件
    for f in log_files:
        os.remove(os.path.join(log_dir, f))
    os.rmdir(log_dir)

    print()


# ============================================================
# 8. 自定义 Filter
# ============================================================

def demo_custom_filter():
    """自定义 Filter — 按条件过滤日志"""
    print("=" * 10, "自定义 Filter", "=" * 10)

    class SensitiveFilter(logging.Filter):
        """过滤包含敏感信息的日志"""
        SENSITIVE_WORDS = ["password", "密码", "token", "secret"]

        def filter(self, record: logging.LogRecord) -> bool:
            message = record.getMessage().lower()
            for word in self.SENSITIVE_WORDS:
                if word in message:
                    # 替换敏感信息
                    record.msg = "[已过滤敏感信息]"
                    record.args = ()
                    return True
            return True

    logger = logging.getLogger("filter_demo")
    logger.setLevel(logging.DEBUG)

    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(levelname)s - %(message)s"))
    handler.addFilter(SensitiveFilter())
    logger.addHandler(handler)

    logger.info("用户登录成功: 张三")
    logger.info("用户密码: 123456")  # 会被过滤
    logger.info("API Token: abc123")  # 会被过滤
    logger.info("正常的业务日志")

    logger.handlers.clear()
    print()


# ============================================================
# 主函数
# ============================================================

def main():
    """主函数：依次演示所有日志管理知识点"""
    demo_basic_config()
    demo_module_logger()
    demo_parameterized_logging()
    demo_exception_logging()
    demo_custom_formatter()
    demo_multi_handler()
    demo_rotating_log()
    demo_custom_filter()


if __name__ == "__main__":
    main()
