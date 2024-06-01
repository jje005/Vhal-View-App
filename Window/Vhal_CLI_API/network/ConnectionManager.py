import logging
import subprocess
import typer

import local_connection_model
import remote_connection_model

app = typer.Typer()


class ConnectionManager:
    _instance = None
    process = subprocess.Popen(['adb', 'connect'], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               text=True)

    def __init__(self):
        self.local_connection_model = None
        self.remote_connection_model = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConnectionManager, cls).__new__(cls)
            cls._instance.initialize()
        return cls._instance

    def initialize(self):
        self.process = subprocess.Popen(["/bin/bash"], stdin=subprocess.PIPE, text=True)

    @app.command()
    def set_connection(self, connection_type: str, address: str, port: int):
        if connection_type == "l" or connection_type == "local":
            self.set_local_connection()
        elif connection_type == "r" or connection_type == "remote":
            self.set_remote_connection(address, port)
        else:
            logging.error("Error: Please enter a valid command")

    @app.command()
    def connection(self, connection_type: str):
        if connection_type == "l" or connection_type == "local":
            if self.local_connection_model.get_port() is None or self.local_connection_model.get_address() is None:
                typer.echo("Error : Local connection information is Not True")
                return
            command = self.local_connection_model.get_address() + " : " + self.local_connection_model.get_port()
            self.run_command(command)
        elif connection_type == "r" or connection_type == "remote":
            if self.remote_connection_model.get_port() is None or self.remote_connection_model.get_address() is None:
                typer.echo("Error : Remote connection information is Not True")
                return
            command = self.remote_connection_model.get_address() + " : " + self.remote_connection_model.get_port()
            self.run_command(command)

    def set_local_connection(self):
        self.local_connection_model.set_address("10.10.10.10")
        self.local_connection_model.set_port(8888)

    def set_remote_connection(self, ip: str, port: int):
        self.remote_connection_model.set_address(ip)
        self.remote_connection_model.set_port(port)

    def run_command(self, command: str):
        try:
            self.process.stdin.write(command)
            self.process.stout()
            self.process.stdin.flush()
        except ConnectionError:
            typer.echo("Error : Can't Connect ")


if __name__ == "__main__":
    app()
