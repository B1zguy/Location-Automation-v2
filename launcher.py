import tanda, log
# move to tanda when ready
from datetime import datetime, timedelta
## Development
from icecream import ic
import dateutil.relativedelta as relativedelta
from pprint import pprint


sourceFile = 'real-data/new-car-trips-simple-export.csv'
destBook = 'location-automation-compilation.xlsx'

dRange = [
    '2021-03-08', # from
    '2021-06-27'  # to
        ]

# print(tanda.every30(dateRange=dRange, endDate=ed))

fromLo = log.LoadnClean(csv=sourceFile)
fromTa = tanda.get_Shifts(dates=dRange)
# pprint(fromTa)
# print(len(fromTa))
# exit()
# List array where each list (a shift) contains rows that match logs in Excel
matchesWrite = log.FindMatches(shifts=fromTa, log=fromLo)
# Calculates Work, Personal & Total distances travelled
oDomCals = log.Travels(data=fromLo, indexes=matchesWrite)

# Write all data to log spreadsheet!
log.ExcelInject(
    highlights=matchesWrite,
    summary=oDomCals,
    spreadsheet=destBook,
    log=fromLo
            )
