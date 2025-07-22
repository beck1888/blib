"""
number_theory.py

A collection of number theory algorithms for use in math-heavy or cryptographic tasks.
Includes utilities for primes, factorization, modular arithmetic, and more.

Functions:
    gcd(a, b): Computes the greatest common divisor of two integers.
    lcm(a, b): Computes the least common multiple of two integers.
    is_prime(n): Checks if a number is prime.
    sieve(n): Generates a list of prime numbers up to a given number.
    factorize(n): Returns all factors of a number.
    prime_factors(n): Returns the prime factorization of a number.
    modinv(a, m): Computes the modular inverse of a number.
    extended_gcd(a, b): Computes the extended Euclidean algorithm.
    fast_exp(base, exp, mod): Performs fast exponentiation with optional modular arithmetic.
"""

def gcd(a: int, b: int) -> int:
    """
    Computes the greatest common divisor (GCD) of two integers using the Euclidean algorithm.

    Args:
        a (int): The first integer.
        b (int): The second integer.

    Returns:
        int: The greatest common divisor of a and b.
    """
    while b:
        a, b = b, a % b
    return a

def lcm(a: int, b: int) -> int:
    """
    Computes the least common multiple (LCM) of two integers.

    Args:
        a (int): The first integer.
        b (int): The second integer.

    Returns:
        int: The least common multiple of a and b, or 0 if either input is 0.
    """
    return abs(a * b) // gcd(a, b) if a and b else 0

def is_prime(n: int) -> bool:
    """
    Checks if a number is prime using basic trial division.

    Args:
        n (int): The number to check.

    Returns:
        bool: True if n is prime, False otherwise.
    """
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
    """
    Generates a list of prime numbers up to and including a given number using the Sieve of Eratosthenes.

    Args:
        n (int): The upper limit for generating prime numbers.

    Returns:
        list[int]: A list of prime numbers up to n.
    """
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
    """
    Returns a list of all factors of a positive integer.

    Args:
        n (int): The number to factorize. Must be a positive integer.

    Returns:
        list[int]: A sorted list of all factors of n.

    Raises:
        ValueError: If n is not a positive integer.
    """
    if n <= 0:
        raise ValueError("Input must be a positive integer.")
    factors = set()
    for i in range(1, int(n**0.5) + 1):
        if n % i == 0:
            factors.add(i)
            factors.add(n // i)
    return sorted(factors)

def prime_factors(n: int) -> list[int]:
    """
    Returns the prime factorization of a number as a list.

    Args:
        n (int): The number to factorize into prime factors.

    Returns:
        list[int]: A list of prime factors of n.
    """
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
    """
    Computes the modular inverse of a number modulo m using the extended Euclidean algorithm.

    Args:
        a (int): The number to find the modular inverse for.
        m (int): The modulus.

    Returns:
        int: The modular inverse of a modulo m.

    Raises:
        ValueError: If the modular inverse does not exist (i.e., gcd(a, m) != 1).
    """
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        raise ValueError(f"Modular inverse does not exist for a={a}, m={m}")
    return x % m

def extended_gcd(a: int, b: int) -> tuple[int, int, int]:
    """
    Computes the extended Euclidean algorithm.

    Args:
        a (int): The first integer.
        b (int): The second integer.

    Returns:
        tuple[int, int, int]: A tuple (gcd, x, y) such that gcd is the greatest common divisor of a and b,
                              and x, y satisfy the equation ax + by = gcd.
    """
    if b == 0:
        return (a, 1, 0)
    g, x1, y1 = extended_gcd(b, a % b)
    return (g, y1, x1 - (a // b) * y1)

def fast_exp(base: int, exp: int, mod: int | None = None) -> int:
    """
    Performs fast exponentiation by squaring, with optional modular arithmetic.

    Args:
        base (int): The base number.
        exp (int): The exponent.
        mod (int | None, optional): The modulus for modular exponentiation. Defaults to None.

    Returns:
        int: The result of base raised to the power exp, optionally modulo mod.
    """
    result = 1
    base = base % mod if mod else base
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod if mod else result * base
        base = (base * base) % mod if mod else base * base
        exp //= 2
    return result