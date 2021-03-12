# -*- coding: utf-8 -*-

from euterpe.database import song_db
from euterpe.misc.colors import *

def pretty_print_songs(songs):
    for song in songs:
        artists = ' ft '.join(song.getArtists()) 
        print("SONG #{0}: {1} from {2}".format(magenta_fg(song.getId()),
                                               yellow_fg(song.getTitle()),
                                               cyan_fg(artists)))

def pretty_print_samples(samples):
    sid = -1
    i = 0
    flag = False
    while i<len(samples):
        sample = samples[i]
        if sample.getSongId() == sid:
            pass
        else:
            if sid != -1:
                print(" ")
            sid = sample.getSongId()
            artists = ' ft '.join(sample.getArtists())
            print("SONG #{0}: {1} from {2}".format(magenta_fg(sample.getSongId()),
                                                   yellow_fg(sample.getTitle()),
                                                   cyan_fg(artists)))
        print("\tEXTRACT #{0}: {1}".format(magenta_fg(sample.getId()),
                                           green_fg(sample.getFile())))
        i += 1

def complete_filter(arg):
    res = []
    for i in ["artist=", "artist~", "title=", "title~", "genre=", "genre~", "year=", "year>", "year<"]:
            if i.startswith(arg) and not arg.startswith(i):
                res.append(i)
    return res

def query_split_line(line):
    buf = line.split('"')
    argv = []
    for i in range(0, len(buf)):
        if i%2 == 0:
            argv += buf[i].split(' ')
        else:
            argv[-1] += buf[i]
    flag = argv[-1]==''
    argv = [arg for arg in argv if arg != '']
    if flag:
        argv.append('')
    return argv

def complete_query(cmd, text, line, begidx, endidx):
    argv = query_split_line(line)
    argc = len(argv)

    res = []
    if argc == 2:
        for i in ['samples', 'songs']:
            if i.startswith(argv[-1]):
                res.append(i)
        return res

    if argc == 3:
        if argv[-1].startswith('order_'):
            for i in ['order_none', 'order_song_id', 'order_artist', 'order_title']:
                if i.startswith(argv[-1]):
                    res.append(i)
            return res
        return ['order_']

    if argc > 3:
        for i in ['artist', 'title', 'year', 'genre']:
            if argv[-1].startswith(i):
                return complete_filter(argv[-1])
            elif i.startswith(argv[-1]):
                res.append(i)
        return res

    return res

def do_query(cmd, args_line):
    db = song_db.get()
    args = [ arg for arg in query_split_line(args_line) if arg != '']
    n_args = len(args)

    if n_args < 2:
        print("Not enough arguments")
        return

    if not args[0] in ['songs', 'samples']:
        print("Please query for songs or samples, not {}".format(red_fg(args[0])))
        return
    
    order_by = None
    if args[1] == 'order_none':
        order_by = None
    elif args[1] == 'order_artist':
        order_by = 'artist'
    elif args[1] == 'order_title':
        order_by = 'title'
    elif args[1] == 'order_song_id':
        order_by = 'song_id'
    else:
        print("Unknown ordering: {}".format(red_fg(args[1])))
        return

    filters = []
    flag = False
    wrong_filters = []
    for i in range(2, n_args):
        if flag == True:
            filters.append('AND')
        else:
            flag = True
        f = args[i]
        if f.startswith('artist'):
            if f[6] == '=':
                filters += [('artist', 'eq', f[7:])]
            elif f[6] == '~':
                filters += [('artist', 'ct', f[7:])]
            else:
                wrong_filters.append(f)
        elif f.startswith('title'):
            if f[5] == '=':
                filters += [('title', 'eq', f[6:])]
            elif f[5] == '~':
                filters += [('title', 'ct', f[6:])]
            else:
                wrong_filters.append(f)
        elif f.startswith('genre'):
            if f[5] == '=':
                filters += [('genre', 'eq', f[6:])]
            elif f[5] == '~':
                filters += [('genre', 'ct', f[6:])]
            else:
                wrong_filters.append(f)
        elif f.startswith('year'):
            if f[4] == '=':
                filters += [('year', 'eq', f[5:])]
            elif f[4] == '<':
                filters += [('year', 'lt', f[5:])]
            elif f[4] == '>':
                filters += [('year', 'gt', f[5:])]
            else:
                wrong_filters.append(f)
        else:
            wrong_filters.append(f)

    if len(wrong_filters) != 0:
        if len(wrong_filters) == 1:
            print("The filter {} is not valid".format(red_fg(wrong_filters[0])))
        else:
            ff = ', '.join([red_fg(f) for f in wrong_filters])
            print("The filters {} are not valid".format(ff))
        return

    if args[0] == 'songs':
        pretty_print_songs(db.getAllSongs(filters, order_by))
    else:
        pretty_print_samples(db.getAllSamples(filters, order_by))
        
if __name__ == "__main__":
    print(complete_query(None, "m", "query songs order_title artist", None, None))
