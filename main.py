import tanda
import log
import click

# sourceFile: str = 'new-car-trips-simple-export.csv'
# destBook: str = 'location-automation-compilation.xlsx'
#from pygments.lexer import default

@click.command()
@click.argument('csv_source', type=click.Path(exists=True)) # "The CSV from the car logger"
@click.argument('sheet_destination', type=click.Path(exists=True)) # "The spreadsheet to output on"
@click.argument('start_date', default='2021-07-01')
@click.argument('end_date', default='2022-06-30')
def locauto(csv_source, sheet_destination, start_date, end_date):
    """
    \b
    Location Automation
    \t Highlight and calculate work-related travel.
    \n
    \b
    [START_DATE]: \t Defaults to 2021-07-01
    [END_DATE]: \t Defaults to 2022-06-30

    \n
    Files must exist, for now.
    """
        ## Step 1 ##

    # Digests and processes raw log data from car
    click.echo('Processing car log...')
    ProcessedLog = log.LoadnClean(csv=csv_source) # --> dataframe

    # Fetches and processes timesheet data from Tanda
    click.echo('Processing timesheets ...')
    ProcessedTime = tanda.get_Shifts(dates=[start_date, end_date]) # --> List Array

        ## Step 2 ##
    # List array where each list (a shift) contains rows that match logs in Excel
    click.echo('Matching timesheets and car logs ...')
    matchesWrite = log.FindMatches(shifts=ProcessedTime, log=ProcessedLog)
    # Calculates Work, Personal & Total distances travelled
    click.echo('Calculate odomoter readings ...')
    oDomCals = log.Travels(data=ProcessedLog, indexes=matchesWrite)
    # ^^^ Calculations based on odometer-like readings

        ## Step 3 ##
    # Write all data to log spreadsheet!
    click.echo('Writing data to final spreadsheet!')
    log.ExcelInject(
        highlights=matchesWrite,
        summary=oDomCals,
        spreadsheet=sheet_destination,
        log=ProcessedLog
    )

if __name__ == "__main__":
    locauto()

# Default docstrings?
"""

    :param csv:
    :param sheet:
    :return:
    """
