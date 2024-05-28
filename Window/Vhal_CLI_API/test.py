import argparse
from core.command_dispatcher import CommandDispatcher


def main():
    dispatcher = CommandDispatcher()
    dispatcher.parse_and_execute()


if __name__ == "__main__":
    main()