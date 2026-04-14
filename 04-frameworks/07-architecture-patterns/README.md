# 项目架构模式：MVC / 分层架构 / DDD

> **模块：** 04-框架与架构
> **难度：** 高级
> **前置知识：** Python 基础、Web 框架、ORM
> **Python 版本：** >= 3.9
> **最后验证日期：** 2025-07-15

## 概念说明

项目架构模式决定了代码的组织方式和职责划分。Python 项目中常用的三种架构模式：

- **MVC 模式** — Django 的 MTV（Model-Template-View）是 MVC 的变体。对标 Java Spring MVC。
- **分层架构** — Controller-Service-Repository 三层分离，职责清晰。对标 Java Spring Boot 标准分层。
- **DDD（领域驱动设计）** — 以业务领域为核心组织代码，适合复杂业务系统。对标 Java DDD 实践。

## Java 对比

| 架构模式 | Python 实践 | Java 实践 | 适用场景 |
|----------|------------|-----------|----------|
| **MVC** | Django MTV | Spring MVC | 全栈 Web 应用 |
| **分层架构** | FastAPI + 手动分层 | Spring Boot 标准分层 | REST API 服务 |
| **DDD** | 手动实现 | Spring + DDD | 复杂业务系统 |

**Java Spring MVC 分层：**
```java
// Controller 层
@RestController
public class UserController {
    @Autowired private UserService userService;

    @GetMapping("/users/{id}")
    public User getUser(@PathVariable Long id) {
        return userService.findById(id);
    }
}

// Service 层
@Service
public class UserService {
    @Autowired private UserRepository userRepository;

    public User findById(Long id) {
        return userRepository.findById(id).orElseThrow();
    }
}

// Repository 层
@Repository
public interface UserRepository extends JpaRepository<User, Long> {}
```

**Python FastAPI 分层：**
```python
# controller (router)
@router.get("/users/{user_id}")
def get_user(user_id: int, service: UserService = Depends()):
    return service.find_by_id(user_id)

# service
class UserService:
    def __init__(self, repo: UserRepository = Depends()):
        self.repo = repo

    def find_by_id(self, user_id: int) -> User:
        user = self.repo.get(user_id)
        if not user:
            raise HTTPException(404, "用户不存在")
        return user

# repository
class UserRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def get(self, user_id: int) -> User | None:
        return self.db.query(User).get(user_id)
```

## 实战代码

### 示例 1：MVC 模式（Django）

**目录：** `examples/mvc-pattern/`

Django MTV 项目结构说明。

### 示例 2：分层架构

**目录：** `examples/layered-pattern/`

Controller-Service-Repository 分层结构说明。

### 示例 3：DDD 模式

**目录：** `examples/ddd-pattern/`

领域驱动设计项目结构说明。

## 架构选型建议

| 项目类型 | 推荐架构 | 原因 |
|----------|----------|------|
| 小型 API（< 10 个端点） | 单文件 / 简单分层 | 过度设计反而增加复杂度 |
| 中型 Web 应用 | MVC（Django） | Django 天然支持 MTV |
| REST API 服务 | 分层架构 | 职责清晰，易于测试 |
| 复杂业务系统 | DDD | 业务逻辑集中，领域模型丰富 |
| 微服务 | 分层架构 / DDD | 每个服务独立架构 |

## 常见陷阱

- ⚠️ Django 的 View 对应 Java 的 Controller，Template 对应 View，不要混淆
- ⚠️ Python 没有接口（Interface），分层架构中用抽象基类（ABC）或 Protocol 替代
- ⚠️ 小项目不要过度设计，简单的模块划分就够了
- ⚠️ DDD 的核心是领域模型，不是目录结构，不要为了 DDD 而 DDD

> 💻 **完整可运行代码：** [mvc-pattern/](examples/mvc-pattern/) | [layered-pattern/](examples/layered-pattern/) | [ddd-pattern/](examples/ddd-pattern/)

## 参考资料

- [Django 项目结构最佳实践](https://docs.djangoproject.com/en/4.2/intro/reusable-apps/)
- [FastAPI 项目结构](https://fastapi.tiangolo.com/tutorial/bigger-applications/)
- [Python DDD 实践](https://www.cosmicpython.com/)
