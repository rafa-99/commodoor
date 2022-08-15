import os
import sys

from libs.modules import ModuleInfo

if sys.platform.startswith('win32'):
	from libs.constant import constant

if sys.platform.startswith('linux'):
	from libs.linux import homes


class Openssh(ModuleInfo):
	def __init__(self):
		ModuleInfo.__init__(self, 'openssh', 'sysadmin')

	def get_ids(self):
		known = set()
		for user, identity in homes.users(file=[
			os.path.join('.ssh', item) for item in (
					'id_rsa', 'id_rsa.pub', 'id_dsa', 'id_dsa.pub', 'id_ecdsa', 'id_ecdsa.pub', 'id_ed25519', 'id_ed25519.pub'
			)
		]):
			if os.path.isfile(identity):
				try:
					with open(identity) as fidentity:
						yield {
							'Source': self.name,
							'File': identity,
							'User': user,
							'Key': fidentity.read()
						}
						known.add(identity)
				except Exception:
					pass

		for user, config in self.get_configs():
			for pw in self.get_ids_from_config(user, config):
				if pw['KEY'] in known:
					continue

				try:
					with open(pw['KEY']) as fidentity:
						pw['KEY'] = fidentity.read()
						yield pw
						known.add(identity)
				except Exception:
					pass

	def get_configs(self):
		return homes.users(file=os.path.join('.ssh', 'config'))

	def create_pw_object(self, identity, host, port, user):
		pw = {'KEY': identity}
		if host:
			pw['Host'] = host
		if port:
			pw['Port'] = port
		if user:
			pw['Login'] = user
		return pw

	def get_ids_from_config(self, default_user, config):
		try:
			hostname = None
			port = 22
			user = default_user
			identity = None

			with open(config) as fconfig:
				for line in fconfig.readlines():
					line = line.strip()

					if line.startswith('#'):
						continue

					line = line.split()
					if len(line) < 2:
						continue

					cmd, args = line[0].lower(), line[1:]
					args = ' '.join([x for x in args if x])

					if cmd == 'host':
						if identity:
							yield self.create_pw_object(
								identity, hostname, port, user
							)

						hostname = None
						port = 22
						user = default_user
						identity = None

					elif cmd == 'hostname':
						hostname = args

					elif cmd == 'user':
						user = args

					elif cmd == 'identityfile':
						if args.startswith('~/'):
							args = config[:config.find('.ssh')] + args[2:]
						identity = args

			if identity:
				yield self.create_pw_object(
					identity, hostname, port, user
				)

		except Exception as e:
			pass

	def extract_private_keys_unprotected(self):
		"""
		Extract all DSA/RSA private keys that are not protected with a passphrase.

		:return: List of encoded key (key file content)
		"""
		keys = []
		if os.path.isdir(self.key_files_location):
			for (dirpath, dirnames, filenames) in os.walk(self.key_files_location, followlinks=True):
				for f in filenames:
					key_file_path = os.path.join(dirpath, f)
					if os.path.isfile(key_file_path):
						try:
							# Read encoded content of the key
							with open(key_file_path, "r") as key_file:
								key_content_encoded = key_file.read()
							# Determine the type of the key (public/private) and what is it algorithm
							if "DSA PRIVATE KEY" in key_content_encoded:
								key_algorithm = "DSA"
							elif "RSA PRIVATE KEY" in key_content_encoded or "OPENSSH PRIVATE KEY" in key_content_encoded:
								key_algorithm = "RSA"
							else:
								key_algorithm = None
							# Check if the key can be loaded (used) without passphrase
							# if key_algorithm is not None and self.is_private_key_unprotected(key_content_encoded,
							#                                                                    key_algorithm):
							if key_algorithm:
								keys.append(key_content_encoded)
						except Exception as e:
							self.error(u"Cannot load key file '%s' '%s'" % (key_file_path, e))
							pass

		return keys

	def run(self):
		if sys.platform.startswith('win32'):
			self.key_files_location = os.path.join(constant.profile["USERPROFILE"], u'.ssh')
			unprotected_private_keys = self.extract_private_keys_unprotected()
			found_keys = list()
			for key in unprotected_private_keys:
				values = {"Private Key": key}
				found_keys.append(values)

		elif sys.platform.startswith('linux'):
			return list(self.get_ids())
