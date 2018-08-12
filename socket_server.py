
#和之前写的fork_tcp_server.py一样的功能
#fork + tcp 并发
from socketserver import *

# 创建服务器类
class Server(ForkingMixIn,TCPServer):
#如果要改成线程的话
class Server(ThreadingMixIn,TCPServer):
	pass


# 和上述结果等效---------------------------
# class Server(ForkingTCPServer):
# 	pass
# 创建处理类

class Handler(StreamRequestHandler):
	#当有客户端连接时候调用该函数自动处理
	# 客户端请求事件
	def handle(self):
		print("connect from",self.client_address)
		while True:
			#self.request是tcp中为我们自动生成的和客户端交互的套接字
			data=self.request.recv(1024)
			if not data:
				break
			print("服务器收到：",data)
			self.request.send(b"receive your message")

# 使用创建的服务器类来生产服务器
Server=Server(('127.0.0.1',9999),Handler)

#运行服务器
Server.serve_forever()
