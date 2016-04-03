import subprocess
import re
import sys

def verifyOutput(testFile, outFile, gspecFile):
	proc = subprocess.Popen(["python", "InoComposer.py", gspecFile, testFile], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	stdoutVal, stderrVal = proc.communicate()
	with open(outFile, "w") as output:
		output.write(stdoutVal)
	result = subprocess.call(["arduino", "--verify", outFile])
	if (result == 0):
		print ("ok")
	else:
		print ("FAIL")

def runTest(test):
	fullTest = "RobotTests/" + test
	gspecFile = fullTest + "/" + test + ".api.gspec"
	outFile = fullTest + "/" + test + ".ino"
	testFiles = subprocess.Popen(["ls", fullTest + "/xml"], stdout=subprocess.PIPE).communicate()[0].split("\n")
	for testFile in testFiles:
		#run the composer if it is an xml file
		if re.match(r".*\.xml", testFile):
			verifyOutput(testFile, outFile, gspecFile)
		



###################MAIN#################################		
#list that houses all the robots with gspecs to be tested
testList = ["Chase"]
 
#actually running the tests for each robot
for test in testList:
	print("RUNNING TEST FOR " + test) 
	runTest(test)

