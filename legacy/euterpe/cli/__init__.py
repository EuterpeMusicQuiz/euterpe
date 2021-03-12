# -*- coding: utf-8 -*-

from euterpe.misc.colors import *
from euterpe.cli import songs
from euterpe.cli.utils import get_mode_prompt

from cmd import Cmd

class MainPrompt(Cmd):
    intro = "TODO: Intro"
    
    prompt = get_mode_prompt("euterpe")
    ruler = '-'
    completekey = 'tab'

    def help_songs(self, args) -> None:
        print("Add, delete, and view songs in Euterpe")
    
    def do_songs(self, args) -> None:
        songs.prompt()

    def help_quit(self, args) -> None:
        print("Leave Euterpe's management console")
    
    def do_quit(self, args) -> None:
        exit(0)
    

def prompt() -> None:
    MainPrompt().cmdloop()
