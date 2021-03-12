# -*- coding: utf-8 -*-

"""
Computation functions for audio analysis.
The first pack of functions is related to frame-scaled computations, such as mean energy and frequencies.
The second pack, on the other hand, is related to song-level computations, such as energy, spectrum and autocorrelation.
"""

from python_speech_features import mfcc
from numpy.fft import fft

from numpy import array, correlate

from euterpe.analyzer.config import *
from euterpe.analyzer.utils import euclidean_distance

## Frame-related functions ##

def compute_mean_energy(frame):
    '''Computes the average energy of a frame'''
    mean_energy = sum(list(map(lambda x : x**2, frame)))
    mean_energy /= len(frame)
    return mean_energy

def compute_frequencies(frame):
    '''Computes the frequency amplitude spectrum of a frame'''
    fft_res = fft(frame)
    frequencies = array(list(map(abs, fft_res[:len(fft_res) // 2])))
    return frequencies

def compute_mfcc(frame):
    '''Computes the mfcc coefficients of a frame'''
    mfcc_lst = mfcc(frame, samplerate=SAMPLE_RATE, winlen=FRAME_SIZE/SAMPLE_RATE, winstep=HOP_SIZE/SAMPLE_RATE, nfft=FFT_SIZE, numcep=N_CEPSTRUM)
    return mfcc_lst[0]

## Song-related functions ##

def compute_energy(frames):
    '''Computes an array of mean energies for a set of frames'''
    energy = array(list(map(compute_mean_energy, frames)))
    return energy

def compute_spectrum(frames):
    '''Computes the average frequency amplitude spectrum of a set of frames'''
    spectrum = sum(array(list(map(compute_frequencies, frames[:-1]))))
    spectrum += compute_frequencies(list(frames[-1]) + [0] * (FRAME_SIZE - len(frames[-1])))
    return spectrum
        
def compute_autocorrelation(frames):
    '''Computes the autocorrelation array from the mean energies of a set of frames'''
    energy = compute_energy(frames)
    autocorrelation = correlate(energy, energy, mode='full')
    return autocorrelation[len(autocorrelation) // 2:]

def compute_mfccs(frames):
    '''Computes an array of mfcc coefficients for a set of frames'''
    mfccs = array(list(map(compute_mfcc, frames)))
    return mfccs

def compute_mfcc_matrix(mfccs):
    '''Computes the autocorrelation matrix resulting from a set of mfcc'''
    mfcc_matrix = []
    for idx1 in range(len(mfccs)):
        mfcc_row = []
        for idx2 in range(idx1 + 1):
            mfcc_row.append(0)
        for idx2 in range(idx1 + 1, len(mfccs)):
            mfcc_row.append(euclidean_distance(mfccs[idx1], mfccs[idx2]))
        mfcc_matrix.append(mfcc_row)
        
    # Applying symmetry
    for idx1 in range(len(mfccs)):
        for idx2 in range(idx1):
            mfcc_matrix[idx1][idx2] = mfcc_matrix[idx2][idx1]

    # Normalisation
    mfcc_matrix = array(mfcc_matrix) / max(max(mfcc_matrix))
    return mfcc_matrix
