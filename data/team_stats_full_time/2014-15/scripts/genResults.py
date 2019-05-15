import sys
import subprocess

directory = "../data/2014354"
filename = "2014354_ts.txt"

firstHalf = "firsthalf.txt"
secondHalf = "secondhalf.txt"
total = "total.txt"
ssnavg = "ssnavg.txt"
ssnhigh = "ssnhigh.txt" 

f = open(filename, 'w')

def run(helper, f):
	p = subprocess.Popen(["python", helper], \
		stdin=open(directory + "/" + f, "r"), \
		stdout=open(filename, "a"))
	p.wait()

with open(filename, "a")as f:
	sys.stderr.write("first half\n")
	f.write("# first half\n")
	f.write("# team1, team2\n")
run("2teamStatisticsHelper.py", firstHalf)

with open(filename, "a")as f:
	sys.stderr.write("second half\n")
	f.write("\n# second half\n")
	f.write("# team1, team2\n")
run("2teamStatisticsHelper.py", secondHalf)

with open(filename, "a") as f:
	sys.stderr.write("total\n")
	f.write("\n# total\n")
	f.write("# team1, team2\n")
run("2teamStatisticsHelper.py", total)

with open(filename, "a") as f:
	sys.stderr.write("ssn avg\n")
	f.write("\n# season average\n")
	f.write("# team1, team2, all\n")
run("3teamStatisticsHelper.py", ssnavg)

with open(filename, "a") as f:
	sys.stderr.write("ssn high\n")
	f.write("\n# season high\n")
	f.write("# team1, team2, all\n")
run("3teamStatisticsHelper.py", ssnhigh)