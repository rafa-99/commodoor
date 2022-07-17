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
