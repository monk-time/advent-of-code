import itertools as it
from functools import reduce
from math import floor, sqrt
from operator import mul


def prime_powers_decomp(n):
    """Generate arrays of powers of prime divisors that divide n.

    220 -> [1, 2, 4], [1, 5], [1, 11]
    """
    if n <= 1:
        yield [1]
        raise StopIteration
    # check powers of 2
    powers, cur_pow = [1], 1
    while n % 2 == 0:
        cur_pow *= 2
        powers.append(cur_pow)
        n //= 2
    if powers:
        yield powers
    # check odd divisors
    factor = 3
    max_factor = floor(sqrt(n))
    while n > 1 and factor <= max_factor:
        if n % factor == 0:
            powers, cur_pow = [1, factor], factor
            n = n // factor
            while n % factor == 0:
                cur_pow *= factor
                powers.append(cur_pow)
                n = n // factor
            yield powers
            max_factor = floor(sqrt(n))
        factor += 2
    if n > 1:
        yield [1, n]


def mul_iter(iterable) -> int:
    return reduce(mul, iterable)


def divisors(n) -> list:
    """Return a list of all divisors of n.

    220 -> [1, 2, 4, 5, 10, 11, 20, 22, 44, 55, 110, 220]
    """
    return sorted(map(mul_iter, it.product(*prime_powers_decomp(n))))


def presents_1(n):
    return sum(divisors(n)) * 10


cache = {}

HOUSE_LIMIT = 50


def sum_of_underused_divisors(n):
    divs = divisors(n)
    for d in divs:
        if d not in cache:
            cache[d] = 1
        else:
            cache[d] += 1
    return sum(d for d in divs if cache[d] <= HOUSE_LIMIT)


def presents_2(n):
    return sum_of_underused_divisors(n) * 11


def first_house_with(n, houses):
    return next(it.dropwhile(lambda x: houses(x) < n, it.count(1)))


if __name__ == '__main__':
    import time

    start_time = time.time()
    print(first_house_with(29000000, presents_1))
    print(first_house_with(29000000, presents_2))
    print(f'--- {time.time() - start_time:.2f} seconds ---')
