#include <stdio.h>
#include <stdlib.h>
#include <stdlib.h>
#include <unistd.h>

char buf[0];

int main() {
  setbuf(stdin, NULL);
  setbuf(stdout, NULL);
  setbuf(stderr, NULL);

  puts("+++++++++++++++++++++++++++");
  puts("    WELCOME TO ADDITION");
  puts("+++++++++++++++++++++++++++");

  unsigned long offset;
  unsigned long toadd;
  char inp[16];

  while (1) {
    write(1, "add where? ", 11);
    fgets(inp, 16, stdin);
    offset = atoll(inp);
    write(1, "add what? ", 10);
    fgets(inp, 16, stdin);
    toadd = atoll(inp);
    *((unsigned long*) &buf[offset]) += toadd;
    if (offset == 1337) {
      break;
    }
  }

  exit(0);
}
