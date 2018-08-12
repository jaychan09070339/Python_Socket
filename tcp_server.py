
from socket import *

HOST='127.0.0.1'
PORT=8889
ADDR=(HOST,PORT)
BUFFERSIZE=1024#1K
#创建一个tcp流式套接字
sockfd=socket(AF_INET,SOCK_STREAM,0)
sockfd.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)#将端口号设置为立即重用
#绑定本机IP和端口号
sockfd.bind(ADDR)
#将套接字变为可监听套接字
sockfd.listen(5)
while True:
	print("wait for connect....")
		#套接字等待客户端请求
	conn,addr=sockfd.accept()
	print("connect from",addr)
		#消息的收发
	while True:	
		data=conn.recv(BUFFERSIZE)
		if not data:
			break
		print("接收到",data)
		n=conn.send("recv your message".encode())
		print("发送了%d字节的数据"%n)
	#关闭套接字
	conn.close()#表示和客户端断开连接
sockfd.close()#不能再使用socketfd了