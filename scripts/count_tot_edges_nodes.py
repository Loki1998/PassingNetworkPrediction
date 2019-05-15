# This script is used to calculate the
#   total edges
#   total nodes
#   total teams
#   average # nodes per team
#   average # edges per team
#  for the 2014-15 season of [group stage, semifinals]

import os
import re

folder = "../data/passing_distributions/2014-15/"
matchdays = ["matchday" + str(i) for i in xrange(1, 7)]
matchdays.append("r-16")
matchdays.append("q-finals")
matchdays.append("s-finals")

totalEdges = 0
totalNodes = 0
totalTeams = 0

for matchday in matchdays:
	path = folder + matchday + "/networks/"
	for network in os.listdir(path):
		if re.search("-edges", network):
			edgeFile = open(path + network, "r")
			totalEdges += len([line for line in edgeFile])
		elif re.search("-nodes", network):
			nodeFile = open(path + network, "r")
			totalNodes += len([line for line in nodeFile])
			totalTeams += 1

print "Total edges: %d" % totalEdges
print "Total nodes: %d" % totalNodes
print "Total teams: %d" % totalTeams
print "Avg # nodes per team: %f" % (totalNodes / float(totalTeams))
print "Avg # edges per team: %f" % (totalEdges / float(totalTeams))

