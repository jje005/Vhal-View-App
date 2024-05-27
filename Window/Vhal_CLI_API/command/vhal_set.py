import subprocess

from Window.Vhal_CLI_API.VhalCommand import getVHAL, getVHALList
from Window.Vhal_CLI_API.model.vehiclePropValue.VehiclePropValue import VehiclePropValue
from Window.Vhal_CLI_API.model.vehiclePropValue.VehiclePropValueList import Vehiclepropvaluelist


#cmd 명령 실행 함수
def run_adb_command(command):
    result = subprocess.run(command, capture_output=True, text=True)
    return result.stdout


#action 실행 함수
def execute_adb_command(action, property_id=None, value=None, area=None):
    if action == "get":
        adb_command = getVHAL(property_id)
    elif action == "set":
        adb_command = set_vhal(property_id, value, area)
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


# set 함수
def set_vhal(property_id, value, area_id):
    adb_command = "adb shell dumpsys android.hardware.automotive.vehicle.IVehicle/default --set "
    adb_command += property_id + " "
    adb_command += match_value_type(property_id, value, area_id)

    return adb_command


# 전체 list에서 id에 해당하는 vhal을 가져와 area값을 가져오는 함수
def match_value_type(property_id, value, area_id):
    vehicle_prop_value_list = Vehiclepropvaluelist(property_id)
    result = subprocess.run(getVHAL(property_id), capture_output=True, text=True, shell=True)

    lines = result.stdout.split('\n')[:-3]
    datas_dict = {}
    for line in lines:
        data_str = line.replace('{', ',')
        data_str = data_str[:-2]
        key_value_pairs = [pair.strip() for pair in data_str.split(',')]

        for pair in key_value_pairs[1:]:
            key, current_value = pair.split(':')
            datas_dict[key.strip()] = current_value.strip()
        vehicle_value = parsing_vhal(datas_dict)
        vehicle_prop_value_list.add(vehicle_value)

    entry = vehicle_prop_value_list.getVehiclePropValue(area_id)
    output = check_value_type(entry.getDataType(), value) + check_value_area(area_id)
    return output


def check_value_type(value_type, value):
    return set_value_type(value_type) + value + " "


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


def parsing_vhal(datas_dict):
    timestamp = datas_dict.get("timestamp", None)
    area_id = datas_dict.get("areaId", None)
    prop = datas_dict.get("prop", None)
    status = datas_dict.get("status", None)

    data_type = ""
    int32_values = datas_dict.get("int32_values", [])
    if int32_values == "[]":
        int32_values = list()
    else:
        data_type = "int32"

    float_values = datas_dict.get("float_values", [])
    if float_values == "[]":
        float_values = list()
    else:
        data_type = "float"

    int64_values = datas_dict.get("int64_values", [])
    if int64_values == "[]":
        int64_values = list()
    else:
        data_type = "int64"

    byte_values = datas_dict.get("byte_values", [])
    if byte_values == "[]":
        byte_values = list()
    else:
        data_type = "bytes"

    string_values = datas_dict.get("stringValue", [])
    if string_values == " " or string_values == "":
        string_values = None
    else:
        data_type = "str"
    entry = VehiclePropValue(timestamp, area_id, prop, status, data_type, int32_values=int32_values,
                             float_values=float_values, int64_values=int64_values, byte_values=byte_values,
                             string_values=string_values)

    return entry