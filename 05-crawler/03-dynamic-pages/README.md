# 动态页面爬取（Selenium / Playwright）

> **模块：** 05-crawler（爬虫）
> **难度：** 进阶
> **前置知识：** HTTP 基础、HTML 解析
> **Python 版本：** >= 3.9
> **最后验证日期：** 2025-07-15

## 概念说明

现代网站大量使用 JavaScript 动态渲染内容（如 React、Vue 单页应用）。传统的 `requests + BeautifulSoup` 只能获取初始 HTML，无法执行 JavaScript，因此看不到动态加载的数据。

解决方案有两种思路：
1. **浏览器自动化**：使用 Selenium / Playwright 控制真实浏览器，等待 JS 渲染完成后再提取数据
2. **分析 API 接口**：通过浏览器开发者工具找到数据接口，直接用 requests 请求 API（推荐优先尝试）

## Java 对比

| 特性 | Java | Python |
|------|------|--------|
| 浏览器自动化 | Selenium WebDriver | Selenium / Playwright |
| 无头浏览器 | HtmlUnit | Playwright (headless) |
| API 分析 | OkHttp + 手动分析 | requests + 开发者工具 |

## 工具对比

| 特性 | Selenium | Playwright |
|------|----------|------------|
| 浏览器支持 | Chrome/Firefox/Edge/Safari | Chromium/Firefox/WebKit |
| 安装复杂度 | 需要下载 WebDriver | `playwright install` 一键安装 |
| 速度 | 较慢 | 较快 |
| API 风格 | 传统命令式 | 现代 async/await |
| 自动等待 | 需手动 WebDriverWait | 内置自动等待 |
| 社区成熟度 | 非常成熟 | 快速增长 |

## 实战代码

### 示例：动态页面处理演示

**文件：** `examples/dynamic_demo.py`

演示内容：
- Selenium / Playwright 概念说明（注释形式，因需要浏览器驱动）
- **可运行的 requests 替代方案**：分析 API 接口直接获取数据
- 模拟动态页面的 JSON API 调用

**运行方式：**
```bash
python examples/dynamic_demo.py
```

**预期输出：**
```
=== 动态页面处理演示 ===
[API 分析法] 模拟获取动态数据成功
[分页加载] 获取到 3 页数据
```

## 推荐策略

```
遇到动态页面时的处理流程：

1. 打开浏览器开发者工具（F12）
2. 切换到 Network 标签页
3. 刷新页面，观察 XHR/Fetch 请求
4. 找到数据接口 → 用 requests 直接请求（首选）
5. 找不到接口 → 使用 Selenium/Playwright
```

## 常见陷阱

- ⚠️ 优先分析 API 接口，浏览器自动化是最后手段（速度慢、资源消耗大）
- ⚠️ Selenium 需要匹配浏览器版本的 WebDriver
- ⚠️ 动态页面可能有反爬检测（WebDriver 指纹）
- ⚠️ 等待元素加载要用显式等待，不要用 `time.sleep()`

> 💻 **完整可运行代码：** [dynamic_demo.py](examples/dynamic_demo.py)

## 参考资料

- [Selenium Python 文档](https://selenium-python.readthedocs.io/)
- [Playwright Python 文档](https://playwright.dev/python/)
