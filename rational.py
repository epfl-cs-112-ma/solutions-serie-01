from dataclasses import dataclass

@dataclass(frozen=True)
class Rational:
    p: int
    q: int

def frac_to_str(r: Rational) -> str:
    """Formats a Rational as a string."""
    if r.q == 1:
        return f"{r.p}"
    else:
        return f"{r.p}/{r.q}"

def pgcd(a: int, b: int) -> int:
    """Computes the greatest common divisor of a and b.

    Requires: a >= b >= 0.
    """
    if b == 0:
        return a
    else:
        return pgcd(b, a % b)

def reduce(p: int, q: int) -> Rational:
    """Reduces a rational p/q into a Rational, so that p and q are mutually prime and q > 0.

    q must be non-zero.
    """
    assert q != 0
    if p == 0:
        # Normalize denominator to 1
        return Rational(0, 1)
    elif q < 0:
        # If the denominator is negative, take the opposite of both sides
        return reduce(-p, -q)
    else:
        # Now we know p != 0 and q > 0; we can normalize by the pgcd
        # Note the usage of // as we need an integer division
        # Using /, even though the division is exact (by construction),
        # results in a `float`, which is not a valid argument for `Rational.q`.
        divisor = pgcd(abs(p), q)
        return Rational(p // divisor, q // divisor)

def add(r1: Rational, r2: Rational) -> Rational:
    return reduce(
        p = r1.p * r2.q + r2.p * r1.q,
        q = r1.q * r2.q
    )

def subtract(r1: Rational, r2: Rational) -> Rational:
    return reduce(
        p = r1.p * r2.q - r2.p * r1.q,
        q = r1.q * r2.q
    )

def multiply(r1: Rational, r2: Rational) -> Rational:
    return reduce(
        p = r1.p * r2.p,
        q = r1.q * r2.q
    )

def divide(r1: Rational, r2: Rational) -> Rational:
    if r2.p == 0:
        raise ValueError("Division by zero")
    else:
        # Since our `reduce` function accepts q < 0 (and normalizes it to
        # q > 0), we do not need to separately deal with p2 < 0.
        return reduce(
            p = r1.p * r2.q,
            q = r1.q * r2.p
        )
