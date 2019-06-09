/*
From Appendix B of http://webhome.cs.uvic.ca/~ruskey/Publications/Universal/ShortPerms.pdf
*/

#include <stdlib.h>
#include <stdio.h>

// #define PERMS
// #define COOL

void bellperms();
void coolperms();
void visit();
void usage_error();
int *perm;
int n;

void main(int argc, char *argv[]) {
    int x;
    if (argc == 1) {usage_error();}
    n = atoi(argv[1]);
    if (n < 1) {usage_error();}
    perm = (int *)malloc((n+1)*sizeof(int));
    for(x=0; x<=n; x++) {perm[x] = n+1-x;}
    #ifdef COOL
    coolperms();
    #else
    bellperms();
    #endif
}

void coolperms() {
    int x;
    int first;
    first = perm[1];
    while (1) {
        visit();
        first = perm[1];
        perm[1] = perm[2];
        for (x=2; x<n && perm[x]>=perm[x+1]; x++) {perm[x]=perm[x+1];}
        if (first == 1 && x==n) {perm[x] = first; return;}
        if (x<n && first<perm[x]) {perm[x]=perm[x+1]; x++;}
        perm[x] = first;
    }
}

void bellperms() {
    int h,i,j,x,temp;
    h = 1;
    while (1) {
        visit();
        if (h == 1) {
            for (x=1; x < n; x++) {perm[x] = perm[x+1];}
            perm[n] = n;
            h = n;
        } else if (h > 2) {
            perm[h] = perm[h-1];
            perm[h-1] = n;
            h--;
        } else {
            temp = perm[1];
            perm[1] = perm[2];
            for (i=2; i < n && perm[i+1] == n-i+1; i++) {
                perm[i] = n-i+1; // printf("i: %d \n", i);
            }
            if (i == n) {
                return;
            }
            perm[i] = temp;
            if (perm[i] == n-i+1) {
            for (x=i; x < n; x++) {perm[x] = perm[x+1];}
            perm[n] = n-i+1;
        } else {
            for (j=i; perm[j] < n-i+1; j++);
            temp = perm[j-1];
            perm[j-1] = perm[j];
            perm[j] = temp;
        }
        h = 1;
        }
    }
}

void visit() {
    int x;
    #ifndef PERMS
    printf("%d ", perm[0]);
    #endif
    for (x=1; x<=n; x++) {
        printf("%d ", perm[x]);
    }

    #ifdef PERMS
    printf("\n");
    #endif
}

void usage_error()
{
    printf("usage: perms n for permutations of [n] (or shorthand Ucycle for permutationso of [n+1]).\n");
    exit(EXIT_FAILURE);
}
