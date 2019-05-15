# Ranks teams by aggregate scores
# and games won during the group stage of
# the 2014-15 season of the Champions League.


from collections import defaultdict

# rank teams by descending aggregate scores
filename = "../data/scores/2014-15_groupStageScores.txt"
scores_file = open(filename, "r")
scores = defaultdict(int)
for line in scores_file:
	team1, score1, score2, team2 = line.rstrip().split(",")
	scores[team1] += int(score1)
	scores[team2] += int(score2)

scores_list = [(scores[team], team) for team in scores]
scores_list = sorted(scores_list, reverse = True)
print ("Sorted by aggregate scores")
print (scores_list)

# rank teams by games won
scores_file = open(filename, "r")
scores = defaultdict(int)
for line in scores_file:
	team1, score1, score2, team2 = line.rstrip().split(",")
	score1 = int(score1)
	score2 = int(score2)
	if score1 > score2:
		scores[team1] += 1
	else:
		scores[team2] += 1

scores_list = [(scores[team], team) for team in scores]
scores_list = sorted(scores_list, reverse = True)
print ("")
print ("Sorted by games won")
print (scores_list)
