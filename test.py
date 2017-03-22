from keje_framework import Keje
import signal
import sys

kf = Keje()

def router(request, client_sock):
	if(request['url'] == "/"):
		kf.response(client_sock, 'hello')
	else:
		print("404 ===" + request['url'])
		kf.response(client_sock, status_code=404)

kf.router = router
kf.start()

def signal_handler(signal, frame):
	print("Server closing...")
	sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.pause()
