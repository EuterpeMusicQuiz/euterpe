# -*- coding: utf-8 -*-

class Sample(object):
    def __init__(self, sample_id, song_id, artists, title, sample_file):
        self._artists = artists
        self._title = title
        self._id = sample_id
        self._song_id = song_id
        self._file = sample_file

    def __repr__(self):
        return "<Sample #{0}, Song #{1}: {2} from {3}, File: \"{4}\">\n".format(self._id, self._song_id, self._title, self._artists, self._file)

    def getId(self):
        return self._id

    def getSongId(self):
        return self._song_id

    def getArtists(self):
        return self._artists

    def getTitle(self):
        return self._title

    def getFile(self):
        return self._file

class Song(object):
    def __init__(self, song_id, artists, title):
        self._artists = artists
        self._title = title
        self._id = song_id

    def __repr__(self):
        return "<Song #{0}: {1} from {2}>\n".format(self._id, self._title, self._artists)
        
    def getId(self):
        return self._id

    def getArtists(self):
        return self._artists

    def getTitle(self):
        return self._title
