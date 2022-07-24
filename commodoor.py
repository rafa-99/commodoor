import argparse

from libs.crypto.hybrid_rsa import genkeys, encrypt, decrypt
from libs.modules import run_module
from libs.io import string_passwords, write_to_file
from modules.modules_manager import ModuleManager

if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument("mode", help="select your mode", choices=['attack', 'decrypt', 'genkeys', 'read'])
	parser.add_argument("-t", "--targets", help="sets the attack targets", nargs='+')
	parser.add_argument("-k", "--key", help="set the key file path")
	parser.add_argument("-i", "--input", help="set the input file path")
	parser.add_argument("-o", "--output", help="sets the output file path")
	args = parser.parse_args()

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

		case 'read':
			if args.input:
				print('Not Implemented Yet')