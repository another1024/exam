#coding=utf-8
import os
import time
import _thread
import sys
import socket
import threading
from check import Check
from docker import Docker
sys.path.append('../')
from config import cursor, db
from config import log


class Test: 
    name = ''
    user = ''
    answer = 0
    all_answer = 0
    code = ''
    check_answer = '0'
    flag = 0
    user_id = ''

    def __init__(self):
    
        return


class Task:
    check = None
    docker = []
    test_list = {}
    out_list = {}
    lock = None
    def __init__(self):
        self.check = Check()
        self.docker.append(Docker('875')) 
        self.lock = threading.Lock()

    def test_one(self,test):
        
        sql = "select * from checkdata where name=%s"
        res = cursor.execute(sql, (test.name))
        print(test.name)
        if res:
            result = cursor.fetchall()
            data_in = []
            data_out = []
            test.all_answer = len(result)
            for i in result:
                data_in.append(i['datain'])
                data_out.append(i['dataout'])
            
            r = self.docker[0].run(test.code,data_in,data_out)
            if r==-1:
                r=0
            elif r==0:
                r=test.all_answer
            r = (r/test.all_answer)*100
        else:
            r = -1
           
        test.answer = r
        
        
 
    def check_test(self,name,user):
        return self.check.main(name,user)

    def save_grade(self,test):
        if(test.answer == -1):
            print("error")
            return
        sql = "insert into user_grade (user_id,paper_name, user_name, exam_grade, cheat_grade, create_time) VALUES (%s,%s,%s,%s,%s,now())"
        try:
            res = cursor.execute(sql, (test.user_id,test.name, test.user, str(test.answer), str(test.check_answer)))
            db.commit()
        except Exception as e:
            print(e)
            db.rollback()
            res = None        
        return 
    def main(self):
        while(1):
            self.lock.acquire()
            
            values = []
            if(len(self.test_list)!=0):
                values  = list(self.test_list.values())
                for k,v in self.test_list.items():
                    self.out_list[k] =v
                self.test_list={} 
                self.lock.release()
            else:
                self.lock.release()
                time.sleep(1)
                
            print(self.out_list.values())
            for i in self.out_list.values():
                if(i.flag==0):
                    self.test_one(i)
                    if(i.answer==100):
                        i.check_answer = self.check_test(i.name,i.user)
                
                    self.save_grade(i)
                    
                    i.flag = 1
                    break
       
    def recvuntil(self,c,fin):
        s = b''
        while(1):
            char = c.recv(1)
            
            if(char !=bytes(fin,'utf-8')):
                
                s+=char    
            else:
                
                return str(s, encoding ='utf-8')      
    
    def get_test(self,c):
        
        t = Test()
        s = self.recvuntil(c,'\x00')
        
        user_id = s
        t.user_id = s
        s = self.recvuntil(c,'\x00')
        
        t.user =s
        
        s = self.recvuntil(c,'\x00')
        
        

        t.name =s
        s = self.recvuntil(c,'\x00')
        
        
        t.code = s
        self.lock.acquire()
        self.test_list[user_id] = t
        self.lock.release()

    def send_test(self,c):
        s = self.recvuntil(c,'\x00')
        user_id = s
        if(user_id in self.test_list.keys()):
            r = bytes('0\x00','utf-8')
        elif(user_id in self.out_list.keys()):
            flag = str(self.out_list[user_id].flag)
            if(self.out_list[user_id].flag==1):
                del self.out_list[user_id]
            r = bytes(flag+'\x00','utf-8')
        else:
            r = bytes('2\x00','utf-8')

        c.send(r)        
    def server(self):
        s = socket.socket()         
        host = '127.0.0.1'
        port = 12345                
        s.bind((host, port))        
        s.listen(5)                 
        while True:
            c,addr = s.accept()
            com = str(c.recv(2),  encoding = "utf-8")
            com = com[0]
            
            if(com=='0'):
                self.get_test(c)           
            else: 
                self.send_test(c)
            c.close()                
if __name__=='__main__':
    task = Task()
    _thread.start_new_thread( task.main, ())
    
    task.server()
        
'''
docker build -t "helloworld" .
sudo docker run -d -p "0.0.0.0:pub_port:9999" -h "helloworld" --name="helloworld" helloworld

'''
