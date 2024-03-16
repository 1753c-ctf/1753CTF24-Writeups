# Matrix Preloaded

## Challenge Description
We'll let you run any code you wish, Mr. Anderson. We trust that you won't do anything irresponsible.

`nc 158.178.197.18 39909`

## Initial Analysis
The challenge provides a netcat command to connect to a server that allows users to run arbitrary code. However, upon analyzing the provided code, we notice that the server implements a seccomp filter that restricts the allowed system calls to only `write`, `exit`, and `exit_group`. Filter is loaded by a shared library, which is in turn loaded through `LD_PRELOAD` environment variable.

## Approach
1. Create a shellcode that spawns a shell using the `execve` system call, without relying on any shared libraries or the dynamic linker.
2. Compile the shellcode as a static binary to avoid the influence of `LD_PRELOAD` and the seccomp filter.
3. Send the compiled shellcode to the server for execution.
4. Interact with the spawned shell to obtain the flag.

## Exploiting the Vulnerability
The solve.py script does the following:
1. Compiles the shellcode from the shell.c file using the following command: ```gcc -nostdlib -nostartfiles -masm=intel shell.c -static -o shell```

2. The `-nostdlib` and `-nostartfiles` flags ensure that the standard libraries and startup files are not used, and the `-static` flag creates a statically linked binary.
3. Reads the compiled shellcode binary into memory.
4. Connects to the server.
5. Sends the length of the shellcode binary (as a 2-byte unsigned short in network byte order) followed by the shellcode itself.
6. Interacts with the spawned shell on the server.

The key points of the exploit are:
- The shellcode in shell.c uses the `execve` system call to spawn a shell directly, without relying on any shared libraries or the dynamic linker.
- The shellcode is compiled as a static binary to avoid the influence of `LD_PRELOAD` and the seccomp filter. A static binary doesn't make use of dynamic linker, which is what does the preloading based on `LD_PRELOAD` variable.

## Obtaining the Flag
1. Run the solve.py script.
2. The script will compile the shellcode, connect to the server, and send the shellcode binary.
3. The server will execute the shellcode, spawning a shell.
4. Interact with the spawned shell to navigate the server's filesystem and obtain the flag.

Flag: `1753c{there_is_no_preload_theres_just_ld_linux_x86_64_so_2}`
### Conclusion
This challenge demonstrates the limitations of relying solely on `LD_PRELOAD` for restricting code execution. By compiling shellcode as a static binary, we can completely bypass the restrictions imposed by preloaded seccomp filter.

The challenge highlights the challenges of sandboxing. It also emphasizes the need to carefully consider the implications of allowing arbitrary code execution, even with restrictions in place.
