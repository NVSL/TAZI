#!/usr/bin/env python

import subprocess
import re
import sys


def setUp():
	failedTests = []

def tearDown():
	# assertEqual([], failedTests)
	print(failedTests)

def helper(file, testDir, outputFile, cDir):
	global total
	total += 1
	sys.stdout.write("Translating " + file + "...")
	proc = subprocess.Popen(["python", "blocklyTranslator.py", "-x", testDir + file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	stdoutVal, stderrVal = proc.communicate()

	with open(outputFile, "a") as outFile:
		outFile.write("=== " + file + " ===\n--- stdout ---\n")
		outFile.write(stdoutVal + "\n--------------")
		outFile.write("\n--- stderr ---")
		outFile.write(stderrVal + "\n--------------\n\n")

	# Check if there is any stderr output
	if (stderrVal == ""):
		print("ok")
	else:
		failedTests.append(file + " translated with error")
		print("FAIL")
		return

	filename = (file.split(".")) [0];
	cfile = cDir + filename + "_cCode.c";
	sys.stdout.write("Compiling " + cfile + "...")
	with open(cfile, "w") as outFile2:
		outFile2.write(stdoutVal)
		outFile2.close();
		exitCode = subprocess.call(["gcc", "-fsyntax-only", cfile])
		# Check that exit code is 0
		if (exitCode == 0):
			print("ok")
			global passed
			passed += 1
		else:
			failedTests.append(file + " did not pass C++ syntax check")
			print("FAIL")

def test_varTests():
	print("\n=== Running var tests ===")
	subprocess.call(["rm", "-f", "testOutputs/varTestOutput"])
	subprocess.call(["mkdir", "cCode/varFiles/"])
	varFiles = subprocess.Popen(["ls", "tests/varTests/"], stdout=subprocess.PIPE).communicate()[0].split("\n")
	for varFile in varFiles:
		if re.match(r".*\.xml", varFile):
			helper(varFile, "tests/varTests/", "testOutputs/varTestOutput", "cCode/varFiles/")

def test_mathTests():
	print("\n=== Running math tests ===")
	subprocess.call(["rm", "-f", "testOutputs/mathTestOutput"])
	subprocess.call(["mkdir", "cCode/mathFiles/"])
	mathFiles = subprocess.Popen(["ls", "tests/MathTests/"], stdout=subprocess.PIPE).communicate()[0].split("\n")
	for mathFile in mathFiles:
		if re.match(r".*\.xml", mathFile):
			helper(mathFile, "tests/MathTests/", "testOutputs/mathTestOutput", "cCode/mathFiles/")


def test_logicTests():
	print("\n=== Running logic tests ===")
	subprocess.call(["rm", "-f", "testOutputs/logicTestOutput"])
	subprocess.call(["mkdir", "cCode/logicFiles/"])
	LogicFiles = subprocess.Popen(["ls", "tests/LogicTests/"], stdout=subprocess.PIPE).communicate()[0].split("\n")
	for logicFile in LogicFiles:
		if re.match(r".*\.xml", logicFile):
			helper(logicFile, "tests/LogicTests/", "testOutputs/logicTestOutput", "cCode/logicFiles/")

def test_loopTests():
	print("\n=== Running loop tests ===")
	subprocess.call(["rm", "-f", "testOutputs/loopTestOutput"])
	subprocess.call(["mkdir", "cCode/loopFiles/"])
	LoopFiles = subprocess.Popen(["ls", "tests/loopTests/"], stdout=subprocess.PIPE).communicate()[0].split("\n")
	for loopFile in LoopFiles:
		if re.match(r".*\.xml", loopFile):
			helper(loopFile, "tests/loopTests/", "testOutputs/loopTestOutput", "cCode/loopFiles/")

def test_randomTests():
	print("\n=== Running random tests ===")
	subprocess.call(["rm", "-f", "testOutputs/randomTestOutput"])
	subprocess.call(["mkdir", "cCode/randomFiles/"])
	RandomFiles = subprocess.Popen(["ls", "tests/randomTests/"], stdout=subprocess.PIPE).communicate()[0].split("\n")
	for randomFile in RandomFiles:
		if re.match(r".*\.xml", randomFile):
			helper(randomFile, "tests/randomTests/", "testOutputs/randomTestOutput", "cCode/randomFiles/")

def test_customTests():
	print("\n=== Running custom tests ===")
	subprocess.call(["rm", "-f", "testOutputs/customTestOutput"])
	subprocess.call(["mkdir", "cCode/customFiles/"])
	CustomFiles = subprocess.Popen(["ls", "tests/customTests/"], stdout=subprocess.PIPE).communicate()[0].split("\n")
	for customFile in CustomFiles:
		if re.match(r".*\.xml", customFile):
			helper(customFile, "tests/customTests/", "testOutputs/customTestOutput", "cCode/customFiles/")

def runTest(func):
	setUp()
	func()
	tearDown()


#########################################
############## Actual MAIN ##############
#########################################

# Get rid of old things first and make some new files
subprocess.call(["mkdir", "testOutputs"])
subprocess.call(["rm", "-rf", "cCode"])
subprocess.call(["mkdir", "cCode"])

# All tests that will need to be run
tests = [testClass.test_varTests, testClass.test_mathTests, testClass.test_logicTests, testClass.test_loopTests, testClass.test_randomTests, testClass.test_customTests]

# 
global total
global passed
total = 0
passed = 0


for testFunction in tests:
	testClass.runTest(testFunction)

print("\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n")
print("Ran " + str(total) + " tests.\n")
print(str(passed) + " tests passed.\n")
print(str(total - passed) + " tests failed.")
if (total - passed > 0):
	print("FIX THEM, YOU LAZY BUM.")
print("\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n")