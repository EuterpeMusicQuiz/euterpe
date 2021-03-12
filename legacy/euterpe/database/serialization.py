# -*- coding: utf-8 -*-

def sanitize(func) :
    return lambda *args, **kwargs : func(*args, **kwargs).replace('"', '""')#.replace("'", "''").replace('\\', '\\\\')

@sanitize
def stz(s):
    return s

@sanitize
def format_genre(genre_name) :
    return genre_name.upper().replace(' ', '').replace('_', '').replace('-', '')



@sanitize
def format_artists(artists) :
    if type(artists) == type("a") :
        return artists
    return "#%FEAT%#".join(artists)


def unformat_artists(artists) :
    return artists.split("#%FEAT%#")

@sanitize
def format_title(title) :
    return title



def format_year(year) :
    if year == None :
        return 0
    return year



@sanitize
def format_language(language) :
    if language == None :
        return "##"
    return language



def format_difficulty(difficulty) :
    if difficulty == None :
        return -1
    return difficulty



def format_samples(samples) :
    return [stz(sample) for sample in samples] 
