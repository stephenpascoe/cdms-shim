"""

cdtime API in Python.

"""

class error(Exception):
    """Cdtime error"""
    pass

# Constants

class _Const(object):
    cdStandardCal =  0x11
    cdClimCal =       0x0
    cdHasLeap =     0x100
    cdHasNoLeap =   0x000
    cd365Days =    0x1000
    cd360Days =    0x0000
    cdJulianCal = 0x10000
    cdMixedCal =  0x20000

    cdStandard    = ( cdStandardCal | cdHasLeap   | cd365Days)
    cdJulian      = ( cdStandardCal | cdHasLeap   | cd365Days | cdJulianCal)
    cdNoLeap      = ( cdStandardCal | cdHasNoLeap | cd365Days)
    cd360         = ( cdStandardCal | cdHasNoLeap | cd360Days)
    cdClim        = ( cdClimCal     | cdHasNoLeap | cd365Days)
    cdClimLeap    = ( cdClimCal     | cdHasLeap   | cd365Days)
    cdClim360     = ( cdClimCal     | cdHasNoLeap | cd360Days)
    cdMixed       = ( cdStandardCal | cdHasLeap   | cd365Days | cdMixedCal)

    PyCdtime_Seconds = 1
    PyCdtime_Minutes = 2
    PyCdtime_Hours = 3
    PyCdtime_Days = 4
    PyCdtime_Weeks = 5
    PyCdtime_Months = 6
    PyCdtime_Seasons = 7
    PyCdtime_Years = 8


StandardCalendar = _Const.cdStandard
GregorianCalendar = _Const.cdStandard
JulianCalendar = _Const.cdJulian
MixedCalendar = _Const.cdMixed
NoLeapCalendar = _Const.cdNoLeap
Calendar360 = _Const.cd360
ClimCalendar = _Const.cdClim
ClimLeapCalendar = _Const.cdClimLeap
DefaultCalendar = _Const.cdMixed
Seconds = _Const.PyCdtime_Seconds
Second = _Const.PyCdtime_Seconds
Minutes = _Const.PyCdtime_Minutes
Minute = _Const.PyCdtime_Minutes
Hours = _Const.PyCdtime_Hours
Hour = _Const.PyCdtime_Hours
Days = _Const.PyCdtime_Days
Day = _Const.PyCdtime_Days
Weeks = _Const.PyCdtime_Weeks
Week = _Const.PyCdtime_Weeks
Months = _Const.PyCdtime_Months
Month = _Const.PyCdtime_Months
Seasons = _Const.PyCdtime_Seasons
Season = _Const.PyCdtime_Seasons
Years = _Const.PyCdtime_Years
Year = _Const.PyCdtime_Years



class CdTime(object):
    def add(self, value, units, calendar):
        raise NotImplementedError

    def sub(self, value, units, calendar):
        raise NotImplementedError

    def torelative(self, units, calendar):
        raise NotImplementedError

    torel = torelative

    def tocomponent(self, celandar):
        raise NotImplementedError

    tocomp = tocomponent

    def cmp(self, other, calendar):
        raise NotImplementedError
    



class RelTime(CdTime):
    """
    :ivar value:
    :ivar units:
    """
    def __getattr__(self):
        raise NotImplementedError

    def __setattr__(self):
        raise NotImplementedError

    def __cmp__(self, t2):
        raise NotImplementedError

    def __repr(self):
        raise NotImplementedError

class CompTime(CdTime):
    """
    :ivar year:
    :ivar month:
    :ivar day:
    :ivar hour:
    :ivar minute:
    :ivar second:
    :ivar absvalue:
    :ivar absunits:
    :ivar fraction:
    """

    def __init__(self, year, month, day, hour, minute, second):
        raise NotImplementedError

    def __cmp__(self, t2):
        raise NotImplementedError

    def __repr__(self):
        raise NotImplementedError



def relativetime(value, units):
    raise NotImplementedError
reltime = relativetime

def componenttime(year, month=None, day=None, hour=None, minute=None, second=None):
    raise NotImplementedError
comptime = componenttime

def abstime(value, units):
    raise NotImplementedError

def s2c(ctime, calendar=None):
    raise NotImplementedError

def s2r(ctime, units, calendar=None):
    raise NotImplementedError

def c2r(comptime, units, calendar=None):
    raise NotImplementedError

def r2c(reltime, calendar=None):
    raise NotImplementedError

def r2r(reltime, units, calendar=None):
    raise NotImplementedError

def compare(t1, t2, calendar=None):
    raise NotImplementedError
