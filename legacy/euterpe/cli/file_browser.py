# -*- coding: utf-8 -*-

import os
import os.path

# check pathlib for cleaner path manipulation

from euterpe.extraction.utils import is_audio_file
from euterpe.misc.colors import blue_fg
from euterpe.misc.utils import get_last_name

class FileBrowser(object):
    def __init__(self, _dir = None):
        if _dir != None and os.path.exists(_dir) and os.path.isdir(_dir):
            self.directory = os.path.realpath(_dir)
        else:
            self.directory = os.getcwd()
            
    def __repr__(self):
        return "{FileBrowser: " + self.directory + "}"

    def __del__(self):
        del self.directory

    def get_subdirectories(self):
        return [self.directory + '/' + subdir for subdir in os.listdir(self.directory) if os.path.isdir(self.directory + '/' + subdir)]

    def get_files(self, only_audio = False):
        return [self.directory + '/' + _file for _file in os.listdir(self.directory) if os.path.isfile(self.directory + '/' + _file) and (is_audio_file(_file) if only_audio else True)]

    def move_up(self, height = 1):
        for n in range(height):
            if not os.path.exists(self.directory + '/..'):
                break
            self.directory = os.path.realpath(self.directory + '/..')

    def move_in(self, subdir):
        if os.path.exists(self.directory + '/' + subdir) and os.path.isdir(self.directory + '/' + subdir):
            self.directory = self.directory + '/' + subdir

    def move_to(self, dir_path):
        dir_path = os.path.realpath(dir_path)
        if os.path.exists(dir_path) and os.path.isdir(dir_path):
            self.directory = dir_path

    def list_subdirectories(self):
        subdirectories = self.get_subdirectories()
        for subdirectory in subdirectories:
            print(blue_fg(get_last_name(subdirectory)), end = 2 * ' ')
        if len(subdirectories) > 0:
            print()
            
    def list_files(self, only_audio = False):
        files = self.get_files(only_audio)
        for _file in files:
            print(get_last_name(_file), end = 2 * ' ')
        if len(files) > 0:
            print()

    def list_content(self, only_audio = False):
        self.list_subdirectories()
        self.list_files(only_audio)

    
