from core.command_dispatcher import CommandDispatcher

class UserInputHandler:
    def __init__(self):
        self.dispatcher = CommandDispatcher()

    def handle_user_input(self):
        while True:
            user_input = input("Enter a command: ")
            if user_input == 'exit':
                break
            self.execute_command(user_input)

    def execute_command(self, user_input):
        # 사용자 입력을 파싱하여 명령어와 인자로 분리
        command_parts = user_input.split(' ')
        command_name = command_parts[0]
        command_args = command_parts[1:]

        if command_name == 'vhal-set':
            self.handle_vhal_set(command_args)
        elif command_name == 'vhal-get':
            self.handle_vhal_get(command_args)
        elif command_name == 'vhal-list':
            self.handle_vhal_list()

    def handle_vhal_set(self, args):
        property_id, value, area_id = args
        result = self.dispatcher.set_vhal(property_id, value, area_id)
        print(result)

    def handle_vhal_get(self, args):
        property_id = args[0]
        result = self.dispatcher.get_vhal(property_id)
        print(result)

    def handle_vhal_list(self):
        result = self.dispatcher.get_vhal_list()
        print(result)

if __name__ == "__main__":
    input_handler = UserInputHandler()
    input_handler.handle_user_input()