"""

bindex interface.

"""

def bindex(lats, lons, head, next):
    #!NOTE: the C implementation has an optional 5th argument but this isn't
    #       used in the bindex module
    raise NotImplementedError

def intersect(slat, slon, elat, elon, lats, lons, head, 
              next, points, latind, lonind):
    #!NOTE: the C implementation has an optional 12th argument but this isn't
    #       used in the bindex module
    raise NotImplementedError
