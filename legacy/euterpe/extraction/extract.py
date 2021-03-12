# -*- coding: utf-8 -*-

"""
Module dedicated to the extraction of samples from a song, and their exportation in the database.
Only paths and metadata are exported, not audio files.
"""

from pydub import AudioSegment

from euterpe.config import get_value
from euterpe.extraction.config import *
from euterpe.extraction.utils import *
from euterpe.misc.utils import get_extension, rdir_generator, rfile_generator
from euterpe.misc.colors import cyan_fg, dim
from euterpe.analyzer.sample_onset import onset_times

from os.path import exists
from os import listdir
from time import time

from progress.bar import ChargingBar

def create_sample(song, dir_path, start_time):
    if get_value('sample', 'mono').lower() == 'true':
        song = song.set_channels(1)

    # Sample creation
    end_time = start_time + SAMPLE_LGTH * 1000
    song = song[start_time:end_time]
    fade_time = FADE_LTH * 1000
    song = song.fade_in(fade_time).fade_out(fade_time)

    # Exporting sample
    sample_path = rfile_generator(dir_path, get_value('sample', 'extension'))#dir_path + '/sample_1.' + get_value('sample', 'extension')
    #i = 2
    #while exists(sample_path):
     #   sample_path = dir_path + '/sample_' + str(i) + '.' + get_value('sample', 'extension')
      #  i += 1
    song.export(sample_path, format=get_value('sample', 'extension'), bitrate=get_value('sample', 'bitrate'), codec=get_value('sample', 'codec'))
    return sample_path

def create_metadata(song_path, sample_dir_path):
    # Samples creation
    dir_path = rdir_generator(sample_dir_path)
    song = AudioSegment.from_file(song_path, format=get_extension(song_path))
    start_times = onset_times(song, N_SAMPLES, SAMPLE_LGTH) 
    for i in range(N_SAMPLES):
        create_sample(song, dir_path, start_times[i] * 1000)

    # Metadata object creation
    metadata = get_metadata(song_path)
    metadata['PATH'] = dir_path
    return metadata

def create_dir_metadata(dir_path, sample_dir_path):
    # Getting the number of audio files in <dir_path>
    lth = 0
    for _file in listdir(dir_path):
        if is_audio_file(dir_path + '/' + _file):
            lth += 1

    # Retrieving metadata for audio files in <dir_path> while creating samples
    metadata_tab = []
    bar = ChargingBar(max=lth, suffix='[%(index)d/%(max)d]')
    for _file in listdir(dir_path):
        if is_audio_file(dir_path + '/' + _file):
            bar.message = INDENT + cyan_fg(_file) + '\n'
            start_time = time()
            metadata_tab.append(create_metadata(dir_path + '/' + _file, sample_dir_path))
            end_time = time()
            elapsed_time = end_time - start_time
            print("\nSong exportation time : " + dim('{:02d}s:{:02d}cs'.format(int(elapsed_time), int((elapsed_time%1)*100))))
            bar.next()
    return metadata_tab
