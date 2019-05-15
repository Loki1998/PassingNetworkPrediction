import glob

# files = glob.glob("*-edges")
# print files
files = ["2014408_tpd-Juventus-edges"]

for f in files:
	edgeFile = open(f, "r")
	outFile = open(f + ".csv", "w")
	outFile.write("Source;Target;Weight\n")
	edgeLines = [line.rstrip() for line in edgeFile]
	for line in edgeLines:
		print "line is: %s" % line
		s, t, w = line.split("\t")
		outFile.write(s + ";" + t + ";" + w + "\n")

# files = glob.glob("*-nodes")
# print files
# for f in files:
# 	nodeFile = open(f, "r")
# 	outFile = open(f + ".csv", "w")
# 	outFile.write("Id;Label\n")
# 	nodeLines = [line.rstrip() for line in nodeFile]
# 	for line in nodeLines:
# 		print "line is: %s" % line
# 		i, l= line.split("\t")
# 		outFile.write(i + ";" + l + "\n")