import subprocess

from model.vehiclePropValue.VehiclePropValue import VehiclePropValue
from model.vehiclePropValue.VehiclePropValueList import Vehiclepropvaluelist


# cmd 명령 실행 함수
def run_adb_command(command):
    result = subprocess.run(command, capture_output=True, text=True)
    return result.stdout


# set 함수
def set_vhal(property_id, value, area_id):
    adb_command = "adb shell dumpsys android.hardware.automotive.vehicle.IVehicle/default --set "
    adb_command += property_id + " "
    adb_command += match_value_type(property_id, value, area_id)

    return adb_command


# 전체 list에서 id에 해당하는 vhal의 area값을 가져오는 함수
def match_value_type(propertyId, value, areaId):
    vehicle_prop_value_list = Vehiclepropvaluelist(propertyId)
    result = subprocess.run(get_vhal(propertyId), capture_output=True, text=True, shell=True)

    lines = result.stdout.split('\n')[:-3]
    data_dict = {}
    for line in lines:
        data_str = line.replace('{', ',')
        data_str = data_str[:-2]
        key_value_pairs = [pair.strip() for pair in data_str.split(',')]

        for pair in key_value_pairs[1:]:
            key, current_value = pair.split(':')
            data_dict[key.strip()] = current_value.strip()
        vehicle_value = parsing_vhal(data_dict)
        vehicle_prop_value_list.add(vehicle_value)

    entry = vehicle_prop_value_list.getVehiclePropValue(areaId)
    output = check_value_type(entry.getDataType(), value) + check_value_area(areaId)
    return output


def check_value_type(value_type, value):
    return set_value_type(value_type) + value + " "


def get_vhal(property_id):
    return f"adb shell dumpsys android.hardware.automotive.vehicle.IVehicle/default --get {property_id}"


def get_vhal_list():
    return "adb shell dumpsys android.hardware.automotive.vehicle.IVehicle/default --list"


def set_value_type(value_type):
    if value_type == "int32":
        return "-i "
    elif value_type == "int64":
        return "-i64 "
    elif value_type == "float":
        return "-f "
    elif value_type == "str":
        return "-s "
    elif value_type == "bytes":
        return "-b "
    else:
        return "-s "


def check_value_area(area_id):
    return "-a " + area_id


def parsing_vhal(data_dict):
    timestamp = data_dict.get("timestamp", None)
    area_id = data_dict.get("areaId", None)
    prop = data_dict.get("prop", None)
    status = data_dict.get("status", None)

    data_type = ""
    int32_values = data_dict.get("int32_values", [])
    if int32_values == "[]":
        int32_values = list()
    else:
        data_type = "int32"

    float_values = data_dict.get("float_values", [])
    if float_values == "[]":
        float_values = list()
    else:
        data_type = "float"

    int64_values = data_dict.get("int64_values", [])
    if int64_values == "[]":
        int64_values = list()
    else:
        data_type = "int64"

    byte_values = data_dict.get("byte_values", [])
    if byte_values == "[]":
        byte_values = list()
    else:
        data_type = "bytes"

    string_values = data_dict.get("stringValue", [])
    if string_values == " " or string_values == "":
        string_values = None
    else:
        data_type = "str"
    entry = VehiclePropValue(timestamp, area_id, prop, status, data_type, int32Values=int32_values, floatValues=float_values, int64Values=int64_values, byteValues=byte_values, stringValues=string_values)


    return entry
