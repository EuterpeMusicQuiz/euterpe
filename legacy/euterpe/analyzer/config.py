# -*- coding: utf-8 -*-

"""
Useful global variables to define audio analysis parameters.
It describes features such as sample rate, frame size and hop size for frames, and fft size for mfccs.
"""

SAMPLE_RATE = 44100

# Frame
N_SECONDS = 4
FRAME_SIZE = SAMPLE_RATE * N_SECONDS
HOP_SIZE = SAMPLE_RATE * N_SECONDS

# MFCC
FFT_SIZE = SAMPLE_RATE * N_SECONDS
N_CEPSTRUM = 11

# Discretization space
N_ZONES = 5
