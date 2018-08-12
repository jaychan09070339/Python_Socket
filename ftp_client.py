from socket import *
import sys
import time

class FTPClient(object):
	def __init__(self,sockfd):
		self.sockfd=sockfd
#list
# @客户端请求
# @服务器端确认请求
# @遍历文件夹下文件 然后 把文件名发给客户端
# @客户端接受并打印
	def do_list(self):
		self.sockfd.send(b"list")#发送请求类型
		#接收服务器确认 OK或 failed
		data=self.sockfd.recv(1024).decode()
		if data== "OK":
			while True:
				data=self.sockfd.recv(1024).decode()
				if data =="#####":
					break
				print(data)
			print("文件列表展示完毕")
			return
		else:
			print("文件列表请求失败")
			return


# @客户端请求
# @服务器端确认请求
# @客户端以w打开文件 服务器端r打开
# @服务器read--send 客户端recv--write

	def do_get(self,filename):
		self.sockfd.send(("get"+filename).encode())
		data=self.sockfd.recv(1024).decode()
		if data == "OK":
			fd=open(filename,'w')
			while True:
				data=self.sockfd.recv(1024).decode()
				if data =="##":
					break
				fd.write(data)
			fd.close()
			print("%s下载完成"%filename)
		else:
			print("下载文件失败")
			return
# @客户端请求
# @服务器端确认请求
# @客户端以r打开文件 服务器端w打开
# @服务器recv--write 客户端 read--send
	def do_put(self,filename):
		try:
			fd=open(filename,'rb')
		except:
			print("上传文件不存在")
			return
		self.sockfd.send(b"put")
		self.sockfd.send(("put"+filename).encode())
		data=self.sockfd.recv(1024).decode()
		if data == "OK":
			for line in fd:
				self.sockfd.send(line)
			time.sleep(0.1)
			self.sockfd.send(b"######")
			print("上传%s文件完成"%filename)
		else:
			print("上传文件失败")
			return

	def do_quit(self):
		self.sockfd.send(b"quit")



def main():
	if len(sys.argv)!=3:
		print("argv is error!")
		sys.exit(1)
	HOST=sys.argv[1]
	PORT=int(sys.argv[2])
	ADDR=(HOST,PORT)
	BUFFERSIZE=1024
	sockfd=socket()
	sockfd.connect(ADDR)
	ftp=FTPClient(sockfd)
	sockfd.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
	while True:
		print("*****命令选项********")
		print("*****list**********")
		print("*****get file******")
		print("*****put file******")
		print("*****quit**********")
		data=input("输入命令>>")

		if data=="list":
			ftp.do_list()
		elif data[:3]=="get":
			filename=data.split(" ")[-1]
			ftp.do_get(filename)
		elif data[:3]=="put":
			filename=data.split(" ")[-1]
			ftp.do_put(filename)
		elif data[:4]=="quit":
			ftp.do_quit()
			sockfd.close()
			sys.exit(0)
		else:
			print("请输入正确命令！")




if __name__ =="__main__":
	main()