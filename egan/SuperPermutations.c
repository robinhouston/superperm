//
//  SuperPermutations.c
//
//  Created by Greg Egan on 20/10/2018.
//
//	Version 1: 21/10/2018
//
//	Generates superpermutations for n>=4, possibly minimal for n>=7
//
//	Method is adapted from:
//
//	"Hamiltonicity of the Cayley Digraph ... " by Aaron Williams
//
//	https://arxiv.org/abs/1307.2549
//
//
//	Usage:	SuperPermutations n [-v[erbose]]
//
//	Writes the superpermutation to a file n_L.txt, where L is the length of the superpermutation

//	Largest n value permitted

#define MAX_N 13

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define TRUE (1==1)
#define FALSE (1==0)

#define CHECK_MEM(p) if (p==NULL) {printf("Insufficient memory\n"); exit(EXIT_FAILURE);};

//	Pieces of data we will use to hold flags

typedef unsigned long int PIECE;

//	Zero a sequence of pieces

#define ZERO(p,n) for (int zp=0;zp<n;zp++) *(p+zp)=0;

//	Copy a sequence of pieces

#define COPY(pSrc,pDest,n) for (int zp=0;zp<n;zp++) *(pDest+zp)=*(pSrc+zp);

//	Set a bit in a block of pieces

#define SETBIT(p,b) *(p+(b)/bitsPerPiece) |= (((PIECE)1)<<((b)%bitsPerPiece));

//	Get a bit in a block of pieces

#define GETBIT(p,b) (((*(p+(b)/bitsPerPiece)) & (((PIECE)1)<<((b)%bitsPerPiece))) ? 1 : 0)


//	Factorial

int factorial(int n)
{
if (n==0) return 1; else return n*factorial(n-1);
}

//	Compare two integer sequences

static int nCompareInt;
int compareInt(const void *ii0, const void *jj0)
{
int *ii=(int *)ii0, *jj=(int *)jj0;
for (int k=0;k<nCompareInt;k++)
	{
	if (ii[k] < jj[k]) return -1;
	else if (ii[k] > jj[k]) return 1;
	};
return 0;
}

//	Generate all permutations of 1 ... n;
//	generates lists for lower values of n
//	in the process.
//
//	We sort each table into lexical order after constructing it.

void makePerms(int n, int **permTab)
{
int fn=factorial(n);
int size=n*fn;
int *res;

res=(int *)malloc(size*sizeof(int));
CHECK_MEM(res)

if (n==1)
	{
	res[0]=1;
	}
else
	{
	makePerms(n-1, permTab-1);
	int *prev=*(permTab-1);
	int p=0;
	int pf=factorial(n-1);
	for (int k=0;k<pf;k++)
		{
		for (int q=n-1;q>=0;q--)
			{
			int r=0;
			for (int s=0;s<n;s++)
				{
				if (s==q) res[p++]=n;
				else res[p++]=prev[k*(n-1)+(r++)];
				};
			};
		};
	qsort(res,fn,n*sizeof(int),compareInt);
	};

*permTab = res;
}

//	Print a single integer sequence

void printInt(int *ii, int n, char *eos)
{
printf("{");
for (int i=0;i<n;i++) printf("%d%s",ii[i],i==n-1?"":",");
printf("}%s",eos);
}

//	Print a block of integer sequences

void printBlock(int *b, int n, int s)
{
printf("{");
for (int i=0;i<s;i++) printInt(b+i*n,n,i==s-1?"}\n":",\n");
}

//	Print a block of integer sequences, numbering them from 0

void printBlockN(int *b, int n, int s)
{
for (int i=0;i<s;i++)
	{
	printf("%4d ",i);
	printInt(b+i*n,n,"\n");
	};
}

//	Print a block of permutations, specified by indices

void printBlockPerms(int *b, int n, int s, int *perms)
{
printf("{");
for (int i=0;i<s;i++) printInt(perms+b[i]*n,n,i==s-1?"}\n":",\n");
}

//	Print a single integer sequence, remapping the integers

void printIntRemapped(int *ii, int n, int *map, char *eos)
{
printf("{");
for (int i=0;i<n;i++) printf("%d%s",map[ii[i]-1],i==n-1?"":",");
printf("}%s",eos);
}

//	Print a block of permutations, specified by indices, remapping the digits

void printBlockPermsRemapped(int *b, int n, int s, int *perms, int *map)
{
printf("{");
for (int i=0;i<s;i++) printIntRemapped(perms+b[i]*n,n,map,i==s-1?"}\n":",\n");
}

//	Find an integer sequence in a sorted block

