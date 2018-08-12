
from socket import *

#要链接的服务器的地址信息
HOST='127.0.0.1'
PORT=9999
ADDR=(HOST,PORT)

#创建客户端套接字谣和访问的服务器的套接字类型相同
connfd = socket(AF_INET,SOCK_STREAM)
#连接服务器
connfd.connect(ADDR)
#和服务器进行通信
while True:
	data=input("发送>>")
	if not data:
		break
	connfd.send(data.encode())
	data=connfd.recv(1024)
print("客户端收到",data.decode())

#关闭套接字
connfd.close()
