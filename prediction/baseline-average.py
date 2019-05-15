# baseline PD predictor
# based on average of passing networks in group stage
# for 2014-15 season

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
totalPassesPerTeam = defaultdict(int)
folder = "../data/passing_distributions/2014-15/"

# accumulate averages on first 4 matchdays
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
                totalPassesPerTeam[teamName] += int(weight)
                # print "%s, %s, %s" % (teamName, p_key, weight)

# take average over 4 matchdays
for teamName in allGroupPasses:
    for p_key in allGroupPasses[teamName]:
        allGroupPasses[teamName][p_key] /= 6
# compute loss on remaining matchdays
avgLoss = 0
totalEx = 0

matchday = "r-16"
path = folder + matchday + "/networks/"
for network in os.listdir(path):
    if re.search("-edges", network):
        edgeFile = open(path + network, "r")
        teamName = getTeamNameFromFile(network)

        for line in edgeFile:
            line = line.rstrip().split("\t")
            p1, p2, weight = line
            p_key = p1 + "-" + p2
            avgPasses = allGroupPasses[teamName][p_key]
            loss = (avgPasses - int(weight)) ** 2
            avgLoss += loss
            totalEx += 1
print "Average loss: %f" % (avgLoss / totalEx)

# for round of 16, store which teams made it
# compare with both games to see how accurate
# the average of all group games is

# output score per team

# rpath = "r-16/networks/"
# r16Teams = []
# scorePerTeam1 = defaultdict(float)
# scorePerTeam2 = defaultdict(float)
#
# for network in os.listdir(folder + rpath):
#     if re.search("-edges", network):
#         totalPasses = 0
#         edgeFile = open(folder + rpath + network, "r")
#         teamName = getTeamNameFromFile(network)
#         scorePerTeam = scorePerTeam1
#         if teamName in r16Teams:
#             scorePerTeam = scorePerTeam2
#         else:
#             r16Teams.append(teamName)
#         for line in edgeFile:
#             line = line.rstrip().split("\t")
#             p1, p2, weight = line
#             p_key = p1 + "-" + p2
#             if p_key in allGroupPasses[teamName]:
#                 # evaluate
#                 est = allGroupPasses[teamName][p_key]
#                 scorePerTeam[teamName] += abs(int(weight) - est)
#             totalPasses += 1
#         # average over passes betwen players
#         scorePerTeam[teamName] /= totalPasses
#
# avgScorePerTeam = defaultdict(float)
# print "Scores for first game in Round of 16:"
# print "-------------------------------------"
# print "Team\t\t\tScore"
# print "----\t\t\t-----"
# for team in scorePerTeam1:
#     avgScorePerTeam[team] += scorePerTeam1[team]
#     print("{0:23}\t{1:0.4f}".format(team, scorePerTeam1[team]))
#
# print ""
# print "Scores for second game in Round of 16:"
# print "-------------------------------------"
# print "Team\t\t\tScore"
# print "----\t\t\t-----"
# for team in scorePerTeam2:
#     avgScorePerTeam[team] += scorePerTeam2[team]
#     print("{0:23}\t{1:0.4f}".format(team, scorePerTeam2[team]))
#
# # calculate average score per team
# for team in avgScorePerTeam:
#     avgScorePerTeam[team] /= 2
#
# print ""
# print "Average Scores for Round of 16:"
# print "-------------------------------------"
# print "Team\t\t\tScore"
# print "----\t\t\t-----"
# for team in avgScorePerTeam:
#     print("{0:23}\t{1:0.4f}".format(team, avgScorePerTeam[team]))
#
# # calculate average score overall
# sumScore = sum([avgScorePerTeam[team] for team in avgScorePerTeam])
# sumScore /= 16
# print ""
# print "Average Score Overall: %.4f" % sumScore
# print "Score indicates the average error over all passes between players for a team."
