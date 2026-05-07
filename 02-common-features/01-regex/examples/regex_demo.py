#!/usr/bin/env python3
"""
Python 正则表达式完整演示

模块: 02-常用功能
知识点: 正则表达式
Python 版本: >= 3.9
最后验证: 2025-07-15

运行方式:
    python regex_demo.py

描述:
    演示 re 模块的核心功能：
    1. match/search — 单次匹配
    2. findall/finditer — 查找所有匹配
    3. sub — 替换
    4. split — 分割
    5. compile — 预编译
    6. 常用模式匹配（邮箱、手机号、URL 等）
    7. 分组捕获与命名分组
    8. 贪婪 vs 非贪婪匹配
"""

import re


# ============================================================
# 1. match vs search
# ============================================================

def demo_match_search():
    """match 从开头匹配，search 搜索任意位置"""
    print("=" * 10, "match vs search", "=" * 10)

    text = "Hello World 123"

    # re.match() 只从字符串开头匹配
    # 类似 Java: Pattern.matches() 或 Matcher.lookingAt()
    m1 = re.match(r"Hello", text)
    print(f"match 从开头匹配: {m1.group()}" if m1 else "match: 未匹配")

    # re.search() 在整个字符串中搜索第一个匹配
    # 类似 Java: Matcher.find()
    m2 = re.search(r"World", text)
    print(f"search 搜索任意位置: {m2.group()}" if m2 else "search: 未匹配")

    # match 不能匹配非开头的内容
    m3 = re.match(r"World", text)
    assert m3 is None, "match 只从开头匹配"

    print()


# ============================================================
# 2. findall 和 finditer
# ============================================================

def demo_findall_finditer():
    """findall 返回列表，finditer 返回迭代器"""
    print("=" * 10, "findall 和 finditer", "=" * 10)

    text = "价格:100元，运费:200元，折扣:50元"

    # findall：返回所有匹配的字符串列表
    # 类似 Java 中循环调用 matcher.find() 收集结果
    numbers = re.findall(r"\d+", text)
    print(f"findall 所有数字: {numbers}")

    # finditer：返回 Match 对象的迭代器，可获取位置信息
    print("finditer 详细信息:")
    for m in re.finditer(r"\d+", text):
        print(f"  '{m.group()}' 位置: {m.start()}-{m.end()}")

    print()


# ============================================================
# 3. sub 替换
# ============================================================

def demo_sub():
    """sub 替换匹配内容"""
    print("=" * 10, "sub 替换", "=" * 10)

    text = "我的手机号是 13812345678，备用号 13987654321"
    print(f"原文: {text}")

    # 使用函数作为替换参数，实现复杂替换逻辑
    # 类似 Java: Matcher.replaceAll() 但更灵活
    def mask_phone(match):
        """手机号脱敏：保留前3后4"""
        phone = match.group()
        return phone[:3] + "****" + phone[7:]

    masked = re.sub(r"1[3-9]\d{9}", mask_phone, text)
    print(f"脱敏: {masked}")

    print()


# ============================================================
# 4. split 分割
# ============================================================

def demo_split():
    """split 按模式分割字符串"""
    print("=" * 10, "split 分割", "=" * 10)

    text = "apple, banana;cherry  date"

    # 按多种分隔符分割（逗号、分号、空格）
    # 比 str.split() 更强大，支持正则模式
    parts = re.split(r"[,;\s]+", text)
    print(f"分割结果: {parts}")

    print()


# ============================================================
# 5. compile 预编译
# ============================================================

def demo_compile():
    """compile 预编译正则表达式，提升重复使用时的性能"""
    print("=" * 10, "compile 预编译", "=" * 10)

    # 预编译：适合需要多次使用同一正则的场景
    # 类似 Java: Pattern pattern = Pattern.compile("...");
    email_pattern = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")

    texts = [
        "联系我: alice@example.com",
        "发送到 bob.test@gmail.com 即可",
        "无邮箱的文本",
    ]

    for text in texts:
        m = email_pattern.search(text)
        if m:
            print(f"找到邮箱: {m.group()}")

    print()


# ============================================================
# 6. 常用模式匹配
# ============================================================

def demo_common_patterns():
    """常用正则模式：邮箱、手机号、URL"""
    print("=" * 10, "常用模式匹配", "=" * 10)

    # --- 邮箱验证 ---
    print("--- 邮箱验证 ---")
    email_re = re.compile(r"^[\w.+-]+@[\w-]+\.[\w.-]+$")
    test_emails = ["alice@example.com", "invalid@.com", "test@co", "a@b.cc"]
    for email in test_emails:
        valid = "有效" if email_re.match(email) else "无效"
        print(f"  {email} -> {valid}")

    # --- 手机号验证 ---
    print("--- 手机号验证 ---")
    phone_re = re.compile(r"^1[3-9]\d{9}$")
    test_phones = ["13812345678", "12345678901", "1381234567", "13812345678a"]
    for phone in test_phones:
        valid = "有效" if phone_re.match(phone) else "无效"
        print(f"  {phone} -> {valid}")

    # --- URL 提取 ---
    print("--- URL 提取 ---")
    url_re = re.compile(r"https?://[^\s<>\"']+")
    text = "访问 https://www.python.org 或 http://example.com/path 了解更多"
    for url in url_re.findall(text):
        print(f"  {url}")

    print()


# ============================================================
# 7. 分组捕获
# ============================================================

def demo_groups():
    """分组捕获与命名分组"""
    print("=" * 10, "分组捕获", "=" * 10)

    date_text = "今天是 2025-07-15，明天是 2025-07-16"

    # --- 基本分组 ---
    print("--- 基本分组 ---")
    # 用 () 创建捕获分组，group(1) 获取第一个分组
    m = re.search(r"(\d{4})-(\d{2})-(\d{2})", date_text)
    if m:
        print(f"日期: {m.group()}, 年={m.group(1)}, 月={m.group(2)}, 日={m.group(3)}")

    # --- 命名分组 ---
    print("--- 命名分组 ---")
    # Python 使用 (?P<name>...) 语法（Java 使用 (?<name>...)）
    m = re.search(r"(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})", date_text)
    if m:
        print(f"年={m.group('year')}, 月={m.group('month')}, 日={m.group('day')}")

    print()


# ============================================================
# 8. 贪婪 vs 非贪婪
# ============================================================

def demo_greedy():
    """贪婪匹配 vs 非贪婪匹配"""
    print("=" * 10, "贪婪 vs 非贪婪", "=" * 10)

    html = "<b>bold</b> and <i>italic</i>"

    # 贪婪匹配（默认）：尽可能多地匹配
    greedy = re.findall(r"<.*>", html)
    print(f"贪婪匹配: {greedy}")

    # 非贪婪匹配：加 ? 后缀，尽可能少地匹配
    non_greedy = re.findall(r"<.*?>", html)
    print(f"非贪婪匹配: {non_greedy}")

    print()


# ============================================================
# 主函数
# ============================================================

def main():
    """主函数：依次演示所有正则表达式知识点"""
    demo_match_search()
    demo_findall_finditer()
    demo_sub()
    demo_split()
    demo_compile()
    demo_common_patterns()
    demo_groups()
    demo_greedy()


if __name__ == "__main__":
    main()
