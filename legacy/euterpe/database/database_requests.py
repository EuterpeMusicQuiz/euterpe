# -*- coding: utf-8 -*-
import euterpe.database.serialization as srz
from sqlite3 import IntegrityError
from euterpe.database.definitions import *

SQLITE_CREATE_DB = ["""
CREATE TABLE IF NOT EXISTS songs(
id INTEGER PRIMARY KEY UNIQUE,
artist TEXT,
title TEXT,
year INTEGER,
language TEXT,
difficulty INTEGER,
UNIQUE(artist, title)
)
""",
"""
CREATE TABLE IF NOT EXISTS samples(
id INTEGER PRIMARY KEY,
file TEXT UNIQUE,
song_id INTEGER,
FOREIGN KEY(song_id) REFERENCES songs(id)
)
""",

"""
CREATE TABLE IF NOT EXISTS genres(
id INTEGER PRIMARY KEY,
name TEXT UNIQUE
)
""",

"""
CREATE TABLE IF NOT EXISTS song_genre(
song_id INTEGER,
genre_id INTEGER,
FOREIGN KEY(song_id) REFERENCES songs(id),
FOREIGN KEY(genre_id) REFERENCES genres(id)
PRIMARY KEY (song_id, genre_id)
)

"""
]



def create_DB(cursor, conn):
    for table in SQLITE_CREATE_DB:
        cursor.execute(table)
        conn.commit()

def add_genre(cursor, conn, name):
    name = srz.format_genre(name)
    cursor.execute("INSERT OR IGNORE INTO genres(name) VALUES(?)", (name,))
    conn.commit()
    (res,) = cursor.execute("SELECT id FROM genres WHERE name=?", (name,)).fetchone()
    return res

def add_samples(cursor, conn, samples, song_id):
    samples = srz.format_samples(samples)
    for ext in samples:
        cursor.execute("INSERT OR IGNORE INTO samples(file, song_id) VALUES(?,?)", (ext, song_id))
    conn.commit()

def remove_sample(cursor, conn, sample_id):
    cursor.execute("DELETE FROM samples WHERE samples.id=?", (sample_id,))
    conn.commit()

def remove_song(cursor, conn, song_id):
    cursor.execute("DELETE FROM samples WHERE samples.song_id=?", (song_id,))
    cursor.execute("DELETE FROM songs WHERE songs.id=?", (song_id,))
    conn.commit()
    
def add_song_genre(cursor, conn, song_id, genre_id):
    cursor.execute("INSERT OR IGNORE INTO song_genre(song_id, genre_id) VALUES(?,?)", (song_id, genre_id))
    conn.commit()

def add_song(cursor, conn, artists, title, year, genres, language, difficulty, samples):
    artist = srz.format_artists(artists)
    title = srz.format_title(title)
    year = srz.format_year(year)
    language = srz.format_language(language)
    difficulty = srz.format_difficulty(difficulty)

    cursor.execute("INSERT OR IGNORE INTO songs(artist, title, year, language, difficulty) VALUES(?,?,?,?,?)", (artist, title, year, language, difficulty))
    conn.commit()
    (song_id,) = cursor.execute("SELECT songs.id FROM songs WHERE artist=? AND title=?", (artist, title)).fetchone()

    add_samples(cursor, conn, samples, song_id)

    genre_ids = [add_genre(cursor, conn, g) for g in genres]
    for genre_id in genre_ids:
        add_song_genre(cursor, conn, song_id, genre_id)

    return song_id

def get_song_from_id(cursor, conn, song_id):
    song = cursor.execute("SELECT songs.artist, songs.title FROM songs WHERE songs.id=?", (song_id,) ).fetchone()
    if song == None:
        return None
    return Song(song_id, srz.unformat_artists(song[0]), song[1])
    
def get_sample_from_id(cursor, conn, sample_id):
    sample = cursor.execute("SELECT samples.file, samples.song_id FROM samples WHERE samples.id=?", (sample_id,) ).fetchone()
    if sample == None:
        return None
    song = get_song_from_id(cursor, conn, sample[1])
    return Sample(sample_id, sample[1], song.getArtists(), song.getTitle(), sample[0])

