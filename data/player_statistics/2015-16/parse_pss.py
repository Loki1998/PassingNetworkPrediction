# This program parses out player summary statistics
# find lines separating teams, which look like M,G,T, etc.
# assign feature number to each feature M,G,T,etc.
# parse through each player, store, and print in format
# player number, featurenum:featurevalue, featurenum:featurevalue

import glob
import re

csv_files = glob.glob("*.csv")



#################################################
# get_team_names()
#
#   get team1 and team2 names
#   replace spaces in team names with "_"
#################################################
def get_team_names(pss):
    # get team names
    teams_orig = pss[3].rstrip().split(",")
    teams = []
    for t in teams_orig:
        if t != "": teams.append(t)
    team1 = teams[0]
    team2 = teams[2]
    # replace spaces with _
    team1 = re.sub(" ", "_", team1)
    team2 = re.sub(" ", "_", team2)
    return (team1, team2)

#################################################
# get_start_end_index(i, j, lines)
#
#   i: starting index to look at in lines (inclusive)
#   j: ending index to look at in lines (exclusive)
#   lines: array of lines of pss
#
#   returns start: index of "M,G,T,..."
#           end: index of next "M,G,T,..."
#################################################
def get_start_end_index(i, j, lines):
    start = 0
    end = 0
    for index, line in enumerate(lines[i:j]):
		if "M,G,T" in line:
			if start == 0:
				start = index
			else:
				end = index
				return (start + i, end + i)
		if "M,Minutes played" in line:
			end = index
			return (start + i, end + i)

# print csv_files


def print_player_line(start, end, rev, outfile):

	for i in xrange(start + 1, end):
		line = pss[i]
		# get rid of leading commas
		line = re.sub("^,*","", line)

		stats = line.rstrip().split(",")
		if rev: # for team2, move name & number to the front
			stats =  [stats[-1]] + [stats[-2]] + stats[:-2]
		
		# index 0 = player name
		# index 1 = player number
		# index 2-13 = features
		name = stats[0]
		num = stats[1]
		player_line = num +  ","
		if len(stats) > 2:
			time = stats[2]
			
			time = re.sub("\"", "", time)
			if time != '':
				if "\'" in time:
					hour, mins = time.split("\'")
				else: # no minutes to parse out
					hour = time
					mins = 0
				hour = float(hour)
				mins = float(mins) / 60
				time = hour + mins
			  	player_line += "1:" + str(time) + ","
		offset = 3
		for j in xrange(offset, len(stats)):
			if stats[j] != "":
				player_line += "%s:%s," % (j - 1, stats[j])
		player_line = player_line[:-1] # get rid of extra comma
		outfile.write(player_line + "\n")

for csv in csv_files:
	pss = [line for line in open(csv, 'r')]
	prefix = re.sub(".csv", "", csv)
	# get team names
	team1, team2 =  get_team_names(pss)
	team1_outfile = open(prefix + "-" + team1, 'w+')
	team2_outfile = open(prefix + "-" + team2, 'w+')


	# team 1
	start, end =  get_start_end_index(0, len(pss), pss)
	print_player_line(start, end, False, team1_outfile)

	# team 2
	start2, end2 = get_start_end_index(end, len(pss), pss)
	print_player_line(start2, end2, True, team2_outfile)

	label_line = pss[start]

	# get rid of leading & trailing commas
	label_line = re.sub("^,*","", label_line)
	label_line = re.sub(",*$","", label_line)

	# make array of feature num -> feature name as String
	labels = label_line.rstrip().split(",")
	feature_outfile = open(prefix + "-" + "features", 'w+')
	for i, label in enumerate(labels):
		feature_outfile.write("%s\t%s\n" % (i + 1, label))


# TODO do for all csv in directory
# for csv_file in csv_files:
