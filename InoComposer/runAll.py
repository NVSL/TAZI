import subprocess
import re
import sys
from InoComposer.py import *
import xml.etree.ElementTree as ETree

def verifyOutput(testFile, outFile, gspecFile):
	#proc = subprocess.Popen(["python", "InoComposer.py", "-g", gspecFile, "-x", testFile], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	#stdoutVal, stderrVal = proc.communicate()
	api_gspec = ETree.parse(args.gspec).getroot()
	xml = open(testFile).read()
	composer = InoComposer(api_gspec, xml)
	fullInoFile = compose.get_ino();
	with open(outFile, "w") as output:
		output.write(fullInoFile)
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

