import sys
counter = 1
team1 = {}
team2 = {}

lines = filter(None, (line.rstrip() for line in sys.stdin))
for line in lines:
	if line:
		value1, value2 = line.rstrip().split()
		team1[counter] = value1
		team2[counter] = value2
		counter += 1

line =  "1, "
for key in team1:
	if team1[key] != "0":
		if "%" in team1[key]:
			per = team1[key][:-1]
			team1[key] = "0." + per
		line += str(key) + ":" + str(team1[key]) + ", "
line = line[:-2]
sys.stdout.write(line + "\n")

line =  "2, "
for key in team2:
	 if team2[key] != "0":
	 	if "%" in team1[key]:
			per = team1[key][:-1]
			team1[key] = "0." + per
		line += str(key) + ":" + str(team2[key]) + ", "
line = line[:-2]
sys.stdout.write(line + "\n")




