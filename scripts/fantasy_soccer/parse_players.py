import xlrd
import os.path
import json

basepath = os.path.dirname(__file__) or "./"
file = os.path.join(basepath, 'player_list.xlsx')
workbook = xlrd.open_workbook(file)

players = {}

counter = 0

for i in range(5):
	sheet = workbook.sheet_by_index(i)

	for row in range(1, sheet.nrows):
		position = sheet.cell(row, 0).value
		
		if position == xlrd.empty_cell.value:
			break

		name = sheet.cell(row, 1).value.strip()
		price = sheet.cell(row, 2).value
		team = sheet.cell(row, 3).value.strip()

		if name.endswith(" New"):
			name = name[:-4]

		if position not in players:
			players[position] = {}
		if team not in players[position]:
			players[position][team] = {}

		players[position][team][name] = price
		counter += 1

print (counter)

with open('player_list.json', 'w') as outfile:
    json.dump(players, outfile)

