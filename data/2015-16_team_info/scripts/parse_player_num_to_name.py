# This script was used to grab all player numbers and player names from
# teams who played in the 2015-16 Champions League.
#
# This script assumes there are files with names of the following
# convention:
#
#   *teamName-nodes
#
# These *-nodes files were created when parsing passing_distributions
# which were copied over from the passing_distributions folder.

# glob for *-nodes
# get team name from nodes
# store player name -> player number
# if see same team name, add new players if any

import glob
import re
from collections import defaultdict

node_files = glob.glob("*-nodes")
prefix = "all_players/player_name_to_num-"
teams = defaultdict(list)

for node_file in node_files:
	m = re.match("^.*-(.*)-nodes$", node_file)
	if m:
		team =  m.group(1)
		team_file = open(node_file, "r")
		for line in team_file:
			num, name = line.rstrip().split("\t")
			if (name, num) not in teams[team]:
				teams[team].append((name, num))

for team in teams:
	team_outfile = open(prefix+team, "w+")
	for player in teams[team]:
		name, num = player
		team_outfile.write("%s,%s\n" % (name, num))
		# player_file = open(prefix+team)
