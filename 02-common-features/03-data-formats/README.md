# 数据格式处理（JSON / YAML / XML）

> **模块：** 02-常用功能
> **难度：** 入门
> **前置知识：** Python 基础（01-python-basics）
> **Python 版本：** >= 3.9
> **最后验证日期：** 2025-07-15

## 概念说明

数据格式处理是日常开发中最常见的任务之一。Python 提供了对 JSON、YAML、XML 三种主流数据格式的完整支持：`json` 模块是标准库自带的，`yaml`（PyYAML）和 `xml.etree.ElementTree` 分别用于 YAML 和 XML 的处理。

对于 Java 开发者来说，Python 的数据格式处理要简洁得多——不需要 Jackson/Gson 那样的复杂配置，也不需要 JAXB 那样的注解映射。Python 的字典（dict）天然对应 JSON 对象，列表（list）对应 JSON 数组，序列化/反序列化几乎是零配置的。

三种格式的核心操作都是两个方向：**解析（parse）** 将文本转为 Python 对象，**生成（dump）** 将 Python 对象转为文本。一个重要的质量保证是**往返一致性（roundtrip）**：`parse(dump(data)) == data`，即序列化再反序列化后数据不丢失。

### 三种格式对比

| 特性 | JSON | YAML | XML |
|------|------|------|-----|
| 可读性 | 好 | 最好（缩进语法） | 一般（标签冗长） |
| Python 模块 | `json`（标准库） | `pyyaml`（第三方） | `xml.etree.ElementTree`（标准库） |
| 数据类型 | 字符串/数字/布尔/null/数组/对象 | 同 JSON + 日期/多行文本等 | 纯文本（需自行转换类型） |
| 注释支持 | ❌ 不支持 | ✅ 支持 `#` 注释 | ✅ 支持 `<!-- -->` 注释 |
| 常见用途 | API 数据交换、配置文件 | 配置文件（Docker/K8s） | 企业级数据交换、SOAP |
| Java 对应库 | Jackson / Gson | SnakeYAML | JAXB / DOM / SAX |

### 核心函数速查

| 操作 | JSON | YAML | XML |
|------|------|------|-----|
| 字符串→对象 | `json.loads(s)` | `yaml.safe_load(s)` | `ET.fromstring(s)` |
| 对象→字符串 | `json.dumps(obj)` | `yaml.dump(obj)` | `ET.tostring(elem)` |
| 文件→对象 | `json.load(f)` | `yaml.safe_load(f)` | `ET.parse(file)` |
| 对象→文件 | `json.dump(obj, f)` | `yaml.dump(obj, f)` | `tree.write(file)` |

## Java 对比

| 特性 | Java | Python |
|------|------|--------|
| JSON 序列化 | `new ObjectMapper().writeValueAsString(obj)` | `json.dumps(obj)` |
| JSON 反序列化 | `mapper.readValue(json, MyClass.class)` | `json.loads(json_str)` |
| 需要定义类 | 是（POJO/DTO） | 否（直接用 dict） |
| YAML 解析 | `new Yaml().load(input)` | `yaml.safe_load(text)` |
| XML 解析 | `DocumentBuilderFactory` + DOM | `ET.fromstring(text)` |
| XPath 查询 | `XPathFactory` | `elem.findall("xpath")` |

**Java 写法：**
```java
// Java：JSON 处理需要 Jackson + POJO 类
import com.fasterxml.jackson.databind.ObjectMapper;

public class User {
    private String name;
    private int age;
    // getter/setter 省略
}

ObjectMapper mapper = new ObjectMapper();
// 序列化
String json = mapper.writeValueAsString(user);
// 反序列化（必须指定目标类）
User user = mapper.readValue(json, User.class);
```

**Python 写法：**
```python
import json

# Python：直接用 dict，无需定义类
user = {"name": "Alice", "age": 30}
# 序列化
json_str = json.dumps(user)
# 反序列化（直接得到 dict）
data = json.loads(json_str)
```

## 实战代码

### 示例 1：JSON 处理

**文件：** `examples/json_demo.py`

演示 JSON 的解析（loads）和生成（dumps），文件读写（load/dump），自定义序列化（处理 datetime 等不可序列化类型）。

**运行方式：**
```bash
python examples/json_demo.py
```

### 示例 2：YAML 处理

**文件：** `examples/yaml_demo.py`

演示 YAML 的解析（safe_load）和生成（dump），多文档处理（safe_load_all）。

> 需要安装依赖：`pip install pyyaml`

**运行方式：**
```bash
python examples/yaml_demo.py
```

### 示例 3：XML 处理

**文件：** `examples/xml_demo.py`

演示 XML 的解析（ElementTree）和生成，XPath 查询，属性操作。

**运行方式：**
```bash
python examples/xml_demo.py
```

### 示例 4：往返一致性验证

**文件：** `examples/roundtrip_test.py`

验证 `parse(format(data)) == data` 的往返一致性，确保序列化和反序列化不丢失数据。

**运行方式：**
```bash
python examples/roundtrip_test.py
```

## 常见陷阱

### 1. json.dumps 不支持所有 Python 类型

`json.dumps()` 只支持基本类型（str/int/float/bool/None/list/dict），遇到 `datetime`、`set`、`bytes` 等类型会抛出 `TypeError`。

```python
import json
from datetime import datetime

# ✗ 错误：datetime 不可序列化
# json.dumps({"time": datetime.now()})  # TypeError!

# ✓ 正确：自定义序列化器
class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

json.dumps({"time": datetime.now()}, cls=DateTimeEncoder)
```

### 2. yaml.load() vs yaml.safe_load()

`yaml.load()` 可以执行任意 Python 代码，存在安全风险。始终使用 `yaml.safe_load()`。

```python
import yaml

# ✗ 危险：yaml.load() 可执行任意代码
# yaml.load(untrusted_input)  # 安全漏洞！

# ✓ 安全：使用 safe_load
data = yaml.safe_load(text)
```

### 3. XML 命名空间处理

XML 命名空间会影响标签查找，需要在查询时指定命名空间前缀。

```python
import xml.etree.ElementTree as ET

# 带命名空间的 XML
xml = '<root xmlns:ns="http://example.com"><ns:item>1</ns:item></root>'
root = ET.fromstring(xml)

# ✗ 找不到：未指定命名空间
root.find("item")  # None!

# ✓ 正确：指定命名空间
ns = {"ns": "http://example.com"}
root.find("ns:item", ns)  # 找到了
```

### 4. JSON 中文编码

`json.dumps()` 默认会将中文转为 Unicode 转义序列。

```python
import json

data = {"名字": "张三"}

# 默认：中文被转义
json.dumps(data)
# '{"\\u540d\\u5b57": "\\u5f20\\u4e09"}'

# ✓ 保留中文
json.dumps(data, ensure_ascii=False)
# '{"名字": "张三"}'
```

> 💻 **完整可运行代码：** [json_demo.py](examples/json_demo.py) | [yaml_demo.py](examples/yaml_demo.py) | [xml_demo.py](examples/xml_demo.py) | [roundtrip_test.py](examples/roundtrip_test.py)

## 参考资料

- [Python 官方文档 - json](https://docs.python.org/zh-cn/3/library/json.html)
- [Python 官方文档 - xml.etree.ElementTree](https://docs.python.org/zh-cn/3/library/xml.etree.elementtree.html)
- [PyYAML 官方文档](https://pyyaml.org/wiki/PyYAMLDocumentation)
- [Real Python - Working With JSON Data](https://realpython.com/python-json/)
