#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

void vuln() {
    char buf[0x40];
    read(0, buf, 0x200);
}

int main() {
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);

    vuln();

    return 0;
}
