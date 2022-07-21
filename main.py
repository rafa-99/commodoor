from libs.modules import run_module
from modules.modules_manager import ModuleManager

if __name__ == '__main__':
	passwords = []
	manager = ModuleManager()

	# -----------------------------------------
	manager.select_target_modules('all')
	drivers = manager.factory_drivers()
	for driver in drivers:
		run_module(passwords, driver)

	print(passwords)

	# -----------------------------------------

	# file = open('results.txt', 'w')
	# file.write("-----------------------------------------\n")
	# for password in passwords:
	# 	for key, value in password.items():
	# 		file.write(key + " : " + value + "\n")
	# 	file.write("-----------------------------------------\n")
	# file.close()

	# -----------------------------------------
