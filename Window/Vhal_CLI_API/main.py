import argparse
import datetime
import subprocess

import can.interface

from Window.Vhal_CLI_API.VhalCommand import setVHAL



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
            message = bus.recv(timeout=0.1) #100ms 타임아웃 설정

            if message:
                can_iuput_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print("CAN Signal Input", can_iuput_time)
                canId = message.arbitration_id
                iginitionState = str(message.data[0])
                gearSelection = str(message.data[1])
                vehicleSpeed = str(message.data[2])
                chargePortConnection = str(message.data[3])
                ChargePortOpen = str(message.data[4])
                parkingBreakAuto = str(message.data[5])

                if in_count % 10 == 0:
                    if iginitionState is not None:
                        result = subprocess.run(setVHAL("289408009", iginitionState, "0"), capture_output=True,
                                                text=True, shell=True)

                    if gearSelection is not None:
                        result = subprocess.run(setVHAL("289408000", gearSelection, "0"), capture_output=True,
                                                text=True, shell=True)

                    if vehicleSpeed is not None:
                        result = subprocess.run(setVHAL("291504648", vehicleSpeed, "0"), capture_output=True, text=True,
                                                shell=True)

                    if chargePortConnection is not None:
                        result = subprocess.run(setVHAL("287310603", chargePortConnection, "0"), capture_output=True,
                                                text=True, shell=True)

                    if ChargePortOpen is not None:
                        result = subprocess.run(setVHAL("287310602", ChargePortOpen, "0"), capture_output=True,
                                                text=True, shell=True)

                    if parkingBreakAuto is not None:
                        result = subprocess.run(setVHAL("287310851", parkingBreakAuto, "0"), capture_output=True,
                                                text=True, shell=True)

    except KeyboardInterrupt:
        pass

    if __name__ == "__main__":
        main()