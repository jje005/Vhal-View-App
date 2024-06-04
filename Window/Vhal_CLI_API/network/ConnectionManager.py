import configparser
import subprocess
from typing import Optional
from enum import Enum
import typer


class ConnectionType(Enum):
    LOCAL = "local"
    REMOTE = "remote"


class ConnectionManager:
    _instance = None
    process = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConnectionManager, cls).__new__(cls)
            cls._instance.initialize()
        return cls._instance

    def initialize(self):
        self.process = subprocess.Popen(['adb', 'connect'], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        text=True)

    def change(self):
        self.disconnection()
        connection_type = self.get_connection_type()
        if connection_type == "local":
            self.connection_remote()
        elif connection_type == "remote":
            self.connection_local()
        else:
            typer.echo("ADB와 애뮬레이터 연결이 안되어있어 전환을 할 수 없습니다.")

    def disconnection(self):
        connection_type = self.get_connection_type()
        command = "adb disconnect"
        ip, port = self.get_connection(connection_type)
        command += f"{ip}:{port}"
        typer.echo(f"{connection_type}와 ADB 연결을 종료하겠습니다.")
        subprocess.run(command, capture_output=True, shell=True)



    def connection_remote(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        ip = config['remote']['ip']
        port = config['remote']['port']
        command = ip + " : " + port
        config['config'] = {'connection_type': 'remote'}

        self.run_command(command)

    def connection_local(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        ip = config['local']['ip']
        port = config['local']['port']

        if ip is None or port is None:
            typer.echo("Error : Local connection information is Not True")
            return
        command = ip + " : " + port

        config['config'] = {'connection_type': 'local'}

        self.run_command(command)

    def connection(self, connection_type: str):
        if connection_type == "l" or connection_type == "local":
            self.connection_local()
        elif connection_type == "r" or connection_type == "remote":
            self.connection_remote()

    def run_command(self, command: str):
        try:
            self.process.stdin.write(command)
            self.process.stdin.flush()
        except ConnectionError:
            typer.echo("Error : Can't Connect ")
        finally:
            typer.echo("Success")

    def set_connection(self, connection_type: str, address, port):
        config = configparser.ConfigParser()
        config.read('config.ini')

        if connection_type == 'remote':
            config['remote'] = {'ip': address, 'port': port}
            config['connection_type'] = {'type': "remote"}
        elif connection_type == 'local':
            config['local'] = {'ip': address, 'port': port}
            config['connection_type'] = {'type': "local"}
        else:
            raise ValueError("Invalid connection type. Use 'remote' or 'local'.")

        with open('config.ini', 'w') as configfile:
            config.write(configfile)

    def get_connection(self, connection_type: str) -> tuple:
        config = configparser.ConfigParser()
        config.read('config.ini')

        if connection_type in config:
            ip = config[connection_type]['ip']
            port = int(config[connection_type]['port'])
            return ip, port
        else:
            raise ValueError("Invalid connection type. Use 'remote' or 'local'.")

    def get_connection_type(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        connection_type = config['connection_type']['type']
        return connection_type


connection_instance = ConnectionManager()
