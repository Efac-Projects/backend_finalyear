import json
from json import JSONEncoder
import numpy 

class NumpyArrayEncorder(JSONEncorder):
    def default(self, obj):
        if isinstance(obj,numpy.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)