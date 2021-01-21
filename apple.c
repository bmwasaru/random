#include <stdio.h>

int main(int argc, char **argv, char **envp, char **apple) {
    int n = 0;
    while (*apple)
        printf("apple[%d] = %s\n", n++, *apple++);
    return 0;
}
