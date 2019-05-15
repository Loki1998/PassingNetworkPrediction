import collections, math, random
import classes
import copy
import os
import glob
import re
from collections import defaultdict
import unicodedata
import random

class PredictPD():

	def __init__(self):

		# Entire model uses one set of weights
		self.weights = defaultdict(int)
		self.stepSize = 0.008

		# -------- Initialize directory paths --------
		self.data_dir = "../data/"
		self.folder = self.data_dir + "passing_distributions/2014-15/"
		countAvgFile = self.data_dir + "counts/avg_passes_count.txt"
		squad_dir = self.data_dir + "squads/2014-15/squad_list/"
		rankFile = self.data_dir + "rankings/2013_14_rankings.txt"
		passPerPosDir = self.data_dir + "games_by_pos/perTeam/"
		self.matchdays = ["matchday" + str(i) for i in range(1, 7)]

		# uncomment if want to add round of 16 games to matchdays
		# self.matchdays.append("r-16")

		# # uncomment if want to add quarter final games to matchdays
		# self.matchdays.append("q-finals")
		# --------------------------------------------

		# -------- Initialize features --------
		self.countAvgPassesFeature = classes.CountAvgPassesFeature(countAvgFile)
		self.playerPosFeature = classes.PlayerPositionFeature(squad_dir)
		self.rankFeature = classes.RankingFeature(rankFile)
		self.meanDegreeFeature = classes.MeanDegreeFeature()
		self.betweenFeature = classes.BetweennessFeature()
		self.passComplAttempFeature = classes.PassesComplAttempPerPlayerFeature()
		self.countPassesPosFeature = classes.CountPassesPerPosFeature(passPerPosDir, "group")
		self.passComplAttempTeamFeature = classes.CountPassesComplAttempPerTeamFeature("group")
		# -------------------------------------

		# -------- Initialize data structures --------
		self.matches = defaultdict(str)

		self.totalPassesBetweenPos = defaultdict(lambda: defaultdict(int))
		self.totalPassesBetweenPlayers = defaultdict(lambda: defaultdict(int))
		self.totalPasses = defaultdict(int)

		self.teamNumToPos = defaultdict(lambda: defaultdict(str))
		self.initTeamNumToPos(squad_dir)

		self.passComplPerTeam = defaultdict(int)
		self.passAttemPerTeam = defaultdict(int)
		self.passPercPerTeam = defaultdict(float)

		self.teamStatsByMatch = defaultdict(lambda: defaultdict(list))
		# --------------------------------------------
	
	# Average pairwise error over all players in a team
	# given prediction and gold
	def evaluate(self, features, weight):
		score = self.computeScore(features, self.weights)
		loss = self.computeLoss(features, self.weights, float(weight))
		# print "Score: %f, loss: %f" % (score, loss)
		return (score, loss)

	def computeLoss(self, features, weights, label):
		return (self.computeScore(features, weights) - label)**2

	# score is dot product of features & weights
	def computeScore(self, features, weights):
		score = 0.0
		for v in features:
			score += float(features[v]) * float(weights[v])
		return score

	# returns a vector
	# 2 * (phi(x) dot w - y) * phi(x)
	def computeGradientLoss(self, features, weights, label):
		scalar =  2 * self.computeScore(features, weights) - label
		mult = copy.deepcopy(features)
		for f in mult:
			mult[f] = float(mult[f])
			mult[f] *= scalar
		return mult

	# use SGD to update weights
	def updateWeights(self, features, weights, label):
		grad = self.computeGradientLoss(features, weights, label)
		for w in self.weights:
			self.weights[w] -= self.stepSize * grad[w]

	def getTeamNameFromNetwork(self, network):
		teamName = re.sub("[^-]*-", "", network, count=1)
		teamName = re.sub("-edges", "", teamName)
		teamName = re.sub("_", " ", teamName)
		return teamName

	def getTeamNameFromFile(self, teamFile):
		teamName = re.sub("-squad.*", "", teamFile)
		teamName = re.sub("_", " ", teamName)
		return teamName

	def initTeamNumToPos(self, squad_dir):
		for team in os.listdir(squad_dir):
			if re.search("-squad", team):
				path = squad_dir + team
				teamFile = open(squad_dir + team, "r")
				teamName = self.getTeamNameFromFile(team)
				for player in teamFile:
					num, name, pos = player.rstrip().split(", ")
					self.teamNumToPos[teamName][num] = pos

	def getMatchIDFromFile(self, network):
		matchID = re.sub("_.*", "", network)
		return matchID

	def getOppTeam(self, matchID, teamName):
		team1, team2 = self.matches[matchID].split("/")
		if team1 == teamName:
			return team2
		else: return team1

	def getMatchday(self, matchID):
		matchID = int(matchID)
		if matchID <= 2014322:
			return 0
		elif matchID >=2014323 and matchID <= 2014338:
			return 1
		elif matchID >= 2014339 and matchID <= 2014354:
			return 2
		elif matchID >= 2014355 and matchID <= 2014370:
			return 3
		elif matchID >= 2014371 and matchID <= 2014386:
			return 4
		elif matchID >= 2014387 and matchID <= 2014402:
			return 5
		elif matchID >= 2014403 and matchID <= 2014418:
			return 6
		elif matchID >= 2014419 and matchID <= 2014426:
			return 7
		elif matchID >= 2014427 and matchID <= 2014430:
			return 8

	def featureExtractor(self, teamName, p1, p2, matchID, matchNum, weight):

		avgPasses = self.countAvgPassesFeature.getCount(teamName, p1, p2)

		isSamePos = self.playerPosFeature.isSamePos(teamName, p1, p2)
		isDiffPos = abs(1 - isSamePos)

		oppTeam = self.getOppTeam(matchID, teamName)
		diffInRank = self.rankFeature.isHigherInRank(teamName, oppTeam)

		features = defaultdict(float)
		features["avgPasses"] = avgPasses
		features["isSamePos"] = isSamePos
		# features["isDiffPos"] = isDiffPos
		features["diffInRank"] = diffInRank

		pos1 = self.teamNumToPos[teamName][p1]
		pos2 = self.teamNumToPos[teamName][p2]

		# keep a running total of past passes between positions
		# how about a running average...
		p_key = pos1 + "-" + pos2
		# --- Average passes per position, running average
		
		# self.totalPassesBetweenPos[teamName][p_key] += int(weight)
		# self.totalPasses[teamName] += int(weight)
		# # print "totalPassesBetweenPos[%s][%s] = %s" % (teamName, p_key, self.totalPassesBetweenPos[teamName][p_key])
		# # print "totalPasses[%s] = %s" % (teamName, self.totalPasses[teamName])
		# avgPassesPerPos = self.totalPassesBetweenPos[teamName][p_key] / float(self.totalPasses[teamName])

		# ---
		
		# --- Average passes per position, precomputed
		avgPassesPerPos = self.countPassesPosFeature.getCount(teamName, p_key)
		# ---

		# features["avgPassesPerPos"] = avgPassesPerPos

		
		# --- Running average
		# avgPassCompl = self.passComplPerTeam[teamName] / (matchNum + 1.0)
		# avgPassAttem = self.passAttemPerTeam[teamName] / (matchNum + 1.0)
		# avgPassPerc = self.passPercPerTeam[teamName] / (matchNum + 1.0)
		# avgPassFail = avgPassCompl - avgPassAttem

		# oppAvgPassCompl = self.passComplPerTeam[oppTeam] / (matchNum + 1.0)
		# oppAvgPassAttem = self.passAttemPerTeam[oppTeam] / (matchNum + 1.0)
		# oppAvgPassPerc = self.passPercPerTeam[oppTeam] / (matchNum + 1.0)
		# oppAvgPassFail = oppAvgPassCompl - oppAvgPassAttem

		# --- 

		# --- Precomputed
		avgPassCompl = self.passComplAttempTeamFeature.getPCCount(teamName, matchNum)
		avgPassAttem = self.passComplAttempTeamFeature.getPACount(teamName, matchNum)
		avgPassPerc = self.passComplAttempTeamFeature.getPCPerc(teamName, matchNum)
		avgPassFail = avgPassCompl - avgPassAttem

		oppAvgPassCompl = self.passComplAttempTeamFeature.getPCCount(oppTeam, matchNum)
		oppAvgPassAttem = self.passComplAttempTeamFeature.getPACount(oppTeam, matchNum)
		oppAvgPassPerc = self.passComplAttempTeamFeature.getPCPerc(oppTeam, matchNum)
		oppAvgPassFail = oppAvgPassCompl - oppAvgPassAttem
		# ---
  
		# for feature: won against a similar ranking team
		# 1. define history that we are able to use, i.e. previous games
		matchday = self.getMatchday(matchID)
		history = self.teamPlayedWith[teamName][:matchday]

		if len(history) > 0:
			def computeSim(rank1, rank2):
				return (rank1**2 + rank2**2)**0.5

			# 2. find most similar opponent in terms of rank
			# TODO: similarity could be defined better?
			oppTeamRank = self.rankFeature.getRank(oppTeam)
			simTeam = ""
			simTeamDistance = float('inf')
			rank1 = oppTeamRank
			for team in history:
				rank2 = self.rankFeature.getRank(team)
				sim = computeSim(rank1, rank2)
				if sim < simTeamDistance:
					simTeamDistance = sim
					simTeam = sim
			# 3. find out whether the game was won or lost
			# features["wonAgainstSimTeam"] = self.teamWonAgainst[teamName][matchday]

		# mean degree feature
		features["meanDegree"] = self.meanDegreeFeature.getMeanDegree(matchID, teamName)

		# features["betwPerGameP1"] = self.betweenFeature.getBetweenCentr(matchID, teamName, p1)
		features["betwPerGameP2"] = self.betweenFeature.getBetweenCentr(matchID, teamName, p2)

		# features["avgPassComplPerP1"] = self.passComplAttempFeature.getPC(teamName, p1)
		# features["avgPassComplPerP2"] = self.passComplAttempFeature.getPC(teamName, p2)
		# features["avgPassAttempPerP1"] = self.passComplAttempFeature.getPA(teamName, p1)
		# features["avgPassAttempPerP2"] = self.passComplAttempFeature.getPA(teamName, p2)
		features["avgPCPercPerP1"] = self.passComplAttempFeature.getPCPerc(teamName, p1)
		# features["avgPCPercPerP2"] = self.passComplAttempFeature.getPCPerc(teamName, p2)

		return features

	def initMatches(self):

		# store match data for all games
		# match data including team + opponent team
		allGames = copy.deepcopy(self.matchdays)
		if "r-16" not in allGames:
			allGames.append("r-16")
		if "q-finals" not in allGames:
			allGames.append("q-finals")
		if "s-finals" not in allGames:
			allGames.append("s-finals")
		for matchday in allGames:
			print ("Init matchday: %s" % matchday)
			path = self.folder + matchday + "/networks/"
			for network in os.listdir(path):
				if re.search("-edges", network):
					edgeFile = open(path + network, "r")
					teamName = self.getTeamNameFromNetwork(network)
					matchID = self.getMatchIDFromFile(network)

					m = self.matches[matchID]
					if m == "":
						self.matches[matchID] = teamName
					else:
						self.matches[matchID] += "/" + teamName

		allScoresFilename = "../data/scores/2014-15_allScores.txt"
		allScores = open(allScoresFilename, "r")
		self.matchesWithScores = [line.rstrip() for line in allScores]
		self.teamPlayedWith = defaultdict(list)
		self.teamWonAgainst = defaultdict(list)

		# for every team, store opponents in order by matchday
		for match in self.matchesWithScores:
			team1, score1, score2, team2 = match.split(", ")
			team1Won = 0
			if score1 > score2:
				team1Won = 1

			self.teamPlayedWith[team1].append(team2)
			self.teamPlayedWith[team2].append(team1)
			self.teamWonAgainst[team1].append(team1Won)
			self.teamWonAgainst[team2].append(abs(1 - team1Won))

	def initTeamStats(self):
		for matchday in self.matchdays:
			path = self.folder + matchday + "/networks/"
			# iterate over games
			for network in os.listdir(path):
				if re.search("-team", network):
					teamName = self.getTeamNameFromNetwork(network)
					teamName = re.sub("-team", "", teamName)
					matchID = self.getMatchIDFromFile(network)

					stats_file = open(path + network, "r")
					for line in stats_file:
						stats = line.rstrip().split(", ")
					
					self.teamStatsByMatch[teamName][matchID] = stats

	# Training
	# 	have features calculate numbers based on data
	# 	learn weights for features via supervised data (group stage games) and SGD/EM
	def train(self):
		# iterate over matchdays, predicting passes, performing SGD, etc.

		num_iter = 2
		self.initMatches()
		self.initTeamStats()
		
		pos = ["GK", "STR", "DEF", "MID"]
		allPosCombos = [pos1 + "-" + pos2 for pos1 in pos for pos2 in pos]

		for i in range(num_iter):
			avgLoss = 0
			totalEx = 0
			print ("Iteration %s" % i)
			print ("------------")
			for w in self.weights:
				print ("weights[%s] = %f" % (w, float(self.weights[w])))
			# iterate over matchdays -- hold out on some matchdays
			matchNum = 0

			# # try shuffling matchdays
			# random.shuffle(self.matchdays)

			allGames = []

			for matchday in self.matchdays:
				print ("On " + matchday)
				path = self.folder + matchday + "/networks/"
				# iterate over games
				for network in os.listdir(path):
					if re.search("-edges", network):
						# passesBetweenPos = defaultdict(lambda: defaultdict(int))
						allGames.append((path, network))

			# try shuffling games
			# random.shuffle(allGames)

			for game in allGames:
				path, network = game
				edgeFile = open(path + network, "r")

				teamName = self.getTeamNameFromNetwork(network)
				matchID = self.getMatchIDFromFile(network)
				# print "team: %s" % teamName
				for players in edgeFile:
					p1, p2, weight = players.rstrip().split("\t")
					# print "p1: %s, p2: %s, weight: %f" % (p1, p2, float(weight))

					# teamFile = open(path + matchID + "_tpd-" + re.sub(" ", "_", teamName) + "-team", "r")
					# for line in teamFile:
					# 	stats = line.rstrip().split(", ")
					# self.passComplPerTeam[teamName] += float(stats[0])
					# self.passAttemPerTeam[teamName] += float(stats[1])
					# self.passPercPerTeam[teamName] += float(stats[2])

					features = self.featureExtractor(teamName, p1, p2, matchID, matchNum, weight)

					# for f in features:
					# 	print "features[%s] = %f" % (f, float(features[f]))
					# for w in self.weights:
					# 	print "weights[%s] = %f" % (w, float(self.weights[w]))

					score, loss = self.evaluate(features, weight)
					self.updateWeights(features, self.weights, int(weight))
					avgLoss += loss
					totalEx += 1
				matchNum += 1
			print ("Average loss: %f" % (avgLoss / totalEx))

	# Testing
	#	Predict, then compare with dev/test set (r-16 games)
	def test(self):
		# sum up average error

		print ("Testing")
		print ("-------")
		avgLoss = 0
		totalEx = 0
		matchNum = 0

		# uncomment below if testing on round of 16
		matchday = "r-16"

		# uncomment below if testing on quarter finals
		# matchday = "q-finals"

		# uncommend below if testing on semi-finals
		# matchday = "s-finals"
		print ("On " + matchday)
		path = self.folder + matchday + "/networks/"
		# iterate over games
		for network in os.listdir(path):
			if re.search("-edges", network):
				edgeFile = open(path + network, "r")

				predEdgeFile = open("../predicted/pred-" + network, "w+")

				teamName = self.getTeamNameFromNetwork(network)
				matchID = self.getMatchIDFromFile(network)
				print ("team: %s" % teamName)
				for players in edgeFile:
					p1, p2, weight = players.rstrip().split("\t")
					print ("p1: %s, p2: %s, weight: %f" % (p1, p2, float(weight)))

					features = self.featureExtractor(teamName, p1, p2, matchID, matchNum, weight)

					for f in features:
						print ("features[%s] = %f" % (f, float(features[f])))
					for w in self.weights:
						print ("weights[%s] = %f" % (w, float(self.weights[w])))

					score, loss = self.evaluate(features, weight)

					# print out predicted so can visually compare to actual
					predEdgeFile.write(p1 + "\t" + p2 + "\t" + str(score) + "\n")

					avgLoss += loss
					totalEx += 1
				matchNum += 1

		print ("Average loss: %f" % (avgLoss / totalEx))
		print ("Total average loss: %f" % avgLoss)
		print ("Total examples (passes): %f" % totalEx)

pred = PredictPD()
pred.train()
pred.test()
