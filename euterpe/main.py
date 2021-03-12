import pathlib
import logging
import argparse

from euterpe._version import VERSION
from euterpe.config import get_config


def parse_args() -> argparse.Namespace:
    argparser: argparse.ArgumentParser = argparse.ArgumentParser()

    argparser.add_argument(
        "--version",
        action="store_true",
        dest="show_version",
        help="show version and exit"
    )
    argparser.add_argument(
        "-c", "--config",
        type=pathlib.Path,
        dest="config_path",
        help="config file",
    )
    argparser.add_argument(
        "-s", "--samples",
        type=pathlib.Path,
        dest="samples_dir",
        help="samples directory (where samples are stored)"
    )
    argparser.add_argument(
        "-i", "--index",
        type=pathlib.Path,
        dest="index_file",
        help="index file (database for indexing samples directory)"
    )
    log_verb = argparser.add_mutually_exclusive_group()
    log_verb.add_argument(
        "-v", "--verbose",
        action="count",
        default=0,
        dest="verbose",
        help="increase log verbosity (up to 3 times)"
    )
    log_verb.add_argument(
        "-q", "--quiet",
        action="count",
        default=0,
        dest="quiet",
        help="decrease log verbosity (up to 3 times)"
    )

    return argparser.parse_args()


def set_logging_level(args: argparse.Namespace) -> None:
    log_level = 30  # WARNING
    for i in range(args.verbose):
        log_level -= 10
    for i in range(args.quiet):
        log_level += 10
    logging.root.level = log_level


def main() -> None:
    args = parse_args()

    if args.show_version:
        print(VERSION)
        exit(0)

    set_logging_level(args)

    config = get_config(args.config_path)
    if args.samples_dir is not None:
        config.storage.samples_dir = args.samples_dir
    if args.index_file is not None:
        config.storage.index_file = args.index_file


if __name__ == "__main__":
    main()
