
#fork + udp 
from socketserver import *

class Server(ForkingUDPServer):
	pass

class Handler(DatagramRequestHandler):
	#udp无连接 所以request的含义不同
	def handle(self):
		data=self.rfile.readline()
		print("接收到了",data.decode())
		self.wfile.write(b'receive message')

server=Server(('127.0.0.1',8888),Handler)
server.serve_forever()