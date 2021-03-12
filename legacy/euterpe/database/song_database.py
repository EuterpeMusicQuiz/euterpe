# -*- coding: utf-8 -*-
import euterpe.database.database_requests as sdb
import sqlite3
import euterpe.database.definitions

_DB = None
class song_db(object):
    @classmethod
    def init(cls, db_file_name):
        global _DB
        _DB = SongDB(db_file_name)

    @classmethod
    def get(cls):
        global _DB
        return _DB

class SongDB(object):
    def __init__(self, db_file_name):
        self._name = db_file_name
        try:
            self._conn = sqlite3.connect(self._name)
            self._cursor = self._conn.cursor()
            sdb.create_DB(self._cursor, self._conn)
        except Exception as e:
            print("Error during database creation.\nPlease check that Euterpe has write/read access to the database.")
            if '_conn' in self.__dict__:
                self._conn.rollback()
            exit(1)

    def __repr__(self):
        return "{SongDB: " + self._name + "}"
        
    def __del__(self):
        if '_conn' in self.__dict__:
            self._conn.close()

    def addSong(self, artists, title, year=None, genres=[], language=None, difficulty=None, sample_names = []):
        sdb.add_song(self._cursor, self._conn, artists, title, year, genres, language, difficulty, sample_names)

    def addSamples(self, song_id, sample_names):
        sdb.add_samples(self._cursor, self._conn, sample_names, song_id)

    def removeSample(self, sample_id):
        sdb.remove_sample(self._cursor, self._conn, sample_id)

    def removeSong(self, song_id):
        sdb.remove_song(self._cursor, self._conn, song_id)
        
    def getRandomSamples(self, n, filters=[]):
        if n <= 0:
            return []
        return sdb.get_random_samples(self._cursor, self._conn, n, filters)

    def getAllSamples(self, filters=[], order_by=None):
        return sdb.get_random_samples(self._cursor, self._conn, -1, filters, order_by)

    def getRandomSongs(self, n, filters=[]):
        if n <= 0:
            return []
        return sdb.get_random_songs(self._cursor, self._conn, n, filters)

    def getAllSongs(self, filters=[], order_by=None):
        return sdb.get_random_songs(self._cursor, self._conn, -1, filters, order_by)
    
    def getSongFromId(self, song_id):
        return sdb.get_song_from_id(self._cursor, self._conn, song_id)
    
    def getSampleFromId(self, sample_id):
        return sdb.get_sample_from_id(self._cursor, self._conn, sample_id)

    def getSongsFromArtist(self, artist):
        return sdb.get_songs_from_artist(self._cursor, self._conn, artist)

    def getSamplesFromSongId(self, song_id):
        return sdb.get_samples_from_song_id(self._cursor, self._conn, song_id)
