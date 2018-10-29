#http://www.david-greve.de/luach-code/jewish-python.html - Changed GetShaaZmanit to be 2 decimal places and added dayhours and nighthours
#Sunrise, sunset, degrees below horizons, proportional hours
#
#The FormatTime12 function takes a calculated time and returns a formatted string, in which the time in am/pm format is contained
#The FormatTime24 function takes a calculated time and returns a formatted string, in which the time in 24 hour format is contained
#The GetSunrise-function takes the gregorian month, day, year and the location. location is a tuple (latitude, longitude, timezone, elevation) It returns the Sunrise. Elevation is in metres (0 if not known), timezone is relative to GMT, e.g. 1 = GMT+1, for the values of latitude and longitude, the deegrees must be multiplied with hundred and then the minutes added, positive latitudes are north, negative latitudes are south, positive longitudes are east, negative longitudes are west.
#The GetSunriseDeegreesBelowHorizon function takes the gregorian month, day, year, the degrees below horizon and the location and returns the calculated time
#The GetSunset function takes the gregorian month, day, year and location. It returns the Sunset.
#The GetSunsetDeegreesBelowHorizon function takes the month, day, year, degrees below horizon and the location and returns the calculated time
#The AddMinutes function takes the time and the minutes. It returns a time to which minutes were added
#The SubtractMinutes function takes the time and the minutes. It returns a new time from which minutes were subtracted
#The GetProportional function takes the number of the proportional hour, sunrise and the sunset. It returns the calculated time
#The GetShaaZmanit function takes the sunrise and the sunset and returns the length of a proportional hor (Shaa Zmanit)

import math

# FormatTime12, FormatTime24
# GetSunrise, GetSunriseDegreesBelowHorizon
# GetSunset, GetSunsetDegreesBelowHorizon
# AddMinutes, SubtractMinutes
# GetProportionalHours, GetShaaZmanit

# Methods for Shabbat time calculation:
# location is a tuple (latitude, longitude, timezone, elevation)
# For example: Pforzheim has the tuple (4854, 842, 1, 257)
#
# GetSunset(uMonth, uDay, uYear, location)
# GetSunsetDegreesBelowHorizon(uMonth, uDay, uYear,
#                   fDegreesBelowHorizon, location)
# AddMinutes(time, min)
# SubtractMinutes(time, min)

locationPforzheim = (4854, 842, 1, 263)


def FormatTime12(time):
    if time == None:
        return "--:--"

    hour = time[0]
    min = time[1]

    hourModulo12 = hour % 12
    if (hourModulo12 == 0):
        hourModulo12 = 12

    if (hour >= 12):
        ampm = "PM"
    else:
        ampm = "AM"

    if (hourModulo12 < 10):
        hourStr = "0" + str(hourModulo12)
    else:
        hourStr = str(hourModulo12)
    if (min < 10):
        minStr = "0" + str(min)
    else:
        minStr = str(min)
    return hourStr + ":" + minStr + ampm


def FormatTime24(time):
    if time == None:
        return "--:--"

    hour = time[0]
    min = time[1]

    if (hour < 10):
        hourStr = "0" + str(hour)
    else:
        hourStr = str(hour)
    if (min < 10):
        minStr = "0" + str(min)
    else:
        minStr = str(min)
    return hourStr + ":" + minStr


def FormatTimeShaaZmanit(time):
    if time == None:
        return "--:--"

    hour = time[0]
    min = time[1]

    if (hour < 10):
        hourStr = "0" + str(hour)
    else:
        hourStr = str(hour)
    if (min < 10):
        minStr = "0" + str(min)
    else:
        minStr = str(min)
    return hourStr + ":" + minStr


def leap(y):
    if (y % 400 == 0):
        return True
    if (y % 100 != 0):
        if (y % 4 == 0):
            return True
    return False


def doy(d, m, y):
    monCount = [0, 1, 32, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335, 366]
    if ((m > 2) and (leap(y))):
        return monCount[m] + d + 1
    else:
        return monCount[m] + d


def todec(deg, min):
    return (deg + min / 60.0)


def M(x):
    return (0.9856 * x - 3.251)


def L(x):
    return (x + 1.916 * math.sin(0.01745 * x) + 0.02 * math.sin(2 * 0.01745 * x) + 282.565)


def adj(x):
    return (-0.06571 * x - 6.620)


def float_abs(x):
    if (x < 0.0):
        return (-x)
    else:
        return (x)


