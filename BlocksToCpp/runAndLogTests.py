#!/usr/bin/env python

import unittest
import subprocess
import re
import sys


class TestBlocklyTranslator(unittest.TestCase):

#	def test_FileXmlToCpp(self):
#		print("\n=== Running xml file tests ===")
#		subprocess.call(["rm", "-f", "testOutputs/xmlTestOutput"])
#		xmlFiles = subprocess.Popen(["ls", "tests/xml/"], stdout=subprocess.PIPE).communicate()[0].split("\n")
#		for xmlFile in xmlFiles:
#			if re.match(r".*\.xml", xmlFile):
#				print("Testing " + xmlFile + "...")
#				proc = subprocess.Popen(["python", "blocklyTranslator.py", "-x", "tests/xml/" + xmlFile], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#				stdoutVal, stderrVal = proc.communicate()
#				with open("testOutputs/xmlTestOutput", "a") as outFile:
#					outFile.write("=== " + xmlFile + " ===\n--- stdout ---\n")
#					outFile.write(stdoutVal + "\n--------------")
#					outFile.write("\n--- stderr ---")
#					outFile.write(stderrVal + "\n--------------\n\n")
#				file = "cCode/" +  xmlFile + "_cCode.c";
#				with open(file, "w") as outFile2:
#					outFile2.write(stdoutVal)
#					result = subprocess.check_call(["gcc", "-fsyntax-only", file])
#					if result != 0:
#						print "FAIL TEST"
#					if result == 0:
#						print "PASS TEST"


	def setUp(self):
		self.failedTests = []
		self.maxDiff = None

	def tearDown(self):
		self.assertEqual([], self.failedTests)

	def helper(self, file, testDir, outputFile, cDir):
		sys.stdout.write("Translating " + file + "...")
		proc = subprocess.Popen(["python", "blocklyTranslator.py", "-x", testDir + file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		stdoutVal, stderrVal = proc.communicate()

		with open(outputFile, "a") as outFile:
			outFile.write("=== " + file + " ===\n--- stdout ---\n")
			outFile.write(stdoutVal + "\n--------------")
			outFile.write("\n--- stderr ---")
			outFile.write(stderrVal + "\n--------------\n\n")

		# Check if there is any stderr output
		try:
			self.assertEqual(stderrVal, "")
			print("ok")
		except AssertionError, e:
			self.failedTests.append(file + " translated with error")
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
			try:
				self.assertEqual(exitCode, 0)
				print("ok")
			except AssertionError, e:
				self.failedTests.append(file + " did not pass C++ syntax check")
				print("FAIL")

	def test_VarTests(self):
		print("\n=== Running var tests ===")
		subprocess.call(["rm", "-f", "testOutputs/varTestOutput"])
		subprocess.call(["mkdir", "cCode/varFiles/"])
		varFiles = subprocess.Popen(["ls", "tests/varTests/"], stdout=subprocess.PIPE).communicate()[0].split("\n")
		for varFile in varFiles:
			if re.match(r".*\.xml", varFile):
				self.helper(varFile, "tests/varTests/", "testOutputs/varTestOutput", "cCode/varFiles/")

	def test_mathTests(self):
		print("\n=== Running math tests ===")
		subprocess.call(["rm", "-f", "testOutputs/mathTestOutput"])
		subprocess.call(["mkdir", "cCode/mathFiles/"])
		mathFiles = subprocess.Popen(["ls", "tests/MathTests/"], stdout=subprocess.PIPE).communicate()[0].split("\n")
		for mathFile in mathFiles:
			if re.match(r".*\.xml", mathFile):
				self.helper(mathFile, "tests/MathTests/", "testOutputs/mathTestOutput", "cCode/mathFiles/")


	def test_logicTests(self):
		print("\n=== Running logic tests ===")
		subprocess.call(["rm", "-f", "testOutputs/logicTestOutput"])
		subprocess.call(["mkdir", "cCode/logicFiles/"])
		LogicFiles = subprocess.Popen(["ls", "tests/LogicTests/"], stdout=subprocess.PIPE).communicate()[0].split("\n")
		for logicFile in LogicFiles:
			if re.match(r".*\.xml", logicFile):
				self.helper(logicFile, "tests/LogicTests/", "testOutputs/logicTestOutput", "cCode/logicFiles/")
	
	def test_loopTests(self):
		print("\n=== Running loop tests ===")
		subprocess.call(["rm", "-f", "testOutputs/loopTestOutput"])
		subprocess.call(["mkdir", "cCode/loopFiles/"])
		LoopFiles = subprocess.Popen(["ls", "tests/loopTests/"], stdout=subprocess.PIPE).communicate()[0].split("\n")
		for loopFile in LoopFiles:
			if re.match(r".*\.xml", loopFile):
				self.helper(loopFile, "tests/loopTests/", "testOutputs/loopTestOutput", "cCode/loopFiles/")
	
	def test_randomTests(self):
		print("\n=== Running random tests ===")
		subprocess.call(["rm", "-f", "testOutputs/randomTestOutput"])
		subprocess.call(["mkdir", "cCode/randomFiles/"])
		RandomFiles = subprocess.Popen(["ls", "tests/randomTests/"], stdout=subprocess.PIPE).communicate()[0].split("\n")
		for randomFile in RandomFiles:
			if re.match(r".*\.xml", randomFile):
				self.helper(randomFile, "tests/randomTests/", "testOutputs/randomTestOutput", "cCode/randomFiles/")
	
	def test_customTests(self):
		print("\n=== Running custom tests ===")
		subprocess.call(["rm", "-f", "testOutputs/customTestOutput"])
		subprocess.call(["mkdir", "cCode/customFiles/"])
		CustomFiles = subprocess.Popen(["ls", "tests/customTests/"], stdout=subprocess.PIPE).communicate()[0].split("\n")
		for customFile in CustomFiles:
			if re.match(r".*\.xml", customFile):
				self.helper(customFile, "tests/customTests/", "testOutputs/customTestOutput", "cCode/customFiles/")

if __name__ == "__main__":
	subprocess.call(["mkdir", "testOutputs"])
	subprocess.call(["rm", "-rf", "cCode"])
	subprocess.call(["mkdir", "cCode"])
	unittest.main()