def get_samples_from_song_id(cursor, conn, song_id):
    song = get_song_from_id(cursor, conn, song_id)
    samples = cursor.execute("SELECT samples.id, samples.file FROM samples WHERE samples.song_id=?", (song_id,) ).fetchall()
    return [Sample(sample[0], sample[1], song.getArtists(), song.getTitle(), song_id) for sample in samples]

def get_songs_from_artist(cursor, conn, artist):
    songs = cursor.execute("SELECT songs.id, songs.artist, songs.title FROM songs WHERE songs.artist LIKE ? --case-insensitive", (artist,))
    return [Song(song[0], srz.unformat_artists(song[1]), song[2]) for song in songs]

def get_random_samples(cursor, conn, n, filters, order_by=None):
    return get_random_elements(cursor, conn, n, filters, "samples", order_by)

def get_random_songs(cursor, conn, n, filters, order_by=None):
    return get_random_elements(cursor, conn, n, filters, "songs", order_by)
    
def get_random_elements(cursor, conn, n, filters, elt_type, order_by=None):
    request_songs = "SELECT DISTINCT songs.id, songs.artist, songs.title FROM songs JOIN song_genre ON song_genre.song_id=songs.id JOIN genres ON song_genre.genre_id=genres.id"
    params = []

    if len(filters) != 0:
        request_songs += " WHERE "
    
    for token in filters:
        if isinstance(token, str):
            if token == "(":
                request_songs += "("
            elif token == ")":
                request_songs += ")"
            elif token.lower() == "and":
                request_songs += " AND "
            elif token.lower == "or":
                request_songs += " OR "
            else:
                return None
        else:
            if token[0].lower() == "genre":
                request_songs += "genres.name"
                params.append(srz.format_genre(token[2]))
            elif token[0].lower() == "language":
                request_songs += "songs.language"
                params.append(srz.format_language(token[2]))
            elif token[0].lower() == "year":
                request_songs += "songs.year"
                params.append(srz.format_year(token[2]))
            elif token[0].lower() == "difficulty":
                request_songs += "songs.difficulty"
                params.append(srz.format_difficulty(token[2]))
            elif token[0].lower() == "artist":
                request_songs += "LOWER(songs.artist)"
                params.append(token[2].lower())
            elif token[0].lower() == "title":
                request_songs += "LOWER(songs.title)"
                params.append(token[2].lower())
            else:
                return None
            if token[1].lower() == "eq":
                request_songs += "=?"
            elif token[1].lower() == "ne":
                request_songs += "<>?"
            elif token[1].lower() == "lt":
                request_songs += "<?"
            elif token[1].lower() == "gt":
                request_songs += ">?"
            elif token[1].lower() == "le":
                request_songs += "<=?"
            elif token[1].lower() == "ge":
                request_songs += ">=?"
            elif token[1].lower() == "ct":
                request_songs += " LIKE ?"
                params[-1] = "%" + params[-1] + "%"
            else:
                return None


    if n == -1:
        if order_by == "random":
            request_songs += " ORDER BY RANDOM()"
        elif order_by == "song_id":
            request_songs += " ORDER BY songs.id"
        elif order_by == "artist":
            request_songs += " ORDER BY songs.artist"
        elif order_by == "title":
            request_songs += " ORDER BY songs.title"
    else:
        request_songs += " ORDER BY RANDOM()  LIMIT ?"
        params.append(n)

    songs = cursor.execute(request_songs, params).fetchall()
    if elt_type == "songs":
        return [Song(s[0], srz.unformat_artists(s[1]), s[2]) for s in songs]
    
    res = []
    request = "SELECT samples.id, samples.file FROM samples JOIN songs ON songs.id=samples.song_id WHERE songs.id=?"
    if n == -1:
        request += " ORDER BY samples.id"
    else:
        request += " ORDER BY RANDOM() LIMIT 1"
    for song in songs:
        samples = cursor.execute(request, (song[0],)).fetchall()
        for sample in samples:
            res.append(Sample(sample[0], song[0], srz.unformat_artists(song[1]), song[2], sample[1]))

    return res
