from keje_framework import Keje
from router import Router
import signal
import sys

kf = Keje()
router = Router(kf)

kf.router = router.router
kf.start()

def signal_handler(signal, frame):
	print("Server closing...")
	sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.pause()
