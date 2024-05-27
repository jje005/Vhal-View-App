import can
import sys
import VhalManager
sys.path.append("../model/vehiclePropValue")



#1차 데모 
def main():
    # CAN 네트워크에 연결
    bus = can.interface.Bus(channel='vcan0', bustype='socketcan')

    # 메시지 수신
    try:
        while True:
            message = bus.recv()  # 메시지가 수신될 때까지 대기
            if message:
                print(f'Received: {message.arbitration_id}')
                canId = message.arbitration_id
                iginitionState = str(message.data[0])
                gearSelection = str(message.data[1])
                vehicleSpeed = str(message.data[2])
                chargePortConnection = str(message.data[3])
                ChargePortOpen = str(message.data[4])
                parkingBreakAuto = str(message.data[5])


                print(canId)

                print("CAN Signal Value to iginit State : " + iginitionState)
                print("CAN Signal Value to Gear Selection : " + gearSelection)
                print("CAN Signal Value to Vehicle Speed : " + vehicleSpeed)
                print("CAN Signal Value to Charege Port Connection : " + chargePortConnection)
                print("CAN Signal Value to Charege Port Open : " + ChargePortOpen)
                print("CAN Signal Value to Auto Parking break : " + parkingBreakAuto)



                VhalManager.set("289408009", iginitionState, "0")
                VhalManager.set("289408000", gearSelection, "0")
                VhalManager.set("291504648", vehicleSpeed, "0")
                VhalManager.set("287310603", chargePortConnection, "0")
                VhalManager.set("287310602", ChargePortOpen, "0")
                VhalManager.set("289408009", parkingBreakAuto, "0")

    except KeyboardInterrupt:
        pass
	        

if __name__ == "__main__":
    main()
                # 사용자 입력 받기
            # user_input = input("Enter command (e.g., 'adb set property_id value area'): ").split()

            # 입력이 유효한지 확인
            # if not user_input:
            #     print("Invalid input. Please enter a command.")
            #     continue

            # action = user_input[0]
            # if action == "list":
            #     runCommand(action)
            # elif action == "get":
            #     property_id = user_input[1]
            #     runCommand(action, property_id)
            # elif action == "set":
            #     property_id = user_input[1]
            #     property_value = user_input[2]
            #     property_area = user_input[3]
            #     runCommand(action, property_id, property_value, property_area)
            # else:
            #     print("Invalid input. Please enter a valid command.")