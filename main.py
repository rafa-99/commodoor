#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import ctypes
from libs.modules import soft_import
from libs.constant import constant

def get_username_winapi():
    GetUserNameW = ctypes.windll.advapi32.GetUserNameW
    GetUserNameW.argtypes = [ctypes.c_wchar_p, ctypes.POINTER(ctypes.c_uint)]
    GetUserNameW.restype = ctypes.c_uint

    _buffer = ctypes.create_unicode_buffer(1)
    size = ctypes.c_uint(len(_buffer))
    while not GetUserNameW(_buffer, ctypes.byref(size)):
        # WinError.h
        # define ERROR_INSUFFICIENT_BUFFER        122L    // dderror
        if ctypes.GetLastError() == 122:
            _buffer = ctypes.create_unicode_buffer(len(_buffer)*2)
            size.value = len(_buffer)
        
        else:
            return os.getenv('username') # Unusual error

    return _buffer.value

def setenvironment():

    user = get_username_winapi()
    constant.username = user
    template_path = {
        'APPDATA': u'{drive}:\\Users\\{user}\\AppData\\Roaming\\',
        'USERPROFILE': u'{drive}:\\Users\\{user}\\',
        'HOMEDRIVE': u'{drive}:',
        'HOMEPATH': u'{drive}:\\Users\\{user}',
        'ALLUSERSPROFILE': u'{drive}:\\ProgramData',
        'COMPOSER_HOME': u'{drive}:\\Users\\{user}\\AppData\\Roaming\\Composer\\',
        'LOCALAPPDATA': u'{drive}:\\Users\\{user}\\AppData\\Local',
    }

    constant.profile = template_path
    # Get value from environment variables
    for env in constant.profile:
        if os.environ.get(env):
            try:
                constant.profile[env] = os.environ.get(env).decode(sys.getfilesystemencoding())
            except Exception:
                constant.profile[env] = os.environ.get(env)

    # Replace "drive" and "user" with the correct values
    for env in constant.profile:
        constant.profile[env] = constant.profile[env].format(drive=constant.drive, user=user)

if __name__ == '__main__':
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
    setenvironment()
    passwords = firefox_browsers[0].run()
    print(passwords)