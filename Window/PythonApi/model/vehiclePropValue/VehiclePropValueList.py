# VehiclePropValueList.py

import sys
sys.path.append(r'D:\00.Project\SDV\SDVPRJ\-SDV\PythonAdb\model\vehiclePropValue')



class VehiclePropValueList:
    def __init__(self, propertiesId, vehiclePropValues=None):
        self.vehiclePropValues = vehiclePropValues if vehiclePropValues is not None else []
        self.propertiesId = propertiesId

    def __str__(self):
        valuesStr = ', '.join(str(value) for value in self.vehiclePropValues)
        return f"VehiclePropValueList({valuesStr}), propertiesId: {self.propertiesId}"

    def add(self, vehiclePropValue):
        self.vehiclePropValues.append(vehiclePropValue)

    def remove(self, vehiclePropValue):
        if vehiclePropValue in self.vehiclePropValues:
            self.vehiclePropValues.remove(vehiclePropValue)
        else:
            print("VehiclePropValue not found in the list.")
    
    def getVehiclePropValue(self, areaId):
        for vehiclePropValue in self.vehiclePropValues:
            if vehiclePropValue.getAreaId() == areaId:
                return vehiclePropValue
        print("Can't find VehiclePropValue to Id")
        return None

    def getVehiclePropValues(self):
        return self.vehiclePropValues

    def getPropertiesId(self):
        return self.propertiesId
    