int searchBlock(int *base, int n, int s, int *target)
{
int *res = (int *) bsearch(target, base, s, n*sizeof(int), compareInt);
if (res) return (int)(res-base)/n;
else return -1;
}

//	The weight 1 successor of a permutation:  left rotation

void successor1(int *perm, int *s, int n)
{
for (int k=0;k<n;k++) s[k]=perm[(k+1)%n];
}

//	The weight 1 predecessor of a permutation:  right rotation

void predecessor1(int *perm, int *s, int n)
{
for (int k=0;k<n;k++) s[k]=perm[(k+n-1)%n];
}

//	The weight 2 successor of a permutation:
//	two left rotations then swap last two elements

void successor2(int *perm, int *s, int n)
{
for (int k=0;k<n;k++) s[k]=perm[(k+2)%n];
int tmp=s[n-1];
s[n-1]=s[n-2];
s[n-2]=tmp;
}

//	The weight 2 predecessor of a permutation:
//	two right rotations then swap first two elements

void predecessor2(int *perm, int *s, int n)
{
for (int k=0;k<n;k++) s[k]=perm[(k+n-2)%n];
int tmp=s[0];
s[0]=s[1];
s[1]=tmp;
}

//	Generate an alternating cycle, applying succesor2 then predecessor1 in turn
//	Each cycle is of length 2(n-1)

int *altCycle(int n, int startPerm, int *s2tab, int *p1tab, int *storage)
{
int nCycle = 2*(n-1);
int *res = storage ? storage : (int *)malloc(nCycle*sizeof(int));
CHECK_MEM(res)

int p=startPerm;
for (int i=0;i<n-1;i++)
	{
	res[2*i]=p;
	p=s2tab[p];
	res[2*i+1]=p;
	p=p1tab[p];
	};
return res;
}

//	Our version of Williams's F function
//
//	F(n,r,m) produces a list of all (n-3)! permutations starting with m n r
//	fn is n!, permTab is table of all permutations for {1}, {1,2}, {1,2,3}, ..., {1,...,n}

int *F(int n, int r, int m, int fn, int **permTab)
{
static int ex[MAX_N], fs[MAX_N];
int *res;
int f3=factorial(n-3);
res = (int *)malloc(f3*sizeof(int));
CHECK_MEM(res)

fs[0]=m;
fs[1]=n;
fs[2]=r;

//	List the n-3 digits in {1,...n} \ {m,n,r}

int q=0;
for (int i=1;i<=n-1;i++) if (i!=m && i!=r) ex[q++]=i;

//	List the permutations

for (int j=0;j<f3;j++)
	{
	int *pm3 = permTab[n-4]+j*(n-3);
	for (int k=0;k<n-3;k++) fs[k+3]=ex[pm3[k]-1];
	res[j]=searchBlock(permTab[n-1],n,fn,fs);
	};

return res;
}

//	Our version of Williams's A2 function
//
//	A2 gives (n-1) x (n-3)! altCycles, each of length 2(n-1);
//	these altCycles get their starting points from n-1 F() lists of length (n-3)!

int *A2(int n, int fn, int **permTab, int *s2tab, int *p1tab, int *nres)
{
int f3=factorial(n-3);
int cycleLen=2*(n-1);
int nCycles=(n-1)*f3;
*nres=nCycles*cycleLen;
int *res=(int *)malloc((*nres)*sizeof(int));
CHECK_MEM(res);

int *storage=res;
for (int r=1;r<=n-1;r++)
	{
	int *f=F(n,r,(r%(n-1))+1, fn, permTab);
	for (int j=0;j<f3;j++)
		{
		altCycle(n, f[j], s2tab, p1tab, storage);
		storage+=2*(n-1);
		};
	free(f);
	};
return res;
}

//	Our version of Williams's C2 function
//
//	C2 gives two loops that together form a cycle cover of S_n
//
//	The edges used are weight-1 edges that are NOT in the A2 cycles, and weight-2 edges otherwise.

