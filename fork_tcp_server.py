
from socket import * 
import os
import signal #主进程不退出 子进程先退出 处理僵尸进程

def hander(c):
	while True:
		data=c.recv(BUFFERSIZE).decode()
		if not data:
			break
		print("服务器收到",data)
		c.send(b'receive your message')
	c.close()
	os._exit(0)


# 创建套接字 绑定监听
HOST="127.0.0.1"
PORT=8888
ADDR=(HOST,PORT)
BUFFERSIZE=1024

s=socket()
s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
s.bind(ADDR)
s.listen(5)

signal.signal(signal.SIGCHLD,signal.SIG_IGN)

# 接收客户端连接请求 创建新的进程
while True:
	try:
		c,addr=s.accept()
	except KeyboardInterrupt:
		print("服务器结束")
		s.close()
		os._exit(0)
	except Exception:
		continue
	print("接收到客户端连接",c.getpeername())

	pid=os.fork()#产生分叉，主进程和子进程开始创建分工
	if pid<0:
		print("创建子进程失败")
	elif pid==0:
		s.close()#s用不到就关闭
		print("处理客户端请求事件")# 子进程处理客户端事件
		handler(c)#处理客户端的函数
	else:
		c.close()#c用不到就关闭
		continue# 主进程继续接受下一个客户端连接请求 




# 有客户端断开则关闭相应的子进程