'''
    Just a backup/shelf for now
'''

import requests
from pprint import pprint
from collections import OrderedDict
import pytz
from datetime import datetime
import pandas as pd # probs not need be imported again?

token = '857e0a90cdedf0427b7c57175dec19eef0626b92cf717009ba3ada0b2bdcc500'
baseEP = 'https://my.tanda.co/api/v2'
header = {'Authorization': 'bearer ' + token, 'Cache-Control': 'no-cache'}

# Endpoints
userE = baseEP + '/users/me'
cTimeE = baseEP + '/timesheets/current'
shiftE = baseEP + '/shifts'

# Parameters
cTimeP = {
    'show_costs': 'false',
    'show_award_interpretation': 'true'
    }
shiftP = {
    'show_costs': 'false',
    'show_award_interpretation': 'true',
    'user_ids': '207955',
    'from': '2021-03-8', # 2021-03-8
    'to': '2021-03-29' # 2021-03-28
    }

# api_call = requests.get(userEP, headers=header)
api_call = requests.get(shiftE, headers=header, params=shiftP)

#a = api_call.json()
a = api_call.json(object_pairs_hook=OrderedDict)
#pprint(a)

api_return = api_call.json()
#pprint(api_return)

# Utilised in Extraction function
def tc(time): # aka TimeConversion
    # CSV: 08-Mar-2021 20:26
    datetimeFormat = '%d-%b-%Y %H:%M'
    #zone = pytz.timezone('Australia/Perth')

    #return datetime.fromtimestamp(time, zone)#.strftime(datetimeFormat)
    return datetime.fromtimestamp(time)  # .strftime(datetimeFormat)

def Extraction(data):
    # Holds tuples for upcoming dataframe
    tmpStore = []
    for shift in data:
        start = shift['start']
        end = shift['finish']
        # Catch empty shift entries
        if start != None and end != None:
            tmpStore.append((tc(start), tc(end)))
            #print('TEST:  ', (tc(start), tc(end)))

        else:
            tURL = 'my.tanda.co/timesheets/'
            tSheetID = tURL + str(shift['timesheet_id'])
            #print(shift['date'], start, end, tSheetID)
            print('FOUND EMPTY >>> \n', shift['date'], start, end, tSheetID, '\n <<< END EMPTY')

    return tmpStore

#print('from tanda file: \n', api_return)
#pprint(Extraction(data=api_return))
print('\n\n\n')


def get_Shifts():
    return Extraction(data=api_return)

#pprint(api_return)