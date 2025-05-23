import pytest
from factorial import factorial

@pytest.mark.parametrize("input,expected", [
    (0, 1),
    (1, 1),
    (2, 2),
    (3, 6),
    (4, 24),
    (5, 120),
    (6, 720),
])
def test_factorial(input, expected):
    assert factorial(input) == expected
