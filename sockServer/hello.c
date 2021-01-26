#include <stdio.h>

struct teststruct
{
	char name[3];
	int x;
	int y;
};

int test(int a, int b)
{
	printf("Hello world! บร\n");
	return a+b;
}

char* test1(struct teststruct *p)
{
	char *str="บร";
	printf("str:0x%x, 0x%x 0x%x\n", str[0], str[1], str[2]);
	printf("name:%s\n", p->name);
	printf("0x%x, 0x%x, 0x%x\n", p->name[0], p->name[1], p->name[2]);
	printf("x:%d, y:%d\n", p->x, p->y);
	return p->name;
}