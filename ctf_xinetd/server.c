#include<stdio.h>
#include<stdlib.h>
#include <unistd.h>
#include <seccomp.h>
#include <linux/seccomp.h>



#include <string.h>
#include <sys/time.h>
#include <sys/resource.h>
#include <sys/wait.h>


#define KB (1024)

void set_limit(void)
{
    struct rlimit memory_limit;

    //限制进程虚拟地址段大小
    memory_limit.rlim_cur = memory_limit.rlim_max = 10*1024*KB;
    if(setrlimit(RLIMIT_AS, &memory_limit))
        perror("setrlimit:");

    //限制进程数据段大小
    memory_limit.rlim_cur = memory_limit.rlim_max = 10*1024*KB;
    if(setrlimit(RLIMIT_DATA, &memory_limit))
        perror("setrlimit:");

    //限制进程栈大小
    memory_limit.rlim_cur = memory_limit.rlim_max = 1024*KB;
    if(setrlimit(RLIMIT_STACK, &memory_limit))
        perror("setrlimit:");

    //限制进程CPU时间
    memory_limit.rlim_cur = memory_limit.rlim_max = 5;
    if(setrlimit(RLIMIT_CPU, &memory_limit))
        perror("setrlimit:");
}

int main() {
  
  char file_name[30] = "./test";
  char *argv[] = {"/", NULL};
  char *env[] = {NULL};

  setbuf(stdin, 0LL);
  setbuf(stdout, 0LL);
  setbuf(stderr, 0LL);
 set_limit(); 
  // Init the filter
  scmp_filter_ctx ctx;
  ctx = seccomp_init(SCMP_ACT_KILL);
  
  seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(execve), 1,
                        SCMP_A0(SCMP_CMP_EQ, file_name));

 
  seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(read),0);
  seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(write),0);
  seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(exit_group),0);
  seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(brk),0);
  seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(fstat),0);
  seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(access),0);
  seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(uname),0);
  seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(readlink),0);
  seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(arch_prctl),0);
 
  seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(open),0);
  seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(openat),0);
  seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(close),0);
  seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(dup),0);
  seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(dup2),0);
  seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(dup3),0);


  seccomp_load(ctx);


  execve(file_name, argv, env);
  return 0;
}
/*

gcc -g server.c -o server -lseccomp
*/
