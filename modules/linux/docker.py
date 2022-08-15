import json
import os

from libs.modules import ModuleInfo
from libs.linux import homes


class Docker(ModuleInfo):
	def __init__(self):
		ModuleInfo.__init__(self, 'docker', 'sysadmin')

	def get_paths(self):
		return homes.get(file=os.path.join('.docker', 'config.json'))

	def get_creds(self, path):
		try:
			with open(path) as config:
				config = json.load(config)
				if 'auths' not in config:
					return

				for hub, auth in config['auths'].iteritems():
					user, password = auth['auth'].decode('base64').split(':', 1)
					yield hub, user, password
		except Exception:
			return

	def run(self):
		all_passwords = []
		for path in self.get_paths():
			for hub, user, password in self.get_creds(path):
				all_passwords.append(
					{
						'Source': self.name,
						'User': user,
						'Password': password,
						'Hub': hub,
					}
				)

		return all_passwords
