from socket import *

HOST = '172.18.111.179'
PORT = 21567
BUFSIZE = 1024
ADDR = (HOST,PORT)
tcpCliSock = socket(AF_INET,SOCK_STREAM)
tcpCliSock.connect(ADDR)
while True:
    data = bytes(input('>'),encoding = 'utf-8')
    if not data:
        break
    tcpCliSock.send(data)
    data = tcpCliSock.recv(BUFSIZE)
    if not data:
        break
    data = str(data).replace('b\"','').replace("b\'",'').replace('\"','').replace("\'",'')
    print(data)
tcpCliSock.close()