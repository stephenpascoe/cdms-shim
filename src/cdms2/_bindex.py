"""

bindex interface.

"""

import numpy as np

NBINI = 720
NBINJ = 360
BINLEN = NBINI*NBINJ
XBINI = (360.0/float(NBINI))
XBINJ = (180.0/float(NBINJ))

def bindex(lats, lons):
    """
    Creates an index consisting of 2 arrays as described below.

    :param lats: The 1D ravelled array of latitudes of a grid
    :param lons: The 1D ravelled array of latitudes of a grid
    :return: `(head, next)` where `head` is an array of shape (720 * 360, ) containing 
        the indexes into `lats` or `lons` for each point on a 720x360 grid.  `next` is
        an array of shape (720 * 360, ) containing indexes of `head` for the next grid point

    """
def bindexHorizontalGrid(lats, lons):
    assert len(lats.shape) == 1
    n = lats.shape[0]

    i = np.floor(lons/XBINI).astype(np.int) % NBINI
    i = np.where(i < 0, i + NBINI, i)

    j = np.floor((lats + 90.0) / XBINJ).astype(np.int)
    mj = np.where(j > 0, j, 0)
    j = np.where(mj > NBINJ - 1, NBINJ - 1, mj)

    oind = NBINJ*i + j

    head = np.ones(BINLEN, np.int) * -1
    last = np.ones(BINLEN, np.int) * -1
    next = np.ones(n, np.int) * -1

    #!FIXME: this is slow but making it faster would probably require Cython 
    #        or the original bindex code
    for ireg in xrange(n):
        oind_i = oind[ireg]
        if head[oind_i] == -1:
            head[oind_i] = last[oind_i] = ireg
        else:
            next[last[oind_i]] = ireg
            last[oind_i] = ireg


    return (head, next)

def intersect(slat, slon, elat, elon, lats, lons, head, 
              next, points, latind, lonind):
    #!NOTE: the C implementation has an optional 12th argument but this isn't
    #       used in the bindex module
    raise NotImplementedError


def intersect(slat, slon, elat, elon, lats, lons,
              head, next, points, latind, lonind):
    npoints = 0
    ngrid = len(lats)
    

    schunk = int(slon/360.0)
    echunk = int(elon/360.0)
    xslon = slon - 360.0 * schunk
    xelon = elon - 360.0 * echunk
    if schunk == echunk:
        npoints = intersect_l(slat, xslon, elat, xelon, lats, lons, 
                              head, ngrid, next, points, npoints, latind, lonind)
    else:
        loni = '%so' % lonind[0]
        npoints = intersect_l(slat, xslon, elat, 360.0, lats, lons, 
                              head, ngrid, next, points, npoints, latind, loni)
        loni = 'c%s' % lonind[1]
        npoints = intersect_l(slat, 0.0, elat, xelon, lats, lons, 
                              head, ngrid, next, points, npoints, latind, loni)

    return npoints

def intersect_l(slat, slon, elat, elon, lats, lons, head, ngrid, next, points, npoints, latind, lonind):

    si = int(slon/XBINI)
    si = min(max(si,0),(NBINI-1))
    sj = int((slat+90.0)/XBINI)
    sj = min(max(sj,0),NBINJ-1)
    ei = int(elon/XBINI)
    ei = min(max(ei,0),(NBINI-1))
    ej = int((elat+90.0)/XBINI)
    ej = min(max(ej,0),NBINJ-1)

    latind0 = latind[0]
    latind1 = latind[1]
    lonind0 = lonind[0]
    lonind1 = lonind[1]

    if slon == elon and (lonind0 == 'o' or lonind1 == 'o'):
        return npoints

    for i in xrange(si, ei+1):
        for j in xrange(sj, ej+1):
            hind = NBINJ*i + j
            rind = head[hind]
            if i == si or i == ei or j == sj or j == ej:
                while rind != -1:
                    lat = lats[rind]
                    lon = lons[rind]
                    if (((latind0=='c' and slat<=lat) or (latind0=='o' and slat<lat)) and
			((latind1=='c' and lat<=elat) or (latind1=='o' and lat<elat)) and
			((lonind0=='c' and slon<=lon) or (lonind0=='o' and slon<lon)) and
			((lonind1=='c' and lon<=elon) or (lonind1=='o' and lon<elon))):
                        if npoints == ngrid:
                            print 'Internal error in intersect.'
                            return npoints
                        points[npoints] = rind
                        npoints += 1
                    rind = next[rind]
            else:
                while rind != -1:
                    if npoints == ngrid:
                        print 'Internal error in intersect.'
                        return npoints
                    points[npoints] = rind
                    npoints += 1
                    rind = next[rind]
                    
    return npoints

if __name__ == '__main__':
    import cdms2.bindex
    
    lats = np.arange(-90, 90, 2.5)
    lons = np.arange(0, 360, 1.5)
    X, Y = np.meshgrid(lons, lats)
    
    Xr, Yr = X.ravel(), Y.ravel()
    head, next = cdms2.bindex.bindexHorizontalGrid(Yr, Xr)
    head2, next2 = bindexHorizontalGrid(Yr, Xr)

    print (head - head2 == 0).all()
    print (next - next2 == 0).all()

    slon = 270.0
    elon = 380.0
    lonopt = 'oc'

    slat = -45.0
    elat = 90.0
    latopt = 'cc'

    points = np.zeros(len(Yr), np.int)
    npoints = cdms2.bindex._bindex.intersect(slat, slon, elat, elon, Yr, Xr, head2, next2,
                                             points, latopt, lonopt)

    points2 = np.zeros(len(Yr), np.int)
    npoints2 = intersect(slat, slon, elat, elon, Yr, Xr, head2, next2,
                                             points, latopt, lonopt)

    print npoints == npoints2
    print (points - points == 0).all()

    print npoints, npoints2
