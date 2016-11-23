#!/usr/bin/env python

import subprocess
import re
import sys
import os

#global testsDone
#global testsPassed
testsDone = 0
testsPassed = 0

def translate(file):
	global testsPassed
	sys.stderr.write("Translating " + file + "...\n");
	proc = subprocess.Popen(["python", "blocklyTranslator.py", "-x", "testsForOutput/" + file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	stdoutVal, stderrVal = proc.communicate()
	
	outputFile = (file.split(".")) [0]
	outputFile = outputFile + "_cCode.c"
	outputFile = os.path.join("testsForOutputCCode",  outputFile)
	with open(outputFile, "w") as outFile:
		outFile.write(stdoutVal);
		outFile.close();
	#output2File = "testsForOutputCCode/" + "cCode.c"	
	#with open(output2File, "w") as out2File:
	#	out2File.write(stdoutVal);
	#	out2File.close();
	exitCode = subprocess.call(["g++", outputFile])
	if exitCode != 0:
		print("COMPILE ERRORS!!")
		return
	else:
		exitCode2 = subprocess.call(["./a.out"])
		if exitCode == 0:
			testsPassed += 1
		else: 
			print("RUNTIME ERRORS!!")


#Going through all the files
subprocess.call(["mkdir", "testsForOutputCCode/"])
files = subprocess.Popen(["ls", "testsForOutput/"], stdout=subprocess.PIPE).communicate()[0].split("\n")
for f in files:
	if re.match(r".*\.xml", f):
		translate(f);
		testsDone = testsDone + 1

print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
print(str(testsPassed) + " tests compiled out of a total of " + str(testsDone) + " tests. ") 
print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")

