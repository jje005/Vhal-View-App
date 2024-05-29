import datetime
import os
import subprocess
import sys
import asyncio

import can.interface

from vcan.vcan_handler_backup import setVHAL

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Vhal_CLI_API')))


def process_can_message(message):
    print(f"Received CAN message: {message}")

    can_iuput_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("CAN Signal Input", can_iuput_time)

    iginition_state = str(message.data[0])
    gear_selection = str(message.data[1])
    vehicle_speed = str(message.data[2])
    charge_port_connection = str(message.data[3])
    charge_port_open = str(message.data[4])
    parking_break_auto = str(message.data[5])

    if iginition_state is not None:
        result = subprocess.run(setVHAL("289408009", iginition_state, "0"), capture_output=True,
                                text=True, shell=True)

    if gear_selection is not None:
        result = subprocess.run(setVHAL("289408000", gear_selection, "0"), capture_output=True,
                                text=True, shell=True)

    if vehicle_speed is not None:
        result = subprocess.run(setVHAL("291504648", vehicle_speed, "0"), capture_output=True, text=True,
                                shell=True)

    if charge_port_connection is not None:
        result = subprocess.run(setVHAL("287310603", charge_port_connection, "0"), capture_output=True,
                                text=True, shell=True)

    if charge_port_open is not None:
        result = subprocess.run(setVHAL("287310602", charge_port_open, "0"), capture_output=True,
                                text=True, shell=True)

    if parking_break_auto is not None:
        result = subprocess.run(setVHAL("287310851", parking_break_auto, "0"), capture_output=True,
                                text=True, shell=True)


async def read_can_messages(bus):
    while True:
        messages = bus.recv(0.1)
        if messages:
            process_can_message(messages)
        await asyncio.sleep(0.01)


async def main():
    print("CAN Bus Read Start")
    bus = can.interface.Bus(channel='vcan0', bustype='socketcan')

    print("CAN Bus Read Start")
    in_count = 0

    try:
        await read_can_messages(bus)
    except KeyboardInterrupt:
        pass

    if __name__ == "__main__":
        await main()
