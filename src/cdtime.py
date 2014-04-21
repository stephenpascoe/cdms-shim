"""

cdtime API in Python.

"""

import netcdftime as nct
from copy import deepcopy

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


# Mapping of cdtime calendar to netcdftime calendars
_calendar_map = {
    _Const.cdStandard: 'standard',
    _Const.cdJulian: 'julian',
    _Const.cdMixed: NotImplemented,
    _Const.cdNoLeap: 'noleap',
    _Const.cd360: '360_day',
    _Const.cdClim: NotImplemented,
    _Const.cdClimLeap: NotImplemented,
    _Const.cdMixed: NotImplemented,
}

def _nctime_calendar(cdtime_cal):
    cal = _calendar_map.get(cdtime_cal, NotImplemented)
    if cal is NotImplemented:
        raise NotImplementedError('cdtime calendar %s is not implemented' % cdtime_cal)



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

    def __init__(self, value, units):
        self.value = value
        self.units = units

    def __cmp__(self, t2):
        raise self.cmp(t2)

    def __repr__(self):
        return 'Reltime({0},{1})'.format(self.value, repr(self.units))

    def __str__(self):
        return '%s %s' % (self.value, self.units)

    def add(self, value, units, calendar=None):
        if calendar is None:
            calendar = StandardCalendar
        ct = self.tocomponent(calendar)
        ct2 = ct.add(value, units, calendar)

        return ct2.torelative(self.units, calendar)

    def sub(self, value, units, calendar=None):
        if calendar is None:
            calendar = StandardCalendar
        return self.add(-value, units, calendar)

    def torelative(self, units, calendar=None):
        if calendar is None:
            calendar = StandardCalendar
        if units == self.units:
            return deepcopy(self)
        else:
            ct = self.tocomponent(calendar)
            return ct.torelative(units, calendar)

    torel = torelative

    def tocomponent(self, calendar=None):
        if calendar is None:
            calendar = StandardCalendar

        dt = nct.num2date(self.value, self.units, _calendar_map[calendar])
        ct = CompTime(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)

        return ct

    tocomp = tocomponent

    def cmp(self, other, calendar):
        if isinstance(other, RelTime) and other.units == self.units:
            return cmp(self.value, other.value)
        else:
            ct1 = self.tocomponent(calendar)
            ct2 = self.tocomponent(calendar)
            return ct1.cmp(ct2)


