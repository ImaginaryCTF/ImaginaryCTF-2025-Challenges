#include"stdio.h"
#include"stdlib.h"
#include"time.h"

int main()
{
	srand(time(0));
	char flag[] = "51ngl3_4PP_mul71pl3_53rv1c35";
	char arr[28][28];
	for(int i=0;i<28;i++)
	{
		for(int j=0;j<28;j++)
		{
			arr[i][j]=rand();
		}
	}
	for(int i=0;i<28;i++)
	{
		arr[i][i]=(flag[i]-15)^0x42;
	}
	for(int i=0;i<28;i++)
	{
		printf("{");
		for(int j=0;j<28;j++)
		{
			printf("%d,",arr[i][j]);
		}
		printf("},\n");
	}
	return 0;
}
