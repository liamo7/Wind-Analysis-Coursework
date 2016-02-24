from GroupProject import settings
import pandas as pd
import os


def printAllFilesInDirectory():
    for r, d, f in os.walk(settings.BASE_DIR):
        for file in f:
            print(os.path.join(settings.BASE_DIR, file))


def readFromCsv(pathToFile):

    path = settings.MEDIA_ROOT + '\Project4\sitecalibration\dummy.txt'

    if os.path.exists(path):
        print(path)
    else:
        print('File path does not exist')

    df = pd.read_csv(path, sep='\t')
    return df
