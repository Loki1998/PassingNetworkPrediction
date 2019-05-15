# Calculates how often specific players
# pass to each other in the group stage of the
# 2014-15 Champions League season.
#
# usage: python count_spec_passes_feat.py
# output:
#   teamName, player1-player2, totalPasses
#

import os
import re
from collections import defaultdict

def getTeamNameFromFile(network):
    teamName = re.sub("[^-]*-", "", network, count=1)
    teamName = re.sub("-edges", "", teamName)
    teamName = re.sub("_", " ", teamName)
    return teamName

# allGroupPasses[team][p1-p2] = totalPasses
allGroupPasses = defaultdict(lambda: defaultdict(int))
folder = "../data/passing_distributions/2014-15/"

matchdays = ["matchday" + str(i) for i in xrange(1, 7)]
for matchday in matchdays:
    path = folder + matchday + "/networks/"
    for network in os.listdir(path):
        if re.search("-edges", network):
            edgeFile = open(path + network, "r")
            teamName = getTeamNameFromFile(network)

            for line in edgeFile:
                line = line.rstrip().split("\t")
                p1, p2, weight = line
                p_key = p1 + "-" + p2
                allGroupPasses[teamName][p_key] += int(weight)

for teamName in allGroupPasses:
    for p_key in allGroupPasses[teamName]:
        weight = allGroupPasses[teamName][p_key]
        print "%s, %s, %s" % (teamName, p_key, weight)
