import subprocess

from Window.Vhal_CLI_API.model.vehiclePropValue.VehiclePropValueList import Vehiclepropvaluelist


# list 함수
def get_vhal_list():
    return "adb shell dumpsys android.hardware.automotive.vehicle.IVehicle/default --list"


def get_user_vhal_list():
    print("Fetching VHAL list...")
    vehicle_list = Vehiclepropvaluelist()
