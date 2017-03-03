# TAZI
A visual based programming environment for Gadgetron

## How to run

### Server

```
python main.py
```

### Building the IDE

1) Place the gspec (downloaded from robots.gadgetron.build) into the config directory
2) Set the key for "gspec_file" in the config.json file to the path of the gspec
3) Run IDEGenerator.py inside of the BlockGenerator directory

## Dependencies

python 2.7

### Auto Generating Blocks
To build blocks, you'll need to run TAZI on a Unix based environment. Windows 10 Bash/Cygwin are not supported.

Clang http://clang.llvm.org

A working Gadgetron build (Jet Components/GadgetMaker2)

### Generating IDEs

The python package manager

pip https://pypi.python.org/pypi/pip

```
pip install webapp2 webob jinja2
```

## Structure

| Folder | Description | To-Do
| --- | --- | ---
| BlocksToCpp|  Contains scripts required to translate Blockly blocks to Arduino code | -
| BlockGenerator| Contains scripts to generate Blockly IDE, and Block definitions | Needs refactoring
| ServerFiles | Contains scripts to run the TAZI web server | Needs refactoring
| WebStatic | Contains static files such as html, css, and js. Also includes templates | -
| InoComposer | This directory contains the scripts to generate valid Ino files | Make integration tests
| Proposal | Contains our LaTeX files that we used to propose this project | -
| config | Configuration details for server | Move floating parameters violating DRY here
| programs | Stores xml representation of blockly programs as well as compiled code | Rename?


