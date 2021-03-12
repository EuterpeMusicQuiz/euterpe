# -*- coding: utf-8 -*-

from os.path import exists
from os import makedirs
from random import choice
import string

from euterpe.misc.colors import dim, bright

## String manipulation ##

def get_extension(song_name):
    '''Returns the extension of a file'''
    index = song_name.rfind('.')
    return song_name[index + 1:]

def get_last_name(path):
    '''Returns the file name designed by <path>'''
    index = path.rfind('/')
    return path[index + 1:]

## Directory and file generation ##

CHRS = ''.join([string.digits, string.ascii_letters])
SIZE = 7

def rstr_generator(size=SIZE, chars=CHRS):
    '''Generates a random string of size <size> containing chars from <chars>'''
    return ''.join(choice(chars) for _ in range(size))

def rdir_generator(parent_dir):
    '''Generates a random directory into <parent_dir>'''
    if not exists(parent_dir):
        makedirs(parent_dir)
    d = parent_dir + '/' + rstr_generator()
    while exists(d):
        d = parent_dir + '/' + rstr_generator()
    makedirs(d)
    return d

def rfile_generator(parent_dir, file_extension):
    '''Generates a random file of format <file_extension> into <parent_dir>'''
    if not exists(parent_dir):
        makedirs(parent_dir)
    d = parent_dir + '/' + rstr_generator() + '.' + file_extension
    while exists(d):
        d = parent_dir + '/' + rstr_generator() + '.' + file_extension
    open(d, 'x')
    return d

## Dictionary display ##

def smooth_dict(data):
    '''
    Takes a dictionary <data>
    Returns a stylized printable string containing <data> attributes
    '''
    max_len = 0
    for field in data:
        if len(str(field)) > max_len:
            max_len = len(str(field))
    dict_str = bright("{\n")
    for field in data:
        dict_str += "  " + bright(str(field)) + (max_len - len(field)) * " " + " : " + dim(str(data[field])) + "\n"
    dict_str += bright("}")
    return dict_str
    
def sober_dict(data):
    '''
    Takes a dictionary <data>
    Returns a printable string containing <data> attributes
    '''
    max_len = 0
    for field in data:
        if len(str(field)) > max_len:
            max_len = len(str(field))
    dict_str = "{\n"
    for field in data:
        dict_str += "  " + str(field) + (max_len - len(field)) * " " + " : " + str(data[field]) + "\n"
    dict_str += "}"
    return dict_str
