# None Only

## Challenge Description
TOUCHING THE FLAG STRICTLY FORBIDDEN

`nc 146.235.38.234 46089`

## Initial Analysis
The challenge provides a netcat command to connect to a server that allows users to execute arbitrary code. Upon analyzing the provided code, we notice that the server reads the flag into a memory region and then changes the protection of that region to `PROT_NONE`, making it inaccessible for reading or writing.

Additionally, the server implements a seccomp filter that restricts the allowed system calls to only `write`, `exit`, and `exit_group`. This means that any code executed on the server will be limited to these system calls.

## Approach
1. Analyze the provided code to understand how the flag is loaded into memory and how the user-provided code is executed.
2. Observe that the flag is loaded into a memory region using `fread`, which reads the flag through a buffer on the heap.
3. Realize that even though the flag memory region is protected with `PROT_NONE`, the flag can still be read from the heap buffer used by `fread`.
4. Craft a shellcode that reads a large portion of the heap memory and writes it to the standard output using the allowed `write` system call.
5. Send the shellcode to the server for execution, retrieve the heap memory from the output, and search for the flag within it.

## Exploiting the Vulnerability
The solve.py script does the following:
1. Connects to the server using the provided netcat command.
2. Constructs a shellcode that performs the following actions:
   - Sets `rdi` register to the file descriptor for standard output (1).
   - Sets `rsi` register to a heap address (obtained by dereferencing `[rbp-0x28]`).
   - Aligns the heap address to the start of a page by masking it with `0xfffffffffffff000`.
   - Sets `rdx` register to the count of bytes to write (0x1000).
   - Sets `rax` register to the system call number for `write` (1).
   - Invokes the `write` system call to write the heap memory to standard output.
   - Moves the system call number for `exit` (60) into the `rax` register.
   - Invokes the `exit` system call to terminate the program.
3. Sends the shellcode to the server for execution.
4. Reads a chunk of heap memory (0x1000 bytes) from the server's output.
5. Searches for the flag pattern (`1753c{.*}`) within the received heap memory.
6. Prints the flag if found, or prints "flag not found" otherwise.

The key points of the exploit are:
- The flag is loaded into memory using `fread`, which reads the flag through a buffer on the heap.
- Even though the flag memory region is protected with `PROT_NONE`, the flag can still be read from the heap buffer used by `fread`.
- The shellcode reads a portion of the beginning of heap memory, where flag is likely to be.
- The flag is then searched within the received heap memory using a regular expression pattern.

## Obtaining the Flag
1. Run the solve.py script.
2. The script will connect to the server and send the shellcode.
3. The server will execute the shellcode, which reads the heap memory and writes it to standard output.
4. The script will read the heap memory from the server's output and search for the flag pattern.
5. If the flag is found, it will be printed. Otherwise, "flag not found" will be displayed.

Flag: `1753c{memory_so_vast_yet_you_managed_to_find_it}`

### Conclusion
This challenge demonstrates that even when a memory region is protected with `PROT_NONE`, sensitive data may still be accessible through other means, such as heap buffers used by I/O functions like `fread`.

The exploit takes advantage of the fact that the flag is loaded into memory using `fread`, which reads the flag through a buffer on the heap. By reading a portion of the heap memory and searching for the flag pattern, we can retrieve the flag even though the original flag memory region is inaccessible.

The challenge highlights the importance of securely handling sensitive data throughout its lifecycle, including during I/O operations and memory management. It also emphasizes the need to consider potential side channels and alternative paths through which sensitive data may be accessed or leaked.
