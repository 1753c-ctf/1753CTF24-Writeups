#!/usr/bin/env python3

from taco import taco
import struct

with open('taco/encrypted', 'r') as f:
    ct = f.read()
ct = bytes.fromhex(ct)
pt_start = 'THIS IS A REALLY IMPORTANT MESSAGE, TOP SECRET, DESTROY AFTER RECEIVING: '[:64].encode()

keystream_first_block = taco.xor_bytes(ct, pt_start)

def rev_rotl(x, n):
    return ((x >> n) | (x << (32 - n))) & 0xffffffff

def rev_quarterround(state, indexes):
    state[indexes[0]] ^= taco.rotl(
        (state[indexes[3]] + state[indexes[2]]) & 0xffffffff, 18)
    state[indexes[3]] ^= taco.rotl(
        (state[indexes[2]] + state[indexes[1]]) & 0xffffffff, 13)
    state[indexes[2]] ^= taco.rotl(
        (state[indexes[1]] + state[indexes[0]]) & 0xffffffff, 9)
    state[indexes[1]] ^= taco.rotl(
        (state[indexes[0]] + state[indexes[3]]) & 0xffffffff, 7)

def rev_columnround(state):
    rev_quarterround(state, [15, 3, 7, 11])
    rev_quarterround(state, [10, 14, 2, 6])
    rev_quarterround(state, [5, 9, 13, 1])
    rev_quarterround(state, [0, 4, 8, 12])

def rev_rowround(state):
    rev_quarterround(state, [15, 12, 13, 14])
    rev_quarterround(state, [10, 11, 8, 9])
    rev_quarterround(state, [5, 6, 7, 4])
    rev_quarterround(state, [0, 1, 2, 3])

def rev_doubleround(state):
    rev_rowround(state)
    rev_columnround(state)

def rev_almost_salsa20_block(block):
    state = list(struct.unpack("<" + 'I' * 16, block))

    for i in range(10):
        rev_doubleround(state)

    key = struct.pack('<' + 'I' * 8, *state[1:5], *state[11:15])
    expansion = struct.pack('<' + 'I' * 4, state[0], state[5], state[10], state[15])
    nonce = struct.pack('<' + 'I' * 2, *state[6:8])
    counter = struct.pack('<' + 'I' * 2, *state[8:10])

    assert(expansion == b'expand 32-byte k')

    return (key, nonce, counter)

def genric_rev_test(forward_func, input, rev_func):
    output = forward_func(*input)
    rev = rev_func(output)
    assert(len(input) == len(rev))
    for in_element, out_element in zip(input, rev):
        assert(in_element == out_element)

def rev_inplace_transformation_test(forward_func, state, additional_args, rev_func):
    orig_state = state[:]
    if additional_args:
        forward_func(state, *additional_args)
        rev_func(state, *additional_args)
    else:
        forward_func(state)
        rev_func(state)
    assert(state == orig_state)

# def test_salsa_reverse_block():
#     key = b'01234567890123456789012345678901'
#     nonce = b'abcdABCD'
#     counter = b'00110022'
#     block = taco.salsa20_block(key, nonce, counter)
#     r_key, r_nonce, r_counter = almost_salsa20_block_reverse(block)
#     assert(r_key == key)
#     assert(r_nonce == nonce)
#     assert(r_counter == counter)

def test_rotl(x, n):
    out = taco.rotl(x, n)
    rev = rev_rotl(out, n)
    assert(rev == x)

def test():
    test_rotl(0x12345678, 7)
    rev_inplace_transformation_test(taco.quarterround, list(range(16)), [[0, 1, 2, 3]], rev_quarterround)
    rev_inplace_transformation_test(taco.quarterround, list(range(16)), [[0, 4, 8, 12]], rev_quarterround)
    rev_inplace_transformation_test(taco.columnround, list(range(16)), None, rev_columnround)
    rev_inplace_transformation_test(taco.rowround, list(range(16)), None, rev_rowround)
    rev_inplace_transformation_test(taco.doubleround, list(range(16)), None, rev_doubleround)
    genric_rev_test(taco.salsa20_block, [b'01234567890123456789012345678901', b'abcdABCD', b'00110022'], rev_almost_salsa20_block)
    print('test ok')

test()

stuff = rev_almost_salsa20_block(keystream_first_block)
print(stuff)
