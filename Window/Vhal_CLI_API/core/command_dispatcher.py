import argparse
import subprocess
import sys, os

from commands.Vhal_api import set_vhal, get_vhal, get_vhal_list


def handle_vhal_set(args):
    command = set_vhal(args.property_id, args.value, args.area_id)
    print(command)


def handle_vhal_get(args):
    command = get_vhal(args.property_id)
    print(command)
    result = subprocess.run(command, capture_output=True, text=True)
    return result.stdout


def handle_vhal_list():
    command = get_vhal_list()
    print(command)


class CommandDispatcher:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="Sure SDV CLI API")
        self.subparsers = self.parser.add_subparsers(help="commands")

        self.add_vhal_set_command()
        self.add_vhal_get_command()
        self.add_vhal_list_command()

    def add_vhal_set_command(self):
        parser_vhal_set = self.subparsers.add_parser('vhal-set', help="Set VHAL property")
        parser_vhal_set.add_argument('property_id', type=str, help="Property ID for VHAL")
        parser_vhal_set.add_argument('value', type=str, help="Value to set for the property")
        parser_vhal_set.add_argument('area_id', type=str, help="Area ID for the property")
        parser_vhal_set.set_defaults(func=handle_vhal_set)

    def add_vhal_get_command(self):
        parser_vhal_get = self.subparsers.add_parser('vhal-get', help="Get VHAL property")
        parser_vhal_get.add_argument('property_id', type=str, help="Property ID for VHAL")
        parser_vhal_get.set_defaults(func=handle_vhal_get)

    def add_vhal_list_command(self):
        parser_vhal_list = self.subparsers.add_parser('vhal-list', help="Get VHAL property list")
        parser_vhal_list.set_defaults(func=handle_vhal_list)

    def parse_and_execute(self):
        args = self.parser.parse_args()
        if hasattr(args, 'func'):
            if args is None:
                args.func()
            else:
                args.func(args)
        else:
            self.parser.print_help()


if __name__ == "__main__":
    dispatcher = CommandDispatcher()
    dispatcher.parse_and_execute()
