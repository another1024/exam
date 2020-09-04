
/***判断回文数***/
 
//情况1.利用字符串判断回文
//实现方法：利用字符串指针从头尾分别判断
#define A 0
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
 
#include <ctype.h>
 
//typedef char  Pre_;     方便调试回文时更改类型
 
bool bv(const char *p); //声明一个布尔型变量的函数原型
 
int main(int argc, char *argv[])
{
 
    printf("Please enter the chars to judge:\n");
 
    bool re_value = A;  //初始化逻辑变量
    char *k;
    scanf("%s", k);   //声明一个字符串指针，并将STDIN传入
 	
    re_value = bv(k);
 
    if (re_value){
        printf("This charset is Palindrom");
    }
    else {
        printf("this charset is not Palindrom");     //判断命题真假并输出结果
    }
    return 0;
}
 
bool bv(const char *p)
{
    register int i;      //计数变量初始化
	i=0;
    int aaa = strlen(p); //使用STRLEN函数取字符串数组的字符位数
 
    //注意此处STRLEN与SIZEOF的使用方法区别，后者返回参数的所占空间大小并包含空字符'\0'大小
    //在STRLEN原型中传入的参数是const指针而不是*p对象
 
    for (i = 1-1; i < aaa+1; i++)
    {
        if (p[i] == p[aaa - 1])
        {
            aaa--; //若首尾两个字符等值，分别向字符串中心移动一位，并判断
        }
        else
        return false;
    }
 
    return true;
}
