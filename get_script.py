import os
import re
import shutil

#配置区
local_path = "C:/Users/zach.zhang/Desktop/"
git_default_path_lib = r"E:\git\Standard\lib"
git_default_path_main = r"E:\git\Standard\bin\internal"
os.chdir("E:\\git\\Standard\\")
os.system("git checkout develop")

def mkdir_script(name:str,local_path:str) ->str:
    if not os.path.exists(local_path+name):
        os.mkdir(local_path+name)
        return local_path+name
    else:
        os.mkdir(local_path+name+'_')
        return local_path+name+'_'

def get_script_lib(file_path:str,local_path,name:str)->None:
    if os.path.exists(file_path):
        filename_list = os.listdir(file_path)
        for i in filename_list:
            if re.search("Communal",i):
                filename_list_com = os.listdir(file_path+"/%s"%i)
                for j in filename_list_com:
                    shutil.copy(file_path+"/%s/%s"%(i,j),local_path)
                break
        for y in filename_list:  
            if re.search(name,y):
                filename_list_lib = os.listdir(file_path+"/%s"%y)
                for j in filename_list_lib:
                    shutil.copy(file_path+"/%s/%s"%(y,j),local_path)
                break
    else:
        print("库函数路径有误")



def get_script_main(file_path:str,local_path,name:str)->None:
    if os.path.exists(file_path):
        filename_list = os.listdir(file_path)
        for i in filename_list:
            if re.search(name,i):
                filename_list_main = os.listdir(file_path+"/%s"%i)
                for j in filename_list_main:
                    shutil.copy(file_path+"/%s/%s"%(i,j),local_path)
                break
    else:
        print("主函数路径有误") 

if __name__ == "__main__":
    script_name = input("请输入脚本名称：")
    file_local_path = mkdir_script(script_name,local_path)
    get_script_lib(git_default_path_lib,file_local_path,script_name)
    get_script_main(git_default_path_main,file_local_path,script_name)
    print("成功复制到本地")




