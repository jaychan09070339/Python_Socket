#!usr/bin/python3
from socket import *
import sys
from time import ctime
#通过参数接收
# HOST=sys.argv[1]
# PORT=sys.argv[2]
BUFFERSIZE=1024#表示一次最多可以接收多少字节的消息
HOST="127.0.0.1"
PORT=10002
ADDR=(HOST,PORT)
# 创建数据包套接字
socketfd=socket(AF_INET,SOCK_DGRAM,0)
# 绑定本地IP和端口
socketfd.bind(ADDR)
# 收发消息
while True:
	data,addr=socketfd.recvfrom(BUFFERSIZE)
	print("receive from",addr,data.decode())
	socketfd.sendto(("在%s接收到你的消息"%ctime()).encode(),addr)
	#addr可以随便发给谁
# 关闭套接字
socketfd.close()