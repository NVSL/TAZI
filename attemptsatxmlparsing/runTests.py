#!/usr/bin/env python

import unittest
import os
import re


class TestBlocklyTranslator(unittest.TestCase):

	def test_Metatest(self):
		self.assertEqual("test", "test")
		self.assertTrue("you" > "me")
		self.assertFalse("yay" == "tests")

	def test_FileXmlToCpp(self):
		xmlFiles = os.popen("ls tests/xml/").read().split("\n")
		for xmlFile in xmlFiles:
			if re.match(r".*\.xml", xmlFile):
				print("Testing " + xmlFile + "...")
				output = os.popen("python blocklyTranslator.py -x tests/xml/" + xmlFile).read()
				print(output)
		varFiles = os.popen("ls tests/varTests/").read().split("\n")
		for varFile in varFiles:
			if re.match(r".*\.xml", varFile):
				print("Testing " + varFile + "...")
				output = os.popen("python blocklyTranslator.py -x tests/varTests/" + varFile).read()
				print(output)
		mathFiles = os.popen("ls tests/MathTests/").read().split("\n")
		for mathFile in mathFiles:
			if re.match(r".*\.xml", mathFile):
				print("Testing " + mathFile + "...")
				output = os.popen("python blocklyTranslator.py -x tests/mathTests/" + mathFile).read()
				print(output)
		LogicFiles = os.popen("ls tests/LogicTests/").read().split("\n")
		for logicFile in LogicFiles:
			if re.match(r".*\.xml", logicFile):
				print("Testing " + logicFile + "...")
				output = os.popen("python blocklyTranslator.py -x tests/logicTests/" + logicFile).read()
				print(output)





if __name__ == "__main__":
	unittest.main()
