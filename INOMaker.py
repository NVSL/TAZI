### Translates the file from xml into C++ code using blocklyTranslator ###
def translate(file, testDir, outputFile, cDir):
	global failedTests
	sys.stdout.write("Translating " + file + "...")
	proc = subprocess.Popen(["python", "BlocksToCpp/blocklyTranslator.py", "-x", testDir + file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	stdoutVal, stderrVal = proc.communicate()

#	with open(outputFile, "a") as outFile:
#		outFile.write("=== " + file + " ===\n--- stdout ---\n")
#		outFile.write(stdoutVal + "\n--------------")
#		outFile.write("\n--- stderr ---")
#		outFile.write(stderrVal + "\n--------------\n\n")

	# Check if there is any stderr output
	if (stderrVal == ""):
		print("ok")
		# Write the output to the C file
		filename = (file.split(".")) [0];
		cfile = cDir + filename + "_cCode.c";
		with open(cfile, "w") as outFile2:
			outFile2.write(stdoutVal)
			outFile2.close();
		return True
	else:
		failedTests.append(file + " translated with error")
		print("FAIL")
		return False






def setupTest(typeName):
	global total
	global failedTranslate
	global failedSyntax
	global failedTests
	failedTests = []

	print("\n=== Running " + typeName + " tests ===")
	subprocess.call(["mkdir", "INOOutputs/" + typeName + "Files/"])
	testFiles = subprocess.Popen(["ls", "BlocksToCpp/tests/" + typeName + "Tests/"], stdout=subprocess.PIPE).communicate()[0].split("\n")
	for testFile in testFiles:
		if re.match(r".*\.xml", testFile):
			translateResult = translate(testFile, "BlocksToCpp/tests/" + typeName + "Tests/", "INOOutputs/" + typeName + "TestOutput", "INOCode/" + typeName + "Files/")
			total += 1
			if (translateResult):
				# Passed the translate test, now check C++ syntax
				syntaxResult = checkSyntax(testFile, "tests/" + typeName + "Tests/", "testOutputs/" + typeName + "TestOutput", "cCode/" + typeName + "Files/")
				if syntaxResult == False:
					# Failed the syntax test
					failedSyntax += 1
			else:
				# Failed the translate test
				failedTranslate += 1

	return compileFailures(typeName, failedTests)




#######################################
#MAIN
#######################################
tests = ["custom"
	]
results = {}

# Stuff to keep track
global total
global failedTranslate
global failedSyntax
total = 0
failedTranslate = 0
failedSyntax = 0

# Actually run the tests and store the resulting failures in dict
for testType in tests:
	result = setupTest(testType)
	results[testType] = result

# Print out the test type failures
for testType in tests:
	print(results[testType])

# General final output
print("\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n")
print("Ran " + str(total) + " tests.\n")
print(str(total - failedTranslate - failedSyntax) + " tests passed.\n")
print(str(failedTranslate + failedSyntax) + " total tests failed.")
if (failedTranslate + failedSyntax > 0):
	print("\nOf failed tests:")
	print("    " + str(failedTranslate) + " failed to translate")
	print("    " + str(failedSyntax) + " failed to pass C++ syntax check")
	print("FIX THEM, YOU LAZY BUM.")

print("\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n")
