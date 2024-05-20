# VehiclePropValueModel.py
class VehiclePropValueModel:
    def __init__(self, VehiclePropValueList=None):
        self.VehiclePropValueList = VehiclePropValueList if VehiclePropValueList is not None else []

    def addVehiclePropValue(self, vehicle):
        self.VehiclePropValueList.append(vehicle)

    def __str__(self):
        result = ""
        for i, vehicle in enumerate(self.VehiclePropValueList):
            result += f"Vehicle {i+1}:\n{vehicle}\n"
        return result
    
    def getVehiclePropValueId(self, prop_id):
        matching_vehicles = [vehicle for vehicle in self.VehiclePropValueList if vehicle.prop == prop_id]
        return matching_vehicles
    
    def listAllVehiclePropValueList(self):
        return self.VehiclePropValueList
    
    def setVehiclePropValue(self, prop_id, new_value):
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