# -*- coding: utf-8 -*-

"""
Auxiliary functions for audio analysis.
Various computations for arrays, such as euclidean distance, along with some plotting functions to visualize results of analyses.
"""

from euterpe.analyzer.config import SAMPLE_RATE

## Various computations ##

def euclidean_distance(lst1, lst2):
    '''
    Takes two numpy arrays of identical size
    Returns their euclidean distance
    '''
    assert(len(lst1) == len(lst2))
    distance = (sum((lst1 - lst2)**2) / len(lst1))**0.5
    return distance

# TODO : Use scipy.interpolate instead (much cleaner)
def labeled_values(values, n_zones):
    '''
    Returns a labeled array with integer values between 0 and n_zones - 1
    Each value is assigned a label depending on its zone
    '''
    assert(n_zones > 1)
    values = sorted(values)
    thresholds = [values[(len(values) - 1) * i // n_zones] + n_zones for i in range(1, n_zones + 1)]
    stepwise_values = []
    for value in values:
        for i in range(n_zones):
            if value <= thresholds[i]:
                stepwise_values.append(i)
                break
    return stepwise_values
 
from numpy import linspace   
import matplotlib.pyplot as plt

## Plotting functions ##

def plot_energy(energy, duration):
    time = linspace(0, duration, len(energy))
    plt.plot(time, energy, label="Energy")
    plt.legend()

def plot_spectrum(spectrum):
    frequency = linspace(0, SAMPLE_RATE / 2, len(spectrum))
    plt.plot(frequency, spectrum, label="Spectrum")
    plt.xscale('log')
    plt.legend()

def plot_autocorrelation(autocorrelation, duration):
    time = linspace(0, duration, len(autocorrelation))
    plt.plot(time, autocorrelation, label="Autocorrelation")
    plt.xscale('log')
    plt.legend()

def plot_mfcc_matrix(mfcc_matrix, duration):
    plt.imshow(mfcc_matrix, cmap=plt.cm.gray, extent=(0, duration, duration, 0))
    plt.title("MFCC Autocorrelation")
    plt.colorbar()
