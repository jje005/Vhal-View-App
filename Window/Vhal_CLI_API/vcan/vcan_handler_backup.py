
import subprocess
import re
import can
import datetime


from model.VehiclePropValueList import Vehiclepropvaluelist
from model.VehiclePropValue import VehiclePropValue


# cmd 명령 실행 함수
def run_adb_command(command):
    result = subprocess.run(command, capture_output=True, text=True)
    return result.stdout


# action 실행 함수
def execute_adb_command(action, propertyId=None, value=None, area=None):
    if action == "get":
        adb_command = getVHAL(propertyId)
    elif action == "set":
        adb_command = setVHAL(propertyId, value, area)
    elif action == "list":
        adb_command = getVHALList()
    else:
        print("Unsupported action. Please enter 'get', 'set', or 'list'.")
        return

    print("\n")
    print(adb_command)
    try:

        result = subprocess.run(adb_command, capture_output=True, text=True, shell=True)

        print("ADB Command Output:")
        print(result.stdout)
    except Exception as e:
        print("Error occurred while executing adb command:", e)


# get 함수
def getVHAL(propertyId):
    return f"adb shell dumpsys android.hardware.automotive.vehicle.IVehicle/default --get {propertyId}"


# list 함수
def getVHALList():
    return "adb shell dumpsys android.hardware.automotive.vehicle.IVehicle/default --list"


# set 함수
def setVHAL(propertyId, value, areaId):
    adb_command = "adb shell dumpsys android.hardware.automotive.vehicle.IVehicle/default --set "
    adb_command += propertyId + " "
    adb_command += matchValueType(propertyId, value, areaId)
    result = subprocess.run(adb_command, capture_output=True, text=True, shell=True)
    print(adb_command)
    return adb_command


# 속성값을 가져오는 함수
def matchValueType(propertyId, value, areaId):
    vehiclePropValueList = VehiclePropValueList(propertyId)
    result = subprocess.run(getVHAL(propertyId), capture_output=True, text=True, shell=True)

    lines = result.stdout.split('\n')[:-3]
    datas_dict = {}
    for line in lines:
        data_str = line.replace('{', ',')
        data_str = data_str[:-2]
        key_value_pairs = [pair.strip() for pair in data_str.split(',')]

        for pair in key_value_pairs[1:]:
            key, currentValue = pair.split(':')
            datas_dict[key.strip()] = currentValue.strip()
        vehicleValue = parsingVhal(datas_dict)
        vehiclePropValueList.add(vehicleValue)

    entry = vehiclePropValueList.getVehiclePropValue(areaId)
    output = checkValueType(entry.getDataType(), value) + checkValueArea(areaId)
    return output


def checkValueType(valueType, value):
    return setValueType(valueType) + value + " "


def setValueType(valueType):
    if valueType == "int32":
        return "-i "
    elif valueType == "int64":
        return "-i64 "
    elif valueType == "float":
        return "-f "
    elif valueType == "str":
        return "-s "
    elif valueType == "bytes":
        return "-b "
    else:
        return "-s "


def checkValueArea(areaId):
    return "-a " + areaId


def parsingVhal(datas_dict):
    timestamp = datas_dict.get("timestamp", None)
    areaId = datas_dict.get("areaId", None)
    prop = datas_dict.get("prop", None)
    status = datas_dict.get("status", None)

    dataType = ""
    int32Values = datas_dict.get("int32Values", [])
    if int32Values == "[]":
        int32Values = list()
    else:
        dataType = "int32"

    floatValues = datas_dict.get("floatValues", [])
    if floatValues == "[]":
        floatValues = list()
    else:
        dataType = "float"

    int64Values = datas_dict.get("int64Values", [])
    if int64Values == "[]":
        int64Values = list()
    else:
        dataType = "int64"

    byteValues = datas_dict.get("byteValues", [])
    if byteValues == "[]":
        byteValues = list()
    else:
        dataType = "bytes"

    stringValues = datas_dict.get("stringValue", [])
    if stringValues == " " or stringValues == "":
        stringValues = None
    else:
        dataType = "str"
    entry = VehiclePropValue(timestamp, areaId, prop, status, dataType, int32Values=int32Values,
                             floatValues=floatValues, int64Values=int64Values, byteValues=byteValues,
                             stringValues=stringValues)

    return entry


def main():
    # CAN 네트워크에 연결
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
                    # print("CAN Signal Value to iginit State : " + iginitionState)
                    # print("CAN Signal Value to Gear Selection : " + gearSelection)
                    # print("CAN Signal Value to Vehicle Speed : " + vehicleSpeed)
                    # print("CAN Signal Value to Charege Port Connection : " + chargePortConnection)
                    # print("CAN Signal Value to Charege Port Open : " + ChargePortOpen)
                    # print("CAN Signal Value to Auto Parking break : " + parkingBreakAuto)

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

                # setVHAL("289408009", iginitionState, "0")
                # setVHAL("289408000", gearSelection, "0")
                # setVHAL("291504648", vehicleSpeed, "0")
                # setVHAL("287310603", chargePortConnection, "0")
                # setVHAL("287310602", ChargePortOpen, "0")
                # setVHAL("287310851", parkingBreakAuto, "0")


    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()