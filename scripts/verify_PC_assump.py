# This script calculates 
# 1. the percentage times that a team with a larger passing 
#    completion percentage is also the winning team
# 2. the percentage times that a time with a larger passing volume
#    is also the winning team
#
# Used to support inclusion of passing completion
# and passing volume feature

from collections import defaultdict
import os
import re

allScoresFilename = "../scores/2014-15_groupStageScores.txt"
allScores = open(allScoresFilename, "r")
matchesWithScores = [line.rstrip() for line in allScores]
matchIDToScore = defaultdict(str)

numMatches = 0

yesHighPCPerc = 0
yesHighPCVol = 0
matchdays = ["matchday" + str(i) for i in xrange(1, 7)]
folder = "../data/passing_distributions/2014-15/"
matches = defaultdict(str)

def getTeamNameFromNetwork(network):
	teamName = re.sub("[^-]*-", "", network, count=1)
	teamName = re.sub("-edges", "", teamName)
	teamName = re.sub("_", " ", teamName)
	return teamName

def getMatchIDFromFile(network):
	matchID = re.sub("_.*", "", network)
	return matchID

for matchday in matchdays:
	path = folder + matchday + "/networks/"
	for network in os.listdir(path):
		if re.search("-edges", network):
			edgeFile = open(path + network, "r")
			teamName = getTeamNameFromNetwork(network)
			matchID = getMatchIDFromFile(network)

			m = matches[matchID]
			if m == "":
				matches[matchID] = teamName
			else:
				oppTeam = matches[matchID]
				matches[matchID] += "/" + teamName
				print matches[matchID]
				print "numMatches: %d" % (numMatches)
				matchIDToScore[matchID] = matchesWithScores[numMatches]
				print matchIDToScore[matchID]
				team1, score1, score2, team2 = matchIDToScore[matchID].split(", ")

				teamFile = open(path + matchID + "_tpd-" + re.sub(" ", "_", teamName) + "-team", "r")
				for line in teamFile:
					print line
					passC1, passA1, passPerc1 = line.rstrip().split(", ")

				score1 = int(score1)
				score2 = int(score2)
				passC1 = float(passC1)
				passPerc1 = float(passPerc1)

				oppTeamFile = open(path + matchID + "_tpd-" + re.sub(" ", "_", oppTeam) + "-team", "r")
				for line in oppTeamFile:
					passC2, passA2, passPerc2 = line.rstrip().split(", ")
				passC2 = float(passC2)
				passPerc2 = float(passPerc2)
				print "passVol1: %d, passVol2: %d" % (passC1, passC2)
				print "passPerc: %f, passPerc2: %f" % (passPerc1, passPerc2)

				if score1 > score2 and passC1 > passC2:
					yesHighPCVol += 1
				elif score2 > score1 and passC2 > passC1:
					yesHighPCVol += 1

				if score1 > score2 and passPerc1 > passPerc2:
					yesHighPCPerc += 1
				elif score2 > score1 and passPerc2 > passPerc1:
					yesHighPCPerc += 1

				numMatches += 1

print "Perc times larger PC Perc matches with winning team: %s" % ( 1 - yesHighPCVol / float(numMatches))
print "Perc times larger PC Vol matches with winning team: %s" % (1 - yesHighPCPerc / float(numMatches))
