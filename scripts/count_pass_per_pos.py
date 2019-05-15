# Accumulates counts of how often certain positions pass to each other
# based on passing distributions [group stage, semifinals]
# Uses squad lists to map player numbers to positions [GK, MID, DEF, STR]
#
# Outputs to ../data/games_by_pos/perTeam/
#

from collections import defaultdict
import os
import re

# There are multiple printing options
# 
# 1. With 2 human-friendly columns comparing opposing teams side-by-side
# 2. With 1 computer-friendly column listing one team after another
# 
# To toggle, modify printHuman
printHuman = False

teamNumToPos = defaultdict(lambda: defaultdict(str))

squad_dir = "../data/squads/2014-15/squad_list/"

def getTeamNameFromFile(teamFile):
	teamName = re.sub("-squad.*", "", teamFile)
	teamName = re.sub("_", " ", teamName)
	return teamName

def getTeamNameFromNetwork(network):
    teamName = re.sub("[^-]*-", "", network, count=1)
    teamName = re.sub("-edges", "", teamName)
    teamName = re.sub("_", " ", teamName)
    return teamName

# store team & player number to position
for team in os.listdir(squad_dir):
	if re.search("-squad", team):
		path = squad_dir + team
		teamFile = open(squad_dir + team, "r")
		teamName = getTeamNameFromFile(team)
		for player in teamFile:
			num, name, pos = player.rstrip().split(", ")
			teamNumToPos[teamName][num] = pos

# accumulate passes

folder = "../data/passing_distributions/2014-15/"
totalPassesBetweenPos = defaultdict(lambda: defaultdict(int))

matchdays = ["matchday" + str(i) for i in xrange(1, 7)]
matchdays.append("r-16")
matchdays.append("q-finals")
matchdays.append("s-finals")

pos = ["GK", "STR", "DEF", "MID"]
allPosCombos = [pos1 + "-" + pos2 for pos1 in pos for pos2 in pos]



for matchday in matchdays:
    path = folder + matchday + "/networks/"
    lastMatchID = ""
    lastTeamName = ""
    passesBetweenPos = defaultdict(lambda: defaultdict(int))

    for network in os.listdir(path):
        if re.search("-edges", network):
			matchID = re.sub("_.*", "", network)
			edgeFile = open(path + network, "r")
			teamName = getTeamNameFromNetwork(network)

			for line in edgeFile:
				line = line.rstrip().split("\t")
				p1, p2, weight = line
				pos1 = teamNumToPos[teamName][p1]
				pos2 = teamNumToPos[teamName][p2]

				p_key = pos1 + "-" + pos2
				totalPassesBetweenPos[teamName][p_key] += int(weight)
				passesBetweenPos[teamName][p_key] += int(weight)
			
			if printHuman:
				# print the data in a tabular format for each matchID
				if matchID == lastMatchID:
					print "MatchID: %s" % matchID
					print "{0:10}{1:<20}{2:<}".format("Position", lastTeamName, teamName)
					for posPair in allPosCombos:
						print "{0:10}{1:<20}{2:<}".format(posPair, \
							passesBetweenPos[lastTeamName][posPair], \
							passesBetweenPos[teamName][posPair])
					# reset
					passesBetweenPos = defaultdict(lambda: defaultdict(int))
			
			else:
				# print the data in a .csv/parse-able format
				print "MatchID: %s" % matchID
				print "Team: %s" % teamName
				filename = "../data/games_by_pos/perTeam/" + matchID + "-" + re.sub(" ", "_", teamName)
				outfile = open(filename, "w+")

				for posPair in allPosCombos:
					outfile.write("{0}\t{1}\n".format(posPair, \
						passesBetweenPos[teamName][posPair]))
				passesBetweenPos = defaultdict(lambda: defaultdict(int))

			lastMatchID = matchID
			lastTeamName = teamName


# print in nice table format
# # total number of passes
# for teamName in totalPassesBetweenPos:
# 	print "Team: %s" % teamName
# 	print "Position\tNumber of Passes"
# 	for posPair in totalPassesBetweenPos[teamName]:
# 		print "%s\t%s" % (posPair, totalPassesBetweenPos[teamName][posPair])
