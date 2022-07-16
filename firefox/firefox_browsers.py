from libs.modules import soft_import

mozilla_module_location = "firefox.mozilla", "Mozilla"

Mozilla = soft_import(*mozilla_module_location)

# Name, path
firefox_browsers = [
    (u'firefox', u'{APPDATA}\\Mozilla\\Firefox'),
    (u'blackHawk', u'{APPDATA}\\NETGATE Technologies\\BlackHawk'),
    (u'cyberfox', u'{APPDATA}\\8pecxstudios\\Cyberfox'),
    (u'comodo IceDragon', u'{APPDATA}\\Comodo\\IceDragon'),
    (u'k-Meleon', u'{APPDATA}\\K-Meleon'),
    (u'icecat', u'{APPDATA}\\Mozilla\\icecat'),
]

firefox_browsers = [Mozilla(browser_name=name, path=path) for name, path in firefox_browsers]