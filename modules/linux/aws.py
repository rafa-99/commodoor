import os

from libs.modules import ModuleInfo
from libs.linux import homes

from configparser import ConfigParser


class Aws(ModuleInfo):
	def __init__(self):
		ModuleInfo.__init__(self, 'aws', 'sysadmin')

	def get_paths(self):
		return homes.get(file=os.path.join('.aws', 'credentials'))

	def get_creds(self, path):
		try:
			parser = ConfigParser()
			parser.read(path)
		except Exception:
			return

		for section in parser.sections():
			try:
				key = parser.get(section, 'aws_access_key_id')
				secret = parser.get(section, 'aws_secret_access_key')
				yield section, key, secret
			except Exception:
				continue

	def run(self):
		all_passwords = []
		for path in self.get_paths():
			for section, key, secret in self.get_creds(path):
				all_passwords.append({
					'Source': self.name,
					'Id': key,
					'Key': secret,
					'Service': 'AWS',
					'Name': section
				})

		return all_passwords
