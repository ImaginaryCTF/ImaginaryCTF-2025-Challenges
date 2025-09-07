#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

char *ptr;
size_t size;

void menu() {
    puts("1. create string");
    puts("2. delete string");
    puts("3. multiply");
    puts("4. exit");
    printf("> ");
}

void create() {
    size_t sz;
    printf("String size: ");
    scanf("%zu%*c", &sz);
    ptr = malloc(sz);
    if (!ptr) {
        puts("Allocation failed.");
        exit(1);
    }
    size = sz;
    printf("String content: ");
    fgets(ptr, sz, stdin);
    puts("String created.");
}

void delete() {
    int idx;
    if (size > 0x1000 || size == 0) {
        puts("Permission denied.");
    }
    free(ptr);
    ptr = NULL;
    size = 0;  // Clear size when deleting
    puts("String deleted.");
}

void edit() {
    int idx;
    size_t item;
    long val;
    printf("Index (0-%zu): ", size - 1);
    scanf("%zu%*c", &item);
    ptr[item] *= 2;
    puts("String updated.");
}

int main() {
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    setbuf(stderr, NULL);

    puts("+++++++++++++++++++++++++++");
    puts(" WELCOME TO MULTIPLICATION");
    puts("+++++++++++++++++++++++++++");

    int choice;
    while (1) {
        menu();
        if (scanf("%d%*c", &choice) != 1) {
            puts("Invalid input.");
            break;
        }
        switch (choice) {
            case 1:
                create();
                break;
            case 2:
                delete();
                break;
            case 3:
                edit();
                break;
            case 4:
                puts("Bye!");
                exit(0);
            default:
                puts("Invalid choice.");
                break;
        }
    }

    return 0;
}
