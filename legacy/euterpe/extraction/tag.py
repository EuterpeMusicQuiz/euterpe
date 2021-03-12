# -*- coding: utf-8 -*-

# TODO : 1. Extract fingerprint and duration (in seconds) from an audio file
#           > For duration : duration = mediainfo(song_path)['duration'] then int(float(duration))
#           > For fingerprint : use Chromaprint (https://acoustid.org/chromaprint, in C)
#        2. Use the AcoustID API to get the metadata of this audio file : https://acoustid.org/webservice
#        3. Replace or complete the song's metadata with the ones retrieved
#           > Retriever the song metadata with get_metadata from utils.py
#           > Replace or complete them with replace_metadata or complete_metadata from modify.py
# OKAY, THIS DOES 1ST AND 2ND STEP : https://pypi.org/project/pyacoustid/

"""
Experimental module !
Uses the AcoustID API to retrieve metadata from a song using its fingerprint.
Allows overwriting/completing its original metadata with the found ones using AcoustID.
"""

from acoustid import fingerprint_file, lookup
from requests import post, codes
from euterpe.extraction.utils import *
from euterpe.extraction.config import INDENT
from euterpe.extraction.modify import replace_metadata
from euterpe.misc.utils import get_extension
from euterpe.misc.colors import cyan_fg

from pydub import AudioSegment
from os import listdir

from progress.bar import ChargingBar

APIKEY = '5dZ7UHKdzAw' # Key for the acoustid API, changes regularly

def retrieve(song_path):
    '''
    Takes a song file at <song_path>
    Returns a tuple (artist, title, date) obtained through AcoustID API
    '''
    # Forming the URL for the request on acoustid API
    url = 'https://api.acoustid.org/v2/lookup'
    duration, fingerprint = fingerprint_file(song_path)
    duration, fingerprint = int(float(duration)), fingerprint.decode()
    url += '?client={0}&meta={1}&duration={2}&fingerprint={3}'.format(APIKEY, 'recordings+releases', duration, fingerprint)
    answer = post(url)
    if answer.status_code != codes.ok:
        answer.raise_for_status()
    data = answer.json()
    titles, artists, dates = [], [], []
    # Filling theses 3 tabs
    for item in data['results']:
        if 'recordings' in item:
            for subitem in item['recordings']:
                if 'title' in subitem:
                    titles.append(subitem['title'])
                if 'artists' in subitem:
                    artists.append(subitem['artists'])
                if 'releases' in subitem:
                    for subsubitem in subitem['releases']:
                        if 'date' in subsubitem:
                            dates.append(subsubitem['date']['year'])
                        #if 'artists' in subitem:
                        #    artists.append(subsubitem['artists'])
    artists = [artist for arr in artists for artist in arr]
    artists = [artist['name'] for artist in artists]
    # Extracting the artist, title and date
    max_count = max([dates.count(date) for date in dates])
    date = None
    for dte in dates:
        if dates.count(dte) == max_count:
            if (date == None):
                date = dte
            elif (dte < date):
                date = dte
    max_count = max([artists.count(artist) for artist in artists])
    artist = None
    for artst in artists:
        if artists.count(artst) == max_count:
            artist = artst
            break
    max_count = max([titles.count(title) for title in titles])
    title = None
    for ttle in titles:
        if titles.count(ttle) == max_count:
            title = ttle
            break
    return artist, title, date

def tag(song_path):
    '''
    Takes a song at <song_path>
    Tags it with metadata retrieved through the AcoustID API
    '''
    metadata = get_metadata(song_path)
    artist, title, date = retrieve(song_path)
    tags = {'ARTIST': artist, 'TITLE': title, 'DATE': date}
    replace_metadata(metadata, tags)
    song = AudioSegment.from_file(song_path, format=get_extension(song_path))
    song.export(song_path, format=get_extension(song_path), tags=metadata)

def tag_dir(dir_path):
    '''
    Takes a directory at <dir_path>
    Tags its content (audio files only) with metadata retrieved through the AcoustID API
    '''
    lth = 0
    for _file in listdir(dir_path):
        if is_audio_file(dir_path + '/' + _file):
            lth += 1
    bar = ChargingBar(max=lth, suffix='[%(index)d/%(max)d]')
    for _file in listdir(dir_path):
        song_path = dir_path + '/' + _file
        if is_audio_file(song_path):
            bar.message = INDENT + cyan_fg(_file) + '\n'
            tag(song_path)
            bar.next()
