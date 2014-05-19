"""
Reimplementation of cdat's _regridmodule.c in Python

"""

import numpy as np

class error(Exception):
    pass

def gridattr(n, grid_type, blon=None, elon=None):
    """
    :param n: the number of latitude or longitude points
    :param grid_type: one of gassian, equalarea, uniform or longitude.  If longitude
       blon and elon are defined
    :param blon: first longitude
    :param elon: last longitude

    :returns: (pts, wts, bnds) arrays of points, weights and bounds
     
    """
    #!TODO: these could be shifted to the underlying functions
    pts = np.zeros(n, dtype=np.float)
    wts = np.zeros(n, dtype=np.float)
    bnds = np.zeros(n+1, dtype=np.float)

    if grid_type[:3] == 'gau':
        _gaussian_grid(n, pts, wts, bnds)
    elif grid_type[:3] == 'equ':
        _equalarea_grid(n, pts, wts, bnds)
    elif grid_type[:3] == 'uni':
        _uniform_latitude_grid(n, pts, wts, bnds)
    elif grid_type[:3] == 'lon':
        _uniform_longitude_grid(n, blon, elon, pts, wts, bnds)
    else:
        raise ValueError('Unknown grid type %s' % grid_type)

    return (pts, wts, bnds)

def pressattr(nlev, pts):
    """
    Get a pressure grid.

    :param nlev: number of levels
    :param pts: array with pressure values as doubles
    :return: (ts, bnds) arrays of weights and bounds

    """
    wts = np.zeros(nlev, dtype=np.float)
    bnds = np.zeros(nlev+1, dtype=np.float)

    _press_wts_bnds(nlev, pts, wts, bnds)

    return (wts, bnds)

def maparea(nloni, nlono, nlati, nlato, 
            bnin, bnout, bsin, bsout, 
            bein, beout, bwin, bwout):
    raise NotImplementedError

def rgdarea():
    raise NotImplementedError

def maplength():
    raise NotImplementedError

def rgdlength():
    raise NotImplementedError

def rgdpressure():
    raise NotImplementedError
