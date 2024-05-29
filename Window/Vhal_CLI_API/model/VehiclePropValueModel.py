# VehiclePropValueModel.py
class VehiclePropValueModel:
    def __init__(self, vehicle_prop_value_list=None):
        self.VehiclePropValueList = vehicle_prop_value_list if vehicle_prop_value_list is not None else []

    def add_vehicle_prop_value(self, vehicle):
        self.VehiclePropValueList.append(vehicle)

    def __str__(self):
        result = ""
        for i, vehicle in enumerate(self.VehiclePropValueList):
            result += f"Vehicle {i + 1}:\n{vehicle}\n"
        return result

    def get_vehicle_prop_value_id(self, prop_id):
        matching_vehicles = [vehicle for vehicle in self.VehiclePropValueList if vehicle.prop == prop_id]
        return matching_vehicles

    def list_all_vehicle_prop_value_list(self):
        return self.VehiclePropValueList

    def set_vehicle_prop_value(self, prop_id, new_value):
        for vehicle in self.VehiclePropValueList:
            if vehicle.prop == prop_id:
                if type(new_value) != type(vehicle.string_value):
                    print("Error: New value type cannot be different from the existing type.")
                    return False
                else:
                    vehicle.string_value = new_value
                    print(f"Property value of prop {prop_id} updated successfully.")
                    return True
        print(f"Error: No vehicle found with prop id {prop_id}.")
        return False
