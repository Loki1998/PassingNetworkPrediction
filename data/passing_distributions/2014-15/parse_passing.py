# Jade Huang
# jade.huang@stanford.edu
# Parse passing distributions (PD)
# Assumes PD is in .csv format
# usage: python parse_passing.py -i INFILE -o OUTFILE
#        where INFILE is a .csv file with passing distributions
#        OUTFILE will be the prefix for two edge/node lists
#        (one per team)
#
# Parses passing distributions into
#   edge files (player1  player2  weight)
#   node files (player_num  player_name)
#   team stats files (PC,  PA,  PC%)
#   player stats files (player_num,PC,PA,PC%)

import sys
import re
import argparse
from collections import defaultdict

parser = argparse.ArgumentParser(description='Process some passing \
distributions')
parser.add_argument('-in', '-i', dest='infile', required = True)
parser.add_argument('-out', '-o', dest='outfile', required = True)
parsed_args = parser.parse_args()

infile = open(parsed_args.infile, 'r')
passing_dist = [line for line in infile]

# player number -> player name
num_to_name = defaultdict(str)

# player1 -> player2 = weight
passing_edges = defaultdict(lambda: defaultdict(str))

# player number -> time played
num_to_time = defaultdict(float)

# index in array -> player number
index_to_num = defaultdict(str)

# index in array -> player passing stats
index_to_stats = defaultdict(str)

# player[index] = [stat value, stat value, etc.]
player_stats = defaultdict(list)

# player number -> total passes received
total_passes_received_by_player = defaultdict(float)

# stat index -> total stats
total_passes_received_by_stats = defaultdict(str)
pass_compl = 0
pass_attem = 0
pass_perc = 0

#################################################
# get_start_end_index(i, j, lines)
#
#   i: starting index to look at in lines
#   j: ending index to look at in lines
#   lines: array of lines of passing distributions
#
#   returns start: index of "From,,TP..."
#           end: index of "Total passes received..."
#################################################
def get_start_end_index(i, j, lines):
    start = 0
    end = 0
    for index, line in enumerate(lines[i:j]):
        if "From" in line:
            start = index
        elif "Total passes received" in line:
            end = index
            break
    return (start + i, end + 1 + i)

#################################################
# init()
#
#   initializes data structures for a team
#################################################
def init():
    global num_to_name
    global passing_edges
    global num_to_time
    global index_to_num
    global index_to_stats
    global player_stats
    global total_passes_received_by_player
    global total_passes_received_by_stats

    num_to_name = defaultdict(str)
    passing_edges = defaultdict(lambda: defaultdict(str))
    num_to_time = defaultdict(float)
    index_to_num = defaultdict(str)
    index_to_stats = defaultdict(str)
    player_stats = defaultdict(list)
    total_passes_received_by_player = defaultdict(float)
    total_passes_received_by_stats = defaultdict(str)

#################################################
# setup(start, end)
#
#   start: starting index in passing distributions
#   end: ending index in passing distributions
#        (will just be start + 1)
#   based on line like "From,,TP,1,2,4,...",
#   stores array index -> player number
#   stores array index -> player stats
#################################################
def setup(start, end):
    # setup
    for line in passing_dist[start:end]:
        # strip off beginning labels
        line = line.rstrip().split(",")[3:]

        # adding more descriptive labels
        line[-9] += "-long"
        line[-8] += "-long"
        line[-7] += "-med"
        line[-6] += "-med"
        line[-5] += "-short"
        line[-4] += "-short"
        line[-3] += "-total"
        line[-2] += "-total"
        line[-1] += "-success"

        # making index -> num/stats dicts
        for index in xrange(len(line) - 9):
            index_to_num[index] = line[index]
        offset = len(line) - 9
        for index in xrange(len(line)-9, len(line)):
            index_to_stats[index-offset] = line[index]

