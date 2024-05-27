# get 함수
def get_vhal(property_id):
    return f"adb shell dumpsys android.hardware.automotive.vehicle.IVehicle/default --get {property_id}"
