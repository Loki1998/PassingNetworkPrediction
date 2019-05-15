# This script was used to grab all team names who played in the
# 2015-16 season of the Champions League.
# This script assumes there are files named with the following
# convention:
#
#   *teamName-nodes
#
# Originally, these *-nodes files were created by parsing passing
# distributions which were copied from the passing_distributions
# folder.

import glob
import re
from collections import defaultdict

# glob for *-nodes
node_files = glob.glob("*-nodes")
teams = set()

# get team name from nodes
for node_file in node_files:
	m = re.match("^.*-(.*)-nodes$", node_file)
	if m:
		team =  m.group(1)
		team = re.sub("_", " ", team)
		teams.add(team)

all_teams_outfile = open("all-teams", "w+")
for team in teams:
	all_teams_outfile.write(team + "\n")
