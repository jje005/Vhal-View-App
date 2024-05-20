import socket
import struct
import select
import time

# CAN to Ethernet
def can_to_eth(canId, canData):
    # Convert CAN packet to Ethernet packet format
    eth_packet = struct.pack('!8B', 0xFF, 0xFF, 0xFF, 0xFF, 0xEE, 0xFF, 0x03, 0x02) + canId + canData
    return eth_packet

# Create CAN socket
can_socket = socket.socket(socket.AF_CAN, socket.SOCK_RAW, socket.CAN_RAW)
can_socket.bind(('vcan0',))

# Create Ethernet socket
eth_socket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x0003))
eth_socket.bind(('veth1',0))

# Main loop
while True:
    # Read CAN packet
    can_packet = can_socket.recv(1024)
    print("Received CAN packet:", can_packet.hex())
    canId = can_packet[:4]
    canData = can_packet[4:]
    
    # Convert CAN to Ethernet
    eth_packet = can_to_eth(canId, canData)
    print("Converted CAN packet to Ethernet:", eth_packet.hex()) 
    
    # Send Ethernet packet
    eth_socket.send(eth_packet)
    print("Sent Ethernet packet:", eth_packet.hex()) 