def suntime(d, m, y, \
            zendeg, zenmin, \
            londeg, lonmin, ew, \
            latdeg, latmin, ns, \
            tz, \
            elevation):  # Elevation in meters
    if (zendeg == 90):
        earthRadiusInMeters = 6356.9 * 1000.0
        elevationAdjustment = math.degrees \
            (math.acos(earthRadiusInMeters / (earthRadiusInMeters + elevation)))

        z = zendeg + zenmin / 60.0
        z += elevationAdjustment
        zendeg = math.floor(z)
        zenmin = (z - math.floor(z)) * 60

    day = doy(d, m, y)
    cosz = math.cos(0.01745 * todec(zendeg, zenmin))

    longitude = todec(londeg, lonmin)
    if ew != 0:
        longitude *= -1
    lonhr = longitude / 15.0
    latitude = todec(latdeg, latmin)
    if ns != 0:
        latitude *= -1
    coslat = math.cos(0.01745 * latitude)
    sinlat = math.sin(0.01745 * latitude)

    t_rise = day + (6.0 + lonhr) / 24.0
    t_set = day + (18.0 + lonhr) / 24.0

    xm_rise = M(t_rise)
    xl_rise = L(xm_rise)
    xm_set = M(t_set)
    xl_set = L(xm_set)

    a_rise = 57.29578 * math.atan(0.91746 * math.tan(0.01745 * xl_rise))
    a_set = 57.29578 * math.atan(0.91746 * math.tan(0.01745 * xl_set))
    if (float_abs(a_rise + 360.0 - xl_rise) > 90.0):
        a_rise += 180.0
    if (a_rise > 360.0):
        a_rise -= 360.0

    if (float_abs(a_set + 360.0 - xl_set) > 90.0):
        a_set += 180.0
    if (a_set > 360.0):
        a_set -= 360.0

    ahr_rise = a_rise / 15.0
    sindec = 0.39782 * math.sin(0.01745 * xl_rise)
    cosdec = math.sqrt(1.0 - sindec * sindec)
    h_rise = (cosz - sindec * sinlat) / (cosdec * coslat)

    ahr_set = a_set / 15.0
    sindec = 0.39782 * math.sin(0.01745 * xl_set)
    cosdec = math.sqrt(1.0 - sindec * sindec)
    h_set = (cosz - sindec * sinlat) / (cosdec * coslat)

    if (float_abs(h_rise) <= 1.0):
        h_rise = 57.29578 * math.acos(h_rise)
    else:
        return None  # NO_SUNRISE

    if (float_abs(h_set) <= 1.0):
        h_set = 57.29578 * math.acos(h_set)
    else:
        return None  # NO_SUNSET
    ut_rise = ((360.0 - h_rise) / 15.0) + ahr_rise + adj(t_rise) + lonhr
    ut_set = (h_rise / 15.0) + ahr_set + adj(t_set) + lonhr

    returnSunrise = ut_rise + tz  # sunrise
    returnSunset = ut_set + tz  # sunset
    return (returnSunrise, returnSunset)


def timeadj(t):
    if (t < 0):
        t += 24.0

    hour = int(math.floor(t))
    min = int(math.floor((t - hour) * 60.0 + 0.5))

    if (min >= 60):
        hour += 1
        min -= 60

    if (hour > 24):
        hour -= 24

    return [hour, min]


def GetDegreesBelowHorizonAdd(uMonth, uDay, uYear, \
                              fDegreesBelowHorizon, \
                              location):
    iLatitude, iLongitude, iTimeZone, elevation = location
    if (iLongitude < 0):
        longitudeFlag = 0
    else:
        longitudeFlag = 1
    if (iLatitude < 0):
        latitudeFlag = 1
    else:
        latitudeFlag = 0
    returnTimes = suntime(uDay, uMonth, uYear, \
                          90, 50, \
                          int(math.floor(math.fabs(iLongitude / 100.0))), \
                          abs(iLongitude) % 100, longitudeFlag, \
                          int(math.floor(math.fabs(iLatitude / 100.0))), \
                          abs(iLatitude) % 100, latitudeFlag, \
                          iTimeZone, elevation);
    if (returnTimes != ""):
        srTime = timeadj(returnTimes[1])
        while (srTime[0] > 12):
            srTime[0] -= 12

        db = fDegreesBelowHorizon + 90.0
        deghour = math.floor(db)
        db = db - deghour
        db *= 60.0
        degmin = math.floor(db)
        returnTimes = suntime(uDay, uMonth, uYear, \
                              deghour, degmin, \
                              int(math.floor(math.fabs(iLongitude / 100.0))), \
                              abs(iLongitude) % 100, longitudeFlag, \
                              int(math.floor(math.fabs(iLatitude / 100.0))), \
                              abs(iLatitude) % 100, latitudeFlag, \
                              iTimeZone, elevation)
        if (returnTimes != ""):
            dbTime = timeadj(returnTimes[1])
            while (dbTime[0] > 12):
                dbTime[0] -= 12

            srTimeValue = srTime[0] * 60 + srTime[1]
            dbTimeValue = dbTime[0] * 60 + dbTime[1]
            return dbTimeValue - srTimeValue
    return None


