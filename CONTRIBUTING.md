# 贡献指南

感谢你对 Python 学习知识库的贡献！本文档说明如何新增模块和知识点，确保内容风格一致。

## 目录

- [项目结构概览](#项目结构概览)
- [如何新增知识点](#如何新增知识点)
- [如何新增模块](#如何新增模块)
- [文档规范](#文档规范)
- [代码示例规范](#代码示例规范)
- [提交检查清单](#提交检查清单)

## 项目结构概览

```
python-learning-guide/
├── README.md                # 主索引（新增模块后需更新）
├── templates/               # 文档和代码模板
│   ├── topic_template.md
│   ├── module_readme_template.md
│   ├── cheatsheet_template.md
│   └── example_script_template.py
├── 01-python-basics/        # 各模块目录
├── 02-common-features/
├── ...
└── tests/                   # 测试文件
```

## 如何新增知识点

### 步骤 1：选择所属模块

确定新知识点属于哪个模块（01-08）。如果不属于任何现有模块，请参考[如何新增模块](#如何新增模块)。

### 步骤 2：创建知识点目录

在对应模块目录下创建新的知识点目录，使用数字前缀保持排序：

```bash
# 示例：在常用功能模块下新增一个知识点
mkdir -p 02-common-features/08-new-topic/examples
```

### 步骤 3：使用模板创建文档

复制知识点文档模板并填写内容：

```bash
cp templates/topic_template.md 02-common-features/08-new-topic/README.md
```

文档必须包含以下章节：
- **标题** — 知识点名称
- **概念说明** — 核心概念解释（2-3 段）
- **Java 对比** — 与 Java 对应概念的对比（如适用）
- **实战代码** — 可独立运行的代码示例（必须）
- **运行说明** — 如何运行代码
- **预期输出** — 运行后的预期结果
- **常见陷阱** — Java 开发者容易犯的错误
- **参考资料** — 相关链接

### 步骤 4：创建代码示例

复制代码示例模板并实现：

```bash
cp templates/example_script_template.py 02-common-features/08-new-topic/examples/demo.py
```

代码示例要求：
- 可通过 `python filename.py` 直接运行
- docstring 中包含 Python 版本要求和最后验证日期
- 包含中文注释说明
- 包含适当的错误处理

### 步骤 5：更新模块索引

在模块的 `README.md` 中添加新知识点的链接和描述。

### 步骤 6：更新主索引

在项目根目录的 `README.md` 中：
- 如果知识点属于"面试常考"、"工作常用"或"AI 入门"分类，添加到对应的快速查找表中
- 确保模块导航表信息准确

## 如何新增模块

### 步骤 1：创建模块目录

```bash
mkdir -p XX-module-name
```

使用两位数字前缀，按学习路径顺序编号。

### 步骤 2：创建模块索引

复制模块索引模板：

```bash
cp templates/module_readme_template.md XX-module-name/README.md
```

填写模块简介、知识点列表、推荐学习顺序等。

### 步骤 3：创建模块依赖文件

如果模块需要外部依赖，创建模块级 `requirements.txt`：

```bash
touch XX-module-name/requirements.txt
```

同时更新项目级 `requirements.txt`，在对应分组下添加依赖。

### 步骤 4：创建速查卡片

复制速查卡片模板：

```bash
cp templates/cheatsheet_template.md XX-module-name/cheatsheet.md
```

### 步骤 5：更新主索引

在 `README.md` 中：
- 更新模块导航表
- 更新学习路径图（如需要）
- 更新前置依赖说明

### 步骤 6：重新生成知识图谱

```bash
python tools/generate_mindmap.py
python tools/generate_knowledge_graph.py
```

## 文档规范

### 语言

- 文档内容使用**中文**
- 技术术语可保留英文（如 decorator、generator、ORM 等）
- 代码注释使用中文或英文均可

### 格式

- 使用 Markdown 格式
- 标题层级：`#` 为文档标题，`##` 为主要章节，`###` 为子章节
- 代码块标注语言类型（```python、```java、```bash 等）
- 表格对齐，保持可读性

### 元数据

每个知识点文档头部需包含：

```markdown
> **模块：** {所属模块名}
> **难度：** {入门/进阶/高级}
> **前置知识：** {需要先学习的知识点}
> **Python 版本：** >= 3.9
> **最后验证日期：** {YYYY-MM-DD}
```

## 代码示例规范

### docstring 格式

每个 `.py` 文件必须包含以下 docstring 元数据：

```python
"""
{示例标题}

模块: {所属模块}
知识点: {对应知识点}
Python 版本: >= 3.9
最后验证: YYYY-MM-DD

运行方式:
    python {filename}.py

描述:
    {简要描述}
"""
```

### 代码风格

- 遵循 PEP 8 规范
- 使用 4 空格缩进
- 函数和类包含 docstring
- 关键逻辑添加注释

### 可运行性

- 每个示例必须可通过 `python filename.py` 独立运行
- 包含 `if __name__ == "__main__":` 入口
- 外部依赖在模块 `requirements.txt` 中声明

## 提交检查清单

新增内容前，请确认以下事项：

- [ ] 文档使用了正确的模板格式
- [ ] 所有代码示例可独立运行
- [ ] 代码示例包含 docstring 元数据（Python 版本、验证日期）
- [ ] 模块 README.md 已更新知识点列表
- [ ] 项目根目录 README.md 已更新（如需要）
- [ ] 外部依赖已添加到对应的 requirements.txt
- [ ] 文档包含"实战代码"章节（不能仅有理论）
- [ ] Java 对比章节已填写（如适用）
- [ ] 代码包含适当的错误处理
- [ ] 运行 `python tools/generate_mindmap.py` 更新思维导图
- [ ] 运行 `python tools/generate_knowledge_graph.py` 更新知识图谱
