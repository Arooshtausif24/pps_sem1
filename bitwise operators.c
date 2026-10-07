#include <stdio.h>
#include <string.h>
#include <math.h>
#include <stdlib.h>
//Complete the following function.


void calculate_the_maximum(int n, int k) {
  //Write your code here.
int maxAND = 0;
int maxOr = 0;
int maxXor = 0;

for (int a = 1; a <= n; a++)
{ 
    for (int b = a + 1; b <= n; b++)
    {
    int andResult = a & b;
    int orResult = a | b;
    int xorResult = a ^ b;
    
    if (andResult < k && andResult > maxAND)
    {
        maxAND = andResult;
    }
    if (orResult < k && orResult > maxOr)
    {
        maxOr = orResult;
    }
    if ( xorResult < k && xorResult > maxXor)
    {
        maxXor = xorResult;
    }
}
}

printf("%d\n", maxAND);
printf("%d\n", maxOr);
printf("%d", maxXor);
}
int main() {
    int n, k;
  
    scanf("%d %d", &n, &k);
    calculate_the_maximum(n, k);
 
    return 0;
}