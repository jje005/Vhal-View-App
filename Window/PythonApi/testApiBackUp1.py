import numpy as np
import subprocess
import re
import can
import sys
import VhalManager
sys.path.append("../model/vehiclePropValue")
from VehiclePropValueList import VehiclePropValueList
from VehiclePropValue import VehiclePropValue

# #action 실행 함수
# def runCommand(action, propertyId=None, value=None, area=None):
#     if action == "get" :
#         adb_command = getVHAL(propertyId)
#     elif action == "set":
#         adb_command = setVHAL(propertyId, value, area)
#     elif action =="list":
#         adb_command = getVHALList()
#     else:
#         print("Unsupported action. Please enter 'get', 'set', or 'list'")
#         return
    
#     print("\n")
#     print(adb_command)
#     try:

#         result = subprocess.run(adb_command, capture_output=True, text=True, shell=True)
        
#         print("ADB Command Output:")
#         print(result.stdout)
#     except Exception as e:
#         print("Error occurred while executing adb command : ", e)


# # get 함수
# def getVHAL(propertyId):
#     return f"adb shell dumpsys android.hardware.automotive.vehicle.IVehicle/default --get {propertyId}"

# # list 함수
# def getVHALList():
#     return "adb shell dumpsys android.hardware.automotive.vehicle.IVehicle/default --list"

# # set 함수
# def setVHAL(propertyId, value, areaId):
#     adb_command = "adb shell dumpsys android.hardware.automotive.vehicle.IVehicle/default --set "
#     adb_command += propertyId +" "
#     adb_command += matchValueType(propertyId, value, areaId)

#     return adb_command

# # 속성값을 가져오는 함수
# def matchValueType(propertyId, value, areaId):
#     vehiclePropValueList =  VehiclePropValueList(propertyId)
#     result = subprocess.run(getVHAL(propertyId), capture_output=True, text=True, shell=True)

#     lines = result.stdout.split('\n')[:-3] 
#     datas_dict = {}
#     for line in lines :
#         data_str = line.replace('{', ',')
#         data_str = data_str[:-2]
#         key_value_pairs = [pair.strip() for pair in data_str.split(',')]

#         for pair in  key_value_pairs[1:]:
#             key, currentValue = pair.split(':')
#             datas_dict[key.strip()] = currentValue.strip()
#         vehicleValue = parsingVhal(datas_dict)
#         vehiclePropValueList.add(vehicleValue)
    
#     entry = vehiclePropValueList.getVehiclePropValue(areaId)    
#     output = checkValueType(entry.getDataType(), value) + checkValueArea(areaId)
#     return output

# def checkValueType(valueType, value):
#     return setValueType(valueType) + value +" "

# def setValueType(valueType):
#     if valueType == "int32":
#         return "-i "
#     elif valueType == "int64":
#         return "-i64 "
#     elif valueType == "float":
#         return "-f "
#     elif valueType == "str":
#         return "-s "
#     elif valueType == "bytes":
#         return "-b "
#     else :
#         return "-s "    

# def checkValueArea(areaId):
#     return "-a " + areaId

# def parsingVhal(datas_dict):
#     timestamp = datas_dict.get("timestamp", None)
#     areaId = datas_dict.get("areaId", None)
#     prop = datas_dict.get("prop", None)
#     status = datas_dict.get("status", None)

#     dataType =  ""
#     int32Values = datas_dict.get("int32Values", [])
#     if int32Values == "[]":
#         int32Values = list()
#     else:
#         dataType = "int32"

#     floatValues = datas_dict.get("floatValues", [])
#     if floatValues == "[]":
#         floatValues = list()
#     else:
#         dataType = "float"

#     int64Values = datas_dict.get("int64Values", [])
#     if int64Values == "[]":
#         int64Values = list()
#     else:
#         dataType = "int64"

#     byteValues = datas_dict.get("byteValues", [])
#     if byteValues == "[]":
#         byteValues = list()
#     else:
#         dataType = "bytes"

#     stringValues = datas_dict.get("stringValue", [])
#     if stringValues == " " or stringValues == "":
#        stringValues = None
#     else:
#         dataType = "str"
#     entry = VehiclePropValue(timestamp, areaId, prop, status, dataType, int32Values=int32Values, floatValues=floatValues, int64Values=int64Values, byteValues=byteValues, stringValues=stringValues)

#     return entry


#1차 데모
# def main():
#     # CAN 네트워크에 연결
#     bus = can.interface.Bus(channel='vcan0', bustype='socketcan')

#     # 메시지 수신
#     try:
#         while True:
#             message = bus.recv()  # 메시지가 수신될 때까지 대기
#             if message:
#                 print(f'Received: {message.arbitration_id}')
#                 canId = message.arbitration_id
#                 canValue = str(message.data[0])
#                 print(canValue)
#                 if canId == 1:
#                     VhalManager.runCommand("set", '358614275', canValue, "49")

#     except KeyboardInterrupt:
#         pass



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