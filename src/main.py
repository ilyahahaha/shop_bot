from asyncio import run
from sys import argv

from utils.cli import command_line


async def main() -> None:
    await command_line(argv[1:])


if __name__ == "__main__":
    run(main())
