#!/usr/bin/env python3
"""
HTTP 基础与 requests 库演示

模块: 05-crawler（爬虫）
知识点: HTTP 基础与 requests
Python 版本: >= 3.9
最后验证: 2025-07-15

运行方式:
    pip install requests
    python requests_demo.py

描述:
    演示 requests 库的 GET/POST/Session、超时重试、异常处理和日志记录。
    使用本地模拟 HTTP 响应，不依赖外部网站。
"""

import json
import logging
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread
from urllib.parse import urlparse, parse_qs

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# 本地模拟 HTTP 服务器（替代 httpbin.org）
# ---------------------------------------------------------------------------
class MockHTTPHandler(BaseHTTPRequestHandler):
    """模拟 HTTP 服务，用于演示各种请求场景。"""

    def log_message(self, format, *args):
        """静默服务器日志。"""
        pass

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/get":
            data = {
                "url": self.path,
                "method": "GET",
                "headers": dict(self.headers),
                "args": parse_qs(parsed.query),
            }
            self._send_json(200, data)
        elif parsed.path == "/status/404":
            self._send_json(404, {"error": "Not Found"})
        elif parsed.path == "/delay":
            time.sleep(5)  # 模拟慢响应
            self._send_json(200, {"delayed": True})
        else:
            self._send_json(200, {"path": self.path})

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8") if content_length else ""
        try:
            body_json = json.loads(body) if body else {}
        except json.JSONDecodeError:
            body_json = {"raw": body}
        data = {
            "url": self.path,
            "method": "POST",
            "headers": dict(self.headers),
            "json": body_json,
        }
        self._send_json(200, data)

    def _send_json(self, status, data):
        response = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(response)))
        self.end_headers()
        self.wfile.write(response)


def start_mock_server(port=18080):
    """启动本地模拟服务器。"""
    server = HTTPServer(("127.0.0.1", port), MockHTTPHandler)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    logger.info(f"模拟服务器已启动: http://127.0.0.1:{port}")
    return server


# ---------------------------------------------------------------------------
# 演示函数
# ---------------------------------------------------------------------------
BASE_URL = "http://127.0.0.1:18080"


def demo_get_request():
    """演示 GET 请求。"""
    import requests

    logger.info("--- GET 请求演示 ---")

    # 基本 GET 请求
    resp = requests.get(f"{BASE_URL}/get", timeout=5)
    logger.info(f"状态码: {resp.status_code}")
    logger.info(f"响应体: {resp.json()['method']}")

    # 带查询参数的 GET 请求
    params = {"keyword": "python", "page": 1}
    resp = requests.get(f"{BASE_URL}/get", params=params, timeout=5)
    logger.info(f"带参数请求: {resp.json()['args']}")

    # 自定义请求头
    headers = {
        "User-Agent": "Mozilla/5.0 (学习爬虫)",
        "Accept": "application/json",
    }
    resp = requests.get(f"{BASE_URL}/get", headers=headers, timeout=5)
    logger.info(f"自定义 UA: {resp.json()['headers'].get('User-Agent', 'N/A')}")


def demo_post_request():
    """演示 POST 请求。"""
    import requests

    logger.info("--- POST 请求演示 ---")

    # 发送 JSON 数据
    payload = {"username": "demo_user", "action": "login"}
    resp = requests.post(f"{BASE_URL}/post", json=payload, timeout=5)
    logger.info(f"POST JSON 状态码: {resp.status_code}")
    logger.info(f"服务器收到: {resp.json()['json']}")

    # 发送表单数据
    form_data = {"field1": "value1", "field2": "value2"}
    resp = requests.post(f"{BASE_URL}/post", data=form_data, timeout=5)
    logger.info(f"POST Form 状态码: {resp.status_code}")


def demo_session():
    """演示 Session 会话管理（自动维护 Cookie）。"""
    import requests

    logger.info("--- Session 会话演示 ---")

    session = requests.Session()
    # Session 可以设置默认 Headers，后续请求自动携带
    session.headers.update({"User-Agent": "PythonCrawler/1.0"})

    # 第一次请求
    resp1 = session.get(f"{BASE_URL}/get", timeout=5)
    logger.info(f"Session 请求1: {resp1.status_code}")

    # 第二次请求（自动携带之前的 Cookie 和 Headers）
    resp2 = session.get(f"{BASE_URL}/get", timeout=5)
    logger.info(f"Session 请求2: {resp2.status_code}")

    session.close()
    logger.info("Session 已关闭")


def demo_timeout_retry():
    """演示超时设置与重试机制。"""
    import requests
    from requests.adapters import HTTPAdapter
    from urllib3.util.retry import Retry

    logger.info("--- 超时与重试演示 ---")

    # 1. 超时设置
    try:
        resp = requests.get(f"{BASE_URL}/delay", timeout=1)
    except requests.exceptions.Timeout:
        logger.warning("请求超时（预期行为）— 超时时间 1 秒")

    # 2. 自动重试机制
    session = requests.Session()
    retry_strategy = Retry(
        total=3,              # 最多重试 3 次
        backoff_factor=0.5,   # 退避因子：0.5s, 1s, 2s
        status_forcelist=[500, 502, 503, 504],  # 这些状态码触发重试
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    resp = session.get(f"{BASE_URL}/get", timeout=5)
    logger.info(f"带重试策略的请求: {resp.status_code}")
    session.close()


def demo_error_handling():
    """演示异常处理。"""
    import requests

    logger.info("--- 异常处理演示 ---")

    # 1. 连接错误
    try:
        requests.get("http://127.0.0.1:19999/nonexistent", timeout=2)
    except requests.exceptions.ConnectionError:
        logger.warning("ConnectionError: 无法连接到服务器（预期行为）")

    # 2. 超时错误
    try:
        requests.get(f"{BASE_URL}/delay", timeout=0.5)
    except requests.exceptions.Timeout:
        logger.warning("Timeout: 请求超时（预期行为）")

    # 3. HTTP 错误状态码
    try:
        resp = requests.get(f"{BASE_URL}/status/404", timeout=5)
        resp.raise_for_status()  # 4xx/5xx 会抛出 HTTPError
    except requests.exceptions.HTTPError as e:
        logger.warning(f"HTTPError: {e}（预期行为）")

    # 4. 通用异常捕获
    try:
        requests.get(f"{BASE_URL}/get", timeout=5)
        logger.info("通用异常捕获: 请求成功")
    except requests.exceptions.RequestException as e:
        logger.error(f"请求失败: {e}")


def main():
    """主函数：启动模拟服务器并运行所有演示。"""
    print("=" * 60)
    print("  HTTP 基础与 requests 库演示")
    print("  使用本地模拟服务器，无需外部网络")
    print("=" * 60)

    # 启动本地模拟服务器
    server = start_mock_server(port=18080)

    try:
        demo_get_request()
        print()
        demo_post_request()
        print()
        demo_session()
        print()
        demo_timeout_retry()
        print()
        demo_error_handling()
    finally:
        server.shutdown()
        logger.info("模拟服务器已关闭")

    print("\n✅ 所有演示完成！")


if __name__ == "__main__":
    main()
