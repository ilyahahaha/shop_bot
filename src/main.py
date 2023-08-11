import logging
from sys import argv, stdout

from src.utils.cli import command_line


def main() -> None:
    command_line(argv[1:])


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=stdout)
    main()
