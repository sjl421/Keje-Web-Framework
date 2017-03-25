import socket
from threading import Thread

class Server(object):

	def __init__(self, host='', port=3000, handler=None):
		self.host = host
		self.port = port
		self.handler = handler

	def create_socket(self):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

	def listen_socket(self):
		self.sock.bind((self.host,self.port))
		self.sock.listen(5) # request queue
		print('Server created and listening on port {port}'.format(port=self.port))
		while True:
			client_sock, client_address = self.sock.accept()
			th = Thread(target=self.handle_client, args=(client_sock,))
			th.daemon = True
			th.start()

	def handle_client(self, client_sock):
		request = client_sock.recv(1024)
		self.handler(client_sock, request)

	def _start(self):
		self.create_socket()
		self.listen_socket()

	def start(self):
		t = Thread(target=self._start, args=())
		t.daemon = True
		t.start()