#################################################
# store_edges(start, end)
#
#   start: starting index in passing distributions
#   end: ending index in passing distributions
#
#   based on line like "Yuri Lodygin,1,94'34,,1,10,..",
#   stores player number -> player name
#   stores player stats like time played
#   stores player1 -> player2 edges
#################################################
def store_edges(start, end):
    global pass_compl
    global pass_attem
    global pass_perc
    # store edges
    for line in passing_dist[start:end]:
        split = line.rstrip().split(",")
        if "" == split[len(split)-1]:
            split = split[:-1]
        if "Total passes received" not in split[0]:
            # first store num -> name
            name, num, time = split[0:3]
            if num == '': # in case Excel parsing messed up
                num = re.search('[0-9]+', split[0]).group(0)
            name = re.sub('[0-9]+', "", name)
            num_to_name[num] = name

            # convert time to float
            time = re.sub("\"", "", time)
            if "\'" in time:
                hour, mins = time.split("\'")
            else: # no minutes to parse out
                hour = time
                mins = 0
            hour = float(hour)
            mins = float(mins) / 60
            num_to_time[num] = hour + mins
            split = split[3:]
            if split[len(split) - 1] == '':
                split = split[:-1]
            # print "split is", split

            # store passing edges
            for index in xrange(len(split) - 9):
                if split[index] != '' and split[index] != '-':
                    player2 = index_to_num[index]
                    passing_edges[num][player2] = split[index]
                    # print "%s -> %s: %s" % (num, player2, split[index])

            # store player stats
            player_stats[num] = split[len(split) - 9:]
            # print "player_stats[%s] = "% num, split[14:]
        else:
            # players
            # total_passes = split[3:-9]
            # for index in xrange(len(index_to_num)):
            #     player = index_to_num[index]
            #     total_passes_received_by_player[player] = total_passes[index]
                # print "%s -> %s" % (player, total_passes[index])

            # stats
            total_stats = split[-9:]
            # pre-process
            total_stats_processed = []
            for stat in total_stats:
                if " " in stat:
                    # split
                    stat = stat.split()
                    total_stats_processed += stat
                elif len(stat) == 0:
                    # remove empty spots
                    continue
                elif "%" in stat:
                    stat = stat[:-1]
                    stat = "0." + stat
                    total_stats_processed.append(stat)
                else:
                    total_stats_processed.append(stat)
            # TODO JADE
            print total_stats_processed
            pass_compl = total_stats_processed[-3]
            pass_attem = total_stats_processed[-2]
            pass_perc = total_stats_processed[-1]
            print "pass vol: %s, pass perc: %s" % (pass_attem, pass_perc)

            offset = len(split) - 9
            for index in xrange(len(total_stats_processed)):
                total_passes_received_by_stats[index+offset] = total_stats_processed[index]
            print total_passes_received_by_stats

#################################################
# get_team_names()
#
#   get team1 and team2 names
#   replace spaces in team names with "_"
#################################################
def get_team_names():
    # get team names
    teams_orig = passing_dist[3].rstrip().split(",")
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
# print_edges(team)
#
#   team: team for print edges for
#################################################
def print_edges(team):
    outfile = open(parsed_args.outfile + "-" + team + "-edges", 'w')
    # print edges
    for player1 in passing_edges:
        for player2 in passing_edges[player1]:
            outfile.write("%s\t%s\t%s\n" % (player1, player2, \
                    passing_edges[player1][player2]))

#################################################
# print_nodes(team)
#
#   team: team for print nodes for
#################################################
def print_nodes(team):
    num_name_outfile = open(parsed_args.outfile + "-" + team + "-nodes", 'w')
    for num in num_to_name:
        num_name_outfile.write("%s\t%s\n" % (num, num_to_name[num]))

#################################################
# print_player_stats(team)
#
#   team: team for print player stats for
#################################################
def print_player_stats(team):
    sys.stderr.write("printing player stats...\n")
    player_stats_outfile = open(parsed_args.outfile + "-" + team + "-players", 'w')
    line = ""
    for player in player_stats:
        line += "%s," % player
        # only interested in last three values: total PC, PA, % PC

        # for i in xrange(len(player_stats[player])):
        p_stats = player_stats[player][-3:]
        print "p_stats are", p_stats
        for i in xrange(3):
            line += "%s," % (p_stats[i])
        line = line[:-1] # get rid of last comma
        line += "\n"
    # print line
    player_stats_outfile.write(line)
#################################################
# print_team_stats(team)
#
#   team: team for print player stats for
#################################################
def print_team_stats(team):
    sys.stderr.write("printing team stats...\n")
    team_stats_outfile = open(parsed_args.outfile + "-" + team + "-team", 'w')
    line = ""
    # volume = total_passes_received_by_stats[24]
    # perc = total_passes_received_by_stats[25]
    team_stats_outfile.write(str(pass_compl) + ", " + str(pass_attem) + ", " + str(pass_perc))
    # for stat in total_stats_processed:
    #     line += "%s," % player
    #     for i in xrange(len(player_stats[player])):
    #         line += "%s:%s," % (i, player_stats[player][i])
    #     line = line[:-1] # get rid of last comma
    #     line += "\n"
    # # print line
    # player_stats_outfile.write(line)

#################################################
# print_player_feature_stats()
#
#   team: team for print player stats for
#################################################
def print_player_feature_stats(teams):
    player_feature_stats_outfile = open(parsed_args.outfile + "-" + teams +
            "-players-features", 'w')
    # line = ""
    for index in index_to_stats:
        player_feature_stats_outfile.write("%s\t%s\n" % (index,
            index_to_stats[index]))

#################################################
# prep(start, end)
#
#   start: starting index in passing distribution
#   end: ending index in passing distribution
#################################################
def prep(start, end):
    init()
    setup(start, start + 1)
    store_edges(start+1, end)

team1, team2 = get_team_names()

sys.stderr.write("teams are: " + team1 + " and " + team2 + "\n")
# print player stat feature num -> feature name
# team 1
start1, end1 = get_start_end_index(0, len(passing_dist), passing_dist)
prep(start1, end1)
print_team_stats(team1)
print_player_feature_stats(team1+"+" + team2)
print_edges(team1)
print_nodes(team1)
print_player_stats(team1)

# team 2
start2, end2 = get_start_end_index(end1, len(passing_dist), passing_dist)
prep(start2, end2)
print_team_stats(team2)
print_edges(team2)
print_nodes(team2)
print_player_stats(team2)
