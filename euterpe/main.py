import pathlib
import logging
import argparse
from euterpe.config import get_config


def parse_args() -> argparse.Namespace:
    argparser: argparse.ArgumentParser = argparse.ArgumentParser()

    argparser.add_argument(
        "-c", "--config",
        type=pathlib.Path,
        dest="config_path",
        help="Config file",
    )
    argparser.add_argument(
        "-d", "--datadir",
        type=pathlib.Path,
        dest="data_dir",
        help="Data directory (where samples and indexes are stored)"
    )
    log_verb = argparser.add_mutually_exclusive_group()
    log_verb.add_argument(
        "-v", "--verbose",
        action="count",
        default=0,
        dest="verbose",
        help="Increase log verbosity (up to 3 times)"
    )
    log_verb.add_argument(
        "-q", "--quiet",
        action="count",
        default=0,
        dest="quiet",
        help="Decrease log verbosity (up to 3 times)"
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
    set_logging_level(args)
    get_config(args.config_path)


if __name__ == "__main__":
    main()