def GetSunrise(uMonth, uDay, uYear, location):
    iLatitude, iLongitude, iTimeZone, elevation = location
    if (iLongitude < 0):
        longitudeFlag = 0
    else:
        longitudeFlag = 1
    if (iLatitude < 0):
        latitudeFlag = 1
    else:
        latitudeFlag = 0
    returnTimes = suntime(uDay, uMonth, uYear, \
                          90, 50, \
                          int(math.floor(math.fabs(iLongitude / 100.0))), \
                          abs(iLongitude) % 100, longitudeFlag, \
                          int(math.floor(math.fabs(iLatitude / 100.0))), \
                          abs(iLatitude) % 100, latitudeFlag, \
                          iTimeZone, elevation)
    if (returnTimes != ""):
        returnTime = timeadj(returnTimes[0])

        while (returnTime[0] > 12):
            returnTime[0] -= 12

        return returnTime
    else:
        return None


def GetSunriseDegreesBelowHorizon(uMonth, uDay, uYear, \
                                  fDegreesBelowHorizon, \
                                  location):
    t = GetSunrise(uMonth, uDay, uYear, location)
    if (t != None):
        adding = GetDegreesBelowHorizonAdd(uMonth, uDay, uYear, fDegreesBelowHorizon, location)
        if (adding != None):
            return SubtractMinutes(t, adding)
        else:
            return None
    else:
        return None


def GetSunset(uMonth, uDay, uYear, \
              location):
    iLatitude, iLongitude, iTimeZone, elevation = location
    if (iLongitude < 0):
        longitudeFlag = 0
    else:
        longitudeFlag = 1
    if (iLatitude < 0):
        latitudeFlag = 1
    else:
        latitudeFlag = 0
    returnTimes = suntime(uDay, uMonth, uYear, \
        90, 50, \
        int(math.floor(math.fabs(iLongitude / 100.0))), \
        abs(iLongitude) % 100, longitudeFlag, \
        int(math.floor(math.fabs(iLatitude / 100.0))), \
        abs(iLatitude) % 100, latitudeFlag, \
        iTimeZone, elevation)
    if (returnTimes != None):
        returnTime = timeadj(returnTimes[1])

        while (returnTime[0] < 12):
            returnTime[0] += 12

        return returnTime
    else:
        return None


def GetSunsetDegreesBelowHorizon(uMonth, uDay, uYear, \
                                 fDegreesBelowHorizon, \
                                 location):
    t = GetSunset(uMonth, uDay, uYear, location)
    if (t != ""):
        adding = GetDegreesBelowHorizonAdd(uMonth, uDay, uYear, fDegreesBelowHorizon, location)
        if (adding != None):
            return AddMinutes(t, adding)
        else:
            return None
    else:
        return None


def AddMinutes(time, min):
    if (time == None):
        return None
    time2 = time
    time2[1] += min
    while (time2[1] >= 60):
        time2[1] -= 60
        time2[0] += 1
    return time2


def SubtractMinutes(time, min):
    if (time == None):
        return None
    time2 = time
    time2[1] -= min
    while (time2[1] < 0):
        time2[1] += 60
        time2[0] -= 1
    return time2


def GetProportionalHours(value, sunrise, sunset):
    if (sunrise == None or sunset == None):
        return None
    sr = sunrise[0] * 60 + sunrise[1]
    ss = sunset[0] * 60 + sunset[1]
    retval = sr + math.floor(((ss - sr) * value) / 12)
    return [int(math.floor(retval / 60)), int(retval % 60)]

def GetShaaZmanit(sunrise, sunset):
    sr = sunrise[0] * 60 + sunrise[1]
    ss = sunset[0] * 60 + sunset[1]
    return round((ss - sr) / 0.12) / 100        #round to two decimal places

def Dayhours(sunrise, sunset):
    sr = sunrise[0] * 60 + sunrise[1]
    ss = sunset[0] * 60 + sunset[1]
    return round((ss - sr) / 0.6) / 100         #round to two decimal places

def Nighthours(sunrise, sunset):
    return 24 - Dayhours(sunrise, sunset)
