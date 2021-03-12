# -*- coding: utf-8 -*-

"""
Module with a unique function <process>.
It basically splits a song (pydub.AudioSegment format) into frames
"""

from numpy import array

from euterpe.analyzer.config import FRAME_SIZE, HOP_SIZE

def process(song):
    '''
    Takes the audio file <song> under pydub.AudioSegment format
    Returns a numpy array of frames along with the song's duration in seconds
    Frames are numpy arrays of identical lengths (apart from the last frame) that contain integers
    '''
    # Song is set in mono by default to ease the treatment
    song = song.set_channels(1)

    # Extracting required information #
    raw_data = list(song.get_array_of_samples())
    duration = song.duration_seconds
    n_frames = song.frame_count()

    # Building the array of frames #
    frames = []
    frame_start_idx = 0
    while frame_start_idx + FRAME_SIZE < n_frames:
        frames.append(raw_data[frame_start_idx:frame_start_idx + FRAME_SIZE])
        frame_start_idx += HOP_SIZE
    frames.append(raw_data[frame_start_idx:])
    frames = array(list(map(array, frames)))
    
    return frames, duration
