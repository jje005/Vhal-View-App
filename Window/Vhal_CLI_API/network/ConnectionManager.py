import logging
import subprocess
from typing import Optional
from enum import Enum


class ConnectionType(Enum):
    LOCAL = "local"
    REMOTE = "remote"


import typer

# local_connection_model.py와 remote_connection_model.py에서 클래스 가져오기
from local_connection_model import local_connection_model
from remote_connection_model import remote_connection_model



class ConnectionManager:
    _instance = None
    process = None

    def __init__(self):
        self.ConnectionType: ConnectionType
        self.local_connection_model: local_connection_model = local_connection_model()
        self.remote_connection_model: remote_connection_model = remote_connection_model()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConnectionManager, cls).__new__(cls)
            cls._instance.initialize()
        return cls._instance

    def initialize(self):
        self.process = subprocess.Popen(['adb', 'connect'], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        text=True)

    def set_connection(self, connection_type: str, address: Optional[str], port: Optional[str]):
        if connection_type == "l" or connection_type == "local":
            self.set_local_connection(address, port)
        elif connection_type == "r" or connection_type == "remote":
            self.set_remote_connection(address, port)
        else:
            logging.error("Error: Please enter a valid command")

    def change(self):
        type = self.get_connection_type()
        if type == "local":
            self.connection_remote()
        elif type == "remote":
            self.connection_local()
        else:
            typer.echo("ADB와 애뮬레이터 연결이 안되어있어 전환을 할 수 없습니다.")

    def connection_remote(self):
        if self.remote_connection_model.get_port() is None or self.remote_connection_model.get_address() is None:
            typer.echo("Error : Remote connection information is Not True")
            return
        command = self.remote_connection_model.get_address() + " : " + self.remote_connection_model.get_port()
        self.ConnectionType = "remote"
        self.run_command(command)

    def connection_local(self):
        if self.local_connection_model.get_port() is None or self.local_connection_model.get_address() is None:
            typer.echo("Error : Local connection information is Not True")
            return
        command = self.local_connection_model.get_address() + " : " + self.local_connection_model.get_port()
        self.ConnectionType = "local"
        self.run_command(command)

    def connection(self, connection_type: str):
        if connection_type == "l" or connection_type == "local":
            self.connection_local()
        elif connection_type == "r" or connection_type == "remote":
            self.connection_remote()

    def set_local_connection(self, address: Optional[str], port: Optional[str]):
        if address is None:
            self.local_connection_model.set_address("10.10.10.10")
            typer.echo("Success : Setting local IP : 10.10.10.10")
        else:
            self.local_connection_model.set_address(address)
            typer.echo(f"Success : Setting local IP : {address}")

        if port is None:
            self.local_connection_model.set_port("8888")
            typer.echo("Success : Setting local port : 8888")
        else:
            self.local_connection_model.set_port(port)
            typer.echo(f"Success : Setting local port : {port}")

    def set_remote_connection(self, address: Optional[str], port: Optional[str]):
        self.remote_connection_model.set_address(address)
        self.remote_connection_model.set_port(port)

    def run_command(self, command: str):
        try:
            self.process.stdin.write(command)
            self.process.stout()
            self.process.stdin.flush()
        except ConnectionError:
            typer.echo("Error : Can't Connect ")

    def get_connection_type(self):
        return self.ConnectionType.value


connection_instance = ConnectionManager()
