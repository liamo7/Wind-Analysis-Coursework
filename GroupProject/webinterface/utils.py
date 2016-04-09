from base64 import b64encode, b64decode
from json import dumps, loads, JSONEncoder
import pickle



# Code takn from user 'simlmx' from stackOverflow.com
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
