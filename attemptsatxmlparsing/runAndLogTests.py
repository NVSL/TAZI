#!/usr/bin/env python

import unittest
import subprocess
import re


class TestBlocklyTranslator(unittest.TestCase):

	def test_Metatest(self):
		self.assertEqual("test", "test")
		self.assertTrue("you" > "me")
		self.assertFalse("yay" == "tests")

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

					

	def test_VarTests(self):
		print("\n=== Running var tests ===")
		subprocess.call(["rm", "-f", "testOutputs/varTestOutput"])
		varFiles = subprocess.Popen(["ls", "tests/varTests/"], stdout=subprocess.PIPE).communicate()[0].split("\n")
		for varFile in varFiles:
			if re.match(r".*\.xml", varFile):
				print("Testing " + varFile + "...")
				proc = subprocess.Popen(["python", "blocklyTranslator.py", "-x", "tests/varTests/" + varFile], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
				stdoutVal, stderrVal = proc.communicate()
				with open("testOutputs/varTestOutput", "a") as outFile:
					outFile.write("=== " + varFile + " ===\n--- stdout ---\n")
					outFile.write(stdoutVal + "\n--------------")
					outFile.write("\n--- stderr ---")
					outFile.write(stderrVal + "\n--------------\n\n")
				varFile = (varFile.split(".")) [0];
				file = "cCode/varFiles/" + varFile + "_cCode.c";
				with open(file, "w") as outFile2:
					outFile2.write(stdoutVal)
					outFile2.close()
					#result = subprocess.Popen(["gcc", "-fsyntax-only", file])
					exitCode = subprocess.call(["gcc", "-fsyntax-only", file])
					#result = subprocess.Popen(["echo $?"]).communicate()[0];
					#result.wait()
					if exitCode != 0:
						print "FAIL TEST"
					else:
						print "PASS TEST"

	def test_mathTests(self):
		print("\n=== Running math tests ===")
		subprocess.call(["rm", "-f", "testOutputs/mathTestOutput"])
		mathFiles = subprocess.Popen(["ls", "tests/MathTests/"], stdout=subprocess.PIPE).communicate()[0].split("\n")
		for mathFile in mathFiles:
			if re.match(r".*\.xml", mathFile):
				print("Testing " + mathFile + "...")
				proc = subprocess.Popen(["python", "blocklyTranslator.py", "-x", "tests/MathTests/" + mathFile], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
				stdoutVal, stderrVal = proc.communicate()
				with open("testOutputs/mathTestOutput", "a") as outFile:
					outFile.write("=== " + mathFile + " ===\n--- stdout ---\n")
					outFile.write(stdoutVal + "\n--------------")
					outFile.write("\n--- stderr ---")
					outFile.write(stderrVal + "\n--------------\n\n")
				mathFile = (mathFile.split(".")) [0];
				file = "cCode/mathFiles/" + varFile + "_cCode.c";
				with open(file, "w") as outFile2:
					outFile2.write(stdoutVal)
					outFile2.close()
					#result = subprocess.Popen(["gcc", "-fsyntax-only", file])
					exitCode = subprocess.call(["gcc", "-fsyntax-only", file])
					#result = subprocess.Popen(["echo $?"]).communicate()[0];
					#result.wait()
					if exitCode != 0:
						print "FAIL TEST"
					else:
						print "PASS TEST"


	def test_logicTests(self):
		print("\n=== Running logic tests ===")
		subprocess.call(["rm", "-f", "testOutputs/logicTestOutput"])
		LogicFiles = subprocess.Popen(["ls", "tests/LogicTests/"], stdout=subprocess.PIPE).communicate()[0].split("\n")
		for logicFile in LogicFiles:
			if re.match(r".*\.xml", logicFile):
				print("Testing " + logicFile + "...")
				proc = subprocess.Popen(["python", "blocklyTranslator.py", "-x", "tests/LogicTests/" + logicFile], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
				stdoutVal, stderrVal = proc.communicate()
				with open("testOutputs/logicTestOutput", "a") as outFile:
					outFile.write("=== " + logicFile + " ===\n--- stdout ---\n")
					outFile.write(stdoutVal + "\n--------------")
					outFile.write("\n--- stderr ---")
					outFile.write(stderrVal + "\n--------------\n\n")
				logicFile = (logicFile.split(".")) [0];
				file = "cCode/logicFiles/" + logicFile + "_cCode.c";
				with open(file, "w") as outFile2:
					outFile2.write(stdoutVal)
					outFile2.close();
					#result = subprocess.Popen(["gcc", "-fsyntax-only", file])
					exitCode = subprocess.call(["gcc", "-fsyntax-only", file])
					#stdout=subprocess.PIPE, stderr=subprocess.PIPE)
					#result = subprocess.Popen(["echo $?"]).communicate()[0];
					#result.wait()
					if exitCode != 0:
						print "FAIL TEST"
					else:
						print "PASS TEST"


if __name__ == "__main__":
	subprocess.call(["mkdir", "testOutputs"])
	unittest.main()
