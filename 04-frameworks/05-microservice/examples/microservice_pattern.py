#!/usr/bin/env python3
"""
微服务通信模式模拟

模块: 04-框架与架构
知识点: 微服务架构
Python 版本: >= 3.9
最后验证: 2025-07-15

运行方式:
    python microservice_pattern.py

描述:
    使用 Python 标准库模拟微服务核心模式：
    1. 服务注册与发现
    2. HTTP 服务间调用
    3. 简单负载均衡（轮询）
    4. 断路器模式（Circuit Breaker）
    5. 重试机制
    不依赖外部服务，纯 Python 实现
"""

import json
import random
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any
from urllib.request import Request, urlopen
from urllib.error import URLError


# ============================================================
# 1. 服务注册与发现
# ============================================================

@dataclass
class ServiceInstance:
    """服务实例"""
    name: str
    host: str
    port: int
    metadata: dict = field(default_factory=dict)

    @property
    def url(self) -> str:
        return f"http://{self.host}:{self.port}"


class ServiceRegistry:
    """
    服务注册中心 — 对标 Java Eureka / Consul
    管理所有微服务实例的注册和发现
    """

    def __init__(self):
        self._services: dict[str, list[ServiceInstance]] = {}

    def register(self, instance: ServiceInstance):
        """注册服务实例"""
        if instance.name not in self._services:
            self._services[instance.name] = []
        self._services[instance.name].append(instance)
        print(f"  [注册中心] 注册: {instance.name} -> {instance.url}")

    def deregister(self, instance: ServiceInstance):
        """注销服务实例"""
        if instance.name in self._services:
            self._services[instance.name] = [
                s for s in self._services[instance.name]
                if s.url != instance.url
            ]

    def discover(self, service_name: str) -> list[ServiceInstance]:
        """发现服务实例列表"""
        return self._services.get(service_name, [])

    def list_all(self) -> dict[str, int]:
        """列出所有已注册服务"""
        return {name: len(instances) for name, instances in self._services.items()}


# ============================================================
# 2. 负载均衡器
# ============================================================

class LoadBalancer:
    """
    轮询负载均衡器 — 对标 Java Ribbon / Spring Cloud LoadBalancer
    """

    def __init__(self, registry: ServiceRegistry):
        self._registry = registry
        self._counters: dict[str, int] = {}

    def choose(self, service_name: str) -> ServiceInstance | None:
        """轮询选择一个服务实例"""
        instances = self._registry.discover(service_name)
        if not instances:
            return None

        if service_name not in self._counters:
            self._counters[service_name] = 0

        index = self._counters[service_name] % len(instances)
        self._counters[service_name] += 1
        return instances[index]


# ============================================================
# 3. 断路器模式
# ============================================================

class CircuitState(Enum):
    CLOSED = "CLOSED"        # 正常状态，请求正常通过
    OPEN = "OPEN"            # 熔断状态，请求直接失败
    HALF_OPEN = "HALF_OPEN"  # 半开状态，允许少量请求试探


class CircuitBreaker:
    """
    断路器 — 对标 Java Resilience4j / Hystrix
    防止故障服务拖垮整个系统
    """

    def __init__(self, failure_threshold: int = 3, recovery_timeout: float = 5.0):
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.last_failure_time = 0.0

    def call(self, func, *args, **kwargs) -> Any:
        """通过断路器执行调用"""
        if self.state == CircuitState.OPEN:
            if time.time() - self.last_failure_time > self.recovery_timeout:
                self.state = CircuitState.HALF_OPEN
                print(f"    [断路器] 状态: OPEN -> HALF_OPEN（尝试恢复）")
            else:
                raise ConnectionError("断路器已打开，请求被拒绝")

        try:
            result = func(*args, **kwargs)
            if self.state == CircuitState.HALF_OPEN:
                self.state = CircuitState.CLOSED
                self.failure_count = 0
                print(f"    [断路器] 状态: HALF_OPEN -> CLOSED（恢复正常）")
            return result
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = time.time()
            if self.failure_count >= self.failure_threshold:
                self.state = CircuitState.OPEN
                print(f"    [断路器] 状态: -> OPEN（连续失败 {self.failure_count} 次）")
            raise


# ============================================================
# 4. 模拟微服务
# ============================================================

class MockService:
    """模拟微服务（不启动真实 HTTP 服务器）"""

    def __init__(self, name: str, fail_rate: float = 0.0):
        self.name = name
        self.fail_rate = fail_rate

    def handle_request(self, endpoint: str, data: dict | None = None) -> dict:
        """处理请求"""
        # 模拟随机故障
        if random.random() < self.fail_rate:
            raise ConnectionError(f"{self.name} 服务暂时不可用")

        time.sleep(0.01)  # 模拟网络延迟

        if endpoint == "/health":
            return {"status": "UP", "service": self.name}
        elif endpoint == "/api/users":
            return {"users": [{"id": 1, "name": "张三"}, {"id": 2, "name": "李四"}]}
        elif endpoint == "/api/orders":
            return {"orders": [{"id": 101, "amount": 99.9}]}
        else:
            return {"error": "Not Found"}


