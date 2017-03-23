from server import Server
import types
import re

class Keje(object):

	def __init__(self,host='', port=3000, router=None):
		self.server = Server(host, port)
		self.router = router
		self.views_folder = 'views'

	def start(self):
		self.server.start()
		self.server.handler = self.request_handler

	def request_handler(self, client_sock, request):
		for line in request.strip().splitlines():
			if 'HTTP/1.1' in line:
				r = line.split(" ")
				new_request={}
				new_request['method'] = r[0]
				new_request['url'] = r[1]
				new_request['http'] = r[2]
				if( '.js' in r[1] or '.css' in r[1]):
					self.read_assets(new_request, client_sock)
				elif(new_request['method'] == 'GET'):
					self.router(new_request, client_sock)
				break

	def read_assets(self,request, client_sock): # read js or css file and response
		if( '.js' in request['url']):
			self.response(client_sock, request['url'], is_asset=True)

	def response(self, client_sock, filename='hello.html', data={}, status_code=200, is_asset=False):
		if(status_code != 404):
			
			if(not is_asset):
				filename = self.views_folder + '/' + filename + '.html'
			else:
				filename = '.' + filename
			
			client_sock.send('HTTP/1.1 {status_code} OK\r\n'.format(status_code=status_code))
			client_sock.send("server: gws\r\n")
			client_sock.send("content-type: text/html; charset=UTF-8\r\n\r\n")
			client_sock.send( self.read_file(filename, data) )

		else:
			client_sock.send('HTTP/1.1 {status_code} OK\r\n'.format(status_code=status_code))
			client_sock.send("server: gws\r\n")
			client_sock.send("content-type: text/plain; charset=UTF-8\r\n\r\n")
			client_sock.send("404! File not found!")

		client_sock.close()

	def read_file(self, filename, data={}):
		with open(filename, 'r') as htmlfile:
			file = htmlfile.read()
		file = self.paste_template(file, data)
		return file

	def paste_template(self, file, data):
		regex = re.compile('#{\w+}')
		matchs = regex.findall(file)
		if(len(matchs) != 0):
			for m in matchs:
				template = m
				m = m.replace("#", '')
				m = m.replace("{", '')
				m = m.replace("}", '')
				if(m in data):
					file = file.replace(template, str(data[m]))
		return file
