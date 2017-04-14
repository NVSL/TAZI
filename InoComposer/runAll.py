import subprocess
import re
import sys
from InoComposer import *
import xml.etree.ElementTree as ETree

def verifyOutput(testFile, outFile, gspecFile):
    global failedTests
    global passedTests
    #proc = subprocess.Popen(["python", "InoComposer.py", "-g", gspecFile, "-x", testFile], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    #stdoutVal, stderrVal = proc.communicate()
    api_gspec = ETree.parse(gspecFile).getroot()
    print( "Testing: ", testFile)
    xml = open(testFile).read()
    composer = InoComposer(api_gspec, xml,"test")
    fullInoFile = composer.get_ino();
    with open(outFile, "w+") as output:
        output.write(fullInoFile)
        print (fullInoFile)
        result = subprocess.call("arduino_debug.exe --verify --verbose-build .\\" + outFile )
    if (result == 0):
        passedTests = passedTests + 1
        print ("ok")
    else:
        failedTests = failedTests + 1
        print ("FAIL")

def runTest(test):
    fullTest = os.path.join("RobotTests", test)
    gspecFile = os.path.join(fullTest, test + ".api.gspec")
    outFile = os.path.join(fullTest, test + ".ino")
    #os.makedirs(fullTest)
    testFiles = os.listdir( os.path.join(fullTest, "xml" ) )
    #testFiles = subprocess.Popen(["ls", fullTest + "/xml"], stdout=subprocess.PIPE).communicate()[0].split("\n")
    for testFile in testFiles:
        #run the composer if it is an xml file
        sketch = os.path.join(fullTest, "xml", testFile )
        if re.match(r".*\.xml", testFile):
            verifyOutput(sketch, outFile, gspecFile)



###################MAIN#################################

global failedTests
global passedTests
failedTests = 0
passedTests = 0

#list that houses all the robots with gspecs to be tested
testList = ["Chase"]
 
#actually running the tests for each robot
for test in testList:
	print("RUNNING TEST FOR " + test) 
	runTest(test)

print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
print ("RESULTS: ")
total = failedTests + passedTests
print ("Total Tests: " + str(total))
print ("Passed Tests: " + str(passedTests))
print ("Failed Tessts: " + str(failedTests))
print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")


