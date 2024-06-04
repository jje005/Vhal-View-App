import logging
import os
import subprocess
import sys
from typing import Optional

import typer

#CLI 라이브러리
app = typer.Typer()
connection_app = typer.Typer()
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from VehiclePropValue import VehiclePropValue
from VehiclePropValueList import Vehiclepropvaluelist

#sys.path.append("D:/00.Project/SDV/Vhal-View-App/Window/Vhal_CLI_API/network")
from ConnectionManager import connection_instance

process = subprocess.Popen(['adb', 'shell'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                           text=True)
logging.basicConfig(
    format='%(asctime)s.%(msecs)03d - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.DEBUG,
    handlers=[logging.StreamHandler(sys.stdout)]
)


@app.command()
def set(property_id, value, area_id):
    global output

    adb_command = f"dumpsys android.hardware.automotive.vehicle.IVehicle/default --set {property_id} "
    adb_command += match_value_type(property_id, value, area_id)
    print(adb_command)
    try:
        process.stdin.write(adb_command)
        process.stdin.flush()
    except ValueError:
        typer.echo("Error: Unable to write to process!!!!")


@app.command()
def set_float(property_id: int, value, area_id):
    adb_command = f"dumpsys android.hardware.automotive.vehicle.IVehicle/default --set {property_id} -f {value} -a {area_id}\n"
    try:
        process.stdin.write(adb_command)
        process.stdin.flush()
    except ValueError:
        typer.echo("Error: Unable to write to process")


@app.command()
def set_integer(property_id, value: int, area_id: int):
    adb_command = f"dumpsys android.hardware.automotive.vehicle.IVehicle/default --set {property_id} -i {value} -a {area_id}"
    try:
        process.stdin.write(adb_command)
        process.stdin.flush()
    except ValueError:
        typer.echo("Error: Unable to write to process")


# 전체 list에서 id에 해당하는 vhal의 area값을 가져오는 함수
def match_value_type(property_id, value, area_id):
    vehicle_prop_value_list = Vehiclepropvaluelist(property_id)
    command = f"adb shell dumpsys android.hardware.automotive.vehicle.IVehicle/default --get {property_id}"
    result = subprocess.run(command, shell=True, text=True, capture_output=True)
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

    entry = vehicle_prop_value_list.getVehiclePropValue(area_id)
    return check_value_type(entry.getDataType(), value) + check_value_area(area_id)


def check_value_type(value_type, value):
    return set_value_type(value_type) + value + " "


@app.command()
def get(property_id: int):
    get_vhal(property_id)


def get_vhal(property_id):
    global output
    adb_command = f"dumpsys android.hardware.automotive.vehicle.IVehicle/default --get {property_id}\n"
    try:
        process.stdin.write(adb_command)
        process.stdin.flush()
        output, error = process.communicate(timeout=5)
        if output:
            typer.echo(output)
        if error:
            typer.echo(f"Error: {error}")
    except ValueError:
        typer.echo("Error : Can't find Property Id")
    except subprocess.TimeoutExpired:
        typer.echo("Error: Command timed out")
    return output


@app.command()
def list():
    adb_command = "dumpsys android.hardware.automotive.vehicle.IVehicle/default --list\n"
    try:
        process.stdin.write(adb_command)
        process.stdin.flush()
        output, error = process.communicate(timeout=5)
        if output:
            typer.echo(output)
        if error:
            typer.echo(f"Error: {error}")
    except ValueError:
        typer.echo("Error : Can't find Property Id List")
    except subprocess.TimeoutExpired:
        typer.echo("Error: Command timed out")

@app.command()
def get_connection(connection_type:str):
    messages = None
    messages = connection_instance.get_connection(connection_type)
    if messages is None:
        return typer.echo("Error: Connection Setting Error")
    return typer.echo(messages)


@app.command()
def set_connection(connection_type: str, address, port):
    connection_instance.set_connection(connection_type, address, port)

@app.command()
def connection(connection_type: str):
    if connection_type == "l" or connection_type == "local" or connection_type == "r" or connection_type == "remote":
        connection_instance.connection(connection_type)
    else:
        typer.echo("Error : Connection Type error ")


@app.command()
def change():
    connection_instance.change()


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
    return f"-a {area_id}"


def parsing_vhal(data_dict):
    timestamp = data_dict.get("timestamp", None)
    area_id = data_dict.get("areaId", None)
    prop = data_dict.get("prop", None)
    status = data_dict.get("status", None)

    data_type = ""
    int32_values = data_dict.get("int32Values", [])

    if int32_values == "[]":
        int32_values = None
    else:
        data_type = "int32"
    float_values = data_dict.get("floatValues", [])
    if float_values == "[]":
        float_values = None
    else:
        data_type = "float"

    int64_values = data_dict.get("int64Values", [])
    if int64_values == "[]":
        int64_values = None
    else:
        data_type = "int64"

    byte_values = data_dict.get("byteValues", [])
    if byte_values == "[]":
        byte_values = None
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


if __name__ == "__main__":
    app()
