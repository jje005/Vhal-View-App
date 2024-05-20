## CLIENT ##

import socket
from _thread import *

HOST = '10.10.110.71' ## server에 출력되는 ip를 입력해주세요 ##
PORT = 9876

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

# Create CAN socket
can_socket = socket.socket(socket.AF_CAN, socket.SOCK_RAW, socket.CAN_RAW)
can_socket.bind(('vcan0',))


def recv_data(client_socket):
    while True:
        data = client_socket.recv(1024)
        print("recive : ", repr(data.decode()))

start_new_thread(recv_data, (client_socket,))
print('>> Connect Server')

while True:
    can_packet = can_socket.recv(1024)
    print("Received CAN packet:", can_packet.hex())
    canId = can_packet[:4]
    canData = can_packet[4:]
    message = canId + canData
    if message == 'quit':
        close_data = message
        break

    client_socket.send(message.decode())

client_socket.close()