int *C2(int n, int fn, int **permTab, int *s1tab, int *s2tab, int *p1tab, int bitsPerPiece, int piecesPerBitString, int *len1, int *len2)
{
int *res = (int *)malloc(fn*sizeof(int));
CHECK_MEM(res);

//	We specify sets of permutations using bit flags

PIECE *flags = (PIECE *)malloc(piecesPerBitString*sizeof(PIECE));
CHECK_MEM(flags)
ZERO(flags,piecesPerBitString)

PIECE *pool = (PIECE *)malloc(piecesPerBitString*sizeof(PIECE));
CHECK_MEM(pool)
ZERO(pool,piecesPerBitString)

//	Get the A2 cycles, so we can mark the weight 1 edges they contain (pointed backwards)

int na2 = 0;
int *a2 = A2(n, fn, permTab, s2tab, p1tab, &na2);
for (int i=0;i<na2;i+=2) SETBIT(flags,a2[i])
free(a2);

//	Assemble the two loops, starting the first one from the identity permutation

int nLoops=0;
int nPerms=0;
int start=0, prev, next;
for (nLoops=0;nLoops<2;nLoops++)
	{
	res[nPerms++]=start;
	SETBIT(pool,start)
	prev=start;
	while (TRUE)
		{
		if (GETBIT(flags,prev)) next=s2tab[prev]; else next=s1tab[prev];
		if (next==start) break;
		res[nPerms++]=next;
		SETBIT(pool,next)
		prev=next;
		};
	if (nLoops==0)
		{
		*len1 = nPerms;
		*len2 = fn - nPerms;
		};
	start=0;
	while (GETBIT(pool,start)) start++;
	};

free(flags);
free(pool);
return res;
}

//	Main program
//	============
//

