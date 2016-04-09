def getWindTestData():

    data = {
        'col1': {
            'name': 'Mast - 82m Wind Direction Mean',
            'positionInFile': 1,
            'columnType': 3,
            'valueType': 3,
            'measurementHeight': 82,
            'instrumentCalibrationSlope': 0.04577,
            'instrumentCalibrationOffset': 0.2653
        },

        'col2': {
            'name': 'Mast - 80m Wind Speed Mean',
            'positionInFile': 2,
            'columnType': 2,
            'valueType': 3,
            'measurementHeight': 80,
            'instrumentCalibrationSlope': 0.04581,
            'instrumentCalibrationOffset': 0.2638
        },

        'col3': {
            'name': 'Mast - 80m Wind Speed Std Dev',
            'positionInFile': 3,
            'columnType': 2,
            'valueType': 4,
            'measurementHeight': 80,
            'instrumentCalibrationSlope': 0.04577,
            'instrumentCalibrationOffset': 0.2688
        },

        'col4': {
            'name': 'Mast - 64m Wind Speed Mean',
            'positionInFile': 4,
            'columnType': 2,
            'valueType': 3,
            'measurementHeight': 64,
            'instrumentCalibrationSlope': 0.04583,
            'instrumentCalibrationOffset': 0.2621
        },

        'col5': {
            'name': 'Mast - 35.0m Wind Speed Mean',
            'positionInFile': 5,
            'columnType': 2,
            'valueType': 3,
            'measurementHeight': 35,
            'instrumentCalibrationSlope': 0.04581,
            'dataLoggerCalibrationSlope': 0.0462
        },

        'col6': {
            'name': 'Pressure (mBar)',
            'positionInFile': 6,
            'columnType': 6,
            'valueType': 3,
            'measurementHeight': 30
        },

        'col7': {
            'name': 'Relative humidity (%)',
            'positionInFile': 7,
            'columnType': 5,
            'valueType': 3,
            'measurementHeight': 30
        },

        'col8': {
            'name': 'Temperature (C)',
            'positionInFile': 8,
            'columnType': 4,
            'valueType': 3,
            'measurementHeight': 30
        },

        'colSets': {
            'label': 'anemometers',
            'columnSet': ['Mast - 80m Wind Speed Mean', 'Mast - 64m Wind Speed Mean', 'Mast - 35.0m Wind Speed Mean']
        }
    }

    return data


def getPowerTestData():

    data = {
        'col1': {
            'name': 'Power mean (kW)',
            'positionInFile': 1,
            'columnType': 8,
            'valueType': 3
        }
    }

    return data


def getLidarTestData():

    data = {

        'col1': {
            'name': 'LiDAR - 132.5m Wind Speed Mean',
            'positionInFile': 1,
            'columnType': 2,
            'valueType': 3,
            'measurementHeight': 132.5
        },

        'col2': {
            'name': 'LiDAR - 127.5m Wind Speed Mean',
            'positionInFile': 2,
            'columnType': 2,
            'valueType': 3,
            'measurementHeight': 127.5
        },

        'col3': {
            'name': 'LiDAR - 117.5m Wind Speed Mean',
            'positionInFile': 3,
            'columnType': 2,
            'valueType': 3,
            'measurementHeight': 117.5
        },

        'col4': {
            'name': 'LiDAR - 107.5m Wind Speed Mean',
            'positionInFile': 4,
            'columnType': 2,
            'valueType': 3,
            'measurementHeight': 107.5
        },

        'col5': {
            'name': 'LiDAR - 97.5m Wind Speed Mean',
            'positionInFile': 5,
            'columnType': 2,
            'valueType': 3,
            'measurementHeight': 97.5
        },

        'col6': {
            'name': 'LiDAR - 87.5m Wind Speed Mean',
            'positionInFile': 6,
            'columnType': 2,
            'valueType': 3,
            'measurementHeight': 87.5
        },

        'col7': {
            'name': 'LiDAR - 77.5m Wind Speed Mean',
            'positionInFile': 7,
            'columnType': 2,
            'valueType': 3,
            'measurementHeight': 77.5
        },

        'col8': {
            'name': 'LiDAR - 67.5m Wind Speed Mean',
            'positionInFile': 8,
            'columnType': 2,
            'valueType': 3,
            'measurementHeight': 67.5
        },

        'col8': {
            'name': 'LiDAR - 57.5m Wind Speed Mean',
            'positionInFile': 9,
            'columnType': 2,
            'valueType': 3,
            'measurementHeight': 57.5
        },

        'col8': {
            'name': 'LiDAR - 42.5m Wind Speed Mean',
            'positionInFile': 10,
            'columnType': 2,
            'valueType': 3,
            'measurementHeight': 42.5
        }
    }

    return data

from windAnalysis.ppaTypes import *
def getEnum():

    data = getWindTestData()
    print(data)

    for key, val in data.items():
        print(val['columnType'])



    print(ColumnType(data['col1']['columnType']))
    print(data['col1']['columnType'])


