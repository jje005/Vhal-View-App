import subprocess
import re
import can
import time
import logging

import sys
sys.path.append("/home/Vhal-View-App/Window/Vhal_CLI_API/")
from commands.Vhal_api import set, get, list, set_integer, set_float, process


def main():
    bus = can.interface.Bus(channel='vcan0', bustype='socketcan')

    prev_ignitionState = 0
    prev_gearSelection = 0
    prev_vehicleSpeed = 0
    prev_chargePortConnection = 0
    prev_ChargePortOpen = 0
    prev_parkingBreakAuto = 0


    # 메시지 수신
    inCount = 0
    try:
        while True:
            logging.info('START CAN BUS REVEIVE')
            message = bus.recv()  # 100ms 타임아웃 설정

            if message:
                ignitionState = str(message.data[0])
                gearSelection = str(message.data[1])
                vehicleSpeed = str(message.data[2])
                chargePortConnection = str(message.data[3])
                ChargePortOpen = str(message.data[4])
                parkingBreakAuto = str(message.data[5])

                if prev_ignitionState != ignitionState:
                    prev_ignitionState = ignitionState
                    set_integer(process, "289408009", ignitionState, "0")

                if prev_gearSelection != gearSelection:
                    prev_gearSelection = gearSelection
                    set_integer(process, "289408009", gearSelection, "0")

                if prev_vehicleSpeed != vehicleSpeed:
                    prev_vehicleSpeed = vehicleSpeed
                    set_float(process, "289408009", vehicleSpeed, "0")

                if prev_chargePortConnection != chargePortConnection:
                    prev_chargePortConnection = chargePortConnection
                    set_integer(process, "289408009", chargePortConnection, "0")

                if prev_ChargePortOpen != ChargePortOpen:
                    prev_ChargePortOpen = ChargePortOpen
                    set_integer(process, "289408009", ChargePortOpen, "0")

                if prev_parkingBreakAuto != parkingBreakAuto:
                    prev_parkingBreakAuto = parkingBreakAuto
                    set_integer(process, "289408009", parkingBreakAuto, "0")


    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()