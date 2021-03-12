#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from euterpe import config
from euterpe import cli
from euterpe.database import song_db
from euterpe.misc import colors

import argparse
import sys

def scan_params():
    parser = argparse.ArgumentParser(description='Euterpe\'s command line interface', add_help=True, allow_abbrev=True)

    parser.add_argument('--run', '-r', action='store_true', required=False,
                       help="Run the web server instead of the management console")
    parser.add_argument('--config', '-c', action='store', required=False, type=str, metavar='config_path',
                        help="Manually set the path of the config file")
    
    
    return parser.parse_args(sys.argv[1:])

def main_run() -> None:
    pass

def main_manage() -> None:
    cli.prompt()

def main() -> None:
    args = scan_params()
    config.init(args.config)
    conf = config.get_value('storage', 'database_file')
    print("Opening database at '{}'".format(colors.yellow_fg(conf)))
    song_db.init(conf)

    if args.run:
        main_run()
    else:
        main_manage()
        
if __name__ == '__main__':
    main()
