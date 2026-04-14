# 单元测试（pytest）

> **模块：** 02-常用功能
> **难度：** 入门
> **前置知识：** Python 基础（01-python-basics）
> **Python 版本：** >= 3.9
> **最后验证日期：** 2025-07-15

## 概念说明

单元测试是保证代码质量的关键技能。Python 最流行的测试框架是 **pytest**，它比标准库的 `unittest` 更简洁、更强大。对于 Java 开发者来说，pytest 类似于 JUnit 5，但不需要继承测试基类、不需要 `@Test` 注解——任何以 `test_` 开头的函数都会被自动发现和执行。

pytest 的核心特性包括：**断言（assert）** 直接使用 Python 的 `assert` 语句（而非 `assertEquals` 等方法）、**fixture** 提供测试前置/后置逻辑（类似 JUnit 的 `@BeforeEach`）、**参数化（parametrize）** 用一组数据运行同一个测试（类似 JUnit 5 的 `@ParameterizedTest`）、**mock** 替换外部依赖（类似 Mockito）。

pytest 的设计哲学是"约定优于配置"：测试文件以 `test_` 开头、测试函数以 `test_` 开头、断言用原生 `assert`，零配置即可运行。

### pytest vs unittest vs JUnit 对比

| 特性 | pytest | unittest | JUnit 5 |
|------|--------|----------|---------|
| 测试发现 | 自动（`test_` 前缀） | 自动（`test` 前缀） | `@Test` 注解 |
| 断言方式 | `assert x == y` | `self.assertEqual(x, y)` | `assertEquals(x, y)` |
| 前置逻辑 | `@pytest.fixture` | `setUp()` | `@BeforeEach` |
| 参数化 | `@pytest.mark.parametrize` | 不支持（需 subTest） | `@ParameterizedTest` |
| Mock | `unittest.mock` | `unittest.mock` | Mockito |
| 异常测试 | `pytest.raises()` | `assertRaises()` | `assertThrows()` |
| 需要类 | 否（函数即可） | 是（继承 TestCase） | 是（测试类） |
| 插件生态 | 丰富（pytest-cov 等） | 有限 | 丰富 |

### pytest 核心功能速查

| 功能 | 语法 | 说明 |
|------|------|------|
| 基本断言 | `assert result == expected` | 直接使用 Python assert |
| 近似比较 | `assert result == pytest.approx(3.14)` | 浮点数近似比较 |
| 异常测试 | `with pytest.raises(ValueError):` | 验证抛出指定异常 |
| fixture | `@pytest.fixture` | 提供测试数据或前置逻辑 |
| 参数化 | `@pytest.mark.parametrize("x,y", [...])` | 多组数据运行同一测试 |
| 跳过测试 | `@pytest.mark.skip(reason="...")` | 跳过指定测试 |
| 标记 | `@pytest.mark.slow` | 自定义标记分类 |
| 临时目录 | `tmp_path` fixture | pytest 内置临时目录 |


## Java 对比

| 特性 | Java (JUnit 5) | Python (pytest) |
|------|----------------|-----------------|
| 测试类 | 必须定义类 | 函数即可，无需类 |
| 注解/装饰器 | `@Test` | 无需装饰器（`test_` 前缀） |
| 断言 | `assertEquals(expected, actual)` | `assert actual == expected` |
| 前置 | `@BeforeEach void setUp()` | `@pytest.fixture` |
| 参数化 | `@ParameterizedTest @ValueSource` | `@pytest.mark.parametrize` |
| Mock | `@Mock` + Mockito | `unittest.mock.patch` |
| 异常 | `assertThrows(Ex.class, () -> ...)` | `with pytest.raises(Ex):` |
| 运行 | `mvn test` | `pytest` |

**Java 写法（JUnit 5）：**
```java
import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

class CalculatorTest {

    private Calculator calc;

    @BeforeEach
    void setUp() {
        calc = new Calculator();
    }

    @Test
    void testAdd() {
        assertEquals(5, calc.add(2, 3));
    }

    @ParameterizedTest
    @CsvSource({"1,1,2", "2,3,5", "-1,1,0"})
    void testAddParameterized(int a, int b, int expected) {
        assertEquals(expected, calc.add(a, b));
    }

    @Test
    void testDivideByZero() {
        assertThrows(ArithmeticException.class,
            () -> calc.divide(1, 0));
    }
}
```

