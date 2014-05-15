"""
Implementation of Cdunif on top of netCDF4-python

"""

import numpy as np

import netCDF4 as NC

from Cdunif_abc import AbstractCdunifFile, AbstractCdunifVariable

class CdunifError(Exception):
    pass


def _remove_unicode(x):
    if type(x) == unicode:
        return x.encode('utf-8')
    else:
        return x

class CdunifFile(AbstractCdunifFile):
    def __init__(self, filename, mode, history=None):
        if history is not None:            raise NotImplementedError('cdms-shim does not support adding history on file creation')
        #!TODO: check mode translation

        self.__dict__['_obj'] = NC.Dataset(filename, mode)

    @property
    def variables(self):
        return {_remove_unicode(k): CdunifVariable(v) for k, v in self._obj.variables.items()}

    @property
    def dimensions(self):
        #!NOTE: should return None if unlimited and not 0
        def dim_len(dim):
            if dim.isunlimited():
                if len(dim) == 0:
                    return 0
                else:
                    return None
            else:
                return len(dim)

        return {_remove_unicode(k): dim_len(v) for k, v in self._obj.dimensions.items()}

    @property
    def dimensioninfo(self):
        """
        A dictionary {'dimname': (units, typecode, name, varname, dimtype, order), ...}

        dimtype is always 'global' for NetCDF-classic.
        units and typecode are detected from any variable of the same name.
        varname appears to be '' for NetCDF-classic

        """


        ret = {}
        for i, dimname in enumerate(self._obj.dimensions):
            try:
                var = self.variables[dimname]
            except KeyError:
                units = ''
                typecode = ''
            else:
                try:
                    units = var._obj.getncattr('units')
                except AttributeError:
                    units = ''
                typecode = var._obj.dtype.char
                
            ret[_remove_unicode(dimname)] = (units, typecode, _remove_unicode(dimname), 
                                             '', 'global', i)
                                             
        return ret


    def __getattr__(self, attr):
        return _remove_unicode(self._obj.getncattr(attr))
                                             
    def __setattr__(self, attr, value):
        #!TODO: Should we convert to unicode?
        return self._obj.setncattr(attr, value)

    # Replaces access to attributes via __dict__.  cdms2 needs to be patched to use this instead
    def _attrs(self):
        return [_remove_unicode(v) for v in self._obj.ncattrs()]

    def _getattr(self, attr):
        return _remove_unicode(self._obj.getncattr(attr))

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
        try:
            dimvar = self._obj.variables[name]
            return dimvar[:]
        except KeyError:
            try: 
                dim = self._obj.dimensions[name]
            except KeyError:
                raise TypeError('Dimension not found')
            else:
                return np.arange(len(dim), dtype=np.float32)


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
        return self._obj.dimensions

    # Replaces access to attributes via __dict__.  cdms2 needs to be patched to use this instead
    def _attrs(self):
        return [_remove_unicode(v) for v in (self._obj.ncattrs())]

    def _getattr(self, attr):
        return _remove_unicode(self._obj.getncattr(attr))

    def __getattr__(self, attr):
        return _remove_unicode(self._obj.getncattr(attr))

    def __setattr__(self, attr, value):
        return self._obj.setncattr(attr, value)

    def __len__(self):
        return len(self._obj)

    def __getitem__(self, key):
        return self._obj.__getitem__(key)

    def __setitem__(self, key, value):
        return self._obj.__setitem__(key, value)

    def typecode(self):
        return self._obj.dtype.char

    def assignValue(self, value):
        self._obj[:] = value

    def getValue(self):
        return self._obj[:]

    def getitem(self, item):
        return self._obj[item]

    def getslice(self, low, high):
        return self._obj[low:high]

    def setitem(self, item, value):
        self._obj[item] = value

    def setslice(self, low, high, value):
        self._obj[low:high] = value



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

def CdunifGetNCFLAGS(flagname):
    if flagname not in _ncflags:
        raise ValueError('Unrecognised NetCDF flag %s' % flagname)

    return _ncflags[flagname]
    
