#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main() {
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);

    long what1, what2;
    long *where1, *where2;

    printf("system @ %p\n", &system);
    printf("what? ");
    scanf("%ld%*c", &what1);
    printf("what? ");
    scanf("%ld%*c", &what2);
    printf("where? ");
    scanf("%p%*c", &where1);
    printf("where? ");
    scanf("%p%*c", &where2);

    where1[0] = what1;
    where1[1] = what2;
    where2[0] = what1;
    where2[1] = what2;

    return 0;
}
