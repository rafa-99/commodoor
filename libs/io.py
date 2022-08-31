import logging

from libs.constant import constant


def print_logging(function, prefix='[!]', message='', color=False, intensity=False):
	if constant.quiet_mode:
		return

	try:
		msg = u'{prefix} {msg}'.format(prefix=prefix, msg=message)
	except Exception:
		msg = '{prefix} {msg}'.format(prefix=prefix, msg=str(message))

	if color:
		function(msg)
	else:
		function(msg)


def do_print(self, message='', color=False, intensity=False):
	# quiet mode => nothing is printed
	if constant.quiet_mode:
		return

	message = self.try_unicode(message)
	if color:
		self.set_color(color=color, intensity=intensity)
		self.print_without_error(message)
		self.set_color()
	else:
		self.print_without_error(message)


def print_debug(error_level, message):
	# Quiet mode => nothing is printed
	if constant.quiet_mode:
		return

	# print when password is found
	if error_level == 'OK':
		do_print(message='[+] {message}'.format(message=message), color='green')

	# print when password is not found
	elif error_level == 'FAILED':
		do_print(message='[-] {message}'.format(message=message), color='red', intensity=True)

	elif error_level == 'CRITICAL' or error_level == 'ERROR':
		print_logging(function=logging.error, prefix='[-]', message=message, color='red', intensity=True)

	elif error_level == 'WARNING':
		print_logging(function=logging.warning, prefix='[!]', message=message, color='cyan')

	elif error_level == 'DEBUG':
		print_logging(function=logging.debug, message=message, prefix='[!]')

	else:
		print_logging(function=logging.info, message=message, prefix='[!]')


def string_passwords(passwords):
	string = ""
	keys = set(password.get('Source') for password in passwords)

	for key in keys:
		string = string + "#########################################\n" + key.title() + "\n" + \
				 "#########################################\n"
		for password in passwords:
			if password.get('Source') == key:
				password.pop('Source')
				if key == 'chromium' or key == 'firefox' or key == 'vault':
					string = string + "URL: " + password.get('URL') + "\n" + \
							 "Login: " + str(password.get('Login')) + "\n" + \
							 "Password: " + str(password.get('Password')) + "\n"

				else:
					for k, v in password.items():
						string = string + str(k) + " : " + str(v) + "\n"
				string = string + "-----------------------------------------\n"
		string = string + "\n"

	return string


def write_to_file(data, path, mode='w'):
	file = open(path, mode)
	file.write(data)
	file.close()


def decode_check(string, encoding='utf-8'):
	if isinstance(string, bytes):
		return string.decode(encoding)
	else:
		return string
