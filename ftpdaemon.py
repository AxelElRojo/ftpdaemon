from ftp import client
from startup import startup
from inotify import adapters
from dotenv import load_dotenv
import os, fasteners, atexit
load_dotenv("/opt/ftpdamon/")
lock = fasteners.InterProcessLock(os.path.join(os.getenv("FTP_LOCAL_ROOT"), ".ftpdaemon.lock"))
atexit.register(lambda: os.remove(os.path.join(os.getenv("FTP_LOCAL_ROOT"), ".ftpdaemon.lock")))
with lock:
	startup()
	i = adapters.Inotify()
	i.add_watch(os.getenv("FTP_LOCAL_ROOT"))
	for event in i.event_gen(yield_nones=False):
		(_, types, path, filename) = event
		if 'IN_CLOSE_WRITE' in types or 'IN_CLOSE_NOWRITE' in types or 'IN_MODIFY' in types:
			if len(filename) > 0 and filename[0] != '.':
				client.upload(os.path.join(path, filename))