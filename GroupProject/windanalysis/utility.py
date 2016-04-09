__author__ = 'Brian'
from webinterface.models import Datafile
from .ppaTypes import *
import pandas as pd
import os

# TODO: Move this to data.py, add datafile sources and rename function to 'recreate file from source' or similar
def synchroniseDataFiles(newFilePath, containingDirectory, dataFiles):

    if not os.path.exists(containingDirectory):
        os.makedirs(containingDirectory)

    synchronisedFile = Datafile('combined.txt', containingDirectory, FileType.COMBINED)

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


