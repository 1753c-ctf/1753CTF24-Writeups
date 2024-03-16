#!/usr/bin/env python3
# 
# there's probably a lot of ways to make a curve insecure
# here's a paper with some: https://wstein.org/edu/2010/414/projects/novotney.pdf
# here's one way way to make a curve with smooth order
# https://crypto.stanford.edu/pbc/notes/ep/cm.html
# which makes dlog easy because of pohlig-hellman

from pwn import *
from sage.all import *
from Crypto.Util.number import getPrime, isPrime, long_to_bytes

def read_point(target, str_before_point):
    target.recvuntil(str_before_point)
    challenge_line = target.recvline().decode()
    challenge_point = challenge_line.split(',')
    return [int(x) for x in challenge_point]

def gen_q(non_square_factors, bit_length, smoothness_bits):
    '''
    make a prime q such that
    q - 1 = non_square_factors * square_primes
    and all factors in square_primes have even power
    '''
    prime_count = bit_length // smoothness_bits
    prime_count //= 2
    primes = [getPrime(smoothness_bits) for _ in range(prime_count)]
    for _ in range(100):
        p = reduce(lambda acc, fac: acc * fac**2, primes, 1) * non_square_factors
        for i in range(10000):
            if isPrime(p * i**2 + 1):
                return p * i**2 + 1
        primes[0] = getPrime(smoothness_bits)

def make_smooth_order_ec(generator_order_bits, smoothness_bits):
    t=2
    D=7
    q = gen_q(D*4, generator_order_bits*2, smoothness_bits)
    print(f'{q=}')
    print(f'{factor(q-1)=}')

    k = (-3375*pow(1728+3375, -1, q))%q
    E=EllipticCurve(GF(q), [3*k, 2*k])
    if E.twists()[0].order() != q - 1:
        E = E.twists()[1]
    assert(E.order() == q - 1)
    print(f'{E=}')

    g = E.gen(0)
    print(f'{g=}')
    print(f'{g.order()=}')
    e = int(Zmod(g.order()).random_element())
    x = g*e
    l = g.discrete_log(x)
    assert(e==l)

    return E

E = make_smooth_order_ec(256, 16)
g = E.gen(0)

target = remote('127.0.0.1', 1337)

target.sendlineafter(b'p: ', str(E.base_field().order()).encode())
target.sendlineafter(b'a: ', str(E.a4()).encode())
target.sendlineafter(b'b: ', str(E.a6()).encode())
target.sendlineafter(b'g.x: ', str(E.gen(0)[0]).encode())
target.sendlineafter(b'g.y: ', str(E.gen(0)[1]).encode())
target.sendlineafter(b'n: ', str(E.gen(0).order()).encode())

challenge_point = E.point(read_point(target, b'g*x: '))

challenge = g.discrete_log(challenge_point)

target.sendlineafter(b'x?: ', str(challenge).encode())

flag_point = E.point(read_point(target, b'flag: '))

flag = g.discrete_log(flag_point)
flag = long_to_bytes(flag)

print(f'{flag=}')

target.interactive()
