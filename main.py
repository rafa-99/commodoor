import argparse

from libs.modules import run_module
from libs.io import string_passwords, write_to_file
from modules.modules_manager import ModuleManager

if __name__ == '__main__':

# 	parser = argparse.ArgumentParser()
# 	parser.add_argument("mode", help="select your mode", choices=['attack', 'decrypt', 'genkeys', 'read'])
# 	parser.add_argument("-t", "--targets", help="sets the attack targets")
# 	parser.add_argument("-k", "--key", help="set the key file path")
# 	parser.add_argument("-i", "--input", help="set the input file path")
# 	parser.add_argument("-o", "--output", help="sets the output file path")
# 	args = parser.parse_args()
#
# 	match args.mode:
# 		case 'attack':
# 			if args.targets:
# 				print(args.targets)
# 				if args.output:
# 					print(args.output)
# 					if args.key:
# 						print(args.key)
# 		case 'decrypt':
# 			if args.input:
# 				print(args.input)
# 				if args.key:
# 					print(args.key)
# 		case 'genkeys':
# 			print(args.mode)
# 		case 'read':
# 			if args.input:
# 				print(args.input)
#
# 	print(args)

# -----------------------------------------

	passwords = []
	manager = ModuleManager()

# -----------------------------------------

	manager.select_target_modules('all')
	drivers = manager.factory_drivers()
	for driver in drivers:
		run_module(passwords, driver)

	stringed_passwords = string_passwords(passwords)
	print(stringed_passwords)
	# write_to_file(stringed_passwords)
