import pytest

from rational import *

def R(p: int, q: int) -> Rational:
    """Construct a Rational with the given p, q.

    This is an alias of Rational(p, q), to reduce the visual noise in tests.

    As basic safety, this function asserts that q > 0, but it does not assert
    that p and q are mutually prime.
    """
    assert q > 0
    return Rational(p, q)

def test_frac_to_str() -> None:
    assert frac_to_str(R(0, 1)) == "0"
    assert frac_to_str(R(5, 1)) == "5"
    assert frac_to_str(R(-6, 1)) == "-6"

    assert frac_to_str(R(5, 6)) == "5/6"
    assert frac_to_str(R(-5, 8)) == "-5/8"

def test_reduce() -> None:
    assert reduce(5, 7) == R(5, 7)
    assert reduce(6, 30) == R(1, 5)
    assert reduce(20, 24) == R(5, 6)
    assert reduce(7, 7) == R(1, 1)

    assert reduce(0, 33) == R(0, 1)

    assert reduce(-3, 7) == R(-3, 7)
    assert reduce(3, -7) == R(-3, 7)
    assert reduce(-3, -7) == R(3, 7)

    assert reduce(20, -24) == R(-5, 6)

def test_add() -> None:
    assert add(R(1, 2), R(-3, 5)) == R(-1, 10)
    assert add(R(2, 1), R(-3, 5)) == R(7, 5)
    assert add(R(2, 1), R(2, 1)) == R(4, 1)

def test_subtract() -> None:
    assert subtract(R(1, 2), R(-3, 5)) == R(11, 10)
    assert subtract(R(2, 1), R(-3, 5)) == R(13, 5)
    assert subtract(R(-3, 5), R(-3, 5)) == R(0, 1)

def test_multiply() -> None:
    assert multiply(R(1, 2), R(-3, 5)) == R(-3, 10)
    assert multiply(R(2, 1), R(-3, 5)) == R(-6, 5)
    assert multiply(R(-3, 5), R(-3, 5)) == R(9, 25)

def test_divide() -> None:
    assert divide(R(1, 2), R(-3, 5)) == R(-5, 6)
    assert divide(R(2, 1), R(-3, 5)) == R(-10, 3)
    assert divide(R(-3, 5), R(-3, 5)) == R(1, 1)

    # We had to look up things on the Web to come up with this:
    with pytest.raises(ValueError):
        divide(R(5, 2), R(0, 1))
