import socket
import struct
import select
import time

# CAN to Ethernet
def can_to_eth(can_packet):
    # Convert CAN packet to Ethernet packet format
    eth_packet = struct.pack('!8B', 0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF, 0x01, 0x02) + can_packet
    return eth_packet

# Ethernet to CAN
def eth_to_can(eth_packet):
    # Extract CAN packet from Ethernet packet
    can_packet = eth_packet[8:]
    return can_packet

# Create CAN socket
can_socket = socket.socket(socket.AF_CAN, socket.SOCK_RAW, socket.CAN_RAW)
can_socket.bind(('vcan0',))

# Create Ethernet socket
eth_socket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x0003))
eth_socket.bind(('veth1',0))

# Main loop
while True:
    # Read CAN packet
    can_packet = can_socket.recv(16)
    print("Received CAN packet:", can_packet.hex())  # 출력 확인
    
    # Convert CAN to Ethernet
    eth_packet = can_to_eth(can_packet)
    print("Converted CAN packet to Ethernet:", eth_packet.hex())  # 출력 확인
    
    # Send Ethernet packet
    eth_socket.send(eth_packet)
    print("Sent Ethernet packet:", eth_packet.hex())  # 출력 확인

    # Wait for a short period to avoid immediate collision
    time.sleep(0.1)

    # Check if Ethernet packet is available
    ready_to_read, _, _ = select.select([eth_socket], [], [], 0.1)
    if eth_socket in ready_to_read:
        # Read Ethernet packet
        eth_packet = eth_socket.recv(1024)
        print("Received Ethernet packet:", eth_packet.hex())  # 출력 확인

        # Convert Ethernet to CAN
        can_packet = eth_to_can(eth_packet)
        print("Converted Ethernet packet to CAN:", can_packet.hex())  # 출력 확인

        # Send CAN packet
        can_socket.send(can_packet)
        print("Sent CAN packet:", can_packet.hex())  # 출력 확인

