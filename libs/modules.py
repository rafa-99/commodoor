#!/usr/bin/env python
# -*- coding: utf-8 -*-
from libs.output import print_debug
from importlib import import_module

class ModuleInfo(object):

    def __init__(self, name, category, options={}, suboptions=[], registry_used=False, winapi_used=False,
                 system_module=False, dpapi_used=False, only_from_current_user=False):
        self.name = name
        self.category = category
        self.options = {
            'command': '-{name}'.format(name=self.name),
            'action': 'store_true',
            'dest': self.name,
            'help': '{name} passwords'.format(name=self.name)
        }
        self.suboptions = suboptions
        self.registry_used = registry_used
        self.system_module = system_module
        self.winapi_used = winapi_used
        self.dpapi_used = dpapi_used
        self.only_from_current_user = only_from_current_user
        
    def error(self, message):
        print_debug('ERROR', message)

    def info(self, message):
        print_debug('INFO', message)

    def debug(self, message):
        print_debug('DEBUG', message)

    def warning(self, message):
        print_debug('WARNING', message)

class _MOCK_ImportErrorInModule(ModuleInfo):

    def __init__(self, name, exception):
        super(_MOCK_ImportErrorInModule, self).__init__(name, "unused")
        self.__message_to_print = "Module %s is not used due to unresolved dependence:\r\n%s" % (name, str(exception))

    def run(self):
        self.error(self.__message_to_print)


def soft_import(package_name, module_name):
    """ Imports module or return mock object which only print error
    """
    try:
        module = import_module(package_name)
        return getattr(module, module_name)
    except ImportError as ex:

        def get_import_error_mock(module_name, exception):
            return lambda *args, **kwargs: _MOCK_ImportErrorInModule(module_name, exception)

        return get_import_error_mock(module_name, ex)