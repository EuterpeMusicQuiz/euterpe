# -*- coding: utf-8 -*-

'''
Caution : File implies file name
'''

from euterpe.extraction.utils import is_audio_file
from euterpe.misc.utils import get_last_name, smooth_dict
from euterpe.misc.colors import *

class AudioFileManager(object):
    def __init__(self):
        self.audio_files = []

    def __repr__(self):
        return "{AudioFileManager: " + str(len(self.audio_files)) + " audio files}"

    def __del__(self):
        del self.audio_files

    def add_audio_file(self, _file, _metadata = dict()):
        if _file not in [cpl[0] for cpl in self.audio_files] and is_audio_file(_file):
            self.audio_files.append((_file, _metadata))

    def remove_audio_file(self, _file):
        _files = [cpl[0] for cpl in self.audio_files]
        if _file in _files:
            idx = _files.index(_file)
            self.audio_files.remove(self.audio_files[idx])
            
    def add_audio_files(self, _files, _metadata_lst = []):
        idx = 0
        for _file in _files:
            self.add_audio_file(_file, dict() if len(_metadata_lst) <= idx else _metadata_lst[idx])
            idx += 1

    def remove_audio_files(self, _files):
        for _file in _files:
            self.remove_audio_file(_file)

    def clear(self):
        self.audio_files = []

    def list_content(self, only_file = True):
        idx = 0
        for audio_file in self.audio_files:
            print(yellow_fg(str(idx) + " : " + get_last_name(audio_file[0])), end = 2 * ' ') if only_file else print(yellow_fg(str(idx) + " : " + get_last_name(audio_file[0])) + "\n" + smooth_dict(audio_file[1]))
            idx += 1
        if only_file and len(self.audio_files) > 0:
            print()
