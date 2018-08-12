#!usr/bin/python3
from socket import *

HOST="127.0.0.1"
PORT=10002
ADDR=(HOST,PORT)
BUFFERSIZE=1024
# 创建数据包套接字
sockfd=socket(AF_INET,SOCK_DGRAM,0)

# 消息收发
while True:
	data=input("消息>>")
	if not data:
		break
	sockfd.sendto(data.endcode(),ADDR)
	data,addr=sockfd.recvfrom(BUFFERSIZE)
	print("从服务器接收",data.decode())

# 关闭套接字
sockfd.close()