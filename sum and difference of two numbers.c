#include <stdio.h>
#include <string.h>
#include <math.h>
#include <stdlib.h>

int main()
{
int n1, n2, sum1, difference1;
float n3, n4, difference2, sum2;
scanf("%d %d", &n1, &n2);
scanf("%f %f", &n3, &n4);
sum1 = n1 + n2;
difference1 = n1 - n2;
sum2 = n3 + n4;
difference2 = n3 - n4;
printf("%d %d\n", sum1, difference1);
printf("%.1f %.1f", sum2, difference2);


    return 0;
}