import base64
import json
import os
import random
import shutil
import sqlite3
import string
import tempfile
import traceback
import sys

from Crypto.Cipher import AES

from libs.constant import constant
from libs.modules import ModuleInfo

if sys.platform.startswith('win32'):
	from libs.windows.winstructure import Win32CryptUnprotectData
	from modules.windows.credman import Credman

if sys.platform.startswith('linux'):
	from hashlib import pbkdf2_hmac
	from libs.crypto.aes import AESModeOfOperationCBC
	from libs.linux import homes


class Chromium(ModuleInfo):
	def __init__(self, browser_name, paths):
		self.paths = paths if isinstance(paths, list) else [paths]
		self.database_query = 'SELECT action_url, username_value, password_value FROM logins'
		ModuleInfo.__init__(self, browser_name, 'browsers', winapi_used=True)
		self.enc_config = {
			'iv': b' ' * 16,
			'length': 16,
			'salt': b'saltysalt',
			'iterations': 1,
		}
		self.AES_BLOCK_SIZE = 16

	def _get_database_dirs(self):
		"""
        Return database directories for all profiles within all paths
        """
		databases = set()
		for path in [p.format(**constant.profile) for p in self.paths]:
			profiles_path = os.path.join(path, u'Local State')
			if os.path.exists(profiles_path):
				master_key = None
				# List all users profile (empty string means current dir, without a profile)
				profiles = {'Default', ''}

				# Automatic join all other additional profiles
				for dirs in os.listdir(path):
					dirs_path = os.path.join(path, dirs)
					if os.path.isdir(dirs_path) and dirs.startswith('Profile'):
						profiles.add(dirs)

				with open(profiles_path) as f:
					try:
						data = json.load(f)
						# Add profiles from json to Default profile. set removes duplicates
						profiles |= set(data['profile']['info_cache'])
					except Exception:
						pass

				with open(profiles_path) as f:
					try:
						master_key = base64.b64decode(json.load(f)["os_crypt"]["encrypted_key"])
						master_key = master_key[5:]  # removing DPAPI
						master_key = Win32CryptUnprotectData(master_key, is_current_user=constant.is_current_user,
															 user_dpapi=constant.user_dpapi)
					except Exception:
						master_key = None

				# Each profile has its own password database
				for profile in profiles:
					# Some browsers use names other than "Login Data"
					# Like YandexBrowser - "Ya Login Data", UC Browser - "UC Login Data.18"
					try:
						db_files = os.listdir(os.path.join(path, profile))
					except Exception:
						continue
					for db in db_files:
						if db.lower() in ['login data', 'ya passman data']:
							databases.add((os.path.join(path, profile, db), master_key))
		return databases

	def _decrypt_v80(self, buff, master_key):
		try:
			iv = buff[3:15]
			payload = buff[15:]
			cipher = AES.new(master_key, AES.MODE_GCM, iv)
			decrypted_pass = cipher.decrypt(payload)
			if sys.platform.startswith('win32'):
				decrypted_pass = decrypted_pass[:-16].decode()  # remove suffix bytes
			elif sys.platform.startswith('linux'):
				decrypted_pass = decrypted_pass[:-16]
			return decrypted_pass

		except:
			pass

	def _export_credentials(self, db_path, is_yandex=False, master_key=None):
		"""
        Export credentials from the given database

        :param unicode db_path: database path
        :return: list of credentials
        :rtype: tuple
        """
		credentials = []
		yandex_enckey = None

		if is_yandex:
			try:
				credman_passwords = Credman().run()
				for credman_password in credman_passwords:
					if b'Yandex' in credman_password.get('URL', b''):
						if credman_password.get('Password'):
							yandex_enckey = credman_password.get('Password')
							self.info('EncKey found: {encKey}'.format(encKey=repr(yandex_enckey)))
			except Exception:
				self.debug(traceback.format_exc())
				# Passwords could not be decrypted without encKey
				self.info('EncKey has not been retrieved')
				return []

		try:
			conn = sqlite3.connect(db_path)
			cursor = conn.cursor()
			cursor.execute(self.database_query)
		except Exception:
			self.debug(traceback.format_exc())
			return credentials

		for url, login, password in cursor.fetchall():
			try:
				# Yandex passwords use a masterkey stored on windows credential manager
				# https://yandex.com/support/browser-passwords-crypto/without-master.html
				if is_yandex and yandex_enckey:
					try:
						try:
							p = json.loads(str(password))
						except Exception:
							p = json.loads(password)

						password = base64.b64decode(p['p'])
					except Exception:
						# New version does not use json format
						pass

				# Passwords are stored using AES-256-GCM algorithm
				# The key used to encrypt is stored on the credential manager

				# yandex_enckey:
				#   - 4 bytes should be removed to be 256 bits
				#   - these 4 bytes correspond to the nonce ?

				# cipher = AES.new(yandex_enckey, AES.MODE_GCM)
				# plaintext = cipher.decrypt(password)
				# Failed...
				else:
					# Decrypt the Password
					if password and password.startswith(b'v10'):  # chromium > v80
						if master_key:
							password = self._decrypt_v80(password, master_key)
					else:
						try:
							password_bytes = Win32CryptUnprotectData(password, is_current_user=constant.is_current_user,
																	 user_dpapi=constant.user_dpapi)
						except AttributeError:
							try:
								password_bytes = Win32CryptUnprotectData(password,
																		 is_current_user=constant.is_current_user,
																		 user_dpapi=constant.user_dpapi)
							except:
								password_bytes = None

						if password_bytes not in [None, False]:
							password = password_bytes.decode("utf-8")

				if not url and not login and not password:
					continue

				credentials.append((url, login, password))
			except Exception:
				self.debug(traceback.format_exc())

		conn.close()
		return credentials

	def copy_db(self, database_path):
		"""
        Copying db will bypass lock errors
        Using user tempfile will produce an error when impersonating users (Permission denied)
        A public directory should be used if this error occured (e.g C:\\Users\\Public)
        """
		random_name = ''.join([random.choice(string.ascii_lowercase) for i in range(9)])
		root_dir = [
			tempfile.gettempdir(),
			os.environ.get('PUBLIC', None),
			os.environ.get('SystemDrive', None) + '\\',
		]
		for r in root_dir:
			try:
				temp = os.path.join(r, random_name)
				shutil.copy(database_path, temp)
				self.debug(u'Temporary db copied: {db_path}'.format(db_path=temp))
				return temp
			except Exception:
				self.debug(traceback.format_exc())
		return False

	def clean_file(self, db_path):
		try:
			os.remove(db_path)
		except Exception:
			self.debug(traceback.format_exc())

	def get_paths(self):
		for profile_dir in homes.get(directory=self.paths):
			try:
				subdirs = os.listdir(profile_dir)
			except Exception:
				continue

			for subdir in subdirs:
				login_data = os.path.join(profile_dir, subdir, 'Login Data')
				if os.path.isfile(login_data):
					yield login_data

	def remove_padding(self, data):
		"""
		Remove PKCS#7 padding
		"""
		nb = data[-1]

		try:
			return data[:-nb]
		except Exception:
			self.debug(traceback.format_exc())
			return data

	def chrome_decrypt(self, encrypted_value, key, init_vector):
		encrypted_value = encrypted_value[3:]
		aes = AESModeOfOperationCBC(key, iv=init_vector)
		cleartxt = b"".join([aes.decrypt(encrypted_value[i:i + self.AES_BLOCK_SIZE])
							 for i in range(0, len(encrypted_value), self.AES_BLOCK_SIZE)])
		return self.remove_padding(cleartxt)

	def get_passwords(self, path):
		try:
			conn = sqlite3.connect(path)
		except Exception:
			return

		cursor = conn.cursor()
		try:
			cursor.execute('SELECT origin_url,username_value,password_value FROM logins')
			for url, login, password in cursor:
				# Password encrypted on the database
				if password[:3] == b'v10' or password[:3] == b'v11':

					# To decrypt it, Chromium Safe Storage from libsecret module is needed
					if not constant.chrome_storage:
						self.info('Password encrypted and Chrome Secret Storage not found')
						continue

					else:
						psswrd = password
						try:
							for css in constant.chrome_storage:
								enc_key = pbkdf2_hmac(
									hash_name='sha1',
									password=css,
									salt=self.enc_config['salt'],
									iterations=self.enc_config['iterations'],
									dklen=self.enc_config['length'])

								try:
									password = self.chrome_decrypt(password, key=enc_key, init_vector=self.enc_config['iv'])
									password = password.decode()
								except UnicodeDecodeError:
									password = self._decrypt_v80(password, enc_key)
								if password:
									break
								else:
									password = psswrd

						except Exception:
							print(traceback.format_exc())

				if login:
					creds = (url, login, password)
					yield creds
		except Exception:
			print(traceback.format_exc())

		finally:
			cursor.close()
			conn.close()
			os.remove(path)

	def run(self):
		credentials = []

		if sys.platform.startswith('win32'):
			for database_path, master_key in self._get_database_dirs():
				is_yandex = False if 'yandex' not in database_path.lower() else True

				# Remove Google Chrome false positif
				if database_path.endswith('Login Data-journal'):
					continue

				self.debug('Database found: {db}'.format(db=database_path))

				# Copy database before to query it (bypass lock errors)
				path = self.copy_db(database_path)
				if path:
					try:
						credentials.extend(self._export_credentials(path, is_yandex, master_key))
					except Exception:
						self.debug(traceback.format_exc())
					self.clean_file(path)

		elif sys.platform.startswith('linux'):
			for path in self.get_paths():
				tmp = u'/tmp/chrome.db'
				shutil.copyfile(path, tmp)

				for pw in self.get_passwords(tmp):
					credentials.append(pw)

		return [{'Source': self.name, 'URL': url, 'Login': login, 'Password': password} for url, login, password in
				set(credentials)]
