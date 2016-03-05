__author__ = 'Brian'
from test_wind.data import Datafile
from test_wind.ppaTypes import *
import pandas as pd

# TODO: Move this to data.py, add datafile sources and rename function to 'recreate file from source' or similar
def synchroniseDataFiles(filename, newFilePath, dataFiles):
    synchronisedFile = Datafile(name=filename, containingDirectory=newFilePath, fileType=FileType.COMBINED)

    columnNumber = 1
    for f in dataFiles:
        synchronisedFile.columns.extend(f.columns)
        synchronisedFile.columnSets.update(f.columnSets)
        for columnName in f.data.columns:
            for columnRecord in synchronisedFile.columns:
                if columnRecord.name == columnName:
                    columnRecord.positionInFile = columnNumber
                    columnNumber += 1
                    break

    synchronisedFile.data = pd.concat([dataFile.data for dataFile in dataFiles], join='inner', axis=1)

    return synchronisedFile


