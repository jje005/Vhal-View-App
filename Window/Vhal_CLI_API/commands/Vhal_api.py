import subprocess
import sys
import logging

sys.path.append("D:/00.Project/SDV/Vhal-View-App/Window/Vhal_CLI_API/model")

from VehiclePropValue import VehiclePropValue
from VehiclePropValueList import Vehiclepropvaluelist

process = subprocess.Popen(['adb', 'shell'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                           text=True)

logging.basicConfig(
    format='%(asctime)s.%(msecs)03d - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.DEBUG,
    handlers=[logging.StreamHandler(sys.stdout)]
)


# set 함수 (value Type을 모를때 사용)
def set_vhal(process, property_id, value, area_id):
    adb_command = "dumpsys android.hardware.automotive.vehicle.IVehicle/default --set "
    adb_command += property_id + " "
    adb_command += match_value_type(property_id, value, area_id)
    try:
        process.stdin.write(adb_command)
        process.stdin.flush()
    except ValueError:
        print("Error: Unable to write to process")


# Float 타입 set 메소드
def set_vhal_Integer(process, propertyId, value, areaId):
    adb_command = f"dumpsys android.hardware.automotive.vehicle.IVehicle/default --set {propertyId} -f {value} -a {areaId}\n"
    try:
        process.stdin.write(adb_command)
        process.stdin.flush()
    except ValueError:
        print("Error: Unable to write to process")


# Integer 타입 set 메소드
def set_vhal_Integer(process, propertyId, value, areaId):
    adb_command = f"dumpsys android.hardware.automotive.vehicle.IVehicle/default --set {propertyId} -i {value} -a {areaId}\n"
    try:
        process.stdin.write(adb_command)
        process.stdin.flush()
    except ValueError:
        print("Error: Unable to write to process")


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
    adb_command = f"dumpsys android.hardware.automotive.vehicle.IVehicle/default --get {property_id}"
    try:
        process.stdin.write(adb_command)
        output = process.communicate()
        print(output)
    except ValueError:
        logging.info("Error : Can't fine Property Id ")


def get_vhal_list():
    adb_command = "dumpsys android.hardware.automotive.vehicle.IVehicle/default --list"
    try:
        process.stdin.write(adb_command)
        process.stout()
        process.stdin.flush()

    except ValueError:
        logging.info("Error : Can't fine Property Id List ")


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
    entry = VehiclePropValue(timestamp, area_id, prop, status, data_type, int32Values=int32_values,
                             floatValues=float_values, int64Values=int64_values, byteValues=byte_values,
                             stringValues=string_values)

    return entry
