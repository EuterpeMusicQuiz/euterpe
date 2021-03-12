# -*- coding: utf-8 -*-
import configparser
from sys import platform
import os

from euterpe.misc import colors

class ConfigNotFoundError(Exception):
    pass

class ConfigError(Exception):
    pass

def get_path_linux():
    home = os.environ['HOME']
    for path in [home+'/.config/euterpe.conf', home+'/euterpe.conf', '/etc/euterpe.conf']:
        if os.path.exists(path):
            return path
    raise ConfigNotFoundError
    
def get_path(path=None):
    if path != None:
        if os.path.exists(path):
            return path
        else :
            print("Config file '{}' not found...".format(path))

    if platform.startswith('linux'):
        return get_path_linux()

    print("No default config file location has been set for your platform ({0}) currently... please specify the config file location explicitly.".format(platform))
    raise ConfigNotFoundError

CONFIG = None

def init(path=None):
    path = get_path(path)
    print("Using config file at '{}'".format(colors.yellow_fg(path)))
    global CONFIG
    CONFIG = configparser.ConfigParser()
    try:
        CONFIG.read(path)
    except Exception:
        raise ConfigError("Your config file at {0} contains errors...".format(path))

def get_value(section, key):
    global CONFIG
    if CONFIG == None:
        print("Config not initialized")
        raise ConfigError
    try:
        return CONFIG[section][key]
    except Exception:
        raise ConfigError("Couldn't get value of item {1} in section {0}".format(section, key))
