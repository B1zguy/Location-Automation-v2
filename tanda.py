import requests
from datetime import datetime, timedelta
import pytz # For converting to Perth timezone
## Development
from pprint import pprint
from icecream import ic


token = '857e0a90cdedf0427b7c57175dec19eef0626b92cf717009ba3ada0b2bdcc500'
base = 'https://my.tanda.co/api/v2'
header = {'Authorization': 'bearer ' + token, 'Cache-Control': 'no-cache'}

# Endpoints & Parameters
shiftE = base + '/shifts'

# Requires dates at to complete paramaters
# Vars injected from launcher.py at runtime
shiftP = {
    'show_costs': 'false',
    'show_award_interpretation': 'true',
    'user_ids': '207955'
        }

fmt = '%Y-%m-%d'

# Quick function to convert date string to datetime obj
# Need to convert couple times so chucking it in one place
# Not permanent cos Tanda needs them as strings
def dateChange(laDate):
    return [datetime.strptime(laDate[i], fmt) for i, d in enumerate(laDate)]
    # https://stackoverflow.com/a/7422624/7923512

# Yeah cbf combining functions
def dateString(ds):
    return [ds[i].strftime(fmt) for i, d in enumerate(ds)]

# Move given date range 30 days per API return
# To overcome 31 days query limit of Tanda
# Gathering all shifts prior to processing
def next30(dateRange):

    ''' if isinstance(dateRange[0], str):
        fmt = '%Y-%m-%d'
        dateRange = [datetime.strptime(dateRange[i], fmt) for i, d in enumerate(dateRange)]
        # https://stackoverflow.com/a/7422624/7923512'''

    # Add one to not include current day in next block
    dateRange[0] = dateRange[1] + timedelta(days=1)
    dateRange[1] = dateRange[0] + timedelta(days=10)

    return dateRange

def Extraction(data):
    # Holds tuples for upcoming dataframe
    tmpStore = []
    for shift in data:
        start = shift['start']
        end = shift['finish']
        # Catch empty shift entries
        if start != None and end != None:
            # Looks like time is given in local time ...
            ##tmpStore.append((datetime.fromtimestamp(start), datetime.fromtimestamp(end)))
            ###tmpStore.append((datetime.fromtimestamp(start, tz=pytz.timezone('Australia/Perth')), datetime.fromtimestamp(end, tz=pytz.timezone('Australia/Perth'))))
            # Had to hardcode timezone offset just to push this out the door
            # It was basing off local time before.
            tmpStore.append((datetime.fromtimestamp(start) - timedelta(hours=2), datetime.fromtimestamp(end) - timedelta(hours=2)))
            print(tmpStore)
            print('')
        else:
            tURL = 'my.tanda.co/timesheets/'
            tSheetID = tURL + str(shift['timesheet_id'])
            #print(shift['date'], start, end, tSheetID)
            print('FOUND EMPTY >>> \n', shift['date'], start, end, tSheetID, '\n <<< END EMPTY')

    return tmpStore

def api_Call(tandaDates):
    shiftP['from'] = tandaDates[0]
    shiftP['to'] = tandaDates[1]

    return requests.get(shiftE, headers=header, params=shiftP).json()


def get_Shifts(dates):
    datesCon = dateChange(dates)
    # End date used to terminate loop and
    # create remainder/final range
    datesConEnd = datesCon[1]
    # While loop begins at dRange's 'from' date yet don't
    #   want loop to be dRange thus trim to same day so it
    #   can properly count every 30 days.
    # The next30 funct already adds one so
    #   removing prior to launching loop
    datesCon[1] = datesCon[0] = datesCon[0] + timedelta(days=-1)
    # Probs could find a better way than repeating var
    #   yet just wanna finish this project, sorry.
    check30 = (datesConEnd - datesCon[1]).days
    # Initiating api return incase loop is skipped
    api_return = []

    while check30 > 10:
        datesCon = next30(dateRange=datesCon)
        check30 = (datesConEnd - datesCon[1]).days
        api_return.extend(api_Call(tandaDates=(dateString(datesCon))))
    # Just 'manually' create the range for the final tidbit
    if check30 <= 10 and datesCon[1] != datesConEnd:
        datesCon[0] = datesCon[1] + timedelta(days=1)
        datesCon[1] = datesConEnd
        api_return.extend(api_Call(tandaDates=(dateString(datesCon))))

    # shiftP['from'] = dates[0]
    # shiftP['to'] = dates[1]
    # api_return = requests.get(shiftE, headers=header, params=shiftP).json()

    # Checks if return is error
    # Can only query 31 days at time
    if type(api_return) not in [list]:
        print(api_return)
        exit()
    # pprint api_return))
    # exit()
    return Extraction(data=api_return)
