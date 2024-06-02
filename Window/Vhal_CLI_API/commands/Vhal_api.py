import logging
import subprocess
import sys
import typer

#CLI 라이브러리
app = typer.Typer()
sys.path.append("D:/00.Project/SDV/Vhal-View-App/Window/Vhal_CLI_API/model")

from VehiclePropValue import VehiclePropValue
from VehiclePropValueList import Vehiclepropvaluelist

sys.path.append("D:/00.Project/SDV/Vhal-View-App/Window/Vhal_CLI_API/network")
from ConnectionManager import connection_instance
app.add_typer(connection_instance.app, name="connection")


process = subprocess.Popen(['adb', 'shell'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                           text=True)

logging.basicConfig(
    format='%(asctime)s.%(msecs)03d - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.DEBUG,
    handlers=[logging.StreamHandler(sys.stdout)]
)


@app.command()
def set(property_id: int, value, area_id: int):
    adb_command = "dumpsys android.hardware.automotive.vehicle.IVehicle/default --set "
    adb_command += property_id + " "
    adb_command += match_value_type(property_id, value, area_id)
    try:
        process.stdin.write(adb_command)
        process.stdin.flush()
    except ValueError:
        typer.echo("Error: Unable to write to process")


@app.command()
def set_float(propertyId: int, value: int, areaId: float):
    adb_command = f"dumpsys android.hardware.automotive.vehicle.IVehicle/default --set {propertyId} -f {value} -a {areaId}\n"
    try:
        process.stdin.write(adb_command)
        process.stdin.flush()
    except ValueError:
        typer.echo("Error: Unable to write to process")


@app.command()
def set_integer(propertyId: int, value: int, areaId: float):
    adb_command = f"dumpsys android.hardware.automotive.vehicle.IVehicle/default --set {propertyId} -i {value} -a {areaId}\n"
    try:
        process.stdin.write(adb_command)
        process.stdin.flush()
    except ValueError:
        typer.echo("Error: Unable to write to process")


# 전체 list에서 id에 해당하는 vhal의 area값을 가져오는 함수
def match_value_type(propertyId, value, areaId):
    vehicle_prop_value_list = Vehiclepropvaluelist(propertyId)
    #result = get(propertyId)
    #lines = result.stdout.split('\n')[:-3]

    lines = get(propertyId).stdout.split('\n')[:-3]
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


@app.command()
def get(property_id: int):
    adb_command = f"dumpsys android.hardware.automotive.vehicle.IVehicle/default --get {property_id}"
    try:
        process.stdin.write(adb_command)
        output = process.communicate()
        typer.echo(output)
    except ValueError:
        typer.echo("Error : Can't fine Property Id ")


@app.command()
def list():
    adb_command = "dumpsys android.hardware.automotive.vehicle.IVehicle/default --list"
    try:
        process.stdin.write(adb_command)
        process.stout()
        process.stdin.flush()

    except ValueError:
        typer.echo("Error : Can't fine Property Id List ")


app.add_typer(connection_instance.app, name="connection")



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


def main():
    print("Hello")


if __name__ == "__main__":
    app()