**Python 写法（pytest）：**
```python
import pytest

# 无需类，函数即可
def test_add():
    assert add(2, 3) == 5

# 参数化：一行搞定
@pytest.mark.parametrize("a, b, expected", [
    (1, 1, 2), (2, 3, 5), (-1, 1, 0),
])
def test_add_parametrize(a, b, expected):
    assert add(a, b) == expected

# 异常测试
def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError):
        divide(1, 0)
```

## 实战代码

### 示例：pytest 完整演示

**文件：** `examples/test_demo.py`

演示 pytest 的核心功能：基本断言、fixture、参数化测试、mock、异常测试。

**安装依赖：**
```bash
pip install pytest
```

**运行方式：**
```bash
pytest examples/test_demo.py -v
```

**预期输出：**
```
examples/test_demo.py::test_add PASSED
examples/test_demo.py::test_string_operations PASSED
examples/test_demo.py::test_list_operations PASSED
examples/test_demo.py::test_add_parametrize[1-1-2] PASSED
examples/test_demo.py::test_add_parametrize[2-3-5] PASSED
examples/test_demo.py::test_add_parametrize[-1-1-0] PASSED
examples/test_demo.py::test_add_parametrize[0-0-0] PASSED
examples/test_demo.py::test_add_parametrize[100--100-0] PASSED
examples/test_demo.py::test_divide_by_zero PASSED
examples/test_demo.py::test_value_error PASSED
examples/test_demo.py::test_with_fixture PASSED
examples/test_demo.py::test_user_creation PASSED
examples/test_demo.py::test_mock_api_call PASSED
examples/test_demo.py::test_mock_datetime PASSED
examples/test_demo.py::test_approx PASSED
examples/test_demo.py::test_tmp_path PASSED
```

## 常见陷阱

### 1. 测试文件/函数命名不规范

pytest 默认只发现 `test_` 开头的文件和函数。

```python
# ✗ 不会被 pytest 发现
def check_add():
    assert add(1, 2) == 3

# ✓ 正确命名
def test_add():
    assert add(1, 2) == 3
```

### 2. fixture 作用域混淆

fixture 默认每个测试函数执行一次（`scope="function"`），如果初始化开销大，可以调整作用域。

```python
# 每个测试函数都会创建新的数据库连接（开销大）
@pytest.fixture
def db_conn():
    return create_connection()

# ✓ 整个模块共享一个连接
@pytest.fixture(scope="module")
def db_conn():
    conn = create_connection()
    yield conn
    conn.close()
```

### 3. Mock 后忘记恢复

使用 `unittest.mock.patch` 时，推荐用上下文管理器或装饰器，确保自动恢复。

```python
from unittest.mock import patch

# ✗ 手动 patch 容易忘记恢复
mock = patch("module.func")
mock.start()
# ... 测试 ...
mock.stop()  # 容易忘记！

# ✓ 使用上下文管理器
with patch("module.func") as mock_func:
    mock_func.return_value = 42
    # ... 测试 ...
    # 自动恢复
```

### 4. 断言消息不清晰

pytest 的 assert 会自动显示详细的失败信息，但复杂断言可以加自定义消息。

```python
# pytest 自动显示详细信息
assert result == expected
# AssertionError: assert 3 == 5

# 复杂场景可加自定义消息
assert len(users) > 0, f"用户列表不应为空，实际: {users}"
```

> 💻 **完整可运行代码：** [test_demo.py](examples/test_demo.py)

## 参考资料

- [pytest 官方文档](https://docs.pytest.org/en/stable/)
- [Python 官方文档 - unittest.mock](https://docs.python.org/zh-cn/3/library/unittest.mock.html)
- [Real Python - Testing with pytest](https://realpython.com/pytest-python-testing/)
- [pytest fixture 详解](https://docs.pytest.org/en/stable/how-to/fixtures.html)