int main(int argc, const char * argv[])
{
int n=-1;
int verbose=FALSE, ok=FALSE;

//	Get parameters fromm the command line
//	Usage:	SuperPermutations n [-v[erbose]]

if (argc>=2) if (sscanf(argv[1],"%d",&n)!=1) n=-1;
if (n>MAX_N||n<4)
	{
	if (n>=0) printf("n = %d is out of range, must be from 4 to %d\n",n,MAX_N);
	}
else ok=TRUE;
if (argc>=3)
	{
	if (strcmp(argv[2],"-v")==0 || strcmp(argv[2],"-verbose")==0 || strcmp(argv[2],"verbose")==0 || strcmp(argv[2],"v")==0) verbose=TRUE;
	else ok=FALSE;
	};
if (!ok)
	{
	printf("Usage:	SuperPermutations n [-v[erbose]]\n");
	exit(EXIT_FAILURE);
	};

int fn=factorial(n);
printf("n = %d, n! = %d\n",n,fn);
nCompareInt=n;			//	Global copy of n needed by permutation comparison routine compareInt()

int **permTab;
permTab = (int **)malloc(n*sizeof(int *));
CHECK_MEM(permTab)
makePerms(n,permTab+n-1);
int *perms=permTab[n-1];
if (verbose)
{
	printf("Permutations:\n");
	printBlockN(perms,n,fn);
};

//	Build successor and predecessor tables

int *s = (int *)malloc(n*sizeof(int));
CHECK_MEM(s)

if (verbose)
{
printf("Successor 1:\n");
};
int *s1tab = (int *)malloc(fn*sizeof(int));
CHECK_MEM(s1tab)
for (int k=0;k<fn;k++)
	{
	successor1(perms+k*n,s,n);
	s1tab[k]=searchBlock(perms,n,fn,s);
	if (verbose)
{
	printf("%4d  %4d\n",k,s1tab[k]);
	};
	};

if (verbose)
{
printf("Successor 2:\n");
};
int *s2tab = (int *)malloc(fn*sizeof(int));
CHECK_MEM(s2tab)
for (int k=0;k<fn;k++)
	{
	successor2(perms+k*n,s,n);
	s2tab[k]=searchBlock(perms,n,fn,s);
	if (verbose)
{
	printf("%4d  %4d\n",k,s2tab[k]);
	};
	};

if (verbose)
{
printf("Predecessor 1:\n");
};
int *p1tab = (int *)malloc(fn*sizeof(int));
CHECK_MEM(p1tab)
for (int k=0;k<fn;k++)
	{
	predecessor1(perms+k*n,s,n);
	p1tab[k]=searchBlock(perms,n,fn,s);
	if (verbose)
{
	printf("%4d  %4d\n",k,p1tab[k]);
	};
	};

if (verbose)
{
printf("Predecessor 2:\n");
};
int *p2tab = (int *)malloc(fn*sizeof(int));
CHECK_MEM(p2tab)
for (int k=0;k<fn;k++)
	{
	predecessor2(perms+k*n,s,n);
	p2tab[k]=searchBlock(perms,n,fn,s);
	if (verbose)
{
	printf("%4d  %4d\n",k,p2tab[k]);
	};
	};
	
//	Structure of storage for flags

int bytesPerPiece = sizeof(PIECE);
int bitsPerPiece = 8*bytesPerPiece;
int bitsNeeded = fn;
int piecesPerBitString = bitsNeeded/bitsPerPiece;
while (piecesPerBitString*bitsPerPiece < bitsNeeded) piecesPerBitString++;

if (verbose)
{
//	Check altCycle()
printf("\nExample of altCycle(), starting at identity perm:\n");
int *aa=altCycle(n, 0, s2tab, p1tab, NULL);
printBlockPerms(aa,n,2*(n-1),perms);
};

if (verbose)
{
//	Check F()
printf("\nExample of our version of Williams F(), F(n,1,2):\n");
int *ff=F(n, 1, 2, fn, permTab);
printBlockPerms(ff,n,factorial(n-3),perms);
};

if (verbose)
{
//	Check A2()
printf("\nOur version of Williams A2():\n");
int na2 = 0;
int *a2=A2(n, fn, permTab, s2tab, p1tab, &na2);
printBlockPerms(a2,n,na2,perms);
};

//	Get C2()

int len1 = 0, len2 = 0;
int *c2a=C2(n, fn, permTab, s1tab, s2tab, p1tab, bitsPerPiece, piecesPerBitString, &len1, &len2);
int *c2b=c2a+len1;

if (verbose)
{
//	Show C2()
printf("\nOur version of Williams C2():\n");
printf("First cycle:\n");
printBlockPerms(c2a,n,len1,perms);
printf("Second cycle:\n");
printBlockPerms(c2b,n,len2,perms);
};

//	Get the final path by splicing together the two loops in the cycle cover C2
//
//	We choose splice points where we join the loops with a weight-1 edge, while breaking a weight-2 edge in each loop

int *path = (int *)malloc(fn*sizeof(int));
CHECK_MEM(path)
int i0=-1, j0=-1;
int done=FALSE;

for (int i=0;i<len1 && !done;i++)
for (int j=0;j<len2 && !done;j++)
	{
	if (s1tab[c2a[i]]==c2b[j] && s2tab[c2a[i]]==c2a[(i+1)%len1] && p2tab[c2b[j]]==c2b[(j+len2-1)%len2])
		{
		i0=i;
		j0=j;
		done=TRUE;
		break;
		};
	};

if (!done)
	{
	printf("Could not find optimal splice point between the loops\n");
	exit(EXIT_FAILURE);
	};
	
//	Splice the loops

int nPath=0;
for (int i=0;i<len1;i++) path[nPath++] = c2a[(i0+1+i)%len1];
for (int i=0;i<len2;i++) path[nPath++] = c2b[(j0+i)%len2];

//	We remap the digits so we start at the identity

int map[MAX_N];
for (int i=0;i<n;i++) map[*(perms+path[0]*n+i)-1]=i+1;

if (verbose)
{
printf("\nHamiltonian path:\n");
printBlockPermsRemapped(path,n,fn,perms,map);
};

//	Compute the total weight and verify that the path contains every permutation, and only edges of weights 1 and 2

PIECE *flags = (PIECE *)malloc(piecesPerBitString*sizeof(PIECE));
CHECK_MEM(flags)
ZERO(flags,piecesPerBitString)
SETBIT(flags,path[0])

int totalWeight = n + fn - 1;
for (int i=0;i<fn-1;i++)
	{
	if (s2tab[path[i]]==path[i+1]) totalWeight++;
	else if (s1tab[path[i]]!=path[i+1])
		{
		printf("*** Edge at index %d in path that is not of weight 1 or 2 ***\n",i);
		};
	if (GETBIT(flags,path[i+1]))
		{
		printf("*** Repeated permutation at index %d in path ***\n",i+1);
		}
	else SETBIT(flags,path[i+1])
	};
printf("Total weight = %d\n",totalWeight);

//	Write final digits to file; in case we are going beyond 9, we need to remap as characters from 0...9abcd...

char *charMap="0123456789abcdefghijklmnopqrstuvwxyz";

char fileName[128];
sprintf(fileName,"%d_%d.txt",n,totalWeight);
FILE *fp=fopen(fileName,"wa");
if (fp==NULL)
	{
	printf("Unable to open output file %s\n",fileName);
	exit(EXIT_FAILURE);
	};
	
int skip=0, nchars=0;
for (int i=0;i<fn;i++)
	{
	int p=path[i];
	for (int j=skip;j<n;j++) {fprintf(fp,"%c",charMap[map[*(perms+p*n+j)-1]]); nchars++;}
	if (i!=fn-1) skip = s1tab[path[i]]==path[i+1] ? n-1 : n-2;
	};
	
if (nchars!=totalWeight)
	{
	printf("*** Mismatch between %d characters written, and total weigt %d\n",nchars, totalWeight);
	};

fprintf(fp,"\n");
fclose(fp);
printf("Wrote file %s\n",fileName);
return 0;
}
