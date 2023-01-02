import ftplib, os
from dotenv import load_dotenv
from dateutil import parser
from datetime import timedelta, datetime
class FTPClient:
	def __init__(self):
		load_dotenv("/opt/ftpdamon/")
		self.client = ftplib.FTP(host=os.getenv("FTP_HOST"))
		self.client.login(user=os.getenv("FTP_USER"), passwd=os.getenv("FTP_PASSWD"))
		self.client.cwd(os.getenv("FTP_REMOTE_ROOT"))
	def __del__(self):
		self.client.close()
	def download(self, filename : str) -> bool:
		with open(filename, 'wb') as fp:
			return self.client.retrbinary("RETR {}".format(filename.split('/')[-1]), fp.write).split(' ')[0] == 2
	def upload(self, filename : str) -> bool:
		with open(filename, 'rb') as fp:
			return self.client.storbinary("STOR {}".format(filename.split('/')[-1]), fp)[0] == 2
	def checkMDTM(self, filename : str) -> datetime:
		timestamp = self.client.voidcmd("MDTM {}".format(filename))[4:].strip()
		return parser.parse(timestamp) + timedelta(hours=int(os.getenv("FTP_TIME_DIFF"))*-1)
	def isRemoteNewer(self, filename : str) -> bool:
		try:
			srvTime = self.checkMDTM("{}".format(filename.split('/')[-1]))
			locTime = parser.parse(datetime.fromtimestamp(os.path.getmtime(filename)).strftime('%Y%m%d%H%M%S'))
		except ftplib.error_perm as e:
			return False
		except IOError as e:
			return True
		else:
			return srvTime > locTime
	def listFiles(self) -> list:
		res = []
		files = self.client.nlst()
		for f in files:
			if f[0] != '.':
				res.append(f)
		return res
client = FTPClient()