# -*- coding: utf-8 -*-

from colorama import Fore, Style

"""
Module to enhance your strings with colors and emphase
"""

def blue_fg(string):
    '''Colorize <string> in blue'''
    return Fore.BLUE + str(string) + Fore.RESET

def cyan_fg(string):
    '''Colorize <string> in cyan'''
    return Fore.CYAN + str(string) + Fore.RESET

def green_fg(string):
    '''Colorize <string> in green'''
    return Fore.GREEN + str(string) + Fore.RESET

def black_fg(string):
    '''Colorize <string> in black'''
    return Fore.BLACK + str(string) + Fore.RESET

def red_fg(string):
    '''Colorize <string> in red'''
    return Fore.RED + str(string) + Fore.RESET

def yellow_fg(string):
    '''Colorize <string> in yellow'''
    return Fore.YELLOW + str(string) + Fore.RESET

def magenta_fg(string):
    '''Colorize <string> in magenta'''
    return Fore.MAGENTA + str(string) + Fore.RESET

def bright(string):
    '''Brighten <string>, typically similar to bold font'''
    return Style.BRIGHT + str(string) + Style.RESET_ALL

def dim(string):
    '''Gives <string> a sober grey-like font'''
    return Style.DIM + str(string) + Style.RESET_ALL
