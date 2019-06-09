#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "khash.h"

static const char *const SYMBOLS = "123456789";

KHASH_SET_INIT_STR(str_set);
KHASH_MAP_INIT_STR(str_map, int);

static int n;
static long int n_perms;
static char *superperm;
static char *p;
static char *end;

static khash_t(str_set) *permutations;
static khash_t(str_map) *one_cycles;
static khash_t(str_map) *two_cycles;

inline void cyclerep(char *dst, char *src, int n) {
	char min_char = 0xFF;
	int min_char_index;

	for (int i = 0; i < n; ++i) {
		if (src[i] < min_char) {
			min_char = src[i];
			min_char_index = i;
		}
	}

	int j = 0;
	for (int i = min_char_index; i < n; ++i) {
		dst[j++] = src[i];
	}
	for (int i = 0; i < min_char_index; ++i) {
		dst[j++] = src[i];
	}
}

void search(char *p, int w) {
	int absent;
	khint_t it = kh_put(str_set, permutations, p, &absent);
	if (absent) kh_key(permutations, it) = strdup(p);
	else return;

	char one_cycle[10];
	char two_cycle[10];

	cyclerep(&one_cycle, p, n);
	two_cycle[0] = p[n-1];
	cyclerep(&two_cycle[1], p, n-1);

	khint_t one_cycle_it = kh_get(str_map, one_cycles, one_cycle);
	if (one_cycle_it == kh_end(one_cycles)) {
		one_cycle_it = kh_put(str_map, one_cycles, one_cycle, &absent);
		kh_val(one_cycles, one_cycle_it) = 1;
	}
	else {
		kh_val(one_cycles, one_cycle_it)++;
	}

	khint_t two_cycle_it = kh_get(str_map, two_cycles, two_cycle);
	if (two_cycle_it == kh_end(two_cycles)) {
		two_cycle_it = kh_put(str_map, two_cycles, two_cycle, &absent);
		kh_val(two_cycles, two_cycle_it) = 1;
	}
	else {
		kh_val(two_cycles, two_cycle_it)++;
	}

	if (kh_size(permutations) == n_perms) {
		printf("%s\n", superperm);
	}
	else if (kh_val(one_cycles, one_cycle_it) == n) {

	}
	else {
		
	}
}

inline long int factorial(int n) {
	long int r = 1;
	for(int i = 1; i <= n; i++) r *= i;
	return r;
}

int main(int argc, char **argv) {
	if (argc != 2) {
		fprintf(stderr, "Usage: %s <n>\n", argv[0]);
		return 1;
	}

	n = atoi(argv[1]);
	if (n < 4 || n > 9) {
		fprintf(stderr, "The value of n must be between 4 and 9 (not %d)\n", n);
		return 1;
	}

	n_perms = factorial(n);
	superperm = calloc(n_perms * 3 + n + 1, 1);
	memcpy(superperm, SYMBOLS, n);

	permutations = kh_init(str_set);
	one_cycles = kh_init(str_map);
	two_cycles = kh_init(str_map);

	search(p, n);

	return 0;
}
