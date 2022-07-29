# Move date ahead by months
import dateutil.relativedelta as relativedelta
from datetime import datetime
dRange = (
    '2021-03-01', # from
    '2021-05-15'  # to
        )
fmt = '%Y-%m-%d'
tt = datetime.strptime(dRange[0], fmt)
ti = tt + relativedelta.relativedelta(months=+2)

# Getting month range
# Rather, getting last day of month and
# day of the first day of month
import calendar
c = calendar.monthrange(2021, 4)
ic(c)
print(c[0])
print(c[1])