import datetime
import os
import subprocess
import sys

import can.interface

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Vhal_CLI_API')))


def main():
    bus = can.interface.Bus(channel='vcan0', bustype='socketcan')

    prev_iginitionState = None
    prev_gearSelection = None
    prev_vehicleSpeed = None
    prev_chargePortConnection = None
    prev_ChargePortOpen = None
    prev_parkingBreakAuto = None

    print("CAN Bus Read Start")
    in_count = 0

    try:
        while True:
            # 100ms 타임 아웃 설정
            message = bus.recv(timeout=0.1)

            if message:
                can_iuput_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print("CAN Signal Input", can_iuput_time)
                can_id = message.arbitration_id
                iginition_state = str(message.data[0])
                gear_selection = str(message.data[1])
                vehicle_speed = str(message.data[2])
                charge_port_connection = str(message.data[3])
                charge_port_open = str(message.data[4])
                parking_break_auto = str(message.data[5])

                if in_count % 10 == 0:
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

    except KeyboardInterrupt:
        pass

    if __name__ == "__main__":
        main()