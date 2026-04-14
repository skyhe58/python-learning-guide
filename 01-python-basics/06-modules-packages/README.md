# 模块与包管理

> **模块：** 01-Python 基础
> **难度：** 入门
> **前置知识：** 类与面向对象（05-oop）
> **Python 版本：** >= 3.9
> **最后验证日期：** 2025-07-15

## 概念说明

在 Python 中，**模块（Module）** 就是一个 `.py` 文件，**包（Package）** 就是一个包含 `__init__.py` 的目录。这与 Java 中"包是命名空间、类是编译单元"的设计有本质区别——Python 的模块系统更加简单直接：一个文件就是一个模块，一个目录就是一个包。

Python 的 `import` 机制是动态的：在运行时查找并加载模块，而非 Java 那样在编译时解析依赖。Python 解释器按照 `sys.path` 列表中的路径顺序搜索模块，找到第一个匹配的就加载。这种动态性带来了灵活性，但也意味着拼写错误或路径配置问题只有在运行时才会暴露。

Python 的包管理工具 **pip** 类似于 Java 的 Maven/Gradle，但更加轻量。pip 从 **PyPI（Python Package Index）** 下载和安装第三方包，配合 `requirements.txt` 或 `pyproject.toml` 管理项目依赖。与 Maven 的 `pom.xml` 相比，Python 的依赖管理更简洁，但也缺少 Maven 那样的依赖树解析和冲突自动处理能力。

### 核心概念一览

| 概念 | 说明 |
|------|------|
| 模块（Module） | 一个 `.py` 文件，包含函数、类、变量等定义 |
| 包（Package） | 包含 `__init__.py` 的目录，用于组织多个模块 |
| `import` | 导入模块或包，支持多种语法形式 |
| `from ... import` | 从模块中导入特定对象 |
| `as` | 为导入的模块或对象设置别名 |
| `__init__.py` | 包的初始化文件，可以为空或包含包级别的代码 |
| `__name__` | 模块属性，直接运行时为 `"__main__"`，被导入时为模块名 |
| `sys.path` | 模块搜索路径列表，决定 Python 在哪里查找模块 |
| `pip` | Python 包管理工具，安装/卸载/管理第三方包 |
| `requirements.txt` | 项目依赖声明文件，列出所有第三方包及版本 |

## Java 对比

### 导入机制

| 特性 | Java | Python |
|------|------|--------|
| 导入语法 | `import java.util.List;` | `import os` 或 `from os import path` |
| 通配符导入 | `import java.util.*;` | `from os import *`（不推荐） |
| 别名 | 不支持（Java 没有 import alias） | `import numpy as np` |
| 导入时机 | 编译时解析 | 运行时动态加载 |
| 导入对象 | 只能导入类 | 可以导入模块、函数、类、变量等任何对象 |
| 静态导入 | `import static Math.PI;` | `from math import pi`（天然支持） |

**Java 写法：**
```java
// Java：导入类，必须指定完整包路径
import java.util.List;
import java.util.ArrayList;
import java.util.Map;
import java.util.HashMap;

// 通配符导入（不推荐，但可用）
import java.util.*;

// 静态导入
import static java.lang.Math.PI;
import static java.lang.Math.sqrt;

public class Demo {
    public static void main(String[] args) {
        List<String> list = new ArrayList<>();
        double r = sqrt(PI);
    }
}
```

**Python 写法：**
```python
# Python：导入模块或模块中的任何对象
import os
import sys
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict, Counter

# 别名导入（Java 不支持）
import numpy as np
from matplotlib import pyplot as plt

# 导入后直接使用
cwd = os.getcwd()
now = datetime.now()
p = Path(".")
```

### 包与模块组织

| 特性 | Java | Python |
|------|------|--------|
| 包定义 | `package com.example.utils;`（声明在文件头） | 目录 + `__init__.py`（文件系统即包结构） |
| 包层级 | 用 `.` 分隔（`com.example.utils`） | 用 `.` 分隔（`mypackage.utils`） |
| 一个文件一个类 | 强制（public class 必须与文件名一致） | 一个文件可以包含多个类、函数、变量 |
| 包初始化 | 无 | `__init__.py` 在包被导入时自动执行 |
| 可见性控制 | `public`/`private`/`protected`/默认 | `_` 前缀约定（`from pkg import *` 不导入） |
| 命名空间包 | 不支持 | Python 3.3+ 支持无 `__init__.py` 的命名空间包 |

