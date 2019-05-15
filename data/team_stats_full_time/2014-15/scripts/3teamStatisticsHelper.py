import sys
counter = 1
team1 = {}
team2 = {}
team3 = {}
teamList = [team1, team2, team3]
lines = filter(None, (line.rstrip() for line in sys.stdin))

for line in lines:
	# sys.stderr.write("line: " + line)
	if line:
		value1, value2, value3 = line.rstrip().split(None, 2)
		team1[counter] = value1
		team2[counter] = value2
		team3[counter] = value3
		counter += 1

for i in xrange(len(teamList)):
	line = "%s, " % (i+1)
	for key in teamList[i]:
		if teamList[i][key] != "0":
			if "%" in teamList[i][key]:
				per = teamList[i][key][:-1]
				teamList[i][key] = "0." + per
			line += str(key) + ":" + str(teamList[i][key]) + ", "
	line = line[:-2]
	print line




