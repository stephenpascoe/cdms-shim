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
        """
        A dictionary {'dimname': (units, typecode, name, ?, dimtype, order), ...}

        dimtype is always 'global' for NetCDF-classic.
        units and typecode are detected from any variable of the same name.
        ? appears to be ''

        """
        raise NotImplementedError

    # Replaces access to attributes via __dict__.  cdms2 needs to be patched to use this instead
    @abstractmethod
    def _attrs(self):
        """
        Return a dictionary of dataset attributes.

        """
        raise NotImplementedError

    @abstractmethod
    def _getattr(self, attr):
        raise NotImplementedError

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
        """
        Return the array representing dimension `name`.

        If a coordinate-array exists return that array, otherwise return
        the range of floats of the right length.

        """
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

    # Replaces access to attributes via __dict__.  cdms2 needs to be patched to use this instead
    @abstractmethod
    def _attrs(self):
        raise NotImplementedError

    @abstractmethod
    def _getattr(self, attr):
        raise NotImplementedError

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

    @abstractmethod
    def typecode(self):
        raise NotImplementedError

    @abstractmethod
    def assignValue(self, value):
        raise NotImplementedError

    @abstractmethod
    def getValue(self):
        raise NotImplementedError

    @abstractmethod
    def getitem(self, item):
        raise NotImplementedError

    @abstractmethod
    def getslice(self, item):
        raise NotImplementedError

    @abstractmethod
    def setitem(self, item, value):
        raise NotImplementedError

    @abstractmethod
    def setslice(self, low, high, value):
        raise NotImplementedError


#def CdunifSetNCFLAGS():
#    pass
#
#def CdunifGetNCFLAGS():
#    pass