**Java 包结构：**
```
src/
└── com/
    └── example/
        └── utils/
            ├── StringUtils.java    // package com.example.utils;
            └── MathUtils.java      // package com.example.utils;
```

**Python 包结构：**
```
mypackage/
├── __init__.py          # 包初始化文件（可以为空）
├── utils.py             # 模块：mypackage.utils
├── models.py            # 模块：mypackage.models
└── sub_package/         # 子包
    ├── __init__.py
    └── helpers.py       # 模块：mypackage.sub_package.helpers
```

### 依赖管理

| 特性 | Java (Maven/Gradle) | Python (pip) |
|------|---------------------|--------------|
| 配置文件 | `pom.xml` / `build.gradle` | `requirements.txt` / `pyproject.toml` |
| 仓库 | Maven Central / JCenter | PyPI (pypi.org) |
| 安装命令 | `mvn install` / `gradle build` | `pip install -r requirements.txt` |
| 单包安装 | 在配置文件中添加依赖 | `pip install package_name` |
| 版本锁定 | `<version>1.2.3</version>` | `package==1.2.3` |
| 版本范围 | `[1.0, 2.0)` | `package>=1.0,<2.0` |
| 依赖树 | `mvn dependency:tree` | `pip show package` / `pipdeptree` |
| 虚拟环境 | 不需要（项目级依赖隔离） | `venv` / `conda`（强烈推荐） |
| 打包格式 | `.jar` / `.war` | `.whl`（wheel）/ `.tar.gz` |
| 发布 | `mvn deploy` | `twine upload` |

**Java Maven 依赖声明：**
```xml
<!-- pom.xml -->
<dependencies>
    <dependency>
        <groupId>com.google.guava</groupId>
        <artifactId>guava</artifactId>
        <version>32.1.3-jre</version>
    </dependency>
    <dependency>
        <groupId>org.apache.commons</groupId>
        <artifactId>commons-lang3</artifactId>
        <version>3.14.0</version>
    </dependency>
</dependencies>
```

**Python pip 依赖声明：**
```
# requirements.txt — 比 Maven 简洁得多
requests>=2.31.0
flask>=3.0.0
sqlalchemy>=2.0
pytest>=7.4.0
```

### 绝对导入 vs 相对导入

| 特性 | Java | Python |
|------|------|--------|
| 绝对导入 | `import com.example.utils.StringUtils;` | `from mypackage.utils import helper` |
| 相对导入 | 不支持 | `from . import utils`（当前包）<br>`from .. import models`（上级包） |
| 推荐方式 | 只有绝对导入 | 优先使用绝对导入，包内部可用相对导入 |

```python
# 绝对导入（推荐，清晰明确）
from mypackage.utils import helper
from mypackage.sub_package.helpers import format_data

# 相对导入（仅在包内部使用）
from . import utils           # 当前包的 utils 模块
from .utils import helper     # 当前包 utils 模块的 helper
from .. import models          # 上级包的 models 模块
from ..models import User      # 上级包 models 模块的 User
```

## 实战代码

### 示例：模块与包管理完整演示

**文件：** `examples/modules_demo.py`

演示 Python 模块与包管理的核心知识：import 的各种方式、标准库模块使用（os、sys、json、pathlib、datetime）、`__name__ == "__main__"` 的作用、模块搜索路径 `sys.path`、`dir()` 查看模块内容、自定义模块的创建说明，并在注释中与 Java 对比。

**运行方式：**
```bash
python examples/modules_demo.py
```

