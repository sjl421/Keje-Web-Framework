from Keje import app
from router import Router
import signal
import sys

app = app()
router = Router(app)

app.router = router.router
app.start()

def signal_handler(signal, frame):
	print("Server closing...")
	sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.pause()
