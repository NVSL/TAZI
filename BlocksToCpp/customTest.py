#!/usr/bin/env python

import subprocess
import re
import sys
import os


### Translates the file from xml into C++ code using blocklyTranslator ###
def translate(file, testDir, outputFile, cDir):
    global failedTests
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
        # Write the output to the C file
        if not os.path.exists( cDir ): os.makedirs( cDir )
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


### Checks if the output conforms to C++ syntax ###
def checkSyntax(file, testDir, outputFile, cDir):
    global failedTests
    filename = (file.split(".")) [0];
    cfile = cDir + filename + "_cCode.c";
    sys.stdout.write("Compiling " + cfile + "...")
    exitCode = subprocess.call(["g++", "-fsyntax-only", cfile])
    # Check that exit code is 0
    if (exitCode == 0):
        print("ok")
        return True
    else:
        failedTests.append(file + " did not pass C++ syntax check")
        print("FAIL")
        return False


### Compiles the failure list into a string, to be printed later at the end of the test script ###
def compileFailures(typeName, failedList):
    result = "\n-----------------------------------------\n"
    result += "        FAILED TESTS FOR " + typeName + "\n\n"
    if (failedList == []):
        result += "No failed tests.\n"
    else:
        for item in failedList:
            result += item + "\n"
    result += "\n-----------------------------------------\n"
    return result


### Sets up and runs test according to the type name -- this means an entire folder ###
def setupTest(typeName):
    global total
    global failedTranslate
    global failedSyntax
    global failedTests
    failedTests = []
    print("\n=== Running " + typeName + " tests ===")
    slashes = "\\" if os.name == "nt" else "/"
    test_dir = slashes.join(["tests", typeName + "Tests"]) + slashes
    output_dir = slashes.join([ "testOutputs", typeName + "TestOutput"])  
    c_dir = slashes.join( [ "cCode" , typeName + "Files" ]) + slashes
    subprocess.call(["rm", "-f", output_dir ]) 
    subprocess.call(["mkdir", c_dir]) 
    testFiles = subprocess.Popen(["ls", test_dir], stdout=subprocess.PIPE).communicate()[0].split("\n")
    for testFile in testFiles:
        if re.match(r".*\.xml", testFile):
            translateResult = translate(testFile, test_dir, output_dir, c_dir)
            total += 1
            if (translateResult):
                # Passed the translate test, now check C++ syntax
                syntaxResult = checkSyntax(testFile, test_dir, output_dir, c_dir)
                if syntaxResult == False:
                # Failed the syntax test
                    failedSyntax += 1
            else:
                # Failed the translate test
                failedTranslate += 1
    return compileFailures(typeName, failedTests)



#########################################
############## Actual MAIN ##############
#########################################

# Get rid of old things first and make some new files
subprocess.call(["rm", "-rf", "testOutputs"])
subprocess.call(["mkdir", "testOutputs"])
subprocess.call(["mkdir", "cCode"])

# All tests that will need to be run
tests = ["var", 
    "math", 
    "logic", 
    "loop", 
    "random", 
    "function"
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
