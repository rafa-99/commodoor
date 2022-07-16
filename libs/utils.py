#!/usr/bin/env python
# -*- coding: utf-8 -*-

def print_debug(error_level, message):
    # Quiet mode => nothing is printed
    if constant.quiet_mode:
        return

    # print when password is found
    if error_level == 'OK':
        constant.st.do_print(message='[+] {message}'.format(message=message), color='green')

    # print when password is not found
    elif error_level == 'FAILED':
        constant.st.do_print(message='[-] {message}'.format(message=message), color='red', intensity=True)

    elif error_level == 'CRITICAL' or error_level == 'ERROR':
        constant.st.print_logging(function=logging.error, prefix='[-]', message=message, color='red', intensity=True)

    elif error_level == 'WARNING':
        constant.st.print_logging(function=logging.warning, prefix='[!]', message=message, color='cyan')

    elif error_level == 'DEBUG':
        constant.st.print_logging(function=logging.debug, message=message, prefix='[!]')

    else:
        constant.st.print_logging(function=logging.info, message=message, prefix='[!]')