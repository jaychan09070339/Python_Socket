from socket import *
import os
import sys
import signal
import time

FILE_PATH="/Users/user/Desktop/"

class FTPServer(object):
	def __init__(self,connfd):
		self.connfd=connfd

	def do_list(self):
		#服务器端确认请求是否可以执行
		filelist=os.listdir(FILE_PATH)
		if filelist==None:
			self.connfd.send(b"failed!")
		else:	
			self.connfd.send(b"OK!")
			time.sleep(0.1)
			for filename in filelist:
				if filename[0]!="." and os.path.isfile(FILE_PATH+filename):
					self.connfd.send(filename.encode())
					time.sleep(0.1)
			self.connfd.send(b"#####")
			print("文件列表发送完毕")
			return



	def do_get(self,filename):
		try:
			fd=open(FILE_PATH+filename,'rb')
		except:
			self.connfd.send(b'failed')
		self.connfd.send(b'OK')
		time.sleep(0.1)
		for line in fd:
			self.connfd.send(line)
		fd.close()
		time.sleep(0.1)
		self.connfd.send(b"#####") 
		print("文件发送成功")
		return


	def do_put(self,filename):
		try:
			fd=open(FILE_PATH+filename,'w')
		except:
			self.connfd.send(b'failed')
		self.connfd.send(b'OK')
		while True:
			data=self.connfd.recv(1024).decode()
			if data=="#####":
				break
			fd.write(data)
		fd.close()
		print("接收文件完毕")
		return


def main():
	if len(sys.argv)!=3:
		print("argv is error!")
		sys.exit(1)
	HOST=sys.argv[1]
	PORT=int(sys.argv[2])
	ADDR=(HOST,PORT)
	BUFFERSIZE=1024


	sockfd=socket()
	sockfd.bind(ADDR)
	sockfd.listen(5)
	signal.signal(signal.SIGCHLD,signal.SIG_IGN)
	sockfd.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
	while True:
		try:
			connfd,addr=sockfd.accept()
		except KeyboardInterrupt:
			sockfd.close()
			sys.exit(0)
		except Exception:
			continue
		print("connect from",addr)
		pid = os.fork()
		if pid < 0:
			print("child process creates failed")
		if pid ==0:
			sockfd.close()#没用就关掉
			ftp=FTPServer(connfd)

			while True:
				#接收客户端请求
				data=connfd.recv(BUFFERSIZE).decode()
				if data[4] =='list':
					print("recv list")
					ftp.do_list()
				elif data[3] == "get":
					print("recv get")
					filename=data.split(" ")[-1]
					ftp.do_get(filename)
				elif data[3] == "put":
					print("recv put")
					ftp.do_put()
				elif data[4] == "quit":
					print("recv quit")
					sockfd.close()
					sys.exit(0)
		else:
			connfd.close()#没用就关掉
			continue





if __name__=="__main__":
	main()