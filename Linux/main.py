from socket import *

HOST = '0.0.0.0'
PORT = 3000
BUFSIZE = 1024

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind((HOST, PORT))
serverSocket.listen(1)

print('Server listening on port', PORT)

while True:
    clientSocket, addr_info = serverSocket.accept()
    print('Accepted connection from', addr_info)
    
    data = clientSocket.recv(1024)
    print('Received data:', data.decode())
    
    # 여기서 적절한 응답을 보내도록 수정
    
    clientSocket.close()
