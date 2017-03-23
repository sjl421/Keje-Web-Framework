from keje_framework import Keje
from router import Router
import signal
import sys
import re

kf = Keje()
router = Router(kf)

'''def router(request, client_sock):
	if(request['url'] == "/"):
		kf.response(client_sock, 'hello')
	elif(request['url'] == '/users'):
		kf.response(client_sock, 'users')
	elif( re.match( '/user/[0-9]+', request['url'] ) ):
		kf.response(client_sock, 'user')
	else:
		kf.response(client_sock, status_code=404)
'''

kf.router = router.router
kf.start()

def signal_handler(signal, frame):
	print("Server closing...")
	sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.pause()