class ServiceClient:
    """
    服务间调用客户端 — 对标 Java Feign Client
    集成服务发现、负载均衡、断路器
    """

    def __init__(self, lb: LoadBalancer):
        self._lb = lb
        self._breakers: dict[str, CircuitBreaker] = {}
        self._mock_services: dict[str, MockService] = {}

    def register_mock(self, name: str, service: MockService):
        """注册模拟服务（用于演示）"""
        self._mock_services[name] = service

    def call(self, service_name: str, endpoint: str,
             data: dict | None = None, retries: int = 2) -> dict:
        """
        调用远程服务
        包含：服务发现 -> 负载均衡 -> 断路器 -> 重试
        """
        if service_name not in self._breakers:
            self._breakers[service_name] = CircuitBreaker()

        breaker = self._breakers[service_name]
        last_error = None

        for attempt in range(retries + 1):
            instance = self._lb.choose(service_name)
            if not instance:
                raise ConnectionError(f"服务 {service_name} 无可用实例")

            try:
                mock = self._mock_services.get(service_name)
                if mock:
                    result = breaker.call(mock.handle_request, endpoint, data)
                else:
                    result = breaker.call(self._http_call, instance.url + endpoint)
                return result
            except ConnectionError as e:
                last_error = e
                if attempt < retries:
                    print(f"    [重试] {service_name} 第 {attempt + 1} 次失败，重试中...")
                    time.sleep(0.1 * (attempt + 1))

        raise last_error or ConnectionError("调用失败")

    @staticmethod
    def _http_call(url: str) -> dict:
        """实际 HTTP 调用（生产环境使用）"""
        req = Request(url, headers={"Content-Type": "application/json"})
        with urlopen(req, timeout=5) as resp:
            return json.loads(resp.read().decode())


# ============================================================
# 演示
# ============================================================

def demo_service_discovery():
    """服务注册与发现演示"""
    print("=" * 55)
    print("1. 服务注册与发现")
    print("=" * 55)

    registry = ServiceRegistry()

    # 注册服务实例
    registry.register(ServiceInstance("user-service", "10.0.0.1", 8001))
    registry.register(ServiceInstance("user-service", "10.0.0.2", 8001))
    registry.register(ServiceInstance("order-service", "10.0.0.3", 8002))

    print(f"  已注册服务: {registry.list_all()}")

    instances = registry.discover("user-service")
    print(f"  user-service 实例: {[i.url for i in instances]}\n")

    return registry


def demo_load_balancing(registry: ServiceRegistry):
    """负载均衡演示"""
    print("=" * 55)
    print("2. 负载均衡（轮询）")
    print("=" * 55)

    lb = LoadBalancer(registry)

    for i in range(4):
        instance = lb.choose("user-service")
        if instance:
            print(f"  第 {i + 1} 次请求 -> {instance.url}")

    print()
    return lb


def demo_circuit_breaker():
    """断路器模式演示"""
    print("=" * 55)
    print("3. 断路器模式")
    print("=" * 55)

    breaker = CircuitBreaker(failure_threshold=3, recovery_timeout=1.0)
    call_count = 0

    def unreliable_call():
        nonlocal call_count
        call_count += 1
        if call_count <= 4:
            raise ConnectionError("服务不可用")
        return {"status": "ok"}

    # 连续失败触发熔断
    for i in range(5):
        try:
            result = breaker.call(unreliable_call)
            print(f"  调用 {i + 1}: 成功 -> {result}")
        except ConnectionError as e:
            print(f"  调用 {i + 1}: 失败 -> {e}")

    # 等待恢复
    print("  等待断路器恢复...")
    time.sleep(1.1)
    call_count = 10  # 模拟服务恢复

    try:
        result = breaker.call(unreliable_call)
        print(f"  恢复调用: 成功 -> {result}")
    except ConnectionError as e:
        print(f"  恢复调用: 失败 -> {e}")

    print()


def demo_service_call():
    """完整服务间调用演示"""
    print("=" * 55)
    print("4. 完整服务间调用（发现+均衡+断路器+重试）")
    print("=" * 55)

    registry = ServiceRegistry()
    registry.register(ServiceInstance("user-service", "10.0.0.1", 8001))
    registry.register(ServiceInstance("order-service", "10.0.0.2", 8002))

    lb = LoadBalancer(registry)
    client = ServiceClient(lb)

    # 注册模拟服务
    client.register_mock("user-service", MockService("user-service", fail_rate=0.0))
    client.register_mock("order-service", MockService("order-service", fail_rate=0.3))

    # 调用用户服务
    try:
        result = client.call("user-service", "/api/users")
        print(f"  用户服务响应: {result}")
    except ConnectionError as e:
        print(f"  用户服务失败: {e}")

    # 调用订单服务（可能失败，会触发重试）
    for i in range(3):
        try:
            result = client.call("order-service", "/api/orders", retries=2)
            print(f"  订单服务响应 [{i + 1}]: {result}")
        except ConnectionError as e:
            print(f"  订单服务失败 [{i + 1}]: {e}")

    print()


# ============================================================
# 主函数
# ============================================================

def main():
    """运行所有微服务模式演示"""
    print("微服务通信模式演示\n")

    registry = demo_service_discovery()
    demo_load_balancing(registry)
    demo_circuit_breaker()
    demo_service_call()

    print("=" * 55)
    print("模式对照:")
    print("  ServiceRegistry  ↔ Eureka / Consul")
    print("  LoadBalancer     ↔ Ribbon / Spring Cloud LB")
    print("  CircuitBreaker   ↔ Resilience4j / Hystrix")
    print("  ServiceClient    ↔ Feign Client")
    print("=" * 55)


if __name__ == "__main__":
    main()
