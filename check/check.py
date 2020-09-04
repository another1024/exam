# -*- coding: utf-8 -*-
import pydot
from networkx.drawing.nx_pydot import write_dot
import os
import networkx as nx
import  networkx.algorithms.isomorphism as iso
import  re
import sys
import string
import random
sys.path.append('../')
from config import cursor, db

'''
clang 1.c -emit-llvm -c -o 1.bc
opt -load ./psu/bulid/libpdg.so -dot-pdg ./1.bc
dot -Tpdf pdgragh.main.dot > pgf.pdf


CREATE TABLE `check`(`id` INT UNSIGNED AUTO_INCREMENT, `paper_id` VARCHAR(100) NOT NULL,`dot` VARCHAR(65500) NOT NULL ,   PRIMARY KEY (`id`)) DEFAULT CHARSET=utf8;

'''

class Check:

    find_node = []
    dot = None
    path = './check_file/'
    def findb(self,node):
        
        for i in self.dot.successors(node):
           
            if i not in self.find_node:
                self.find_node.append(i)
                self.finddp(i)


    def finddp(self,node):
        self.find_node.append(node)
        for i in self.dot.predecessors(node):
            if i not in self.find_node:
                self.finddp(i)
               
                if 'label' in self.dot.nodes[i].keys():
                    s = self.dot.nodes[i]['label']
                    
                    if s.find('global')!=-1:
                        self.findb(i)

        return 

    def open_dot(self,s):

        get_dot = pydot.graph_from_dot_file(s)
        dot=get_dot[0]
        dot = nx.nx_pydot.from_pydot(dot)
        return dot

    def del_edge(self):
        
        
        for edge in list(self.dot.edges.keys()):
            
            
            if( 'style' not in self.dot.edges[edge].keys()  ):
               #print(self.dot.edges[edge])
               if(len(edge)==2):
                   self.dot.remove_edge(edge[0],edge[1])
               else:
                   self.dot.remove_edge(edge[0],edge[1],edge[2])

    def findfun(self):
        io_function = []
        nodes = self.dot.nodes     
          
        for node in list(nodes):
       
            if 'label' in self.dot.nodes[node].keys():
                s = self.dot.nodes[node]['label']
                
                if 'printf' in s or 'puts' in s or 'scanf' in s or 'getchar' in s:
                    io_function.append(node)
        for call in    io_function:
            self.finddp(call)

    def del_other(self):
        edges = self.dot.edges
        for edge in list(edges):
            if( edge[0] not in self.find_node or  edge[1] not in self.find_node  ):
               if(len(edge)==2):
                   self.dot.remove_edge(edge[0],edge[1])
               else:
                   self.dot.remove_edge(edge[0],edge[1],edge[2])
        nodes = self.dot.nodes
        for node in list(nodes):
            if node not in self.find_node:
                self.dot.remove_node(node)

    def graph_find(self,dot_test):
        GM = iso.GraphMatcher(self.dot,dot_test,node_match=iso.categorical_node_match(['label'],['']))
        size = 0 
        for subgraph in GM.subgraph_isomorphisms_iter(): 
            size+=len(subgraph)
        
        return size
  
    def add_point(self):
        p  = re.compile("\s%\w+")
        for i in self.dot.nodes:
            s=self.dot.nodes[i]['label']
            s=re.sub(p," var",s)
            self.dot.nodes[i]['label']=s
    

    def system(self,s):
        s = os.popen(s+'  2>&1')
        return s.read()



    def find_all_file(self,paper_id,name):
        
        files = os.listdir(self.path)
        r = []
        
        for f in files: 
            if not os.path.isdir(f) and f.find('@'+paper_id) !=-1 and f.find(name) == -1:
                r.append(self.path+"/"+f)
        
        return r  
    def randname(self):
        salt = ''.join(random.sample(string.ascii_letters + string.digits, 5))
        return salt

    def save(self,paper_id,name):
        write_dot(self.dot,self.path+'/@'+paper_id+'_'+name+'_'+self.randname())
        
    def main(self,paper_id,name):
        s = self.system('rm -rf ./env/*;clang test.c -emit-llvm -c -o ./env/test.bc')
        os.system('cd ./env;opt -load ../psu/bulid/libpdg.so -dot-pdg ./test.bc; ')
        self.dot = self.open_dot('./env/pdgragh.main.dot')
        
        self.del_edge()
        self.findfun()
        self.del_other()
        self.add_point()
        file_list = self.find_all_file(paper_id,name)
        r=0
        for i in file_list:
            
            dot_test = self.open_dot(i)

            r = max(self.graph_find(dot_test),r)
        size_all = self.graph_find(self.dot)
        self.save(paper_id,name)
       
        return str(r/size_all)

if __name__=='__main__':
    check = Check()
    print(check.main('1','aaa'))
