'''
    Just a backup/shelf for now
'''

import xlwings as xw
import pandas as pd
from icecream import ic
from pprint import pprint
import tanda
# For Excel times/dates
from datetime import datetime, timezone

sourceFile = 'new-car-trips-simple-export.csv'
destBook = 'location-automation.xlsx'

# Read CSV, extract necessary columns, calc extra col
def LoadnClean(csv):
    columns = ['Start Time', 'End Time',  'Odometer Start (km)', 'Odometer End (km)']
    df = pd.read_csv(csv, skiprows=10, usecols=columns)
    df['Travelled (Odometer)'] = df['Odometer End (km)'] - df['Odometer Start (km)']
    return df

print(LoadnClean(csv=sourceFile))
exit()

wb = xw.Book(destBook)
ws = wb.sheets['Results']
# ws.clear_contents() # does not clear formatting
ws.clear()
# Deploy extracted CSV unto Excel spreadsheet
# Only need point to top-left-most cell
ws.range("A1").options(index=False).value = LoadnClean(csv=sourceFile) # index=False omits index from dataframe

# Captures from Excel as dataframe
#def RangerFinder():


fromEx = ws.range('A1:B224').options( # auto find last row later
    pd.DataFrame,
    header=1,
    index=False,
    ).value

rrr = ws.range('A' + str(ws.cells.last_cell.row)).end('up').row
print(rrr)



fromTa = tanda.get_Shifts()
fromTa2 = tanda.get_Shifts2()
# Don't know if really need to separately capture for odeometer
Odom = ws.range('E1:E224').options( # auto find last row later
    pd.DataFrame,
    header=1,
    index=False,
    ).value

# Last row test
#qw = str(ws.cells.last_cell.row).end('up').row
#qw = ws.range('A1').end('down')
qw = ws.cells.last_cell.row
qw = str(qw)
qwe = ws.range('A'+ qw).end('up').row
print(qwe)

exit()

# Needed to add timezone info to Excels frame so it matches w/ Tanda's
fromEx['Start Time'] = fromEx['Start Time'].dt.tz_localize('Australia/Perth')
fromEx['End Time'] = fromEx['End Time'].dt.tz_localize('Australia/Perth')

# Compare sourced shifts to Excel log
def FindMatches(shifts, log):
    matches = []
    for entries in shifts:
        # Still datetime objects
        start = entries[0]
        end = entries[1]

        mask = (log['Start Time'] >= start) & (log['End Time'] <= end)
        filtered = log.loc[mask]
        # Add two to every index of the filtered results
        iAdd = list(map(lambda x : x+2, filtered.index.tolist()))
        matches.append(iAdd)
        #print(iAdd)
        #print('Start: ' + str(start), '\n', 'Finish: ' + str(end), '\n',filtered, '\n\n')

    return matches

# List array where each list (a shift) contains rows that match logs in Excel
matchesWrite = FindMatches(shifts=fromTa2, log=fromEx)

# Highlight matches
for shift in matchesWrite:
    for row in shift:
        cells = 'A{}:B{}'.format(row, row)
        #print(cells)
        ws.range(cells).color = (186, 192, 228)
        #print(row)
    #print('##########')

def Travels(data, indexes):
    workTotal = 0
    total = data['Travelled (Odometer)'].sum()
    # Shift Odometer's index so it matches with Excel
    # Recall Excel's earlier dataframe was also shifted to match with Excel's numbering
    data['Travelled (Odometer)'] = data['Travelled (Odometer)'].shift(2)
    #print('indexes ~~~~~~  ', indexes, '\n')
    '''for idx, val in enumerate(indexes):
        print(idx, val)
        indexes[idx] = list(map(lambda x : x-2, val))
        print(indexes)'''
    for i in indexes:
        # Need to do double-sum() to get an int
        # Something about how pandas returns a dataframe
        workTotal += data.loc[i].sum().sum()

    personal = total - workTotal

    return workTotal, personal, total

# Calculates Work, Personal & Total distances travelled
oDomCals = Travels(data=Odom, indexes=FindMatches(shifts=fromTa2, log=fromEx))

ocArray = [
    ['Work Travel', 'Personal Travel', 'Total Travel (km)'],
    [oDomCals[0], oDomCals[1], oDomCals[2]]
        ]
#pprint(ocArray)
#print('\n\n', 'total ', rr[0], '\n', 'workTotal: ', rr[1])
ws.range("G4").value = ocArray
expCols = ws.range("G4").expand()
expCols.autofit()


# print('\n\n', 'Odom *******', Odom)
#print(asd[0])
#print(Odom.loc[1])
#print(Odom.iloc[1])

#ic('\n\n', '2222 asd/indexes *******', asd)


# List array version
'''TaArray = fromTa.values.tolist()
pprint(TaArray)
print('\n', '\n')
print(type(TaArray[0][0]))
b = TaArray[0][0]
e = TaArray[0][1]
print(b, e)'''


'''print('\n')
print('from ex: >>>', fromEx.values)
#print('from ta: ~~~', fromTa)
p = fromEx.values
print(type(p))
print(len(p))'''

#print(len(fromEx.values.tolist()))

'''n = fromEx.values
ic(n)
#nn = datetime.utcfromtimestamp(n.astype('0')/1e9)
#nn = np.array([n], dtype='M8[ms]').astype('0')[0,1]
#nn = n.astype(datetime, copy=False)
nn = (n - np.datetime64('1970-01-01T00:00:00Z')) / np.timedelta64(1, 's')
ic(nn)'''

'''for i in fromEx.values:
    print(i)
    print(type(i[0]))'''


exit()

tt = fromTa.at[0, 'Start']
ic(tt)
ic(type(tt))
ett = fromEx.at[0, 'Start Time'].tz_localize('Australia/Perth')
ic(ett)
ic(type(ett))




#for i, j in fromTa['Start'], fromTa['Finish']:
#    print(i, j)
ee = fromEx.at[0, 'Start Time']
ic(ee)
ic(type(ee))





exit()

# Filter Tanda dataframe
fmt = '%d-%m-%Y %H:%M' # same as tanda file (remember remove)
# Need to give Tanda's dates a timezone so they can be compared w/ Excel's
# Probs better way - this does it for the project
# I think timezone.utc sets to local, which is fine for project
TaStart = datetime.strptime('10-03-2021 00:00', fmt).replace(tzinfo=timezone.utc)
TaEnd = datetime.strptime('10-03-2021 23:59', fmt).replace(tzinfo=timezone.utc)

TaMask = (fromTa['Start'] >= TaStart) & (fromTa['Finish'] <= TaEnd)

print('tanda ~~~~~~~~~~~~~~~')
print(TaFiltered, '\n')

# Filter Excel dataframe
ExStart = pd.to_datetime('10-03-2021 00:00', dayfirst=True)
ExEnd = pd.to_datetime('10-03-2021 23:59', dayfirst=True)
ExMask = (fromEx['Start Time'] >= ExStart) & (fromEx['End Time'] <= ExEnd)
ExFiltered = fromEx.loc[ExMask]
print('excel ~~~~~~~~~~~~~~~')
print(ExFiltered)
