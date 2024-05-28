
import subprocess
import re
import can
import datetime

from commands.Vhal_api import set_vhal

def main():
    bus = can.interface.Bus(channel='vcan0', bustype='socketcan')

    prev_iginitionState = 1
    prev_gearSelection = 4
    prev_vehicleSpeed = 0
    prev_chargePortConnection = 1
    prev_ChargePortOpen = 1
    prev_parkingBreakAuto = 1

    print("CAN Bus Read Start")
    # 메시지 수신
    inCount = 0
    try:
        while True:
            message = bus.recv(timeout=0.1)  # 100ms 타임아웃 설정

            if message:
                canInputTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print("CAN Signal Input", canInputTime)
                canId = message.arbitration_id
                iginitionState = str(message.data[0])
                gearSelection = str(message.data[1])
                vehicleSpeed = str(message.data[2])
                chargePortConnection = str(message.data[3])
                ChargePortOpen = str(message.data[4])
                parkingBreakAuto = str(message.data[5])

                if inCount % 10 == 0:
                    if iginitionState is not None:
                        result = subprocess.run(set_vhal("289408009", iginitionState, "0"), capture_output=True,
                                                text=True, shell=True)

                    if gearSelection is not None:
                        result = subprocess.run(set_vhal("289408000", gearSelection, "0"), capture_output=True,
                                                text=True, shell=True)

                    if vehicleSpeed is not None:
                        result = subprocess.run(set_vhal("291504648", vehicleSpeed, "0"), capture_output=True, text=True,
                                                shell=True)

                    if chargePortConnection is not None:
                        result = subprocess.run(set_vhal("287310603", chargePortConnection, "0"), capture_output=True,
                                                text=True, shell=True)

                    if ChargePortOpen is not None:
                        result = subprocess.run(set_vhal("287310602", ChargePortOpen, "0"), capture_output=True,
                                                text=True, shell=True)

                    if parkingBreakAuto is not None:
                        result = subprocess.run(set_vhal("287310851", parkingBreakAuto, "0"), capture_output=True,
                                                text=True, shell=True)

    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()