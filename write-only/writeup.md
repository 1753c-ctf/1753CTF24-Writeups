# Write Only

## Challenge Description
The flag is there. But that doesn't mean you'll be able to see it.

`nc 147.78.1.47 40183`

## Initial Analysis
The challenge provides a netcat command to connect to a server that allows users to execute arbitrary code. Upon analyzing the provided code, we notice that the server reads the flag into a memory region mapped with `PROT_WRITE` protection, which suggests that the flag is write-only and cannot be directly read.

Additionally, the server implements a seccomp filter that restricts the allowed system calls to only `write`, `exit`, and `exit_group`. This means that any code executed on the server will be limited to these system calls.

## Approach
1. Analyze the provided code to understand how the flag is loaded into memory and how the user-provided code is executed.
2. Observe that the flag is loaded into a memory region mapped with `PROT_WRITE` protection, which implies that it is write-only.
3. Realize that on x86_64 architecture, `PROT_WRITE` implies `PROT_READ`, meaning that the flag can actually be read from the memory region.
4. Craft a shellcode that reads the flag from the memory region and writes it to the standard output using the allowed `write` system call.
5. Send the shellcode to the server for execution and retrieve the flag from the output.

## Exploiting the Vulnerability
The solve.py script does the following:
1. Connects to the server using the provided netcat command.
2. Constructs a shellcode that performs the following actions:
   - Moves the file descriptor for standard output (1) into the `rdi` register.
   - Moves the address of the flag (stored in `rax` by the server) into the `rsi` register.
   - Moves the count of bytes to write (0x80) into the `rdx` register.
   - Moves the system call number for `write` (1) into the `rax` register.
   - Invokes the `write` system call to write the flag to standard output.
   - Moves the system call number for `exit` (60) into the `rax` register.
   - Invokes the `exit` system call to terminate the program.
3. Sends the shellcode to the server for execution.
4. Interacts with the server to retrieve the flag from the output.

The key points of the exploit are:
- On x86_64 architecture, `PROT_WRITE` implies `PROT_READ`, meaning that a memory region mapped with `PROT_WRITE` protection can actually be read.
- The server loads the flag into a memory region and passes its address to the user-provided code in the `rax` register.
- The shellcode reads the flag from the memory region using the address in `rax` and writes it to standard output using the `write` system call.

## Obtaining the Flag
1. Run the solve.py script.
2. The script will connect to the server and send the shellcode.
3. The server will execute the shellcode, which reads the flag from memory and writes it to standard output.
4. The flag will be displayed in the output of the script.

Flag: `1753c{yes_its_write_only_but_you_can_read_it_too}`

### Conclusion
This challenge demonstrates that the concept of write-only memory, despite it's usefulness, is not enforced on x86_64 architecture. Even though the flag is loaded into a memory region mapped with `PROT_WRITE` protection, it can still be read because `PROT_WRITE` implies `PROT_READ`.

The exploit takes advantage of this fact by crafting a shellcode that reads the flag from the memory region using the address provided by the server and writes it to standard output using the allowed `write` system call.

The challenge highlights the importance of understanding the underlying architecture and memory protection mechanisms when implementing security measures. It also emphasizes the need to be cautious when assuming that certain memory regions are truly write-only or read-only.
