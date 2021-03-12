# -*- coding: utf-8 -*-

"""
File which consists of a sole function <onset_times>.
Concisely, it provides a list of time values for a song.
Each of these times corresponds to an interesting onset time for a sample.
"""

from euterpe.analyzer.process import process
from euterpe.analyzer.analyze import compute_energy
from euterpe.analyzer.utils import labeled_values
from euterpe.analyzer.config import N_SECONDS, N_ZONES

from random import randint

# First version solely based on energy
def onset_times(song, n_samples, sample_duration):
    '''
    Takes a path to an audio file
    Returns a list of <n_samples> values, each value corresponding to the starting time of a sample of <sample_duration> seconds
    Condition : <sample_duration> shorter than the song duration, preferably at most a third of it
    '''
    frames, duration = process(song)
    assert(sample_duration <= duration)

    # Computing song energy and discretizing energies into N_ZONES #
    energy = compute_energy(frames)
    energy_zones = labeled_values(energy, N_ZONES)

    # Getting interesting indexes #
    indexes = []
    i = 1
    while i < len(energy_zones) - 1:
        if abs(energy_zones[i + 1] - energy_zones[i - 1]) > max(1, N_ZONES // 5):
            indexes.append(i)
        i += 1

    # Filtering or extending indexes array to have <n_samples> values #
    selected_indexes = []
    if len(indexes) <= n_samples:
        selected_indexes = indexes
        for i in range(len(indexes), n_samples):
            selected_indexes.append(randint(0, len(energy_zones) - 1 - sample_duration // N_SECONDS))
    else:
        for i in range(n_samples):
            selected_indexes.append(indexes[i * (len(indexes) - 1) // n_samples])
            
    # Translating those indexes into starting times for samples #
    times = [index * duration // len(energy_zones) for index in selected_indexes]
    times = [max(0, time - sample_duration // 2) for time in times]
    times = [min(time, duration - sample_duration) for time in times]
    return times
