import re
class Router:
	def __init__(self, keje_framework):
		self.kf = keje_framework

	def router(self, request, client_sock):
		self.request = request
		self.client_sock = client_sock
		if(request['url'] == "/"):
			self.index()
		elif(request['url'] == '/users'):
			self.users()
		elif( re.match( '/user/[0-9]+', request['url'] ) ):
			id = request['url']
			id = id[id.rfind('/')+1:len(id)]
			self.user(id)
		else:
			self.not_found()
		return

	def index(self):
		data = { 'message': 'Keje, Web Framework!', 'id': 5 }
		self.kf.response(self.client_sock, 'hello', data=data)

	def users(self):
		self.kf.response(self.client_sock, 'users', data={})

	def user(self, id):
		data = { 'id': id }
		self.kf.response(self.client_sock, 'user', data=data)

	def not_found(self):
		self.kf.response(self.client_sock,  data={}, status_code=404)
