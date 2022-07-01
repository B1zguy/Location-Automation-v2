# Just prints a value on each line
for cell in ws.range('A1:F4'):
    print(cell.value)

# Colouring cells
for cell in Range('A1:B2'):
    if cell.value < 2:
        cell.color = (255, 0, 0)
#ws.range("A2").api.Interior.ColordIndex.set(3)
ws.range("A2").color = (123,123,123) # works

# Captures from Excel as list array
print('from excel:')
t = ws.range('A1:B10').value
pprint(t)

# Print particular cells from dataframne
#print(type(gs.at[0, 'Start']))
ta = fromTa.at[0, 'Start']
print('ta ####', ta)
# Print particular cells from list array
ex = t[1][0]
print('\n', 'ex', ex)
#print(type(t[1][0]))
print(type(ex))

print(fromEx.dt.to_pydatetime())