class VehiclePropValue:
    def __init__(self, timestamp, areaId, prop, status, dataType=None, int32Values=None, floatValues=None, int64Values=None, byteValues=None, stringValues=None):
        self.timestamp = timestamp
        self.areaId = areaId
        self.prop = prop
        self.status = status
        self.dataType = dataType
        self.int32Values = int32Values if int32Values is not None else []
        self.floatValues = floatValues if floatValues is not None else []
        self.int64Values = int64Values if int64Values is not None else []
        self.byteValues = byteValues if byteValues is not None else []
        self.stringValues = stringValues if stringValues is not None else []

    def __str__(self):
        return f"VehiclePropValue(timestamp: {self.timestamp}, areaId: {self.areaId}, prop: {self.prop}, status: {self.status}, dataType: {self.dataType}, int32Values: {self.int32Values}, floatValues: {self.floatValues}, int64Values: {self.int64Values}, byteValues: {self.byteValues}, stringValues: {self.stringValues})"
    
    def setDataType(self, int32Values=None, floatValues=None, int64Values=None, byteValues=None, stringValues=None):
        if self.int32Values :
            self.dataType = type(int32Values)
        elif self.floatValues :
            self.dataType = type(floatValues)
        elif self.int64Values :
            self.dataType = type(int64Values)
        elif self.byteValues :
            self.dataType = type(byteValues)
        else :
            self.dataType = type(stringValues)

    def getDataType(self):
        return self.dataType

    
    def setTimestamp(self, timestamp):
        self.timestamp = timestamp

    def getTimeStamp(self):
        return self.timestamp
    
    def setAreaId(self, areaId):
        self.areaId = areaId

    def getAreaId(self):
        return self.areaId
    
    def setProp(self, prop):
        self.prop = prop
    
    def getProp(self):
        return self.prop
    
    def setStatus(self, status):
        self.status = status

    def getStatus(self):
        return self.status

    def getInt32Values(self):
        return self.int32Values

    def setInt32Values(self, values):
        self.int32Values = values

    def getFloatValues(self):
        return self.floatValues

    def setFloatValues(self, values):
        self.floatValues = values

    def getInt64Values(self):
        return self.int64Values

    def setInt64Values(self, values):
        self.int64Values = values

    def getByteValues(self):
        return self.byteValues

    def setByteValues(self, values):
        self.byteValues = values

    def getStringValues(self):
        return self.stringValues

    def setStringValues(self, values):
        self.stringValues = values