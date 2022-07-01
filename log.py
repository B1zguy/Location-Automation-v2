import xlwings as xw
import pandas as pd
import tanda # Project file
## Development
from pprint import pprint
from icecream import ic


# Read CSV, extract necessary columns, calc extra col
# Returns Pandas dataframe
def LoadnClean(csv):
    columns = ['Start Time', 'End Time',  'Odometer Start (km)', 'Odometer End (km)']
    df = pd.read_csv(csv, skiprows=10, usecols=columns)
    df['Travelled (Odometer)'] = df['Odometer End (km)'] - df['Odometer Start (km)']

    # Convert dates to datetime object (or is Timestamp obj - Pandas)
    fmt = '%d-%b-%Y %H:%M' # 08-Mar-2021 20:26
    df['Start Time'] = pd.to_datetime(df['Start Time'], format=fmt)
    df['End Time'] = pd.to_datetime(df['End Time'], format=fmt)

    return df

# Compare sourced shifts to Excel log
def FindMatches(shifts, log):
    # Extract start & times
    log = log[['Start Time', 'End Time']]
    matches = []
    for entries in shifts:
        # Still datetime objects
        start = entries[0]
        end = entries[1]

        mask = (log['Start Time'] >= start) & (log['End Time'] <= end)
        filtered = log.loc[mask]
        # ic(filtered)
        # Add two to every index of the filtered results
        # to align with Excel's row numbering
        iAdd = list(map(lambda x : x+2, filtered.index.tolist()))
        matches.append(iAdd)
    pprint(matches)
    ic(len(matches))
    return matches

# Calculating and prepare Odometer data
def Travels(data, indexes):
    workTotal = 0
    total = data['Travelled (Odometer)'].sum()
    # Shift Odometer's index so it matches with Excel
    # Recall log/Excel's earlier dataframe was also shifted to match with Excel's numbering
    # Needed to instantiate new var so orig dataframe isn't messed w/
    dataOdom = data['Travelled (Odometer)'].shift(2)
    for i in indexes:
        # Need to do double-sum() to get an int
        # Something about how pandas returns a dataframe
        workTotal += dataOdom.loc[i].sum().sum()
    personal = total - workTotal

    ocArray = [
        ['Work Travel', 'Personal Travel', 'Total Travel (km)'],
        [workTotal, personal, total]
    ]
    return ocArray

def ExcelInject(highlights, summary, spreadsheet, log):
    wb = xw.Book(spreadsheet)
    ws = wb.sheets['Results']
    # ws.clear_contents() # does not clear formatting
    ws.clear()

    # Deploy log dataframe (that was CSV) unto Excel spreadsheet
    # Only need point to top-left-most cell
    ws.range("A1").options(index=False).value = log  # index=False omits index from dataframe

    # Highlight matches in Excel
    for shift in highlights:
        for row in shift:
            cells = 'A{}:B{}'.format(row, row)
            ws.range(cells).color = (186, 192, 228)

    # Inject travel summary array
    ws.range("G4").value = summary
    # Next two steps just select range of cells summary covers
    # so their width can be nicely adjusted
    # Need to do this cos haven't explicitly specified cell range
    expCols = ws.range("G4").expand()
    expCols.autofit()

