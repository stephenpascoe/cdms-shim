"""
Implementation of Cdunif on top of netCDF4-python

"""

import netCDF4 as NC

from Cdunif_abc import AbstractCdunifFile, AbstractCdunifVariable

class CdunifError(Exception):
    pass

class CdunifFile(AbstractCdunifFile):
    def __init__(self, filename, mode, history=None):
        if history is not None:            raise NotImplementedError('cdms-shim does not support adding history on file creation')
        #!TODO: check mode translation

        self.__dict__['_obj'] = NC.Dataset(filename, mode)

    @property
    def variables(self):
        return {k: CdunifVariable(v) for k, v in self._obj.variables.items()}

    @property
    def dimensions(self):
        return {k: len(v) for k, v in self._obj.dimensions.items()}

    @property
    def dimensioninfo(self):
        raise NotImplementedError

    def __getattr__(self, attr):
        return self._obj.getncattr(attr)

    def __setattr__(self, attr, value):
        return self._obj.setncattr(attr, value)

    def close(self):
        self._obj.close()

    def createDimension(self, name, length):
        return self._obj.createDimension(name, length)

    def createVariable(self, name, typecode, dimensions):
        if _ncflags['shuffle'] == 1:
            shuffle = True
        else:
            shuffle = False

        if _ncflags['deflate'] == 1:
            zlib = True
        else:
            zlib = False

        complevel = _ncflags['deflate_level']

        return CdunifVariable(self._obj.createVariable(name, typecode, dimensions,
                                                       shuffle=shuffle,
                                                       zlib=zlib, complevel=complevel))

    def readDimension(self, name):
        return len(self._obj.dimensions[name])

    def sync(self):
        return self._obj.sync()
        

class CdunifVariable(AbstractCdunifVariable):

    def __init__(self, variable):
        self.__dict__['_obj'] = variable

    @property
    def shape(self):
        return self._obj.shape

    @property
    def dimensions(self):
        return {k: len(v) for k, v in self._obj.dimensions.items()}

    #!FIXME: how to emulate attributes in __dict__

    def __getattr__(self, attr):
        return self._obj.getncattr(attr)

    def __setattr__(self, attr, value):
        return self._obj.setncattr(attr, value)

    def __len__(self):
        return len(self._obj)

    def __getitem__(self, key):
        return self._obj.__getitem__(key)

    def __setitem__(self, key, value):
        return self._obj.__setitem__(key, value)


_ncflags = {
    'shuffle': 1,       # shuffle
    'deflate': 0,       # zlib
    'deflate_level': 0, # complevel
}

def CdunifSetNCFLAGS(flagname, flagval):
    if flagname == 'shuffle':
        if flagval not in [0, 1]:
            raise ValueError('shuffle flag must be 0 or 1')
    elif flagname == 'deflate':
        if flagval not in [0, 1]:
            raise ValueError('deflate flag must be 0 or 1')
    elif flagname == 'deflate_level':
        if flagval > 10:
            raise ValueError('deflate_level flag must be <= 10')
    else:
        raise ValueError('Unrecognised NetCDF flag %s' % flagname)

    _ncflags[flagname] = flagval

def CdunifGetNCFLAGS(flagname, flagval):
    if flagname not in _ncflags:
        raise ValueError('Unrecognised NetCDF flag %s' % flagname)

    return _ncflags[flagname]
    
