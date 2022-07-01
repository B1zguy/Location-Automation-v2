
# api_call = requests.get(userEP, headers=header)
api_call = requests.get(cTimeE, headers=header, params=cTimeP)

# a = api_call.json()
a = api_call.json(object_pairs_hook=OrderedDict)
#b = api_call.content.decode(requests.utils.guess_json_utf(api_call.content)).encode('utf-8')
pprint(a[0]['shifts'])
#print(type(a))

print(len(a[0]['shifts']))
print('\n\n', "==================== looped below")

for i in a[0]['shifts']:
    pprint(i)
    print('***********')
print(type(a[0]['shifts']))
print('\n\n', "====================")

for k, v in a[0]['shifts'][0].items():
    pprint(k)

print('\n\n', "OG ==================== OG")
pprint(a)

print('\n\n', "****** ==================== ******")
#pprint(b)


Ordering dictionaries:
https://stackoverflow.com/a/51412438/7923512



def tc(time): # aka TimeConversion
    # CSV: 08-Mar-2021 20:26
    datetimeFormat = '%d-%b-%Y %H:%M'
    zone = pytz.timezone('Australia/Perth')

    return datetime.fromtimestamp(time, zone)#.strftime(datetimeFormat)

def tc(time): # aka TimeConversion
    # CSV: 08-Mar-2021 20:26
    t = datetime.utcfromtimestamp(int(time))
    tWithz = datetime(
        year=t.year,
        month=t.month,
        day=t.day,
        hour=t.hour,
        minute=t.minute,
        second=t.second,
        tzinfo=pytz.UTC
        )

    return tWithz

# Returning as dataframe
def get_Shifts():
    return pd.DataFrame(Extraction(data=api_return), columns=('Start', 'Finish'))

# Getting ordered dictionary
from collections import OrderedDict
a = api_call.json(object_pairs_hook=OrderedDict)
#pprint(a)