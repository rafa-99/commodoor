from libs.modules import run_module
from libs.io import string_passwords
from modules.modules_manager import ModuleManager

if __name__ == '__main__':
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
