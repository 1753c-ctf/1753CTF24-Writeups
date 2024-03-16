# Brain Heck

## Challenge Description
Ok, jumps are quite useful sometimes, you can have them I guess

`nc 129.151.142.36 36391`

## Initial Analysis
The challenge provides a netcat command to connect to a server running a modified version of the Brainfuck compiler from the previous challenge. This time, the compiler supports jump instructions (`[` and `]`), which were not present in the previous version.

Upon analyzing the provided code, we notice that the balance of jump instructions is not checked, which means we can send code with extra `[` and create a piece of data that will be recognized as `]` to jump over the `exit()` syscall and into our shellcode.

## Approach
1. Connect to the provided IP and port using netcat.
2. Craft an exploit that leverages the lack of jump balance checking to execute arbitrary shellcode.
3. Send the exploit code to the server and obtain a shell.

## Exploiting the Vulnerability
The exploit script (solve.py) does the following:
1. Defines a shellcode that executes `/bin/sh` using the `execve()` syscall.
2. Constructs a Brainfuck code that:
   - Creates a `]` signature.
   - Moves the data pointer further to the right, to where the program will jump after detecting `]` signature.
   - Increments the data cells to write the shellcode bytes.
   - Adds an unmatched `[` instruction to jump through the `exit()` syscall and into the data region where the shellcode is located.

The key points of the exploit are:
- The `rcond_signature` variable represents the value needed to create a `]` signature in the data region.
- The `rcond_signature_to_end` variable represents the offset from the `]` signature to the end of the `]` instruction.
- The unmatched `[` instruction at the end of the Brainfuck code will cause a jump through the `exit()` syscall and into the data region where the shellcode is located.

## Obtaining the Flag
1. Connect to the provided IP and port using `nc 129.151.142.36 36391`.
2. Send the generated Brainfuck code from the exploit script to the server.
3. The shellcode will be executed, giving you a shell on the remote system.
4. Retrieve the flag from the remote system.

Flag: `1753c{jump_balance_not_checked_brain_is_a_heck}`

### Conclusion
This challenge builds upon the previous "Brain Frick" challenge and introduces jump instructions. By exploiting the lack of jump balance checking, we can construct a Brainfuck code that jumps over the `exit()` syscall and into the data region where our shellcode is located. This allows us to execute arbitrary code and obtain a shell on the remote system.

The challenge emphasizes the importance of properly validating and sanitizing user input, especially when dealing with interpreted languages or compilers. Failing to do so can lead to vulnerabilities that can be exploited to execute malicious code.