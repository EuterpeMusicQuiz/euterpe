# -*- coding: utf-8 -*-

"""
Useful variables for sample exportation and metadata manipulation.
"""

## Sample-related characteristics ##
SAMPLE_LGTH = 30 # seconds
FADE_LTH = 4 # seconds
N_SAMPLES = 3 # samples by song

## Information on audio and metadata composition ##
METADATA = ['ARTIST', 'TITLE', 'DATE', 'GENRE', 'LANGUAGE']
AUDIO_EXTENSIONS = ['8svx', 'aif', 'aifc', 'aiff', 'aiffc', 'al', 'amb', 'amr-nb', 'amr-wb', 'anb', 'au', 'avr', 'awb', 'caf', 'cdda', 'cdr', 'cvs', 'cvsd', 'cvu', 'dat', 'dvms', 'f32', 'f4', 'f64', 'f8', 'fap', 'flac', 'fssd', 'gsm', 'gsrt', 'hcom', 'htk', 'ima', 'ircam', 'la', 'lpc', 'lpc10', 'lu', 'mat', 'mat4', 'mat5', 'maud', 'mp2', 'mp3', 'nist', 'ogg', 'paf', 'prc', 'pvf', 'raw', 's1', 's16', 's2', 's24', 's3', 's32', 's4', 's8', 'sb', 'sd2', 'sds', 'sf', 'sl', 'sln', 'smp', 'snd', 'sndfile', 'sndr', 'sndt', 'sou', 'sox', 'sph', 'sw', 'txw', 'u1', 'u16', 'u2', 'u24', 'u3', 'u32', 'u4', 'u8', 'ub', 'ul', 'uw', 'vms', 'voc', 'vorbis', 'vox', 'w64', 'wav', 'wavpcm', 'wv', 'wve', 'xa', 'xi'] # type ffmpeg -formats to get all supported formats

## Common extensions ##
# {'flac', 'mp3', 'ogg', 'wav'}

## Default folder ##
SONG_DIR_PATH = './songs' # Deprecated, only used in prompt.py

## Miscellaneous ##
INDENT = 4 * " "

