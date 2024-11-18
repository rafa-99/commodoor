import base64
import os
import sys

from xml.etree.cElementTree import ElementTree

from libs.modules import ModuleInfo

if sys.platform.startswith('win32'):
	from libs.constant import constant

if sys.platform.startswith('linux'):
	from libs.linux import homes


class Filezilla(ModuleInfo):
	def __init__(self):
		ModuleInfo.__init__(self, 'filezilla', 'sysadmin')

	def run(self):

		if sys.platform.startswith('win32'):
			path = os.path.join(constant.profile['APPDATA'], u'FileZilla')
		else:
			path = ""

		if os.path.exists(path) or sys.platform.startswith('linux'):
			pwd_found = []

			if sys.platform.startswith('win32'):
				files = [u'sitemanager.xml', u'recentservers.xml', u'filezilla.xml']

			elif sys.platform.startswith('linux'):
				files = homes.get(file=[os.path.join(d, f) for d in ('.filezilla', '.config/filezilla')
										for f in ('sitemanager.xml', 'recentservers.xml', 'filezilla.xml')])

			for file in files:
				if sys.platform.startswith('win32'):
					xml_file = os.path.join(path, file)
				elif sys.platform.startswith('linux'):
					xml_file = file

				if os.path.exists(xml_file):
					tree = ElementTree(file=xml_file)
					if tree.findall('Servers/Server'):
						servers = tree.findall('Servers/Server')
					else:
						servers = tree.findall('RecentServers/Server')

					for server in servers:
						host = server.find('Host')
						port = server.find('Port')
						login = server.find('User')
						password = server.find('Pass')

						# if all((host, port, login)) does not work
						if host is not None and port is not None and login is not None:
							values = {
								'Source': self.name,
								'Host': host.text,
								'Port': port.text,
								'Login': login.text,
							}

						if password is not None and password.text is not None:
							if 'encoding' in password.attrib and password.attrib['encoding'] == 'base64':
								values['Password'] = base64.b64decode(password.text)
							else:
								values['Password'] = password.text

						if values:
							pwd_found.append(values)

			return pwd_found
