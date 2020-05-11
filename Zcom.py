import winreg
import serial
import sys
import signal
import threading

class MyThread(threading.Thread):
    def __init__(self,func,args='',name=''):
        threading.Thread.__init__(self)
        self.func = func
        self.name = name 
        self.args = args

    def run(self):
        self.func()

def check_port():
    """
    检测和记录设备管理器下所有串口号和端口号
    :key: 当前驱动在注册表的目录
    :name: 当前驱动在注册表的名称
    :value: 当前驱动在出册表的数据
    :port_list_name: 当前PC所有端口号
    :return: 当前PC所有端口信息
    """
    port_list_name = []
    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"HARDWARE\DEVICEMAP\SERIALCOMM")
    line = 0
    try:
        while 1:
            name, value, type = winreg.EnumValue(key, line)
            line += 1
            port_list_name.append(value)
    except:
        print(port_list_name)

def read():
    at_buffer =''
    while 1:  
        try:
            at_port_data_temp = at_port_open.read(1024)
            #print(at_port_data_temp)
            if at_port_data_temp is not b'':
                if len(at_buffer):  # buffer有内容时进行拼接后重置,避免重复拼接
                    at_data_buffer = at_buffer.encode("utf-8") + at_port_data_temp
                    at_buffer = ""
                else:
                    at_data_buffer = at_port_data_temp
                at_data_replace = str(at_data_buffer,'utf-8')
                print(at_data_replace.strip())
                # print("xxx:",at_data_buffer)
                # print("yyyyy:",at_data_replace)
                # at_result_temp = at_data_replace.split('\\r\\n')
                # at_result_string = "".join(at_result_temp)
                # if len(at_result_temp) == 1 and not at_data_replace.endswith("\\r\\n"):  # 此时执行AT后AT回显没有及时返回OK暂时只返回Atcommand
                #     at_buffer = at_buffer + at_data_buffer.decode("utf-8")
                # if len(at_result_temp) > 1 and not at_data_replace.endswith("\\r\\n"):
                #     index = 0  # 数据存储到列表的索引
                #     last_index = len(at_result_temp) - 1
                #     while index < last_index:
                #         #if at_command in at_result_temp[index]:
                #         if at_result_temp[index].endswith("\\r"):
                #             at_result_temp[index] = at_result_temp[index].replace("\\r", "\r")
                #         index = index + 1
                #         at_buffer = at_buffer + at_result_temp[last_index]
                # if at_data_replace.endswith("\\r\\n"):
                #     for at_result in at_result_temp:
                #         if at_result.endswith('\\r'):
                #             at_result = at_result.replace("\\r","")
                #         if at_result =='':
                #             continue
                #         print(at_result)
        except Exception as e:
            print(e)
              
while True:
    try:
        data = input('>')
    except EOFError:
        break
    if data =='check':
        check_port()
    if data.split(" ")[0] == 'open':
        try:
            com = data.split(" ")[1]
            at_port_open = serial.Serial(com, baudrate=115200, timeout=0.08)
            print("%s串口已打开"%(str(com)))
            t = MyThread(read)
            t.daemon = True
            t.start()
            while True:
                command = str(input(""))
                at_port_open.write(bytes(command+"\r\n","utf-8"))
        except Exception as e:
            print(e)
    if data =='close':
        try:
            if at_port_open.isOpen():
                at_port_open.close()
                print("串口已关闭")
            else:
                print("串口未打开")        
        except Exception as e:
            print(e)
    if data == 'exit':
        sys.exit(0)