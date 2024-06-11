import can
import logging
import os
import sys

##Window용
#sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

##Docker용
sys.path.append("/home/Vhal-View-App/Window/Vhal_CLI_API")
from commands.Vhal_api import set, get, list, set_integer, set_float, process, set_connection, connection


def main():
    #user_select_emulator = input("Trying to connect to the remote emulator? (y/n)")
    #if user_select_emulator == "yes" or user_select_emulator == "y" or user_select_emulator == "YES" or user_select_emulator == "Y":
     #   address = input("Please enter the IP address (ex:10.10.10.10)")
        #port = input("Please enter the port address[4]")
        #set_connection("remote", address, port)
        #connection("remote")


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
            logging.info('START CAN BUS Receive')
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
                    set_integer("289408009", ignitionState, "0")

                if prev_gearSelection != gearSelection:
                    prev_gearSelection = gearSelection
                    set_integer("289408000", gearSelection, "0")

                if prev_vehicleSpeed != vehicleSpeed:
                    prev_vehicleSpeed = vehicleSpeed
                    set_float("291504648 ", vehicleSpeed, "0")

                if prev_chargePortConnection != chargePortConnection:
                    prev_chargePortConnection = chargePortConnection
                    set_integer("287310603", chargePortConnection, "0")

                if prev_ChargePortOpen != ChargePortOpen:
                    prev_ChargePortOpen = ChargePortOpen
                    set_integer("287310602", ChargePortOpen, "0")

                if prev_parkingBreakAuto != parkingBreakAuto:
                    prev_parkingBreakAuto = parkingBreakAuto
                    set_integer( "287310851", parkingBreakAuto, "0")

    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
