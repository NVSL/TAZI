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


if __name__ == "__main__":
	unittest.main()