#http://www.david-greve.de/luach-code/jewish-python.html
import datetime
from common.date_utils_py2.calendar_util import gregorian_to_jd, jd_to_hebrew, hebrew_to_jd, leap_gregorian
from common.jewish_dates.sun import GetSunrise, GetSunset, GetShaaZmanit, Dayhours, Nighthours
import time
from datetime import datetime
from common.jewish_dates.parasha import getTorahSections

# Returns the weekday from a given hebrew date (0 for Sunday, 1 for Monday,...)
def _getWeekdayOfHebrewDate(hebDay, hebMonth, hebYear):
    # Calculating the julian date
    julian = hebrew_to_jd(hebYear, hebMonth, hebDay)
    weekday = (int(julian) + 2) % 7
    return weekday


def _get_hag_and_shabbat(g_day, g_month, g_year):
    julian = gregorian_to_jd(g_year, g_month, g_day)
    hebYear, hebMonth, hebDay = jd_to_hebrew(julian)

    shabbat = 'Shabbat' if _getWeekdayOfHebrewDate(hebDay, hebMonth, hebYear) == 6 else ''

    # Holidays in Nisan
    if hebDay == 15 and hebMonth == 1:
        return "Pesach"
    if hebDay == 21 and hebMonth == 1:
        return "Pesach"

    # Holidays in Sivan
    if hebDay == 6 and hebMonth == 3:
        return "Shavuot"

    # Holidays in Tishri
    if hebMonth == 7:
        if hebDay == 1 or hebDay == 2:
            return "RoshHashana"
        elif hebDay == 10:
            return "Yom Kippur"
        elif hebDay == 15:
            return "Sukkot"
        elif 15 < hebDay < 22 and shabbat:     #Treat Shabbat on Sukkot like Sukkot (so the blinds don't go down)
            return "Sukkot"
        elif hebDay == 22:
            return "SimchatTorah"

    return shabbat

def test_calculate_holiday():
    #A test program for the holiday calculation:

    year = 2017 #int(raw_input("Gregorian Year? "))
    nonleapgmonths = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    leapgmonths = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    for month in range(1,13):
        if leap_gregorian(year):
            lastDay = leapgmonths[month-1]
        else:
            lastDay = nonleapgmonths[month-1]
        for day in range(1,lastDay+1):
            hag = calculate_holiday(day, month, year, True)
            if hag:
                print(str(day) + "/" + str(month) + "/" + str(year) + ": " + str(hag))

def get_hag_and_shabbat(date):
    return _get_hag_and_shabbat(date.day, date.month, date.year)

# from common.date_utils_py2.times import today_sunrise_sunset
# location = 'Azriel_wiki'
# sunrise1, sunset1 = today_sunrise_sunset(location)
# print(sunrise1, sunset1)

def get_day_times(date=0):
    '''Returns sunrise, sunset, shaa, day, night'''
    tz_offset = -time.altzone / 60 / 60

    if not date:
        date = datetime.now()

    location = (3215, 3458, tz_offset, 53)  # Azriel_wiki, Israel, 32 deg 15 min N, 34 deg 58 min E, Asia/Jerusalem, 53
    sunrise = GetSunrise(date.month, date.day, date.year, location)
    sunset = GetSunset(date.month, date.day, date.year, location)
    shaa = GetShaaZmanit(sunrise, sunset)
    day = Dayhours(sunrise, sunset)
    night = Nighthours(sunrise, sunset)
    print('sunrise: %s, sunset: %s, shaa-zmanit: %s, day-hours: %s, night-hours: %s' % (sunrise, sunset, shaa, day, night))
    return sunrise, sunset, shaa, day, night
