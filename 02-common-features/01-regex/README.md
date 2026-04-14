# 正则表达式

> **模块：** 02-常用功能
> **难度：** 入门
> **前置知识：** Python 基础（01-python-basics）
> **Python 版本：** >= 3.9
> **最后验证日期：** 2025-07-15

## 概念说明

正则表达式（Regular Expression，简称 regex）是一种强大的文本模式匹配工具，Python 通过标准库 `re` 模块提供完整的正则表达式支持。对于 Java 开发者来说，Python 的正则表达式语法与 Java 基本一致（都基于 Perl 风格），但使用方式更加简洁——不需要创建 `Pattern` 和 `Matcher` 对象，一个函数调用即可完成匹配。

Python 正则表达式的核心函数包括：`re.match()`（从字符串开头匹配）、`re.search()`（在字符串中搜索第一个匹配）、`re.findall()`（查找所有匹配）、`re.sub()`（替换匹配内容）。对于需要多次使用的正则表达式，可以用 `re.compile()` 预编译以提升性能。

Python 的原始字符串（raw string，`r"..."`）是编写正则表达式的最佳实践，它避免了反斜杠的双重转义问题——这是 Java 开发者在 Python 中写正则时最需要注意的差异。

### re 模块核心函数

| 函数 | 说明 | 返回值 |
|------|------|--------|
| `re.match(pattern, string)` | 从字符串**开头**匹配 | `Match` 对象或 `None` |
| `re.search(pattern, string)` | 搜索字符串中**第一个**匹配 | `Match` 对象或 `None` |
| `re.findall(pattern, string)` | 查找**所有**匹配 | 字符串列表 |
| `re.finditer(pattern, string)` | 查找所有匹配，返回迭代器 | `Match` 对象迭代器 |
| `re.sub(pattern, repl, string)` | 替换匹配内容 | 替换后的字符串 |
| `re.split(pattern, string)` | 按模式分割字符串 | 字符串列表 |
| `re.compile(pattern)` | 预编译正则表达式 | `Pattern` 对象 |

### 常用正则模式速查表

| 模式 | 说明 | 示例 |
|------|------|------|
| `.` | 匹配任意字符（除换行符） | `a.c` → `abc`, `a1c` |
| `\d` | 匹配数字 `[0-9]` | `\d+` → `123` |
| `\w` | 匹配字母/数字/下划线 `[a-zA-Z0-9_]` | `\w+` → `hello_1` |
| `\s` | 匹配空白字符 | `a\sb` → `a b` |
| `^` | 匹配字符串开头 | `^Hello` |
| `$` | 匹配字符串结尾 | `world$` |
| `*` | 重复 0 次或多次 | `ab*c` → `ac`, `abbc` |
| `+` | 重复 1 次或多次 | `ab+c` → `abc`, `abbc` |
| `?` | 重复 0 次或 1 次 | `ab?c` → `ac`, `abc` |
| `{n,m}` | 重复 n 到 m 次 | `a{2,4}` → `aa`, `aaa` |
| `[abc]` | 字符集合 | `[aeiou]` 匹配元音 |
| `[^abc]` | 排除字符集合 | `[^0-9]` 匹配非数字 |
| `(...)` | 分组捕获 | `(\d+)-(\d+)` |
| `(?:...)` | 非捕获分组 | `(?:ab)+` |
| `(?P<name>...)` | 命名分组 | `(?P<year>\d{4})` |
| `\|` | 或运算 | `cat\|dog` |
| `*?`, `+?` | 非贪婪匹配 | `<.*?>` 最短匹配 |

### 常用实战正则表达式

| 用途 | 正则表达式 | 说明 |
|------|-----------|------|
| 邮箱地址 | `r'[\w.+-]+@[\w-]+\.[\w.-]+'` | 基础邮箱匹配 |
| 中国手机号 | `r'1[3-9]\d{9}'` | 11 位手机号 |
| URL | `r'https?://[\w\-._~:/?#\[\]@!$&\'()*+,;=%]+'` | HTTP/HTTPS 链接 |
| IPv4 地址 | `r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'` | 基础 IP 匹配 |
| 日期 (YYYY-MM-DD) | `r'\d{4}-\d{2}-\d{2}'` | ISO 日期格式 |
| 中文字符 | `r'[\u4e00-\u9fff]+'` | 匹配中文 |

## Java 对比

| 特性 | Java | Python |
|------|------|--------|
| 正则模块 | `java.util.regex` | `re` |
| 编译模式 | `Pattern.compile("\\d+")` | `re.compile(r"\d+")` |
| 转义 | 需要双重转义 `"\\d"` | 原始字符串 `r"\d"` |
| 匹配对象 | `Matcher` | `Match` |
| 查找所有 | 需要循环 `matcher.find()` | `re.findall()` 一步到位 |
| 替换 | `matcher.replaceAll()` | `re.sub()` |
| 命名分组 | `(?<name>...)` | `(?P<name>...)` |

