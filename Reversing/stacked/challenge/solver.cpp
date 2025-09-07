#include"stdio.h"

unsigned char inline rtr(unsigned char c)
{
	return (c << 1) | (c >> (8-1) );
}

unsigned char inline off(unsigned char c)
{
	return c-15;
}

unsigned char eor(unsigned char c)
{
	return c^0x069;
}


int main()
{
	unsigned char arr[]={0x094, 0x07, 0x0d4, 0x064, 0x07, 0x054, 0x063, 0x024, 0x0ad, 0x098, 0x045, 0x072, 0x035};
	printf("%c ", off(eor(rtr(arr[0]))));
	printf("%c ", eor(eor(eor(arr[1]))));
	printf("%c ", rtr(off(rtr(arr[2]))));
	printf("%c ", rtr(rtr(eor(arr[3]))));
	printf("%c ", eor(eor(eor(arr[4]))));
	printf("%c ", rtr(off(rtr(arr[5]))));
	printf("%c ", rtr(eor(rtr(arr[6]))));
	printf("%c ", rtr(rtr(eor(arr[7]))));
	printf("%c ", rtr(off(eor(arr[8]))));
	printf("%c ", eor(eor(rtr(arr[9]))));
	printf("%c ", off(off(rtr(arr[10]))));
	printf("%c ", rtr(rtr(eor(arr[11]))));
	printf("%c ", eor(off(rtr(arr[12]))));
	return 0;
}
