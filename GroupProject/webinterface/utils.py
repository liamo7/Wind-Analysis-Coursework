from base64 import b64encode, b64decode
from json import JSONEncoder
from pandas import read_csv
import pickle



# Code taken from user 'simlmx' from stackOverflow.com
# Link: http://stackoverflow.com/questions/8230315/python-sets-are-not-json-serializable
#
# Converts complex objects, and lists/dicts to json to solve problems with type errors

class PythonObjectEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (list, dict, str, int, float, bool, type(None))):
            return super().default(obj)
        return {'_python_object': b64encode(pickle.dumps(obj)).decode('utf-8')}

def as_python_object(dct):
    if '_python_object' in dct:
        return pickle.loads(b64decode(dct['_python_object'].encode('utf-8')))


def convertToSiteCalibrationDict(path):
    parse = read_csv(path, sep='\t')
    valueDict = parse.to_dict()

    degree = list(valueDict['degree'].values())
    offset = list(valueDict['offset'].values())
    slope = list(valueDict['slope'].values())
    siteCalDict = {}

    for ss, elem in enumerate(degree):
        siteCalDict[str(elem)] = {}
        siteCalDict[str(elem)]['slope'] = slope[ss]
        siteCalDict[str(elem)]['offset'] = offset[ss]


    return siteCalDict
