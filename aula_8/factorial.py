def factorial(n):
    """Calculate the factorial of a number recursively."""
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)
