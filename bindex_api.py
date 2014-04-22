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
    #!TODO: replace this slow implementation with a numpy-optimised one


    head = np.ones((BINLEN, ), np.int) * -1
    last = np.ones((BINLEN, ), np.int) * -1
    next = np.ones((BINLEN, ), np.int) * -1

    assert len(lats.shape) == 1
    n = lats.shape[0]

    for ireg in xrange(n):
        i = int(np.floor(lons[ireg]/XBINI))
        i = i % NBINI

        if i < 0: i += NBINI

        j = int(np.floor((lats[ireg]+90.0)/XBINJ))
        j = min(max(j, 0), NBINJ - 1)

        oind = NBINJ*i + j

        if head[oind] == -1:
            head[oind] = last[oind] = ireg
        else:
            next[last[oind]] = ireg
            last[oind] = ireg

    return (head, next)


def intersect(slat, slon, elat, elon, lats, lons, head, 
              next, points, latind, lonind):
    #!NOTE: the C implementation has an optional 12th argument but this isn't
    #       used in the bindex module
    raise NotImplementedError


if __name__ == '__main__':
    lats = np.arange(-90, 90, 0.5)
    lons = np.arange(0, 360, 0.5)
    X, Y = np.meshgrid(lons, lats)

    head, next = bindex(Y, X)
