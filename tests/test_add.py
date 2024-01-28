def add(a: int, b: int) -> int:
    return a + b


def sub(a: int, b: int) -> int:
    return a - b


def test_add():
    assert add(2, 3) == 5


def test_sub():
    assert sub(2, 3) == -1
