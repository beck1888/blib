"""
number_theory.py

A collection of number theory algorithms for use in math-heavy or cryptographic tasks.
Includes utilities for primes, factorization, modular arithmetic, and more.
"""

def gcd(a: int, b: int) -> int:
    """Computes the greatest common divisor using the Euclidean algorithm."""
    while b:
        a, b = b, a % b
    return a

def lcm(a: int, b: int) -> int:
    """Computes the least common multiple."""
    return abs(a * b) // gcd(a, b) if a and b else 0

def is_prime(n: int) -> bool:
    """Checks if a number is prime (basic trial division)."""
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def sieve(n: int) -> list[int]:
    """Returns a list of prime numbers up to and including n using Sieve of Eratosthenes."""
    if n < 2:
        return []
    prime = [True] * (n + 1)
    prime[0] = prime[1] = False
    for i in range(2, int(n**0.5) + 1):
        if prime[i]:
            for j in range(i * i, n + 1, i):
                prime[j] = False
    return [i for i, is_p in enumerate(prime) if is_p]

def factorize(n: int) -> list[int]:
    """Returns a list of all factors of a number."""
    if n <= 0:
        raise ValueError("Input must be a positive integer.")
    factors = set()
    for i in range(1, int(n**0.5) + 1):
        if n % i == 0:
            factors.add(i)
            factors.add(n // i)
    return sorted(factors)

def prime_factors(n: int) -> list[int]:
    """Returns the prime factorization of n as a list."""
    i = 2
    factors = []
    while i * i <= n:
        while n % i == 0:
            factors.append(i)
            n //= i
        i += 1
    if n > 1:
        factors.append(n)
    return factors

def modinv(a: int, m: int) -> int:
    """Returns the modular inverse of a modulo m using extended Euclidean algorithm."""
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        raise ValueError(f"Modular inverse does not exist for a={a}, m={m}")
    return x % m

def extended_gcd(a: int, b: int) -> tuple[int, int, int]:
    """Extended Euclidean algorithm. Returns (gcd, x, y) where ax + by = gcd."""
    if b == 0:
        return (a, 1, 0)
    g, x1, y1 = extended_gcd(b, a % b)
    return (g, y1, x1 - (a // b) * y1)

def fast_exp(base: int, exp: int, mod: int | None = None) -> int:
    """Fast exponentiation by squaring. Supports optional modular exponentiation."""
    result = 1
    base = base % mod if mod else base
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod if mod else result * base
        base = (base * base) % mod if mod else base * base
        exp //= 2
    return result