from server import Server
from jinja2 import Template
from request_handler import HTTPRequest
import types
import re

class Keje(object):

	def __init__(self,host='', port=3000, router=None):
		self.server = Server(host, port)
		self.router = router
		self.views_folder = 'views'
		self.content_type = "text/html"

	def start(self):
		self.server.start()
		self.server.handler = self.request_handler

	def request_handler(self, client_sock, request):
		parsed_request = self.parse_request(request)
		if('.js' in parsed_request.path or '.css' in parsed_request.path ):
			self.read_assets(parsed_request, client_sock)
		else:
			self.router(parsed_request, client_sock)
	
	def parse_request(self, request):
		parsed_request = HTTPRequest(request)
		return parsed_request

	def read_assets(self,request, client_sock): # read js or css files
		if( '.js' in request.path or '.css' in request.path):
			self.response(client_sock, request.path, is_asset=True)

	def response(self, client_sock, filename='hello.html', data={}, status_code=200, is_asset=False): #send response with optional parameters
		if(status_code != 404):
			if(not is_asset):
				filename = self.views_folder + '/' + filename + '.html'
				self.content_type = "text/html"
			else:
				filename = '.' + filename
				if('.js' in filename):
					self.content_type = 'text/javascript'
				elif('.css' in filename):
					self.content_type = 'text/css'
			
			client_sock.send('HTTP/1.1 {status_code} OK\r\n'.format(status_code=status_code))
			client_sock.send("server: gws\r\n")
			client_sock.send("content-type: {ct}; charset=UTF-8\r\n\r\n".format(ct=self.content_type))
			client_sock.send( self.read_file(filename, data) )

		else:
			client_sock.send('HTTP/1.1 {status_code} OK\r\n'.format(status_code=status_code))
			client_sock.send("server: gws\r\n")
			client_sock.send("content-type: text/plain; charset=UTF-8\r\n\r\n")
			client_sock.send("404! File not found!")

		client_sock.close()

	def read_file(self, filename, data={}):
		with open(filename, 'r') as read_file:
			file_contains = read_file.read()
		if('.html' in filename):
			file_contains = self.paste_template(file_contains, data)
		return file_contains

	def paste_template(self, file, data):
		template = Template(file)
		return template.render(data)
