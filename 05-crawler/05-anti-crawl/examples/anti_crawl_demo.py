#!/usr/bin/env python3
"""
反爬策略与应对演示

模块: 05-crawler（爬虫）
知识点: 反爬策略
Python 版本: >= 3.9
最后验证: 2025-07-15

运行方式:
    python anti_crawl_demo.py

描述:
    演示常见的反爬应对技巧：User-Agent 轮换、请求频率控制、
    异常处理与自动重试。使用本地模拟服务器。
"""

import json
import logging
import random
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# 常用 User-Agent 列表
# ---------------------------------------------------------------------------
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15",
]


# ---------------------------------------------------------------------------
# 模拟带反爬检测的服务器
# ---------------------------------------------------------------------------
request_counter: dict[str, int] = {}


class AntiCrawlHandler(BaseHTTPRequestHandler):
    """模拟带反爬检测的服务器。"""

    def log_message(self, format, *args):
        pass

    def do_GET(self):
        ua = self.headers.get("User-Agent", "")
        client_ip = self.client_address[0]

        # 反爬检测 1: 检查 User-Agent
        if not ua or ua.startswith("python-requests"):
            self._send_json(403, {"error": "疑似爬虫，请设置合理的 User-Agent"})
            return

        # 反爬检测 2: 频率限制（每秒最多 3 次）
        current_time = int(time.time())
        key = f"{client_ip}:{current_time}"
        request_counter[key] = request_counter.get(key, 0) + 1
        if request_counter[key] > 3:
            self._send_json(429, {"error": "请求过于频繁，请稍后再试"})
            return

        # 正常响应
        self._send_json(200, {
            "message": "请求成功",
            "user_agent": ua[:50],
            "timestamp": current_time,
        })

    def _send_json(self, status, data):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(body)


def start_server(port=18082):
    server = HTTPServer(("127.0.0.1", port), AntiCrawlHandler)
    Thread(target=server.serve_forever, daemon=True).start()
    return server


# ---------------------------------------------------------------------------
# 反爬应对演示
# ---------------------------------------------------------------------------
BASE_URL = "http://127.0.0.1:18082"


def demo_ua_rotation():
    """演示 User-Agent 轮换。"""
    import requests

    logger.info("--- 1. User-Agent 轮换 ---")

    # 错误示范：使用默认 UA（会被检测）
    try:
        resp = requests.get(BASE_URL, timeout=5)
        if resp.status_code == 403:
            logger.warning(f"默认 UA 被拒绝: {resp.json()['error']}")
    except requests.exceptions.RequestException as e:
        logger.error(f"请求失败: {e}")

    # 正确做法：随机轮换 UA
    for i in range(3):
        ua = random.choice(USER_AGENTS)
        try:
            resp = requests.get(
                BASE_URL,
                headers={"User-Agent": ua},
                timeout=5,
            )
            logger.info(f"请求 {i+1}: 状态 {resp.status_code}, UA={ua[:40]}...")
        except requests.exceptions.RequestException as e:
            logger.error(f"请求失败: {e}")
        time.sleep(0.5)  # 频率控制


def demo_rate_limiting():
    """演示请求频率控制。"""
    import requests

    logger.info("\n--- 2. 请求频率控制 ---")

    ua = random.choice(USER_AGENTS)
    headers = {"User-Agent": ua}

    # 不控制频率（可能触发 429）
    logger.info("快速连续请求（可能触发频率限制）:")
    for i in range(5):
        try:
            resp = requests.get(BASE_URL, headers=headers, timeout=5)
            status = "✅" if resp.status_code == 200 else "❌"
            logger.info(f"  请求 {i+1}: {status} {resp.status_code}")
        except requests.exceptions.RequestException as e:
            logger.error(f"  请求 {i+1}: 失败 {e}")

    time.sleep(1.5)  # 等待频率限制重置

    # 控制频率
    logger.info("\n带频率控制的请求:")
    for i in range(3):
        try:
            resp = requests.get(BASE_URL, headers=headers, timeout=5)
            logger.info(f"  请求 {i+1}: ✅ {resp.status_code}")
        except requests.exceptions.RequestException as e:
            logger.error(f"  请求 {i+1}: 失败 {e}")
        time.sleep(random.uniform(0.5, 1.5))  # 随机延迟


def demo_retry_with_backoff():
    """演示异常处理与指数退避重试。"""
    import requests

    logger.info("\n--- 3. 指数退避重试 ---")

    ua = random.choice(USER_AGENTS)

    def fetch_with_retry(url, max_retries=3, base_delay=1.0):
        """带指数退避的请求函数。"""
        for attempt in range(max_retries):
            try:
                resp = requests.get(
                    url,
                    headers={"User-Agent": ua},
                    timeout=5,
                )
                if resp.status_code == 200:
                    return resp.json()
                elif resp.status_code == 429:
                    delay = base_delay * (2 ** attempt) + random.uniform(0, 1)
                    logger.warning(f"  频率限制，第 {attempt+1} 次重试，等待 {delay:.1f}s")
                    time.sleep(delay)
                else:
                    logger.warning(f"  状态码 {resp.status_code}，重试中...")
                    time.sleep(base_delay)
            except requests.exceptions.Timeout:
                logger.warning(f"  超时，第 {attempt+1} 次重试")
                time.sleep(base_delay)
            except requests.exceptions.ConnectionError:
                logger.error(f"  连接失败，第 {attempt+1} 次重试")
                time.sleep(base_delay * 2)
            except requests.exceptions.RequestException as e:
                logger.error(f"  请求异常: {e}")
                break
        logger.error("  所有重试均失败")
        return None

    result = fetch_with_retry(BASE_URL)
    if result:
        logger.info(f"最终结果: {result['message']}")


def main():
    """主函数。"""
    print("=" * 60)
    print("  反爬策略与应对演示")
    print("  ⚠️ 仅用于学习，请遵守网站规则")
    print("=" * 60)

    server = start_server(port=18082)

    try:
        demo_ua_rotation()
        demo_rate_limiting()
        demo_retry_with_backoff()
    finally:
        server.shutdown()

    print("\n✅ 反爬演示完成！")


if __name__ == "__main__":
    main()
