class remote_connection_model:
    def __init__(self):
        self.__private_address = None
        self.__private_port = None

    def set_address(self, address: str):
        self.__private_address = address

    def get_address(self):
        return self.__private_address

    def set_port(self, port: str):
        self.__private_port = port

    def get_port(self):
        return self.__private_port
