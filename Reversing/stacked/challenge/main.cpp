#include"stdio.h"
#include"string.h"

char globalvar=0;

unsigned char flag[]="REDACTEDREDAC";

volatile unsigned char eor(unsigned char a)
{
	return a^0x069;
}

volatile unsigned char inc(unsigned char a)
{
	flag[globalvar]=a;
	globalvar++;
	return flag[globalvar];
}

volatile unsigned char rtr(unsigned char a)
{
	return (a >> 1) | (a << (8-1) );
}

volatile unsigned char off(unsigned char a)
{
	return a+15;
}

int main()
{
	inc(rtr(off(eor(
	inc(eor(rtr(rtr(
	inc(rtr(off(off(
	inc(rtr(eor(eor(
	inc(eor(off(rtr(
	inc(eor(rtr(rtr(
	inc(rtr(eor(rtr(
	inc(rtr(off(rtr(
	inc(eor(eor(eor(
	inc(eor(rtr(rtr(
	inc(rtr(off(rtr(
	inc(eor(eor(eor(
	inc(rtr(eor(off(flag[globalvar]))))))))))))))))))))))))))))))))))))))))))))))))))));
	for(int i=0;i<13;i++)printf("%x ",flag[i]);
	printf("\n");
	return 0;
}
