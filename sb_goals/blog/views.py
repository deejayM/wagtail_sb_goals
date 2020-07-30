import datetime

from django.shortcuts import render
from django.utils import timezone

# add your views here.


# functions for this App

def days_in_month(year:int, month:int) -> int:
    """
    Inputs:
      year  - an integer between datetime.MINYEAR and datetime.MAXYEAR
              representing the year
      month - an integer between 1 and 12 representing the month

    Returns:
      The number of days in the input month.
    """
    #if month is december, we proceed to next year
    def month_december(month):
        if month > 12:
            return month-12  #minus 12 if cross year.
        else:
            return month

    #if month is december, we proceed to next year
    def year_december(year, month):
        if month > 12:
            return year + 1
        else:
            return year

    #verify if month/year is valid
    if (month < 1) or (month > 12):
        return  0
    elif (year < 1) or (year > 9999):
        return  0
    else:
        #subtract current month from next month then get days
        date1 = (datetime.date(year_december(year, month+1), month_december(month+1), 1) - datetime.date(year, month, 1)).days
        return (date1)


