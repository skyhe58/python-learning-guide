# 微服务架构：gRPC / Nameko / FastAPI

> **模块：** 04-框架与架构
> **难度：** 高级
> **前置知识：** Python 基础、Web 框架、异步编程
> **Python 版本：** >= 3.9
> **最后验证日期：** 2025-07-15

## 概念说明

微服务架构将单体应用拆分为多个独立部署的小型服务，每个服务专注于单一业务功能。Python 生态中的微服务方案：

- **gRPC Python** — Google 的高性能 RPC 框架，基于 Protocol Buffers。对标 Java gRPC。
- **Nameko** — Python 微服务框架，内置 RPC、事件系统、依赖注入。
- **FastAPI 微服务模式** — 使用 FastAPI 构建 HTTP 微服务，轻量灵活。对标 Java Spring Cloud + Feign。

## Java 对比

| 特性 | gRPC Python | Nameko | FastAPI 微服务 | Java gRPC | Spring Cloud |
|------|------------|--------|---------------|-----------|-------------|
| **通信协议** | HTTP/2 + Protobuf | AMQP (RabbitMQ) | HTTP/REST | HTTP/2 + Protobuf | HTTP/REST |
| **序列化** | Protocol Buffers | JSON | JSON | Protocol Buffers | JSON |
| **服务发现** | 需要额外组件 | RabbitMQ 内置 | 需要额外组件 | 需要额外组件 | Eureka/Consul |
| **负载均衡** | 客户端负载均衡 | RabbitMQ 分发 | Nginx/Traefik | 客户端负载均衡 | Ribbon/LoadBalancer |
| **性能** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **学习曲线** | 中（需学 Protobuf） | 低 | 低 | 中 | 高 |

**Java gRPC 写法：**
```java
// 服务端
public class GreeterImpl extends GreeterGrpc.GreeterImplBase {
    @Override
    public void sayHello(HelloRequest req, StreamObserver<HelloReply> observer) {
        HelloReply reply = HelloReply.newBuilder()
            .setMessage("Hello " + req.getName())
            .build();
        observer.onNext(reply);
        observer.onCompleted();
    }
}

// 客户端
ManagedChannel channel = ManagedChannelBuilder.forAddress("localhost", 50051).build();
GreeterGrpc.GreeterBlockingStub stub = GreeterGrpc.newBlockingStub(channel);
HelloReply reply = stub.sayHello(HelloRequest.newBuilder().setName("World").build());
```

**Python gRPC 写法：**
```python
# 服务端
import grpc
from concurrent import futures

class GreeterServicer(greeter_pb2_grpc.GreeterServicer):
    def SayHello(self, request, context):
        return greeter_pb2.HelloReply(message=f"Hello {request.name}")

server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
greeter_pb2_grpc.add_GreeterServicer_to_server(GreeterServicer(), server)
server.add_insecure_port("[::]:50051")
server.start()

# 客户端
channel = grpc.insecure_channel("localhost:50051")
stub = greeter_pb2_grpc.GreeterStub(channel)
response = stub.SayHello(greeter_pb2.HelloRequest(name="World"))
```

## 实战代码

### 示例 1：微服务通信模式模拟

**文件：** `examples/microservice_pattern.py`

使用 Python 标准库模拟微服务间 HTTP 通信模式，包含服务注册、服务发现、负载均衡。

**运行方式：**
```bash
python examples/microservice_pattern.py
```

## 微服务设计原则

| 原则 | 说明 | Python 实践 |
|------|------|------------|
| 单一职责 | 每个服务只做一件事 | 一个 FastAPI 应用 = 一个服务 |
| 独立部署 | 服务可独立发布 | Docker 容器化 |
| 去中心化 | 每个服务有自己的数据库 | 每个服务独立的 SQLite/PostgreSQL |
| 容错设计 | 服务故障不影响全局 | 断路器模式、重试机制 |
| API 网关 | 统一入口 | Nginx / Kong / Traefik |

## 常见陷阱

- ⚠️ 微服务不是银弹，小型项目用单体架构更合适
- ⚠️ 服务间通信增加了网络延迟和复杂度，需要做好超时和重试
- ⚠️ 分布式事务很难处理，优先考虑最终一致性（Saga 模式）
- ⚠️ 日志和监控在微服务架构中至关重要，需要集中式日志收集

> 💻 **完整可运行代码：** [microservice_pattern.py](examples/microservice_pattern.py)

## 参考资料

- [gRPC Python 官方文档](https://grpc.io/docs/languages/python/)
- [Nameko 官方文档](https://nameko.readthedocs.io/)
- [FastAPI 官方文档](https://fastapi.tiangolo.com/)
- [微服务架构设计模式](https://microservices.io/patterns/)
