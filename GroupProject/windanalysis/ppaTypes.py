from enum import Enum

class FileType(Enum):
    METEO = 1
    POWER = 2
    LIDAR = 3
    COMBINED = 4

class ColumnType(Enum):
    TIMESTAMP = 1
    WIND_SPEED = 2
    WIND_DIRECTION = 3
    TEMPERATURE = 4
    RELATIVE_HUMIDITY = 5
    PRESSURE = 6
    RAINFALL = 7
    POWER = 8
    MINUTE_COUNT = 9
    TURBULENCE_INTENSITY = 10
    WIND_SHEAR_EXPONENT = 11
    AIR_DENSITY = 12
    DERIVED = 13
    AVAILABILITY = 14

class ValueType(Enum):
    TIMESTAMP = 1
    QUANTITY = 2
    MEAN = 3
    STANDARD_DEVIATION = 4
    SUM = 5
    DERIVED = 6
    PERCENT = 7

class FilterType(Enum):
    INCLUDE_DATA = 1
    EXCLUDE_TIMESTAMP = 2

class BinStatus(Enum):
    MEASURED = 1
    INTERPOLATED = 2
    EXCLUDED = 3
    PADDED = 4
    WARRANTED = 5

class REWSMeasurementType(Enum):
    REMOTE_SENSING_DEVICE = 1
    MAST_ABOVE_HUB_HEIGHT = 2