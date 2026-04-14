# AI 应用 速查卡片

## 核心概念

| 概念 | 说明 | 示例 |
|------|------|------|
| NumPy | 科学计算基础库 | `np.array([1,2,3])` |
| Pandas | 数据分析库 | `pd.DataFrame(data)` |
| Matplotlib | 绘图库 | `plt.plot(x, y)` |
| LLM | 大语言模型 | GPT-4 / Llama / Qwen |
| RAG | 检索增强生成 | 文档检索 + LLM 生成 |
| Embedding | 文本向量化 | 将文本转为数值向量 |
| Agent | AI 智能体 | 自主决策 + 工具调用 |
| Prompt Engineering | 提示词工程 | 设计输入引导输出 |

## NumPy 速查

```python
import numpy as np

a = np.array([1, 2, 3])           # 创建数组
np.zeros((3, 3))                   # 全零矩阵
np.ones((2, 4))                    # 全一矩阵
np.arange(0, 10, 2)               # 等差数列
a.reshape(1, 3)                    # 改变形状
a.mean(), a.max(), a.sum()         # 统计运算
m1 @ m2                            # 矩阵乘法
```

## Pandas 速查

```python
import pandas as pd

df = pd.DataFrame({"col": [1, 2, 3]})  # 创建 DataFrame
df.head(), df.describe()                 # 查看数据
df[df["col"] > 1]                        # 过滤
df.groupby("col").mean()                 # 分组聚合
df.sort_values("col", ascending=False)   # 排序
df.to_csv("out.csv", index=False)        # 导出
```

## LLM API 调用

```python
from openai import OpenAI

# OpenAI
client = OpenAI(api_key="your-key")

# Ollama（免费替代）
client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "你是助手"},
        {"role": "user", "content": "你好"},
    ],
    temperature=0.7,
)
print(response.choices[0].message.content)
```

## Prompt Engineering 技巧

```python
# 1. 角色设定
system = "你是一位资深 Python 开发者"

# 2. Few-shot 示例
prompt = """
示例: "好用" → 正面
示例: "难用" → 负面
请分类: "非常满意" → """

# 3. Chain of Thought
prompt = "请一步一步思考..."

# 4. 输出格式约束
prompt = "请以 JSON 格式返回: {\"answer\": \"...\"}"
```

## RAG 流程

```python
# 1. 文档加载 → 2. 文本分块 → 3. 向量化 → 4. 存入向量库
# 5. 用户提问 → 6. 查询向量化 → 7. 相似度检索 → 8. LLM 生成回答

# 简化版（使用 LangChain）
from langchain.chains import RetrievalQA
qa = RetrievalQA.from_chain_type(llm=llm, retriever=vectorstore.as_retriever())
result = qa.invoke({"query": "问题"})
```

## 常见陷阱

- ⚠️ API Key 不要硬编码，使用环境变量 `os.environ["OPENAI_API_KEY"]`
- ⚠️ 注意 Token 限制，GPT-4 上下文窗口有限
- ⚠️ Temperature=0 更确定，Temperature=1 更创造性
- ⚠️ RAG 分块大小影响检索质量，太大太小都不好
- ⚠️ Embedding 模型和 LLM 是不同的模型，不要混淆
- ⚠️ Agent 可能陷入循环，需要设置最大步数限制

## 面试高频考点

- LLM 的 Token 机制和上下文窗口
- RAG 的完整流程和各环节优化
- Prompt Engineering 的核心技巧
- Embedding 向量的相似度计算方法
- AI Agent 的 ReAct 模式
- LangChain 的 Chain 和 LCEL 语法
- 向量数据库的选型（ChromaDB / FAISS / Pinecone）
- Fine-tuning vs RAG 的适用场景对比
