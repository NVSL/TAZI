# TAZI
A visual based programming environment for Gadgetron

## Dependencies
Clang http://clang.llvm.org

A working Gadgetron build (Jet Components, GadgetMaker2)

## Structure

| Folder | Description | Status
| --- | --- | ---
| BlocksToCpp|  Contains scripts required to translate Blockly blocks to Arduino code | Needs refactoring
| GCGF| Contains scripts to generate Blockly IDE, Blocks, and Arduino code | Needs refactoring
| Server | Contains scripts to run the TAZI web server and compile/run code | Needs refactoring
| Proposal | Contains our LaTeX files that we used to propose this project | :D

## How to run
The current code is configured to work within the Gadgetron project. Running 'make' in the subdirectories will prepare the environments. 
Currently running 'make' at the top level will prepare the server to run locally. Running 'make run' inside the server directory will start the server on your local machine