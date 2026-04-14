# HTTP 基础与 requests 库

> **模块：** 05-crawler（爬虫）
> **难度：** 入门
> **前置知识：** Python 基础、异常处理、文件操作
> **Python 版本：** >= 3.9
> **最后验证日期：** 2025-07-15

## 概念说明

HTTP（HyperText Transfer Protocol）是 Web 通信的基础协议。爬虫的本质就是模拟浏览器发送 HTTP 请求，获取服务器返回的数据。

Python 的 `requests` 库是最流行的 HTTP 客户端库，提供了简洁优雅的 API，支持 GET/POST/PUT/DELETE 等所有 HTTP 方法，以及 Session 会话管理、超时控制、重试机制等高级功能。

## Java 对比

| 特性 | Java | Python |
|------|------|--------|
| HTTP 客户端 | HttpClient / OkHttp / RestTemplate | requests |
| 会话管理 | CookieManager | requests.Session |
| 异步请求 | CompletableFuture + HttpClient | httpx (async) / aiohttp |
| JSON 解析 | Jackson / Gson | response.json() 内置 |

**Java 写法：**
```java
HttpClient client = HttpClient.newHttpClient();
HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://httpbin.org/get"))
    .timeout(Duration.ofSeconds(10))
    .build();
HttpResponse<String> response = client.send(request, BodyHandlers.ofString());
System.out.println(response.body());
```

**Python 写法：**
```python
import requests
response = requests.get("https://httpbin.org/get", timeout=10)
print(response.json())
```

## 核心知识点

### 1. HTTP 请求方法

| 方法 | 用途 | 幂等性 |
|------|------|--------|
| GET | 获取资源 | 是 |
| POST | 创建资源/提交数据 | 否 |
| PUT | 更新资源（全量） | 是 |
| DELETE | 删除资源 | 是 |
| PATCH | 更新资源（部分） | 否 |

### 2. 请求头（Headers）

常用请求头：
- `User-Agent`：标识客户端类型
- `Accept`：期望的响应格式
- `Content-Type`：请求体格式
- `Cookie`：会话信息
- `Referer`：来源页面

### 3. 响应状态码

| 状态码 | 含义 | 处理方式 |
|--------|------|----------|
| 200 | 成功 | 正常解析 |
| 301/302 | 重定向 | requests 自动跟随 |
| 403 | 禁止访问 | 检查 Headers/Cookie |
| 404 | 未找到 | 跳过或记录 |
| 429 | 请求过多 | 降低频率/等待 |
| 500 | 服务器错误 | 重试 |

## 实战代码

### 示例：requests 完整演示

**文件：** `examples/requests_demo.py`

演示内容：
- GET/POST 请求
- Session 会话管理
- 超时与重试机制
- 异常处理与日志记录
- 使用本地模拟 HTTP 服务（不依赖外部网站）

**运行方式：**
```bash
pip install requests
python examples/requests_demo.py
```

**预期输出：**
```
=== HTTP 基础演示（使用本地模拟）===
[GET 请求] 状态码: 200
[POST 请求] 状态码: 200
[Session 会话] 演示完成
[超时重试] 重试机制演示完成
[异常处理] 所有异常场景已覆盖
```

## 常见陷阱

- ⚠️ 忘记设置 `timeout` 参数，导致请求永久阻塞
- ⚠️ 不检查 `response.status_code`，直接解析响应体
- ⚠️ 频繁创建 Session 而不复用，浪费连接资源
- ⚠️ 忽略 `response.encoding`，导致中文乱码（用 `response.encoding = 'utf-8'`）
- ⚠️ 不处理网络异常（ConnectionError、Timeout），程序直接崩溃

> 💻 **完整可运行代码：** [requests_demo.py](examples/requests_demo.py)

## 参考资料

- [requests 官方文档](https://docs.python-requests.org/)
- [HTTP 协议 MDN 文档](https://developer.mozilla.org/zh-CN/docs/Web/HTTP)
- [httpbin.org 测试服务](https://httpbin.org/)
