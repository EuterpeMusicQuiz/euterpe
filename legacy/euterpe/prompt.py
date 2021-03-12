from euterpe.extraction.extract import create_dir_metadata
from euterpe.extraction.modify import replace_metadata
from euterpe.extraction.config import SONG_DIR_PATH, METADATA, AUDIO_EXTENSIONS
from euterpe.misc.utils import smooth_dict, sober_dict, get_extension
from euterpe.misc.colors import *
from euterpe.extraction.tag import tag_dir
from euterpe.config import get_value

from cmd import Cmd
from os import walk
from os.path import exists, isdir
from subprocess import call
from colorama import Fore
from time import time

def parse(string):
    string = string.split(":")
    indexes = []
    i = 0
    for s in string:
        if s == '':
            indexes.append(i)
        elif not s.isdigit():
            return False, string
        else:
            string[string.index(s)] = int(s)
        i += 1
    indexes = [indexes[i] - i for i in range(len(indexes))]
    for index in indexes:
        del string[index]
    string = list(set(string))
    string.sort()
    string = list(filter(lambda x: x != 0, string))
    return True, string

class Prompt(Cmd):
    intro = "Type " + bright("help") + " to get started"

    prompt = "$ "
    ruler = '-'
    completekey = 'tab'

    doc_header = "Documented commands (type " + bright("help <cmd>") + ")"
    undoc_header = "Undocumented commands"
    misc_header = "Not commands"

    subfolders = []
    metadata = []
    recursively = True

    ## MISCELLANEOUS ##
    
    def __init__(self):
        Cmd.__init__(self)
        self.sample_dir_path = get_value('storage', 'samples_dir')
        
    ## BASIC COMMANDS ##

    def emptyline(self):
        pass

    def default(self, line):
        print("Unknown command")

    def preloop(self):
        print("Command-line tool for exporting songs as samples and filling the database with their metadata")

    def postloop(self):
        print("End of the session")

    ## ADDED COMMANDS ##

    def do_quit(self, args):
        exit()

    def help_quit(self):
        print("Leaves the command-line tool")

    def do_exit(self, args):
        return True

    def help_exit(self):
        print("Leaves the current session")

    def do_path(self, args):
        global SONG_DIR_PATH

        if args.startswith('display'):
            if (len(args) == 7): # 7 == len('display')
                print("Song directory path : " + blue_fg(SONG_DIR_PATH))
                print("Sample directory path : " + blue_fg(self.sample_dir_path))
                print("Subfolder management is recursive : ", end='')
                print(green_fg("Yes") if Prompt.recursively else red_fg("No"))
            else:
                print("Usage : 'path display'")
        elif args.startswith('modify'):
            if args.endswith('song'):
                print("Write the path for the " + blue_fg(args[7:]) + " folder, otherwise type " + bright('exit')) # 7 == len('modify ')
                res = input("[$] ")
                if (res == 'exit'):
                    print(magenta_fg(bright('Modification canceled')))
                    return
                while not exists(res) or not isdir(res):
                    print(red_fg("Path doesn't exist or isn't a folder"))
                    print("Please write it again, or type " + bright('exit') + " to cancel")
                    res = input("[$] ")
                    if (res == 'exit'):
                        print(magenta_fg(bright('Modification canceled')))
                        return
                if (res[-1] == '/'):
                    res = res[:-1]
                if (args[7:] == 'song'): # 7 == len('modify ')
                    SONG_DIR_PATH = res
                print(green_fg('Done'))
            else:
                print("Usage : 'path modify song'")
        else:
            print("Usage :")
            print("'path display'")
            print("'path modify song'")

    def help_path(self):
        print("Type " + bright("path display") + " to get the current directories for song picking and sample exporting")
        print("Type " + bright("path modify song") + " to modify default directory for songs")

    def complete_path(self, text, line, begidx, endidx):
        if len(line) == 5:
            return ['display', 'modify']
        lines = list(filter(None, line.split(" ")))
        lth = len(lines)
        final = lines[lth - 1]
        if lth == 2:
            if final != 'modify':
                if final.startswith('d') and line[-1] != ' ':
                    return ['display']
                elif final.startswith('m'):
                    return ['modify']
            elif final == 'modify' and endidx < 12:
                return ['modify']
            else:
                return ['song']
        elif lth == 3 and lines[lth - 2] == 'modify':
            if final.startswith('s') and line[-1] != ' ':
                return ['song']
            elif line[-1] != ' ':
                return ['song']

    def do_add(self, args):
        global SONG_DIR_PATH

        if args.startswith('subfolder'):
            if (len(args) == 9): # 9 == len('subfolder')
                rank = 1
                roots = [item[0] for item in walk(SONG_DIR_PATH)]
                for root in roots:
                    print(bright(str(rank)), cyan_fg(root))
                    rank += 1
                print("Type the numbers corresponding to the subfolders you wish to add, and separate them using " + dim('":"'))
                print("For instance, " + bright('3:12:1:5'))
                print("If your intention is to add all of them, simply write " + bright("all") + ", otherwise type " + bright('exit'))
                res = input("[$] ")
                if (res == 'exit'):
                    print(magenta_fg(bright('Operation canceled')))
                    return
                elif (res == 'all'):
                    res = [str(i) + ":" for i in range(1, len(roots) + 1)]
                    res = ''.join(res)
                while not parse(res)[0]:
                    print(red_fg("Unvalid format, please respect " + bright('2:4:15:6')) + red_fg(" standard"))
                    print("Please write it again, or type " + bright('exit') + " to cancel, or type " + bright('all') + " to add all subfolders")
                    res = input("[$] ")
                    if (res == 'exit'):
                        print(magenta_fg(bright('Operation canceled')))
                        return
                    elif (res == 'all'):
                        res = [str(i) + ":" for i in range(1, len(roots) + 1)]
                        res = ''.join(res)
                ranks = parse(res)[1]
                indexes = [ranks[i] - 1 for i in range(len(ranks))]
                for i in indexes:
                    if  i < len(roots) and roots[i] not in Prompt.subfolders:
                        Prompt.subfolders.append(roots[i])
                        Prompt.metadata.append({tag: None for tag in METADATA})
                # Adding other subfolders according to hierarchy
                if Prompt.recursively:
                    for item in Prompt.subfolders:
                        for subitem in roots:
                            if item in subitem and item != subitem and subitem not in Prompt.subfolders:
                                Prompt.subfolders.append(subitem)
                                Prompt.metadata.append({tag: None for tag in METADATA})
                print(green_fg('Done'))
            else:
                print("Usage : 'add subfolder'")
        elif args.startswith('metadata'):
            if (len(args) == 8): # 8 == len('metadata')
                rank = 1
                for sub in Prompt.subfolders:
                    print(bright(blue_fg(str(rank))), blue_fg(sub))
                    print(smooth_dict(Prompt.metadata[rank - 1]))
                    rank += 1
                print("Type the numbers corresponding to the subfolders whose metadata you wish to modify, and separate them using " + dim('":"'))
                print("For instance, " + bright('6:2:16:1'))
                print("If your intention is to modify all of them, simply write " + bright("all") + ", otherwise type " + bright('exit'))
                res = input("[$] ")
                if (res == 'exit'):
                    print(magenta_fg(bright('Operation canceled')))
                    return
                elif (res == 'all'):
                    res = ['0:'] + [str(i) + ":" for i in range(1, len(Prompt.subfolders) + 1)]
                    res = ''.join(res)
                while not parse(res)[0]:
                    print(red_fg("Unvalid format, please respect " + bright('3:1:9:18')) + red_fg(" standard"))
                    print("Please write it again, or type " + bright('exit') + " to cancel, or type " + bright('all') + " to modify all")
                    res = input("[$] ")
                    if (res == 'exit'):
                        print(magenta_fg(bright('Operation canceled')))
                        return
                    elif (res == 'all'):
                        res = [str(i) + ":" for i in range(1, len(Prompt.subfolders) + 1)]
                        res = ''.join(res)
                ranks = parse(res)[1]
                for r in ranks:
                    if r - 1 < len(Prompt.subfolders):
                        print(blue_fg(Prompt.subfolders[r - 1]))
                        print(smooth_dict(Prompt.metadata[r - 1]))
                        for field in Prompt.metadata[r - 1]:
                            print(bright(magenta_fg('<' + field + '>')), Fore.MAGENTA)
                            res = input("[$] ")
                            if (res == '' or (not res.isdigit() and field == 'DATE')):
                                Prompt.metadata[r - 1][field] = None
                            else:
                                Prompt.metadata[r - 1][field] = res
                        print(Fore.RESET)
                print(green_fg('Done'))
            else:
                print("Usage : 'add metadata'")
        else:
            print("Usage :")
            print("'add subfolder'")
            print("'add metadata'")

    def help_add(self):
        print("Type " + bright("add subfolder") + " to add folders whose audio files will be exported")
        print("Type " + bright("add metadata") + " to modify default metadata concerning songs within chosen folders")

    def complete_add(self, text, line, begidx, endidx):
        if len(line) == 4:
            return ['subfolder', 'metadata']
        lines = list(filter(None, line.split(" ")))
        lth = len(lines)
        final = lines[lth - 1]
        if lth == 2:
            if final != 'subfolder':
                if final.startswith('m') and line[-1] != ' ':
                    return ['metadata']
                elif final.startswith('s') and line[-1] != ' ':
                    return ['subfolder']
            elif final == 'subfolder' and endidx < 14:
                return ['subfolder']
            elif final == 'metadata' and endidx < 13:
                return ['metadata']

    def do_remove(self, args):
        global SONG_DIR_PATH

        if args.startswith('subfolder'):
            if len(args) == 9: # 9 == len('subfolder')
                rank = 1
                for sub in Prompt.subfolders:
                    print(bright(str(rank)), cyan_fg(sub))
                    rank += 1
                print("Type the numbers corresponding to the subfolders you wish to remove, and separate them using " + dim('":"'))
                print("For instance, " + bright('3:2:14:6'))
                print("If your intention is to remove all of them, simply write " + bright("all") + ", otherwise type " + bright('exit'))
                res = input("[$] ")
                if res == 'exit':
                    print(magenta_fg(bright('Operation canceled')))
                    return
                elif res == 'all':
                    res = [str(i) + ":" for i in range(1, len(Prompt.subfolders) + 1)]
                    res = ''.join(res)
                while not parse(res)[0]:
                    print(red_fg("Unvalid format, please respect " + bright('3:8:1:7')) + red_fg(" standard"))
                    print("Please write it again, or type " + bright('exit') + " to cancel, or type " + bright('all') + " to remove all")
                    res = input("[$] ")
                    if res == 'exit':
                        print(magenta_fg(bright('Operation canceled')))
                        return
                    elif res == 'all':
                        res = [str(i) + ":" for i in range(1, len(Prompt.subfolders) + 1)]
                        res = ''.join(res)
                ranks = parse(res)[1]
                indexes = [ranks[i] - i - 1 for i in range(len(ranks))]
                # Hierarchical removing
                if Prompt.recursively:
                    metadata_removed, subfolders_removed = [], []
                    for r in ranks:
                        subfolders_removed.append(Prompt.subfolders[r - 1])
                        metadata_removed.append(Prompt.metadata[r - 1])
                        for subitem in Prompt.subfolders:
                            if Prompt.subfolders[r - 1] in subitem and Prompt.subfolders[r - 1] != subitem:
                                subfolders_removed.append(subitem)
                                metadata_removed.append(Prompt.metadata[Prompt.subfolders.index(subitem)])
                    Prompt.subfolders = [subfolder for subfolder in Prompt.subfolders if subfolder not in subfolders_removed]
                    Prompt.metadata = [metadata for metadata in Prompt.metadata if metadata not in metadata_removed]
                else:
                    for i in indexes:
                        if i < len(Prompt.subfolders):
                            del Prompt.subfolders[i]
                            del Prompt.metadata[i]
                print(green_fg('Done'))
            else:
                print("Usage : 'remove subfolder'")
        elif args.startswith('metadata'):
            if (len(args) == 8): # 4 == len('metadata')
                rank = 1
                for sub in Prompt.subfolders:
                    print(bright(blue_fg(str(rank))), blue_fg(sub))
                    print(smooth_dict(Prompt.metadata[rank - 1]))
                    rank += 1
                print("Type the numbers corresponding to the subfolders whose metadata you wish to reset, and separate them using " + dim('":"'))
                print("For instance, " + bright('6:2:16:1'))
                print("If your intention is to reset all of them, simply write " + bright("all") + ", otherwise type " + bright('exit'))
                res = input("[$] ")
                if (res == 'exit'):
                    print(magenta_fg(bright('Operation canceled')))
                    return
                elif (res == 'all'):
                    res = [str(i) + ":" for i in range(1, len(Prompt.subfolders) + 1)]
                    res = ''.join(res)
                while not parse(res)[0]:
                    print(red_fg("Unvalid format, please respect " + bright('3:1:9:18')) + red_fg(" standard"))
                    print("Please write it again, or type " + bright('exit') + " to cancel, or type " + bright('all') + " to reset all")
                    res = input("[$] ")
                    if (res == 'exit'):
                        print(magenta_fg(bright('Operation canceled')))
                        return
                    elif (res == 'all'):
                        res = [str(i) + ":" for i in range(1, len(Prompt.subfolders) + 1)]
                        res = ''.join(res)
                ranks = parse(res)[1]
                for r in ranks:
                    if r - 1 < len(Prompt.metadata):
                        for field in Prompt.metadata[r - 1]:
                            Prompt.metadata[r - 1][field] = None
                print(green_fg('Done'))
            else:
                print("Usage : 'remove metadata'")
        else:
            print("Usage :")
            print("'remove subfolder'")
            print("'remove metadata'")

    def help_remove(self):
        print("Type " + bright("remove subfolder") + " to remove folders whose audio files will be exported")
        print("Type " + bright("remove metadata") + " to reset default metadata concerning songs from chosen folders")

    def complete_remove(self, text, line, begidx, endidx):
        if len(line) == 7:
            return ['subfolder', 'metadata']
        lines = list(filter(None, line.split(" ")))
        lth = len(lines)
        final = lines[lth - 1]
        if lth == 2:
            if final != 'subfolder':
                if final.startswith('m') and line[-1] != ' ':
                    return ['metadata']
                elif final.startswith('s') and line[-1] != ' ':
                    return ['subfolder']
            elif final == 'subfolder' and endidx < 17:
                return ['subfolder']
            elif final == 'metadata' and endidx < 16:
                return ['metadata']

    def do_export(self, args):
        print("Processing...")
        # Organising files via a tree depth roaming (parcours en profondeur)
        permutation = []
        copy = Prompt.subfolders.copy()
        Prompt.subfolders.sort()
        for element in copy:
            permutation.append(Prompt.subfolders.index(element))
        Prompt.metadata = [Prompt.metadata[permutation.index(i)] for i in range(len(permutation))]

        # Pre-metadata replacement for folders
        for item in Prompt.subfolders:
            for subitem in Prompt.subfolders[Prompt.subfolders.index(item) + 1:]:
                if item in subitem:
                    replace_metadata(Prompt.metadata[Prompt.subfolders.index(subitem)], Prompt.metadata[Prompt.subfolders.index(item)])

        # Samples creation
        metadata = []
        for sub in Prompt.subfolders:
            print(yellow_fg(sub))
            start_time = time()
            metadata.append(create_dir_metadata(sub, self.sample_dir_path))
            end_time = time()
            if [item for item in [item[2] for item in walk(sub)][0] if get_extension(item) in AUDIO_EXTENSIONS]: # Checks if directory contains at least one audio file
                elapsed_time = end_time - start_time
                print("\nFolder exportation time : " + blue_fg('{:02d}h:{:02d}m:{:02d}s'.format(int(elapsed_time//3600), int((elapsed_time%3600)//60), int(elapsed_time%60))) + "\n")
        for i in range(len(Prompt.metadata)):
            for j in range(len(metadata[i])):
                replace_metadata(metadata[i][j], Prompt.metadata[i])
        metadata = [item for arr in metadata for item in arr] # final item which contains all metadata
        file = open(self.sample_dir_path + '/metadata.txt', 'a')
        for d in metadata:
            file.write(sober_dict(d) + '\n')
            print(smooth_dict(d))
        file.close()
        # TODO : Truly export these metadata in the database
        print(green_fg('Done'))

    def help_export(self):
        print("Exports the subfolders' content, then overriding metadata for folders whose metadata have been set")

    def do_tag(self, args):
        print("This operation is " + red_fg("irreversible") + ", take it into account before doing it")
        #TODO : function that automatically adds metadata to files in selected folders
        rank = 1
        roots = [item[0] for item in walk(SONG_DIR_PATH)]
        for root in roots:
            print(bright(str(rank)), cyan_fg(root))
            rank += 1
        print("Type the numbers corresponding to the subfolders whose content you wish to automatically tag, and separate them using " + dim('":"'))
        print("For instance, " + bright('3:12:1:5'))
        print("Note that tagging ", end='')
        print(green_fg("will"), end='') if Prompt.recursively else print(red_fg("won't"), end='')
        print(" be recursive")
        print("If your intention is to add all of them, simply write " + bright("all") + ", otherwise type " + bright('exit'))
        res = input("[$] ")
        if (res == 'exit'):
            print(magenta_fg(bright('Operation canceled')))
            return
        elif (res == 'all'):
            res = [str(i) + ":" for i in range(1, len(roots) + 1)]
            res = ''.join(res)
        while not parse(res)[0]:
            print(red_fg("Unvalid format, please respect " + bright('2:4:15:6')) + red_fg(" standard"))
            print("Please write it again, or type " + bright('exit') + " to cancel, or type " + bright('all') + " to add all subfolders")
            res = input("[$] ")
            if (res == 'exit'):
                print(magenta_fg(bright('Operation canceled')))
                return
            elif (res == 'all'):
                res = [str(i) + ":" for i in range(1, len(roots) + 1)]
                res = ''.join(res)
        print("Processing...")
        ranks = parse(res)[1]
        indexes = [ranks[i] - 1 for i in range(len(ranks)) if ranks[i] - 1 < len(roots)]
        for i in indexes:
            print(yellow_fg(roots[i]))
            start_time = time()
            tag_dir(roots[i])
            end_time = time()
            if [item for item in [item[2] for item in walk(roots[i])][0] if get_extension(item) in AUDIO_EXTENSIONS]: # Checks if directory contains at least one audio file
                elapsed_time = end_time - start_time
                print("\nFolder exportation time : " + blue_fg('{:02d}h:{:02d}m:{:02d}s'.format(int(elapsed_time//3600), int((elapsed_time%3600)//60), int(elapsed_time%60))))
        # Adding other subfolders according to hierarchy
        if Prompt.recursively:
            for i in indexes:
                for subitem in roots:
                    if roots[i] in subitem and roots[i] != subitem:
                        print(yellow_fg(subitem))
                        start_time = time()
                        tag_dir(subitem)
                        end_time = time()
                        if [item for item in [item[2] for item in walk(subitem)][0] if get_extension(item) in AUDIO_EXTENSIONS]: # Checks if directory contains at least one audio file
                            elapsed_time = end_time - start_time
                            print("\nFolder exportation time : " + blue_fg('{:02d}h:{:02d}m:{:02d}s'.format(int(elapsed_time//3600), int((elapsed_time%3600)//60), int(elapsed_time%60))))
        print(green_fg('Done'))
        pass

    def help_tag(self):
        print("Automatically tags the sound files contained in the selected directory, these changes are irreversible so be cautious")
        pass

    def do_status(self, args):
        lth = min(len(Prompt.subfolders), len(Prompt.metadata))
        if lth == 0:
            print(yellow_fg("No subfolders have been added"))
        else:
            for i in range(lth):
                print(yellow_fg(Prompt.subfolders[i]))
                print(smooth_dict(Prompt.metadata[i]))

    def help_status(self):
        print("Lists subfolders whose content will be sampled, and default metadata for songs inside them")

    def do_list(self, args):
        if args == '':
            call('ls')
        else:
            call(['ls', args])

    def help_list(self):
        print("Lists the content of the directory passed in argument")

    def do_tree(self, args):
        if args == '':
            call('tree')
        else:
            call(['tree', args])

    def help_tree(self):
        print("Lists the content of the directory passed in argument as a tree")

    def help_help(self):
        print("Lists available commands with 'help' or detailed help with 'help <cmd>'")
