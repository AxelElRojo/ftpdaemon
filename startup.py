import os
from dotenv import load_dotenv
from ftp import client
def startup():
	load_dotenv("/opt/ftpdamon/")
	files = client.listFiles()
	entries = os.scandir(os.getenv("FTP_LOCAL_ROOT"))
	for entry in entries:
		files.append(entry.name)
	files = list(dict.fromkeys(files))
	for file in files:
		if file[0] != '.':
			if client.isRemoteNewer(os.path.join(os.getenv("FTP_LOCAL_ROOT"), file)):
				client.download(os.path.join(os.getenv("FTP_LOCAL_ROOT"), file))
			else:
				client.upload(os.path.join(os.getenv("FTP_LOCAL_ROOT"), file))
if __name__ == '__main__':
	startup()