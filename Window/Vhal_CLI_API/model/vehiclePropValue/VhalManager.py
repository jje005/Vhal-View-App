import sys
import subprocess
from VehiclePropValueList import Vehiclepropvaluelist
from VehiclePropValue import VehiclePropValue

class VhalManager:
    vehiclePropValueList = Vehiclepropvaluelist


    def __init__(self):
        return


    def runCommand(userInput=None):
        userInput
        inputAdbCommand = VhalManager.run(propertyId, value, area)
        try:
            result = subprocess.run(inputAdbCommand, capture_output=True, text=True, shell=True)

            print("ADB Command Output:")
            print(result.stdout)
        except Exception as e:
            print("Error occurred while executing adb command : ", e)


    @staticmethod
    def ValList():
        return "adb shell dumpsys android.hardware.automotive.vehicle.IVehicle/default --list"


    @staticmethod
    def VahlGet(property_id):
        return f"adb shell dumpsys android.hardware.automotive.vehicle.IVehicle/default --get {property_id}"


    @staticmethod
    def VhalSet(propertyId, value, areaId):
        adbCommand = "adb shell dumpsys android.hardware.automotive.vehicle.IVehicle/default --set "
        adbCommand += propertyId +" "
        adbCommand += VhalManager.matchValueType(propertyId, value, areaId)
        return adbCommand
    

    def matchValueType(propertyId, value, areaId):
        vehiclePropValueList =  Vehiclepropvaluelist(propertyId)
        result = subprocess.run(VhalManager.run(propertyId), capture_output=True, text=True, shell=True)

        lines = result.stdout.split('\n')[:-3] 
        datas_dict = {}
        for line in lines :
            data_str = line.replace('{', ',')
            data_str = data_str[:-2]
            key_value_pairs = [pair.strip() for pair in data_str.split(',')]

            for pair in  key_value_pairs[1:]:
                key, currentValue = pair.split(':')
                datas_dict[key.strip()] = currentValue.strip()
            vehicleValue = VhalManager.parsingVhal(datas_dict)
            vehiclePropValueList.add(vehicleValue)
        
        entry = vehiclePropValueList.getVehiclePropValue(areaId)    
        output = VhalManager.checkValueType(entry.getDataType(), value) + VhalManager.checkValueArea(areaId)
        return output


    def checkValueType(valueType, value):
        return VhalManager.setValueType(valueType) + value +" "


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
        else :
            return "-s "    


    def checkValueArea(areaId):
        return "-a " + areaId


    def parsingVhal(datas_dict):
        timestamp = datas_dict.get("timestamp", None)
        areaId = datas_dict.get("areaId", None)
        prop = datas_dict.get("prop", None)
        status = datas_dict.get("status", None)

        dataType =  ""
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
        entry = VehiclePropValue(timestamp, areaId, prop, status, dataType, int32_values=int32Values, float_values=floatValues, int64_values=int64Values, byte_values=byteValues, string_values=stringValues)

        return entry