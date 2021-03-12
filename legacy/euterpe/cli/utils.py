# -*- coding: utf-8 -*-

from euterpe.misc.colors import *

def get_mode_prompt(mode_name):
    return bright("[" + cyan_fg(mode_name) + "] ")
