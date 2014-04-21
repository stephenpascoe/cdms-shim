"""
The Cdunif interface translated into Python

"""

from abc import ABCMeta, abstractmethod, abstractproperty

class AbstractCdunifFile(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, filename, mode, history=None):
        if history is not None:
            raise NotImplementedError('cdunif-shim does not support adding history on file creation')

    @abstractproperty
    def dimensions(self):
        raise NotImplementedError

    @abstractproperty
    def variables(self):
        raise NotImplementedError

    @abstractproperty
    def dimensioninfo(self):
        raise NotImplementedError

    #!FIXME: How to emulate attributes in __dict__

    @abstractmethod
    def __getattr__(self, attr):
        raise NotImplementedError

    @abstractmethod
    def __setattr__(self, attr, value):
        raise NotImplementedError

    @abstractmethod
    def close(self):
        raise NotImplementedError

    @abstractmethod
    def createDimension(self, name, length):
        raise NotImplementedError

    @abstractmethod
    def createVariable(self, name, typecode, dimensions):
        raise NotImplementedError

    @abstractmethod
    def readDimension(self, name):
        raise NotImplementedError

    @abstractmethod
    def sync(self):
        raise NotImplementedError

    def flush(self):
        return self.sync()


class AbstractCdunifVariable(object):

    @abstractproperty
    def shape(self):
        raise NotImplementedError

    @abstractproperty
    def dimensions(self):
        raise NotImplementedError

    #!FIXME: how to emulate attributes in __dict__

    @abstractmethod
    def __getattr__(self, attr):
        raise NotImplementedError

    @abstractmethod
    def __setattr__(self, attr, value):
        raise NotImplementedError

    @abstractmethod
    def __len__(self):
        raise NotImplementedError

    @abstractmethod
    def __getitem__(self, key):
        raise NotImplementedError

    @abstractmethod
    def __setitem__(self, key, value):
        raise NotImplementedError


#def CdunifSetNCFLAGS():
#    pass
#
#def CdunifGetNCFLAGS():
#    pass

