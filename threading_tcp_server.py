
from socket import *
import threading
import os

#有客户端断开则关闭相应的子线程
def handler():
	while True:
	try:
		c,addr=s.accept()
	except KeyboardInterrupt:
		print("服务器结束")
		s.close()

# 创建套接字 绑定 监听
HOST="127.0.0.1"
PORT=8888
ADDR=(HOST,PORT)
BUFFERSIZE=1024

s=socket()
s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
s.bind(ADDR)
s.listen(5)
# 接收客户端连接请求 创建新的线程
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
	#分支线程处理客户端事件
	t=threading.Thread(target=handler,args=(c,))
	t.setDaemon(True)#不设置join
	t.start()
# 主线程继续接收下一个客户端连接请求
#线程可以连接数量会比进程多很多
