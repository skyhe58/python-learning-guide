# 反爬策略与应对

> **模块：** 05-crawler（爬虫）
> **难度：** 进阶
> **前置知识：** HTTP 基础、requests 库
> **Python 版本：** >= 3.9
> **最后验证日期：** 2025-07-15

## 概念说明

网站为了保护数据和服务器资源，会部署各种反爬措施。了解这些措施有助于编写更健壮的爬虫，同时也提醒我们要遵守网站规则，合理控制爬取频率。

**重要声明：** 本节内容仅用于学习目的。在实际爬取时，请务必遵守目标网站的 robots.txt 协议和服务条款。

## 常见反爬措施

| 反爬措施 | 检测方式 | 应对策略 |
|----------|----------|----------|
| User-Agent 检测 | 检查请求头 | 轮换 UA |
| IP 频率限制 | 统计请求频率 | 控制频率 / 代理池 |
| Cookie/Session 验证 | 检查登录状态 | 维护 Session |
| 验证码 | 人机验证 | OCR / 打码平台 |
| JavaScript 渲染 | 检查 JS 执行 | Selenium/Playwright |
| 请求签名 | 加密参数验证 | 逆向分析 |

## 实战代码

### 示例：反爬应对演示

**文件：** `examples/anti_crawl_demo.py`

演示内容：
- User-Agent 轮换
- 请求频率控制
- 异常处理与重试
- 日志记录

**运行方式：**
```bash
python examples/anti_crawl_demo.py
```

## 常见陷阱

- ⚠️ 不要过于频繁地请求同一网站，可能导致 IP 被封
- ⚠️ 使用代理时要验证代理的可用性
- ⚠️ 遵守 robots.txt 和网站服务条款
- ⚠️ 爬取数据用于商业用途可能涉及法律风险

> 💻 **完整可运行代码：** [anti_crawl_demo.py](examples/anti_crawl_demo.py)

## 参考资料

- [robots.txt 规范](https://www.robotstxt.org/)
- [requests 高级用法](https://docs.python-requests.org/en/latest/user/advanced/)
