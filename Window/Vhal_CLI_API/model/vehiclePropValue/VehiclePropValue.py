class VehiclePropValue:
    def __init__(self, timestamp, area_id, prop, status, data_type=None, int32_values=None, float_values=None, int64_values=None, byte_values=None, string_values=None):
        self.timestamp = timestamp
        self.areaId = area_id
        self.prop = prop
        self.status = status
        self.dataType = data_type
        self.int32Values = int32_values if int32_values is not None else []
        self.floatValues = float_values if float_values is not None else []
        self.int64Values = int64_values if int64_values is not None else []
        self.byteValues = byte_values if byte_values is not None else []
        self.stringValues = string_values if string_values is not None else []

    def __str__(self):
        return f"VehiclePropValue(timestamp: {self.timestamp}, areaId: {self.areaId}, prop: {self.prop}, status: {self.status}, dataType: {self.dataType}, int32Values: {self.int32Values}, floatValues: {self.floatValues}, int64Values: {self.int64Values}, byteValues: {self.byteValues}, stringValues: {self.stringValues})"
    
    def set_data_type(self, int32_values=None, float_values=None, int64_values=None, byte_values=None, string_values=None):
        if self.int32Values :
            self.dataType = type(int32_values)
        elif self.floatValues :
            self.dataType = type(float_values)
        elif self.int64Values :
            self.dataType = type(int64_values)
        elif self.byteValues :
            self.dataType = type(byte_values)
        else :
            self.dataType = type(string_values)

    def getDataType(self):
        return self.dataType

    
    def set_timestamp(self, timestamp):
        self.timestamp = timestamp

    def get_time_stamp(self):
        return self.timestamp
    
    def set_area_id(self, areaId):
        self.areaId = areaId

    def getAreaId(self):
        return self.areaId
    
    def set_prop(self, prop):
        self.prop = prop
    
    def get_prop(self):
        return self.prop
    
    def set_status(self, status):
        self.status = status

    def get_status(self):
        return self.status

    def get_int32_values(self):
        return self.int32Values

    def set_int32_values(self, values):
        self.int32Values = values

    def get_float_values(self):
        return self.floatValues

    def set_float_values(self, values):
        self.floatValues = values

    def get_int64_values(self):
        return self.int64Values

    def set_int64_values(self, values):
        self.int64Values = values

    def get_byte_values(self):
        return self.byteValues

    def set_byte_values(self, values):
        self.byteValues = values

    def get_string_values(self):
        return self.stringValues

    def set_string_values(self, values):
        self.stringValues = values