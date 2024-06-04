class Vehiclepropvaluelist:
    def __init__(self, properties_id, vehicle_prop_values=None):
        self.vehiclePropValues = vehicle_prop_values if vehicle_prop_values is not None else []
        self.propertiesId = properties_id

    def __str__(self):
        values_str = ', '.join(str(value) for value in self.vehiclePropValues)
        return f"VehiclePropValueList({values_str}), propertiesId: {self.propertiesId}"

    def add(self, vehicle_prop_value):
        self.vehiclePropValues.append(vehicle_prop_value)

    def remove(self, vehicle_prop_value):
        if vehicle_prop_value in self.vehiclePropValues:
            self.vehiclePropValues.remove(vehicle_prop_value)
        else:
            print("VehiclePropValue not found in the list.")

    def getVehiclePropValue(self, area_id):
        for vehiclePropValue in self.vehiclePropValues:
            if vehiclePropValue.getAreaId() == area_id:
                return vehiclePropValue
        print("Can't find VehiclePropValue to Id")
        return None

    def get_vehicle_prop_values(self):
        return self.vehiclePropValues

    def get_properties_id(self):
        return self.propertiesId