**预期输出：**
```
========== import 的各种方式 ==========
--- import 模块 ---
当前工作目录: /path/to/current/dir
操作系统: posix
--- from 模块 import 对象 ---
当前时间: 2025-07-15 10:30:00
一周后: 2025-07-22 10:30:00
--- as 别名 ---
当前目录: /path/to/current/dir
目录下的 .py 文件: [...]

========== 标准库模块使用 ==========
--- os 模块 ---
当前目录: /path/to/current/dir
环境变量 HOME: /home/user
--- sys 模块 ---
Python 版本: 3.x.x
平台: linux/darwin/win32
--- json 模块 ---
JSON 字符串: {"name": "张三", "age": 25, "skills": ["Python", "Java"]}
解析回来: {'name': '张三', 'age': 25, 'skills': ['Python', 'Java']}
--- pathlib 模块 ---
当前文件: /path/to/modules_demo.py
父目录: /path/to/examples
文件是否存在: True
--- datetime 模块 ---
现在: 2025-07-15 10:30:00
格式化: 2025年07月15日 10:30:00

========== __name__ == "__main__" ==========
当前模块的 __name__: __main__
说明: 直接运行此脚本时 __name__ 为 '__main__'
说明: 被其他模块 import 时 __name__ 为模块名

========== 模块搜索路径 sys.path ==========
Python 模块搜索路径（前 5 个）:
  1. /path/to/current/dir
  2. /usr/lib/python3.x
  ...

========== dir() 查看模块内容 ==========
--- math 模块的常用属性 ---
常量: pi=3.141592653589793, e=2.718281828459045
函数: ['acos', 'asin', 'atan', 'ceil', 'cos', 'exp', 'floor', ...]
--- 查看对象的所有属性 ---
字符串的方法数量: 78
常用字符串方法: ['capitalize', 'center', 'count', 'encode', 'endswith', ...]

========== 自定义模块说明 ==========
--- 创建自定义模块 ---
1. 创建 my_utils.py 文件，定义函数和类
2. 在同目录下的其他文件中 import my_utils
3. 使用 my_utils.function_name() 调用
--- 创建包 ---
1. 创建目录 mypackage/
2. 添加 __init__.py（可以为空）
3. 添加模块文件 mypackage/utils.py
4. 使用 from mypackage import utils
```

## 常见陷阱

### 1. 循环导入（Circular Import）

Java 中循环依赖在编译时就会被检测到，Python 的循环导入在运行时才会出问题，而且错误信息可能很难理解。

```python
# ✗ 错误：循环导入
# a.py
from b import func_b  # 导入 b 时，b 又要导入 a，死循环
def func_a():
    return func_b()

# b.py
from a import func_a  # ImportError 或 AttributeError
def func_b():
    return func_a()

# ✓ 解决方案 1：延迟导入（在函数内部导入）
# a.py
def func_a():
    from b import func_b  # 在需要时才导入
    return func_b()

# ✓ 解决方案 2：重构代码，提取公共部分到第三个模块
```

### 2. `from module import *` 污染命名空间

Java 的 `import java.util.*` 只导入类名，不会覆盖已有变量。Python 的 `from module import *` 会将模块中所有公开名称导入当前命名空间，可能覆盖已有变量。

```python
# ✗ 不推荐：通配符导入
from os.path import *  # 导入了 join, exists, split 等
from string import *   # 可能覆盖上面导入的名称！

# ✓ 推荐：明确导入需要的对象
from os.path import join, exists
from string import ascii_letters
```

### 3. 模块名与标准库冲突

如果你的文件名与标准库模块同名，Python 会优先导入你的文件而非标准库。

```python
# ✗ 错误：文件名为 json.py
# json.py
import json  # 导入的是自己！不是标准库的 json
data = json.loads('{"a": 1}')  # AttributeError

# ✓ 正确：避免使用标准库模块名作为文件名
# my_json_utils.py
import json  # 正确导入标准库
```

### 4. 相对导入只能在包内使用

直接运行包内的模块文件时，相对导入会失败。

```python
# mypackage/utils.py
from . import helpers  # 相对导入

# ✗ 错误：直接运行会失败
# $ python mypackage/utils.py
# ImportError: attempted relative import with no known parent package

# ✓ 正确：作为包的一部分运行
# $ python -m mypackage.utils
```

### 5. 忘记 `__init__.py`（Python 3.3 之前）

Python 3.3+ 引入了命名空间包，目录不需要 `__init__.py` 也能作为包导入。但为了兼容性和明确性，建议始终添加 `__init__.py`。

```
# ✓ 推荐：始终添加 __init__.py
mypackage/
├── __init__.py      # 即使为空也要添加
├── module_a.py
└── module_b.py
```

> 💻 **完整可运行代码：** [modules_demo.py](examples/modules_demo.py)

## 参考资料

- [Python 官方文档 - 模块](https://docs.python.org/zh-cn/3/tutorial/modules.html)
- [Python 官方文档 - 导入系统](https://docs.python.org/zh-cn/3/reference/import.html)
- [Python 官方文档 - pip](https://pip.pypa.io/en/stable/)
- [PyPI - Python Package Index](https://pypi.org/)
- [Real Python - Python Modules and Packages](https://realpython.com/python-modules-packages/)
- [Real Python - Absolute vs Relative Imports](https://realpython.com/absolute-vs-relative-python-imports/)
