# -*- coding: utf-8 -*-

"""
Auxiliary functions :
- <is_audio_file>
- <get_metadata>
They pretty much speak for themselves...
"""

from euterpe.extraction.config import AUDIO_EXTENSIONS, METADATA
from euterpe.misc.utils import get_extension
from euterpe.misc.colors import bright

from os.path import isfile
from pydub.utils import mediainfo

# TODO : build an exception class NotAudioFile

# import fleep to check if file is audio file
def is_audio_file(file_path):
    '''Checks whether file at <file_path> is an audio file or not'''
    return get_extension(file_path) in AUDIO_EXTENSIONS and isfile(file_path)

def get_metadata(song_path):
    '''Returns the metadata of the file corresponding to <song_path>'''
    metadata = dict()
    if not is_audio_file(song_path):
        print(bright(song_path) + " is not an audio file")
        return metadata
    else:
        songinfo = mediainfo(song_path)
        if 'TAG' not in songinfo:
            print(bright(song_path) + " has not metadata")
            return metadata
        for field in METADATA:
            if field in songinfo['TAG']:
                metadata[field] = songinfo['TAG'][field]
            else:
                metadata[field] = None
        return metadata