**Java 写法：**
```java
import java.util.regex.*;

// Java：需要双重转义，步骤较多
Pattern pattern = Pattern.compile("(\\d{4})-(\\d{2})-(\\d{2})");
Matcher matcher = pattern.matcher("今天是 2025-07-15");
if (matcher.find()) {
    System.out.println("年: " + matcher.group(1));  // 2025
    System.out.println("月: " + matcher.group(2));  // 07
}

// 查找所有匹配需要循环
List<String> results = new ArrayList<>();
while (matcher.find()) {
    results.add(matcher.group());
}
```

**Python 写法：**
```python
import re

# Python：原始字符串，无需双重转义
m = re.search(r"(\d{4})-(\d{2})-(\d{2})", "今天是 2025-07-15")
if m:
    print(f"年: {m.group(1)}")  # 2025
    print(f"月: {m.group(2)}")  # 07

# 查找所有匹配，一步到位
results = re.findall(r"\d{4}-\d{2}-\d{2}", text)
```

## 实战代码

### 示例：正则表达式完整演示

**文件：** `examples/regex_demo.py`

演示 `re` 模块的核心功能：match/search/findall/finditer/sub/split/compile，常用模式匹配（邮箱、手机号、URL 等），分组捕获与命名分组，贪婪 vs 非贪婪匹配。

**运行方式：**
```bash
python examples/regex_demo.py
```

**预期输出：**
```
========== match vs search ==========
match 从开头匹配: Hello
search 搜索任意位置: World

========== findall 和 finditer ==========
findall 所有数字: ['100', '200', '50']
finditer 详细信息:
  '100' 位置: 3-6
  '200' 位置: 9-12
  '50' 位置: 15-17

========== sub 替换 ==========
原文: 我的手机号是 13812345678，备用号 13987654321
脱敏: 我的手机号是 138****5678，备用号 139****4321

========== split 分割 ==========
分割结果: ['apple', 'banana', 'cherry', 'date']

========== compile 预编译 ==========
找到邮箱: alice@example.com
找到邮箱: bob.test@gmail.com

========== 常用模式匹配 ==========
--- 邮箱验证 ---
  alice@example.com -> 有效
  invalid@.com -> 无效
--- 手机号验证 ---
  13812345678 -> 有效
  12345678901 -> 无效
--- URL 提取 ---
  https://www.python.org
  http://example.com/path

========== 分组捕获 ==========
--- 基本分组 ---
日期: 2025-07-15, 年=2025, 月=07, 日=15
--- 命名分组 ---
年=2025, 月=07, 日=15

========== 贪婪 vs 非贪婪 ==========
贪婪匹配: ['<b>bold</b> and <i>italic</i>']
非贪婪匹配: ['<b>', '</b>', '<i>', '</i>']
```

## 常见陷阱

### 1. 忘记使用原始字符串

Java 开发者习惯双重转义 `"\\d"`，在 Python 中应使用原始字符串 `r"\d"`。

```python
# ✗ 不推荐：普通字符串需要双重转义
pattern = "\\d+\\.\\d+"

# ✓ 推荐：原始字符串，清晰易读
pattern = r"\d+\.\d+"
```

### 2. 混淆 match 和 search

`re.match()` 只从字符串**开头**匹配，`re.search()` 在整个字符串中搜索。

```python
text = "Hello World 123"

re.match(r"\d+", text)   # None！因为开头不是数字
re.search(r"\d+", text)  # Match: '123'
```

### 3. findall 遇到分组时的行为变化

当正则表达式包含分组 `()` 时，`findall` 返回的是分组内容而非完整匹配。

```python
# 无分组：返回完整匹配
re.findall(r"\d{4}-\d{2}-\d{2}", "2025-07-15")
# ['2025-07-15']

# 有分组：返回分组内容！
re.findall(r"(\d{4})-(\d{2})-(\d{2})", "2025-07-15")
# [('2025', '07', '15')]  ← 注意：返回的是元组！

# 如果只想分组但不影响 findall，使用非捕获分组
re.findall(r"(?:\d{4})-(?:\d{2})-(?:\d{2})", "2025-07-15")
# ['2025-07-15']
```

### 4. 贪婪匹配导致意外结果

默认的 `*` 和 `+` 是贪婪的，会尽可能多地匹配。

```python
html = "<b>bold</b> and <i>italic</i>"

# ✗ 贪婪：匹配了整个字符串
re.findall(r"<.*>", html)
# ['<b>bold</b> and <i>italic</i>']

# ✓ 非贪婪：加 ? 后缀
re.findall(r"<.*?>", html)
# ['<b>', '</b>', '<i>', '</i>']
```

> 💻 **完整可运行代码：** [regex_demo.py](examples/regex_demo.py)

## 参考资料

- [Python 官方文档 - re 模块](https://docs.python.org/zh-cn/3/library/re.html)
- [Python 官方文档 - 正则表达式 HOWTO](https://docs.python.org/zh-cn/3/howto/regex.html)
- [regex101.com - 在线正则测试工具](https://regex101.com/)
- [Real Python - Regular Expressions](https://realpython.com/regex-python/)
