#!/usr/bin/env python3
"""
pytest 单元测试完整演示

模块: 02-常用功能
知识点: 单元测试
Python 版本: >= 3.9
最后验证: 2025-07-15

运行方式:
    pytest test_demo.py -v

描述:
    演示 pytest 的核心功能：
    1. 基本断言（assert）
    2. 参数化测试（@pytest.mark.parametrize）
    3. 异常测试（pytest.raises）
    4. fixture（测试前置/后置）
    5. mock（unittest.mock）
    6. 近似比较（pytest.approx）
    7. 临时文件（tmp_path）
"""

import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime


# ============================================================
# 被测试的函数（通常在单独的模块中）
# ============================================================

def add(a: int, b: int) -> int:
    """加法"""
    return a + b


def divide(a: float, b: float) -> float:
    """除法，除数为零时抛出异常"""
    if b == 0:
        raise ZeroDivisionError("除数不能为零")
    return a / b


def parse_age(value: str) -> int:
    """解析年龄字符串，无效输入抛出 ValueError"""
    age = int(value)
    if age < 0 or age > 150:
        raise ValueError(f"年龄无效: {age}")
    return age


class User:
    """简单的用户类"""

    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    def greet(self) -> str:
        return f"你好，我是 {self.name}，今年 {self.age} 岁"

    def is_adult(self) -> bool:
        return self.age >= 18


def fetch_user_data(user_id: int) -> dict:
    """模拟 API 调用（实际会发 HTTP 请求）"""
    import requests
    response = requests.get(f"https://api.example.com/users/{user_id}")
    return response.json()


def get_greeting() -> str:
    """返回基于当前时间的问候语"""
    hour = datetime.now().hour
    if hour < 12:
        return "早上好"
    elif hour < 18:
        return "下午好"
    else:
        return "晚上好"


# ============================================================
# 1. 基本断言
# ============================================================

def test_add():
    """最简单的测试：直接用 assert"""
    assert add(2, 3) == 5
    assert add(0, 0) == 0
    assert add(-1, 1) == 0


def test_string_operations():
    """字符串操作断言"""
    s = "Hello, Python!"
    assert s.startswith("Hello")
    assert "Python" in s
    assert s.lower() == "hello, python!"
    assert len(s) == 14


def test_list_operations():
    """列表操作断言"""
    items = [1, 2, 3, 4, 5]
    assert len(items) == 5
    assert 3 in items
    assert items[0] == 1
    assert sorted([3, 1, 2]) == [1, 2, 3]


# ============================================================
# 2. 参数化测试
# ============================================================

@pytest.mark.parametrize("a, b, expected", [
    (1, 1, 2),
    (2, 3, 5),
    (-1, 1, 0),
    (0, 0, 0),
    (100, -100, 0),
])
def test_add_parametrize(a, b, expected):
    """参数化测试：一组数据运行同一个测试
    类似 JUnit 5 的 @ParameterizedTest + @CsvSource
    """
    assert add(a, b) == expected


# ============================================================
# 3. 异常测试
# ============================================================

def test_divide_by_zero():
    """验证除零时抛出 ZeroDivisionError"""
    with pytest.raises(ZeroDivisionError, match="除数不能为零"):
        divide(1, 0)


def test_value_error():
    """验证无效输入抛出 ValueError"""
    with pytest.raises(ValueError):
        parse_age("-5")

    with pytest.raises(ValueError):
        parse_age("200")

    with pytest.raises(ValueError):
        parse_age("abc")  # int() 转换失败


# ============================================================
# 4. Fixture
# ============================================================

@pytest.fixture
def sample_user():
    """fixture：提供测试用的 User 对象
    类似 JUnit 的 @BeforeEach
    """
    return User(name="张三", age=25)


@pytest.fixture
def user_list():
    """fixture：提供测试用的用户列表"""
    return [
        User("张三", 25),
        User("李四", 17),
        User("王五", 30),
    ]


def test_with_fixture(sample_user):
    """使用 fixture 提供的测试数据"""
    assert sample_user.name == "张三"
    assert sample_user.is_adult() is True
    assert sample_user.greet() == "你好，我是 张三，今年 25 岁"


def test_user_creation(user_list):
    """使用 fixture 提供的用户列表"""
    assert len(user_list) == 3
    adults = [u for u in user_list if u.is_adult()]
    assert len(adults) == 2


# ============================================================
# 5. Mock
# ============================================================

def test_mock_api_call():
    """Mock 外部 API 调用
    类似 Java Mockito 的 when(...).thenReturn(...)
    """
    mock_response = MagicMock()
    mock_response.json.return_value = {"id": 1, "name": "张三", "age": 25}

    with patch("requests.get", return_value=mock_response) as mock_get:
        result = fetch_user_data(1)

        # 验证返回值
        assert result["name"] == "张三"
        assert result["age"] == 25

        # 验证调用参数
        mock_get.assert_called_once_with("https://api.example.com/users/1")


def test_mock_datetime():
    """Mock datetime 控制时间"""
    # 模拟早上 9 点
    mock_now = MagicMock(return_value=datetime(2025, 7, 15, 9, 0, 0))
    with patch("datetime.datetime") as mock_dt:
        mock_dt.now = mock_now
        # 直接测试逻辑
        hour = mock_now().hour
        assert hour == 9


# ============================================================
# 6. 近似比较
# ============================================================

def test_approx():
    """浮点数近似比较 — 避免精度问题"""
    # ✗ 直接比较可能失败
    # assert 0.1 + 0.2 == 0.3  # 可能失败！

    # ✓ 使用 pytest.approx
    assert 0.1 + 0.2 == pytest.approx(0.3)
    assert divide(1, 3) == pytest.approx(0.3333, rel=1e-3)


# ============================================================
# 7. 临时文件（内置 fixture）
# ============================================================

def test_tmp_path(tmp_path):
    """使用 pytest 内置的 tmp_path fixture 创建临时文件"""
    # tmp_path 是 pathlib.Path 对象，指向临时目录
    test_file = tmp_path / "test.txt"
    test_file.write_text("Hello, pytest!", encoding="utf-8")

    assert test_file.exists()
    assert test_file.read_text(encoding="utf-8") == "Hello, pytest!"


# ============================================================
# 直接运行支持（展示测试结果）
# ============================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
