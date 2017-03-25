import re
import model

class Router:
	def __init__(self, keje_framework):
		self.kf = keje_framework

	def router(self, request, client_sock):
		self.request = request
		self.client_sock = client_sock
		method = request.command
		path = request.path
		request_version = request.request_version
		headers = request.headers
		rfile = request.rfile

		if(path == "/"):
			self.index()
		elif(path == '/users'):
			self.users()
		elif(path == '/create'):
			if(method == 'GET'):
				self.create_user()
			else:
				self.post_create_user(headers, rfile)
		elif(path=='/delete'):
			if(method == 'GET'):
				self.delete_user()
			else:
				self.post_delete_user(headers, rfile)
		elif( re.match( '/user/[0-9]+', path ) ):
			id = path
			id = id[id.rfind('/')+1:len(id)]
			self.user(id)
		else:
			self.not_found()
		return

	def index(self):
		data = { 'message': 'Keje, Web Framework!', 'id': 5 }
		self.kf.response(self.client_sock, 'hello', data=data)

	def users(self):
		data = model.users()
		data = { 'users':data }
		self.kf.response(self.client_sock, 'users', data=data)
	
	def delete_user(self):
		data = {}
		self.kf.response(self.client_sock, 'delete', data=data)

	def post_delete_user(self, headers, rfile):
		length = headers.getheader('content-length')
		posted_data = rfile.getvalue()
		posted_data = posted_data[posted_data.rfind('\n')+1:]
		_id = posted_data.split('=')[1]
		model.post_delete_user(_id)
		self.delete_user()

	def create_user(self):
		data = {}
		self.kf.response(self.client_sock, 'create', data=data)

	def post_create_user(self, headers, rfile):
		length = headers.getheader('content-length')
		posted_data = rfile.getvalue()
		posted_data = posted_data[posted_data.rfind('\n')+1:]
		(_id, _name) = posted_data.split('&')
		_id = _id.split('=')[1]
		_name = _name.split('=')[1]
		model.post_create_user(_id, _name)
		self.create_user()

	def user(self, id):
		data = model.user(id)
		if(data == {}):
			data = { 'name':'not found!' }
		self.kf.response(self.client_sock, 'user', data=data)

	def not_found(self):
		self.kf.response(self.client_sock,  data={}, status_code=404)