class CompTime(CdTime):
    """
    :property year:
    :property month:
    :property day:
    :property hour:
    :property minute:
    :property second:
    :property absvalue:
    :property absunits:
    :property fraction:
    """

    def __init__(self, year, month, day, hour, minute, second):
        self._datetime = nct.datetime(year, month, day, hour, minute, second)

    def __cmp__(self, t2):
        return self.cmp(t2)

    def __repr__(self):
        return 'CompTime({year},{month},{day},{hour},{minute},{second})'.format(
            **self._datetime.__dict__)

    def __str__(self):
        return str(self._datetime)

    @property
    def year(self):
        return self._datetime.year
    @year.setter
    def set_year(self, year):
        self._datetime.year = year

    @property
    def month(self):
        return self._datetime.month
    @month.setter
    def set_month(self, month):
        self._datetime.month = month

    @property
    def day(self):
        return self._datetime.day
    @month.setter
    def set_day(self, day):
        self._datetime.day = day

    @property
    def hour(self):
        return self._datetime.hour
    @hour.setter
    def set_hour(self, hour):
        self._datetime.hour = hour

    @property
    def minute(self):
        return self._datetime.minute
    @minute.setter
    def set_minute(self, minute):
        self._datetime.minute = minute

    @property
    def second(self):
        return self._datetime.second
    @second.setter
    def set_second(self, second):
        self._datetime.second = second

    @property
    def absunits(self):
        raise NotImplementedError

    @property
    def absvalue(self):
        raise NotImplementedError

    @property
    def absfraction(self):
        raise NotImplementedError

    def add(self, value, units, calendar=None):
        if calendar is None:
            calendar = StandardCalendar

        if units >= Months:
            if units == Years:
                incr = 12.0 * value
            elif units == Seasons:
                incr = 3.0 * value
            elif units == Months:
                incr = value
            else:
                raise ValueError('Unrecognised cdtime units %s' % units)
        
            origin = 'months since %s' % self._datetime
            dt = nct.num2date(incr, origin, _calendar_map[celandar])    
        else:
            if units == Weeks:
                value = value * 168.0
            elif units == Days:
                value = value * 24.0
            elif units == Hours:
                pass
            elif units == Minutes:
                value = value / 60.0
            elif units == Seconds:
                value = value / 3600.0
            else:
                raise ValueError('Unrecognised cdtime units %s' % units)

            origin = 'hours since %s' % self._datetime
            dt = nct.num2date(value, origin, _calendar_map[calendar])

        ct = CompTime(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)
        return ct

    def sub(self, value, units, calendar=None):
        if calendar is None:
            calendar = StandardCalendar

        return self.add(-value, units, calendar)

    def torelative(self, units, calendar=None):
        if calendar is None:
            calendar = StandardCalendar

        t = nct.date2num(self._datetime, units, calendar=_calendar_map[calendar])
        return RelTime(t, units)
    torel = torelative

    def tocomponent(self, calendar=None):
        if calendar is None:
            calendar = StandardCalendar

        return deepcopy(self)
    tocomp = tocomponent

    def cmp(self, other, calendar=None):
        if calendar is None:
            calendar = StandardCalendar

        if isinstance(other, RelTime):
            other_ct = other.tocomponent(calendar)
        else:
            other_ct = other

        for comp in ['year', 'month', 'day', 'hour', 'minute', 'second']:
            v1 = getattr(self, comp)
            v2 = getattr(other_ct, comp)
            ret = cmp(v1, v2)
            if ret != 0:
                return ret

        return 0



def relativetime(value, units):
    """
    Create a relative time type.

    value is an integer or floating point value.
    relunits is a string of the form "unit(s) [since basetime]"
    where
    unit = [second | minute | hour | day | week | month |
    season | year]
    basetime has the form yyyy-mm-dd hh:mi:ss. The default
    basetime is 1979-1-1, if no since clause is specified.

    Example: r = cdtime.reltime(28, "days since 1996-1-1")
    """
    return RelTime(value, units)

reltime = relativetime

def componenttime(year, month=1, day=1, hour=0, minute=0, second=0):
    """
    Create a component time type.

    year is an integer.
    month is an integer in the range 1 .. 12
    day is an integer in the range 1 .. 31
    hour is an integer in the range 0 .. 23
    minute is an integer in the range 0 .. 59
    second is a floating point number in the range 0.0 ,, 60.0

    Example:   c = cdtime.comptime(1996, 2, 28)

    """

    return CompTime(year, month, day, hour, minute, second)

comptime = componenttime

def abstime(value, units):
    """
    Marked as deprecated in the PCMDI docs.

    absvalue is a floating-point encoding of an absolute time.
    absunits is the units template, a string of the form "unit as
    format", where unit is one of second, minute, hour, day,
    calendar_month, or calendar_year. format is a string of
    the form "%x[%x[...] ][.%f]", where 'x' is one of the format
    letters 'Y' (year, including century), 'm' (two digit month,
    01=January), 'd' (two-digit day within month), 'H' (hours
    since midnight), 'M' (minutes), or 'S' (seconds ). The optional
    '.%f' denotes a floating-point fraction of the unit.
    
    Example:    c = cdtime.abstime(19960228.0, "day as %Y%m%d.%f")
    """
    raise NotImplementedError

def s2c(ctime, calendar=None):
    raise NotImplementedError

def s2r(ctime, units, calendar=None):
    raise NotImplementedError

def c2r(comptime, units, calendar=None):
    return comptime.torelative(units, calendar)

def r2c(reltime, calendar=None):
    return reltime.tocomponent(calendar)

def r2r(reltime, units, calendar=None):
    return reltime.torelative(units, calendar)

def compare(t1, t2, calendar=None):
    return t1.cmp(t2, calendar=None)
