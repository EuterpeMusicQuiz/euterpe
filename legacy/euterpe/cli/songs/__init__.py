# -*- coding: utf-8 -*-

from euterpe.cli.songs import *
from euterpe.cli.songs import query_delete
from euterpe.cli.utils import get_mode_prompt
from cmd import Cmd

class SongsPrompt(Cmd):
    intro = "TODO: Intro"
    
    prompt = get_mode_prompt("songs")
    ruler = '-'
    completekey = 'tab'

    def help_exit(self):
        print("Exit songs's management section")
    
    def do_exit(self, args):
        return True

    def help_undo(self):
        pass

    def do_undo(self, args):
        pass

    def help_status(self):
        pass

    def do_status(self, args):
        pass

    def help_commit(self):
        pass

    def do_commit(self, args):
        pass
    
    def help_query(self):
        pass

    def complete_query(self, text, line, begidx, endidx):
        return query_delete.complete_query(self, text, line, begidx, endidx)
    
    def do_query(self, args):
        return query_delete.do_query(self, args)

    def help_add(self):
        pass

    def do_add(self, args):
        pass

    def help_delete(self):
        print("Delete songs and samples")
    
    def do_delete(self, args):
        pass
    
def prompt() -> None:
    SongsPrompt().cmdloop()
