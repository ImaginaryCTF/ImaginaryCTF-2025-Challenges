#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h>
#include <string.h>
#include <sys/stat.h>

char flag[0x100];

void win() {
    read(open("secret.txt", O_RDONLY), flag, 0x30);
    write(open("win.txt", O_WRONLY | O_CREAT, S_IRWXU), flag, 0x30);
}

int main() {
    char buf[0x300];
    unsigned int sz;
    read(0, buf, 4);
    sz = atoi(buf);
    if (sz < 0x300) {
        read(0, buf, sz);
        buf[sz-1] = '\0';
        printf(buf);
        _exit(0);
    }
    exit(1);
}
