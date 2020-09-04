import os
from pwn import *
class Docker:
    docker_id = ''
    ip = '127.0.0.1'
    port = 9999

    def system(self,s):
        s = os.popen(s+'  2>&1')
        return s.read()

    def __init__(self,docker_id,ip='127.0.0.1',port=9999):
        self.ip=ip
        self.port=port
        self.docker_id = docker_id 
        #self.system('docker start '+self.docker_id)
        return

    def test(self,data_in,data_out):
        p = remote(self.ip,self.port)
        if data_in  :
            p.send(data_in)
        size = len(data_out)
        
        s = str(p.recv(size,timeout = 1), encoding = "utf-8")
        print(s,data_out)
        if(s==data_out):
            return 1
        else:
            return 0
    

    def run(self,code,data_in,data_out):
        flag1=0
        flag2=0
        flag3=0

        f = open('test.c', 'wt',encoding='utf-8')
        f.write(code)
        f.close()
        
        s1 = self.system('gcc  -static -o ./test ./test.c ')


        if(s1 == ''):
            flag1 = 1
        s2 = self.system('sudo docker cp ./test '+self.docker_id+':/home/ctf')
        
        if(s2 == ''):
            flag2 = 1
        
        s3 = self.system('sudo docker exec -it '+self.docker_id+' /bin/bash -c \' chmod +x /home/ctf/test\'')
        if(s3 == ''):
            flag3 = 1
        
        if flag1 and flag2 and flag3:
           
            for i in range(len(data_out)):
                if(self.test(data_in[i],data_out[i]) == 0):
                    return i+1
            return 0
        elif flag1==0:
            return 1
        else:
            
            return -1

