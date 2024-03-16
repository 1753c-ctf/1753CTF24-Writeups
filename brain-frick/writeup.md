# Brain Frick

## Challenge Description
Brainfuck is cool, but interpreters written in js are slow, we need performance!

`nc 140.238.91.110 36369`

## Initial Analysis
The challenge provides a netcat command to connect to a server running a Brainfuck compiler. It suggests that the compiler is optimized for performance, unlike JavaScript-based interpreters.

## Approach
1. Connect to the provided IP and port using netcat.
2. Analyze the code of the Brainfuck compiler (brainfrick.cpp) to identify any vulnerabilities.
3. Craft an exploit to leverage the identified vulnerability and gain arbitrary code execution.

## Exploiting the Vulnerability
Upon analyzing the code, we discovered that the compiler lacks bounds checking on the data pointer. By moving the data pointer to the left using the `<` instruction, we can access the compiled code region. This allows us to overwrite the `exit()` syscall at the end of the compiled code with our own shellcode.

The exploit script (solve.py) does the following:
- Defines a shellcode that executes `/bin/sh` using the `execve()` syscall.
- Moves the data pointer to the left using `<<` to reach the compiled code region.
- Overwrites the `exit()` syscall bytes (0x0F, 0x05) with `nop` instructions (0x90).
- Writes the shellcode bytes after the overwritten `exit()` syscall by moving the pointer to the right and incrementing each byte accordingly.

## Obtaining the Flag
1. Connect to the provided IP and port using `nc 140.238.91.110 36369`.
2. Copy and paste the generated Brainfuck code from the exploit script into the prompt.
3. The shellcode will be executed, giving you a shell on the remote system.
4. Retrieve the flag from the remote system.

Flag: `1753c{bounds_not_checked_brain_is_a_frick}`

### Conclusion
This challenge demonstrates the importance of proper bounds checking and memory safety in compilers and interpreters. By exploiting the lack of bounds checking on the data pointer, we were able to overwrite the compiled code and execute arbitrary shellcode, effectively breaking out of the Brainfuck sandbox.
