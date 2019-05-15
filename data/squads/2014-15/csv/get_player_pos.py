# Jade Huang
# Get player number, name, and position from squad lists

import glob
import re

csvs = glob.glob("*.csv")
for csv in csvs:
    csv_file = open(csv, "r")
    goalkeepers = []
    defenders = []
    midfielders = []
    forwards = []
    players = []

    for line in csv_file:
        line = line.rstrip().split(",")
        line = line[:2]
        if line[0] == "Goalkeepers":
            players = []
        elif line[0] == "Defenders":
            # store goalkeepers
            goalkeepers = players
            players = []
        elif line[0] == "Midfielders":
            # store defenders
            defenders = players
            players = []
        elif line[0] == "Forwards":
            # store forwards
            midfielders = players
            players = []
        elif line[0] == "Coach":
            forwards = players
            players= []
        else:
        # skip if first line is not a num
            if not line[0].isdigit():
                continue
            players.append(line)

    squad_list = re.sub(".csv", "-squad.csv", csv)
    squad_file = open(squad_list, "w+")
    for gk in goalkeepers:
        squad_file.write(gk[0] + ", " + gk[1]+ ", GK")
        squad_file.write("\n")
    for de in defenders:
        squad_file.write(de[0] + ", " + de[1] + ", DEF")
        squad_file.write("\n")
    for md in midfielders:
        squad_file.write(md[0] + ", " + md[1] + ", MID")
        squad_file.write("\n")
    for fw in forwards:
        squad_file.write(fw[0] + ", " + fw[1] + ", STR")
        squad_file.write("\n")

