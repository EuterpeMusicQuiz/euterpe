# -*- coding: utf-8 -*-

from euterpe.misc.utils import get_last_name
from euterpe.cli.utils import get_mode_prompt
from euterpe.cli.file_browser import FileBrowser
from euterpe.cli.audio_file_manager import AudioFileManager

from cmd import Cmd

class AddSongPrompt(Cmd):
    intro = "Prompt for song addition to the database"
    
    prompt = get_mode_prompt("add_song")
    ruler = '-'
    completekey = 'tab'

    def __init__(self, _dir = None):
        Cmd.__init__(self)
        self.fb = FileBrowser(_dir)
        self.afm = AudioFileManager()
        self.history = [(self.fb.directory, self.afm.audio_files)] # array of tuples (directory, audio_files)

    ## STANDARD COMMANDS ##

    def emptyline(self):
        pass

    def default(self, line):
        print("Unknown command")

    def preloop(self):
        print("Command-line tool for song addition")

    def postloop(self):
        print("End of the session")

    ## CUSTOM COMMANDS ##

    def help_exit(self):
        print("Exit song addition section")
    
    def do_exit(self, args):
        return True

    def help_undo(self):
        print("Cancel the last action")

    def do_undo(self, args):
        if len(self.history) > 1:
            self.fb.directory, self.afm.audio_files = self.history[-2]
            del self.history[-1]
            
    def help_list(self):
        print("List files and subdirectories")
    
    def do_list(self, args):
        self.fb.list_content(True)

    def help_move(self):
        print("Browse through the file system")

    def do_move(self, args):
        if args.startswith('up'):
            if len(args) == 2:
                self.fb.move_up()
            elif len(args.split(" ")) == 2 and args.split(" ")[1].isdigit():
                self.fb.move_up(int(args.split(" ")[1]))
            else:
                print("Usage: TODO")
        elif args.startswith('in'):
            if len(args.split(" ")) == 2:
                self.fb.move_in(args.split(" ")[1])
            else:
                print("Usage: TODO")
        elif args.startswith('to'):
            if len(args.split(" ")) == 2:
                self.fb.move_to(args.split(" ")[1])
            else:
                print("Usage: TODO")
        else:
            print("Usage: TODO")
        self.history.append((self.fb.directory, self.afm.audio_files))

    def help_status(self):
        print("Display which files are currently added, along with their additional metadata")

    def do_status(self, args):
        self.afm.list_content(False)
            
    def help_add(self):
        print("Add either all audio files from current directory or selected files")

    def do_add(self, args):
        if args.startswith('all ') or args == 'all':
            self.afm.add_audio_files(self.fb.get_files(True))
        elif all(arg.isdigit() for arg in args.split(" ")): 
            self.afm.add_audio_files([self.fb.get_files(True)[int(idx)] for idx in args.split(" ")])
        elif all(isinstance(arg, str) for arg in args.split(" ")):
            self.afm.add_audio_files([self.fb.directory + '/' + arg for arg in args.split(" ") if self.fb.directory + '/' + arg in self.fb.get_files(True)])
        self.history.append((self.fb.directory, self.afm.audio_files))

    def help_delete(self):
        print("Delete elements using indexes separated by spaces")
    
    def do_delete(self, args):
        if args.startswith('all ') or args == 'all':
            self.afm.audio_files = []
        elif all(arg.isdigit() for arg in args.split(" ")): 
            self.afm.remove_audio_files([self.afm.audio_files[int(idx)][0] for idx in args.split(" ")])
        self.history.append((self.fb.directory, self.afm.audio_files))
        
def prompt(_dir = None):
    AddSongPrompt(_dir).cmdloop()


