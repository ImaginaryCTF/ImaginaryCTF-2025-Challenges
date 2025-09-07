#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

char sh[] = "/bin/sh";

__attribute__((naked)) void pop_rdi_ret(void) {
    __asm__ volatile(
        "pop %rdi\n"
        "ret\n"
    );
}

int main() {
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);

    char buf[0x38];

    printf("Welcome to babybof!\n");
    printf("Here is some helpful info:\n");
    printf("system @ %p\n", &system);
    printf("pop rdi; ret @ %p\n", &pop_rdi_ret+4);
    printf("ret @ %p\n", &pop_rdi_ret+5);
    printf("\"/bin/sh\" @ %p\n", &sh);
    printf("canary: %p\n", ((long*)buf)[7]);
    printf("enter your input (make sure your stack is aligned!): ");

    gets(buf);

    printf("your input: %s\n", buf);
    printf("canary: %p\n", ((long*)buf)[7]);
    printf("return address: %p\n", ((long*)buf)[9]);

    return 0;
}
