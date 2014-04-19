"""
The Cdunif interface translated into Python

"""

class CdunifFile(object):

    def __init__(self, filename, node, history=None):
        if history is not None:
            raise NotImplementedError('cdunif-shim does not support adding history on file creation')

    @property
    def attributes(self):
        raise NotImplementedError

    @property
    def variables(self):
        raise NotImplementedError

    @property
    def dimensioninfo(self):
        raise NotImplementedError

    #!FIXME: How to emulate attributes in __dict__

    def __getattr__(self, attr):
        raise NotImplementedError

    def __setattr__(self, attr, value):
        raise NotImplementedError

    def __repr__(self):
        raise NotImplementedError

    def close(self):
        raise NotImplementedError

    def createDimension(self, name, length):
        raise NotImplementedError

    def createVariable(self, name, typecode, dimensions):
        raise NotImplementedError

    def readDimension(self, name):
        raise NotImplementedError

    def sync(self):
        raise NotImplementedError

    def flush(self):
        return self.sync()


class CdunifVariable(object):

    @property
    def shape(self):
        raise NotImplementedError

    @property
    def dimensions(self):
        raise NotImplementedError

    #!FIXME: how to emulate attributes in __dict__

    def __getattr__(self, attr):
        raise NotImplementedError

    def __setattr__(self, attr, value):
        raise NotImplementedError

    def __len__(self):
        raise NotImplementedError

    def __getitem__(self, key):
        raise NotImplementedError

    def __setitem__(self, key, value):
        raise NotImplementedError


def CdunifSetNCFLAGS():
    pass

def CdunifGetNCFLAGS():
    pass

