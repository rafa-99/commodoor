from libs.modules import run_module
from modules.modules_manager import ModuleManager

if __name__ == '__main__':
	passwords = []
	manager = ModuleManager()

	# -----------------------------------------
	manager.select_target_modules('ALL')
	drivers = manager.prepare_modules_drivers()
	for driver in drivers:
		run_module(passwords, driver)
	print(passwords)
	# -----------------------------------------
